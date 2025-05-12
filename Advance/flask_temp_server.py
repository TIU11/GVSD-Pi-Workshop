# For Phidget version
from flask import Flask
from time import strftime
from gpiozero import LED, Buzzer
from Phidget22.Phidget import *
from Phidget22.Devices.TemperatureSensor import *

# OR for DS18B20 version (comment out Phidget imports above)
# from flask import Flask
# import os
# import glob
# from time import strftime
# from gpiozero import LED, Buzzer
#Setup
# Version 1: Using Phidget Temperature Sensor
app = Flask(__name__)

# Optional components setup
led = LED(18)       # Status LED
buzzer = Buzzer(5)  # Alert buzzer

# Function to read temperature from Phidget
def get_temp_phidget():
    """Read temperature from Phidget sensor"""
    # Create temperature sensor object
    temp_sensor = TemperatureSensor()
    
    # Open connection and wait for sensor
    temp_sensor.openWaitForAttachment(2000)
    
    # Read temperature
    temperature_c = temp_sensor.getTemperature()
    
    # Convert to Fahrenheit
    temperature_f = (temperature_c * 9/5) + 32
    
    # Close connection
    temp_sensor.close()
    
    return temperature_c, temperature_f
#Functions
# OR Version 2: Using DS18B20 Temperature Sensor
def setup_ds18b20():
    """Initialize DS18B20 sensor"""
    # Enable 1-Wire interface (run once at startup)
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    # Find the sensor device
    base_dir = '/sys/bus/w1/devices/'
    device_folders = glob.glob(base_dir + '28*')
    
    if device_folders:
        device_file = device_folders[0] + '/w1_slave'
        return device_file
    else:
        return None

def get_temp_ds18b20(device_file):
    """Read temperature from DS18B20 sensor"""
    if not device_file:
        return None, None
    
    # Read raw temperature data
    with open(device_file, 'r') as f:
        lines = f.readlines()
    
    # Check if reading is valid
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        with open(device_file, 'r') as f:
            lines = f.readlines()
    
    # Extract temperature value
    temp_line = lines[1]
    temp_pos = temp_line.find('t=')
    
    if temp_pos != -1:
        temp_string = temp_line[temp_pos+2:]
        temperature_c = float(temp_string) / 1000.0
        temperature_f = (temperature_c * 9/5) + 32
        return temperature_c, temperature_f
    
    return None, None
# Main Loop
# Create web page
@app.route('/')
def index():
    """Main web page that shows temperature"""
    
    # Get current time
    current_time = strftime("%Y-%m-%d %H:%M:%S")
    
    # CHOOSE ONE: Get temperature from either Phidget or DS18B20
    
    # Option 1: Using Phidget sensor
    try:
        temp_c, temp_f = get_temp_phidget()
        sensor_type = "Phidget"
        error_message = None
        
        # Alert if temperature is too high
        if temp_f > 80:
            led.on()
            buzzer.beep(0.5, 0.5, 3)
        else:
            led.off()
            buzzer.off()
            
    except Exception as e:
        temp_c, temp_f = 0, 0
        sensor_type = "Phidget"
        error_message = f"Error: {str(e)}"
    
    # # Option 2: Using DS18B20 sensor (uncomment to use)
    # device_file = setup_ds18b20()
    # temp_c, temp_f = get_temp_ds18b20(device_file)
    # sensor_type = "DS18B20"
    # error_message = None if temp_c else "Error reading sensor"
    
    # Create HTML page with inline styling using TIU brand colors
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Raspberry Pi Temperature Monitor</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta http-equiv="refresh" content="5">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap');
            
            body {{
                font-family: 'DM Sans', sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f4f1eb;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            .header {{
                background: linear-gradient(to right, #830000, #a04040);
                color: white;
                padding: 15px;
                margin: -30px -30px 20px -30px;
                border-radius: 10px 10px 0 0;
            }}
            .temp-display {{
                font-size: 48px;
                margin: 20px 0;
                color: #333;
            }}
            .temp-f {{
                color: #830000;
            }}
            .temp-c {{
                color: #193854;
            }}
            .info {{
                color: #666;
                margin: 10px 0;
            }}
            .led-controls {{
                margin-top: 30px;
            }}
            button {{
                padding: 10px 20px;
                font-size: 16px;
                margin: 0 10px;
                cursor: pointer;
                background-color: #748E54;
                color: white;
                border: none;
                border-radius: 5px;
            }}
            button:hover {{
                background-color: #5d7243;
            }}
            .footer {{
                margin-top: 30px;
                font-size: 12px;
                color: #8e8271;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Temperature Monitor</h1>
                <p>Using {sensor_type} Sensor</p>
            </div>
            
            {"<div class='temp-display'>" if not error_message else ""}
            {"<span class='temp-f'>" + f"{temp_f:.1f}°F" + "</span>" if not error_message else ""}
            {" | " if not error_message else ""}
            {"<span class='temp-c'>" + f"{temp_c:.1f}°C" + "</span>" if not error_message else ""}
            {"</div>" if not error_message else ""}
            
            {"<p class='info' style='color: red;'>" + error_message + "</p>" if error_message else ""}
            
            <p class="info">Last updated: {current_time}</p>
            
            <div class="led-controls">
                <h3>LED Control</h3>
                <form method="post" action="/led/on" style="display: inline;">
                    <button type="submit">LED ON</button>
                </form>
                <form method="post" action="/led/off" style="display: inline;">
                    <button type="submit">LED OFF</button>
                </form>
            </div>
            
            <p class="info" style="margin-top: 30px;">
                Page refreshes every 5 seconds
            </p>
            
            <div class="footer">
                TIU STEM Workshop - Raspberry Pi & Phidgets
            </div>
        </div>
    </body>
    </html>
    '''
    
    return html

# LED control routes
@app.route('/led/on', methods=['POST'])
def led_on():
    """Turn LED on"""
    led.on()
    return index()  # Return to main page

@app.route('/led/off', methods=['POST'])
def led_off():
    """Turn LED off"""
    led.off()
    buzzer.off()  # Also silence the buzzer
    return index()  # Return to main page

# Run the web server
if __name__ == '__main__':
    print("Starting Flask server...")
    print("Access the web page at: http://[YOUR_PI_IP]:5000")
    print("Press Ctrl+C to stop the server")
    app.run(host='0.0.0.0', port=5000, debug=True)
#OR
#Test Your Sensor First
# Test Phidget sensor --- Rest can be commented. 
def test_phidget():
    from Phidget22.Phidget import *
    from Phidget22.Devices.TemperatureSensor import *
    
    temp_sensor = TemperatureSensor()
    temp_sensor.openWaitForAttachment(2000)
    temp_c = temp_sensor.getTemperature()
    temp_f = (temp_c * 9/5) + 32
    temp_sensor.close()
    
    print(f"Phidget Temp: {temp_f:.1f}°F ({temp_c:.1f}°C)")

# Test DS18B20 sensor  
def test_ds18b20():
    import os, glob
    
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    
    device = glob.glob('/sys/bus/w1/devices/28*')[0]
    device_file = device + '/w1_slave'
    
    with open(device_file, 'r') as f:
        lines = f.readlines()
    
    temp_line = lines[1]
    temp_pos = temp_line.find('t=')
    temp_c = float(temp_line[temp_pos+2:]) / 1000.0
    temp_f = (temp_c * 9/5) + 32
    
    print(f"DS18B20 Temp: {temp_f:.1f}°F ({temp_c:.1f}°C)")

# Run test
# test_phidget()  # Uncomment to test Phidget
# test_ds18b20()  # Uncomment to test DS18B20
