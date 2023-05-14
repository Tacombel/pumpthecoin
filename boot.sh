#!/bin/bash
source venv/bin/activate
exec gunicorn --workers=1 -b :5200 --access-logfile - --error-logfile - pumpthecoin-flask:app