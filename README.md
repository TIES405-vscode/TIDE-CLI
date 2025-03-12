# TIDE-CLI

A command line interface for completing TIM programming exercises

## Development

### Requirements

- Python 3.10 or higher
- [Poetry](https://python-poetry.org/docs/#installation) and [Poetry shell plugin](https://github.com/python-poetry/poetry-plugin-shell) for dependency management, see the links for installation instructions
- If you run into issues when trying to install Poetry and/or the Poetry shell plugin via the system's own package manager, you can try the following:
	- install Poetry via `pipx` as per the official Poetry instructions linked above
	- if you have trouble installing the shell plugin: activate the Poetry virtual environment with `poetry env activate` and continue onto `Step 4` (requires Poetry v2.x)


For managing multiple versions of Python see e.g. [pyenv](https://github.com/pyenv/pyenv) (or [pyenv-win](https://github.com/pyenv-win/pyenv-win) for Windows systems)

### Usage as python application

Step 1: Clone TIDE-CLI repository https://github.com/TIDE-project/TIDE-CLI

Step 2: Modify src/tidecli/tide_config.py BASE_URL to correspond the TIM-server being used

Step 3: Run `poetry shell` to enter virtual environment (or `poetry env activate` if you didn't install the shell plugin). 

Step 4: Run `poetry install` to install dependencies. If Poetry install fails, run first `poetry lock`

Step 5: Go to correct folder: `cd src/tidecli`

Step 6: To run the application, run `python main.py login` to login to the application

Step 7: Run `python main.py` to see the list of available commands

### Building the CLI tool as an executable

There may be a need for build the CLI tool into an executable using user's own operating system. If that is the case, please follow these after above steps are completed until `Step 4`.

**Build the CLI tool**

Step 1: `poetry run build`

Step 2: `cd dist && ls -la`, file permissions should look like `-rwxr-xr-x`

Step 3: Move app named 'main' as 'tide' to some folder that is in PATH. E.g. `mv main /usr/bin/tide`.

Step 4: Start use, please refer user instructions in TIM.

## Testing

### Running unit tests

After cloning and starting the Poetry environment:

Step 1: Navigate to test folder `cd tests`

Step 2: Run unit tests with command `python -m unittest`

### Running integration tests

Step 1: Start up TIM dev server (for instructions on this, see https://github.com/TIM-JYU/TIM)

Step 1.5: Authenticate to TIDE. See [Manual authentication required for running the tests](#manual-authentication-required-for-running-the-tests) section below.

Step 2: Navigate to integration test folder `cd tests/integration`

Step 3: Run `poetry run pytest`. If the TIM instance used for tests is not running in localhost, set the correct address to TIM_DOMAIN environmental variable, e.g. `TIM_DOMAIN=192.168.148.69 poetry run pytest`

### Current state of integration tests

This section covers the current state of integration tests, and running them.

#### Manual authentication required for running the tests

In the current state, there is no implementation for authenticating TIDE automatically, thus the test user has to authenticate TIDE manually before running the tests.

Step 1: Run `DEV=true poetry run python src/tidecli/main.py login` at the project root.

Step 2: Log in using the test user credentials ("testuser1", "test1pass") and authenticate TIDE.

#### State of tests for the login command

Tide uses webbrowser.open function to show the authentication page to the user.
The problem faced while trying to mock this function was the fact that
webbrowser.open is followed by a code that has to be running while the user
interacts with the browser, thus the mock would have to be non-blocking like
the original function. This proved to be too complex of a problem to tackle.

A solution to the problem of authenticating the user automatically may lie in not mocking the webbrowser.open function and instead getting it to launch Chromium with --remote-debugging-port flag and attaching to it. See [connect over cdp in Playwright documentation](https://playwright.dev/python/docs/api/class-browsertype#browser-type-connect-over-cdp).

