import requests as requests

from emailCollectionService import getAllEmails
from loginService import login
from util import getCourseId, getAllStudentProfileLinks, cleanEmailList

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"

URL_SELECT_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

URL_GET_COURSE_MEMBERS_NOID = "https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid="

if __name__ == '__main__':

    with requests.Session() as session:

        if login(session, URL_LOGIN):

            courseName = input("What course are you looking for?\n")
            courseId = getCourseId(session.get(URL_SELECT_ALL_SEMESTERS), courseName)

            allStudentProfileLinks = getAllStudentProfileLinks(session.get(URL_GET_COURSE_MEMBERS_NOID + courseId))
            print("get emails now")
            allStudentEmails: list[str] = getAllEmails(session, allStudentProfileLinks)

            cleanEmailList(allStudentEmails)

            for email in allStudentEmails:
                print(f"%s;" % email, end="")

            exit(0)

    exit(1)
