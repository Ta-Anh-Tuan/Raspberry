import bme280
import smbus2
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep, time
import math

# Cài đặt BME280
port = 1
address = 0x76  # Địa chỉ I2C của BME280
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

# Cài đặt Anemometer
wind_count = 0
radius_cm = 9.0  # Bán kính của anemometer
interval = 5  # Khoảng thời gian lấy mẫu (giây)
wind_sensor = Button(5)

def spin():
    global wind_count
    wind_count += 1

wind_sensor.when_pressed = spin

# Cài đặt màn hình LCD
lcd = Adafruit_CharLCD(rs=27, en=22, d4=25, d5=24, d6=23, d7=18, cols=16, lines=2)

# Hàm đọc dữ liệu từ BME280
def read_bme280():
    bme280_data = bme280.sample(bus, address)
    return bme280_data.temperature, bme280_data.humidity, bme280_data.pressure

# Hàm tính tốc độ gió
def calculate_wind_speed():
    global wind_count
    circumference_cm = 2 * math.pi * radius_cm
    rotations = wind_count / 2.0  # Mỗi vòng quay tạo ra 2 tín hiệu
    dist_km = (circumference_cm * rotations) / 100000  # Đổi sang km
    km_per_sec = dist_km / interval
    km_per_hour = km_per_sec * 3600  # Đổi sang km/h
    wind_count = 0  # Reset bộ đếm
    return km_per_hour

# Hàm hiển thị dữ liệu lên màn hình LCD
def display_lcd(temp, humidity, wind_speed):
    lcd.clear()
    lcd.message(f'Temp: {temp:.1f}C\nHumidity: {humidity:.1f}%')
    sleep(2)
    lcd.clear()
    lcd.message(f'Wind Speed:\n{wind_speed:.1f} km/h')
    sleep(2)

# Vòng lặp chính
try:
    while True:
        # Đọc dữ liệu từ BME280
        temperature, humidity, _ = read_bme280()

        # Tính tốc độ gió
        sleep(interval)
        wind_speed = calculate_wind_speed()

        # Hiển thị dữ liệu lên màn hình LCD
        display_lcd(temperature, humidity, wind_speed)

except KeyboardInterrupt:
    lcd.clear()
    print("Đã dừng chương trình!")

finally:
    GPIO.cleanup()
