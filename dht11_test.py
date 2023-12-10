# Complete project details at https://RandomNerdTutorials.com/raspberry-pi-pico-dht11-dht22-micropython/

from machine import Pin
from time import sleep
import dht 


def measure_temp():

    sensor = dht.DHT11(Pin(22))
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        return temp, temp_f, hum

    except OSError as e:
        print('Failed to read sensor.')
        return 0,0,0
        
