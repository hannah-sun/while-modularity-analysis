FROM python:3.7-alpine

RUN apk add gcc libc-dev

RUN mkdir /requirements
WORKDIR /requirements
RUN wget https://github.com/stevenshan/while-transpiler/archive/latest.tar.gz
RUN tar -xf latest.tar.gz
WORKDIR /requirements/while-transpiler-latest
RUN python setup.py install

ADD . /source
WORKDIR /source
RUN python setup.py install
WORKDIR /source/while-programs

EXPOSE 80/tcp

CMD ["whiletranspiler", "-w", "--plugin", "plugin"]

