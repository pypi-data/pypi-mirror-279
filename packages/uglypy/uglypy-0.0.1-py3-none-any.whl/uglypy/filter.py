import logging
from datetime import datetime, timedelta
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentFilter:
    def __init__(self, max_age_days: int):
        self.max_age_days = max_age_days

    def filter_content(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        for article in articles:
            if 'published' not in article or not article['published']:
                # Treat as fresh and set the aggregation date to current date
                article['published'] = datetime.now().strftime("%Y-%m-%d")
                logger.debug(f"Article '{article['title']}' has no date, treating as fresh with current date.")
        
        filtered_articles = [article for article in articles if self.is_fresh(article)]
        return filtered_articles

    def is_fresh(self, article: Dict[str, str]) -> bool:
        # Check if the article is within the max age days
        try:
            publish_date = datetime.strptime(article['published'], "%Y-%m-%d")
            age = datetime.now() - publish_date
            is_fresh = age <= timedelta(days=self.max_age_days)
            logger.debug(f"Article '{article['title']}' published on {article['published']} is {'fresh' if is_fresh else 'old'}.")
            return is_fresh
        except ValueError:
            logger.error(f"Error parsing date for article '{article['title']}': {article['published']}")
            return False

def filter_old_items(articles: List[Dict[str, str]], max_age_days: int) -> List[Dict[str, str]]:
    content_filter = ContentFilter(max_age_days)
    filtered_articles = content_filter.filter_content(articles)
    logger.info(f"Filtered down to {len(filtered_articles)} articles from {len(articles)} based on age.")
    return filtered_articles

