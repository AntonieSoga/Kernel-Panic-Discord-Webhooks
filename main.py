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
            
            # 1. Skip if fetcher returned None (due to network error or empty feed)
            if not entry:
                continue

            last_link = self.state.get_last_link(name)
            current_link = entry.get('link')

            # 2. Safety Check: Ensure current_link is actually a string and not None/Empty
            if not current_link or not isinstance(current_link, str):
                print(f"[-] Invalid link format for {name}, skipping state update.")
                continue

            if current_link != last_link:
                image_url = fetcher.extract_image(entry)
                clean_summary = re.sub('<[^<]+?>', '', entry.get('summary', ''))

                success = self.notifier.send(
                    title=entry.get('title'),
                    summary=clean_summary,
                    link=current_link,
                    image_url=image_url,
                    source_name=name
                )
                # 3. Only update state if notification was successful AND link is valid
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