#!/usr/bin/env bash

screen -dmS storjlib_rpc_server;
sleep 1
screen -S storjlib_rpc_server -X stuff $'env/bin/python -m storjlib.api startserver --hostname="127.0.0.1" --port=7000 &> storjlib_rpc_server.log\n'

