from gpiozero import LED, MCP3008
import time
import csv
from Phidget22.Phidget import *
from Phidget22.Devices.LCD import *
# Setup
alert_led = LED(17)

# Set up Phidget LCD
lcd = LCD()
lcd.setDeviceSerialNumber(123456)
lcd.setChannel(0)
lcd.openWaitForAttachment(5000)
lcd.setBacklight(0)  # Green
lcd.writeText(LCDFont.FONT_5X8, 0, 0, "Temperature Monitor")

threshold_voltage = 0.6  # Alert threshold
# Functions
def read_temp_voltage():
    # Simplified for demo - read thermistor
    return 0.5 + (time.time() % 10) / 50
# Main Loop
with open('temperature_log.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Voltage', 'Status'])
    
    try:
        while True:
            voltage = read_temp_voltage()
            now = time.strftime('%H:%M:%S')
            
            if voltage > threshold_voltage:
                alert_led.on()
                status = "ALERT"
                lcd.setBacklight(1)  # Red
            else:
                alert_led.off()
                status = "Normal"
                lcd.setBacklight(0)  # Green
            
            # Update LCD
            lcd.writeText(LCDFont.FONT_5X8, 0, 1, f"Voltage: {voltage:.3f}V")
            lcd.writeText(LCDFont.FONT_5X8, 0, 2, f"Status: {status}")
            
            # Log data
            writer.writerow([now, f"{voltage:.3f}", status])
            f.flush()
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        lcd.close()
