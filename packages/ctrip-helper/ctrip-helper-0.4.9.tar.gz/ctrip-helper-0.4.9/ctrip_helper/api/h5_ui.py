# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     h5_ui.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/06/04
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import time
from enum import Enum
from json import loads
from decimal import Decimal
from selenium import webdriver
from ctrip_helper.config import url_map
from selenium.webdriver.remote.webelement import WebElement
from ctrip_helper.utils import get_chinese_pinyin_first_letter
from ctrip_helper.libs import get_element, logger, scroll_element, click, scroll_calendar_container, get_elements, \
    get_element_by_parent_element, get_elements_by_parent_element


class UILocatorRegx(Enum):
    airline_alias = {"locator": "xpath",
                     "regx": '//div[@id="navigation-box"]//div[contains(@class, "ListTitle_title")]'}
    airline_departure_city = {"locator": "xpath",
                              "regx": '//div[contains(@class, "CityDate_search-city-date-container")]' +
                                      '//div[@data-testid="u_departure-city"]'}
    airline_city_pinyin_first_letter = {"locator": "xpath",
                                        "regx": '//div[@class="m-indexes__menu"]//div[@id="{}"]'}
    airline_city_input = {"locator": "xpath",
                          "regx": '//div[@class="city-picker"]//div[@class="city-item"]//div[contains(text(), "{}")]'}
    airline_arrival_city = {"locator": "xpath",
                            "regx": '//div[contains(@class, "CityDate_search-city-date-container")]' +
                                    '//div[@data-testid="u_arrival-city"]'}
    airline_arrival_city_input = {"locator": "xpath",
                                  "regx": '//div[contains(@class, "CityDate_search-city-date-container")]' +
                                          '//div[@data-testid="u_arrival-city"]'}
    airline_departure_date = {"locator": "xpath",
                              "regx": '//div[contains(@class, "CityDate_search-city-date-container")]' +
                                      '//div[@data-testid="u_departure_date"]'}
    calender_title_header = {"locator": "xpath", "regx": '//span[contains(text(), "选择去程日期")]'}
    calendar_week_header = {"locator": "xpath", "regx": '//div[@class="list-head"]'}
    month_wrap_container = {"locator": "xpath",
                            "regx": '//div[@class="calendar-wrap"]//div[@id="label-{}"]'}
    airline_departure_date_input = {"locator": "xpath",
                                    "regx": '//div[@class="calendar-wrap"]//div[@data-testid="date-item-{}"]'}
    airline_search_button = {"locator": "xpath",
                             "regx": '//div[contains(@class, "CityDate_search-city-date-container")]' +
                                     '//div[contains(@class, "search-btn")]'}
    airline_flight_list_pages = {"locator": "xpath", "regx": '//div[@class="zt-main-list"]/div'}
    flight_list_per_page = {"locator": "xpath", "regx": '//div[@class="zt-main-list"]/div[@class="wrap_0"]/div'}
    airline_flight_list_data = {"locator": "xpath",
                                "regx": '//div[@class="zt-main-list"]//div[@data-testid="common-card-{}_{}"]'}
    flight_list_calendar_header = {"locator": "xpath", "regx": '//div[contains(@class, "Calendar_calendar-wrap")]'}
    flight_list_filter_header = {"locator": "xpath", "regx": '//div[contains(@class, "FilterBar_FilterBarNew")]'}


