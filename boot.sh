#!/bin/bash
source venv/bin/activate
exec gunicorn --config gunicorn.conf.py --access-logfile - --error-logfile - pumpthecoin-flask:app