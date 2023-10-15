""" This module defines control flow for certain actions to be called from the main file of this
project
"""
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
        print(f"${email};", end="")


def check_availability_of_courses(session: requests.Session, args: tuple[str]) -> None:
    """ checks whether a course is available right now. Uses the global search
    :param session:
    :param args:
    :return:
    """
    print("getting courses availability duh")
    print(args)
    for arg in args:
        # the URL ist that easy.
        url = (f"https://e-learning.tuhh.de/studip/dispatch.php/search/globalsearch?q="
               f"${arg}#GlobalSearchCourses")
        print(url)
        search_course_response = session.get(url)
        # but the response appears to be different. Thus it seems I am in need of a need parser
        print(get_course_id(search_course_response, arg))
