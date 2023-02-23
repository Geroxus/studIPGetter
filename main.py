import requests as requests

from login import login
from util import getCourseId

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"

URL_SELECT_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

URL_GET_COURSE_MEMBERS_NOID = "https://e-learning.tuhh.de/studip/dispatch.php/course/members?cid="

if __name__ == '__main__':

    with requests.Session() as session:

        if login(session, URL_LOGIN):

            response = session.get(URL_SELECT_ALL_SEMESTERS)
            courseName = input("What course are you looking for?\n")
            courseId = getCourseId(response)
            response = session.get(URL_GET_COURSE_MEMBERS_NOID + courseId)
            if courseId:
                exit(0)

    exit(1)
