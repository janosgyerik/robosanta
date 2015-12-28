#!/bin/sh -e

cd $(dirname "$0")/..

requirements=requirements.txt

./pip.sh install --upgrade -r $requirements
