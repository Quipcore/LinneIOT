import network
import urequests as requests
from time import sleep_ms, sleep
import dht11 as dht
from machine import Pin


TOKEN = "" #Put your TOKEN here
DEVICE_LABEL = "picowboard" # Assign the device label desire to be send
TEMP_LABEL = "temp" # Assign the temperature label desire to be send
HUMIDITY_LABEL = "humidity" # Assign the humidity label desire to be send
WIFI_SSID = "" # Assign your the SSID of your network
WIFI_PASS = "" # Assign your the password of your network
DELAY = 5  # Delay in seconds
LED_PIN = Pin("LED", Pin.OUT)


# Builds the json to send the request
def build_json(temp_value, humidity_value):
    try:
        data = {TEMP_LABEL: {"value": temp_value}, HUMIDITY_LABEL: {"value": humidity_value}}
        return data
    except:
        return None

# Sending data to Ubidots Restful Webserice
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

#Connect to WIFI
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

#Toggle the LED pin n amount times
def warning_LED(amount):
    for i in range(amount):   
        LED_PIN.on()
        sleep_ms(500)
        LED_PIN.off()
        sleep_ms(500)

def main():
    connect()
    bad_value = -10000
    while check_status_pin():
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
            
        sleep_ms(DELAY*1000)
        
def check_status_pin():
    status_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)
    print(status_pin.value())
    return status_pin.value() != 1
      
while check_status_pin():  
    main()
warning_LED(10)
LED_PIN.off()
