import aiohttp
from bs4 import BeautifulSoup
import re
from . import DataVolume

class PremiumSimSession:

    def __init__(self):
        self.__premiumsim_service_url = "https://service.premiumsim.de"
        self.__session = aiohttp.ClientSession()  # Create session here
        self.__parser_name = "html.parser"

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.__session.close()  # Close session

    def __login_page_url(self):
        return self.__premiumsim_service_url + "/"

    def __login_validation_url(self):
        return self.__premiumsim_service_url + "/public/login_check"

    def __data_usage_url(self):
        return self.__premiumsim_service_url + "/mytariff/invoice/showGprsDataUsage"

    async def __login_page_tokens(self, login_page_response):
        csrf = self.__get_csrf_for_login(await login_page_response.text())
        sid = login_page_response.cookies["_SID"].value

        return csrf, sid

    def __get_csrf_for_login(self, login_page_content):
        login_page_soup = BeautifulSoup(login_page_content, self.__parser_name)
        csrf = login_page_soup.find(id="UserLoginType__token")['value']

        return csrf

    def __handle_login_response(self, login_result_content):
        expectedLoginString = u"Zeit neu starten"
        loginFailedString = u"Die Angaben sind nicht korrekt."

        if expectedLoginString.encode() in login_result_content:
            return True
        elif loginFailedString.encode() in login_result_content:
            raise IOError("Your credentials are incorrect.")
        else:
            raise IOError("Unknown error.")

    async def try_login(self, user, passwd):
        async with self.__session.get(self.__login_page_url()) as login_page_response:
            captured_csrf, captured_sid = await self.__login_page_tokens(login_page_response)

        payload = {
            'UserLoginType[alias]': user,
            'UserLoginType[password]': passwd,
            'UserLoginType[logindata]': '',
            'UserLoginType[_token]': captured_csrf,
            '_SID': captured_sid
        }

        async with self.__session.post(self.__login_validation_url(), data=payload) as login_validation_response:
            login_result_content = await login_validation_response.read()
            return self.__handle_login_response(login_result_content)

    def __data_pack_description_to_numeric_gigabytes(self, data_pack_description):
        matches = re.search(r'(\d+,\d+)\s(\w+)', data_pack_description.replace("\n", "").strip())

        size = matches.group(1).replace(",", ".")
        unit = matches.group(2)

        if unit == "GB":
            return float(size)
        elif unit == "MB":
            return float(size) / 1024

    def __percent_value_to_numeric(self, percentage_text):
        match = re.search(r"left:\s*([\d.]+)%", percentage_text)
        return float(match.group(1))

    def __handle_data_usage_response(self, data_usage_page_content):
        data_usage_soup = BeautifulSoup(data_usage_page_content, self.__parser_name)

        current_month = data_usage_soup.find(id="tab-cur")

        # Available data volume
        data_packs_div = current_month.find(class_="e-data_usage_meter-legend inclusive")
        total_data_packs_gb = self.__data_pack_description_to_numeric_gigabytes(data_packs_div.text)
        
        # Used data volume
        data_usage_div = current_month.find(class_="e-data_usage_meter-legend usage")
        gb_used = self.__data_pack_description_to_numeric_gigabytes(data_usage_div.text)

        percent_used_div = current_month.find(class_="e-data_usage_meter-used_data block relative")
        percent_used = self.__percent_value_to_numeric(percent_used_div["style"])

        data_usage_result = DataVolume.DataVolume(total_data_packs_gb, gb_used, percent_used)
        return data_usage_result

    async def current_month_data_usage(self):
        async with self.__session.get(self.__data_usage_url()) as data_usage_response:
            data_usage_content = await data_usage_response.text()
            return self.__handle_data_usage_response(data_usage_content)