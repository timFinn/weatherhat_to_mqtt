# Kevin McAleer 
# 18 February 2022
# This enables data from the Pimoroni WeatherHat to be sent to a local MQTT server

# Timothy Finnegan
# 23 June 2024
# This iteration includes specific constants for my configuration
#   and removes the timestamp

import weatherhat
import paho.mqtt.client as mqtt
from time import sleep
from datetime import datetime 
from gpiozero import CPUTemperature

mqtt_server = '10.0.0.240' # Replace with the IP or URI of the MQTT server you use
client_id = "weatherhat"

update_frequency_in_seconds = 1

sensor = weatherhat.WeatherHAT()

cpu = CPUTemperature()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("$SYS/#")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client(client_id=client_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(host=mqtt_server)

cputemp_topic = "sensors/pi/cpu_temp"
temp_topic = "sensors/weather/temperature"
humidity_topic = "sensors/weather/humidity"
rel_hum_topic = "sensors/weather/relative_humidity"
pressure_topic = "sensors/weather/pressure"
dewpoint_topic = "sensors/weather/dewpoint"
light_topic = "sensors/weather/light"
wind_dir_topic = "sensors/weather/wind_direction"
wind_spd_topic = "sensors/weather/wind_speed"
rain_topic = "sensors/weather/rain"
rain_total_topic = "sensors/weather/rain_total"

import socket

# Wait until the network is and host name resolution is available:

def hostAvail(hostname):
    try:
        socket.gethostbyname(hostname)
        return True
    except socket.error:
        return False
    return False

while not hostAvail("broker.local"):
    print("Waiting for dbserver")
    sleep(2)

# Continue with code here...

def sendPayload(topic, data):
    payload = f"{{topic}:{data}}"
    client.publish(topic=topic, payload=payload, qos=0, retain=False)
    print(f"sending {payload} to server")

while True:

    # update the sensor readings
    sensor.update(interval=1.0)
    
    # sleep for update frequency second 
    sleep(update_frequency_in_seconds)


    sendPayload(cputemp_topic, cpu.temperature)
    sendPayload(temp_topic, sensor.temperature)
    sendPayload(humidity_topic, sensor.humidity)
    sendPayload(rel_hum_topic, sensor.relative_humidity)
    sendPayload(pressure_topic, sensor.pressure)
    sendPayload(dewpoint_topic, sensor.dewpoint)
    sendPayload(light_topic, sensor.lux)
    sendPayload(wind_dir_topic, sensor.wind_direction)
    sendPayload(wind_spd_topic, sensor.wind_speed)
    sendPayload(rain_topic, sensor.rain)
    sendPayload(rain_total_topic, sensor.rain_total)
