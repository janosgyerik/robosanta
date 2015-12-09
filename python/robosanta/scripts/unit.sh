#!/bin/sh -e

cd $(dirname "$0")/..

find robosanta -name test_\*.py | xargs ./run.sh
