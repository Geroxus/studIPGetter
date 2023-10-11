import requests

from emailCollectionService import getAllEmails
from util import getCourseId, getAllStudentProfileLinks, cleanEmailList

URL_SELECT_MY_COURSES_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

URL_GET_COURSE_MEMBERS_NOID = "https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid="


def printEmailsForAllParticipantsInCourse(session: requests.Session, args: tuple[str]) -> None:
    courseName: str = args[0]
    courseId = getCourseId(session.get(URL_SELECT_MY_COURSES_ALL_SEMESTERS), courseName)
    allStudentProfileLinks = getAllStudentProfileLinks(session.get(URL_GET_COURSE_MEMBERS_NOID + courseId))
    print("get emails now")
    allStudentEmails: list[str] = getAllEmails(session, allStudentProfileLinks)
    cleanEmailList(allStudentEmails)
    for email in allStudentEmails:
        print(f"%s;" % email, end="")


def checkAvailabilityOfCourses(session: requests.Session, args: tuple[str]) -> None:
    print("getting courses availability duh")
    print(args)
    for arg in args:
        # the URL ist that easy.
        url = f"https://e-learning.tuhh.de/studip/dispatch.php/search/globalsearch?q=${arg}#GlobalSearchCourses"
        print(url)
        searchCourseResponse = session.get(url)
        # but the response appears to be different. Thus it seems I am in need of a need parser
        print(getCourseId(searchCourseResponse, arg))
