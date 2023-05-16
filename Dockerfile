FROM python:3.8.10-slim-buster
RUN useradd microservicios

WORKDIR /home/pumpthecoin

RUN mkdir /home/pumpthecoin/contest
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY boot.sh config.py .flaskenv pumpthecoin.py pumpthecoin-flask.py spf_earnings.py contest.py update_balance.py gunicorn_config.py ./
RUN chmod +x boot.sh

ENV FLASK_APP pumpthecoin-flask
ENV PYTHONUNBUFFERED 1

RUN chown -R microservicios:microservicios ./
USER microservicios

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]