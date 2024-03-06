""" async module collecting emails with a specific format from some html response.
Makes web calls itself
"""
import asyncio
import json

import requests
from requests import Response

from util import string_between


def print_emails_for_all_participants_in_course(session: requests.Session, args: tuple[str]) \
        -> None:
    """ uses "my_courses" to find course
    :param session:
    :param args:
    :return:
    """
    course_name: str = args[0]
    course_id = get_course_id(session.get("https://e-learning.tuhh.de/studip/dispatch.php/"
                                          "my_courses/set_semester?sem_select=all"), course_name)
    all_student_profile_links = get_all_student_profile_links(session
                                                              .get(
        f"https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid={course_id}"))
    print("get emails now")
    all_student_emails: list[str] = get_all_emails(session, all_student_profile_links)
    clean_email_list(all_student_emails)
    for email in all_student_emails:
        print(f"{email};", end="")


def get_all_emails(session: requests.Session, student_profile_links: list[str]) -> list[str]:
    """ only method that is supposed to be called from the outside.
    :param session:
    :param student_profile_links:
    :return: list with the emails found behind all student_profile_links
    """
    email_list: list[str] = []
    asyncio.run(collect_all_emails(session, student_profile_links, email_list))
    return email_list


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


def get_course_id(response: Response, course_name) -> str:
    """ searches through the html of the response.
    Only works when the response is from the "my_courses" page
    :param response:
    :param course_name:
    :return: the id of the course as a str
    """
    for line in response.text.splitlines():
        my_courses_data: dict
        json_name_in_page_source = "window.STUDIP.MyCoursesData = {\"courses\":"
        if json_name_in_page_source in line:
            prefix_end_pos = len(json_name_in_page_source)
            suffix_start_pos = line.find("\"groups\":")
            my_courses_data = json.loads(line[prefix_end_pos:suffix_start_pos - 1])
            for course in my_courses_data.values():
                if course_name in course["name"]:
                    return course["id"]
    raise RuntimeError(
        f"getCourseId|courseName={course_name}|response.status_code={response.status_code}")


def get_all_student_profile_links(response: Response) -> list[str]:
    """parses the provided response
    :param response:
    :return: list with links to profiles
    """
    result: list[str] = []
    between = string_between(response.text, "Studierende", "</tbody>").split("<tbody>")[1]
    for line in between.splitlines():
        if "profile" in line:
            result.append(string_between(line, "<a href=\"", "\" >"))
    return result


def clean_email_list(all_student_emails: list[str]):
    """ performs simple cleanups on the list of emails
    :param all_student_emails:
    :return:
    """
    counter: int = 0
    for email in all_student_emails:
        if email == "no-mail":
            all_student_emails.remove(email)
            counter = counter + 1
    print(f"There have been {counter} Students without an E-Mail")
