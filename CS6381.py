import zmq
import time
import random
import netifaces as ni
from kazoo.client import KazooClient
import configparser
import uuid

context = zmq.Context()
zkserver = "10.0.0.1:2181"
socket_arr = []
zone_list =[1, 2, 3]
ZONE_THRESHOLD = 2

topics ={"weather": 3, "golf": 3, "hats": 3, "test": 3}

class Broker():
    def __init__(self,zone):
        self.zone = zone
        self.id = uuid.uuid4()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        self.ip = get_ip()
        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()
        self.path_zone = f"/{self.zone}"
        self.path = f"/{self.zone}/broker"
        self.election_path = f"/{self.zone}/broker-election"

    def connect_broker(self):
        print(f"Broker: {self.ip}")

        if not self.zk.exists(self.path_zone):
            self.zk.create(self.path_zone)

        if not self.zk.exists(self.election_path):
            self.zk.create(self.election_path)

        print("Starting Leader Election")
        election = self.zk.Election(self.election_path, self.ip)
        election.run(self.leader_elected)

    def leader_elected(self):
        print("Leader is now Elected")
        print("Leader broker now connecting to subs and pubs")

        @self.zk.DataWatch(self.path)
        def broker_watcher(data, stat):
            print(("Broker::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is None:
                if not self.zk.exists(self.path):
                    self.zk.create(self.path, value=self.ip.encode(
                        'utf-8'), ephemeral=True)

            # Connect Broker
            print("This is broker: creating xsub and xpubsockets")
            xsubsocket = context.socket(zmq.XSUB)
            xsubsocket.bind("tcp://*:{}".format(self.ports['SUBP']))

            xpubsocket = context.socket(zmq.XPUB)
            xpubsocket.setsockopt(zmq.XPUB_VERBOSE, 1)
            xpubsocket.bind("tcp://*:{}".format(self.ports['PUBP']))

            zmq.proxy(xsubsocket, xpubsocket)


class Publisher:
    def __init__(self, topic = "weather",hist = 3):
        self.history = int(hist)
        self.window = ["0 0","0 0","0 0"]
        self.count = 0
        self.index = ""

        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        # unique id to every publisher
        self.id = uuid.uuid4()
        self.publisher_id = random.randrange(0, 9999)
        print(f"Pub id: {self.publisher_id}")

        self.topic = topic
        self.zone = 0
        self.topic_path = f"/{self.topic}"

        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()


        # Round Robin load balancing

        # If topic doesn't exist randomly assign to zone
        # Make sure zone is not full

        if not self.zk.exists(self.topic_path):
            self.zk.create(self.topic_path)
            num = random.choice(range(0, 2))
            if not self.zk.exists(f"/{num}/topic"):
                self.zk.create(f"/{num}/topic")

            children = self.zk.get_children(f"/{num}/topic", False)
            print("children:")
            print(children)
            if len(children) > ZONE_THRESHOLD -1:
                print("---------------------")
                print(f"TOO MANY TOPICS in zone {num}")
                print("Adding topic to other zone")
                print("---------------------")
                self.zone = (num + 1) % 2
                if not self.zk.exists(f"/{self.zone}/topic"):
                    self.zk.create(f"/{self.zone}/topic")
            else:
                self.zone = num
            self.zk.create(f"/{self.topic}/{self.zone}")
        # if the topic has already been created
        else:
            if self.zk.exists(f"/{self.topic}/0"):
                self.zone = 0
            else:
                self.zone = 1

        print(f"Publisher is in zone: {self.zone}")

        self.election_path = f"/{self.zone}/topic/{topic}/pub_election"
        self.path_zone = f"/{self.zone}"
        self.path_test = f"/{self.zone}/topic"
        self.path_test2 = f"/{self.zone}/topic/{topic}"
        self.path_b = f"/{self.zone}/topic/{topic}/pub"
        self.path = f"/{self.zone}/topic/{topic}/pub/{self.publisher_id}"
        self.broker_path = f"/{self.zone}/broker"
        self.ip = get_ip()
        self.socket = context.socket(zmq.PUB)

    def connect1(self):

        # if not self.zk.exists(self.path_test):
        #     self.zk.create(self.path_test)
        # children = self.zk.get_children(self.path_test, False)
        # print("children:")
        # print(children)
        # for child in children:
        #     print("new child")

        if not self.zk.exists(self.path_test):
            self.zk.create(self.path_test)

        if not self.zk.exists(self.path_test2):
            self.zk.create(self.path_test2)

        if not self.zk.exists(self.election_path):
            self.zk.create(self.election_path)

        self.set_broker_watch()

        print("Waiting for publisher with highest ownership strength")
        election = self.zk.Election(self.election_path, self.ip)
        election.run(self.leader_elected)

    def connect2(self):
        if not self.zk.exists(self.path_test):
            self.zk.create(self.path_test)

        if not self.zk.exists(self.path_test2):
            self.zk.create(self.path_test2)

        if not self.zk.exists(self.election_path):
            self.zk.create(self.election_path)

        print("Waiting for publisher with highest ownership strength")
        election = self.zk.Election(self.election_path, self.ip)
        election.run(self.leader_elected)

    def leader_elected(self):
        print("Publishers with highest leadership strength chosen")
        print("Leader Pub now connecting")

        @self.zk.DataWatch(self.path_b)
        def pub_watcher(data, stat):
            print(("Broker::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is None:
                if not self.zk.exists(self.path_b):
                    self.zk.create(self.path_b, value=self.ip.encode(
                        'utf-8'), ephemeral=True)

            self.port = self.ports['SUBP']
            conn_str = f'tcp://{self.ip}:{self.port}'
            print(f"binding: {conn_str}")
            self.socket.bind("tcp://*:5556")

        self.run_pub()

    def set_broker_watch(self):
        # Connect Publisher
        @self.zk.DataWatch(self.broker_path)
        def broker_watcher(data, stat):
            print(("Publisher::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is not None:
                new_ip = data.decode('utf-8')
                self.port = self.ports['SUBP']
                conn_str = f'tcp://{new_ip}:{self.port}'
                print(f"Publisher connecting to broker at ip: {new_ip} port: {self.port}")
                self.socket.connect(conn_str)

    def connect(self):

        if not self.zk.exists(self.path_zone):
            self.zk.create(self.path_zone)

        if not self.zk.exists(self.path_test):
            self.zk.create(self.path_test)

        if not self.zk.exists(self.path_test2):
            self.zk.create(self.path_test2)

        if not self.zk.exists(self.path_b):
            self.zk.create(self.path_b)

        print(f"Publisher: creating znode {self.path}:{self.ip}")
        self.zk.create(self.path, value=self.ip.encode(
            'utf-8'), ephemeral=True)

        @self.zk.DataWatch(self.broker_path)
        def broker_watcher(data, stat):
            print(("Publisher::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is not None:
                new_ip=data.decode('utf-8')
                self.port = self.ports['SUBP']
                conn_str = f'tcp://{new_ip}:{self.port}'
                print(f"Publisher connecting to broker at ip: {new_ip} port: {self.port}")
                self.socket.connect(conn_str)


    def connect_direct(self):

        if not self.zk.exists(self.path_test):
            self.zk.create(self.path_test)

        if not self.zk.exists(self.path_test2):
            self.zk.create(self.path_test2)

        if not self.zk.exists(self.path_b):
            self.zk.create(self.path_b)

        print(f"Publisher: creating znode {self.path}:{self.ip}")
        self.zk.create(self.path, value=self.ip.encode(
            'utf-8'), ephemeral=True)

        self.port = self.ports['SUBP']
        conn_str = f'tcp://{self.ip}:{self.port}'
        print(f"binding: {conn_str}")
        self.socket.bind("tcp://*:5556")

    def publish(self, topic, messagedata):
        self.socket.send_string(f"{topic}{messagedata}")

    def run_pub(self):

        while True:
            self.count = 0;
            while self.count < self.history:
                publisher_id = self.publisher_id
                sent_time = time.time()
                blah = random.randrange(1, 50)
                msg = f'{publisher_id} {blah}'
                self.window[self.count] = msg
                self.index = f", {self.history},"
                for w in self.window:
                    self.index = self.index+ " "+ w
                self.index = self.index + ", "
                self.publish(self.topic, self.index)
                print(f"sent: {self.index}")
                self.count = self.count + 1
                time.sleep(1)


class Subscriber():

    def __init__(self, topic = 8, hist = 3):
        self.history = int(hist)
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        self.port = self.ports['PUBP']
        self.topic = topic
        self.sub_id = random.randrange(0, 9999)
        self.zone = 0

        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()

        # check for correct zone
        if self.zk.exists(f"/{self.topic}/0"):
            self.zone = 0
        else:
            self.zone = 1


        print(f"Subscriber is in zone: {self.zone}")

        self.path_zone = f"/{self.zone}"
        self.broker_path = f"/{self.zone}/broker"
        self.path_s = f"/{self.zone}/topic/{topic}/sub"
        self.path = f"/{self.zone}/topic/{topic}/sub/{self.sub_id}"
        self.pub_path = f"/{self.zone}/topic/{topic}/pub"
        self.ip = get_ip()
        self.socket = context.socket(zmq.SUB)


        if not self.zk.exists(self.path_s):
            self.zk.create(self.path_s)

        print(f"Subscriber: creating znode {self.path}:{self.ip}")
        self.zk.create(self.path, value=self.ip.encode(
            'utf-8'), ephemeral=True)

    def connect(self):
        print(f"Subscriber: {self.ip}")
        @self.zk.DataWatch(self.broker_path)
        def broker_watcher(data, stat):
            print(("Sub::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is not None:
                new_ip=data.decode('utf-8')
                conn_str = f'tcp://{new_ip}:{self.port}'
                print(f"connecting: {conn_str}")
                self.socket.connect(conn_str)

        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def connect1(self):
        print(f"Subscriber: {self.ip}")

        @self.zk.DataWatch(f"/{self.zone}/topic/{self.topic}/pub")
        def broker_watcher(data, stat):
            print(("Sub::broker_watcher - data = {}, stat = {}".format(data, stat)))
            if data is not None:
                new_ip=data.decode('utf-8')
                conn_str = f'tcp://{new_ip}:{self.port}'
                print(f"connecting: {conn_str}")
                self.socket.connect(conn_str)

        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def connect_direct(self):
        chilren = self.zk.get_children(self.pub_path, False)
        count = 0
        for child in chilren:
            new_path = f"/topic/{self.topic}/pub/{child}"
            sk = context.socket(zmq.SUB)
            socket_arr.append(sk)
            @self.zk.DataWatch(new_path)
            def children_watcher(data, stat):
                if data is not None:
                    new_ip = data.decode('utf-8')
                    conn_str = f'tcp://{new_ip}:{self.port}'
                    print(f"connecting: {conn_str}")
                    socket_arr[count].connect(conn_str)

            socket_arr[count].setsockopt_string(zmq.SUBSCRIBE, self.topic)
            count = count + 1


    def listen(self):
        return self.socket.recv_string()

    def listen_d(self, sk):
        return sk.recv_string()


    def run_sub(self):
        while True:
            word = ""
            rec_time = time.time()
            f = open("times.txt", "a")
            message = self.listen()
            # extra, extra2, topic, sub_history,msg = message.split()
            # print(f"{topic} {sub_history} {msg}")
            x = message.split(", ")
            sub_history = x[1]
            ha = x[2].split(" ")

            first = False
            n = 0
            for thing in ha:
                if thing == '0':
                    n = n + 2
                    first = True
                else:
                    n = n + 1

            if self.history > n/2:
                print("History too high. Subscriber did not meet match conditions. ")
                break

            i = 0
            print("Subscriber recieved message: ")
            while i < self.history *2:
                if (i%2 == 0):
                    word = word + f" {self.topic} " + ha[i]
                else:
                    word = word + " " + ha[i]
                i = i +1

            print(f"{word}")

            print("\n")
            # f.write(f"{sent_time} , {rec_time} \n")
            f.close()
            time.sleep(1)

    def run_sub_direct(self):
        while True:
            for sk in socket_arr:
                rec_time = time.time()
                f = open("times.txt", "a")
                message = self.listen_d(sk)
                extra, pub_id, extra2, topic, sent_time = message.split()
                print("Subscriber recieved message: ")
                print(pub_id, topic, sent_time)
                print("\n")
                f.write(f"{pub_id} , {sent_time} , {rec_time} \n")
                f.close()
                time.sleep(1)



def get_ip():
    interfces = ni.interfaces()[1]
    return ni.ifaddresses(interfces)[ni.AF_INET][0]['addr']

