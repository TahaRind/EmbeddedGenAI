import config
from ai_client import AIClient
from ai_agent import AIAgent
import desk_assistant

# 1. Select which feature module to run
ACTIVE_FEATURE = desk_assistant

def run(feature):
    # Initialize feature-specific hardware & lifecycle hooks
    exec_env, on_boot, on_ready = feature.setup()

    if on_boot:
        on_boot()

    # Initialize generic AI client & agent
    client = AIClient(
        api_key=config.API_KEY,
        api_url=config.API_URL,
        model=config.MODEL,
        system_prompt=feature.SYSTEM_PROMPT
    )
    client.connect_wifi(config.SSID, config.PASSWORD)

    agent = AIAgent(client, exec_env=exec_env)

    if on_ready:
        on_ready()

    print("System Ready! Type a command (or /reset):")

    # Generic command loop
    while True:
        user_input = input().strip()
        if user_input == "/reset":
            client.reset()
            print("Memory reset.")
        elif user_input:
            agent.step(user_input)

run(ACTIVE_FEATURE)
