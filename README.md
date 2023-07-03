# Tutorial on how to build a temperature and humidity sensor
Felix Lidö - fl223gf
"Short project overview"
Time: 1-2 hours

## Objective


## Material
#####  Materials required for build:
| Material | Price (sek) | Link |
|:------ |:-----------: | :-------:|
| Rasberry Pi Pico WH| 109 | [Electrokit](https://www.electrokit.com/produkt/raspberry-pi-pico-wh/)|
| DHT11 Sensor| 49 | [Electrokit](https://www.electrokit.com/produkt/digital-temperatur-och-fuktsensor-dht11/) |
| Jumper wire | 29|[Electrokit](https://www.electrokit.com/produkt/labbsladd-20-pin-15cm-hane-hane/)|
|220 $\Omega$ Resistor|3|[Electrokit](https://www.electrokit.com/en/product/resistor-1w-5-220ohm-220r/)|



##### Extra material used for debugging: 
| Material | Price (sek) | Link |
|:------ |:-----------: | :-------:|
|Push button PCB 0.8 mm black|5.50|[Electrokit](https://www.electrokit.com/en/product/push-button-pcb-0-8-mm-black/)|



## Computer setup

## Putting everything together

## Platfrom

## The code
```python
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
