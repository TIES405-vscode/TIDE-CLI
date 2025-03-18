"""
Main module for the Tide CLI.

This module contains the main command group for the Tide CLI.
The whole CLI app may be located in different module.
"""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki, Vesa Lappalainen"]
__license__ = "MIT"
__date__ = "10.12.2024"

import json
from os import name
from pathlib import Path
from typing import List
from tidecli.models.tim_feedback import PointsData
from tidecli.utils import login_handler
from tidecli.utils.error_logger import Logger
import click

from tidecli.api.routes import (
    get_ide_courses,
    get_task_points,
    get_tasks_by_doc,
    get_tasks_by_course,
    get_task_by_ide_task_id,
    submit_task,
)
from tidecli.models.submit_data import SubmitData
from tidecli.models.task_data import TaskData
from tidecli.utils.file_handler import (
    answer_with_original_noneditable_sections,
    create_task,
    get_task_file_data,
    get_metadata,
    create_tasks,
)
from tidecli.utils.handle_token import delete_token
from tidecli.utils.login_handler import is_logged_in

logger = Logger()


@click.group()
def tim_ide() -> None:
    """CLI tool for downloading and submitting TIM tasks."""
    pass


@tim_ide.command()
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
def check_login(jsondata: bool) -> None:
    """
    Check login status, prints the username when logged in.

    If the --json flag is used, the output is printed in JSON format.
    """
    user = login_handler.get_signed_in_user()
    if not is_logged_in(print_errors=False, print_token_info=False) or not user:
        if jsondata:
            click.echo(json.dumps({"logged_in": None}, ensure_ascii=False, indent=4))
        else:
            click.echo("Not logged in.")
        return

    if jsondata:
        click.echo(
            json.dumps(
                {"logged_in": user.username},
                ensure_ascii=False,
                indent=4,
            )
        )
    else:
        click.echo(f"Logged in as {user.username}")


@tim_ide.command()
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
def login(jsondata: bool) -> None:
    """
    Log in the user and saves the token to the keyring.

    Functionality: Opens a browser window for the user to log in.
    """
    if is_logged_in(print_errors=True, print_token_info=True):
        return
    if jsondata:
        click.echo(
            json.dumps(login_handler.login(jsondata=True), ensure_ascii=False, indent=4)
        )
    else:
        details = login_handler.login()
        logger.info(str(details).split("\n"))
        click.echo(details)


@tim_ide.command()
def logout() -> None:
    """Log out the user and deletes the token from the keyring."""
    click.echo(delete_token())


@tim_ide.command()
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
def courses(jsondata: bool) -> None:
    """
    List all courses.

    Prints all courses that the user has access to.

    If --json flag is used, the output is printed in JSON format.
    """
    if not is_logged_in():
        return

    data = get_ide_courses()

    if not jsondata:
        for course in data:
            click.echo(course.pretty_print())

    if jsondata:
        # Create JSON object list
        courses_json = [course.model_dump() for course in data]
        click.echo(json.dumps(courses_json, ensure_ascii=False, indent=4))


@click.group()
def task() -> None:
    """
    Task related commands.

    This command is used with subcommands.
    """
    pass


@task.command(name="list")
@click.option("--json", "-j", "jsondata", is_flag=True, default=False)
@click.argument("demo_path", type=str, required=True)
def list_tasks(demo_path: str, jsondata: bool) -> None:
    """
    Fetch tasks by doc path.

    Fetches all tasks from the given doc path and prints them.
    :param demo_path: Path to the demo file.
    :param jsondata: If True, prints the output in JSON format.

    """
    if not is_logged_in():
        return

    tasks: List[TaskData] = get_tasks_by_doc(doc_path=demo_path)

    if not jsondata:
        for t in tasks:
            click.echo(t.pretty_print())

    if jsondata:
        # Create JSON object list
        # TODO: the json printed contains a ton of unnecessary information
        tasks_json = [t.to_json() for t in tasks]
        click.echo(json.dumps(tasks_json, ensure_ascii=False, indent=4))


@task.command(name="points")
@click.option("--json", "-j", "print_json", is_flag=True, default=False)
@click.argument("doc_path", type=str, required=True)
@click.argument("ide_task_id", type=str, required=True)
def points(doc_path: str, ide_task_id: str, print_json: bool):
    points: PointsData = get_task_points(ide_task_id, doc_path)
    if print_json:
        click.echo(points.model_dump_json())
    else:
        click.echo(points.pretty_print())


