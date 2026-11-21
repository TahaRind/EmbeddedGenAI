import network
import urequests
import json
import time
import gc

class AIClient:
    def __init__(self, api_key, api_url, model, system_prompt="You are a helpful assistant.", max_history=10):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def connect_wifi(self, ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        print("Connecting to WiFi", end="")
        while not wlan.isconnected():
            print(".", end="")
            time.sleep(0.5)
        print("\nConnected! IP:", wlan.ifconfig()[0])

    def ask(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        if len(self.messages) > self.max_history + 1:
            self.messages = [self.messages[0]] + self.messages[-self.max_history:]

        payload_bytes = json.dumps({
            "model": self.model,
            "messages": self.messages
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
            "Content-Length": str(len(payload_bytes))
        }

        try:
            gc.collect()
            response = urequests.post(self.api_url, headers=headers, data=payload_bytes)
            if response.status_code == 200:
                data = response.json()
                reply = data["choices"][0]["message"]["content"]
                self.messages.append({"role": "assistant", "content": reply})
                response.close()
                gc.collect()
                return reply
            else:
                err = f"HTTP {response.status_code}: {response.text}"
                self.messages.pop()
                response.close()
                return err
        except Exception as e:
            self.messages.pop()
            return f"Request error: {e}"

    def reset(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]
