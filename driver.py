from CS6381 import *
import threading

if __name__ == "__main__":
    b = Broker()
    t1 = threading.Thread(target=b.connect_broker)

    time.sleep(1)
    p = Publisher(True, "Weather")
    p.connect()

    t2 = threading.Thread(target=p.run_pub)

    s = Subscriber(True, "Weather")
    s.connect()
    t3 = threading.Thread(target=s.run_sub)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t2.setDaemon(True)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()