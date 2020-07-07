#!/usr/bin/env bash

mkdir -p /tmp/covid2
LOGFILE=/tmp/covid2/covid2.`date +'%Y%m%d'`.log

bash ~/github/covid2/run_daily.sh > ${LOGFILE} 2>&1

