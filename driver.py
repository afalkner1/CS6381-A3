from CS6381 import *
import threading

if __name__ == "__main__":
    b = Broker()
    t1 = threading.Thread(target=b.connect_broker)

    time.sleep(1)
    p = Publisher("Weather")
    p.connect()

    t2 = threading.Thread(target=p.run_pub)

    s = Subscriber("Weather")
    s.connect()

    s2 = Subscriber("Weather")
    s2.connect()

    s3 = Subscriber("Weather")
    s3.connect()

    s4 = Subscriber("Weather")
    s4.connect()

    s5 = Subscriber("Weather")
    s5.connect()

    s6 = Subscriber("Weather")
    s6.connect()

    s7 = Subscriber("Weather")
    s7.connect()

    s8 = Subscriber("Weather")
    s8.connect()

    s9 = Subscriber("Weather")
    s9.connect()

    s10 = Subscriber("Weather")
    s10.connect()

    s11 = Subscriber("Weather")
    s11.connect()

    s12 = Subscriber("Weather")
    s12.connect()

    s13 = Subscriber("Weather")
    s13.connect()

    s14 = Subscriber("Weather")
    s14.connect()

    s15 = Subscriber("Weather")
    s15.connect()

    t3 = threading.Thread(target=s.run_sub)
    t4 = threading.Thread(target=s2.run_sub)
    t5 = threading.Thread(target=s3.run_sub)
    t6 = threading.Thread(target=s4.run_sub)

    t7 = threading.Thread(target=s5.run_sub)
    t8 = threading.Thread(target=s6.run_sub)
    t9 = threading.Thread(target=s7.run_sub)
    t10 = threading.Thread(target=s8.run_sub)

    t11 = threading.Thread(target=s9.run_sub)
    t12 = threading.Thread(target=s10.run_sub)
    t13 = threading.Thread(target=s11.run_sub)
    t14 = threading.Thread(target=s12.run_sub)

    t15 = threading.Thread(target=s13.run_sub)
    t16 = threading.Thread(target=s14.run_sub)
    t17 = threading.Thread(target=s14.run_sub)

    t1.setDaemon(True)
    t2.setDaemon(True)
    t3.setDaemon(True)
    t4.setDaemon(True)
    t5.setDaemon(True)
    t6.setDaemon(True)

    t7.setDaemon(True)
    t8.setDaemon(True)
    t9.setDaemon(True)
    t10.setDaemon(True)

    t11.setDaemon(True)
    t12.setDaemon(True)
    t13.setDaemon(True)
    t14.setDaemon(True)
    t15.setDaemon(True)


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()

    t7.start()
    t8.start()
    t9.start()
    t10.start()

    t11.start()
    t12.start()
    t13.start()
    t14.start()
    t15.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()

    t7.join()
    t8.join()
    t9.join()
    t10.join()

    t11.join()
    t12.join()
    t13.join()
    t14.join()
    t15.join()


