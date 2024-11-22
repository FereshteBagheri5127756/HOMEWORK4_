
import network
import urequests
import time
import dht
from machine import Pin

# تنظیمات Wi-Fi
WIFI_SSID = 'saeed'
WIFI_PASSWORD = 'saeed.433434'

# تنظیمات سرور
SERVER_URL = 'http://192.168.1.38:5000/temperature'

# پین سنسور DHT22
DHT_PIN = 4  # تغییر بر اساس پین متصل

# اتصال به Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("در حال اتصال به Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("اتصال برقرار شد:", wlan.ifconfig())

# خواندن داده از سنسور
def read_temperature():
    try:
        sensor = dht.DHT22(Pin(DHT_PIN))
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        return temperature, humidity
    except Exception as e:
        print("خطا در خواندن سنسور:", e)
        return None, None

# ارسال داده به سرور

def send_to_server(temperature, humidity):
    try:
        data = {
            "temperature": temperature,
            "humidity": humidity
        }
        response = urequests.post(SERVER_URL, json=data)
        print("پاسخ سرور:", response.text)
        response.close()
    except Exception as e:
        print("خطا در ارسال داده:", e)

# حلقه اصلی
def main():
    connect_to_wifi()
    while True:
        temperature, humidity = read_temperature()
        if temperature is not None:
            print("دمای فعلی = {}°C  رطوبت: {}%" . format(temperature,humidity)) | 
            send_to_server(temperature, humidity)
        time.sleep(10)  # اندازه‌گیری هر 10 ثانیه

if __name__ == "__main__":
    main()





