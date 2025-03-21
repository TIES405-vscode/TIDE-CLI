"""
Task data models.

Provides validation and conversion to JSON for task data.
"""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import re
from pathlib import Path
from typing import Dict

from pydantic import BaseModel


class TaskFile(BaseModel):
    """Model for single code file."""

    task_id_ext: str
    """Extended version of task ID as string."""

    content: str
    """Content of the file."""

    file_name: str = ""
    """Name of the file."""

    source: str = "editor"
    """Source attribute in TIM. Not used in CLI app."""

    task_directory: str | None = None
    """Directory of the task."""

    task_type: str | None = None
    """Type of the task."""

    user_input: str = ""
    """User input argument for submit."""

    user_args: str = ""
    """User arguments for submit."""

    def to_json(self) -> dict:
        """Convert to JSON."""
        return {
            "task_id_ext": self.task_id_ext,
            "content": self.content,
            "file_name": self.file_name,
            "source": self.source,
            "user_input": self.user_input,
            "user_args": self.user_args,
        }


class SupplementaryFile(BaseModel):
    file_name: str
    content: str | None
    source: str | None
    task_directory: str | None = None


_task_type_split_re = re.compile(r"[/,; ]")


class TaskData(BaseModel):
    """
    Model for task data.

    :param path: Path to the task
    :param type: Type of the task
    :param doc_id: Document ID
    :param ide_task_id: Task ID
    :param task_files: List of task files
    :param stem: Stem of the task
    :param header: Header of the task

    """

    path: str
    """Path to the task."""

    type: str
    """Type of the task."""

    doc_id: int
    """Document ID where task belongs in TIM."""

    ide_task_id: str
    """Task ID in TIM for IDE fetch."""

    task_files: list[TaskFile]
    """List of task files."""

    supplementary_files: list[SupplementaryFile] = []
    """List of supplemental files."""

    stem: str | None = None
    """Stem of the task, may containg a short instructions."""

    task_directory: str | None = None
    """Directory of the task."""

    header: str | None = None
    """Header of the task."""

    max_points: float | None = None
    """Maximum points for the task"""

    deadline: str | None = None
    """ISO8601 date string for the task deadline. Server time is UTC+0, so users of this property will need to account for the local offset."""

    answer_limit: int | None = None
    """Maximum number of submission attempts for the task."""

    def get_default_task_directory(self) -> Path:
        """Return default task directory."""
        return Path(Path(self.path).name) / self.ide_task_id

    def get_task_directory(self) -> Path:
        """Return the directory to which task files will be save."""
        if self.task_directory is not None:
            return Path(self.task_directory)
        else:
            return self.get_default_task_directory()

    @property
    def run_type(self) -> str:
        """Return run type eg. cc from cc/input/comtest."""
        return _task_type_split_re.split(self.type)[0]

    def pretty_print(self) -> str:
        """
        Pretty print the task data.

        Prints the task data in a readable string.
        :return: Task data as string like Task: <header>, ID: <ide_task_id>

        """
        if self.header is not None:
            return f"Taskname: {self.header}, ID: {self.ide_task_id}"
        else:
            return f"ID: {self.ide_task_id}"

    def to_json(self) -> dict:
        """Convert to dict."""
        task_data = self.model_dump()
        task_data["task_files"] = [
            task_file.model_dump() for task_file in self.task_files
        ]

        return task_data


class TideCoursePartData(BaseModel):
    """
    Model for Tide course part data. Could be like a week or something else

    """

    tasks: Dict[str, TaskData] = {}


class TideCourseData(BaseModel):
    """
    Model for Tide course data.

    """

    course_parts: Dict[str, TideCoursePartData] = {}
