FROM python:3.8.10-slim-buster

RUN apt update
RUN apt install -y nano

RUN useradd microservicios
RUN mkdir /home/microservicios
RUN mkdir /home/microservicios/pumpthecoin
RUN mkdir /home/microservicios/pumpthecoin/contest
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

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]