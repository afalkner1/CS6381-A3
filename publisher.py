import sys
from random import randrange
import argparse
from CS6381 import Publisher
import time
import uuid
import random

topic = sys.argv[1]
p = Publisher(topic)
p.connect()

while True:
    publisher_id = p.publisher_id
    text = random.randrange(0, 9999)
    sent_time = time.time()
    msg = f'{publisher_id} {topic} {text} {sent_time}'
    p.publish(topic,msg)
    print(publisher_id, topic, sent_time)
    time.sleep(1)

