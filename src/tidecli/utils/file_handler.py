"""Module for creating file structures for tasks and demos."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import re
import json
from collections import defaultdict
from typing import Any
import click.exceptions
from pathlib import Path
import itertools
from os.path import relpath

from tidecli.models.task_data import (
    SupplementaryFile,
    TaskData,
    TaskFile,
    TideCourseData,
    TideCoursePartData,
)
from tidecli.utils.error_logger import Logger
from tidecli.api import routes

METADATA_NAME = ".timdata"
"""File to store metadata in task folder."""

# Search strings for finding the beginning and end of the task content
BEGIN_MSG_SEARCH_STRING = r"Write your code below this line"
END_MSG_SEARCH_STRING = r"Write your code above this line"


def write_file(file_path: Path, content: str | bytes) -> None:
    """
    Write content to a file.

    :param file_path: Path to the file
    :param content: Content to write
    """
    if isinstance(content, str):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
            file.close()
    else:
        with open(file_path, "wb") as file:
            file.write(content)
            file.close()


def create_tasks(
    tasks: list[TaskData], overwrite: bool, user_path: str | None = None
) -> None:
    """
    Create multiple tasks.

    :param tasks: List of TaskData objects
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if tasks are created, False if not
    """
    combined_tasks = combine_tasks(tasks)

    for task in combined_tasks:
        create_task(task=task, overwrite=overwrite, user_path=user_path)


def combine_tasks(tasks: list[TaskData]) -> list[TaskData]:
    """
    Combine tasks with same ide_task_id.

    :param tasks: List of TaskData objects
    return: List of TaskData objects
    """
    # Combine tasks with same ide_task_id
    tasks_by_ide_task_id: dict[str, list[TaskData]] = {}
    for t in tasks:
        ide_task_id = t.ide_task_id
        task_list = tasks_by_ide_task_id.get(ide_task_id, [])
        task_list.append(t)
        tasks_by_ide_task_id[ide_task_id] = task_list

    # Create new list with combined tasks
    combined_tasks = []
    for ide_task_id, task_list in tasks_by_ide_task_id.items():
        combined_tasks.append(
            TaskData(
                path=task_list[0].path,
                type=task_list[0].type,
                doc_id=task_list[0].doc_id,
                ide_task_id=ide_task_id,
                task_files=[f for t in task_list for f in t.task_files],
                task_directory=task_list[0].task_directory,
                supplementary_files=[
                    f for t in task_list for f in t.supplementary_files
                ],
                stem=task_list[0].stem,
                header=task_list[0].header,
                max_points=task_list[0].max_points,
                answer_limit=task_list[0].answer_limit,
                deadline=task_list[0].deadline,
            )
        )

    return combined_tasks


def get_file_content_from_source(source: str) -> bytes | Any:
    """
    Get content of a file from its source address.
    If address does not start with http URL, it is assumed to be a TIM path.

    :param source: file source address
    return: Content of the source
    """
    if source is not None:
        if re.match(r"^https?://", source):
            # Source is a http URL
            return routes.get_file_content(source)
        else:
            # Source is assumed to be a TIM path
            return routes.get_file_content(source, is_tim_file=True)


def create_task(task: TaskData, overwrite: bool, user_path: str | None = None) -> bool:
    """
    Create a single task.

    :param task: TaskData object
    :param overwrite: Flag if overwrite
    :param user_path: Path to user given folder

    return: True if task is created, False if not
    """
    # Sets path to current path or user given path
    if user_path:
        save_path = Path.cwd() / user_path
    else:
        save_path = Path.cwd()

    saved = save_task_files(task, save_path=save_path, overwrite=overwrite)

    if not saved:
        return False

    write_metadata(folder_path=save_path, metadata=task)

    return saved


def save_task_file(
    task_file: TaskFile | SupplementaryFile, save_path: Path, overwrite: bool = False
) -> None:
    """
    Save task file in the given path.

    :param task_file: TaskFile object
    :param save_path: Path to save the file
    :param overwrite: Flag if overwrite
    return: True if file is saved, False if not
    """

    file_path = save_path / task_file.file_name

    if file_path.exists():
        if not overwrite:
            click.echo(
                f"File {file_path} already exists\n"
                f"To overwrite add -f to previous command\n"
            )
            return
    file_path.parent.mkdir(parents=True, exist_ok=True)
    if task_file.content is not None:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(task_file.content)
            file.close()
    elif task_file.source is not None:
        # TODO: Handle potential errors from API call (allow errors so that consequent files are saved)
        # Currently, only files that in the list before an error are saved
        content = get_file_content_from_source(task_file.source)
        with open(file_path, "wb") as file:
            file.write(content)
            file.close()

    working_dir = Path.cwd()
    click.echo(
        f"Wrote file {save_path.relative_to(working_dir) if save_path.is_relative_to(working_dir) else save_path}: {task_file.file_name}"
    )


def save_task_files(task: TaskData, save_path: Path, overwrite: bool = False) -> bool:
    """
    Save task files in the given path.

    :param task: TaskData object
    :param save_path: Path to save the files
    :param overwrite: Flag if overwrite
    :return: True if files are saved, False if not
    """

    task_files = task.task_files + task.supplementary_files
    save_dir = save_path / task.get_task_directory()

    for task_file in task_files:
        if task_file.task_directory is not None:
            save_dir = save_path / task_file.task_directory
        save_task_file(task_file, save_dir, overwrite)

    return True


def write_metadata(folder_path: Path, metadata: TaskData) -> None:
    """
    Write metadata.json to the given folder path.

    :param metadata: TaskData object
    :param folder_path: Path to folder to create metadata.json
    """
    metadata_path = Path(folder_path) / METADATA_NAME
    write_mode = "w"
    course_metadata: TideCourseData = TideCourseData()
    course_part_name = metadata.path
    taskname = metadata.ide_task_id
    if metadata_path.exists():
        try:
            with open(metadata_path, "r", encoding="utf-8") as file:
                old_metadata = json.load(file)
                course_metadata = TideCourseData(**old_metadata)
        except Exception as e:
            # raise click.ClickException(f"Error reading metadata: {e}")
            click.echo(f"Error reading metadata: {e}")  # Try to recover
    with open(metadata_path, write_mode, encoding="utf-8") as file:
        course_part = course_metadata.course_parts.setdefault(
            course_part_name, TideCoursePartData()
        )

        if course_part.tasks.get(taskname, metadata) != metadata:
            click.echo("Task metadata updated")
        course_part.tasks[taskname] = metadata

        content = course_metadata.model_dump_json(indent=4)
        file.write(content)
        file.close()


def create_file(item: dict, folder_path: Path, overwrite=False):
    """
    Create files of tasks in the given path.

    :param item: Single dict, contains file data
    :param folder_path: Path to folder to create task folder and file
    :param overwrite: Flag if overwrite

    """
    # By default, writemode is CREATE
    # If path exists already, write mode is WRITE (overwrites)
    if folder_path.exists():
        if not overwrite:
            raise click.ClickException(f"Folder {folder_path} already exists")

    # Write the file with desired writemode, CREATE or WRITE
    with open(folder_path, "x", encoding="utf-8") as file:
        file.write(item["code"])
        file.close()


def include_user_answer_to_task_file(f1: TaskFile, f2: Path) -> bool:
    logger = Logger()
    logger.debug(f"Validating {f2.name} against metadata content of task.")
    with open(f2, "r", encoding="utf-8") as answer_file:
        answer_content = answer_file.read()
        answer_bycode, answer_gapcode = split_file_contents(answer_content)
        metadata_bycode, metadata_gapcode = split_file_contents(f1.content)

        if len(metadata_bycode) == 0:
            f1.content = answer_content
            logger.debug("Normal exercise, no gap found.")
            return True

        if validate_answer_file(answer_bycode, metadata_bycode):
            # TODO: tarvitaan lisää testitapauksia,
            # Validator OK
            logger.debug("Gap-type exercise answer file is valid.")
            f1.content = "\n".join(answer_gapcode)
            return True

        logger.debug("Gap-type exercise answer not valid.")

        # Validator complains about answer.
        # Answer is submitted despite of complains.
        f1.content = "\n".join(answer_gapcode)
        # return False
        return True  # Do not be so spesific about the validation


def get_task_file_data(
    file_path: Path | None,
    file_dir: Path,
    metadata_dir: Path,
    metadata: TideCourseData,
    with_starter_content: bool = False,
) -> list[TaskFile]:
    """
    Get file data from the given path excluding .json files.

    :param metadata: TaskData object
    :param file_path: Path to file to search for
    :param file_dir: Path to the file directory containing the files.
    :param with_starter_content: Flag to use starter content instead of user answer
    :return: List of TaskFile objects
    """
    # TODO: refactor

    result = []
    tasks = set()
    file_path = file_path.absolute() if file_path is not None else None
    file_dir = file_dir.absolute()

    for course_part in metadata.course_parts.values():
        for task in course_part.tasks.values():
            for task_file in task.task_files:
                timdata_task_directory = (
                    task_file.task_directory
                    if task_file.task_directory is not None
                    else task.get_task_directory()
                )
                timdata_file_path = (
                    metadata_dir / timdata_task_directory / task_file.file_name
                ).absolute()
                timdata_file_dir = (metadata_dir / timdata_file_path.parent).absolute()

                if file_path is not None:
                    path_match = timdata_file_path == file_path
                else:
                    path_match = (
                        file_dir == timdata_file_dir
                        or file_dir in timdata_file_dir.parents
                    )

                if path_match:
                    if not with_starter_content:
                        if not include_user_answer_to_task_file(
                            task_file, timdata_file_path
                        ):
                            continue
                    result.append(task_file)
                    tasks.add(task.ide_task_id)

                    if len(tasks) > 1:
                        # Prompt user for which tasks to submit?
                        raise click.ClickException(
                            "Multiple tasks found in the same directory. Give exact file name."
                        )
    return result


def get_metadata(metadata_dir: Path) -> tuple[TideCourseData, Path]:
    """
    Get metadata from the given path.

    :param metadata_dir: Path to the directory containing the
    metadata.json file.
    :return: Tuple of metadata and metadata directory
    :raises: ClickException if metadata not found
    """
    metadata_dir = metadata_dir.absolute()
    while True:
        metadata_path = metadata_dir / METADATA_NAME
        if metadata_path.exists():
            break
        if (
            str(metadata_dir) == metadata_dir.root
            or metadata_dir == metadata_dir.parent
        ):
            raise click.ClickException(f"Metadata not found in {metadata_path}")
        metadata_dir = metadata_dir.parent

    try:
        with open(metadata_path, "r", encoding="utf-8") as file:
            metadata = json.load(file)
            if "course_parts" not in metadata:
                task_data = TaskData(**metadata)
                for task_file_data in task_data.task_files:
                    if task_file_data.task_type is None:
                        task_file_data.task_type = task_data.type

                return (
                    TideCourseData(
                        course_parts={
                            task_data.path: TideCoursePartData(
                                tasks={task_data.ide_task_id: task_data}
                            )
                        }
                    ),
                    metadata_dir,
                )
            return TideCourseData(**metadata), metadata_dir
    except Exception as e:
        raise click.ClickException(f"Error reading metadata: {e}")


def split_file_contents(content: str) -> tuple[list[str], list[str]]:
    """
    Split file contents to find gaps in tasks.

    :param content: Content of the file
    """
    lines = re.split(r"\r?\n", content)
    gap = find_gaps_in_tasks(lines)
    if gap is None:
        return [], []

    start, end = gap

    # Create list of strings for validation
    bycodebegin = lines[: start + 1]
    bycodeend = lines[end:]
    gap_content = lines[start + 1 : end]

    bycode = bycodebegin + bycodeend

    logger = Logger()
    log_text = "\n".join(gap_content)
    logger.debug(f"Text in the gap: \n{0}".format(log_text))

    return bycode, gap_content


def validate_answer_file(answer_by: list[str], metadata_by: list[str]) -> bool:
    """
    Validate answer file with the metadata.

    No other lines in the file should be modified
    than the task content lines. The task content lines are marked with
    comments/messages

    :param answer_by: list of answers
    :param metadata_by: list of metedatas
    :return: True if the file is valid, False if not
    """
    logger = Logger()

    if len(answer_by) == 0 and len(metadata_by) == 0:
        logger.debug("Both files are empty.")
        return False

    # Clear the contents of the answer file and metadata content
    clear_answer = clear_contents(answer_by)
    clear_metadata_content = clear_contents(metadata_by)

    if clear_answer is None or clear_metadata_content is None:
        return False

    if len(clear_answer) != len(clear_metadata_content):
        return False

    # Difference helps, when length of the contents are the same.
    bycodediff = clear_answer.difference(clear_metadata_content)
    logger.debug("Diff between cleared answer and .timdata content: \n")
    logger.debug(bycodediff)

    if len(bycodediff) > 0:
        logger.info("Note: file has been modified outside of desired area.")

    return len(bycodediff) == 0


def clear_contents(lines_by: list[str]) -> set[str] | None:
    """
    Clear the contents of the answer file.

    :param lines_by: List of lines in the file
    :return: Set of lines in the file
    """
    logger = Logger()

    # Remove empty lines for comparison
    for i, line in enumerate(lines_by):
        clean = line.strip()
        if clean == "" or clean == "\n":
            lines_by.pop(i)

    logger.debug("\n".join(lines_by))

    return set(lines_by)


def find_gaps_in_tasks(lines: list[str]) -> tuple[int, int] | None:
    """
    Find gaps in tasks.

    :param lines: List of lines in the file
    """
    # TODO: Find multiple gaps, store tuples into a list
    start: int | None = None
    end: int | None = None

    for i, line in enumerate(lines):
        if re.search(BEGIN_MSG_SEARCH_STRING, line):
            start = i
        if re.search(END_MSG_SEARCH_STRING, line):
            end = i

    gap = (start, end)
    if start is None or end is None:
        return None

    return gap


# TODO: a function for adding removed gap markers
def answer_with_original_noneditable_sections(answer: str, original: str) -> str:
    """
    Combine answer with original file, keeping non-editable sections from original.

    :param answer: Answer file content
    :param original: Original file content
    """
    answer_lines = re.split(r"\r?\n", answer)
    original_lines = re.split(r"\r?\n", original)

    answer_gaps = find_gaps_in_tasks(answer_lines)
    original_gaps = find_gaps_in_tasks(original_lines)

    if answer_gaps is None or original_gaps is None:
        return answer

    combined_lines = itertools.chain(
        original_lines[: original_gaps[0] + 1],
        answer_lines[answer_gaps[0] + 1 : answer_gaps[1]],
        original_lines[original_gaps[1] :],
    )

    return "\n".join(combined_lines)
