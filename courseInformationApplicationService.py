import requests

from emailCollectionService import getAllEmails
from util import getCourseId, getAllStudentProfileLinks, cleanEmailList

URL_SELECT_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

URL_GET_COURSE_MEMBERS_NOID = "https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid="


def printEmailsForAllParticipantsInCourse(session: requests.Session, courseName: str):
    courseId = getCourseId(session.get(URL_SELECT_ALL_SEMESTERS), courseName)
    allStudentProfileLinks = getAllStudentProfileLinks(session.get(URL_GET_COURSE_MEMBERS_NOID + courseId))
    print("get emails now")
    allStudentEmails: list[str] = getAllEmails(session, allStudentProfileLinks)
    cleanEmailList(allStudentEmails)
    for email in allStudentEmails:
        print(f"%s;" % email, end="")
