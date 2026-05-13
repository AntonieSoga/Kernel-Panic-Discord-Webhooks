import re
import os
from src.fetcher import RSSFetcher
from src.notifier import DiscordNotifier
from src.state_manager import StateManager
from bs4 import BeautifulSoup

class NewsEngine:
    def __init__(self, feeds: dict, notifier: DiscordNotifier, state: StateManager, unit_name: str = "SECURITY"):
        self.feeds = feeds 
        self.notifier = notifier
        self.state = state
        self.unit_name = unit_name

    def run(self):
        print(f"[*] Starting update for {self.unit_name} Unit...")
        for name, url in self.feeds.items():
            fetcher = RSSFetcher(url)
            entry = fetcher.fetch_latest()
            
            if not entry:
                continue

            last_link = self.state.get_last_link(name)
            current_link = entry.get('link')

            if not current_link or not isinstance(current_link, str):
                print(f"[-] Invalid link format for {name}, skipping state update.")
                continue

            if current_link != last_link:
                image_url = fetcher.extract_image(entry)
                
                # Handling summary extraction safely
                raw_summary = entry.get('summary', entry.get('description', 'No description available.'))
                clean_summary = BeautifulSoup(raw_summary, 'html.parser').get_text()

                success = self.notifier.send(
                    title=entry.get('title'),
                    summary=clean_summary,
                    link=current_link,
                    image_url=image_url,
                    source_name=name
                )
                
                if success:
                    print(f"[+] Notified: {name}")
                    self.state.update_last_link(name, current_link)
            else:
                print(f"[-] No new updates for {name}.")

if __name__ == "__main__":
    # Load Webhooks from Environment
    SEC_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
    DS_WEBHOOK = os.getenv('DS_WEBHOOK') 

    # Check at least one exists
    if not SEC_WEBHOOK and not DS_WEBHOOK:
        print("Critical: No Webhook URLs found.")
        exit(1)

    state = StateManager()

    # 1. SECURITY INTELLIGENCE SOURCES
    if SEC_WEBHOOK:
        SEC_SOURCES = {
            "TheHackerNews": "https://feeds.feedburner.com/TheHackersNews",
            "ThreatPost": "https://threatpost.com/feed/",
            "NVD-Analyzed": "https://nvd.nist.gov/feeds/xml/cve/misc/nvd-rss-analyzed.xml",
            "Unit42": "https://unit42.paloaltonetworks.com/feed/",
            "CERT-CC": "https://www.kb.cert.org/vulfeed/",
        }
        sec_engine = NewsEngine(
            feeds=SEC_SOURCES,
            notifier=DiscordNotifier(SEC_WEBHOOK),
            state=state,
            unit_name="SECURITY"
        )
        sec_engine.run()

    # 2. DATA SCIENCE SOURCES
    if DS_WEBHOOK:
        DS_SOURCES = {
            "KDnuggets": "https://www.kdnuggets.com/feed",
            "DataScienceCentral": "https://www.datasciencecentral.com/feed/",
            "TowardsDataScience": "https://towardsdatascience.com/feed",
            "MachineLearningMastery": "https://machinelearningmastery.com/feed/",
            "Reddit-DataScience": "https://www.reddit.com/r/datascience/.rss"
        }
        ds_engine = NewsEngine(
            feeds=DS_SOURCES,
            notifier=DiscordNotifier(DS_WEBHOOK),
            state=state,
            unit_name="DATA_SCIENCE"
        )
        ds_engine.run()