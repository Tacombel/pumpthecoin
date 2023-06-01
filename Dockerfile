FROM python:3.8.10-slim-buster
RUN useradd microservicios

WORKDIR /home/pumpthecoin

RUN mkdir /home/pumpthecoin/contest
COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY .flaskenv boot.sh config.py contest.py db_add_column.py db_add_comment.py db_remove_row.py  gunicorn.conf.py  pumpthecoin-flask.py pumpthecoin.py send_telegram.py spf_earnings.py update_balance.py ./
RUN chmod +x boot.sh

ENV FLASK_APP pumpthecoin-flask
ENV PYTHONUNBUFFERED 1

RUN chown -R microservicios:microservicios ./
USER microservicios

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]