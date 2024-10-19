import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from smbus2 import SMBus

# Cau hinh cac chan GPIO
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
ANEMOMETER_PIN = 27
LED_PIN = 16
BUTTON_START_PIN = 24
BUTTON_STOP_PIN = 23
I2C_ADDR = 0x27  # Dia chi I2C cua LCD

# Cau hinh GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_START_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(ANEMOMETER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LCD 16x2 I2C setup
class LCD:
    def __init__(self, addr):
        self.addr = addr
        self.bus = SMBus(1)
        self.init_display()

    def init_display(self):
        self.command(0x33)  # Khoi tao
        self.command(0x32)  # Khoi tao
        self.command(0x06)  # Di chuyen con tro tu dong
        self.command(0x0C)  # Bat hien thi
        self.command(0x28)  # Man hinh 2 dong, ma tran 5x7
        self.command(0x01)  # Xoa man hinh

    def command(self, cmd):
        self.bus.write_byte_data(self.addr, 0, cmd)
        time.sleep(0.0005)

    def write(self, text):
        for char in text:
            self.bus.write_byte_data(self.addr, 0x40, ord(char))

    def display(self, line1, line2):
        self.command(0x80)  # Dat con tro vao dong 1
        self.write(line1.ljust(16))
        self.command(0xC0)  # Dat con tro vao dong 2
        self.write(line2.ljust(16))

# Khoi tao man hinh LCD
lcd = LCD(I2C_ADDR)

# Bien dieu khien
system_running = False

# Xu ly su kien nhan nut
def start_system(channel):
    global system_running
    system_running = True
    GPIO.output(LED_PIN, True)
    print("He thong bat dau")

def stop_system(channel):
    global system_running
    system_running = False
    GPIO.output(LED_PIN, False)
    print("He thong dung")

# Ket noi nut bam voi ham xu ly
GPIO.add_event_detect(BUTTON_START_PIN, GPIO.FALLING, callback=start_system, bouncetime=300)
GPIO.add_event_detect(BUTTON_STOP_PIN, GPIO.FALLING, callback=stop_system, bouncetime=300)

# Ham doc toc do gio tu Anemometer
def read_wind_speed():
    pulse_count = 0
    start_time = time.time()

    while time.time() - start_time < 5:  # Dem so lan quay trong 5 giay
        if GPIO.input(ANEMOMETER_PIN) == 0:
            pulse_count += 1
        time.sleep(0.1)
    
    # Cong thuc tinh toc do gio dua vao so lan quay (can tra thong so cua cam bien)
    wind_speed = pulse_count * 1.2  # Vi du: 1.2 m/s cho moi pulse
    return wind_speed

# Ham chinh thu thap du lieu va hien thi
def weather_monitoring():
    while True:
        if system_running:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            wind_speed = read_wind_speed()

            if humidity is not None and temperature is not None:
                lcd.display(f"Nhiet: {temperature:.1f}C", f"Do am: {humidity:.1f}%")
                print(f"Nhiet do: {temperature:.1f}C, Do am: {humidity:.1f}%")
            else:
                print("Loi cam bien DHT22")
            
            lcd.display(f"Toc do: {wind_speed:.1f}m/s", " ")
            print(f"Toc do gio: {wind_speed:.1f} m/s")

            time.sleep(5)
        else:
            time.sleep(1)

try:
    weather_monitoring()
except KeyboardInterrupt:
    print("Dong he thong")
finally:
    GPIO.cleanup()
