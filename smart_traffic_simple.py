from gpiozero import LED, Button, Buzzer
from time import sleep

red = LED(17)
yellow = LED(27)
green = LED(22)
button = Button(4)
buzzer = Buzzer(5)

while True:
    red.on()
    yellow.off()
    green.off()
    
    button.wait_for_press()
    buzzer.beep(0.2, 0.2, 1)
    
    red.off()
    green.on()
    sleep(5)
    
    green.off()
    yellow.on()
    buzzer.beep(0.1, 0.1, 3)
    sleep(2)
    
    yellow.off()
    red.on()
