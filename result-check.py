import requests
import time

def check_jee_mains_result(url, webhook_url, interval=5):
    """Checks the JEE Mains result website and notifies via Discord webhook when available."""
    while True:
        try:
            response = requests.get(url, timeout=60)
            if response.status_code != 500:
                    notify_discord(webhook_url, "website change")
            else:
                print("Still showing 'Internal Server Error', retrying...")
        except requests.RequestException as e:
            print(f"Request failed: {e}, retrying...")
        
        time.sleep(interval)  # Wait before retrying

def notify_discord(webhook_url, message):
    """Sends a message to a Discord webhook."""
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 204:
            print("Notification sent successfully.")
        else:
            print(f"Failed to send notification. Response code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Failed to send Discord notification: {e}")

if __name__ == "__main__":
    JEE_MAINS_URL = "https://jeemain.nta.nic.in/results-for-jeemain-2025-session-1/link"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/912965858198949918/LEjxLyA9OP51xgRYqSufxCDCTi-6zvOXmqfoUq0_YF0Gp68CcBEmzoAcJnA8ulpzfXYT"
    check_jee_mains_result(JEE_MAINS_URL, DISCORD_WEBHOOK_URL)
