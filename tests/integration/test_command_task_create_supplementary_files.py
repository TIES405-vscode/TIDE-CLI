from pathlib import Path

import pytest
from click.testing import CliRunner

from tidecli.main import task

#     # task with supplementary files defined in markdown
#     (
#         "users/test-user-1/course-1",
#         "exercise-1",
#         "t2",
#     ),
#     # task with supplementary files autogenerated by TIM
#     (
#         "users/test-user-1/course-1",
#         "exercise-1",
#         "t3",
#     ),
#     # task with supplementary files from external source
#     (
#         "users/test-user-1/course-2",
#         "exercise-b",
#         "t1",
#     ),
#     # TODO: task with supplementary files from TIM source

@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_markdown_creates_expected_files(tmp_dir):
    pytest.xfail("Not implemented.")


@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_markdown_creates_files_with_expected_content(tmp_dir):
    pytest.xfail("Not implemented.")


@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_external_creates_expected_files(tmp_dir):
    pytest.xfail("Not implemented.")


@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_external_creates_files_with_expected_content(tmp_dir):
    pytest.xfail("Not implemented.")


@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_tim_creates_expected_files(tmp_dir):
    pytest.xfail("Not implemented.")


@pytest.mark.xfail
def test_task_create_with_supplementary_files_from_tim_creates_files_with_expected_content(tmp_dir):
    pytest.xfail("Not implemented.")