@task.command(name="create-course")
@click.option(
    "--force",
    "-f",
    "force",
    is_flag=True,
    default=False,
    help="Overwrite existing files",
)
@click.option(
    "--dir",
    "-d",
    "user_dir",
    is_flag=False,
    type=str,
    default=None,
    help="Path to a user defined folder for created tasks",
)
@click.option("--path", "-p", "course_path", type=str, default=None, required=False)
@click.option("--id", "-i", "course_id", type=int, default=None, required=False)
def create_course(course_path: str, course_id: int, force: bool, user_dir: str) -> None:
    """
    Create all ide tasks from a course.

    Fetches and creates all ide tasks for a given course, by course document id or document path.
    Course path and ID refer to the document where the paths to ide tasks are defined.

    Providing either COURSE_PATH or COURSE_ID is required.

    :param course_path: Path to the course document
    :param course_id: ID for the course document
    :force: If True, overwrites existing task files
    :user_dir: Path to user defined task folder
    """

    if not is_logged_in():
        raise click.UsageError("Could not create tasks: User is not logged in")
    elif course_path or course_id:
        tasks: List[TaskData] = get_tasks_by_course(
            doc_id=course_id, doc_path=course_path
        )
        for taskSet in tasks:
            create_tasks(tasks=taskSet, overwrite=force, user_path=user_dir)
    else:
        raise click.UsageError(
            "Please provide either course path or course document ID."
        )


@task.command()
@click.option("--all", "-a", "all_tasks", is_flag=True, default=False)
@click.option("--force", "-f", "force", is_flag=True, default=False)
@click.option("--dir", "-d", "user_dir", type=str, default=None)
@click.argument("demo_path", type=str)
@click.argument("ide_task_id", type=str, default=None, required=False)
def create(
    demo_path: str,
    ide_task_id: str,
    all_tasks: bool,
    force: bool,
    user_dir: str,
) -> None:
    """Create tasks based on options."""
    if not is_logged_in():
        return

    if all_tasks:
        # Create all tasks
        tasks: List[TaskData] = get_tasks_by_doc(doc_path=demo_path)
        create_tasks(tasks=tasks, overwrite=force, user_path=user_dir)

    elif ide_task_id:
        # Create a single task
        task_data: TaskData = get_task_by_ide_task_id(
            ide_task_id=ide_task_id, doc_path=demo_path
        )
        create_task(task=task_data, overwrite=force, user_path=user_dir)

    else:
        click.echo(
            "Please provide either --all or an ide_task_id."
        )  # TODO: update this message


@task.command()
@click.argument("file_path_string", type=str, required=True)
def reset(file_path_string: str) -> None:
    """
    Enter the path of the task file to reset.

    param file_path_string: Path to the task file in the local file system.
    """
    # TODO: currently resets only non-gap parts, should reset all parts or be renamed
    if not is_logged_in():
        return

    file_path = Path(file_path_string)
    if not file_path.exists() or not file_path.is_file():
        raise click.ClickException(
            "Invalid path. Please provide a valid path to the task file you want to reset."
        )

    file_contents = file_path.read_text()

    metadata, metadata_dir = get_metadata(file_path.parent)

    file_dir = file_path.parent

    task_files = get_task_file_data(
        file_path, file_dir, metadata_dir, metadata, with_starter_content=True
    )
    if not task_files:
        raise click.ClickException("Invalid task file")

    task_file_contents = next(
        (x.content for x in task_files if x.file_name == file_path.name), None
    )
    if task_file_contents is None:
        raise click.ClickException("File is not part of this task")

    file_path.write_text(task_file_contents)

    combined_contents = answer_with_original_noneditable_sections(
        file_contents, task_file_contents
    )

    file_path.write_text(combined_contents)


@tim_ide.command()
@click.argument("path", type=str, required=True)
def submit(path: str) -> None:
    """
    Enter the path of a task folder or a file to submit the task/tasks to TIM.
    If the path is a folder, all task files in the folder will be submitted.
    If the path is a file, only that task file will be submitted.

    param path: Path to a task folder or a file.
    """
    if not is_logged_in():
        return

    path: Path = Path(path)
    if not path.exists():
        raise click.ClickException(
            "Invalid path. Give a path to the task folder "
            "in the local file system or existing filename."
        )
    if not path.is_dir():
        file_dir = path.parent
        file_path = path
    else:
        file_dir = path
        file_path = None

    # Get metadata from the task folder
    metadata, metadata_dir = get_metadata(file_dir)

    if not metadata:
        raise click.ClickException("Invalid metadata")
    answer_files = get_task_file_data(file_path, file_dir, metadata_dir, metadata)
    if not answer_files:
        raise click.ClickException("Invalid task file")

    for f in answer_files:
        click.echo(f"Submitting: {f.file_name}, wait...")
        t = SubmitData(code_files=[f], code_language=f.task_type)
        feedback = submit_task(t)
        click.echo(feedback.console_output())


tim_ide.add_command(task)

if __name__ == "__main__":
    tim_ide()
