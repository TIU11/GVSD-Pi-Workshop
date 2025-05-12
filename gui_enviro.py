from guizero import App, Text, PushButton, CheckBox, Box
from gpiozero import LED, DigitalInputDevice
import time
#Setup
# Hardware setup
light = LED(17)
light_sensor = DigitalInputDevice(4)

# GUI setup
app = App(title="Environmental Control Dashboard", width=400, height=300)
app.bg = "#e8f4f8"

# Global variable
auto_mode = True
#Functions
def toggle_light():
    if light.is_lit:
        light.off()
        light_button.text = "Turn Light ON"
        light_button.bg = "lightgray"
        status_text.value = "Light is OFF"
    else:
        light.on()
        light_button.text = "Turn Light OFF"
        light_button.bg = "yellow"
        status_text.value = "Light is ON"

def toggle_auto_mode():
    global auto_mode
    auto_mode = auto_checkbox.value
    
    if auto_mode:
        mode_text.value = "Automatic Mode (Light Sensor Controlled)"
        light_button.disable()
        check_light_sensor()
    else:
        mode_text.value = "Manual Mode"
        light_button.enable()

def check_light_sensor():
    if auto_mode:
        if light_sensor.value:
            light.off()
            status_text.value = "Bright Environment - Light OFF"
            status_text.text_color = "blue"
        else:
            light.on()
            status_text.value = "Dark Environment - Light ON"
            status_text.text_color = "orange"
#Main Loop
# Create GUI elements
title = Text(app, text="Smart Light Control Panel", size=20)
title.text_color = "#193854"

# Status display
status_box = Box(app, width="fill", height=50, border=True)
Text(status_box, text="Status:", size=14)
status_text = Text(status_box, text="Initializing...", size=14)

# Controls
control_box = Box(app, width="fill", height=150, border=True)

auto_checkbox = CheckBox(control_box, text="Automatic Light Control", 
                        command=toggle_auto_mode)
auto_checkbox.value = auto_mode

mode_text = Text(control_box, text="Automatic Mode (Light Sensor Controlled)", 
                size=14)

light_button = PushButton(control_box, text="Turn Light ON", 
                         command=toggle_light)
light_button.bg = "lightgray"
light_button.disable()  # Start disabled in auto mode

# Footer
footer = Text(app, text="TIU STEM Workshop - Raspberry Pi & Phidgets", size=10)

# Update loop
def update_gui():
    check_light_sensor()
    app.after(500, update_gui)

update_gui()

# Display app
app.display()
