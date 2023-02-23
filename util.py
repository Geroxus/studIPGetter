import json

from requests import Response

from main import courseName


def getCourseId(response: Response):
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
