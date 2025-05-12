import spidev
import time
from gpiozero import LED
import csv
from Phidget22.Phidget import *
from Phidget22.Devices.LCD import *
# Setup
power_led = LED(17)

# Set up SPI for ADC0834
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

# Set up Phidget LCD
lcd = LCD()
lcd.setDeviceSerialNumber(123456)
lcd.setChannel(0)
lcd.openWaitForAttachment(5000)
lcd.setBacklight(0)  # Green
lcd.writeText(LCDFont.FONT_5X8, 0, 0, "Solar Energy Monitor")

voltage_threshold = 0.5  # Volts
# Functions
def read_adc0834(channel):
    cmd = 128 + channel << 4
    reply_bytes = spi.xfer2([cmd, 0, 0])
    value = reply_bytes[2]
    return value

def convert_to_voltage(adc_value):
    # ADC0834 is 8-bit (0-255), reference 3.3V
    # Voltage divider ratio is 11:1
    voltage = adc_value * 3.3 / 255.0 * 11.0
    return voltage
# Main Loop
# Initialize energy tracking
total_energy = 0
last_time = time.time()

with open('solar_energy.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Voltage (V)', 'Power (mW)', 'Energy (mWh)'])
    
    try:
        while True:
            current_time = time.time()
            delta_time = current_time - last_time
            last_time = current_time
            
            # Read and convert voltage
            adc_value = read_adc0834(0)
            voltage = convert_to_voltage(adc_value)
            
            # Calculate power
            current = voltage / 50.0  # Assuming 50Ω load
            power = voltage * current
            
            # Calculate energy
            energy_increment = power * delta_time
            total_energy += energy_increment
            total_energy_mWh = total_energy * 1000 / 3600
            
            now = time.strftime('%H:%M:%S')
            
            # Control LED
            if voltage > voltage_threshold:
                power_led.on()
                status = "Generating"
            else:
                power_led.off()
                status = "Low/No Light"
            
            # Update LCD
            lcd.writeText(LCDFont.FONT_5X8, 0, 1, f"Voltage: {voltage:.2f}V   ")
            lcd.writeText(LCDFont.FONT_5X8, 0, 2, f"Power: {power*1000:.1f}mW  ")
            lcd.writeText(LCDFont.FONT_5X8, 0, 3, f"Energy: {total_energy_mWh:.2f}mWh")
            
            # Log data
            writer.writerow([now, f"{voltage:.2f}", f"{power*1000:.1f}", f"{total_energy_mWh:.2f}"])
            f.flush()
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        power_led.off()
        lcd.close()
        spi.close()
