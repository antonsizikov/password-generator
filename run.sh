#!/bin/bash

export FLET_FORCE_WEB_SERVER=true
export FLET_SERVER_PORT=9111

BASEDIR=$(dirname "$0")

python ${BASEDIR}/main.py