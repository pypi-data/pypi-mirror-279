#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import time
import json
import requests

from urllib import parse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from up2b.up2b_lib.custom_types import (
    Config,
    ErrorResponse,
    ImageBedType,
    ImageType,
    ImageStream,
    ImagePath,
    ImgtuResponse,
    UploadErrorResponse,
    CompressedFormat,
)
from up2b.up2b_lib.errors import MissingAuth
from up2b.up2b_lib.file import File
from up2b.up2b_lib.http import upload_with_progress_bar
from up2b.up2b_lib.up2b_api import Base
from up2b.up2b_lib.constants import IMAGE_BEDS_NAME, ImageBedCode
from up2b.up2b_lib.log import child_logger

logger = child_logger(__name__)


class Imgtu(Base):
    image_bed_type = ImageBedType.common
    image_bed_code = ImageBedCode.IMGTU
    max_size = 10 * 1024 * 1024
    base_url = "https://imgse.com/"
    __headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:85.0) Gecko/20100101 Firefox/85.0",
    }

    compressed_format: CompressedFormat = CompressedFormat.JPEG

    def __init__(
        self,
        auto_compress: bool = False,
        add_watermark: bool = False,
        ignore_cache: bool = False,
        conf: Optional[Config] = None,
        timeout: Optional[float] = None,
        quiet: bool = False,
    ):
        super().__init__(
            auto_compress, add_watermark, ignore_cache, conf, timeout, quiet
        )

        self.cookie: Optional[str] = None
        self.token: Optional[str] = None
        if self.auth_info:
            self.cookie = self.auth_info["cookie"]
            self.token = self.auth_info["token"]
            self.username = self.auth_info["username"]
            self.__headers["Cookie"] = self.cookie

    def login(self, username: str, password: str) -> bool:
        url = self._url("login")
        auth_token, cookie = self._parse_auth_token()

        if not auth_token or not cookie:
            raise MissingAuth("auth token or cookie is None")

        headers = self.__headers.copy()
        headers["Cookie"] = cookie

        data = {
            "login-subject": username,
            "password": password,
            "auth_token": auth_token,
        }

        resp = requests.post(
            url, headers=headers, data=data, allow_redirects=False, timeout=self.timeout
        )
        if resp.status_code == 301:
            # If there is a KEEPLOGIN field in the cookie,
            # pictures will be uploaded as a normal user
            self.cookie = cookie + "; " + resp.headers["Set-Cookie"].split("; ")[0]

            # If there is no KEEPLOGIN field in the cookie,
            # pictures will be uploaded as a tourist
            # self.cookie = cookie

            auth_info = {
                "token": auth_token,
                "cookie": self.cookie,
                "username": username,
                "password": password,
            }
            self._save_auth_info(auth_info)
            return True

        return False

    def _parse_auth_token(self) -> Tuple[Optional[str], Optional[str]]:
        url = self._url("login")
        resp = requests.get(url, headers=self.__headers, timeout=self.timeout)
        if resp.status_code == 200:
            auth_token = re.search(
                r'PF.obj.config.auth_token = "([a-f0-9]{40})"', resp.text
            )
            if not auth_token:
                return None, None
            resp_set_cookie = resp.headers["Set-Cookie"].split("; ")[0]
            return auth_token.group(1), resp_set_cookie
        else:
            logger.error("response error", status_code=resp.status_code)
            return None, None

    @property
    def headers(self):
        assert self.cookie != None

        headers = self.__headers.copy()
        headers.update(
            {
                "Cookie": self.cookie,
            }
        )
        return headers

    def _update_auth_token(self):
        resp = requests.get(self.base_url, headers=self.headers, timeout=self.timeout)
        auth_token = re.search(
            r'PF.obj.config.auth_token = "([a-f0-9]{40})"', resp.text
        )

        assert auth_token != None

        auth_token = auth_token.group(1)
        if not self.auth_info:
            self.auth_info = {}

        self.auth_info["token"] = self.token = auth_token
        self._save_auth_info(self.auth_info)

    def __upload(
        self, image: ImageType, retries: int = 0
    ) -> Union[str, UploadErrorResponse]:
        url, md5, ok = self._check_cache(image)  # type: ignore

        if ok and not self.ignore_cache:
            return url

        self.check_login()

        image = self._compress_image(image)

        if isinstance(image, Path):
            image = self._add_watermark(image)

        logger.debug("uploading", image_path=image)

        url = self._url("json")
        filename_with_suffix = os.path.basename(str(image))
        filename_without_suffix, suffix = os.path.splitext(filename_with_suffix)
        if isinstance(image, Path):
            if suffix.lower() == ".apng":
                suffix = ".png"
            filename = filename_without_suffix + suffix
        else:
            filename = filename_with_suffix + "." + image.mime_type

        file = File("source", image, filename=filename)

        timestamp = int(time.time() * 1000)

        data = {
            "type": "file",
            "action": "upload",
            "timestamp": str(timestamp),
            "auth_token": self.token,
            "nsfw": "0",
        }

        try:
            if not self.quiet:
                resp = upload_with_progress_bar(
                    url, file, self.timeout, data, self.headers
                )
            else:
                resp = requests.post(
                    url,
                    headers=self.headers,
                    data=data,
                    files=file.to_dict(),
                    timeout=self.timeout,
                )
        except requests.exceptions.ConnectionError as e:
            return UploadErrorResponse(400, str(e), str(image))

        resp.encoding = "utf-8"

        try:
            json_resp = resp.json()
        except json.decoder.JSONDecodeError:
            return UploadErrorResponse(resp.status_code, resp.text, str(image))

        try:
            uploaded_url: str = json_resp["image"]["image"]["url"]
            logger.info(
                "uploaded url",
                target=image,
                url=uploaded_url,
            )

            self.cache.save(
                md5,
                IMAGE_BEDS_NAME[self.image_bed_code],
                uploaded_url,
                self.ignore_cache,
            )

            return uploaded_url
        except KeyError:
            if json_resp["error"]["message"] == "请求被拒绝 (auth_token)":
                if retries >= 3:
                    return UploadErrorResponse(
                        resp.status_code, resp.json()["error"]["message"], str(image)
                    )

                logger.warning(
                    "`auth_token` has expired, the program will try to update `auth_token` automatically, number of retries",
                    retries=retries + 1,
                )
                self._update_auth_token()

                return self.__upload(image, retries + 1)
            else:
                return UploadErrorResponse(
                    resp.status_code, resp.json()["error"]["message"], str(image)
                )

    def upload_image(self, image_path: ImagePath) -> Union[str, UploadErrorResponse]:
        return self.__upload(image_path)

    def upload_image_stream(
        self, image: ImageStream
    ) -> Union[str, UploadErrorResponse]:
        return self.__upload(image)

    def get_all_images(self) -> Union[List[ImgtuResponse], ErrorResponse]:
        self.check_login()

        url = self._url(self.username)

        # 集合去重
        images: Set[Tuple[str, ...]] = set()

        def visit_next_page(url: str):
            resp = requests.get(url, headers=self.__headers, timeout=self.timeout)
            resp.encoding = "utf-8"

            if resp.status_code != 200:
                return ErrorResponse(resp.status_code, resp.text)

            # 只获取默认的公开相册里的图片
            # images_object = re.findall(
            #     r"data-privacy=\"public\" data-object='(.+?)'", resp.text)
            # 获取用户所有图片
            images_object = re.findall(r"data-object='(.+?)'", resp.text)
            images_object = [json.loads(parse.unquote(i)) for i in images_object]
            for image in images_object:
                images.add(
                    (
                        image["url"],
                        image["display_url"],
                        image["id_encoded"],
                        image["width"],
                        image["height"],
                    )
                )

            next_page_url = re.search(
                r'data-pagination="next" href="(.+?)" ><span', resp.text
            )
            if next_page_url:
                next_page_url = next_page_url.group(1)
            else:
                next_page_url = ""

            if next_page_url:
                visit_next_page(next_page_url)

        resp = visit_next_page(url)
        if resp:
            return resp

        result: List[ImgtuResponse] = []

        for item in images:
            result.append(
                ImgtuResponse(
                    item[2],
                    item[0],
                    item[1],
                    int(item[3]),
                    int(item[4]),
                )
            )

        return result

    def delete_image(self, img_id: str, retries: int = 0) -> Optional[ErrorResponse]:
        self.check_login()

        url = self._url("json")
        data = {
            "auth_token": self.token,
            "action": "delete",
            "single": "true",
            "delete": "image",
            "deleting[id]": img_id,
        }
        resp = requests.post(
            url, headers=self.__headers, data=data, timeout=self.timeout
        )
        if resp.status_code == 400:
            if resp.json()["error"]["message"] == "请求被拒绝 (auth_token)":
                if retries >= 3:
                    return ErrorResponse(
                        resp.status_code, resp.json()["error"]["message"]
                    )

                logger.warn(
                    "`auth_token` has expired, the program will try to update `auth_token` automatically, number of retries: %d",
                    retries + 1,
                )
                self._update_auth_token()
                return self.delete_image(img_id, retries + 1)

        if resp.status_code == 200:
            return None

        return ErrorResponse(resp.status_code, resp.json()["error"]["message"])

    def delete_images(
        self, imgs_id: List[str], retries: int = 0
    ) -> Dict[str, ErrorResponse]:
        self.check_login()

        url = self._url("json")
        data = {
            "auth_token": self.token,
            "action": "delete",
            "from": "list",
            "multiple": "true",
            "delete": "images",
            "deleting[ids][]": imgs_id,
        }
        resp = requests.post(
            url, headers=self.__headers, data=data, timeout=self.timeout
        )
        json_resp = resp.json()
        if resp.status_code == 400:
            if json_resp["error"]["message"] == "请求被拒绝 (auth_token)":
                if retries >= 3:
                    # 删除多张图片时如果重试3次仍无法成功响应则退出程序
                    logger.fatal(
                        "authentication information is invalid",
                        error=resp.json()["error"]["message"],
                    )

                logger.warn(
                    "`auth_token` has expired, the program will try to update `auth_token` automatically, number of retries: %d",
                    retries + 1,
                )
                self._update_auth_token()
                return self.delete_images(imgs_id, retries + 1)
            elif json_resp["error"]["code"] == 106:
                # imgtu 只有删除的所有 id 都无效时才会返回这个错误
                # 只要有一个有效 id，就会返回 200
                return {img_id: ErrorResponse(404, "服务器中无此图片") for img_id in imgs_id}

        return {}

    def _url(self, path: str) -> str:
        return self.base_url + path

    def __repr__(self):
        return "imgtu.com"

    @property
    def description(self):
        return "中国大陆访问可能不太稳定"
