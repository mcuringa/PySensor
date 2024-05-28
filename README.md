# PySensor
CircuitPython client code for QT Py that logs sensor data to a firebase cloud server.

`circuit`
=================
[CircuitPython](https://learn.adafruit.com/welcome-to-circuitpython/what-is-circuitpython) code is
in the `circuit` directory. This folder contains examples and functions to make it easier
to read and log sensor data for the [QT Py ESP32-S2 WiFi Dev Board](https://www.adafruit.com/product/5325).

You can quickly get started using the [Mu Editor](https://codewith.mu/). These programs have
also been written and tested with [VS Code](https://code.visualstudio.com/) and the
[Adafruit CircuitPython](https://learn.adafruit.com/adafruit-circuitpython-ide-setup) extension.

required libraries
------------------
The `lib` directory contains all of the [adafruit libraries](https://circuitpython.org/libraries) required
to run the example code. You can copy the entire `lib` directory to the `CIRCUITPY` drive on your QT Py.

configuration
-------------
The `config.py` file contains the configuration settings for the QT Py.
You can change the following settings:

**Core Settings**

_see `config-example.py` for an example configuration file_

**Sensor settings**

Some sensors require calibration and configuration based
on your location. The config contains default settings, but you
may need to modify them for better results.


serial connection
-----------------
On Linux, you can view the serial output with the following command:

```bash
screen /dev/ttyACM0 115200
```

Where `/dev/ttyACM0` is the serial port for the QT Py. You can find the serial port by running
`ls /dev/tty*` before and after plugging in the QT Py.

firebase `functions`
====================

The `functions` directory contains the [Firebase Cloud Functions](https://firebase.google.com/docs/functions)
code that create a "serverless" REST API to log sensor data. The rest API has two endpoints:

- `POST /log` - Log sensor data
- `GET /log` - Retrieve sensor data

The GET request returns the log data for a specific user in .csv format.

Authentication
--------------
The server uses a simple authentication scheme. Each request **must** contain a `secret`
and a matching `username`

Keys can be generated using the python `secrets` module:

```python
import secrets
# create 10 keys of 32 characters each
for i in Range(40):
    print(secrets.token_urlsafe(32))
```

Each use **must** maintain the secret key in a secure location. It should not be shared.
Each user has a secure URL to download their data. For example:

`https://<firebaseurl>?username=<foo>&secret=5ahItOm6TEYAhtE5D5OAlw`