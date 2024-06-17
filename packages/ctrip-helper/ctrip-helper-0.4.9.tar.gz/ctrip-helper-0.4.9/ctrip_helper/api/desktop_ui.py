# -*- coding: utf-8 -*-
"""
# ---------------------------------------------------------------------------------------------------------
# ProjectName:  ctrip-helper
# FileName:     desktop_ui.py
# Description:  TODO
# Author:       mfkifhss2023
# CreateDate:   2024/05/29
# Copyright ©2011-2024. Hunan xxxxxxx Company limited. All rights reserved.
# ---------------------------------------------------------------------------------------------------------
"""
import re
import time
from enum import Enum
from decimal import Decimal
from selenium import webdriver
from ctrip_helper.libs import logger
from ctrip_helper.config import url_map
from selenium.webdriver.common.keys import Keys
from ctrip_helper.utils import is_later_than_current_time
from ctrip_helper.libs import get_element, send_keys, is_switch_latest_page, get_screenshot, exception_html_save_to_txt


class UILocatorRegx(Enum):
    all_orders_select_box = {"locator": "xpath",
                             "regx": '//ul[@class="fix_myctrip_order_layer"]//div[@class="select-box"]'}
    order_id_input_box = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//input[@id="searchBookingNum"]'}
    order_query_button = {"locator": "xpath", "regx": '//div[@class="order_inquiry"]//button[@class="btn_sel"]'}
    order_status_with_list = {"locator": "xpath",
                              "regx": '//ul[@class="t_body"]//span[@class="order-price-status-title"]'}
    # itinerary_conflict_timely = {"locator": "xpath",
    #                              "regx": '//div[@class="ant-modal"]//div[@data-testid=' +
    #                                      '"repeatPayLayer_RightBottomBtnTxt_buttonType来得及，继续支付"]'}
    itinerary_conflict_timely = {"locator": "xpath", "regx": '//div[contains(@data-testid, "继续支付")'}
    order_status_sub_title = {"locator": "xpath",
                              "regx": '//div[contains(@data-testid, "orderstatus_StatusSubTitleWrap")]'}
    order_status_booking_amount = {"locator": "xpath",
                                   "regx": '//div[@data-testid="fbu_PaymentWrapper"]//span[@data-testid="false"]'}
    order_to_payment = {"locator": "xpath", "regx": '//div[@id="button-group"]//a[@data-ubt-v="主订单支付"]'}
    order_to_cancel = {"locator": "xpath", "regx": '//div[@id="button-group"]//a[@data-ubt-v="取消订单"]'}
    order_status_with_detail = {"locator": "xpath",
                                "regx": '//div[@data-testid="orderstatus_StatusWrap"]' +
                                        '//div[contains(@data-testid, "orderstatus_StatusTitle_colorValue")]'}
    order_continue_cancel = {"locator": "xpath", "regx": '//div[@class="ant-modal"]//div[@data-testid="继续取消"]'}
    order_cancel_got_it = {"locator": "xpath", "regx": '//div[@class="ant-modal"]//div[@data-testid="知道了"]'}
    order_payment_amount = {"locator": "xpath", "regx": '//div[@class="m-order-amount"]//div[@class="m-order-money"]'}
    wallet_disable = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//div[@class="lin-crd-disabled"]'}
    wallet_balance = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//div[contains(@class, "crdlast")]'}
    use_wallet = {"locator": "xpath", "regx": '//div[@class="walelt-card"]//input[@class="am-switch-checkbox"]'}
    wallet_immediately_payment = {"locator": "xpath",
                                  "regx": '//div[@class="wallet_pay_button"]//button[@type="gradient"]'}
    use_yeepay2b_pyament = {"locator": "xpath",
                            "regx": '//div[@class="pay_way_container"]//div[contains(text(), "易宝会员支付")]'}
    yeepay2b_immediately_payment = {"locator": "xpath",
                                    "regx": '//div[@class="pay_btn_container"]//div[@class="trip-pay-btn-text"]'}
    password_input_box = {"locator": "xpath",
                          "regx": '//div[@class="verify-password-box"]//input[contains(@class, "ant-input")]'}
    yeepay2b_accout_input_box = {"locator": "xpath",
                                 "regx": '//div[@class="account-pay-main"]//input[@name="userAccount"]'}
    yeepay2b_password_input_box = {"locator": "xpath",
                                   "regx": '//div[@class="account-pay-main"]//input[@name="tradePassword"]'}
    yeepay2b_payment_next_button = {"locator": "xpath",
                                    "regx": '//div[@class="account-pay-main"]//button[@id="passPayButton"]'}
    is_login_button = {
        "locator": "xpath",
        "regx": '//div[@class="tl_nfes_home_header_login_wrapper_siwkn"]//button[contains(@aria-label, "我的账户")]'
    }
    is_login_span = {"locator": "xpath", "regx": '//div[@class="loginbar"]//span[@class="ctrip-username"]'}
    account_input = {"locator": "xpath",
                     "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="accountNameInput"]'}
    password_input = {"locator": "xpath",
                      "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="passwordInput"]'}
    service_agreement = {"locator": "xpath",
                         "regx": '//div[@data-testid="agreementList"]//label[@for="checkboxAgreementInput"]'}
    login_button = {"locator": "xpath", "regx": '//div[@data-testid="accountPanel"]//input[@data-testid="loginButton"]'}
    slider_verify = {"locator": "xpath", "regx": '//div[@data-testid="captcha"]/div'}
    more_bank_card = {"locator": "xpath", "regx": '//div[@class="payment_trip_pay_container"]//div[@class="more_card"]'}
    bank_card = {"locator": "xpath", "regx": '//div[@class="payment_trip_pay_container"]//div[contains(text(), "{}")]'}
    bank_card_payment = {"locator": "xpath",
                         "regx": '//div[@class="payment_trip_pay_container"]//div[@class="trip-pay-btn-text"]'}
    yeepay2b_payment_success = {"locator": "xpath", "regx": '//div[@class="success-layout"]//p[@class="pay-success"]'}
    submit_payment_result = {"locator": "xpath",
                             "regx": '//div[contains(@class,"cds-dialog-content")]//div[contains(text(), "支付确认")]'}
    wallet_payment_result_status = {
        "locator": "xpath",
        "regx": '//div[@data-testid="orderstatus_StatusWrap"]' +
                '//div[contains(@data-testid, "orderstatus_StatusTitle_colorValue")]'
    }


class SeleniumApi(object):

    @classmethod
    def is_login(cls, driver: webdriver, username: str, platform: str, loop: int = 1, sleep: float = 0,
                 **kwargs) -> bool:
        """是否已登录"""
        is_login_button = get_element(
            driver=driver, locator=UILocatorRegx.is_login_button.value.get("locator"),
            regx=UILocatorRegx.is_login_button.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if is_login_button:
            logger.info("{}平台用户<{}>已登录".format(platform, username))
            return True
        is_login_span = get_element(
            driver=driver, locator=UILocatorRegx.is_login_span.value.get("locator"),
            regx=UILocatorRegx.is_login_span.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if is_login_span:
            logger.info("{}平台用户<{}>已登录".format(platform, username))
            return True
        else:
            return False

    @classmethod
    def open_login_page(cls, driver: webdriver, sleep: float = 0) -> None:
        ctrip_login_prefix = url_map.get('ctrip_login_prefix')
        ctrip_login_suffix = url_map.get('ctrip_login_suffix')
        login_url = "{}{}".format(ctrip_login_prefix, ctrip_login_suffix)
        driver.get(login_url)
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开携程网页版登录页")

    @classmethod
    def enter_user_name(cls, driver: webdriver, username: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.account_input.value.get("locator"),
            regx=UILocatorRegx.account_input.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(username))
            logger.info("输入登录账号：{}".format(username))
            return True
        else:
            return False

    @classmethod
    def enter_user_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.password_input.value.get("locator"),
            regx=UILocatorRegx.password_input.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(password))
            logger.info("输入登录密码：{}".format(password))
            return True
        else:
            return False

    @classmethod
    def click_service_agreement(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        checkbox = get_element(
            driver=driver, locator=UILocatorRegx.service_agreement.value.get("locator"),
            regx=UILocatorRegx.service_agreement.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if checkbox:
            checkbox.click()
            logger.info("选中【阅读并同意携程的服务协议和个人信息保护政策】")
            return True
        else:
            return False

    @classmethod
    def click_login(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        login_button = get_element(
            driver=driver, locator=UILocatorRegx.login_button.value.get("locator"),
            regx=UILocatorRegx.login_button.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if login_button:
            login_button.click()
            logger.info("点击登录页面的【登录】按钮")
            return True
        else:
            return False

    @classmethod
    def is_exist_slider_verify(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        current_url = driver.current_url
        slider_verify = get_element(
            driver=driver, locator=UILocatorRegx.slider_verify.value.get("locator"),
            regx=UILocatorRegx.slider_verify.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if slider_verify:
            logger.info("当前页：{} 出现了滑块验证码".format(current_url))
            return True
        else:
            return False

    @classmethod
    def open_order_query_home_with_flight(cls, driver: webdriver, sleep: float = 0) -> None:
        driver.get(url_map.get('order_query_home_with_flight'))
        if sleep > 0:
            time.sleep(sleep)
        logger.info("打开机票订单查询首页")

    @classmethod
    def click_more_filter_conditions(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        more_filter_expand = get_element(
            driver=driver, locator=UILocatorRegx.all_orders_select_box.value.get("locator"),
            regx=UILocatorRegx.all_orders_select_box.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if more_filter_expand:
            more_filter_expand.click()
            logger.info("选择【更多筛选条件】，展开条件列表")
            return True
        else:
            return False

    @classmethod
    def enter_order_id(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.order_id_input_box.value.get("locator"),
            regx=UILocatorRegx.order_id_input_box.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(order_id))
            logger.info("输入查询订单号：{}".format(order_id))
            return True
        else:
            return False

    @classmethod
    def click_order_query(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        order_query_button = get_element(
            driver=driver, locator=UILocatorRegx.order_query_button.value.get("locator"),
            regx=UILocatorRegx.order_query_button.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_query_button:
            order_query_button.click()
            logger.info("点击【查询】按钮")
            return True
        else:
            return False

    @classmethod
    def get_order_status_with_list(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> str:
        order_status = ""
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_with_list.value.get("locator"),
            regx=UILocatorRegx.order_status_with_list.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_status_element:
            order_status = order_status_element.text.strip()
            logger.info("获取查询列表页订单的状态为：{}".format(order_status))
        return order_status

    @classmethod
    def get_order_status_with_detail(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> str:
        order_status = ""
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_with_detail.value.get("locator"),
            regx=UILocatorRegx.order_status_with_detail.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_status_element:
            order_status = order_status_element.text.strip()
            logger.info("获取订单详情页订单的状态为：{}".format(order_status))
        return order_status

    @classmethod
    def click_order_status_with_query_list(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_with_list.value.get("locator"),
            regx=UILocatorRegx.order_status_with_list.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_status_element:
            order_status_element.click()
            logger.info("点击订单状态，进入订单详情界面")
            return True
        else:
            return False

    @classmethod
    def click_to_payment(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        local_url = "{}?oid={}".format(url_map.get("flight_order_details"), order_id)
        is_success, current_url = is_switch_latest_page(driver=driver, latest_page=local_url, loop=loop, sleep=sleep)
        if is_success is True:
            to_payment_button = get_element(
                driver=driver, locator=UILocatorRegx.order_to_payment.value.get("locator"),
                regx=UILocatorRegx.order_to_payment.value.get("regx"), loop=loop, sleep=sleep, **kwargs
            )
            if to_payment_button:
                to_payment_button.click()
                logger.info("点击【去支付】，进入安全支付界面")
                return True
            else:
                return False
        else:
            logger.warn("当前页: {}，不是本次要支付的订单: {} 的详情页".format(current_url, order_id))
            return False

    @classmethod
    def click_order_cancel(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        local_url = "{}?oid={}".format(url_map.get("flight_order_details"), order_id)
        is_success, current_url = is_switch_latest_page(driver=driver, latest_page=local_url, loop=loop, sleep=sleep)
        if is_success is True:
            order_cancel_button = get_element(
                driver=driver, locator=UILocatorRegx.order_to_cancel.value.get("locator"),
                regx=UILocatorRegx.order_to_cancel.value.get("regx"), loop=loop, sleep=sleep, **kwargs
            )
            if order_cancel_button:
                order_cancel_button.click()
                logger.info("点击【取消订单】，接下来会出现【取消提示】小弹框")
                return True
            else:
                return False
        else:
            logger.warn("当前页: {}，不是本次要支付的订单: {} 的详情页".format(current_url, order_id))
            return False

    @classmethod
    def click_order_continue_cancel(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        continue_cance_button = get_element(
            driver=driver, locator=UILocatorRegx.order_continue_cancel.value.get("locator"),
            regx=UILocatorRegx.order_continue_cancel.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if continue_cance_button:
            continue_cance_button.click()
            logger.info("点击【继续取消】，接下来会出现【知道了】小弹框")
            return True
        else:
            return False

    @classmethod
    def is_order_cancel_success(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        got_it_button = get_element(
            driver=driver, locator=UILocatorRegx.order_cancel_got_it.value.get("locator"),
            regx=UILocatorRegx.order_cancel_got_it.value.get("regx"), sleep=sleep, loop=loop, **kwargs
        )
        if got_it_button:
            return True
        else:
            return False

    @classmethod
    def verify_order_detail_to_safe_payment_with_notice_box(cls, driver: webdriver, loop: int = 1, sleep: float = 0,
                                                            **kwargs) -> bool:
        local_url = url_map.get("safe_payment_home")
        is_success, current_url = is_switch_latest_page(driver=driver, latest_page=local_url, loop=loop, sleep=sleep)
        if is_success is True:
            return True
        else:
            itinerary_conflict_timely_button = get_element(
                driver=driver, locator=UILocatorRegx.itinerary_conflict_timely.value.get("locator"),
                regx=UILocatorRegx.itinerary_conflict_timely.value.get("locator"), loop=loop, sleep=sleep, **kwargs
            )
            if itinerary_conflict_timely_button:
                itinerary_conflict_timely_button.click()
                logger.warning("检测到乘客【行程冲突】的通知，点击【来得及，继续支付】按钮")
                return True
            exception_traceback = kwargs.get("exception_traceback", False)
            if exception_traceback is True:
                get_screenshot(driver=driver, file_name="订单详情跳转至安全收银台", **kwargs)
                exception_html_save_to_txt(driver=driver, file_name="订单详情跳转至安全收银台", **kwargs)
            return False

    @classmethod
    def get_order_amount_with_safe_payment_home(cls, driver: webdriver, loop: int = 1, sleep: float = 0,
                                                **kwargs) -> Decimal:
        order_payment_amount = "0.00"
        order_payment_amount_element = get_element(
            driver=driver, locator=UILocatorRegx.order_payment_amount.value.get("locator"),
            regx=UILocatorRegx.order_payment_amount.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_payment_amount_element:
            order_payment_amount = order_payment_amount_element.text.strip()
            logger.info("获取订单的支付金额为：{}".format(order_payment_amount))
        return Decimal(order_payment_amount)

    @classmethod
    def is_cancel_order_with_payment_amount(cls, driver: webdriver, out_total_amount: str, amount_loss_limit: str,
                                            profit_cap: str, passenger_number: int, platform: str, loop: int = 1,
                                            sleep: float = 0, discount_amount: str = None, **kwargs) -> tuple:
        """在订单详情页，判断是否需要取消订单，检验支付金额是否满足政策要求"""
        flag = False
        remark = ""
        booking_amount_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_booking_amount.value.get("locator"),
            regx=UILocatorRegx.order_status_booking_amount.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if booking_amount_element:
            booking_amount_text = booking_amount_element.text.strip()
            # 使用 findall 获取所有匹配项
            amount_match = re.search(r"¥(\d+)", booking_amount_text)
            if amount_match:
                amount_str = amount_match.group(1)
                logger.warning("从{}订单获取的支付金额：{}，劲旅订单总价：{}".format(
                    platform, amount_str, out_total_amount
                ))
                # 预期订单利润
                ex_order_profit = Decimal(out_total_amount) - Decimal(amount_str)
                if discount_amount:
                    # 实际订单利润
                    ac_order_profit = ex_order_profit + Decimal(discount_amount)
                else:
                    ac_order_profit = ex_order_profit
                # 订单利润 < 0, 存在亏钱，与亏钱的下限进行比较
                if ac_order_profit < 0:
                    total = Decimal(amount_loss_limit) * passenger_number
                    if ac_order_profit + total < 0:
                        flag = True
                        remark = "订单亏钱{:.2f}太多，超过订单总下限值{}(单人下限{} * {}人)".format(
                            abs(ac_order_profit), total, amount_loss_limit, passenger_number
                        )
                        logger.warning(remark)
                        return flag, remark
                # 订单利润 >= 0, 存在毛利，与利润的上限进行比较
                else:
                    total = Decimal(profit_cap) * passenger_number
                    if ac_order_profit - total > 0:
                        flag = True
                        remark = "订单利润{:.2f}太高，超过订单总下限值{}(单人下限{} * {}人)".format(
                            ac_order_profit, total, profit_cap, passenger_number
                        )
                        logger.warning(remark)
                        return flag, remark
            else:
                remark = "从订单详情页面获取订单过期时间和订单金额有异常"
                logger.warning(remark)
        else:
            remark = "订单详情页面中未找到订单金额元素"
            logger.warning(remark)
        return flag, remark

    @classmethod
    def is_cancel_order_with_remaining_payment_time(cls, driver: webdriver, seconds: int, loop: int = 1,
                                                    sleep: float = 0, **kwargs) -> tuple:
        """在订单详情页，判断是否需要取消订单，判断订单的剩余支付时间"""
        flag = False
        remark = ""
        status_sub_title_element = get_element(
            driver=driver, locator=UILocatorRegx.order_status_sub_title.value.get("locator"),
            regx=UILocatorRegx.order_status_sub_title.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if status_sub_title_element:
            sub_title_text = status_sub_title_element.text.strip()
            # 使用 findall 获取所有匹配项
            time_match = re.search(r"(\d{2}:\d{2})", sub_title_text)
            if time_match:
                time_str = time_match.group(1)
                logger.info("从订单获取到的过期时间为：{}".format(time_str))
                is_later = is_later_than_current_time(time_str=time_str, seconds=seconds)
                if is_later is False:
                    flag = True
                    remark = "支付时间少于{}秒".format(seconds)
                    logger.warning(remark)
                    return flag, remark
            else:
                remark = "从文案<{}>中没有获取订单过期时间".format(sub_title_text)
                logger.warning(remark)
        else:
            remark = "从订单详情页面中未找到订单过期时间元素"
            logger.warning(remark)
        return flag, remark

    @classmethod
    def is_wallet_disable(cls, driver: webdriver, order_id: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        wallet_disable_element = get_element(
            driver=driver, locator=UILocatorRegx.wallet_disable.value.get("locator"),
            regx=UILocatorRegx.wallet_disable.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if wallet_disable_element:
            logger.warning("当前订单: {} 钱包不可用，需要切换至其他支付方式".format(order_id))
            return True
        else:
            return False

    @classmethod
    def get_wallet_balance(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> Decimal:
        wallet_balance = "0.00"
        wallet_balance_element = get_element(
            driver=driver, locator=UILocatorRegx.wallet_balance.value.get("locator"),
            regx=UILocatorRegx.wallet_balance.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if wallet_balance_element:
            text = wallet_balance_element.text.strip()
            logger.info("获取账号礼品卡{}".format(text))
            wallet_balance = text.split("¥")[-1]
        return Decimal(wallet_balance)

    @classmethod
    def click_use_wallet(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        use_wallet_switch = get_element(
            driver=driver, locator=UILocatorRegx.use_wallet.value.get("locator"),
            regx=UILocatorRegx.use_wallet.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if use_wallet_switch:
            use_wallet_switch.click()
            logger.info("选择使用钱包支付")
            return True
        else:
            return False

    @classmethod
    def click_wallet_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.wallet_immediately_payment.value.get("locator"),
            regx=UILocatorRegx.wallet_immediately_payment.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击钱包【立即支付】")
            return True
        else:
            return False

    @classmethod
    def click_use_yeepay2b(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        use_yeepay2b_switch = get_element(
            driver=driver, locator=UILocatorRegx.use_yeepay2b_pyament.value.get("locator"),
            regx=UILocatorRegx.use_yeepay2b_pyament.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if use_yeepay2b_switch:
            use_yeepay2b_switch.click()
            logger.info("选择使用易宝会员支付")
            return True
        else:
            return False

    @classmethod
    def click_yeepay2b_immediately_payment(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        immediately_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_immediately_payment.value.get("locator"),
            regx=UILocatorRegx.yeepay2b_immediately_payment.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if immediately_payment_button:
            immediately_payment_button.click()
            logger.info("点击【易宝支付】按钮")
            return True
        else:
            return False

    @classmethod
    def enter_payment_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0,
                               **kwargs) -> bool:
        password_input_box = get_element(
            driver=driver, locator=UILocatorRegx.password_input_box.value.get("locator"),
            regx=UILocatorRegx.password_input_box.value.get("regx"), sleep=sleep, loop=loop, **kwargs
        )
        if password_input_box:
            if not isinstance(password, str):
                password = str(password)
            for char in password:
                is_success = send_keys(element=password_input_box, value=char, loop=loop, sleep=sleep, **kwargs)
                if is_success is False:
                    return False
                # 可选：添加一个短暂的延迟，模拟更接近人类的输入速度
                time.sleep(0.5)
            return True
        else:
            logger.warning("没有出现输入密码的弹框")
            return False

    @classmethod
    def is_wallet_payment_success(cls, driver: webdriver, platform: str, order_id: str, loop: int = 1, sleep: float = 0,
                                  **kwargs) -> bool:
        order_status_element = get_element(
            driver=driver, locator=UILocatorRegx.wallet_payment_result_status.value.get("locator"),
            regx=UILocatorRegx.wallet_payment_result_status.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if order_status_element:
            text = order_status_element.text.strip()
            if "出票中" in text or "已出票" in text:
                logger.info("{}订单：{}，钱包支付成功".format(platform, order_id))
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def enter_yeepay2b_account(cls, driver: webdriver, account: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        local_url = url_map.get("yeepay2b_cash_desk")
        is_success, current_url = is_switch_latest_page(driver=driver, latest_page=local_url, loop=loop, sleep=sleep)
        if is_success is True:
            input_box = get_element(
                driver=driver, locator=UILocatorRegx.yeepay2b_accout_input_box.value.get("locator"),
                regx=UILocatorRegx.yeepay2b_accout_input_box.value.get("regx"), loop=loop, sleep=sleep, **kwargs
            )
            if input_box:
                # 模拟键盘操作清空输入框内容
                input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
                input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
                input_box.send_keys('{}'.format(account))
                logger.info("输入的易宝会员账号：{}".format(account))
                return True
            else:
                return False
        else:
            logger.warn("当前页: {}，不是易宝支付收银台页".format(current_url))
            return False

    @classmethod
    def enter_yeepay2b_password(cls, driver: webdriver, password: str, loop: int = 1, sleep: float = 0,
                                **kwargs) -> bool:
        input_box = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_password_input_box.value.get("locator"),
            regx=UILocatorRegx.yeepay2b_password_input_box.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if input_box:
            # 模拟键盘操作清空输入框内容
            input_box.send_keys(Keys.CONTROL + "a")  # 选中输入框中的所有内容
            input_box.send_keys(Keys.BACKSPACE)  # 删除选中的内容
            input_box.send_keys('{}'.format(password))
            logger.info("输入的易宝会员账号密码：{}".format(password))
            return True
        else:
            return False

    @classmethod
    def click_yeepay2b_payment_next(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        next_button = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_payment_next_button.value.get("locator"),
            regx=UILocatorRegx.yeepay2b_payment_next_button.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if next_button:
            next_button.click()
            logger.info("易宝支付收银台界面点击【下一步】")
            return True
        else:
            return False

    @classmethod
    def is_yeepay2b_payment_success(cls, driver: webdriver, platform: str, order_id: str, loop: int = 1,
                                    sleep: float = 0, **kwargs) -> bool:
        payment_success_element = get_element(
            driver=driver, locator=UILocatorRegx.yeepay2b_payment_success.value.get("locator"),
            regx=UILocatorRegx.yeepay2b_payment_success.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if payment_success_element:
            logger.info("{}订单：{}，易宝会员支付成功".format(platform, order_id))
            return True
        submit_payment_result_element = get_element(
            driver=driver, locator=UILocatorRegx.submit_payment_result.value.get("locator"),
            regx=UILocatorRegx.submit_payment_result.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if submit_payment_result_element:
            logger.info("{}订单：{}，易宝会员支付成功".format(platform, order_id))
            return True
        else:
            return False

    @classmethod
    def click_more_bank_card(cls, driver: webdriver, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        more_bank_card_expand = get_element(
            driver=driver, locator=UILocatorRegx.more_bank_card.value.get("locator"),
            regx=UILocatorRegx.more_bank_card.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if more_bank_card_expand:
            more_bank_card_expand.click()
            logger.info("点击【更多银行卡】")
            return True
        else:
            return False

    @classmethod
    def click_bank_card(cls, driver: webdriver, payment_card: str, loop: int = 1, sleep: float = 0, **kwargs) -> bool:
        bank_card_regx = UILocatorRegx.bank_card.value.get("regx")
        bank_card_regx = bank_card_regx.format(payment_card)
        bank_card_element = get_element(
            driver=driver, locator=UILocatorRegx.more_bank_card.value.get("locator"),
            regx=bank_card_regx, loop=loop, sleep=sleep, **kwargs
        )
        if bank_card_element:
            bank_card_element.click()
            logger.info("点击选择【{}】银行卡".format(payment_card))
            return True
        else:
            return False

    @classmethod
    def click_bank_card_payment(cls, driver: webdriver, payment_card: str, loop: int = 1, sleep: float = 0,
                                **kwargs) -> bool:
        bank_card_payment_button = get_element(
            driver=driver, locator=UILocatorRegx.bank_card_payment.value.get("locator"),
            regx=UILocatorRegx.bank_card_payment.value.get("regx"), loop=loop, sleep=sleep, **kwargs
        )
        if bank_card_payment_button:
            bank_card_payment_button.click()
            logger.info("点击【银行卡支付】，接下来会出现短信验证码输入框")
            return True
        else:
            return False
