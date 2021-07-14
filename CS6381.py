import zmq
from zmq.utils.monitor import recv_monitor_message
import threading
import time
import random
import matplotlib.pyplot as plt
import netifaces as ni
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.exceptions import (
    ConnectionClosedError,
    NoNodeError,
    KazooException
)
import configparser
import uuid
import socket
import fcntl
import struct
import os

context = zmq.Context()
zkserver = "10.0.0.1:2181"

class Broker():
    def __init__(self):
        self.id = uuid.uuid4()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        self.ip = get_ip()
        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()
        self.path = "/broker"
        self.election_path = "/broker-election"

    def connect_broker(self):
        print(f"Broker: {self.ip}")

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
    def __init__(self, topic = 8):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        # unique id to every publisher
        self.id = uuid.uuid4()
        self.topic = topic;
        self.path_b = f"/topic/{topic}"
        self.path = f"/topic/{topic}/pub"
        self.broker_path = "/broker"

        self.ip = get_ip()
        self.socket = context.socket(zmq.PUB)
        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()


    def connect(self):

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
        self.socket.send_string(f'{topic} {messagedata}')

    def run_pub(self):
        while True:
            publisher_id = random.randrange(0, 9999)
            sent_time = time.time()
            msg = f'{publisher_id} {self.topic} {sent_time}'
            self.publish(self.topic, msg)
            print(publisher_id, self.topic, sent_time)
            time.sleep(1)


class Subscriber():

    def __init__(self, topic = 8):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.ports = config['PORT']
        self.port = self.ports['PUBP']
        self.topic = topic
        self.broker_path = "/broker"
        self.path = f"/topic/{topic}/sub"
        self.pub_path = f"/topic/{topic}/pub"
        self.ip = get_ip()
        self.socket = context.socket(zmq.SUB)
        self.zk = KazooClient(hosts=zkserver)
        self.zk.start()

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

    def connect_direct(self):
        @self.zk.DataWatch(self.pub_path)
        def pub_watcher(data, stat):
            if data is not None:
                new_ip = data.decode('utf-8')
                conn_str = f'tcp://{new_ip}:{self.port}'
                print(f"connecting: {conn_str}")
                self.socket.connect(conn_str)

        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)


    def listen(self):
        return self.socket.recv_string()

    def run_sub(self):
        while True:
            rec_time = time.time()
            f = open("times.txt", "a")
            message = self.listen()
            extra, pub_id, topic, sent_time = message.split()
            print("Subscriber recieved message: ")
            print(pub_id, topic, sent_time)
            print("\n")
            f.write(f"{pub_id} , {sent_time} , {rec_time} \n")
            f.close()
            time.sleep(1)


def get_ip():
    interfces = ni.interfaces()[1]
    return ni.ifaddresses(interfces)[ni.AF_INET][0]['addr']

