#!/bin/bash
cd /app/fin_maestro_kin
redis-server /etc/redis/redis.conf
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
bash /usr/local/bin/shutdown.sh
