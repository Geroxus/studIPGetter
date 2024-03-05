"""diverse helper functions"""
import json

from requests import Response


def get_course_id(response: Response, course_name) -> str:
    """ searches through the html of the response.
    Only works when the response is from the "my_courses" page
    :param response:
    :param course_name:
    :return: the id of the course as a str
    """
    for line in response.text.splitlines():
        my_courses_data: dict
        json_name_in_page_source = "window.STUDIP.MyCoursesData = {\"courses\":"
        if json_name_in_page_source in line:
            prefix_end_pos = len(json_name_in_page_source)
            suffix_start_pos = line.find("\"groups\":")
            my_courses_data = json.loads(line[prefix_end_pos:suffix_start_pos - 1])
            for course in my_courses_data.values():
                if course_name in course["name"]:
                    return course["id"]
    raise RuntimeError(
        f"getCourseId|courseName={course_name}|response.status_code={response.status_code}")


def string_between(string: str, before: str, after: str) -> str:
    """helper function to get a string between two other substrings
    :param string:
    :param before:
    :param after:
    :return:
    """
    return string.split(before)[1].split(after)[0]


def get_all_student_profile_links(response: Response) -> list[str]:
    """parses the provided response
    :param response:
    :return: list with links to profiles
    """
    result: list[str] = []
    between = string_between(response.text, "Studierende", "</tbody>").split("<tbody>")[1]
    for line in between.splitlines():
        if "profile" in line:
            result.append(string_between(line, "<a href=\"", "\" >"))
    return result


def clean_email_list(all_student_emails: list[str]):
    """ performs simple cleanups on the list of emails
    :param all_student_emails:
    :return:
    """
    counter: int = 0
    for email in all_student_emails:
        if email == "no-mail":
            all_student_emails.remove(email)
            counter = counter + 1
    print(f"There have been {counter} Students without an E-Mail")
