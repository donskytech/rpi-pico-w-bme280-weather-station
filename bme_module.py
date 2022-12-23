import machine
import bme280
import math

class BME280Module:
    SEA_LEVEL_PRESSURE_HPA = 1013.25
    def __init__(self, id, scl_pin, sda_pin):
        self.i2c = machine.I2C(id=id, scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=400000)
        self.bme = bme280.BME280(i2c=self.i2c)
        
    def get_sensor_readings(self):
        (temperature, pressure, humidity) = self.bme.values
        temperature_val = float(temperature[:len(temperature) - 1])
        humidity_val = float(humidity[:len(humidity) - 1])
        pressure_val = float(pressure[:len(pressure) - 3])

        # Altitude calculation
        altitude_val = 44330 * (1.0 - math.pow(pressure_val / BME280Module.SEA_LEVEL_PRESSURE_HPA, 0.1903))
        
        return (temperature_val, pressure_val, humidity_val, altitude_val)
    