FROM python:3.6
LABEL maintainer "Ash Wilson"

ADD requirements.txt /usr/src/app/requirements.txt
RUN pip install -r /usr/src/app/requirements.txt
ADD . /usr/src/app

ENTRYPOINT /usr/src/app/script/container/entrypoint.sh
