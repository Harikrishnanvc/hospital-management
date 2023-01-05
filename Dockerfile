FROM python:3.10.6-alpine
ENV PYTHONUNBUFFERED 1
WORKDIR /hospital_management

COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip wheel setuptools
RUN apk add gcc python3-dev jpeg-dev zlib-dev gpgme-dev libc-dev musl-dev g++ freetype-dev postgresql-dev

RUN pip install -r requirements.txt

COPY ./hospital_management /hospital_management
 