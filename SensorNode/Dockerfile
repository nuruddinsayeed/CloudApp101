FROM python:3.9-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers musl-dev build-base

RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .tmp-build-deps

COPY . .

ENV ENV docker

CMD [ "python", "run.py" ]
