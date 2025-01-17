#!/bin/bash
# This is a script used by the devcontainer to build the project

. ${NVM_DIR}/nvm.sh
nvm install
nvm use

npm install

sudo rm /usr/lib/python3.12/EXTERNALLY-MANAGED

/usr/local/py-utils/bin/poetry install
/usr/local/py-utils/bin/poetry run pre-commit install

/usr/bin/pip install python-dotenv
/usr/bin/pip install httpx authlib
