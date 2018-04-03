#!/bin/bash

if [ -f $WORKON_HOME/octopus/bin/activate ]; then
    . $WORKON_HOME/octopus/bin/activate
    echo "It will use the $WORKON_HOME/octopus/bin/python interpreter!!!"
else
    echo "It will use the default python interpreter!!!"
fi

CPU_COUNT=$( python -c "import psutil; print(psutil.cpu_count())")

if [ $CPU_COUNT = "" ]; then
    CPU_COUNT=2
fi
CPU_COUNT=$(expr $CPU_COUNT \* 2)
CPU_COUNT=$(expr $CPU_COUNT + 1)

echo "The CPU_COUNT is $CPU_COUNT"

echo "count of para is $# "
if [ $# -gt 0 ]; then
    if [ $1 = "ssl" ]; then
        nohup gunicorn --workers=$CPU_COUNT -k gevent  --certfile ssl/publiccert.pem --keyfile ssl/privatekey.pem -b 0.0.0.0:5000 wsgi:app &
    fi
else
    nohup gunicorn --workers=$CPU_COUNT -k gevent  -b 0.0.0.0:5000 wsgi:app &
fi
