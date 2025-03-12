import os
import unittest
import pytest
from unittest.mock import patch, MagicMock

import click

from unit.test_data import (
    validate_token_response,
    get_profile_test_response,
    get_ide_courses_test_response,
    get_tasks_by_doc_test_response,
    get_task_by_ide_task_id_test_response,
    submit_task_by_id_tim_test_response,
    submit_task_by_id_test_submit,
)
from tidecli.api.routes import (
    validate_token,
    get_profile,
    get_ide_courses,
    get_tasks_by_doc,
    get_task_by_ide_task_id,
    submit_task,
)
from tidecli.models.course import Course
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.models.tim_feedback import TimFeedback


def _create_mock_request(mock_response: dict) -> MagicMock:
    """
    Create a mock request object with wanted response
    """
    mm = MagicMock()
    mm.json.return_value = mock_response
    return mm


@patch("tidecli.api.routes.requests.request")
@patch("keyring.get_password", return_value="test_token")
class TestRoutes(unittest.TestCase):
    def test_validate_token(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to validate valid token
        """
        mock_request.return_value = _create_mock_request(validate_token_response)

        res = validate_token()
        assert res == validate_token_response

    def test_validate_faulty_token(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to validate token which is faulty
        """
        mock_request.return_value = _create_mock_request({"error": "invalid_token"})

        with self.assertRaises(click.ClickException) as context:
            validate_token()

        self.assertIn(
            "invalid_token",
            str(context.exception.message),
        )

    def test_get_profile(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to get user profile
        """
        return_value = _create_mock_request(get_profile_test_response)
        mock_request.return_value = return_value

        res = get_profile()
        assert res == return_value.json.return_value

    def test_get_user_ide_courses(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route, gets all courses user has bookmarked and have ideDocument tag with task paths
        """
        mock_request.return_value = _create_mock_request(get_ide_courses_test_response)
        validated_value = [Course(**course) for course in get_ide_courses_test_response]

        res = get_ide_courses()
        assert res == validated_value

    def test_get_tasks_by_doc(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to get tasks by document path
        """
        return_value = _create_mock_request(get_tasks_by_doc_test_response)
        mock_request.return_value = return_value
        validated_value = [TaskData(**task) for task in return_value.json.return_value]

        res = get_tasks_by_doc(doc_path="kurssit/testi/test/demot/Demo1")
        assert res == validated_value

    def test_get_task_by_ide_task_id(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to get tasks by ideTask id
        """
        return_value = _create_mock_request(get_task_by_ide_task_id_test_response)
        mock_request.return_value = return_value
        validated_value = TaskData(**return_value.json.return_value)

        res = get_task_by_ide_task_id(
            ide_task_id="t1", doc_path="kurssit/testi/test/demot/Demo1"
        )
        assert res == validated_value

    def test_submit_task_by_id(self, kr_mock, mock_request):
        """
        TDD-unit test model for the route to submit task by task id, document id and paragraph id

        """
        submit_data = SubmitData(**submit_task_by_id_test_submit)
        return_value = _create_mock_request(submit_task_by_id_tim_test_response)

        mock_request.return_value = return_value

        res = submit_task(submit_data)

        assert res == TimFeedback(**return_value.json().get("result"))
