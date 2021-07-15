import sys
import time
from CS6381 import *


s = Subscriber(sys.argv[1])
if (sys.argv[2] == "direct"):
    s.connect_direct()
    s.run_sub_direct()
else:
    s.connect()
    s.run_sub()
#
# while True:
#     rec_time = time.time()
#     f = open("times.txt", "a")
#     message = s.listen()
#     extra, pub_id, topic, text, sent_time = message.split()
#     print("Subscriber recieved message: ")
#     print(pub_id, topic, text, sent_time)
#     print("\n")
#     f.write(f"{pub_id} , {sent_time} , {rec_time} \n")
#     f.close()
#     time.sleep(1)