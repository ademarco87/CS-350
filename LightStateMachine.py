#
# MorseStateMachine.py - This is the Python code used to demonstrate
# building a StateMachine that processes events to switch between 
# displaying Morse Code using a Red (dot) and Blue (dash) LED.
#
# This code works with the test circuit that was built for module 5.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development (Based on LightStateMachine.py)
#------------------------------------------------------------------

##
## Imports required to handle our Button, and our PWMLED devices
##
from gpiozero import Button, PWMLED

##
## Imports required to allow us to build a fully functional state machine
##
from statemachine import StateMachine, State

##
## Import required to allow us to pause for a specified length of time
##
from time import sleep

##
## Imports for 16x2 LCD display support
##
import board
import digitalio
from adafruit_character_lcd.character_lcd import Character_LCD_Mono

##
## DEBUG flag - boolean value to indicate whether or not to print 
## status messages on the console of the program
## 
DEBUG = True

##
## GPIO Pin Assignments
##
RED_LED = 18      # Red LED (dot)
BLUE_LED = 23     # Blue LED (dash)
BUTTON_PIN = 24   # Button

# LCD Pin Assignments
LCD_RS = board.D26
LCD_E = board.D19
LCD_D4 = board.D13
LCD_D5 = board.D6
LCD_D6 = board.D5
LCD_D7 = board.D11

##
## Initialize LEDs
##
redLight = PWMLED(RED_LED)
blueLight = PWMLED(BLUE_LED)
greenButton = Button(BUTTON_PIN)

##
## Initialize LCD Display
##
lcd_rs = digitalio.DigitalInOut(LCD_RS)
lcd_en = digitalio.DigitalInOut(LCD_E)
lcd_d4 = digitalio.DigitalInOut(LCD_D4)
lcd_d5 = digitalio.DigitalInOut(LCD_D5)
lcd_d6 = digitalio.DigitalInOut(LCD_D6)
lcd_d7 = digitalio.DigitalInOut(LCD_D7)

# Define LCD column and row size
lcd_columns = 16
lcd_rows = 2

# Initialize LCD
lcd = Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

##
## Morse Code Dictionary
##
MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', ' ': ' '
}

##
## List of Morse Code Messages
##
messages = ["HELLO", "SOS", "PYTHON"]
current_message_index = 0

##
## MorseMachine - This is our StateMachine implementation class.
##
class MorseMachine(StateMachine):
    "A state machine designed to flash Morse code messages using LEDs"

    ##
    ## Define the two states for our machine.
    ##
    ##  idle - waiting for button press
    ##  transmitting - sending Morse code
    ##
    idle = State(initial=True)
    transmitting = State()

    ##
    ## begin - event that launches the state machine behavior
    ##
    begin = (
        idle.to(transmitting)
    )

    ##
    ## cycle - event that transitions back to idle after sending message
    ##
    cycle = (
        transmitting.to(idle)
    )

    ##
    ## on_enter_transmitting - Action performed when the state machine transitions
    ## into the transmitting state
    ##
    def on_enter_transmitting(self):
        global current_message_index
        message = messages[current_message_index]

        lcd.clear()
        lcd.message = f"Sending:\n{message}"

        if DEBUG:
            print(f"* Transmitting Morse Code: {message}")

        self.flash_morse(message)

        ## Transition back to idle state after completing transmission
        self.cycle()

    ##
    ## flash_morse - Sends Morse code for the given message.
    ##
    def flash_morse(self, message):
        for char in message:
            if char in MORSE_CODE:
                code = MORSE_CODE[char]
                for symbol in code:
                    if symbol == '.':
                        redLight.on()
                        sleep(0.5)  # 500ms for dot
                        redLight.off()
                    elif symbol == '-':
                        blueLight.on()
                        sleep(1.5)  # 1500ms for dash
                        blueLight.off()
                    sleep(0.5)  # Pause between symbols
                sleep(1.0)  # Space between letters

        lcd.clear()
        lcd.message = "Message Sent"

        if DEBUG:
            print("* Morse code transmission complete.")

    ##
    ## processButton - Utility method used to send events to the 
    ## state machine. This is triggered by the button_pressed event
    ##
    def processButton(self):
        global current_message_index
        current_message_index = (current_message_index + 1) % len(messages)
        
        lcd.clear()
        lcd.message = f"Next Msg:\n{messages[current_message_index]}"
        
        if DEBUG:
            print(f"* Button pressed, switching to next message: {messages[current_message_index]}")

        sleep(1)
        lcd.clear()

##
## Initialize our Morse Code State Machine
##
morse_machine = MorseMachine()

##
## greenButton - setup our Button, tied to GPIO 24. Configure the
## action to be taken when the button is pressed to be the 
## execution of the processButton function in our State Machine
##
greenButton.when_pressed = morse_machine.processButton

##
## Setup loop variable
##
repeat = True

##
## Repeat until the user creates a keyboard interrupt (CTRL-C)
##
while repeat:
    try:
        ## Only display if the DEBUG flag is set
        if(DEBUG):
            print("Killing time in a loop...")

        ## If in idle state, begin Morse transmission
        if morse_machine.current_state.id == 'idle':
            morse_machine.begin()

        ## Sleep for a bit to avoid CPU overuse
        sleep(1)

    except KeyboardInterrupt:
        ## Catch the keyboard interrupt (CTRL-C) and exit cleanly
        ## we do not need to manually clean up the GPIO pins, the 
        ## gpiozero library handles that process.
        print("Cleaning up. Exiting...")
        
        ## Clear the LCD screen
        lcd.clear()
        lcd.message = "Exiting..."

        ## Stop the loop
        repeat = False
        sleep(1)
