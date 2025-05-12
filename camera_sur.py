from picamera import PiCamera
from gpiozero import MotionSensor, LED
import time
from datetime import datetime
import os
# Setup
# Create directory for images
if not os.path.exists('motion_images'):
    os.makedirs('motion_images')

# Set up components
camera = PiCamera()
pir = MotionSensor(4)
led = LED(17)

# Configure camera
camera.resolution = (1024, 768)
print("Camera initialized")
# Main Loop
# Wait for PIR to settle
print("Waiting for PIR to settle...")
pir.wait_for_no_motion()
print("Ready! Waiting for motion...")

try:
    while True:
        # Wait for motion
        pir.wait_for_motion()
        
        # Indicate motion detected
        led.on()
        print("Motion detected!")
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"motion_images/motion_{timestamp}.jpg"
        
        # Take photo
        camera.capture(filename)
        print(f"Photo saved as {filename}")
        
        # Brief LED indication
        time.sleep(1)
        led.off()
        
        # Prevent multiple captures
        time.sleep(3)
        print("Ready for next motion detection")
        
except KeyboardInterrupt:
    print("\nProgram terminated")
    camera.close()
#OR
#Video Recording
# For video recording instead
#camera.start_recording(f'video_{timestamp}.h264')
#camera.wait_recording(10)  # 10 seconds
#camera.stop_recording()
