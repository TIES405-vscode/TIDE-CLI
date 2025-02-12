"""
This module contain the functions that make requests to the API.

Functions are used by main program and utility functions.
"""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

from typing import Any
import click
import requests

from urllib.parse import urljoin
from tidecli.models.course import Course
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.models.tim_feedback import TimFeedback
from tidecli.tide_config import (
    TIM_URL,
    INTROSPECT_ENDPOINT,
    PROFILE_ENDPOINT,
    IDE_COURSES_ENDPOINT,
    TASK_BY_IDE_TASK_ID_ENDPOINT,
    SUBMIT_TASK_ENDPOINT,
    TASKS_BY_DOC_ENDPOINT,
    TASKS_BY_COURSE_ENDPOINT,
)
from tidecli.utils.handle_token import get_signed_in_user


def get_file_content(url: str, is_tim_file: bool = True) -> bytes | Any:
    """
    Get the content of the file from the URL.

    :param url: URL of the file
    :param is_tim_file: If the file is from TIM
    return: Content of the file
    """
    headers = None

    if is_tim_file:
        url = urljoin(TIM_URL, url)
        signed_in_user = get_signed_in_user()
        if not signed_in_user:
            raise click.ClickException("User not logged in")

        token: str = signed_in_user.password
        headers = {"Authorization": f"Bearer {token}"}

    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        return res.content
    except Exception as e:
        raise click.ClickException(
            f"Could not get the content of the file from {url}\n{e}"
        ) from e


def tim_request(
    endpoint: str,
    method: str = "GET",
    params: dict[str, str | None] | None = None,
) -> dict:
    """
    Make a request to the TIM API.

    :param endpoint: API endpoint
    :param method: HTTP method
    :param params: data to send
    return: JSON response
    """
    signed_in_user = get_signed_in_user()
    if not signed_in_user:
        raise click.ClickException("User not logged in")

    token: str = signed_in_user.password

    try:
        res = requests.request(
            method,
            f"{TIM_URL}{endpoint}",
            headers={"Authorization": f"Bearer {token}"},
            json=params,
        )

        res_json = res.json()
        if "error" in res_json:
            error = res_json["error"]
            if "error_description" in res_json:
                raise Exception(error + "\n" + res_json["error_description"])
            else:
                raise Exception(error)
        return res_json

    except Exception as e:
        raise click.ClickException(
            f"Could not complete API call {endpoint}\n{e}"
        ) from e


def validate_token() -> dict:
    """
    Validate the token for the user.

    return: JSON response  of token validity
    """
    res = tim_request(endpoint=INTROSPECT_ENDPOINT, method="POST")

    return res


def get_profile() -> dict:
    """
    Get the user profile.

    return: JSON response  of user profile
    """
    return tim_request(endpoint=PROFILE_ENDPOINT)


def get_ide_courses() -> list[Course]:
    """
    Get the logged in user courses.

    Get users that are in user bookmarks and have ideCourse tag.

    return: JSON response of course name and course path,
    course id and paths for demo documents
    """
    res = tim_request(endpoint=IDE_COURSES_ENDPOINT)
    all_courses = [Course(**course) for course in res]

    return all_courses


def get_tasks_by_doc(doc_path: str) -> list[TaskData]:
    """
    Get the tasks by document path or document id.

    :param doc_path: Tasks document path
    return: JSON response of tasks
    """
    doc_id = None  # Tim requires doc_id to be None if not used

    res = tim_request(
        endpoint=TASKS_BY_DOC_ENDPOINT,
        params={"doc_path": doc_path, "doc_id": doc_id},
    )

    tasks = [TaskData(**task) for task in res]

    return tasks


def get_task_by_ide_task_id(
    ide_task_id: str,
    doc_path: str,
) -> TaskData:
    """
    Get the tasks by ideTask id and demo document path or id.

    :param doc_path: Demo document path
    :param ide_task_id: ideTask id
    return: JSON response of tasks
    """
    doc_id = None  # Tim requires doc_id to be None if not used

    res = tim_request(
        endpoint=TASK_BY_IDE_TASK_ID_ENDPOINT,
        params={
            "doc_path": doc_path,
            "doc_id": doc_id,
            "ide_task_id": ide_task_id,
        },
    )

    return TaskData(**res)


def get_tasks_by_course(doc_id: int, doc_path: str) -> list[TaskData]:
    """
    Get all tasks from a single course by document id or document path
    
    :param doc_path: Tasks document path
    return: JSON response of tasks
    """
    doc_id = None  # Tim requires doc_id to be None if not used

    res = tim_request(
        endpoint=TASKS_BY_COURSE_ENDPOINT,
        params={"doc_path": doc_path, "doc_id": doc_id},
    )

    tasks = [TaskData(**task) for task in res]

    return tasks


def submit_task(
    task_files: SubmitData,
) -> TimFeedback:
    """
    Submit the task by task id, document id and paragraph id.

    :param task_files: Task/s data
    return: JSON response of tasks
    """
    res = tim_request(
        endpoint=SUBMIT_TASK_ENDPOINT,
        method="PUT",
        params=task_files.submit_json(),
    )
    feedback = res.get("result")
    if not feedback:
        raise click.ClickException("No feedback received")

    return TimFeedback(**feedback)
