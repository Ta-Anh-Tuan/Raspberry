import RPi.GPIO as GPIO
import time

LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18
DISPLAY_BUTTON = 22
SYSTEM_BUTTON = 27
LED_PIN = 17

LCD_WIDTH = 16
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0

E_PULSE = 0.0005
E_DELAY = 0.0005

def read_bme280():
    temperature = 25.0
    pressure = 980.0
    humidity = 47.0
    return temperature, pressure, humidity

def read_anemometer():
    wind_speed = 25.0
    return wind_speed

def lcd_init():
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(E_DELAY)

def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)

    GPIO.output(LCD_D4, bits & 0x10 == 0x10)
    GPIO.output(LCD_D5, bits & 0x20 == 0x20)
    GPIO.output(LCD_D6, bits & 0x40 == 0x40)
    GPIO.output(LCD_D7, bits & 0x80 == 0x80)
    lcd_toggle_enable()

    GPIO.output(LCD_D4, bits & 0x01 == 0x01)
    GPIO.output(LCD_D5, bits & 0x02 == 0x02)
    GPIO.output(LCD_D6, bits & 0x04 == 0x04)
    GPIO.output(LCD_D7, bits & 0x08 == 0x08)
    lcd_toggle_enable()

def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    time.sleep(E_DELAY)

def lcd_string(message, line):
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)

    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)
    GPIO.setup(DISPLAY_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(SYSTEM_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(LED_PIN, GPIO.OUT)

    lcd_init()

    display_state = 0
    system_state = False

    while True:
        if GPIO.input(SYSTEM_BUTTON) == GPIO.LOW:
            system_state = not system_state
            GPIO.output(LED_PIN, system_state)
            time.sleep(0.3)

        if not system_state:
            lcd_byte(0x01, LCD_CMD)
            continue

        if GPIO.input(DISPLAY_BUTTON) == GPIO.LOW:
            display_state = 1 - display_state
            time.sleep(0.3)

        temperature, pressure, humidity = read_bme280()
        wind_speed = read_anemometer()

        if display_state == 0:
            lcd_string(f"Temp:{temperature:.1f}C", LCD_LINE_1)
            lcd_string(f"Humidity:{humidity:.1f}%", LCD_LINE_2)
        else:
            lcd_string(f"Wind:{wind_speed:.1f}km/h", LCD_LINE_1)
            lcd_string(f"Pressure:{pressure:.1f}hPa", LCD_LINE_2)

        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)/-strong/-heart:>:o:-((:-h GPIO.cleanup()
