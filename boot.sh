#!/bin/bash
source venv/bin/activate
exec gunicorn --workers=3 -b :5200 --access-logfile - --error-logfile - pumpthecoin-flask:app