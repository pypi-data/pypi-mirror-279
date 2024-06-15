"""
  espFOTA.py
  
  espFOTA, a library for the ESP8266/Arduino platform
  for managing Over-The-Air updates for IoT devices
  
  @author Creator Raghul Raj G
  @version 1.0-gr2.1
  @license GNU General Public License v3 (GPLv3)
""" 
import time
import machine
import network
import urequests
import os

class espFOTA:
    def __init__(self, ssid, password, server):
        self.ssid = ssid
        self.password = password
        self.server = server
        
        self.status_LED= machine.Pin(2, machine.Pin.OUT)
        self.status_LED.value(1)

        self.Netconnect()

    def Netconnect(self):
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        if(not(self.wifi.isconnected())):
            self.wifi.disconnect()
            self.wifi.connect(self.ssid, self.password)
        while(not(self.wifi.isconnected())):
            print("Wifi not connected\nReconnecting")
            try:
                self.wifi.connect(self.ssid, self.password)
            except OSError as e:
                print(e)
            time.sleep(1)
            if self.wifi.isconnected():
                self.status_LED.value(0)
                print('WiFi Connected')
                break

    def reconnect(self):
        print("Can't connect")
        time.sleep(5)
        machine.reset() 

    def callback(self):
        response = urequests.get(self.server, stream=True)
        if response.status_code == 200:
            total_size = int(response.headers.get('Content-Length', 0))       
            downloaded_size = 0
            chunk_size = 1024
            try:
                with open("main.py", 'w') as f:
                    while True:
                        chunk = response.raw.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        # Calculate and print the progress percentage
                        progress = (downloaded_size / total_size) * 100
                        print(f"Download progress: {progress:.2f}%")
                    
            finally:
                response.close()
            #restart ESP
            machine.reset()

    def run(self):
        try:
            self.callback()
        except OSError as e:
            self.reconnect()

