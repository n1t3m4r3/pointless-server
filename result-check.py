import requests
import time

def check_jee_mains_result(url, webhook_url, interval=30):
    x1 = requests.get(url, timeout=7)
    x2 = x1.text
    while True:
        try:
            y1 = requests.get(url, timeout=7)
            y2 = y1.text
            if x2 != y2:
                    notify_discord(webhook_url, "website change")
                    time.sleep(60)
            else:
                print("no change")
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
    JEE_MAINS_URL = "https://jeemain.nta.nic.in/#1648447930282-deb48cc0-95ec"
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/912965858198949918/LEjxLyA9OP51xgRYqSufxCDCTi-6zvOXmqfoUq0_YF0Gp68CcBEmzoAcJnA8ulpzfXYT"
    check_jee_mains_result(JEE_MAINS_URL, DISCORD_WEBHOOK_URL)
