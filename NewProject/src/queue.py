# Minimal queue abstraction for PoC using Redis lists
import os
import json

try:
    import redis
except Exception:
    redis = None

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

class ParseQueue:
    def __init__(self):
        if redis is None:
            self.client = None
        else:
            self.client = redis.from_url(REDIS_URL)

    def push(self, payload: dict):
        if self.client is None:
            # fallback to local file queue for PoC
            with open("queue.log", "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        else:
            self.client.rpush("parse_queue", json.dumps(payload))

    def pop(self):
        if self.client is None:
            # read from local file queue (first-in-first-out)
            try:
                lines = []
                with open("queue.log", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if not lines:
                    return None
                first = lines[0]
                # rewrite remaining lines
                with open("queue.log", "w", encoding="utf-8") as f:
                    f.writelines(lines[1:])
                return json.loads(first)
            except FileNotFoundError:
                return None
        item = self.client.lpop("parse_queue")
        if item:
            return json.loads(item)
        return None