class SeleniumApi(object):

    @classmethod
    def open_airline_flight_list_page(cls, driver: webdriver, airline: str, sleep: float = 0) -> None:
        url = url_map.get('h5_flight_list')
        driver.get(url)
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开携程H5版航线<{}>航班列表页".format(airline))

    @classmethod
    def click_airline_alias(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        airline_alias_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_alias.value.get("locator"),
            regx=UILocatorRegx.airline_alias.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if airline_alias_element:
            is_success = click(element=airline_alias_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击航线别名，修改航线的起飞-抵达城市")
                return True
        return False

    @classmethod
    def click_departure_city(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        departure_city_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_departure_city.value.get("locator"),
            regx=UILocatorRegx.airline_departure_city.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if departure_city_element:
            is_success = click(element=departure_city_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击起飞城市选择框")
                return True
        return False

    @classmethod
    def click_city_pinyin_first_letter(cls, driver: webdriver, chinese_city: str, loop: int = 1, sleep: float = 0,
                                       **kwargs) -> bool:
        pinyin = get_chinese_pinyin_first_letter(chinese_str=chinese_city, is_upper=True)
        regx = UILocatorRegx.airline_city_pinyin_first_letter.value.get("regx").format(pinyin[0])
        city_pinyin_first_letter_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_city_pinyin_first_letter.value.get("locator"),
            regx=regx, loop=loop, sleep=sleep, **kwargs
        )
        if city_pinyin_first_letter_element:
            is_success = click(element=city_pinyin_first_letter_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击城市<{}>拼音首字母【{}】成功".format(chinese_city, pinyin[0]))
                return True
        return False

    @classmethod
    def select_departure_city(cls, driver: webdriver, departure_city: str, loop: int = 1, sleep: float = 0,
                              **kwargs) -> bool:
        regx = UILocatorRegx.airline_city_input.value.get("regx").format(departure_city)
        departure_city_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_city_input.value.get("locator"),
            regx=regx, loop=loop, sleep=sleep, **kwargs
        )
        if departure_city_element:
            is_success = click(element=departure_city_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击选择起飞城市：{}".format(departure_city))
                return True
        return False

    @classmethod
    def click_arrival_city(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        arrival_city_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_city_input.value.get("locator"),
            regx=UILocatorRegx.airline_arrival_city.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if arrival_city_element:
            is_success = click(element=arrival_city_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击抵达城市选择框")
                return True
        return False

    @classmethod
    def select_arrival_city(cls, driver: webdriver, arrival_city: str, loop: int = 1, sleep: float = 0,
                            **kwargs) -> bool:
        regx = UILocatorRegx.airline_city_input.value.get("regx").format(arrival_city)
        arrival_city_elment = get_element(
            driver=driver, locator=UILocatorRegx.airline_city_input.value.get("locator"),
            regx=regx, loop=loop, sleep=sleep, **kwargs
        )
        if arrival_city_elment:
            is_success = click(driver=driver, element=arrival_city_elment, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击选择抵达城市：{}".format(arrival_city))
                return True
        return False

    @classmethod
    def click_departure_date(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        departure_date_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_departure_date.value.get("locator"),
            regx=UILocatorRegx.airline_departure_date.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if departure_date_element:
            is_success = click(driver=driver, element=departure_date_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击航线起飞日期选择框")
                return True
        return False

    @classmethod
    def scroll_to_calendar_date(cls, driver: webdriver, date_str: str, loop: int = 1, sleep: float = 0,
                                **kwargs) -> bool:
        month_wrap_regx = UILocatorRegx.month_wrap_container.value.get("regx").format(date_str[:7])
        calender_title_header_element = get_element(
            driver=driver, locator=UILocatorRegx.calender_title_header.value.get("locator"),
            regx=UILocatorRegx.calender_title_header.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        calendar_week_header_element = get_element(
            driver=driver, locator=UILocatorRegx.calendar_week_header.value.get("locator"),
            regx=UILocatorRegx.calendar_week_header.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        month_wrap_element = get_element(
            driver=driver, locator=UILocatorRegx.month_wrap_container.value.get("locator"),
            regx=month_wrap_regx, loop=loop, sleep=sleep, **kwargs
        )
        if calender_title_header_element and calendar_week_header_element and month_wrap_element:
            hearder_high = calender_title_header_element.size['height'] + calendar_week_header_element.size['height']
            scroll_calendar_container(driver=driver, hearder_high=hearder_high, container=month_wrap_element)
            logger.info("滚动屏幕中的日历列表至{}月，使其可见".format(date_str[:7]))
            return True
        return False

    @classmethod
    def select_departure_date_with_calendar(cls, driver: webdriver, date_str: str, loop: int = 1, sleep: float = 0,
                                            **kwargs) -> bool:
        regx = UILocatorRegx.airline_departure_date_input.value.get("regx").format(date_str)
        departure_date_element = get_element(
            driver=driver, locator=UILocatorRegx.airline_departure_date.value.get("locator"),
            regx=regx, loop=loop, sleep=sleep, **kwargs
        )
        if departure_date_element:
            scroll_element(driver=driver, element=departure_date_element)
            is_success = click(driver=driver, element=departure_date_element, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("选择航线起飞日期：{}".format(date_str))
                return True
        return False

    @classmethod
    def click_airline_search(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        search_button = get_element(
            driver=driver, locator=UILocatorRegx.airline_search_button.value.get("locator"),
            regx=UILocatorRegx.airline_search_button.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if search_button:
            is_success = click(driver=driver, element=search_button, loop=loop, sleep=sleep, **kwargs)
            if is_success is True:
                logger.info("点击航线查询页的搜索")
                return True
        return False

    @classmethod
    def parse_flight_data_with_element(cls, element: WebElement, line_id: str, **kwargs) -> dict:
        flight_info = dict(
            line_id=line_id, flight_no='', departure_time='', arrival_time='', departure_city='', arrival_city='',
            trip_tag='', remain_ticket='', flight_price=Decimal("NaN"), trip_limit='', discount_label='', tag_text='',
            transit_middle_time='', transit_city='', flight_security=''
        )
        # 起飞抵达时间
        card_time_regx = './/div[contains(@class, "ListCardTime_time")]'
        # 起飞抵达机场
        card_name_regx = './/div[contains(@class, "ListCardTime_Name")]'
        # 航班号
        flight_no_regx = './/div[contains(@class,"FlightListCard_displayStyle")]'
        # 航班标签
        trip_tag_regx = './/div[contains(@class,"FlightListCard_tripTagBox")]'
        # 余票
        remain_ticket_regx = './/div[contains(@class,"PriceComponent_remain-ticket")]'
        # 航班价格
        flight_price_regx = './/span[contains(@class,"taro-text PriceComponent_price")]'
        # 限制条件
        trip_limit_regx = './/div[contains(@class,"FlightListCard_trip-limit-text")]'
        # 优惠标签
        discount_label_regx = './/div[contains(@class,"FlightListCard_discountLabel")]'
        # 标签文案
        tag_text_regx = './/span[contains(@class,"taro-text CommomCardTag_tagText")]'
        # 中转停留时长
        transit_middle_time_regx = './/div[contains(@class,"TransitLineArrow_middle-time")]'
        # 中转停留城市
        transit_city_regx = './/div[contains(@class,"TransitLineArrow_city")]'
        # 航班说明
        flight_security_regx = './/div[contains(@class,"FlightListCard_flt-security-text")]'
        card_time_elements = get_elements_by_parent_element(
            parent_element=element, locator="xpath", regx=card_time_regx, **kwargs
        )
        if card_time_elements:
            flight_info['departure_time'] = card_time_elements[0].text.strip()
            flight_info['arrival_time'] = card_time_elements[1].text.strip().replace("\n", "|")
        card_name_elements = get_elements_by_parent_element(
            parent_element=element, locator="xpath", regx=card_name_regx, **kwargs
        )
        if card_name_elements:
            flight_info['departure_city'] = card_name_elements[0].text.strip()
            flight_info['arrival_city'] = card_name_elements[1].text.strip()
        flight_no = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=flight_no_regx, **kwargs
        )
        if flight_no:
            flight_info['flight_no'] = flight_no.text.strip()
        trip_tag = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=trip_tag_regx, **kwargs
        )
        if trip_tag:
            flight_info['trip_tag'] = trip_tag.text.strip().replace("\n", "|")
        remain_ticket = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=remain_ticket_regx, **kwargs
        )
        if remain_ticket:
            flight_info['remain_ticket'] = remain_ticket.text.strip()
        flight_price = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=flight_price_regx, **kwargs
        )
        if flight_price:
            flight_info['flight_price'] = Decimal(flight_price.text.strip())
        trip_limit = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=trip_limit_regx, **kwargs
        )
        if trip_limit:
            flight_info['trip_limit'] = trip_limit.text.strip()
        discount_label = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=discount_label_regx, **kwargs
        )
        if discount_label:
            flight_info['discount_label'] = discount_label.text.strip()
        tag_text = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=tag_text_regx, **kwargs
        )
        if tag_text:
            flight_info['tag_text'] = tag_text.text.strip()
        transit_middle_time = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=transit_middle_time_regx, **kwargs
        )
        if transit_middle_time:
            flight_info['transit_middle_time'] = transit_middle_time.text.strip()
        transit_city = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=transit_city_regx, **kwargs
        )
        if transit_city:
            flight_info['transit_city'] = transit_city.text.strip()
        flight_security = get_element_by_parent_element(
            parent_element=element, locator="xpath", regx=flight_security_regx, **kwargs
        )
        if flight_security:
            flight_info['flight_security'] = flight_security.text.strip()
        return flight_info if flight_info.get("flight_no") else dict()

    @classmethod
    def get_airline_flight_list_with_element(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> list:
        flight_info = list()
        airline_alias_header = get_element(
            driver=driver, locator=UILocatorRegx.airline_alias.value.get("locator"),
            regx=UILocatorRegx.airline_alias.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        flight_list_calender_header = get_element(
            driver=driver, locator=UILocatorRegx.flight_list_calendar_header.value.get("locator"),
            regx=UILocatorRegx.flight_list_calendar_header.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        flight_list_filter_header = get_element(
            driver=driver, locator=UILocatorRegx.flight_list_filter_header.value.get("locator"),
            regx=UILocatorRegx.flight_list_filter_header.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        frozen_height = airline_alias_header.size['height'] + flight_list_filter_header.size[
            'height'] + flight_list_calender_header.size['height']
        flight_list_pages = get_elements(
            driver=driver, locator=UILocatorRegx.airline_flight_list_pages.value.get("locator"),
            regx=UILocatorRegx.airline_flight_list_pages.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        flight_list_per_page = get_elements(
            driver=driver, locator=UILocatorRegx.flight_list_per_page.value.get("locator"),
            regx=UILocatorRegx.flight_list_per_page.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if flight_list_pages and flight_list_per_page:
            pages = len(flight_list_pages)
            per_page = len(flight_list_per_page)
            for page in range(pages):
                for line in range(per_page):
                    line_id = "common-card-{}_{}".format(page, line)
                    line_data_regx = UILocatorRegx.airline_flight_list_data.value.get("regx").format(page, line)
                    line_element = get_element(
                        driver=driver, locator=UILocatorRegx.airline_flight_list_data.value.get("locator"),
                        regx=line_data_regx, loop=loop, sleep=sleep, **kwargs
                    )
                    if line_element:
                        scroll_calendar_container(driver=driver, hearder_high=frozen_height, container=line_element)
                        flight_data = cls.parse_flight_data_with_element(
                            element=line_element, line_id=line_id, **kwargs)
                        if flight_data:
                            flight_info.append(flight_data)
        return flight_info

    @classmethod
    def get_airline_flight_list_with_request(cls, driver: webdriver) -> dict:
        data = dict()
        for request in driver.requests:
            url = request.url
            if url.startswith(url_map.get("h5_flight_list_api")) is True:
                status_code = request.response.status_code
                if status_code == 200:
                    body = request.response.body
                    if body:
                        data = loads(body.decode("utf-8"))
                break
        return data

    @classmethod
    def parse_flight_data_with_json(cls, result_data: dict) -> list:
        flights_info = list()
        data = loads(result_data.get("data")) if isinstance(result_data.get("data"), str) else result_data.get("data")
        data = data if isinstance(data, dict) else dict()
        list_cards = data.get("listCards") if isinstance(data.get("listCards"), list) else list()
        for card in list_cards:
            arrival_airport_code = card.get("arrivalAirportCode") or ""
            arrival_airport_name = card.get("arrivalAirportName") or ""
            arrival_airport_terminal = card.get("arrivalName") or ""
            arrival_time = card.get("arrivalTime") or ""
            arrive_date_time = card.get("arriveDateTime") or ""
            cross_days = card.get("crossDays") or 0
            depart_date_time = card.get("departDateTime") or ""
            departure_airport_code = card.get("departureAirportCode") or ""
            departure_airport_name = card.get("departureAirportName") or ""
            departure_airport_terminal = card.get("departureName") or ""
            departure_time = card.get("departureTime") or ""
            departure_week = card.get("departureWeek") or ""
            discounts = card.get("discounts") if isinstance(card.get("discounts"), dict) else dict()
            discounts_economy = discounts.get("ECONOMY") or ""
            discounts_business = discounts.get("BUSINESS") or ""
            final_prices = card.get("finalPrices") if isinstance(card.get("finalPrices"), dict) else dict()
            final_prices_economy = final_prices.get("ECONOMY") or ""
            final_prices_business = final_prices.get("BUSINESS") or ""
            search_key = card.get("searchKey") or ""
            ticket_counts = card.get("ticketCounts") if isinstance(card.get("ticketCounts"), dict) else dict()
            ticket_counts_economy = ticket_counts.get("ECONOMY") or ""
            ticket_counts_business = ticket_counts.get("BUSINESS") or ""
            total_duration = card.get("totalDuration") or ""
            transit = card.get("transit") or ""
            transit_code = card.get("transitCode") or ""
            transit_duration = card.get("transitDuration") or ""
            flight_change_policy = card.get("tripTagsV2") if isinstance(card.get("tripTagsV2"), dict) else dict()
            flight_change_policy_economy = flight_change_policy.get("ECONOMY").get(
                "FLIGHT_CHANGE_ENSURE") or "" if isinstance(card.get("ECONOMY"), dict) else ""
            flight_change_policy_business = flight_change_policy.get("BUSINESS").get(
                "FLIGHT_CHANGE_ENSURE") or "" if isinstance(card.get("BUSINESS"), dict) else ""
            airlines = card.get("airlines") if isinstance(card.get("airlines"), list) else list()
            airline_1 = airlines[0]
            if transit_code:
                airline_2 = airlines[1]
            else:
                airline_2 = dict()
            airline_code_1 = airline_1.get("code") or ""
            flight_craft_1 = airline_1.get("craft") or ""
            flight_name_1 = airline_1.get("displayName") or ""
            flight_no_1 = airline_1.get("flightNo") or ""
            airline_name_1 = airline_1.get("name") or ""
            is_shared_1 = airline_1.get("shared") if isinstance(airline_1.get("shared"), bool) else ""
            airline_short_name_1 = airline_1.get("shortName") or ""
            airline_code_2 = airline_2.get("code") or ""
            flight_craft_2 = airline_2.get("craft") or ""
            flight_name_2 = airline_2.get("displayName") or ""
            flight_no_2 = airline_2.get("flightNo") or ""
            airline_name_2 = airline_2.get("name") or ""
            is_shared_2 = airline_2.get("shared") if isinstance(airline_2.get("shared"), bool) else ""
            airline_short_name_2 = airline_2.get("shortName") or ""
            flight_info = dict(
                flight_no_1=flight_no_1, airline_code_1=airline_code_1, flight_craft_1=flight_craft_1,
                flight_name_1=flight_name_1, airline_name_1=airline_name_1, is_shared_1=is_shared_1,
                airline_short_name_1=airline_short_name_1, flight_no_2=flight_no_2, airline_code_2=airline_code_2,
                flight_craft_2=flight_craft_2, flight_name_2=flight_name_2, airline_name_2=airline_name_2,
                is_shared_2=is_shared_2, airline_short_name_2=airline_short_name_2, depart_date_time=depart_date_time,
                departure_airport_code=departure_airport_code, departure_airport_name=departure_airport_name,
                departure_airport_terminal=departure_airport_terminal, departure_time=departure_time,
                departure_week=departure_week, arrival_airport_code=arrival_airport_code,
                arrival_airport_name=arrival_airport_name, arrival_airport_terminal=arrival_airport_terminal,
                arrival_time=arrival_time, arrive_date_time=arrive_date_time, cross_days=cross_days,
                discounts_economy=discounts_economy, discounts_business=discounts_business, transit_code=transit_code,
                final_prices_economy=final_prices_economy, final_prices_business=final_prices_business,
                ticket_counts_economy=ticket_counts_economy, ticket_counts_business=ticket_counts_business,
                transit_duration=transit_duration, total_duration=total_duration, transit=transit,
                flight_change_policy_economy=flight_change_policy_economy, search_key=search_key,
                flight_change_policy_business=flight_change_policy_business,
            )
            flights_info.append(flight_info)
        return flights_info

    @classmethod
    def open_flight_policy_list_page(cls, driver: webdriver, search_key: str, price: str, flight_no: str,
                                     sleep: float = 0) -> None:
        url = url_map.get('h5_flight_policy_list')
        url = url + '?from=inner&searchKey={}&price={}&code=MU'.format(search_key, price)
        driver.get(url)
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开携程H5版航班<{}>产品策略列表页".format(flight_no))

    @classmethod
    def get_flight_policy_list_with_request(cls, driver: webdriver) -> dict:
        data = dict()
        for request in driver.requests:
            url = request.url
            if url.startswith(url_map.get("h5_flight_policy_list_api")) is True:
                status_code = request.response.status_code
                if status_code == 200:
                    body = request.response.body
                    if body:
                        data = loads(body.decode("utf-8"))
                break
        return data

    @classmethod
    def parse_flight_policy_data_with_json(cls, result_data: dict, flight_no: str) -> list:
        flights_policy = list()
        data = loads(result_data.get("data")) if isinstance(result_data.get("data"), str) else result_data.get("data")
        data = data if isinstance(data, dict) else dict()
        middle = data.get("middle") if isinstance(data.get("middle"), dict) else dict()
        policies = middle.get("policies") if isinstance(middle.get("policies"), list) else list()
        for policy in policies:
            cabin_classes = "|".join(policy.get("cabinClasses")) if isinstance(
                policy.get("cabinClasses"), list) and len(policy.get("cabinClasses")) > 0 else ""
            corner_title = policy.get("cornerTitle") or ""
            policy_note_list = [x.get("content") for x in policy.get("policyNoteList")] if isinstance(
                policy.get("policyNoteList"), list) else list()
            policy_note = ";".join(policy_note_list) if policy_note_list else ""
            prices = policy.get("prices") if isinstance(policy.get("prices"), dict) else dict()
            policy_tags = policy.get("policyTags") if isinstance(policy.get("policyTags"), dict) else dict()
            policy_tag_discount_reduce = policy_tags.get("DISCOUNT_REDUCE") or ""
            policy_tag_airline_marketing = "携程官方旗舰店" if policy_tags.get("AIRLINE_MARKETING") else ""
            policy_tag_airline_member_ship = policy_tags.get("LIMITED_AIRLINE_MEMBERSHIP") or ""
            policy_tag_travel_package = policy_tags.get("TRAVEL_PACKAGE") or ""
            policy_tag_merge_discount = policy_tags.get("MERGE_DISCOUNT") or ""
            extra_tags = policy_tags.get("extraTags") if isinstance(policy_tags.get("extraTags"), dict) else dict()
            extra_tag_travel_package = extra_tags.get("TRAVEL_PACKAGE") or ""
            extra_tag_family_together = extra_tags.get("FAMILY_TOGETHER") or ""
            extra_tag_invoice_type = "全额普通发票" if extra_tag_travel_package else "行程单"
            adult_price = prices.get("ADULT") or 0  # 成人
            child_price = prices.get("CHILD") or 0  # 儿童
            infant_price = policy.get("INFANT") or 0  # 婴儿
            child_book_adult_price = policy.get("CHILD_BOOK_ADULT") or 0  # 儿童预定成人
            product_type_list = "|".join(policy.get("productTypeList")) if isinstance(
                policy.get("productTypeList"), list) and len(policy.get("productTypeList")) > 0 else ""
            segment_tags = ['{}|{}|{}'.format(
                x.get("BAGGAGE"), x.get("REFUND_ENDORSE"), x.get("CABIN_CLASS")
            ) for x in policy.get("segmentTags") if
                x.get("BAGGAGE") and x.get("REFUND_ENDORSE") and x.get("CABIN_CLASS")] if isinstance(
                policy.get("segmentTags"), list) and len(policy.get("segmentTags")) > 0 else list()
            segment_tags = ";".join(segment_tags) if segment_tags else ""
            restriction_tags = "|".join(policy_tags.get("restrictionTags")) if isinstance(
                policy_tags.get("restrictionTags"), list) and len(policy_tags) > 0 else ""
            ticket_count = policy.get("ticketCount") or 0
            flight_policy_info = dict(
                flight_no=flight_no, cabin_classes=cabin_classes, corner_title=corner_title, adult_price=adult_price,
                policy_note=policy_note, policy_tag_discount_reduce=policy_tag_discount_reduce,
                policy_tag_airline_marketing=policy_tag_airline_marketing, restriction_tags=restriction_tags,
                policy_tag_airline_member_ship=policy_tag_airline_member_ship, infant_price=infant_price,
                child_price=child_price, product_type_list=product_type_list, segment_tags=segment_tags,
                ticket_count=ticket_count, extra_tag_travel_package=extra_tag_travel_package,
                policy_tag_travel_package=policy_tag_travel_package, extra_tag_invoice_type=extra_tag_invoice_type,
                extra_tag_family_together=extra_tag_family_together, child_book_adult_price=child_book_adult_price,
                policy_tag_merge_discount=policy_tag_merge_discount,
            )
            flights_policy.append(flight_policy_info)
        return flights_policy

    @classmethod
    def get_batch_flight_policy_by_airline(cls, driver: webdriver, airline_flight_data: list,
                                           sleep: float = 1.0) -> list:
        flights_policy = list()
        for flight_data in airline_flight_data:
            search_key = flight_data.get("search_key")
            flight_no_1 = flight_data.get("flight_no_1")
            final_prices_economy = flight_data.get("final_prices_economy")
            cls.open_flight_policy_list_page(
                driver=driver, search_key=search_key, price=final_prices_economy, sleep=sleep, flight_no=flight_no_1
            )
            response_result = cls.get_flight_policy_list_with_request(driver=driver)
            if response_result:
                flight_policy_data = cls.parse_flight_policy_data_with_json(
                    result_data=response_result, flight_no=flight_no_1
                )
                if flight_policy_data:
                    flights_policy.extend(flight_policy_data)
        return flights_policy
