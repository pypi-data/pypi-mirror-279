# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     http_client.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import urllib3
import requests
import typing as t
from ctrip_helper.libs import logger
from ctrip_helper.utils import covert_dict_key_to_lower, get_html_title

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpService(object):
    __time_out = 30
    __domain = None
    __url = None
    __protocol = None
    __headers: dict = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    def __init__(self, domain: str, protocol: str) -> None:
        self.__domain = domain
        self.__protocol = protocol

    def send_request(self, method: str, path: str, params: dict = None, data: dict or str = None, json: dict = None,
                     headers: dict = None, proxies: dict = None) -> t.Any:
        if isinstance(headers, dict):
            self.__headers = headers
        self.__url = "{}://{}{}".format(self.__protocol, self.__domain, path)
        # 发送HTTP请求
        logger.info(
            "尝试发起http请求，url: {}, 方法：{}，请求params参数：{}，请求headers参数：{}，请求data参数：{}，请求json参数：{}".format(
                self.__url,
                method,
                params or "{}",
                self.__headers,
                data or "{}",
                json or "{}",
            )
        )
        return self.__send_http_request(method=method, proxies=proxies, params=params, data=data, json=json)

    def __send_http_request(self, method: str, params: dict = None, data: dict = None, proxies: dict = None,
                            json: dict = None) -> dict:
        # 实际发送HTTP请求的内部方法
        # 使用 requests 库发送请求
        method = method.lower().strip()
        if method in ("get", "post"):
            try:
                if method == "get":
                    response = requests.get(self.__url, params=params, verify=False, timeout=self.__time_out,
                                            headers=self.__headers, proxies=proxies)
                else:
                    response = requests.post(
                        self.__url, params=params, json=json, data=data, verify=False, timeout=self.__time_out,
                        headers=self.__headers, proxies=proxies
                    )
                result = self.__parse_data_response(response=response)
            except Exception as e:
                logger.error("调用url<{}>异常，原因：{}".format(self.__url, str(e)))
                result = dict(code=500, message=str(e), data=dict())
        else:
            result = dict(code=400, message="Unsupported HTTP method: {}".format(method), data=dict())
        return result

    def __parse_data_response(self, response: requests.Response) -> dict:
        # 获取 Content-Type 头信息
        content_type = response.headers.get('Content-Type') or ""
        # 判断返回的内容类型
        if 'application/json' in content_type or 'text/json' in content_type:
            # JSON 类型
            data = covert_dict_key_to_lower(d=response.json())
        elif 'text/plain' in content_type:
            # 纯文本类型
            data = dict(code=response.status_code, message=get_html_title(
                html=response.text), data=response.text)
        else:
            if response.json():
                # JSON 类型
                data = covert_dict_key_to_lower(d=response.json())
            else:
                # 其他类型，默认视为二进制内容
                content = response.content.decode('utf-8')
                data = dict(code=response.status_code,
                            message=get_html_title(html=content), data=content)
        logger.info("调用url: {}的正常返回值为：{}".format(self.__url, data))
        return data
