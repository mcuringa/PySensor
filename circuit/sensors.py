#  PySensor by matthew x. curinga is marked with CC0 1.0 Universal.
#  To view a copy of this license, visit https://creativecommons.org/publicdomain/zero/1.0/

"""
`sensors.py` prints out sensor data from the VEML7700 and BME680 sensors.
The VEML7700 sensor measures ambient light and lux, while the BME680 sensor
measures temperature, gas, humidity, pressure, and altitude.

Ambient light is measured in lux, which is a unit of illuminance. The lux
value is calculated from the ambient light value. The gas value is the
resistance of the gas sensor in ohms. The temperature is measured in Celsius,
the humidity in percent, the pressure in hectopascals, and the altitude in
meters.

"""
import time
import board
import adafruit_veml7700
import adafruit_bme680
from adafruit_datetime import datetime

import config


def log_lux(lux):
    print("""
Lux sensor data:
----------------""")
    print("Ambient light:", lux.light)
    print("Lux:", lux.lux)


def log_gas(gas):
    print("""
Gas sensor data:
----------------""")
    print(f"Temperature: {gas.temperature + config.temperature_offset:.1f} C")
    print(f"Gas: {gas.gas} ohm")
    print(f"Humidity: {gas.relative_humidity:.1f} %")
    print(f"Pressure: {gas.pressure:.3f} hPa")
    print(f"Altitude: {gas.altitude:.2f} meters")


# Initialize I2C bus
i2c = board.STEMMA_I2C()


lux = adafruit_veml7700.VEML7700(i2c)
gas = adafruit_bme680.Adafruit_BME680_I2C(i2c)
gas.sea_level_pressure = config.sea_level_pressure

while True:

    print("config.sea_level_pressure", config.sea_level_pressure)
    print(f"""
==========================================================
{datetime.now()}
==========================================================""")
    log_lux(lux)
    log_gas(gas)
    time.sleep(10)
