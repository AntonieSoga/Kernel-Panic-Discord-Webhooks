import requests
from .interfaces import Notifier

class DiscordNotifier(Notifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.color = 0x00FF41  # Terminal Green

    def send(self, title: str, summary: str, link: str):
        payload = {
            "embeds": [{
                "title": f"🛰️ Intel: {title}",
                "url": link,
                "description": (summary[:500] + '...') if len(summary) > 500 else summary,
                "color": self.color,
                "footer": {"text": "R00T_CAUSE // Automated Feed"}
            }]
        }
        res = requests.post(self.webhook_url, json=payload)
        return res.status_code == 204