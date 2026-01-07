import feedparser
import re

class RSSFetcher:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_latest(self):
        feed = feedparser.parse(self.feed_url)
        if not feed.entries:
            return None
        return feed.entries[0]

    def extract_image(self, entry):
        """Attempts to find an image URL in common RSS locations."""
        # 1. Check for media content tags
        if 'media_content' in entry:
            return entry.media_content[0]['url']
        
        # 2. Check for links with image types
        if 'links' in entry:
            for link in entry.links:
                if 'image' in link.get('type', ''):
                    return link.get('href')

        # 3. Regex search in the summary/content for <img> tags
        content = entry.get('summary', '') + entry.get('description', '')
        img_match = re.search(r'<img [^>]*src="([^"]+)"', content)
        if img_match:
            return img_match.group(1)
            
        return None