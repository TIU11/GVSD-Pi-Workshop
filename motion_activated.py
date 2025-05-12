from gpiozero import MotionSensor, LED, Buzzer
from time import sleep
import time
import csv
from Phidget22.Phidget import *
from Phidget22.Devices.LCD import *
#Setup
pir = MotionSensor(4)
led = LED(17)
buzzer = Buzzer(22)

# Set up Phidget LCD
lcd = LCD()
lcd.setDeviceSerialNumber(123456)
lcd.setChannel(0)
lcd.openWaitForAttachment(5000)
lcd.setBacklight(0)  # Green
lcd.writeText(LCDFont.FONT_5X8, 0, 0, "Motion Detection")
# Main Loop
with open('motion_events.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Time', 'Event', 'Duration'])
    
    # Wait for sensor to settle
    print("PIR settling...")
    lcd.writeText(LCDFont.FONT_5X8, 0, 1, "Sensor Calibrating...")
    pir.wait_for_no_motion()
    lcd.writeText(LCDFont.FONT_5X8, 0, 1, "System Ready       ")
    
    try:
        while True:
            # Wait for motion
            pir.wait_for_motion()
            motion_start = time.time()
            motion_time = time.strftime('%H:%M:%S')
            
            # Alert
            led.on()
            buzzer.beep(0.1, 0.1, 1)
            lcd.writeText(LCDFont.FONT_5X8, 0, 2, "Motion: DETECTED   ")
            lcd.setBacklight(1)  # Red
            
            # Wait for motion to stop
            pir.wait_for_no_motion()
            motion_end = time.time()
            duration = round(motion_end - motion_start, 2)
            
            # Reset
            led.off()
            lcd.writeText(LCDFont.FONT_5X8, 0, 2, "Motion: NONE       ")
            lcd.setBacklight(0)  # Green
            
            # Log event
            writer.writerow([motion_time, "Motion detected", duration])
            f.flush()
            
    except KeyboardInterrupt:
        led.off()
        lcd.close()
