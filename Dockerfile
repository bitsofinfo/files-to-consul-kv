FROM python:3.7.4-alpine

ARG GIT_TAG=master

RUN echo GIT_TAG=${GIT_TAG}

# install under /usr/local/bin
RUN apk update ; \
    apk upgrade ; \
    apk add git ; \
    echo $PATH ; \
    git clone --branch ${GIT_TAG} https://github.com/bitsofinfo/files-to-consul-kv.git ; \
    cd /files-to-consul-kv; git status; rm -rf .git; cd / ; \
    cp /files-to-consul-kv/*.py /usr/local/bin/ ; \
    rm -rf /files-to-consul-kv ; \
    apk del git ; \
    ls -al /usr/local/bin ; \
    chmod +x /usr/local/bin/*.py ; \
    rm -rf /var/cache/apk/*

# required modules
RUN pip install --upgrade pip python-dateutil requests

ENV PATH="/usr/local/bin/;$PATH"
