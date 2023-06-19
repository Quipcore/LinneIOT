# boot.py -- run on boot-up
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
from machine import Pin, reset, ADC
import dht11 as dht

ssid = 'lido'
password = 'Theyokertma'


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def open_socket(ip):
    # Open a socket
    port = 80
    address = (ip, port)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print(f'Port: {port}, Connection: {connection}')
    return connection

def webpage(temperature, state, sensor_temperature):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form action="./temp">
            <input type="submit" value="Get sensor temp" />
            </form>
            <p>LED is {state}</p>
            <p>Board temperature is {temperature}</p>
            <p>Sensor temperture is {sensor_temperature}</p>
            </body>
            </html>
            """
    return str(html)

def read_temp(temperature_sensor):
    return temperature_sensor.temperature()

    
def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    board_temp = 0
    sensor_temp = 0.0
    temp_sensor = dht.DHT11(Pin(27)) 

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        board_temp = pico_temp_sensor.temp

        sensor_temp = temp_sensor.temperature

        html = webpage(board_temp, state, sensor_temp)
        print(html)
        client.send(html)
        client.close()

try:
    print("\nBooting\n\n")
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
    
except KeyboardInterrupt:
    reset()