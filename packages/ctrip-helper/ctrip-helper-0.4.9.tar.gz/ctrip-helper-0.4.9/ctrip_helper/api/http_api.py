# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     http_api.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import json
import random
from copy import deepcopy
from ctrip_helper.http_client import HttpService
from ctrip_helper.config import url_map, common_headers
from ctrip_helper.utils import gen_sign, generate_random_ipv6_encode, get_dict_lenth, dict_to_jsonstr, to_url_str

"""
# 设置代理 example
proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'https://10.10.1.10:1080',
}
"""


class Api(object):
    __headers = {
        'dnt': '1',
        'referer': 'https://verify.ctrip.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' +
                      'Chrome/102.0.0.0 Safari/537.36'
    }

    def __init__(self):
        self.__domain = url_map.get("domain")
        self.__protocol = url_map.get("protocol")
        self.__http_client = HttpService(self.__domain, self.__protocol)

    def get_city_code(self, headers: dict = None, proxies: dict = None):
        """获取城市编码"""
        city_name, code = [], []
        if headers:
            self.__headers = headers
        r = self.__http_client.send_request(
            method="get", path=url_map.get("city_code"), headers=self.__headers, params=dict(v=str(random.random())),
            proxies=proxies,
        )
        city_s = r.get('data')
        for city in city_s:
            if city == '热门':
                continue
            for key in city:
                try:
                    for k in city_s[city][key]:
                        city_name.append(k['display'])
                        code.append(k['data'])
                except (Exception,):
                    continue
        city_code = dict(zip(city_name, code))

        return city_name, city_code

    def get_international_holiday(self, headers: dict = None, proxies: dict = None) -> dict:
        if headers:
            self.__headers = headers
        return self.__http_client.send_request(
            method="get", path=url_map.get("international_holiday"), headers=self.__headers,
            params=dict(v=str(random.random())),
            proxies=proxies,
        )

    def get_country_code(self, headers: dict = None, proxies: dict = None) -> dict:
        if headers:
            self.__headers = headers
        result = self.__http_client.send_request(
            method="post", path=url_map.get("flight_city"), headers=self.__headers, params=dict(v=str(random.random())),
            proxies=proxies, json={"DataSearchType": 2}
        )
        if result.get("data"):
            data = json.loads(result.get("data"))
            data = {x.get("areaName"): x for x in data}
        else:
            data = dict()
        return data

    def get_internal_airline(self, headers: dict = None, proxies: dict = None) -> dict:
        """获取国内航线"""
        if headers:
            self.__headers = headers
        result = self.__http_client.send_request(
            method="post", path=url_map.get("flight_city"), headers=self.__headers, params=dict(v=str(random.random())),
            proxies=proxies, json={"DataSearchType": 2}
        )
        if result.get("data"):
            data = json.loads(result.get("data"))
        else:
            data = dict()
        return data

    def get_flight_segments(
            self, departure_city_code: str, arrival_city_code: str, departure_date: str, headers: dict = None,
            proxies: dict = None
    ) -> dict:
        if headers:
            self.__headers = headers
        path = "-".join([url_map.get("flight_segments"), departure_city_code.lower(), arrival_city_code.lower()])
        params = {
            "_": 1,
            "depdate": departure_date,  # 起飞时间
            "cabin": "Y_M_S_C_J_F",  # 查询舱位, Y,M:经济舱,S,C:特价舱位,J:商务舱，"C_F"，"Y_S"
            "adult": 1,  # 是否包含成人
            "child": 0,  # 是否包含儿童
            "infant": 0,  # 是否包含婴儿
            "containstax": 1  # 金额是否含税
        }
        result = self.__http_client.send_request(
            method="get", path=path, headers=self.__headers, params=params, proxies=proxies
        )
        if result.get("status") == 0 and result.get("data"):
            data = result.get("data")
        else:
            data = dict()
        return data

    def get_flight_list(
            self, departure_city_code: str, arrival_city_code: str, departure_date: str, headers: dict = None,
            proxies: dict = None, cookie: str = None, token: str = None
    ) -> list:
        flight_segments_result = self.get_flight_segments(
            departure_city_code=departure_city_code, arrival_city_code=arrival_city_code, departure_date=departure_date,
            headers=headers, proxies=proxies
        )
        data = list()
        if flight_segments_result:
            if headers:
                self.__headers = headers
            scope = flight_segments_result.get("scope")
            transaction_id = flight_segments_result.get("transactionID")
            flight_segment = flight_segments_result.get("flightSegments")[0]
            sign = gen_sign(
                departure_date=departure_date, arrival_city_code=arrival_city_code,
                departure_city_code=departure_city_code, transaction_id=transaction_id
            )
            referer = "https://flights.ctrip.com/online/list/oneway-{}-{}?_=1&depdate={}&sortByPrice=true".format(
                departure_city_code.lower(), arrival_city_code.lower(), departure_date
            )
            common_headers_new = deepcopy(common_headers)
            common_headers_new["sign"] = headers.get("sign") if headers else sign
            common_headers_new["scope"] = headers.get("scope") if headers else scope
            common_headers_new["referer"] = headers.get("referer") if headers else referer
            common_headers_new["transactionid"] = headers.get("transactionid") if headers else transaction_id
            if not cookie and not headers:
                arrival_city_id = flight_segment.get("arrivalCityId")
                arrival_city_name = flight_segment.get("arrivalCityName")
                departure_city_id = flight_segment.get("departureCityId")
                departure_city_name = flight_segment.get("departureCityName")
                arrival_city_time_zone = flight_segment.get("arrivalCityTimeZone")
                departure_city_time_zone = flight_segment.get("departureCityTimeZone")
                # ["SZX|深圳(SZX)|30|SZX|480","CGO|郑州(CGO)|559|CGO|480","2024-06-10"]
                quota_str = to_url_str(data='"')
                comma_str = to_url_str(data=',')
                departure_city_encode = '{}{}|{}({})|{}|{}|{}{}{}'.format(
                    quota_str, departure_city_code, to_url_str(data=departure_city_name), departure_city_code,
                    departure_city_id, departure_city_code, departure_city_time_zone, quota_str, comma_str
                )
                arrival_city_encode = '{}{}|{}({})|{}|{}|{}{}{}'.format(
                    quota_str, arrival_city_code, to_url_str(data=arrival_city_name), arrival_city_code,
                    arrival_city_id, arrival_city_code, arrival_city_time_zone, quota_str, comma_str
                )
                data_encode = '{}{}{}'.format(quota_str, departure_date, quota_str)
                search = "[" + "".join([departure_city_encode, arrival_city_encode, data_encode]) + "]"
                cookie = ('UBT_VID=1716362617552.9853FAAvasqr; GUID=09031026416291311476; _RSG=6mq9jgQBNZA7MjC' +
                          'Gs2syWA; _RDG=28c797987f59e226233840389a89d51ba0; _RGUID=a8d72daa-ad27-4c06-a83c-' +
                          'd82d9032d587; nfes_isSupportWebP=1; MKT_CKID=1716642869118.5mwd3.h3jr; _jzqco=%7C%7C%7C%7C' +
                          '1716642869353%7C1.1476965701.1716642869125.1716642869125.1716642869125.1716642869125.' +
                          '1716642869125.0.0.0.1.1; FlightIntl=Search={};'.format(search)
                          + ' _RF1={}; _bfa=1.1716362617552.9853FAAvasqr.'.format(generate_random_ipv6_encode()) +
                          '1.1716862756271.1716862767381.9.2.10320673302')
                common_headers_new["cookie"] = cookie
            if not token and not headers:
                token = ("1001-common-D3kx4bEMPKlUj90jFZjABKctw0pYUSwanwXTw7SInLjUmEQPR71RFPv58jBpWfpEpNiBHiZsy" +
                         "M4ya1E6zjBtJcpW10vQ7jBcWZnvSdjDtEM4K9ZRfGj5YhnjGpJGyTORa6yBFRAUw51jTbvnpWBlYLaRfsW0U" +
                         "jMDYU9wGQYOnwLFeSYb1JpBy3JXbENXJPlrLYlPvFoYgAWnURkMy01ROnwt4jANjQUjo1Rb1yOPjAhWTGinBi" +
                         "f8I07jF3YDgwBfY7FRGkEXqiATjSUETajZOwN0W6aIaJttxlYzLyOPj3hWbFyTdEakvDMJDXj3Mw05RBAysAe" +
                         "ZbvNFyHcWMaJOqeAgEasi0gJQoj7FeP3vHFi6kYabvOpeN7EthiMbjhPyOlvO5vU1Wzbi7ZwcaJL1YAziO8" +
                         "w1LJ7qwtYbbxF7R3bihaymgYcfYoXwUoyfNvtUY56wP4R9DIqZISYgAvocRlcwT1Y8GEHajs4E09i3YaoYUHR" +
                         "lLrO8vFsenUYc9igzYbdwsaYSXjDY9ay3figmW0ae3fEDGjM4W0FEPSe5fjsYstIfmWqlJgor3gKNleD1EFQW" +
                         "tOI9ZYsElYPsyUtKhbEHMRT7vBaYpfWd3eB8Rh7WZbjQqW86JzBYgOrfY65ifkJaXeSmRqt" +
                         "vlzYMnW94eBcRZSWc3EnmWzGyQ3Ea5")
                common_headers_new["token"] = token
            # OW 单程，RT 往返，MT 多程
            flight_segments_result["flightWayEnum"] = "OW"
            # 直飞
            flight_segments_result["directFlight"] = True
            common_headers_new["content-length"] = str(get_dict_lenth(data=flight_segments_result))
            self.__headers.update(common_headers_new)
            result = self.__http_client.send_request(
                method="post", path=url_map.get("flight_list"), headers=self.__headers,
                params=dict(v=str(random.random())), proxies=proxies, data=dict_to_jsonstr(flight_segments_result)
            )
            if result.get("status") == 0 and isinstance(result.get("data"), dict):
                data = result.get("data").get("flightItineraryList") or list()
        return data
