FROM python:3.9-slim

RUN apt-get update && apt-get install -y redis-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY redis.conf /etc/redis/redis.conf
COPY entrypoint.sh /usr/local/bin/
COPY shutdown.sh /usr/local/bin/

VOLUME /redis-cache

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

EXPOSE 8000
EXPOSE 6379

ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379

WORKDIR /app/fin_maestro_kin

RUN chmod +x /usr/local/bin/entrypoint.sh /usr/local/bin/shutdown.sh

RUN touch /var/log/redis/redis-server.log && chown redis:redis /var/log/redis/redis-server.log

ENTRYPOINT ["bash", "/usr/local/bin/entrypoint.sh"]
