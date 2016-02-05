#!/usr/bin/env bash

screen -dmS storjterms_rpc_server;
sleep 1
screen -S storjterms_rpc_server -X stuff $'env/bin/python -m storjterms.api startserver --hostname="127.0.0.1" --port=7000 &> storjterms_rpc_server.log\n'

