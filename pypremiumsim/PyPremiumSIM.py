#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import re
from . import DataVolume
from decimal import Decimal

class PremiumSimSession:

    def __init__(self):
        self.__premiumsim_service_url = "https://service.premiumsim.de"
        self.__session = requests.session()
        self.__parser_name = "html.parser"

    def __login_page_url(self):
        return self.__premiumsim_service_url + "/"

    def __login_validation_url(self):
        return self.__premiumsim_service_url + "/public/login_check"

    def __data_usage_url(self):
        return self.__premiumsim_service_url + "/mytariff/invoice/showGprsDataUsage"

    def __login_page_tokens(self, login_page_response):
        csrf = self.__get_csrf_for_login(login_page_response.content)
        sid = login_page_response.cookies["_SID"]

        return csrf, sid

    def __get_csrf_for_login(self, login_page_content):
        login_page_soup = BeautifulSoup(login_page_content, self.__parser_name)
        csrf = login_page_soup.find(id="UserLoginType_csrf_token")['value']

        return csrf

    def __handle_login_response(self, login_result_content):
        expectedLoginString = "Willkommen in Ihrer persönlichen Servicewelt"
        loginFailedString = "Die Angaben sind nicht korrekt."

        if expectedLoginString.encode() in login_result_content:
            return True
        elif loginFailedString.encode() in login_result_content:
            raise IOError("Your credentials are incorrect.")
        else:
            raise IOError("Unknown error.")

    def try_login(self, user, passwd):
        login_page_response = self.__session.get(self.__login_page_url())
        captured_csrf, captured_sid = self.__login_page_tokens(login_page_response)

        try:
            payload = {
                'UserLoginType[alias]': user,
                'UserLoginType[password]': passwd,
                'UserLoginType[logindata]': '',
                'UserLoginType[csrf_token]': captured_csrf,
                '_SID': captured_sid
            }

            login_validation_request = requests.Request('POST',  self.__login_validation_url(), data=payload)
            prepared_login_request = self.__session.prepare_request(login_validation_request)

            login_validation_response = self.__session.send(prepared_login_request)

            return self.__handle_login_response(login_validation_response.content)

        except requests.exceptions.ConnectionError:
            # The most likely failure case is that we're offline so fail gracefully here
            return False

    def __data_pack_description_to_numeric_gigabytes(self, data_pack_description):
        matches = re.search(r'(\d+,\d+)\s(\w+)', data_pack_description.replace("\n", "").strip())

        size = matches.group(1).replace(",", ".")
        unit = matches.group(2)

        if unit == "GB":
            return Decimal(size)
        elif unit == "MB":
            return Decimal(size) / 1024


    def __handle_data_usage_response(self, data_usage_page_content):
        data_usage_soup = BeautifulSoup(data_usage_page_content, self.__parser_name)

        current_month = data_usage_soup.find(id="currentMonth")
        data_packs = current_month.find(text="Verfügbares Datenvolumen").parent.parent

        total_data_packs = Decimal()

        for child_div in data_packs.find_all('div'):
            pack_gb_size = self.__data_pack_description_to_numeric_gigabytes(child_div.text)
            total_data_packs = total_data_packs + pack_gb_size

        return DataVolume("1.4", "1.2", "1.3")


    def get_data_usage(self):
        data_usage_response = self.__session.get(self.__data_usage_url())

        print(data_usage_response.content)

