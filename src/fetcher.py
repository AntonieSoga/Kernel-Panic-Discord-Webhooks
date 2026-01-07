import feedparser

class RSSFetcher:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_latest(self):
        """Returns the most recent entry from the feed."""
        feed = feedparser.parse(self.feed_url)
        if not feed.entries:
            return None
        return feed.entries[0]