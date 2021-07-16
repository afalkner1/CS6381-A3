from CS6381 import *
import threading

# To run this file on line 223 and 237 of CS6381.py delete the value "extra2"

if __name__ == "__main__":
    b = Broker()
    t1 = threading.Thread(target=b.connect_broker)

    time.sleep(1)
    p = Publisher("Weather")
    p.connect_direct()

    t2 = threading.Thread(target=p.run_pub)

    s = Subscriber("Weather")
    s.connect_direct()

    s2 = Subscriber("Weather")
    s2.connect_direct()

    s3 = Subscriber("Weather")
    s3.connect_direct()

    s4 = Subscriber("Weather")
    s4.connect_direct()

    s5 = Subscriber("Weather")
    s5.connect_direct()

    s6 = Subscriber("Weather")
    s6.connect_direct()

    s7 = Subscriber("Weather")
    s7.connect_direct()

    s8 = Subscriber("Weather")
    s8.connect_direct()

    s9 = Subscriber("Weather")
    s9.connect_direct()

    s10 = Subscriber("Weather")
    s10.connect_direct()

    s11 = Subscriber("Weather")
    s11.connect_direct()

    s12 = Subscriber("Weather")
    s12.connect_direct()

    s13 = Subscriber("Weather")
    s13.connect_direct()

    s14 = Subscriber("Weather")
    s14.connect_direct()

    s15 = Subscriber("Weather")
    s15.connect_direct()

    t3 = threading.Thread(target=s.run_sub_direct)
    t4 = threading.Thread(target=s2.run_sub_direct)
    t5 = threading.Thread(target=s3.run_sub_direct)
    t6 = threading.Thread(target=s4.run_sub_direct)

    t7 = threading.Thread(target=s5.run_sub_direct)
    t8 = threading.Thread(target=s6.run_sub_direct)
    t9 = threading.Thread(target=s7.run_sub_direct)
    t10 = threading.Thread(target=s8.run_sub_direct)

    t11 = threading.Thread(target=s9.run_sub_direct)
    t12 = threading.Thread(target=s10.run_sub_direct)
    t13 = threading.Thread(target=s11.run_sub_direct)
    t14 = threading.Thread(target=s12.run_sub_direct)

    t15 = threading.Thread(target=s13.run_sub_direct)
    t16 = threading.Thread(target=s14.run_sub_direct)
    t17 = threading.Thread(target=s14.run_sub_direct)

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


