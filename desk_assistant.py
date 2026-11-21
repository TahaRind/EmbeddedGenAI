import machine
import time
import dht
import ssd1306

SYSTEM_PROMPT = """
You are an embodied AI controlling an ESP32 Smart Desk Assistant.
Available objects & helpers in your execution scope:
- `sensor`: DHT22 sensor. Call `sensor.measure()` first, then `sensor.temperature()` (C) and `sensor.humidity()` (%).
- `oled`: 128x64 SSD1306 OLED. Methods: `oled.fill(0)`, `oled.text("str", x, y)` (max 16 chars/line, y=0,10,20,30,40,50), `oled.show()`.
- `set_servo(angle)`: Moves servo pointer from 0 to 180 degrees.
- `beep(freq, duration)`: Plays a tone in Hz for `duration` seconds.
- `report(value)`: Call this when reading sensors so the ESP32 sends the value back to you for your final answer.
- `time`: Standard MicroPython time module.

Respond ONLY with valid raw JSON (no markdown):
{"response": "message to user", "execution": "micropython code or empty string"}

Rules:
- Keep `execution` non-blocking (no infinite loops).
- Always call `oled.show()` after updating the screen.
- If asked about temperature/humidity, measure it and call `report(...)`.
"""

def setup():
    """Initializes hardware and returns (exec_env, on_boot, on_ready)."""
    sensor = dht.DHT22(machine.Pin(15))
    i2c = machine.SoftI2C(scl=machine.Pin(20), sda=machine.Pin(21))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    servo_pwm = machine.PWM(machine.Pin(13), freq=50)
    buzzer = machine.PWM(machine.Pin(12), freq=1000, duty=0)

    def set_servo(angle):
        angle = max(0, min(180, angle))
        servo_pwm.duty(int(26 + (angle / 180) * 102))

    def beep(freq=1000, duration=0.2):
        buzzer.freq(freq)
        buzzer.duty(512)
        time.sleep(duration)
        buzzer.duty(0)

    def on_boot():
        oled.fill(0)
        oled.text("Connecting WiFi", 0, 20)
        oled.show()

    def on_ready():
        oled.fill(0)
        oled.text("Desk AI Ready!", 0, 20)
        oled.show()

    exec_env = {
        "time": time,
        "sensor": sensor,
        "oled": oled,
        "set_servo": set_servo,
        "beep": beep,
    }

    return exec_env, on_boot, on_ready
