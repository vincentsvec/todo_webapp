FROM python:3.9-alpine3.13
LABEL maintainer: "vincentsvec.github.io"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./todo_app /todo_app
COPY ./scripts /scripts

WORKDIR /todo_app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
    build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home todo_app && \
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R todo_app:todo_app /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts


ENV PATH="/scripts:/py/bin:$PATH"

USER todo_app

CMD ["run.sh"]