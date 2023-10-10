import requests as requests

from sys import argv
from courseInformationApplicationService import printEmailsForAllParticipantsInCourse
from loginService import login

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"

if __name__ == '__main__':

    if len(argv) == 1:
        print("you have to enter something to do")
        exit(1)
    else:
        if argv[1] == "courseParticipantMails" and len(argv) == 3:
            courseName = argv[2]
        else:
            print("this is not a valid command")
            exit(1)
        for arg in argv:
            print(arg)

    with requests.Session() as session:

        if login(session, URL_LOGIN):

            printEmailsForAllParticipantsInCourse(session, courseName)

            exit(0)

    exit(1)
