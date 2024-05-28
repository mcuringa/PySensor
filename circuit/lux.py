import time
import board
import busio
import adafruit_veml7700

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize the VEML7700 sensor
sensor = adafruit_veml7700.VEML7700(i2c)

# Print sensor data
while True:
    print("Ambient light:", sensor.light)
    print("Lux:", sensor.lux)
    time.sleep(1)
