#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import ssl
import paho.mqtt.client as mqtt
from os import system, name

from tabulate import tabulate
#import arrow


import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 30)
pd.options.display.width = 0

from mqtt_conf import *

maxlen = 5
topicDict = {}


def gotoxy(x, y):
    print("%c[%d;%df" % (0x1B, y, x), end='')


def cls():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


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
    global topicDict

    data = [ "{:%Y-%m-%d %H:%M:%S}".format(datetime.now()) ]

    topicSplit = msg.topic.split("/") 

    if len(topicSplit) > maxlen:
        maxlen = len(topicSplit)

    topicSplit.extend([' '] * (maxlen - len(topicSplit)))

    # topicSplit = [colorString(s) for s in topicSplit]

    #topicFormat = len(topicSplit) * '{:.<25}'
    #topic = topicFormat.format(*topicSplit)
    # topic = "".join(topicSplit)

    payload = colorString(str(msg.payload.decode("utf-8")))

    # payload = str(msg.payload.decode("utf-8"))

    # toPrint = "[{:%Y-%m-%d %H:%M:%S}] {:.<79}-> {}".format(
    #     datetime.now(), topic, payload)

    # topicDict[msg.topic] = toPrint

    # topicIndex = list(topicDict).index(msg.topic)
    # gotoxy(0,5+topicIndex)
    # print(toPrint)

    topicSplit.append(payload)

    topicDict[msg.topic] = data + [colorString(s) for s in topicSplit]

    toDisplay = tabulate (pd.DataFrame.from_dict(topicDict,  orient='index').sort_index())
    cls()

    print("Last uppdate: {:%Y-%m-%d %H:%M:%S}".format(datetime.now()))

    #print(topicDict)
    gotoxy(0, 3)
    print ( toDisplay )
    #print ( tabulate (topicDict) )


    # y = 0
    # for key in sorted(topicDict):
    #     y += 1
    #     gotoxy(0, 3 + y)
    #     print(topicDict[key])


def colorString(string):

    if string in colorDict:
        string = colorDict[string] + string + colors.reset
    # else:
    #     string = colors.fg.lightgrey + string + colors.reset

    # stringFormat = '{:<25}'
    # return stringFormat.format(string)
    return string


if __name__ == "__main__":

    cls()
    gotoxy(0, 0)

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
