import re
import os
from src.fetcher import RSSFetcher
from src.notifier import DiscordNotifier
from src.state_manager import StateManager

class NewsEngine:
    def __init__(self, feeds: dict, notifier: DiscordNotifier, state: StateManager):
        self.feeds = feeds # Dictionary of { "Name": "URL" }
        self.notifier = notifier
        self.state = state

    def run(self):
        for name, url in self.feeds.items():
            fetcher = RSSFetcher(url)
            entry = fetcher.fetch_latest()
            
            if not entry:
                continue

            last_link = self.state.get_last_link(name)
            current_link = entry.get('link')

            if current_link != last_link:
                # Extract image for better visuals
                image_url = fetcher.extract_image(entry)
                
                # Clean HTML tags from summary (common in RSS)
                clean_summary = re.sub('<[^<]+?>', '', entry.get('summary', ''))

                success = self.notifier.send(
                    title=entry.get('title'),
                    summary=clean_summary,
                    link=current_link,
                    image_url=image_url,
                    source_name=name
                )
                if success:
                    self.state.update_last_link(name, current_link)
            else:
                print(f"[-] No new updates for {name}.")

if __name__ == "__main__":
    WEBHOOK = os.getenv('DISCORD_WEBHOOK') 
    if not WEBHOOK:
        print("Critical: No Webhook URL found.")
        exit(1)

    # Define your intelligence sources here
    SOURCES = {
        "TheHackerNews": "https://feeds.feedburner.com/TheHackersNews",
        "KrebsOnSecurity": "https://krebsonsecurity.com/feed/",
        "ThreatPost": "https://threatpost.com/feed/",
        "NVD-Analyzed": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml",
        "Unit42": "https://unit42.paloaltonetworks.com/feed/",
        "CERT-CC": "https://www.kb.cert.org/vulfeed/",
    }

    engine = NewsEngine(
        feeds=SOURCES,
        notifier=DiscordNotifier(WEBHOOK),
        state=StateManager()
    )
    engine.run()