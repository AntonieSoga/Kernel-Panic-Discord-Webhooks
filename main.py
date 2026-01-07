import os
import configparser
from src.fetcher import RSSFetcher
from src.notifier import DiscordNotifier
from src.state_manager import StateManager

class NewsEngine:
    def __init__(self, fetcher, notifier, state):
        self.fetcher = fetcher
        self.notifier = notifier
        self.state = state

    def run(self):
        entry = self.fetcher.fetch_latest()
        if not entry:
            return

        last_link = self.state.get_last_link()
        current_link = entry.get('link')

        if current_link != last_link:
            print(f"[+] New Intel Found: {entry.title}")
            success = self.notifier.send(
                title=entry.get('title'),
                summary=entry.get('summary', 'No summary.'),
                link=current_link
            )
            if success:
                self.state.update_last_link(current_link)
        else:
            print("[-] No new updates since last check.")

if __name__ == "__main__":
    # Load Webhook from Config or Environment (GitHub Secrets)
    config = configparser.ConfigParser()
    config.read('.config.cfg')
    
    WEBHOOK = os.getenv('DISCORD_WEBHOOK') 
    if not WEBHOOK:
        try:
            WEBHOOK = config.get('DISCORD', 'webhook_url').strip('"')
        except:
            print("Critical: No Webhook URL found.")
            exit(1)

    # Initialize Components
    from src.fetcher import RSSFetcher # Added here for brevity
    
    engine = NewsEngine(
        fetcher=RSSFetcher("https://feeds.feedburner.com/TheHackersNews"),
        notifier=DiscordNotifier(WEBHOOK),
        state=StateManager()
    )
    engine.run()