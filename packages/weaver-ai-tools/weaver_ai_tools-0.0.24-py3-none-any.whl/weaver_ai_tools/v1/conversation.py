
import logging
import threading
import json

import redis
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

from .functions import internal_requests
from .config import configuration

class Conversation:
    def get_messages(conversation_id):
        response = internal_requests.get(f"http://web:8000/api/v1/conversations/{conversation_id}").json()
        return response.get("params")

    def add_message(message):
        if configuration.get("delay_response")
            delay_interval = 3 # seconds

            redis_key = f"conversaion_{conversation_id}_queue"
            queue = redis_client.get(redis_key)
            if not queue:
                queue = []
            else:
                queue = json.loads(queue)
            queue.append(query)
            redis_client.set(redis_key, json.dumps(queue))

        threading.Thread(target=run_delay, args=(delay_interval, redis_key)).start()
        print("This is being handled by the bff for now, comming soon.")

    def on_initialize():
        print("comming soon...")
    
    
    def run_delay(time_interval, redis_key):
        messages = redis_client.get(redis_key)

        logging.info(messages)

        time.sleep(time_interval)
        
        if len(messages) == 0: return
        messages = redis_client.get(redis_key)
        redis_client.set(redis_key, "[]")