#Import
from gpiozero import LED, DigitalInputDevice
import time
#Setup
led = LED(17)
light_sensor = DigitalInputDevice(4)
#Functions
def light_detected():
    led.off()
    print("Bright environment - LED OFF")

def darkness_detected():
    led.on()
    print("Dark environment - LED ON")
#Main Loop
# Set up event handlers
light_sensor.when_activated = light_detected
light_sensor.when_deactivated = darkness_detected

print("Light-responsive system active")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nProgram terminated")
