# Tutorial on how to build a temperature and humidity sensor
Felix Lidö - fl223gf

The objective of this project is to measure temprature and humitdity from a sensor. The data is then sent to ubidots for analaysis

**Time**: around one hour

## Objective
The objective of this project is to measure temprature and humitdity from a sensor. The data is then sent to ubidots for analaysis

## Material
#####  Materials required for build:
| Material | Price (sek) | Link |
|:------ |:-----------: | :-------:|
| Rasberry Pi Pico WH| 109 | [Electrokit](https://www.electrokit.com/produkt/raspberry-pi-pico-wh/)|
| DHT11 Sensor| 49 | [Electrokit](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/) |
| Jumper wire | 29|[Electrokit](https://www.electrokit.com/produkt/labbsladd-20-pin-15cm-hane-hane/)|
|220 $\Omega$ Resistor|3|[Electrokit](https://www.electrokit.com/en/product/resistor-1w-5-220ohm-220r/)|

 - Raspberry Pi Pico WH
 - DHT11 Sensor
 - Jumper wire
 - Resistor

##### Extra material used for debugging: 
| Material | Price (sek) | Link |
|:------ |:-----------: | :-------:|
|Push button PCB 0.8 mm black|5.50|[Electrokit](https://www.electrokit.com/en/product/push-button-pcb-0-8-mm-black/)|

- Push button PCB 

## Computer setup

VScode with the pymakr plugin and NodeJS 
pyCharm with Micropython
Thonny

## Putting everything together

![Curcit Diagram](https://github.com/Quipcore/LinneIOT/blob/main/iot.png?raw=true)

## Platfrom

## The code
``` python
from machine import Pin, reset, ADC
#ubidots api
API_KEY =""
TOKEN = "" #Put here your TOKEN
DEVICE_LABEL = "picowboard" # Assign the device label desire to be send
VARIABLE_LABEL = "sensor"  # Assign the variable label desire to be send
TEMP_LABEL = "temp"
HUMIDITY_LABEL = "humidity"
WIFI_SSID = "" # Assign your the SSID of your network
WIFI_PASS = "" # Assign your the password of your network
DELAY = 5  # Delay in seconds
LED_PIN = Pin("LED", Pin.OUT)
```


```python
import dht11 as dht
def main():
    connect()
    bad_value = -10000
    run = True
    while run:
        LED_PIN.on()
        dht11_sensor = dht.DHT11(Pin(27))
        temp = bad_value
        humidity = bad_value
        try:
            temp = dht11_sensor.temperature
            humidity = dht11_sensor.humidity
        except:
            pass
        
        if temp != bad_value and humidity != bad_value:
            returnValue = sendData(DEVICE_LABEL, temp, humidity)
        else:
            print("Failed to get signal")
            LED_PIN.off()
            
        run = check_status_pin()
        sleep_ms(DELAY*1000)
```
```python
def connect():
    wlan = network.WLAN(network.STA_IF)         # Put modem on Station mode
    if not wlan.isconnected():                  # Check if already connected
        print('connecting to network...')
        wlan.active(True)                       # Activate network interface
        # set power mode to get WiFi power-saving off (if needed)
        wlan.config(pm = 0xa11140)
        wlan.connect(WIFI_SSID, WIFI_PASS)  # Your WiFi Credential
        print('Waiting for connection...', end='')
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    # Print the IP assigned by router
    ip = wlan.ifconfig()[0]
    print('\nConnected on {}'.format(ip))
    return ip
```

```python
# Sending data to Ubidots Restful Webserice
import network
import urequests as requests

def sendData(device, temp_value, humidity_value):
    try:
        url = "https://industrial.api.ubidots.com/"
        url = url + "api/v1.6/devices/" + device
        headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}
        data = build_json(temp_value, humidity_value)
        if data is not None:
            print(data)
            req = requests.post(url=url, headers=headers, json=data)
            return req.json()
        else:
           pass
    except:
        pass
```
```py
# Builds the json to send the request
def build_json(temp_value, humidity_value):
    try:
        data = {TEMP_LABEL: {"value": temp_value}, HUMIDITY_LABEL: {"value": humidity_value}}
        return data
    except:
        return None
```

## Transmitting the data/Connectivity

## Presenting the data

## Finalizing the design
