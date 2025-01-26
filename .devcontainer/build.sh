#!/usr/bin/env bash

# Stop on errors
set -e

cd "$(dirname "$0")/.."

# Setup venv if not devcontainer of venv is not activated
if [ ! -n "$DEVCONTAINER" ] && [ ! -n "$VIRTUAL_ENV" ];then
  virtualenv .venv
  source .venv/bin/activate
fi

# Install packages
sudo apt update
sudo apt-get upgrade -y

. ${NVM_DIR}/nvm.sh
nvm install
nvm use

npm install

# Install Python dependencies
python3 -m  pip install --upgrade pip

/usr/local/bin/uv sync --extra cli
/usr/local/bin/uv run pre-commit install

# required for some local testing
# python3 -m pip install python-dotenv
# python3 -m pip install httpx authlib
