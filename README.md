# User Research Assitance (URA)

## Introduction

The User Research Assistance (URA) Tool is designed to help User Researchers to create
User Personas, User Stories, and also track project Stakeholders.
A User Storey cannot be created without first creating a User Persona, so
the UR will need to know who they are creating the storey for. The Personas
can be updated at any time.

## Demonstration

A demonstration of the most current version is available at https://ura.thedds.co.uk/

## Getting Started
Guide users through getting your code up and running on their own system:

### Software and Account dependencies
- Integrated Development Environment (IDE) i.e Atom, VS Code
- Browser i.e Chrome, Safari, Opera
- Install latest Python 3.7.X Version (select default setting)
- Install Git (select default setting)

#### Web Links

- [Python 3.7.X](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Trello](https://trello.com/login)
- [Bitbucket](https://bitbucket.org/product/)
- [Flask Installation](https://flask.palletsprojects.com/en/1.1.x/installation/)

### Getting the project code on your system

#### Download GitHub Repo
- Availble from https://github.com/tiggaa/URA
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
- `python InitDb.py`

## Populate local db with demo data
- `python InitDbData.py`

## Run server
- `FLASK_ENV=development flask run` (Mac)
- `set FLASK_ENV=development & flask run` (windows)

## Deactivate the virtual environment
- `deactivate`
