from gpiozero import TrafficLights, Button, Buzzer
from time import sleep
#Setup
# Set up components with their GPIO pins
traffic = TrafficLights(red=17, yellow=27, green=22)
button = Button(4)
buzzer = Buzzer(5)
#Main Loop
while True:
    # Start with red light on
    traffic.red.on()
    traffic.yellow.off()
    traffic.green.off()
    
    # Wait for button press
    button.wait_for_press()
    
    # Sound buzzer briefly to indicate button press
    buzzer.beep(0.2, 0.2, 1)  # On for 0.2s, off for 0.2s, repeat once
    
    # Change to green
    traffic.red.off()
    traffic.green.on()
    sleep(5)    # Stay green for 5 seconds
    
    # Yellow warning with buzzer
    traffic.green.off()
    traffic.yellow.on()
    buzzer.beep(0.1, 0.1, 3)  # Quick beeps for yellow warning
    sleep(2)    # Stay yellow for 2 seconds
    
    # Back to red
    traffic.yellow.off()
    traffic.red.on()
