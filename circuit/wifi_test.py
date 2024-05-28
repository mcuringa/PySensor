import os
import board
import busio
import digitalio
import adafruit_requests as requests
import wifi
import socketpool
import ssl

import config

# Get WiFi details
ssid = config.ssid
password = config.wifi_password

print("Connecting to Wi-Fi...")
wifi.radio.connect(ssid, password)
print("Connected to", ssid)

# Initialize a requests session
pool = socketpool.SocketPool(wifi.radio)
requests = requests.Session(pool, ssl.create_default_context())

TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_GET_URL = "https://httpbin.org/get"
JSON_POST_URL = "https://httpbin.org/post"

print(f"Fetching text from {TEXT_URL}")

with requests.get(TEXT_URL) as response:
    print("-" * 40)
    print("Text Response: ", response.text)
    print("-" * 40)

print(f"Fetching JSON data from {JSON_GET_URL}")
with requests.get(JSON_GET_URL) as response:
    print("-" * 40)
    print("JSON Response: ", response.json())
    print("-" * 40)

data = "31F"

print(f"POSTing data to {JSON_POST_URL}: {data}")
with requests.post(JSON_POST_URL, data=data) as response:
    print("-" * 40)
    json_resp = response.json()

    # Parse out the 'data' key from json_resp dict.
    print("Data received from server:", json_resp["data"])
    print("-" * 40)

json_data = {"Date": "July 25, 2019"}

print(f"POSTing data to {JSON_POST_URL}: {json_data}")
with requests.post(JSON_POST_URL, json=json_data) as response:
    print("-" * 40)

    json_resp = response.json()
    # Parse out the 'json' key from json_resp dict.
    print("JSON Data received from server:", json_resp["json"])
    print("-" * 40)
