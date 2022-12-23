from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from bme_module import BME280Module

I2C_ID = 0
SCL_PIN = 1
SDA_PIN = 0

app = Microdot()
Response.default_content_type = "text/html"

bme_module = BME280Module(I2C_ID,SCL_PIN,SDA_PIN)

# index.html root route
@app.route("/")
async def index(request):
    return render_template("index.html")

# Read sensor readings and return as JSON
@app.route("/sensorReadings")
async def get_sensor_readings(request):
    temperature, pressure, humidity, altitude = bme_module.get_sensor_readings()
    sensor_readings = {"status": "OK", "temperature": temperature, "pressure": pressure, "humidity": humidity, "altitude": altitude}
    return sensor_readings

# Shutdown the application
@app.route("/shutdown")
async def shutdown(request):
    request.app.shutdown()
    return "The server is shutting down..."

# Static CSS/JSS
@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)


if __name__ == "__main__":
    try:
        app.run()
    except KeyboardInterrupt:
        pass
