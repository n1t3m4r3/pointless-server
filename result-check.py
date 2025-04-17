import requests
import time
from difflib import *

def check_jee_mains_result(url, webhook_url, interval=30):
    oldtxt = requests.get(url, timeout=7).text
    while True:
        try:
            newtxt = requests.get(url, timeout=7).text
            if oldtxt != newtxt:
                    difftxt = ''.join(ndiff(oldtxt.splitlines(keepends=True),newtxt.splitlines(keepends=True)))
                    notify_discord(webhook_url, "The jee website has changed. Delta:\n```\n"+difftxt+'```\n')
                    oldtxt = newtxt
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
    DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1338562729916760146/gTlZwdMtUr0aMzF0VDCrkNX9k-WYxvLU9cYEQMFaaOEfLlQBbLytj40eBQiuFS3hdTXy"
    check_jee_mains_result(JEE_MAINS_URL, DISCORD_WEBHOOK_URL)
