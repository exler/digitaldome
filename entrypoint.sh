#!/bin/bash

set -euo pipefail

python manage.py migrate

PROCESS_TYPE=$1

echo "Running process type: $PROCESS_TYPE"

if [ "$PROCESS_TYPE" = "server" ]; then
    exec gunicorn --bind 0.0.0.0:8000 --workers 2 --worker-class gevent --log-level INFO --access-logfile "-" --error-logfile "-" dome.wsgi
else
    echo "Unknown process type: $PROCESS_TYPE"
fi
