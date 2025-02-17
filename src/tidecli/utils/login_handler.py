"""Module takes care of handling login requests."""

__authors__ = ["Olli-Pekka Riikola, Olli Rutanen, Joni Sinokki"]
__license__ = "MIT"
__date__ = "11.5.2024"

import datetime

import click

from tidecli.api.oauth_login import authenticate
from tidecli.api.routes import validate_token
from tidecli.models.user import User
from tidecli.utils.handle_token import delete_token, get_signed_in_user


def is_logged_in(
    jsondata: bool = False, print_errors: bool = True, print_token_info: bool = False
) -> bool:
    """
    Check if the user is logged in by checking if the user is in the credential manager.
    """
    # TODO: add json formated prints for vscode

    user_login: User | None = get_signed_in_user()

    # If the username exist in credential manager then return the token validity
    if user_login and user_login.password:

        # Validate the token, in case of error in validation,
        # return the error message and ask the user to login again
        try:
            token_validity_time = validate_token()
        except click.ClickException as e:
            if print_errors:
                click.echo(f"Error: {e}\nPlease, login.")
            delete_token()
            return False

        # If the token is not expired then return the token validity time
        expiration_time = token_validity_time.get("exp")
        if expiration_time:
            if print_token_info:
                click.echo(
                    "Logged in as "
                    + user_login.username
                    + "\nToken is still valid for "
                    + str(datetime.timedelta(seconds=expiration_time))
                )
            return True
        else:
            delete_token()
            if print_errors:
                click.echo("Please, login.")
            return False

    # If the username does not exist in credential manager
    else:
        if print_errors:
            click.echo("Please, login.")
        return False


def login(jsondata: bool = False):
    if not jsondata:
        click.echo(f"Logging in...\nPlease, finish authenticating in the browser.")
    if authenticate():
        if jsondata:
            return {"login_success": True}
        return "Login successful!"
    else:
        if jsondata:
            return {"login_success": False}
        return "Login failed. Please, try again."
