"""performs login activities
"""

from getpass import getpass

import requests


def login(s: requests.Session, login_url) -> bool:
    """logs in within provided session and login_url
    requires user input
    :param s:
    :param login_url:
    :return:
    """
    response = s.get(login_url)

    user_name = input("Enter your Username for StudIP: ")
    password = getpass()

    login_ticket = get_login_ticket(response)
    security_token = get_security_token(response)

    payload = {
        "loginname": user_name,
        "password": password,
        "security_token": security_token,
        "login_ticket": login_ticket,
        "resolution": "1920x1080",
        "device_pixel_rate": "1",
        "Login": ""
    }

    return "layout-sidebar" in s.post(login_url, payload).text


def get_login_ticket(response):
    """util method parsing response text
    :param response:
    :return:
    """
    login_ticket_name = "name=\"login_ticket\" value=\""
    login_ticket_location_start = response.text.find(login_ticket_name) + len(login_ticket_name)
    login_ticket = response.text[login_ticket_location_start:login_ticket_location_start + 32]
    return login_ticket


def get_security_token(response):
    """util method parsing response text
    :param response:
    :return:
    """
    sec_token_name = "name=\"security_token\" value=\""
    sec_token_location_start = response.text.find(sec_token_name) + len(sec_token_name)
    security_token = response.text[sec_token_location_start:sec_token_location_start + 44]
    return security_token
