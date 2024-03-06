import json
from unittest import TestCase, mock
from unittest.mock import patch

import requests
from requests import Session

from course_information_service import auto_apply_to_courses, get_courses_for_name


class Test(TestCase):
    response_dict = {"GlobalSearchMyCourses": {"name": "Meine Veranstaltungen",
                                               "fullsearch": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchMyCourses",
                                               "content": [
                                                   {"id": "5106a5e9dfcd3df4845c68535cec666a",
                                                    "number": "lv880_s23",
                                                    "name": "Vorlesung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark> (VL)",
                                                    "url": "https:\/\/e-learning.tuhh.de\/studip\/seminar_main.php?cid=5106a5e9dfcd3df4845c68535cec666a",
                                                    "date": "SoSe 23",
                                                    "dates": "Mi. 11:30 - 14:00 (w\u00f6chentlich), \nTermine am Mittwoch, 05.07.2023 11:30 ... <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/5106a5e9dfcd3df4845c68535cec666a\">(mehr)<\/a>",
                                                    "has_children": "false", "children": [],
                                                    "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=mgdcl\">Christian L\u00fcthje<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=pwacr\">Prof. Dr. Christian Ringle<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/5106a5e9dfcd3df4845c68535cec666a\">... (mehr) <\/a>",
                                                    "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchMyCourses",
                                                    "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"}],
                                               "more": "false", "plus": "false"},
                     "GlobalSearchCourses": {"name": "Veranstaltungen",
                                             "fullsearch": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                             "content": [{"id": "bdefc339d26547c8f48d6a3d62788d51",
                                                          "number": "lv2229_s22",
                                                          "name": "PBL -Projekt-\/problembasierte Lehrveranstaltung: Fachdidaktik <mark>Betriebswirtschaftslehre<\/mark>",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/bdefc339d26547c8f48d6a3d62788d51",
                                                          "date": "SoSe 22", "dates": "",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=pbbkn\">Prof. Dr. S\u00f6nke Knutzen<\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "e27f0020fe611ec353d8889ecc4a39a5",
                                                          "number": "",
                                                          "name": "Vorlesung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark>",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/e27f0020fe611ec353d8889ecc4a39a5",
                                                          "date": "SoSe 22",
                                                          "dates": "Mi. 11:30 - 14:00 (w\u00f6chentlich), \nTermine am Mittwoch, 13.04.2022 12:30 - 14:00, ... <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/e27f0020fe611ec353d8889ecc4a39a5\">(mehr)<\/a>",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=simtw\">Prof. Dr. Thomas Wrona<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=caz2912\">Lydia Schuster, M. Sc<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/e27f0020fe611ec353d8889ecc4a39a5\">... (mehr) <\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "c5c4316812b687dfaf11715c6e22f2d4",
                                                          "number": "lv880_s22",
                                                          "name": "Vorlesung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark>",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/c5c4316812b687dfaf11715c6e22f2d4",
                                                          "date": "SoSe 22", "dates": "",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=simtw\">Prof. Dr. Thomas Wrona<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=curmm\">Prof. Dr. Matthias Meyer<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/c5c4316812b687dfaf11715c6e22f2d4\">... (mehr) <\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "2b859d30ee270e7044122ec307bc8bac",
                                                          "number": "lv882",
                                                          "name": "\u00dcbung: Projekt Entrepreneurship (Do 14:15 - 15:45) - \u00dcbung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark> (GBWL) [A]",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/2b859d30ee270e7044122ec307bc8bac",
                                                          "date": "SoSe 22",
                                                          "dates": "Do. 14:15 - 15:45 (w\u00f6chentlich)",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=com6019\">Oliver Mork<\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "7dcddb79e32640a45a5ef530cb245ba3",
                                                          "number": "lv882",
                                                          "name": "\u00dcbung: Projekt Entrepreneurship (Do 14:15 - 15:45) - \u00dcbung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark> (GBWL) [B]",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/7dcddb79e32640a45a5ef530cb245ba3",
                                                          "date": "SoSe 22",
                                                          "dates": "Do. 14:15 - 15:45 (w\u00f6chentlich)",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=com6019\">Oliver Mork<\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "1c626a222501fe52e9458f4bdb25e04c",
                                                          "number": "lv882",
                                                          "name": "\u00dcbung: Projekt Entrepreneurship (Do 16:00 - 17:30) - \u00dcbung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark> (GBWL) [A]",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/1c626a222501fe52e9458f4bdb25e04c",
                                                          "date": "SoSe 22",
                                                          "dates": "Do. 16:00 - 17:30 (w\u00f6chentlich)",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=com6019\">Oliver Mork<\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"},
                                                         {"id": "10715a5914c9f0c34c6dad43c60c17a0",
                                                          "number": "lv882",
                                                          "name": "\u00dcbung: Projekt Entrepreneurship (Do 16:00 - 17:30) - \u00dcbung: Grundlagen der <mark>Betriebswirtschaftslehre<\/mark> (GBWL) [B]",
                                                          "url": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/course\/details\/index\/10715a5914c9f0c34c6dad43c60c17a0",
                                                          "date": "SoSe 22",
                                                          "dates": "Do. 16:00 - 17:30 (w\u00f6chentlich)",
                                                          "has_children": "false", "children": [],
                                                          "additional": "<a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=ckt0804\">Prof. Dr. Christoph Ihl<\/a>, <a href=\"https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/profile?username=com6019\">Oliver Mork<\/a>",
                                                          "expand": "https:\/\/e-learning.tuhh.de\/studip\/dispatch.php\/search\/globalsearch?q=Betriebswirtschaftslehre&category=GlobalSearchCourses",
                                                          "admission_state": "",
                                                          "img": "https:\/\/e-learning.tuhh.de\/studip\/pictures\/course\/nobody_medium.png?d=1609406164"}],
                                             "more": "true", "plus": "false"}}

    @patch.object(Session, 'get')
    def test_auto_apply_to_courses(self, session):
        # arrange
        session.get.return_value.text = json.dumps(self.response_dict)
        arg: tuple[dict] = (
            {
                "semester": "SoSe 22",
                "courses": [
                    {
                        "name": "Betriebwirtschaftslehre"
                    }
                ]
            },
        )

        # act
        auto_apply_to_courses(session, arg)

        # no assert, I know. Fuck python testing QQ

    @patch.object(requests.Session, 'get')
    def test_get_courses_for_name(self, session: mock.Mock):
        session.get.return_value.text = json.dumps(self.response_dict)
        get_courses_for_name(session, "Betriebswirtschafslehre")

        session.get.assert_called_with("https://e-learning.tuhh.de/studip/dispatch.php/globalsearch/find/100?search=Betriebswirtschafslehre&filters=%7B%22category%22%3A%22show_all_categories%22%2C%22semester%22%3A%22%22%7D")