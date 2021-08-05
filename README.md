# CS6381-A3

This project is a pub-sub model with a broker. It implemennts fault-tolerance, load-balancing, ownership strength and history. Zookeeper is used for broker leader election, and ownership strength. 

Files broker.py, Subscriber.py and publisher.py run all the Zookeeper and ZeroMQ middleware in CS6381.py. 

## How this project works

The znode heirachy can be seen above. For load balancing I have implemented two zones (0 and 1). Each zone has a threshhold for the number of topics it can have. I have used a Round Robin approach whereby when a topic is registered, it is randomly assigned to a zone. Then when one zone is full, the system direct new topics to the zone with space. Each zone has a primary broker and then back-up brokers for fault-tolerance. The primary broker in zone one represents the replica broker. Ownership strength is observed by having the first publisher to that topic having the highest proroty, and then the second publisher to that topic having the secod highest priority. I have implemented this using Zookeeper election. 

There are two approaches to recieve messagess. 

1) Broker

In this method messages are sent from the publisher, to the broker, who then forwards the messages onto the subscribers 

2) Direct 

In this method messages are sent directly from the publishers to the subscribers. 


## Please refer to the video below to see tests 

https://www.youtube.com/watch?v=7kZp_XuEMnc

## To run on mininet 
First create a topology of hosts
```
sudo mn --topo=tree,depth=1,fanout=10
```
### First start Zookeper in host 1 
Note: Zookeeper must be started in host 1.

### Host 1
```
> cd <your distribution of zookeeper>

> ./bin/zkServer.sh start

```

### Host 2
Run first primary broker
Note: There might be a warning flag, you can ignore this or export NO_AT_BRIDGE=1
```
> cd <my CS6381-A2 file>
> python3 broker.py 0

```

### Host 3
Run second primary broker
```
> cd <my CS6381-A2 file>
> python3 broker.py 1

```

### Host 4
Run first publisher 
{topic} is a topic of your choosing for the publisher eg. Weather, 45 ect. 
The second argument states which approach you want to use to sent messages. 
Type "broker" to send messages through broker. 
{hist} is a number for the history window you want

Note: You must run the publisher before the subscriber
```
> cd <my CS6381-A2 file>
> python3 publisher.py {topic} broker {hist}

```
### Host 5
Run second publisher (use new topic)
```
> cd <my CS6381-A2 file>
> python3 publisher.py {topic} broker {hist}

```
### Host 6
Run third publisher  (use new topic)
```
> cd <my CS6381-A2 file>
> python3 publisher.py {topic} broker {hist}

```
### Host 7
Run fourth publisher  (use new topic)
```
> cd <my CS6381-A2 file>
> python3 publisher.py {topic} broker {hist}

```
### Host 8
Run first Subscriber
{topic} is a topic of your choosing for the subscriber eg. Weather, 45 ect. 
The second argument states which approach you want to use to sent messages. 
Type "broker" to send messages through broker. 
{hist} is a number for the history window you want

Note: You must run the publisher before the subscriber
```
> cd <my CS6381-A2 file>
> python3 Subscriber.py {topic} broker {hist}

```

If threshold =3 you will see that on host 6 or host 7 there will be message that one of the zones is full and so the new topic is sent to the free zone. 


## Tests and Graphs

Graph to show message times as hosts increase using approach one. 
![data](/images/broker.png)

Graph to show message times as hosts increase using approach two. 
![data](/images/direct.png)

Comparing this data 
![data](/images/both.png)





