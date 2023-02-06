# data-focused-python

## Modules

### `lounges.py`
Webscrapes [www.loungebuddy.com](https://loungebuddy.com) to return a list of all lounges seperated by terminal based on given airport codes.

## Installation

Uses [pipenv](https://pipenv.pypa.io/) to keep track of requirements and enviornment. To install, run `pip install --user pipenv`

### Virtual Environment

Run `pipenv shell` in your command line to activate this project's virtual environment.
If you have more than one version of Python installed on your machine, you can use pipenv's `--python` option to specify which version of Python should be used to create the virtual environment.
If you want to learn more about virtual environments, read [this article](https://docs.python-guide.org/dev/virtualenvs/#using-installed-packages).


### Downloading Packages

The repository contains `Pipfile` that declares which packages are necessary for the project. To install packages declared by the Pipfile, run `pipenv install` in the command line from the `/app` directory.

To add additional packages, run `pipenv install [PACKAGE_NAME]`, as you would install python packages using pip. This will update `Pipfile` and add the downloaded package under `[packages]`.
Note that `Pipfile.lock` will also be updated with the specific versions of the dependencies that were installed.
Any changes to `Pipfile.lock` should also be committed to your Git repository to ensure that everyone on the team is using the same dependency versions.
