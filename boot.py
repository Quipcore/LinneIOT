import network
import urequests as requests
import machine
from time import sleep_ms, sleep
import random
import dht11 as dht
from machine import Pin, reset, ADC

#ubidots api
API_KEY ="BBFF-34747d2a506900eadbd08b595c17b63d422"
TOKEN = "BBFF-PV8MTDyv4z5lLYHLOZBM6vYt4XucqG" #Put here your TOKEN
DEVICE_LABEL = "picowboard" # Assign the device label desire to be send
VARIABLE_LABEL = "sensor"  # Assign the variable label desire to be send
TEMP_LABEL = "temp"
HUMIDITY_LABEL = "humidity"
WIFI_SSID = "lido" # Assign your the SSID of your network
WIFI_PASS = "Theyokertma" # Assign your the password of your network
DELAY = 5  # Delay in seconds
LED_PIN = Pin("LED", Pin.OUT)


# Builds the json to send the request
def build_json(temp_value, humidity_value):
    try:
        data = {TEMP_LABEL: {"value": temp_value}, HUMIDITY_LABEL: {"value": humidity_value}}
        return data
    except:
        return None

# Random number generator
def random_integer(upper_bound):
    return random.getrandbits(32) % upper_bound

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

def warning_LED(amount):
    for i in range(amount):   
        LED_PIN.on()
        sleep_ms(500)
        LED_PIN.off()
        sleep_ms(500)

def boot_lights():
    warning_LED(10)

#boot_lights()
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
        
def check_status_pin():
    status_pin = Pin(15, Pin.IN, Pin.PULL_DOWN)
    print(status_pin.value())
    return status_pin.value() != 1
      
run_program = check_status_pin()  
while run_program:  
    main()
    run_program = check_status_pin()
warning_LED(10)
LED_PIN.off()