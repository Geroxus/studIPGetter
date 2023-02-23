from getpass import getpass

import requests as requests


def login(s: requests.Session, loginUrl) -> bool:
    response = s.get(loginUrl)

    userName = input("Enter your Username for StudIP: ")
    password = getpass()

    loginTicket = getLoginTicket(response)
    securityToken = getSecurityToken(response)

    payload = {
        "loginname": userName,
        "password": password,
        "security_token": securityToken,
        "login_ticket": loginTicket,
        "resolution": "1920x1080",
        "device_pixel_rate": "1",
        "Login": ""
    }

    return "layout-sidebar" in s.post(loginUrl, payload).text


def getLoginTicket(response):
    loginTicketName = "name=\"login_ticket\" value=\""
    loginTicketLocationStart = response.text.find(loginTicketName) + len(loginTicketName)
    loginTicket = response.text[loginTicketLocationStart:loginTicketLocationStart + 32]
    return loginTicket


def getSecurityToken(response):
    secTokenName = "name=\"security_token\" value=\""
    secTokenLocationStart = response.text.find(secTokenName) + len(secTokenName)
    securityToken = response.text[secTokenLocationStart:secTokenLocationStart + 44]
    return securityToken
