import feedparser
import requests
import time
import re
from typing import Optional

class RSSFetcher:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    def fetch_latest(self) -> Optional[feedparser.FeedParserDict]:
        """
        Fetches the latest feed entries using requests for better stability.
        Includes a retry mechanism for transient network errors.
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                # Use requests to get the content manually
                # Timeout ensures the script doesn't hang forever
                response = requests.get(self.feed_url, timeout=15)
                
                # Check if the request was successful (200 OK)
                response.raise_for_status()
                
                # Parse the raw text content with feedparser
                feed = feedparser.parse(response.text)
                
                # Check if feedparser itself encountered an error
                if feed.bozo:
                    # Optional: Log bozo_exception if you want to see parsing issues
                    pass
                
                return feed

            except (requests.exceptions.RequestException, Exception) as e:
                # If we have retries left, wait and try again
                if attempt < max_retries - 1:
                    wait_time = 2 ** (attempt + 1)
                    print(f"[-] Attempt {attempt + 1} failed for {self.feed_url}: {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"[!] Permanent failure fetching {self.feed_url} after {max_retries} attempts.")
                    return None

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