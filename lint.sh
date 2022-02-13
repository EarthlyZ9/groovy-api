#!/bin/bash
# usage: ./lint-check.sh {path-to-virtual-environment-folder}
if [ -z "$1" ] 
then
    echo "No virtual environment provided. Use default environment [.venv]"
    source .venv/bin/activate
else
    echo "try activating virtual environment [@$1/bin/activate]"
    source $1/bin/activate
fi

pylint groovy
black groovy