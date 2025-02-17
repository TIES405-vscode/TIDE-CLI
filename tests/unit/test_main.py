import os
import unittest
from pathlib import Path

from pyfakefs.fake_filesystem_unittest import TestCase
from unittest.mock import patch

from click.testing import CliRunner

from unit.test_data import (
    get_ide_courses_test_response,
    validate_token_response,
    get_tasks_by_doc_test_response,
    get_task_by_ide_task_id_test_response,
)
from unit.test_routes import _create_mock_request
from tidecli.main import login, logout, courses, task
from tidecli.models.course import Course
from tidecli.models.user import User


class TestMain(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch("tidecli.utils.login_handler.authenticate")
    @patch("keyring.get_password")
    def test_successful_new_login(self, mock_get_password, mock_authenticate):
        """
        Test successful login with new token
        """
        mock_get_password.return_value = None
        mock_authenticate.return_value = True
        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Please, login.\n"
            "Logging in...\n"
            "Please, finish authenticating in the browser."
            "\nLogin successful!\n",
        )

    @patch("tidecli.api.routes.requests.request")
    @patch("keyring.get_password")
    def test_successful_existing_login(self, mock_get_password, mock_request):
        """
        Test successful login with existing token
        """
        mock_get_password.return_value = "test_token"
        mock_request.return_value = _create_mock_request(validate_token_response)

        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Logged in as test_token\nToken is still valid for 10 days, 0:00:00\n",
        )

    @patch("tidecli.utils.login_handler.delete_token")
    @patch("tidecli.api.routes.requests.request")
    @patch("keyring.get_password")
    @patch("tidecli.utils.login_handler.authenticate")
    def test_failed_login_invalid_token(
        self, mock_authenticate, mock_get_password, mock_request, mock_delete
    ):
        """
        Test failed login due to invalid token
        """
        mock_get_password.return_value = "test_token"
        mock_authenticate.return_value = True
        mock_request.return_value = _create_mock_request({"error": "invalid_token"})
        mock_delete.return_value = "Token for user deleted successfully."

        result = self.runner.invoke(login)
        self.assertEqual(
            result.output,
            "Error: Could not complete API call /oauth/introspect\ninvalid_token\n"
            "Please, login.\n"
            "Logging in...\n"
            "Please, finish authenticating in the browser."
            "\nLogin successful!\n",
        )

    @patch("tidecli.main.delete_token")
    def test_logout(self, mock_delete_token):
        return_value = "Token for test deleted successfully!"
        mock_delete_token.return_value = return_value
        result = self.runner.invoke(logout)
        self.assertEqual(result.output, "Token for test deleted successfully!\n")

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    @patch("tidecli.main.is_logged_in") 
    def test_courses(self, mock_is_logged_in, mock_get_signed_in_user, mock_request):
        """
        Test listing courses
        """
        mock_is_logged_in.return_value = True
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_ide_courses_test_response)
        validated_value = [Course(**course) for course in get_ide_courses_test_response]
        console_print = "\n".join([course.pretty_print() for course in validated_value])

        result = self.runner.invoke(courses)
        self.assertEqual(result.output, f"{console_print}\n")

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    @patch("tidecli.main.is_logged_in")
    def test_task_list(self, mock_is_logged_in, mock_get_signed_in_user, mock_request):
        """
        Test listing tasks by document
        """
        mock_is_logged_in.return_value = True
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_tasks_by_doc_test_response)

        result = self.runner.invoke(
            task,
            [
                "list",
                "kurssit/tie/ohj2/2024k/demot/DemoC2",
            ],
        )
        self.assertEqual(result.output, "ID: t1\nID: t2\n")


class TestMainFileAccess(TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the fake filesystem
        cls.setUpClassPyfakefs()

    def setUp(self):
        self.runner = CliRunner()
        self.working_dir = str(Path.cwd())

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    @patch("tidecli.main.is_logged_in")
    def test_task_create_all(self, mock_is_logged_in, mock_get_signed_in_user, mock_request):
        """
        Test creating all tasks and trying to overwrite them without the -f flag
        """
        mock_is_logged_in.return_value = True
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(get_tasks_by_doc_test_response)

        result = self.runner.invoke(
            task,
            [
                "create",
                "kurssit/tie/ohj2/2024k/demot/DemoC2",
                "--all",
            ],
        )

        file_path_1 = Path(self.working_dir, "Demo1", "t1").relative_to(self.working_dir)
        file_path_2 = Path(self.working_dir, "Demo1", "t2").relative_to(self.working_dir)

        self.assertEqual(
            result.output,
            f"Wrote file {file_path_1}: test.c\nWrote file {file_path_2}: test.c\n"
        )

        test_path1 = f"{self.working_dir}Demo1/t1"
        test_path2 = f"{self.working_dir}Demo1/t2"
        test_file1 = f"{self.working_dir}Demo1/t1/test.c"
        test_file2 = f"{self.working_dir}Demo1/t2/test.c"
        test_metadata = f"{self.working_dir}.timdata"

        self.assertTrue(os.path.exists(test_path1))
        self.assertTrue(os.path.exists(test_file1))
        self.assertTrue(os.path.exists(test_path2))
        self.assertTrue(os.path.exists(test_file2))
        self.assertTrue(os.path.exists(test_metadata))


        result_overwrite = self.runner.invoke(
            task,
            [
                "create",
                "kurssit/Demo1",
                "--all",
            ],
        )

        # Test overwrite
        self.assertEqual(
            result_overwrite.output,
            f"File {Path(test_file1)} already exists\nTo overwrite add -f to previous command\n\nFile "
            f"{Path(test_file2)} already exists\nTo overwrite add -f to previous command\n\n",
        )

    @patch("tidecli.api.routes.requests.request")
    @patch("tidecli.api.routes.get_signed_in_user")
    @patch("tidecli.main.is_logged_in")
    def test_task_create_one(self, mock_is_logged_in, mock_get_signed_in_user, mock_request):
        """
        Test creating a single task
        """
        mock_is_logged_in.return_value = True
        mock_get_signed_in_user.return_value = User("test", "test")
        mock_request.return_value = _create_mock_request(
            get_task_by_ide_task_id_test_response
        )

        result = self.runner.invoke(
            task,
            [
                "create",
                "kurssit/Demo1",
                "t3",
            ],
        )

        file_path = Path(self.working_dir, "Demo1", "t3").relative_to(self.working_dir)
        self.assertEqual(
            result.output, f"Wrote file {file_path}: test.c\n"
        )

        test_path1 = f"{self.working_dir}Demo1/t3"
        test_metadata1 = f"{self.working_dir}.timdata"
        test_file1 = f"{self.working_dir}Demo1/t3/test.c"
        self.assertTrue(os.path.exists(test_path1))
        self.assertTrue(os.path.exists(test_metadata1))
        self.assertTrue(os.path.exists(test_file1))
