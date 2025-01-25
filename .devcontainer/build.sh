#!/bin/bash
# This is a script used by the devcontainer to build the project

sudo apt update

. ${NVM_DIR}/nvm.sh
nvm install
nvm use

npm install

# sudo rm /usr/lib/python3.12/EXTERNALLY-MANAGED

/usr/local/bin/uv install
/usr/local/bin/uv run pre-commit install

# required for some local testing
/usr/local/bin/pip install python-dotenv
/usr/local/bin/pip install httpx authlib
