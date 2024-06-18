# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     config.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/26
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""

common_headers = {
    'origin': "https://flights.ctrip.com",
    'content-type': "application/json;charset=UTF-8",
    'accept': "application/json",
    'cache-control': "no-cache",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "zh-CN,zh;q=0.9",
    "Sec-Ch-Ua-Platform": "Windows",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, " +
                  "like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"
}

url_map = {
    'domain': 'flights.ctrip.com',
    "protocol": "https",
    "city_code": "/online/api/poi/get",
    # 获取法定节假日
    "international_holiday": "/international/search/api/base/getHoliday",
    # 获取国家编码
    "country_code": "/international/search/restapi/soa2/15095/json/flightCityPageData",
    # 获取航线的航段信息，参数：/oneway-bjs-sel?_=1&depdate=2021-12-31&cabin=y_s&adult=1&containstax=1
    "flight_segments": "/international/search/api/flightlist/oneway",
    # 获取航线的航班列表
    "flight_list": "/international/search/api/search/batchSearch",
    # 机票订单查询首页
    "order_query_home_with_flight": "https://my.ctrip.com/myinfo/flight",
    # 订单详情页，?oid=32665635142
    "flight_order_details": "https://flights.ctrip.com/online/orderdetail/index",
    # 携程机票安全支付界面，?tradeNo=20240529144727TP1193583667800373067821
    "safe_payment_home": "https://secure.ctrip.com/webapp/payment8/index",
    # 易宝会员支付账号输入界面
    "yeepay2b_cash_desk": "https://cashdesk.yeepay.com/bc-cashier/bcnewpc/request",
    # 登录页
    "ctrip_login_prefix": "https://passport.ctrip.com/user/login",
    "ctrip_login_suffix": "{}?BackUrl=https%3A%2F%2Fwww.ctrip.com%2F#ctm_ref=c_ph_login_buttom",
    # h5 航线航班列表页
    "h5_flight_list": "https://m.ctrip.com/html5/flight/taro/first",
    # h5 航线航班列表api, ?subEnv=fat128
    "h5_flight_list_api": "https://m.ctrip.com/restapi/soa2/14488/flightList",
    # h5 航线航班策略列表页 ?from=inner&searchKey={}&price={}&code=MU
    "h5_flight_policy_list": "https://m.ctrip.com/html5/flight/taro/middle",
    # h5 航线航班策略列表api ?subEnv=fat128
    "h5_flight_policy_list_api": "https://m.ctrip.com/restapi/soa2/14488/policyListSearch",
}

airline_request_params_template = {
    "adultCount": 1,
    "childCount": 0,
    "infantCount": 0,
    "flightWay": "S",  # OW: 单程, S:
    "cabin": "Y_S",
    "scope": "d",
    "extensionAttributes": {
        "LoggingSampling": False,
        "isFlightIntlNewUser": False
    },
    "segmentNo": 1,
    "transactionID": "13960086675943ef869fae36c6818883",
    "flightSegments": list(),  # 航段
    "directFlight": False,  # 是否为直飞
    "extGlobalSwitches": {
        "useAllRecommendSwitch": True,
        "unfoldPriceListSwitch": True
    },
    "noRecommend": False  # 是否要推荐产品
}

flight_segment_template = {
    "departureCityCode": "",
    "arrivalCityCode": "",
    "departureCityName": "",
    "arrivalCityName": "",
    "departureDate": "",
    "departureCountryId": 1,
    "departureCountryName": "中国",
    "departureCountryCode": "CN",
    "departureProvinceId": 0,
    "departureCityId": 0,
    "arrivalCountryId": 1,
    "arrivalCountryName": "中国",
    "arrivalCountryCode": "CN",
    "arrivalProvinceId": 0,
    "arrivalCityId": 0,
    "departureCityTimeZone": 480,
    "arrivalCityTimeZone": 480,
    "timeZone": 480
}
