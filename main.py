from getpass import getpass

import requests as requests

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"

URL_SELECT_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"


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


if __name__ == '__main__':

    with requests.Session() as session:

        if login(session, loginUrl=URL_LOGIN):
            # session.get(URL_SELECT_ALL_SEMESTERS)
            exit(0)

    exit(1)
