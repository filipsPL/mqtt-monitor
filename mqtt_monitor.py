#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import ssl
import paho.mqtt.client as mqtt

from mqtt_conf import *

maxlen = 3


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in topics:
        client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    global maxlen

    topicSplit = msg.topic.split("/")

    if len(topicSplit) > maxlen:
        maxlen = len(topicSplit)

    topicSplit.extend(['.'] * (maxlen - len(topicSplit)))

    topicSplit = [colorString(s) for s in topicSplit]

    #topicFormat = len(topicSplit) * '{:.<25}'
    #topic = topicFormat.format(*topicSplit)
    topic = "".join(topicSplit)

    payload = colorString(str(msg.payload.decode("utf-8")))

    toPrint = "[{:%Y-%m-%d %H:%M:%S}] {:.<79}-> {}".format(
        datetime.now(), topic, payload)
    print(toPrint)


def colorString(string):
    if string in colorDict:
        string = colorDict[string] + string + colors.reset
    else:
        string = colors.fg.lightgrey + string + colors.reset

    return '{:<25}'.format(string)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username, password=password)

if usessl:
    client.tls_set(cert_reqs=ssl.CERT_NONE)
    client.tls_insecure_set(True)

client.connect(host, port, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
