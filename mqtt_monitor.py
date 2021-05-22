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

from colors import *

maxlen = 5
topicDict = {}
messages = 0


def signal_handler(sig, frame):
    print("\n\n\nYou pressed Ctrl+C!\n\n\n")
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
        # print ("subscribing to", topic)
        client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    global maxlen
    global topicDict
    global ts
    global messages

    data = "{:%Y-%m-%d %H:%M:%S}".format(datetime.now())
    ts = datetime.now().timestamp()
    messages += 1

    topicSplit = msg.topic.split("/")

    if len(topicSplit) > maxlen:
        maxlen = len(topicSplit)

    topicSplit.extend([' '] * (maxlen - len(topicSplit)))

    payload = colorString(changeString(str(msg.payload.decode("utf-8"))))

    topicSplit.append(payload)

    topicDict[msg.topic] = [ts] + [data] + [
        colorString(changeString(s)) for s in topicSplit
    ]

    # final calculations on Pandas DataFrame
    toDisplayDf = pd.DataFrame.from_dict(topicDict, orient='index')
    toDisplayDf.insert(1, "ago", 0)
    toDisplayDf["ago"] = toDisplayDf[0].apply(pretty_date)
    toDisplayDf = toDisplayDf.drop([0, 1], axis=1)

    toDisplayDf = toDisplayDf.sort_index()  # .drop([1], axis=1)

    toDisplay = tabulate(toDisplayDf)
    cls()

    displayStatus()

    gotoxy(0, 3)
    print(toDisplay)



def displayStatus():
    gotoxy(0, 0)
    print(
        "Now is: {:%Y-%m-%d %H:%M:%S}\t Last update: {}\tMessages received: {} | Connected to: {}:{}".
        format(datetime.now(), pretty_date(ts), messages, host, port))


def changeString(string):

    if string in wordDict:
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

    optional_arguments.add_argument('--conf',
                                    help='config file',
                                    dest="configFile",
                                    default='')

    optional_arguments.add_argument('--test',
                                    help='perform tests',
                                    dest="performTest",
                                    action='store_true')

    return parser.parse_args()


if __name__ == "__main__":

    ts = datetime.now().timestamp()

    #
    #  ---------------------------------- arguments ------------------------- #
    #

    args = parseArguments()
    configFile = args.configFile
    performTest = args.performTest


    #
    #  ---------------------------------- CONFIG ------------------------- #
    #

    if configFile == "":
        # config file path not provided
        configFile = path.join(path.dirname(__file__), 'mqtt_monitor.conf')

    print("configFile", configFile)
    config = ConfigParser()

    try:
        config.read_file(open(configFile, "r"))
    except:
        print("Can't find config file in %s" % (configFile))
        exit(2)

    host = config['server']['host']
    port = int(config['server']['port'])
    username = config['server']['username']
    password = config['server']['password']
    usessl = config['server']['usessl']

    topics = [x.strip() for x in config['topics']['topics'].split(',')]
    print(topics)

    wordDict = config._sections['tunables']
    print(wordDict)
    colorDict = {}
    for key in config._sections['coloring']:
        colorDict[eval(key)] = eval(config._sections['coloring'][key])

    #
    #  ---------------------------------- MAIN ------------------------- #
    #

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
    print("Press Ctrl+C")

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.

    # client.loop_forever()

    client.loop_start()

    continueLoop = True
    while continueLoop:
        displayStatus()

        # check if we are in a test mode:
        if performTest:
            # if received at least 3 messages or it took longer than 30 seconds
            if messages > 4 or (datetime.now().timestamp() - ts > 30):
                print (colors.fg.green + "Test passed!" + colors.reset)
                exit(0)

        sleep(1)
