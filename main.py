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
                print(f"[+] New Intel from {name}: {entry.title}")
                success = self.notifier.send(
                    title=f"[{name}] {entry.get('title')}",
                    summary=entry.get('summary', 'No summary.'),
                    link=current_link
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
        "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
        "KrebsOnSecurity": "https://krebsonsecurity.com/feed/",
        "ThreatPost": "https://threatpost.com/feed/",
        "NVD-Analyzed": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml",
        "Unit42": "https://unit42.paloaltonetworks.com/feed/",
        "CERT-CC": "https://www.kb.cert.org/vulfeed/",
        "ProjectZero": "https://googleprojectzero.blogspot.com/feeds/posts/default"
    }

    engine = NewsEngine(
        feeds=SOURCES,
        notifier=DiscordNotifier(WEBHOOK),
        state=StateManager()
    )
    engine.run()