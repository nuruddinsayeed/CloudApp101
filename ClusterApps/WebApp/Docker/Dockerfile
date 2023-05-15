FROM python:3.9.16-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt-get update

RUN pip install --no-cache-dir -r requirements.txt
# RUN apk del .tmp-build-deps

COPY . .

ENV ENV docker

CMD [ "python", "run.py" ]