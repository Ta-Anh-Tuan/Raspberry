from EmulatorGUI import GPIO
import time
import traceback

from gpiozero import LEDBoard, Button
from time import sleep
         

def Main():


    LED_PINS = [2, 3, 4, 5, 6, 7, 8, 9]
    BUTTON_PIN = 10

    leds = LEDBoard(*LED_PINS)
    button = Button(BUTTON_PIN)

    running = False

    def toggle_running():
        global running
        running = not running

    button.when_pressed = toggle_running

    def set_leds(byte_value):
        """Update LED states based on the byte value."""
        for i in range(8):
            leds[i].value = (byte_value >> i) & 1

    def run_led_effect():
        """Run LED effect pattern."""
        pattern = [
            0b00011000,
            0b00100100,
            0b01000010,
            0b10000001,
            0b00000000,
            0b10000001,
            0b01000010,
            0b00100100,
            0b00011000
        ]

        while running:
            for p in pattern:
                if not running:
                    break
                set_leds(p)
                sleep(1)

    try:
        print("Program is ready. Press the button to start or stop.")
        while True:
            if running:
                run_led_effect()
            else:
                set_leds(0b00000000)
            sleep(0.1)

    finally:
        pass

Main()