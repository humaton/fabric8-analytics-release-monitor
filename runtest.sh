#!/bin/bash

# fail if smth fails
# the whole env will be running if test suite fails so you can debug
set -e

# for debugging this script, b/c I sometimes get
# unable to prepare context: The Dockerfile (Dockerfile.tests) must be within the build context (.)
set -x

function prepare_venv() {
    VIRTUALENV=`which virtualenv`
    if [ $? -eq 1 ]; then
        # python34 which is in CentOS does not have virtualenv binary
        VIRTUALENV=`which virtualenv-3`
    fi

	${VIRTUALENV} -p python3 venv && source venv/bin/activate && python3 `which pip3` install -r integration_tests/requirements.txt
}


[ "$NOVENV" == "1" ] || prepare_venv || exit 1

behave ./integration_tests