""" This module defines control flow for certain actions to be called from the main file of this
project
"""
import json

import requests

from email_collection_application_service import get_all_emails
from util import get_course_id, get_all_student_profile_links, clean_email_list

URL_SELECT_MY_COURSES_ALL_SEMESTERS = \
    "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

URL_GET_COURSE_MEMBERS_NOID = "https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid="


def print_emails_for_all_participants_in_course(session: requests.Session, args: tuple[str]) \
        -> None:
    """ uses "my_courses" to find course
    :param session:
    :param args:
    :return:
    """
    course_name: str = args[0]
    course_id = get_course_id(session.get(URL_SELECT_MY_COURSES_ALL_SEMESTERS), course_name)
    all_student_profile_links = get_all_student_profile_links(
        session.get(URL_GET_COURSE_MEMBERS_NOID + course_id))
    print("get emails now")
    all_student_emails: list[str] = get_all_emails(session, all_student_profile_links)
    clean_email_list(all_student_emails)
    for email in all_student_emails:
        print(f"{email};", end="")


def check_availability_of_courses(session: requests.Session, args: tuple[str]) -> None:
    """ checks whether a course is available right now. Uses the global search
    :param session:
    :param args:
    :return:
    """
    print("getting availability for:", args)
    for course in args:
        print(course)
        zugang: dict = {
            'gesperrt': 0,
            'password': 0,
            'zeit': 0,
            'erlaubt': 0,
            'unbekannt': 0,
        }
        url = (f"https://e-learning.tuhh.de/studip/dispatch.php/globalsearch/find/100?search="
               f"{course}&filters=%7B%22category%22%3A%22show_all_"
               f"categories%22%2C%22semester%22%3A%22%22%7D")
        search_course_response = session.get(url)
        content = json.loads(search_course_response.text)["GlobalSearchCourses"]["content"]
        print("nr of courses found:", len(content))
        for item in content:
            if "23/24" in item["date"]:
                # hier soll vor allem eine unterscheidung zu aktuellem semester stattfinden!
                pass
            url_course = (f"https://e-learning.tuhh.de/studip/dispatch.php/course/details/index/"
                          f"{item['id']}")
            text = session.get(url_course).text
            if any("Anmeldung gesperrt" in x for x in text.splitlines()):
                zugang['gesperrt'] += 1
            elif any("Zeitgesteuerte Anmeldung" in x for x in text.splitlines()):
                zugang['zeit'] += 1
            elif any("Anmeldung mit Passwort" in x for x in text.splitlines()):
                zugang['password'] += 1
            else:
                attempt_apply(session, item, zugang)
        print(zugang)


def attempt_apply(session: requests.Session, item: dict, zugang: dict) -> None:
    """
    attempts to apply for a course in the item parameter but does not actually go through with
    application
    :param session:
    :param item:
    :param zugang:
    :return:
    """
    url_apply = (f"https://e-learning.tuhh.de/studip/dispatch.php/course/enrolment/apply/"
                 f"{item['id']}")
    text = session.get(url_apply).text.splitlines()
    if any("nicht erfolgreich" in x for x in text):
        rule: str = ''
        for i, e in enumerate(text):
            if "messagebox_details" in e:
                rule = text[i+2]
        print("nicht erfolgreich", {
            'id': item['id'],
            'name': item['name'],
            'rule': rule.strip()
        })
    elif any("wirklich anmelden" in x for x in text):
        zugang['erlaubt'] += 1
        # print("anmeldung erlaubt", item['name'])
    else:
        zugang['unbekannt'] += 1
        print("unbekannter Zustand")
