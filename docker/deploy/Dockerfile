FROM python:3.8.12-slim

ENV PYTHONPATH "${PYTHONPATH}:/srv:/srv/src"

COPY . /srv/
WORKDIR /srv

RUN apt-get update && \
    apt-get install -y \
    gcc curl

COPY ./docker/deploy/entrypoint.sh /tmp/entrypoint.sh

RUN pip install poetry && \
    POETRY_VIRTUALENVS_CREATE=false poetry install --no-ansi

RUN useradd -d /srv metrics \
    && chown metrics:metrics /srv

USER "metrics"

ENTRYPOINT ["sh", "/tmp/entrypoint.sh"]

CMD ["uwsgi", "--ini", "/etc/uwsgi/conf.d/uwsgi.ini"]

EXPOSE 8000
