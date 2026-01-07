import requests
import datetime
import random
from .interfaces import Notifier

class DiscordNotifier(Notifier):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        self.cool_colors = [
            0x00FF41, # Matrix Green
            0x00FFFF, # Cyan
            0xFF0055, # Cyberpunk Pink
            0xFFBF00, # Amber
            0x9D00FF, # Deep Purple
            0xFF4500  # Alert Orange
        ]
        # Operation statuses
        self.op_statuses = [
            "INTEL_SYNC_COMPLETE",
            "PACKET_INSPECTION_SUCCESS",
            "RECON_BUFFER_UPDATED",
            "SIGNAL_STRENGTH_NOMINAL",
            "UPLINK_ESTABLISHED"
        ]

    def _get_random_color(self):
        return random.choice(self.cool_colors)

    def _get_dynamic_footer(self, source):
        # Combines the specific feed name with a random operational status
        status = random.choice(self.op_statuses)
        return f"R00T_CAUSE // SOURCE: {source.upper()} // {status}"

    def send(self, title: str, summary: str, link: str, image_url: str = None, source_name: str = "Unknown"):
        embed_color = self._get_random_color()
        footer_text = self._get_dynamic_footer(source_name)

        payload = {
            "embeds": [{
                "author": {
                    "name": f"SECURITY INTELLIGENCE UNIT",
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/9963/9963277.png"
                },
                # Bold Title
                "title": f"**{title}**",
                "url": link,
                # Bold Description for high contrast
                "description": f"**{summary[:450]}...**" if len(summary) > 450 else f"**{summary}**",
                "color": embed_color,
                # Large image display
                "image": {
                    "url": image_url if image_url else ""
                },
                "footer": {
                    "text": footer_text,
                },
                "timestamp": datetime.datetime.now().isoformat()
            }]
        }
        
        res = requests.post(self.webhook_url, json=payload)
        return res.status_code == 204