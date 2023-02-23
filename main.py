import requests as requests

from login import login

URL_LOGIN = "https://e-learning.tuhh.de/studip/index.php?again=yes"

URL_SELECT_ALL_SEMESTERS = "https://e-learning.tuhh.de/studip/dispatch.php/my_courses/set_semester?sem_select=all"

if __name__ == '__main__':

    with requests.Session() as session:

        if login(session, loginUrl=URL_LOGIN):
            # session.get(URL_SELECT_ALL_SEMESTERS)
            exit(0)

    exit(1)
