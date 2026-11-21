import json

class AIAgent:
    def __init__(self, ai_client, exec_env=None):
        self.ai = ai_client
        self.exec_env = exec_env if exec_env is not None else {}
        self._reports = []
        # Inject the report() helper automatically into every app's environment
        self.exec_env["report"] = self._report

    def _report(self, data):
        self._reports.append(str(data))

    def _parse_json(self, raw_text):
        text = raw_text.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            if len(lines) >= 3:
                text = "\n".join(lines[1:-1]).strip()
        return json.loads(text)

    def _run_code(self, code):
        self._reports = []
        exec(code, self.exec_env)
        return self._reports

    def step(self, user_prompt):
        raw_reply = self.ai.ask(user_prompt)

        if raw_reply.startswith("HTTP ") or raw_reply.startswith("Request error:"):
            print("API Error:", raw_reply)
            return

        try:
            data = self._parse_json(raw_reply)
        except Exception as e:
            print("JSON Parse Error:", e, "\nRaw:", raw_reply)
            return

        if data.get("response"):
            print("AI:", data["response"])

        code = data.get("execution", "").strip()
        if not code:
            return

        print("EXEC:\n" + code)
        try:
            readings = self._run_code(code)
            # If the executed code called report(), send sensor values back to the AI
            if readings:
                followup = self.ai.ask(
                    f"Sensor readings returned: {', '.join(readings)}. Respond to the user and update hardware if needed."
                )
                follow_data = self._parse_json(followup)
                if follow_data.get("response"):
                    print("AI:", follow_data["response"])
                follow_code = follow_data.get("execution", "").strip()
                if follow_code:
                    self._run_code(follow_code)
        except Exception as err:
            print("Execution Error:", err)
