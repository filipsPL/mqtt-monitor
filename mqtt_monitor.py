#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from time import sleep

import ssl
import paho.mqtt.client as mqtt
from os import system, name, path


import argparse
from configparser import ConfigParser

from tabulate import tabulate

import signal
import sys

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 30)
pd.options.display.width = 0

from mqtt_conf import *

maxlen = 5
topicDict = {}


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)


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
    global ts

    data = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
    ts = datetime.now().timestamp()

    topicSplit = msg.topic.split("/")

    if len(topicSplit) > maxlen:
        maxlen = len(topicSplit)

    topicSplit.extend([' '] * (maxlen - len(topicSplit)))

    payload = colorString(changeString(str(msg.payload.decode("utf-8"))))

    topicSplit.append(payload)

    topicDict[msg.topic] = [ts] + [data] + [colorString(changeString(s)) for s in topicSplit]

    # final calculations on Pandas DataFrame
    toDisplayDf = pd.DataFrame.from_dict(topicDict, orient='index')
    toDisplayDf.insert(1, "ago", 0)
    toDisplayDf["ago"] = toDisplayDf[0].apply(pretty_date)
    toDisplayDf = toDisplayDf.drop([0, 1], axis=1)

    toDisplayDf = toDisplayDf.sort_index()  # .drop([1], axis=1)

    # .drop([1], axis=1).sort_index()
    # for key in topicDict:
    #     timeAgo = int(ts - topicDict[key][0])
    #     topicDictCopy[key] = [timeAgo] + topicDict[key]

    # toDisplay = topicDict
    # exit(1)
    toDisplay = tabulate(toDisplayDf)
    cls()

    displayStatus()

    #print(topicDict)
    gotoxy(0, 3)
    print(toDisplay)
    #print ( tabulate (topicDict) )

    # y = 0
    # for key in sorted(topicDict):
    #     y += 1
    #     gotoxy(0, 3 + y)
    #     print(topicDict[key])


def displayStatus():
    gotoxy(0, 0)
    print(
        "Now is: {:%Y-%m-%d %H:%M:%S}\t Last update: {}\t Connected to: {}:{}".
        format(datetime.now(), pretty_date(ts), host, port))


def changeString(string):

    if string in wordDict:
        print (string)
        string = wordDict[string]

    return string


def colorString(string):

    if string in colorDict:
        string = colorDict[string] + string + colors.reset

    return string


def parseArguments():
    parser = argparse.ArgumentParser(
        description='''Program for clustering data''',
        add_help=True,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        conflict_handler='resolve')


    optional_arguments = parser.add_argument_group('Optional arguments')

    optional_arguments.add_argument(
        '--conf',
        help='config file',
        dest="configFile",
    )

    return parser.parse_args()


if __name__ == "__main__":

    ts = datetime.now().timestamp()


    configFile = path.join(path.dirname(__file__), 'mqtt_monitor.conf')
    print ("configFile", configFile)
    config = ConfigParser()
    config.read(configFile)

    host = config['server']['host']
    port = config['server']['port']
    username = config['server']['username']
    password = config['server']['password']
    usessl = config['server']['usessl']

    topics = config['topics']['topics']

    wordDict = config._sections['tunables']
    coloring = config._sections['coloring']

    print(wordDict)

    exit(1)
    _ = parseArguments()

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

    signal.signal(signal.SIGINT, signal_handler)
    print('Press Ctrl+C')

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

    # client.loop_forever()

    client.loop_start()

    while True:
        displayStatus()
        sleep(1)
