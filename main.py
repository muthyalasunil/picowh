import network
import socket
import time
from picozero import pico_temp_sensor, pico_led
import machine
import dht11_test
import ubinascii

from machine import Pin
import uasyncio as asyncio

led = Pin(15, Pin.OUT)
onboard = Pin("LED", Pin.OUT, value=0)

ssid = 'Raspiwifi'
password = 'raspiwifi23'

ip_address = ''
mac_address = ''

def webpage(mac, pico_temp, temp, temp_f, humid):
    #Template HTML
    
    html = "dht11_humid; "+str(humid) +", macid; "+str(mac)+", dht11_temp; "+str(temp)+", pico_temp; "+str(pico_temp)
    return str(html)


def connect_to_network():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        onboard.off()
        time.sleep(2)
        onboard.on()
        time.sleep(2)

    ip = wlan.ifconfig()[0]
    mac = ubinascii.hexlify(wlan.config('mac'),':').decode()

    return wlan, ip, mac

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    
    # We are not interested in HTTP request headers,
    while await reader.readline() != b"\r\n":
        pass

    request = str(request_line)
    response = request
    #led_off = request.find('/light/off')
    #print( 'led on = ' + str(led_on))
    #print( 'led off = ' + str(led_off))
    if request.find('/lighton') > -1:
        onboard.on()
        response = 'lighton'
    elif request.find('/lightoff') > -1:
        onboard.off()
        response = 'lightoff'
    elif request.find('/temperature') > -1:

        pico_temp = pico_temp_sensor.temp
        temp, temp_f, humid = dht11_test.measure_temp()
        wlan = network.WLAN(network.STA_IF)
        mac = ubinascii.hexlify(wlan.config('mac'),':').decode()

        print('------------------------')
        print('Temperature: %3.1f C' %temp)
        print('Temperature: %3.1f F' %temp_f)
        print('Humidity: %3.1f %%' %humid)
        
        response = webpage(mac, pico_temp, temp, temp_f, humid)
        
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    print('Connecting to Network...')
    wlan, ip_address, mac_address = connect_to_network()
    print('ip = ' + ip_address)
    print('mac = ' + mac_address)

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        onboard.on()
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)

        
try:
    asyncio.run(main())
except KeyboardInterrupt:
    machine.reset()
finally:
    asyncio.new_event_loop()
    
    

