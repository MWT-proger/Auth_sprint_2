#!/bin/bash

gunicorn --chdir app main:app -w 2 --threads 2 -b 0.0.0.0:5000 &

python ./app/server.py &

wait -n

exit $?