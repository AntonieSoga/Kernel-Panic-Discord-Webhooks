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
        self.op_statuses = [
            "INTEL_SYNC_COMPLETE",
            "PACKET_INSPECTION_SUCCESS",
            "RECON_BUFFER_UPDATED",
            "SIGNAL_STRENGTH_NOMINAL",
            "UPLINK_ESTABLISHED",
            "DATA_MODELS_SYNCHRONIZED"
        ]

    def _get_random_color(self):
        return random.choice(self.cool_colors)

    def _get_dynamic_footer(self, source):
        status = random.choice(self.op_statuses)
        return f"R00T_CAUSE // SOURCE: {source.upper()} // {status}"

    def send(self, title: str, summary: str, link: str, image_url: str = None, source_name: str = "Unknown"):
        embed_color = self._get_random_color()
        footer_text = self._get_dynamic_footer(source_name)
        
        # Determine Unit Name for visual flair
        # If the source is in the DS list, we label it Data Science
        unit_type = "DATA SCIENCE UNIT" if any(ds in source_name for ds in ["KDnuggets", "Towards", "Machine", "Reddit"]) else "SECURITY INTELLIGENCE UNIT"

        payload = {
            "embeds": [{
                "author": {
                    "name": unit_type,
                    "icon_url": "https://cdn-icons-png.flaticon.com/512/9963/9963277.png"
                },
                "title": f"**{title}**",
                "url": link,
                "description": f"**{summary[:450]}...**" if len(summary) > 450 else f"**{summary}**",
                "color": embed_color,
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