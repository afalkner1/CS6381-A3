# CS6381-A2

This project is a pub-sub model with a broker. Zookeeper is used for broker leader election. 
Files broker.py, Subscriber.py and publisher.py run all the Zookeeper and ZeroMQ middleware in CS6381.py. 

## How this project works

A broker wins the Zookeeper election and creates and ephemeral znode at the location /broker-election. The publishers then create ephemeral nodes at the location /topic/{topic}/pub/{pub_id}. Subscribes then create ephemeral nodes at the location /topic/{topic}/sub/{sub_id}. They publishers and subscribers then perform regular message sending/recieving. 

There are two approaches to recieve messagess. 

1) Broker

In this method messages are sent from the publisher, to the broker, who then forwards the messages onto the subscribers 

2) Direct 

In this method messages are sent directly from the publishers to the subscribers. 


## Please refer to the video below to see tests 

https://www.youtube.com/watch?v=Tqswv4DCiaM

## To run on mininet 
First create a topology of hosts
```
sudo mn --topo=tree,depth=1,fanout=6
```
### First start Zookeper in host 1 
Note: Zookeeper must be started in host 1.

### Host 1
```
> cd <your distribution of zookeeper>

> ./bin/zkServer.sh start

```

### Host 2
Run first broker
Note: There might be a warning flag, you can ignore this or export NO_AT_BRIDGE=1
```
> cd <my CS6381-A2 file>
> python3 broker.py

```

### Host 3
Run second broker
```
> cd <my CS6381-A2 file>
> python3 broker.py

```

### Host 4
Run third broker 
```
> cd <my CS6381-A2 file>
> python3 broker.py

```
### Host 5
{topic} is a topic of your choosing for the publisher eg. Weather, 45 ect. 
The second argument states which approach you want to use to sent messages. 
Type "broker" to send messages through broker

Note: You must run the publisher before the subscriber
```
> cd <my CS6381-A2 file>
> python3 publisher.py {topic} broker

```
### Host 6
{topic} is a topic of your choosing for the Subscriber eg. Weather, 45 ect. 
The second argument states which approach you want to use to recieve messages. 
Type "broker" to recieve messages through broker

Note: You must use same method for both Subscribers and Publishers
```
> cd <my CS6381-A2 file>
> python3 Subscriber.py {topic} broker

```

### Stop first broker

Close Host 2 window. 
Wait and few seconds and then you will see new broker elected 


### Stop second broker

Close Host 3 window 
Wait and few seconds and then you will see new broker elected 



## Tests and Graphs

Graph to show message times as hosts increase using approach one. 
![data](/images/broker.png)

Graph to show message times as hosts increase using approach two. 
![data](/images/direct.png)

Comparing this data 
![data](/images/both.png)

## Responsibilities 

We met over Zoom to plan out our project and implementation. Then, both developed the code independently and would Zoom periodically to discuss what changes we had made. 

All changes were commited through Alex's github account but we shared and both made edits. 

Alex then commented, and tested the code, creating the graphs.


