#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5200 --access-logfile - --error-logfile - pumpthecoin-flask:app