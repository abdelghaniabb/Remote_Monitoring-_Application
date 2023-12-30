#!/usr/bin/python3
"""Get or Control the state of the Raspberry Pi gpio """
try:
    # This part will be executed if the code is executed on a Raspberry Pi
    import RPi.GPIO as GPIO

    def change_gpio(pin, status):
        """Change the state of the specified GPIO pin."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, status)

    def get_state_gpio(pin):
        """Get the state of the specified GPIO pin."""
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)
        return GPIO.input(pin)

except ImportError:
    # This part will only run to pass the test and view the page on a regular computer
    def change_gpio(pin, status):
        pass

    def get_state_gpio(pin):
        return 1
