import time

import redis
from fastapi import FastAPI

app = FastAPI()
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 10
    while True:
        try:
            return cache.decr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.get("/")
async def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
    