#!/bin/bash

publish() {
  topic="$1"
  message="$2"
  mosquitto_pub -h test.mosquitto.org -p 1883 -u "rw" -P "readwrite" -t "$topic" -m "$message"
}


publish slxlfippowa/mqtt-monitor/pi/uptime "$(uptime)"

publish x8gwiazd/mqtt-monitor/url https://github.com/filipsPL/mqtt-monitor
publish x8gwiazd/mqtt-monitor/sensor1 offline
publish jl2u90nbvcj/mqtt-monitor/status ready

sleep 5s

publish x8gwiazd/mqtt-monitor/sensor1 ready

sleep 2s
publish slxlfippowa/mqtt-monitor/sensor2 ready

sleep 3s
publish x8gwiazd/mqtt-monitor/sensor1/temp $((20 + $RANDOM % 30))
publish x8gwiazd/mqtt-monitor/sensor1/hum $((20 + $RANDOM % 30))
publish x8gwiazd/mqtt-monitor/sensor1/p 998.32

sleep 1s
publish x8gwiazd/mqtt-monitor/sensor2/temp $((20 + $RANDOM % 30))
publish x8gwiazd/mqtt-monitor/sensor2/hum $((20 + $RANDOM % 80))
publish x8gwiazd/mqtt-monitor/sensor2/p 999.32

sleep 2s
publish x8gwiazd/mqtt-monitor/pi/uptime "$(uptime)"
publish x8gwiazd/mqtt-monitor/pi/date "$(date)"
sleep 1s
publish x8gwiazd/mqtt-monitor/pi/temp/cpu $((20 + $RANDOM % 50))
publish x8gwiazd/mqtt-monitor/pi/temp/ssd $((20 + $RANDOM % 30))

sleep 1s
publish x8gwiazd/mqtt-monitor/pi/temp/in 21
publish x8gwiazd/mqtt-monitor/pi/temp/out 17
publish x8gwiazd/mqtt-monitor/pi/rssi/wifi1 -67
publish x8gwiazd/mqtt-monitor/pi/rssi/wifi2 -37

sleep 1s
publish x8gwiazd/mqtt-monitor/sensor1 offline
publish x8gwiazd/mqtt-monitor/pi/temp/system $((20 + $RANDOM % 30))
publish x8gwiazd/mqtt-monitor/pi/temp/storage $((20 + $RANDOM % 30))
