import os
import time
import csv
import glob
from datetime import datetime
from gpiozero import LED, Buzzer
#Setup
# Enable 1-Wire interface
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

# Find the probe device
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Setup LED and buzzer for alerts
alert_led = LED(17)
alert_buzzer = Buzzer(5)

# Set temperature thresholds (Fahrenheit)
HIGH_TEMP = 75
LOW_TEMP = 65
#Functions
def read_temp_raw():
    """Read raw temperature data from sensor"""
    with open(device_file, 'r') as f:
        lines = f.readlines()
    return lines

def read_temp():
    """Convert raw data to actual temperature"""
    lines = read_temp_raw()
    
    # Check if reading is valid
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    
    # Extract temperature value
    temp_line = lines[1]
    temp_pos = temp_line.find('t=')
    
    if temp_pos != -1:
        temp_string = temp_line[temp_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    
    return None, None
#Main Loop
# Create CSV log file
log_filename = f"temperature_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(log_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Time', 'Temperature_C', 'Temperature_F', 'Status'])
    
    try:
        while True:
            celsius, fahrenheit = read_temp()
            
            if celsius is not None:
                # Get current time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Determine status and control alerts
                if fahrenheit > HIGH_TEMP:
                    status = "HIGH"
                    alert_led.on()
                    alert_buzzer.beep(0.5, 0.5, 3)  # Beep pattern for high temp
                elif fahrenheit < LOW_TEMP:
                    status = "LOW"
                    alert_led.blink(0.2, 0.8)  # Blink pattern for low temp
                    alert_buzzer.off()
                else:
                    status = "NORMAL"
                    alert_led.off()
                    alert_buzzer.off()
                
                # Log data
                writer.writerow([current_time, f"{celsius:.2f}", f"{fahrenheit:.2f}", status])
                csvfile.flush()  # Save immediately
                
                # Display current reading
                print(f"{current_time} | {fahrenheit:.2f}°F | Status: {status}")
            
            time.sleep(10)  # Read every 10 seconds
            
    except KeyboardInterrupt:
        alert_led.off()
        alert_buzzer.off()
        print("\nTemperature monitoring stopped.")
