# PROJECT OVERFLIGHT

## Introduction

The Project OVERFLIGHT is a trial of Agile within Defence. This
tool will aid Patient Evacuation Coordination Cells (PECCs) in
decision making regarding the tasking of Air Evacuation Assets to
get casualties to the most advantageous Medical Treatment Facility,
thus minimising the impact of the injury to the individual.

## Getting Started
Guide users through getting your code up and running on their own system:

### Software and Account dependencies
- Integrated Development Environment (IDE) i.e Atom, VS Code
- Browser i.e Chrome, Safari, Opera
- Jira, Google Authenticator, Trello, Bitbucket (all account using cabinet office a/c)
- VPN i.e OpenVPN (windows) and TunnelVPN (Mac)
- Install latest Python 3.7.X Version (select default setting)
- Install Git (select default setting)

#### Web Links

- [Python 3.7.X](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Trello](https://trello.com/login)
- [Bitbucket](https://bitbucket.org/product/)
- [Flask Installation](https://flask.palletsprojects.com/en/1.1.x/installation/)

### Getting the project code on your system

Either extract from the archive on the GDrive in "30 - Testing versions", or clone from Bitbucket (see below).

Generate the archive to put on GDrive like so:

`git archive -o ../project-overflight-flask.zip HEAD`

#### Download Bitbucket Repo
- Open your bitbucket account
- Select 'Project Overflight Flask' Project
- In the 'Source' folder - Click 'Clone' and copy the link
- Open your Project folder via cmd/terminal and paste the link (for the first time user, it might ask your for your username and password)

### Setting up a Python development environment
- Create your project folder and Open Cmd/terminal, change directory to the project folder.
- Run these commands (Windows AND Mac):
    - `pip -V` # Check Python has installed pip
    - `pip install virtualenv` # install Virtual Env
    - `python3 -m venv venv` # create Virtual Env
- Activate the virtual environment
    - `venv\Scripts\activate`    (windows)
    - `source venv/bin/activate` (Mac)
- Install flask and required runtime libraries
    - `pip install -r requirements.txt`
- Install libraries required for development
    - `pip install -r requirements-dev.txt`

## Create (or re-create) your local db - deletes all current data
- `flask db init`

## Populate local db with demo data
- `flask db demo`

## Run server
- `FLASK_ENV=development flask run` (Mac)
- `set FLASK_ENV=development & flask run` (windows)

## Deactivate the virtual environment
- `deactivate`

## Run tests and coverage

### To run the tests in series
- `coverage run -m pytest; coverage report`

### To run the tests in parallel
- `pytest --cov=RAPID --concmode=mproc test/`
