console mqtt_monitor
======================


<!-- TOC START min:1 max:6 link:true asterisk:false update:true -->
- [About](#about)
- [Installation](#installation)
    - [Conda python environment](#conda-python-environment)
    - [Set up with pip](#set-up-with-pip)
- [Usage](#usage)
  - [Test server](#test-server)
  - [Set up your own config](#set-up-your-own-config)
- [Screencast](#screencast)
<!-- TOC END -->


# About

This is a simple console mqtt topic monitor written in python 3. It allows you to subscribe and listen to a number of mqtt topics and display it in a form of table. Optionally it adds some eye-candies and colors to the presented data.

![](obrazki/README-1de557a3.png)

It was tested (with GitHub Actions CI/CD) and works under:
- OS: Ubuntu, MacOS, and Windows
- Python versions: 3.5, 3.8, and 3.9


CI Status: [![Python application](https://github.com/filipsPL/mqtt-monitor/actions/workflows/python-app.yml/badge.svg)](https://github.com/filipsPL/mqtt-monitor/actions/workflows/python-app.yml)



# Installation

`git clone git@github.com:filipsPL/mqtt-monitor.git`

### Conda python environment

```
conda env create -f conda.yml
conda activate mqttmonitor
```

### Set up with pip

`pip install -r requirements.txt`

# Usage

## Test server

Connect to the test server and wait for messages:

`./mqtt_monitor.py --conf mqtt_monitor.conf.sample`

## Set up your own config

- create a conf file from template `cp mqtt_monitor.conf.sample mqtt_monitor.conf`
- edit `mqtt_monitor.conf`
- run `./mqtt_monitor.py --conf mqtt_monitor.conf`
- enjoy


# Screencast

See the monitor in action:

[![asciicast](https://asciinema.org/a/emHhmWkkbyLIGC8CpPD7xwZBu.svg)](https://asciinema.org/a/emHhmWkkbyLIGC8CpPD7xwZBu)
