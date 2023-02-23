import json

from requests import Response


def getCourseId(response: Response, courseName):
    for line in response.text.splitlines():
        myCoursesData: dict
        jsonNameInPageSource = "window.STUDIP.MyCoursesData = {\"courses\":"
        if jsonNameInPageSource in line:
            prefixEndPos = len(jsonNameInPageSource)
            suffixStartPos = line.find("\"groups\":")
            myCoursesData = json.loads(line[prefixEndPos:suffixStartPos - 1])
            for course in myCoursesData.values():
                if courseName in course["name"]:
                    return course["id"]
    return False


def stringBetween(string: str, before: str, after: str) -> str:
    return string.split(before)[1].split(after)[0]


def getAllStudentProfileLinks(response: Response) -> list[str]:
    result: list[str] = []
    between = stringBetween(response.text, "Studierende", "</tbody>").split("<tbody>")[1]
    for line in between.splitlines():
        if "profile" in line:
            result.append(stringBetween(line, "<a href=\"", "\" >"))
    return result
