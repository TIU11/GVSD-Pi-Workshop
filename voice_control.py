import speech_recognition as sr
from gpiozero import LED
import time
#Setup
# Set up LEDs
red_led = LED(17)
green_led = LED(27)

# Initialize speech recognition
recognizer = sr.Recognizer()
#Functions
def process_command(command):
    command = command.lower()
    print(f"I heard: {command}")
    
    if "red on" in command or "turn on red" in command:
        red_led.on()
        print("Red LED turned ON")
        return True
    elif "red off" in command or "turn off red" in command:
        red_led.off()
        print("Red LED turned OFF")
        return True
    elif "green on" in command or "turn on green" in command:
        green_led.on()
        print("Green LED turned ON")
        return True
    elif "green off" in command or "turn off green" in command:
        green_led.off()
        print("Green LED turned OFF")
        return True
    elif "all on" in command:
        red_led.on()
        green_led.on()
        print("All LEDs turned ON")
        return True
    elif "all off" in command:
        red_led.off()
        green_led.off()
        print("All LEDs turned OFF")
        return True
    elif "exit" in command:
        print("Exiting program...")
        return False
    else:
        print("Command not recognized. Try again.")
        return True
#Main Loop
print("Voice-controlled LED system")
print("Say commands like: 'Turn on red', 'Green off', 'All on', 'Exit'")
print("System ready! Listening...")

running = True
while running:
    with sr.Microphone() as source:
        print("\nListening...")
        
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        
        try:
            # Listen for speech
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Processing...")
            
            # Recognize speech
            text = recognizer.recognize_google(audio)
            
            # Process command
            running = process_command(text)
            
        except sr.WaitTimeoutError:
            print("No speech detected. Listening again...")
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
        except Exception as e:
            print("error")

# Cleanup
red_led.off()
green_led.off()
print("Program terminated.")
