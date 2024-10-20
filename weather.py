import smbus2
import bme280
import RPi.GPIO as GPIO
from time import sleep, time
from gpiozero import Button
from Adafruit_CharLCD import Adafruit_CharLCD

# Cài đặt GPIO cho anemometer
wind_sensor = Button(5)  # GPIO 5
wind_count = 0
radius_cm = 9.0  # Bán kính của anemometer
interval = 5  # Khoảng thời gian lấy mẫu (giây)

# Cài đặt kết nối BME280
port = 1
address = 0x76  # Địa chỉ I2C của BME280
bus = smbus2.SMBus(port)
bme280.load_calibration_params(bus, address)

# Cài đặt màn hình LCD
lcd = Adafruit_CharLCD(rs=27, en=22, d4=25, d5=24, d6=23, d7=18, cols=16, lines=2)

# Cài đặt nút bật/tắt chương trình
on_off_button = Button(6)  # GPIO 6
is_running = False  # Trạng thái chương trình, ban đầu là Tắt

# Hàm xử lý tín hiệu từ anemometer
def spin():
    global wind_count
    wind_count += 1

wind_sensor.when_pressed = spin

# Hàm bật/tắt chương trình
def toggle_program():
    global is_running
    is_running = not is_running  # Đảo ngược trạng thái

on_off_button.when_pressed = toggle_program

# Hàm tính tốc độ gió
def calculate_wind_speed():
    global wind_count
    circumference_cm = 2 * 3.14159 * radius_cm
    rotations = wind_count / 2.0  # Mỗi vòng quay đầy đủ tạo ra 2 tín hiệu
    dist_km = (circumference_cm * rotations) / 100000  # Chuyển đổi sang km
    km_per_sec = dist_km / interval
    km_per_hour = km_per_sec * 3600  # Chuyển đổi sang km/h
    wind_count = 0  # Reset bộ đếm
    return km_per_hour

# Hàm đọc dữ liệu từ BME280
def read_bme280():
    data = bme280.sample(bus, address)
    return data.temperature, data.humidity

# Hàm hiển thị lên màn hình LCD
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
        if is_running:  # Kiểm tra trạng thái bật/tắt
            # Đọc dữ liệu từ BME280
            temperature, humidity = read_bme280()

            # Tính tốc độ gió
            sleep(interval)
            wind_speed = calculate_wind_speed()

            # Hiển thị lên màn hình LCD
            display_lcd(temperature, humidity, wind_speed)
        else:
            lcd.clear()
            lcd.message("Program is OFF")
            sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    print("Đã dừng chương trình!")

finally:
    GPIO.cleanup()
