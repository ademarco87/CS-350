## Thermostat.py - Final Version
## CS 350 Final Project Submission

from time import sleep
from datetime import datetime
from statemachine import StateMachine, State
import board
import adafruit_ahtx0
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import serial
from gpiozero import Button, PWMLED
from threading import Thread
from math import floor

DEBUG = True  # Enable debugging output

# Initialize I2C communication
i2c = board.I2C()
thSensor = adafruit_ahtx0.AHTx0(i2c)

# Configure UART serial communication
ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Define GPIO pins for LEDs
redLight = PWMLED(18)
blueLight = PWMLED(23)

class ManagedDisplay():
    """Class to manage the LCD display."""
    def __init__(self):
        # Initialize LCD display pins
        self.lcd_rs = digitalio.DigitalInOut(board.D17)
        self.lcd_en = digitalio.DigitalInOut(board.D27)
        self.lcd_d4 = digitalio.DigitalInOut(board.D5)
        self.lcd_d5 = digitalio.DigitalInOut(board.D6)
        self.lcd_d6 = digitalio.DigitalInOut(board.D13)
        self.lcd_d7 = digitalio.DigitalInOut(board.D26)

        self.lcd_columns = 16  # Define LCD column count
        self.lcd_rows = 2  # Define LCD row count
        
        # Initialize LCD display
        self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, 
                    self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7, 
                    self.lcd_columns, self.lcd_rows)
        self.lcd.clear()  # Clear display

    def updateScreen(self, message):
        """Updates the LCD screen with a message."""
        self.lcd.clear()
        self.lcd.message = message

# Create display instance
screen = ManagedDisplay()

class TemperatureMachine(StateMachine):
    """State machine to manage thermostat states."""
    off = State(initial=True)
    heat = State()
    cool = State()
    setPoint = 72  # Default setpoint temperature

    # Define state transitions
    cycle = (off.to(heat) | heat.to(cool) | cool.to(off))

    def on_enter_heat(self):
        """Handle entering heat state."""
        self.updateLights()
        if DEBUG:
            print("* Changing state to heat")

    def on_exit_heat(self):
        """Handle exiting heat state."""
        redLight.off()

    def on_enter_cool(self):
        """Handle entering cool state."""
        self.updateLights()
        if DEBUG:
            print("* Changing state to cool")

    def on_exit_cool(self):
        """Handle exiting cool state."""
        blueLight.off()

    def on_enter_off(self):
        """Handle entering off state."""
        redLight.off()
        blueLight.off()
        if DEBUG:
            print("* Changing state to off")

    def processTempStateButton(self):
        """Cycle thermostat state when button is pressed."""
        if DEBUG:
            print("Cycling Temperature State")
        self.cycle()

    def processTempIncButton(self):
        """Increase temperature setpoint when button is pressed."""
        self.setPoint += 1
        self.updateLights()
        if DEBUG:
            print(f"Increasing Set Point to {self.setPoint}")

    def processTempDecButton(self):
        """Decrease temperature setpoint when button is pressed."""
        self.setPoint -= 1
        self.updateLights()
        if DEBUG:
            print(f"Decreasing Set Point to {self.setPoint}")

    def updateLights(self):
        """Update LED indicators based on thermostat state."""
        temp = floor(self.getFahrenheit())
        redLight.off()
        blueLight.off()
        
        if DEBUG:
            print(f"State: {self.current_state.id}, SetPoint: {self.setPoint}, Temp: {temp}")
        
        if self.current_state == self.heat:
            if temp < self.setPoint:
                redLight.pulse()
            else:
                redLight.on()
        elif self.current_state == self.cool:
            if temp > self.setPoint:
                blueLight.pulse()
            else:
                blueLight.on()

    def setupSerialOutput(self):
        """Prepare thermostat status output for UART transmission."""
        output = f"{self.current_state.id},{floor(self.getFahrenheit())},{self.setPoint}"
        return output

    def run(self):
        """Start display management thread."""
        myThread = Thread(target=self.manageMyDisplay)
        myThread.start()

    def getFahrenheit(self):
        """Retrieve temperature in Fahrenheit."""
        return (((9/5) * thSensor.temperature) + 32)

    endDisplay = False  # Control display state

    def manageMyDisplay(self):
        """Manage LCD display output."""
        counter = 1
        altCounter = 1
        while not self.endDisplay:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if altCounter < 6:
                lcd_line_2 = f"Temp: {floor(self.getFahrenheit())}F"
                altCounter += 1
            else:
                lcd_line_2 = f"{self.current_state.id.upper()} {self.setPoint}F"
                altCounter += 1
                if altCounter >= 11:
                    self.updateLights()
                    altCounter = 1
            
            screen.updateScreen(f"{current_time}\n{lcd_line_2}")
            
            if counter % 30 == 0:
                ser.write(self.setupSerialOutput().encode())
                counter = 1
            else:
                counter += 1
            sleep(1)
        
        screen.updateScreen("System Off")
        screen.cleanupDisplay()

# Initialize State Machine
tsm = TemperatureMachine()
tsm.run()

greenButton = Button(24)
greenButton.when_pressed = tsm.processTempStateButton

redButton = Button(25)
redButton.when_pressed = tsm.processTempIncButton

blueButton = Button(12)
blueButton.when_pressed = tsm.processTempDecButton

repeat = True

while repeat:
    try:
        sleep(30)
    except KeyboardInterrupt:
        print("Cleaning up. Exiting...")
        repeat = False
        tsm.endDisplay = True
        sleep(1)
