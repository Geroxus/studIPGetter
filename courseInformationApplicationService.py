from emailCollectionService import getAllEmails
from main import session, URL_SELECT_ALL_SEMESTERS, URL_GET_COURSE_MEMBERS_NOID
from util import getCourseId, getAllStudentProfileLinks, cleanEmailList


def printEmailsForAllParticipantsInCourse():
    courseName = input("What course are you looking for?\n")
    courseId = getCourseId(session.get(URL_SELECT_ALL_SEMESTERS), courseName)
    allStudentProfileLinks = getAllStudentProfileLinks(session.get(URL_GET_COURSE_MEMBERS_NOID + courseId))
    print("get emails now")
    allStudentEmails: list[str] = getAllEmails(session, allStudentProfileLinks)
    cleanEmailList(allStudentEmails)
    for email in allStudentEmails:
        print(f"%s;" % email, end="")
