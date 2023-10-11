from typing import Callable

import requests as requests

from sys import argv
from courseInformationApplicationService import printEmailsForAllParticipantsInCourse
from loginService import login

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"


def executeInSession(funtion: Callable, *args: str):
    with requests.Session() as session:
        if login(session, URL_LOGIN):
            funtion(session, args)
            exit(0)
    exit(1101)


if __name__ == '__main__':

    if len(argv) == 1:
        print("you have to enter something to do")
        exit(1001)
    else:
        if argv[1] == "courseParticipantMails" and len(argv) == 3:
            courseName = argv[2]
            executeInSession(printEmailsForAllParticipantsInCourse, argv[2])
        elif argv[1] == "courseAvailabilityCheck" and len(argv) > 2:
            print("new command, wip")
            exit(0)
        else:
            print("this is not a valid command")
            exit(1011)
        for arg in argv:
            print(arg)


