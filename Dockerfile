FROM python:3.9-alpine3.13
LABEL maintainer="Juanse Vargas"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app

EXPOSE 8000

# Postgres dependencies explained:
# 1. postgresql client is the dependency Pyscopg2 relies on to work. Needs to staty in docker image in prod.
# 2. add virtual tmp build deps is an groupping of the packages that fllow that sentence: musl, postgres dev, etc.
# The latter will be removed in line ~29 after rm -rf line, because it's only needed for installation, but not for running.
# 3. mkdir -p creates the subdirectories too (flag p).
# 4. chown -R django-user:django-user , user and group are called django-user
# 5. Pillow python image manager needs jpeg-dev

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol

#    mkdir -p /vol/web/media \
#    chown -R django-user:django-user /vol && \
#    chmod -R 755 /vol

ENV PATH="/py/bin:$PATH"

USER django-user

