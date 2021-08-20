from celery_base import task
from random import random
from docker_logs import get_logger

logging = get_logger("runner")

#result = task.delay(random()).get(timeout=10)


#logging.info(f"Task returned: {result}")