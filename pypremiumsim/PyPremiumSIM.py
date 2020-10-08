#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup


class PremiumSimSession:

    def __init__(self):
        self.__premiumsim_service_url = "https://service.premiumsim.de"
        self.__session = requests.session()
        self.__parser_name = "html.parser"

        headers = {'Connection': 'keep-alive',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept': '*/*',
                   'User-agent': 'Mozilla/5.0 (comptabile)'}

        self.__session.headers = headers

    def __login_page_url(self):
        return self.__premiumsim_service_url + "/"

    def __login_validation_url(self):
        return self.__premiumsim_service_url + "/public/login_check"

    def __get_csrf_for_login(self, login_page_content):
        login_page_soup = BeautifulSoup(login_page_content, self.__parser_name)
        csrf = login_page_soup.find(id="SendPasswordNotificationType_csrf_token")['value']

        return csrf

    def __handle_login_response(self, login_result_content, user):
        expectedLoginString = "<span id=\"LoginName1\">" + user + "</span>"
        loginFailedString = "Your credentials are incorrect."

        if expectedLoginString.encode() in login_result_content:
            return True
        elif loginFailedString.encode() in login_result_content:
            raise IOError("Your credentials are incorrect.")
        else:
            raise IOError("Unknown error.")

    def try_login(self, user, passwd):
        login_page_response = self.__session.get(self.__login_page_url())
        login_page_soup = BeautifulSoup(login_page_response.content, self.__parser_name)

        login_send_url = self.login_url()
        try:
            login_form_response = self.__session.get(login_send_url)
            soup = BeautifulSoup(login_form_response.content, "html.parser")

            VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
            VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
            EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']
            EVENTTARGET = soup.find(id="__EVENTTARGET")['value']
            EVENTARGUMENT = soup.find(id="__EVENTARGUMENT")['value']
            SCROLLPOSITIONX = soup.find(id="__SCROLLPOSITIONX")['value']
            SCROLLPOSITIONY = soup.find(id="__SCROLLPOSITIONY")['value']
            VIEWSTATEENCRYPTED = soup.find(id="__VIEWSTATEENCRYPTED")['value']
            PREVIOUSPAGE = soup.find(id="__PREVIOUSPAGE")['value']

            login_details = {
                "__VIEWSTATE": VIEWSTATE,
                "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": EVENTVALIDATION,
                "__EVENTTARGET": EVENTTARGET,
                "__EVENTARGUMENT": EVENTARGUMENT,
                "__SCROLLPOSITIONX": SCROLLPOSITIONX,
                "__SCROLLPOSITIONY": SCROLLPOSITIONY,
                "__VIEWSTATEENCRYPTED": VIEWSTATEENCRYPTED,
                "__PREVIOUSPAGE": PREVIOUSPAGE,
                'ctl00$ContentPlaceHolder1$UserName': user,
                'ctl00$ContentPlaceHolder1$Password': passwd,
                'ctl00$ContentPlaceHolder1$btnlogin': "Login",
                'AjaxScriptManager_HiddenField': '',
                '_URLLocalization_Var001': False}

            login_response = self.__session.post(login_send_url, data=login_details)
            return self.__handle_login_response(login_response.content, user)

        except requests.exceptions.ConnectionError:
            # The most likely failure case is that we're offline so fail gracefully here
            return False

