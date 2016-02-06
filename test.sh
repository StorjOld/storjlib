#!/usr/bin/env bash

# exit immediately if a simple command exits with a nonzero exit value
set -e

export PYCOIN_NATIVE=openssl
PEP8=${VIRTUALENV_PATH}pep8
COVERAGE=${VIRTUALENV_PATH}coverage

echo $PEP8
echo $COVERAGE

# ensure pep8
$PEP8 storjlib

# start server
screen -S rpc_server -d -m $COVERAGE run --source=storjlib -m storjlib.api startserver --hostname=127.0.0.1 --port=7000

# run compatibility tests
bash -c "source <(curl -s https://raw.githubusercontent.com/Storj/storjspec/master/test_storjlib_compatibility.sh)"

# stop server
screen -S rpc_server -X stuff "^C"
# sleep 10

# report coverage
#$COVERAGE report --fail-under=95
