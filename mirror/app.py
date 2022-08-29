from redis import Redis
from flask import Flask, Response, request, abort
from uuid import uuid4
from json import dumps
from time import sleep
from re import compile
import httpx

from .event import Event
from settings import policy, redis as redisconf

app = Flask(__name__)
redis: Redis = Redis(*redisconf.address, decode_responses=True)

@app.route("/")
async def details():
    """ View details about Mirror installation """

    return "I'm a teapot!", 418

@app.route("/subscribe", methods=["GET"])
async def subscribe():
    """ Subscribe to event stream """

    ttl: int = request.args.get("ttl", default=policy.min_ttl, type=int)
    if ttl < policy.min_ttl:
        abort(403)

    url: str = request.args.get("url", type=str)
    if not url or not url_regex.match(url):
        abort(400)
    
    ray_id: str = str(uuid4())

    def stream():
        """ Stream events """

        while True:

            sleep(ttl)

            try:
                response = httpx.get(url=url)
                data = response.json()
            except Exception as exception:
                return Event(ray_id=ray_id, code=response.status_code,
                        data={"message": str(exception)}) \
                        .format()
            
            # If data isn't changed - ignore
            json = dumps(data)
            if redis.get(ray_id) == json:
                continue

            redis.set(ray_id, json)
            yield Event(ray_id=ray_id, code=response.status_code, data=data).format()

    return Response(stream(), mimetype="text/event-stream")