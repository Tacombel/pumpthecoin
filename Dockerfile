FROM python:3.10.6-slim-buster

RUN apt update
RUN apt install -y nano

RUN useradd microservicios
RUN mkdir -p /home/microservicios/pumpthecoin/contest
WORKDIR /home/microservicios/pumpthecoin

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY boot.sh contest.py db_add_column.py db_add_comment.py db_remove_row.py  gunicorn.conf.py  pumpthecoin-flask.py pumpthecoin.py send_telegram.py spf_earnings.py update_balance.py ./
RUN chmod +x boot.sh
RUN chown -R microservicios:microservicios ./

ENV FLASK_APP pumpthecoin-flask
ENV PYTHONUNBUFFERED 1

USER microservicios

ENTRYPOINT ["./boot.sh"]