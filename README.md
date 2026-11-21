# EmbeddedGenAI
AI processing unit for embedded systems

A modular MicroPython framework for the **ESP32-S3** that connects an LLM (via Groq or OpenAI-compatible APIs) directly to physical sensors, displays, and actuators. Instead of just chatting, the AI responds with structured JSON containing both a human-readable reply and live MicroPython code executed on the microcontroller—complete with a two-way sensor feedback loop.

---

## Features

* **Layered, Modular Architecture:** Clean separation between network/API calls, AI code execution, hardware blueprints, and the runtime launcher.
* **Live Code Execution (`exec`):** The AI dynamically controls GPIO pins, I2C displays, PWM servos, and buzzers at runtime.
* **Two-Way Sensor Feedback (`report()`):** Executed code can read sensors (like temperature/humidity) and pass readings back to the AI for context-aware follow-up actions.
* **Swap-in Feature Blueprints:** Easily switch between different hardware setups by changing one variable (`ACTIVE_FEATURE`) in `main.py`.
* **ESP32 Memory Management:** Built-in conversation history trimming and garbage collection (`gc.collect()`) to prevent TLS/JSON out-of-memory errors.

---

## Project Structure

```text
/
├── config.py          # Wi-Fi credentials, API key, endpoint, and model selection
├── ai_client.py       # Layer 1: Wi-Fi management and UTF-8 HTTPS API client
├── ai_agent.py        # Layer 2: JSON parser, sandboxed exec() runner, and report() loop
├── desk_assistant.py  # Layer 3: Hardware blueprint (DHT22 + OLED + Servo + Buzzer)
├── ssd1306.py         # I2C OLED display driver
└── main.py            # Layer 4: Universal runtime launcher and serial command loop
```

---

## Hardware Wiring (Smart Desk Assistant)

Designed for **ESP32-S3** (physical breadboard or Wokwi simulator):

| Component | Pin / Signal | ESP32-S3 Pin | Notes |
| :--- | :--- | :--- | :--- |
| **All Components** | `GND` | `GND` | Common ground |
| **SSD1306 OLED (128x64)** | `VCC` | `3.3V` | I2C Address `0x3C` |
| | `SDA` | `GPIO 21` | `SoftI2C` data |
| | `SCL` | `GPIO 22` | `SoftI2C` clock |
| **DHT22 Sensor** | `VCC` | `3.3V` | |
| | `DATA` | `GPIO 15` | Temperature & humidity |
| **SG90 Servo** | `VCC` (Red) | `5V` | |
| | `Signal` (Orange) | `GPIO 13` | 50Hz PWM (`0°–180°`) |
| **Passive Buzzer** | `+` | `GPIO 12` | PWM tone generator |
| | `-` | `GND` | |

---

## Setup & Installation

1. **Flash MicroPython:** Ensure your ESP32-S3 is running MicroPython (tested on `v1.28.0`).
2. **Add Credentials:** Edit `config.py` with your Wi-Fi and API details:
   ```python
   SSID = "your_wifi_ssid"
   PASSWORD = "your_wifi_password"
   API_KEY = "your_api_key"
   API_URL = "https://api.groq.com/openai/v1/chat/completions"
   MODEL = "openai/gpt-oss-20b"
   ```
3. **Upload Files:** Upload `config.py`, `ai_client.py`, `ai_agent.py`, `desk_assistant.py`, `ssd1306.py`, and `main.py` to the root directory of your ESP32-S3.
4. **Boot:** Reset the board or run `main.py`. Open a serial terminal at `115200` baud.

---

## Usage

Once the OLED displays `Desk AI Ready!`, type natural-language commands into the serial monitor:

* **Sensor + Action:**
  > *"Check the room temperature and humidity, display them on the OLED, and move the servo to 0 if cold, 90 if comfy, or 180 if hot."*
* **Multi-Actuator Expression:**
  > *"Act excited—wave the servo three times, show a happy face on the OLED, and play a chime."*
* **Reset Conversation Memory:**
  > `/reset`

---

## Creating a New Feature Blueprint

To build a different hardware project without touching the core engine:

1. Create a new file (e.g., `my_project.py`) defining a `SYSTEM_PROMPT` string and a `setup()` function that returns `(exec_env, on_boot, on_ready)`.
2. In `main.py`, import your module and update:
   ```python
   import my_project
   ACTIVE_FEATURE = my_project
   ```
README.md
Displaying README.md.
