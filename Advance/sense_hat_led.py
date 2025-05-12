from sense_hat import SenseHat  # Physical Sense HAT
# OR for testing:
# from sense_emu import SenseHat  # Sense HAT Emulator
from time import sleep
#Setup
sense = SenseHat()

# Define some useful colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
blank = (0, 0, 0)
# Main Loop
# Display a simple message
sense.show_message("Hello!", text_colour=green)

# Clear the display
sense.clear()

# Set individual pixels
sense.set_pixel(3, 3, red)  # Center pixel
sense.set_pixel(4, 4, blue) # Another pixel

# Fill the entire display
sense.clear(green)  # Fill with green
sleep(2)
sense.clear()      # Clear to black
#OR
#Create an Emoji
# Create a simple smiley face
smiley = [
    b, b, b, b, b, b, b, b,
    b, b, y, b, b, y, b, b,
    b, b, y, b, b, y, b, b,
    b, b, b, b, b, b, b, b,
    y, b, b, b, b, b, b, y,
    b, y, y, y, y, y, y, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b
]

# Define colors
y = (255, 255, 0)  # Yellow
b = (0, 0, 0)      # Black

sense.set_pixels(smiley)
