#!/usr/bin/env bash

# exit immediately if a simple command exits with a nonzero exit value
set -e

# ensure pep8
env/bin/pep8 storjlib
env/bin/pep8 tests

# start server
screen -dmS rpc_server;
screen -S rpc_server -X stuff $'env/bin/coverage run --source="storjlib" -m storjlib.api startserver --hostname="127.0.0.1" --port=7000\n'

# run compatibility tests
bash -c "source <(curl -s https://raw.githubusercontent.com/Storj/storjspec/master/test_storjlib_compatibility.sh)"

# stop server
screen -S rpc_server -X stuff "^C"
sleep 1
screen -S rpc_server -X kill

# run storjlib tests
env/bin/coverage run --source="storjlib" setup.py test

# report coverage
env/bin/coverage report
