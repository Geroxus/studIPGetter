import asyncio

import requests as requests

from util import stringBetween


async def addEmailToList(session: requests.Session, profileLink: str, emailList: list[str]):
    response = session.get(profileLink)
    email = stringBetween(response.text, "@tuhh.de\">", "</a>") if "E-Mail:" in response.text else "no-mail"

    email = email.replace("\n", "")
    email = email.strip()

    emailList.append(email)


async def collectAllEmails(session: requests.Session, studentProfileLinks: list[str], emailList: list[str]):
    async with asyncio.TaskGroup() as tg:
        for profileLink in studentProfileLinks:
            tg.create_task(addEmailToList(session, profileLink, emailList))


def getAllEmails(session: requests.Session, studentProfileLinks: list[str]) -> list[str]:
    emailList: list[str] = []
    asyncio.run(collectAllEmails(session, studentProfileLinks, emailList))
    return emailList
