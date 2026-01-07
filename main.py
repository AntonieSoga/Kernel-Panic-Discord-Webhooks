import os
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
    # Load Webhook Environment (GitHub Secrets)
    WEBHOOK = os.getenv('DISCORD_WEBHOOK') 

    # Initialize Components
    from src.fetcher import RSSFetcher # Added here for brevity
    
    engine = NewsEngine(
        fetcher=RSSFetcher("https://feeds.feedburner.com/TheHackersNews"),
        notifier=DiscordNotifier(WEBHOOK),
        state=StateManager()
    )
    engine.run()