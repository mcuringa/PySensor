"""
Connect to the lux and environmental sensors and log data to
the firebase server.
"""
import time
import adafruit_veml7700
import adafruit_bme680
from adafruit_datetime import datetime
import wifi
import socketpool
import ssl

import board
import adafruit_requests as requests


import config

conn = None


def connect_wifi():
    print("connecting to wifi...", config.ssid)
    global conn
    if conn:
        return conn

    wifi.radio.connect(config.ssid, config.wifi_password)

    # Initialize a requests session
    pool = socketpool.SocketPool(wifi.radio)
    conn = requests.Session(pool, ssl.create_default_context())
    print("Wifi connected")
    return conn


def log_lux(requests, lux):
    data = {
        "username": config.logger_user,
        "secret": config.logger_secret,
        "ambient_light": lux.light,
        "lux": lux.lux,
    }

    print(f"""Logging lux data:
          {data}""")

    if not requests:
        print("no wifi connection")
        return

    with requests.post(config.logger_url, data=data) as response:
        print("-" * 40)
        print("response code:", response.status_code)
        print("-" * 40)


def log_gas(gas):
    print("""
Gas sensor data:
----------------""")
    print(f"Temperature: {gas.temperature + config.temperature_offset:.1f} C")
    print(f"Gas: {gas.gas} ohm")
    print(f"Humidity: {gas.relative_humidity:.1f} %")
    print(f"Pressure: {gas.pressure:.3f} hPa")
    print(f"Altitude: {gas.altitude:.2f} meters")


def init_sensor():
    i2c = board.STEMMA_I2C()
    lux = adafruit_veml7700.VEML7700(i2c)
    gas = adafruit_bme680.Adafruit_BME680_I2C(i2c)
    gas.sea_level_pressure = config.sea_level_pressure
    return lux, gas


lux, gas = init_sensor()

while True:
    conn = connect_wifi()
    log_lux(conn, lux)
    # log_gas(gas)
    time.sleep(config.log_timeout)
