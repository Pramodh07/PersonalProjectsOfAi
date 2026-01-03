# Minimal queue abstraction for PoC using Redis lists
import os
import json

try:
    import redis
except Exception:
    redis = None

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
QUEUE_LOG_PATH = os.getenv("QUEUE_LOG_PATH", "queue.log")

class ParseQueue:
    def __init__(self, queue_path: str = None):
        if redis is None:
            self.client = None
        else:
            self.client = redis.from_url(REDIS_URL)
        # allow overriding path for tests
        self.queue_path = queue_path or QUEUE_LOG_PATH

    def push(self, payload: dict):
        if self.client is None:
            # fallback to local file queue for PoC
            with open(self.queue_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(payload) + "\n")
        else:
            self.client.rpush("parse_queue", json.dumps(payload))

    def pop(self):
        if self.client is None:
            # read from local file queue (first-in-first-out)
            try:
                lines = []
                with open(self.queue_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                if not lines:
                    return None
                first = lines[0]
                # rewrite remaining lines
                with open(self.queue_path, "w", encoding="utf-8") as f:
                    f.writelines(lines[1:])
                return json.loads(first)
            except FileNotFoundError:
                return None
        item = self.client.lpop("parse_queue")
        if item:
            return json.loads(item)
        return None

    def clear(self):
        if self.client is None:
            try:
                open(self.queue_path, "w", encoding="utf-8").close()
            except Exception:
                pass
        else:
            try:
                self.client.delete("parse_queue")
            except Exception:
                pass
