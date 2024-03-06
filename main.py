"""main"""
import sys
from typing import Callable
from sys import argv

import requests

from course_information_service import check_availability_of_courses
from email_collection_service import print_emails_for_all_participants_in_course
from login_service import login

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"


def execute_in_session(funtion: Callable, *args: str):
    """wraps the callable in a with session body and performs login
    :param funtion:
    :param args:
    :return:
    """
    with requests.Session() as session:
        if login(session, URL_LOGIN):
            funtion(session, args)
            sys.exit(0)
    sys.exit(1101)


def print_help():
    program_name = "main.py"  # TODO make it generate this name programmatically
    help_string = (f"{program_name} [COMMAND] [ARGS...]\n"
                   f"Available commands are:\n"
                   f"courseParticipantMails\n"
                   f"courseAvailabilityCheck\n")
    print(help_string)


if __name__ == '__main__':
    if len(argv) == 1:
        print("you have to enter something to do")
        sys.exit(1001)
    else:
        if argv[1] == "help":
            print_help()
        elif argv[1] == "courseParticipantMails" and len(argv) == 3:
            execute_in_session(print_emails_for_all_participants_in_course, argv[2])
        elif argv[1] == "courseAvailabilityCheck" and len(argv) == 3:
            execute_in_session(check_availability_of_courses, *argv[2].split(","))
        else:
            print("this is not a valid command")
            sys.exit(1011)
