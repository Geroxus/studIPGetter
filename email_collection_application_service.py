""" async module collecting emails with a specific format from some html response.
Makes web calls itself
"""
import asyncio

import requests

from util import string_between


async def add_email_to_list(session: requests.Session, profile_link: str, email_list: list[str]) \
        -> None:
    """makes a request to the profile_link within the provided session.
    Writes result into the provided email_list
    :param session: 
    :param profile_link: 
    :param email_list: 
    :return: 
    """
    response = session.get(profile_link)
    email = string_between(response.text,
                          "@tuhh.de\">", "</a>") if "E-Mail:" in response.text else "no-mail"

    email = email.replace("\n", "")
    email = email.strip()

    email_list.append(email)


async def collect_all_emails(session: requests.Session, student_profile_links: list[str],
                             email_list: list[str]):
    """async dispatcher
    :param session:
    :param student_profile_links:
    :param email_list:
    :return:
    """
    async with asyncio.TaskGroup() as tg:
        for profile_link in student_profile_links:
            tg.create_task(add_email_to_list(session, profile_link, email_list))


def get_all_emails(session: requests.Session, student_profile_links: list[str]) -> list[str]:
    """ only method that is supposed to be called from the outside.
    :param session:
    :param student_profile_links:
    :return: list with the emails found behind all student_profile_links
    """
    email_list: list[str] = []
    asyncio.run(collect_all_emails(session, student_profile_links, email_list))
    return email_list
