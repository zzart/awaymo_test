# alpine 3.6 contains python 3.6.1
FROM alpine:3.6

LABEL maintainer =  mariusz@pixey.pl

WORKDIR /awaymo

# set a user so we don't run the app in the container as root

RUN set -x ; \
    addgroup -g 1000 -S dev ; \
    adduser -u 1000 -D -S -G dev dev && exit 0 ; exit 1

RUN chown dev:dev /awaymo

ADD requirements.txt /awaymo/
ADD requirements_test.txt /awaymo/
ADD tox.ini /awaymo/

# Few extra packages needed for Cython
RUN apk update && \
    apk add python3 python3-dev gcc musl-dev linux-headers libffi libffi-dev libressl-dev libxml2-dev libxslt-dev g++ pcre pcre-dev git && \
    rm -fr /var/cache/apk/* && \
    pip3 install -r requirements.txt && \
    pip3 install -r requirements_test.txt

USER dev

ADD api          /awaymo/api
ADD config          /awaymo/config
ADD utils          /awaymo/utils

ENV PORT 8080

EXPOSE ${PORT}

ENV AWAYMO_HOME /awaymo
ENV PYTHONPATH /awaymo


CMD ["uwsgi", "--ini", "config/uwsgi.ini"]
