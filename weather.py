import bme280
import smbus2
from gpiozero import Button, LED
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep
import math
import RPi.GPIO as GPIO

# Cai dat BME280
port = 1
address = 0x76  # Dia chi I2C cua BME280
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

# Cai dat Anemometer
wind_count = 0
radius_cm = 9.0  # Ban kinh cua anemometer
interval = 5  # Khoang thoi gian lay mau (giay)
wind_sensor = Button(5)  # Ket noi voi GPIO 5

def spin():
    global wind_count
    wind_count += 1

wind_sensor.when_pressed = spin

# Cai dat nut Start/Stop
start_button = Button(23)  # GPIO 23
stop_button = Button(24)   # GPIO 24
is_running = False  # Trang thai chuong trinh, ban dau la Tat

# Cai dat LED
status_led = LED(16)  # Den LED ket noi voi GPIO 16

# Ham bat chuong trinh
def start_program():
    global is_running
    is_running = True
    status_led.on()  # Bat den LED

# Ham tat chuong trinh
def stop_program():
    global is_running
    is_running = False
    status_led.off()  # Tat den LED

start_button.when_pressed = start_program
stop_button.when_pressed = stop_program

# Cai dat man hinh LCD I2C (giao tiep I2C)
lcd = Adafruit_CharLCD(rs=0, en=0, d4=0, d5=0, d6=0, d7=0, cols=16, lines=2, i2c_expander='PCF8574', address=0x27)

# Ham doc du lieu tu BME280
def read_bme280():
    bme280_data = bme280.sample(bus, address)
    return bme280_data.temperature, bme280_data.humidity, bme280_data.pressure

# Ham tinh toc do gio
def calculate_wind_speed():
    global wind_count
    circumference_cm = 2 * math.pi * radius_cm
    rotations = wind_count / 2.0  # Moi vong quay tao ra 2 tin hieu
    dist_km = (circumference_cm * rotations) / 100000  # Doi sang km
    km_per_sec = dist_km / interval
    km_per_hour = km_per_sec * 3600  # Doi sang km/h
    wind_count = 0  # Reset bo dem
    return km_per_hour

# Ham hien thi du lieu len man hinh LCD
def display_lcd(temp, humidity, wind_speed):
    lcd.clear()
    lcd.message(f'Temp: {temp:.1f}C\nHumidity: {humidity:.1f}%')
    sleep(2)
    lcd.clear()
    lcd.message(f'Wind Speed:\n{wind_speed:.1f} km/h')
    sleep(2)

# Vong lap chinh
try:
    while True:
        if is_running:  # Chi chay khi nut Start da duoc nhan
            # Doc du lieu tu BME280
            temperature, humidity, _ = read_bme280()

            # Tinh toc do gio
            sleep(interval)
            wind_speed = calculate_wind_speed()

            # Hien thi du lieu len man hinh LCD
            display_lcd(temperature, humidity, wind_speed)
        else:
            lcd.clear()
            lcd.message("Program is OFF")
            sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    print("Da dung chuong trinh!")
finally:
    GPIO.cleanup()
