#!/bin/bash
source venv/bin/activate
exec gunicorn --config gunicorn_config.py --access-logfile - --error-logfile - pumpthecoin-flask:app