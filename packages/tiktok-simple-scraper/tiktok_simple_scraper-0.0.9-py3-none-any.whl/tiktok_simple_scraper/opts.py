import logging
import os
from datetime import datetime, timedelta
from typing import List

from tiktok_simple_scraper.entities import ScraperOptions, ScrapeCallbacks, SocialMedia, Account, Post, Comment

logger = logging.getLogger(__name__)


class LogCallbacks(ScrapeCallbacks):

    def on_success_login(self) -> None:
        logger.info('Login successful')

    def on_account_scrape_start(self, social_media: SocialMedia, account_id: str) -> None:
        logger.info(f'{social_media.value} START Scraping account {account_id}')

    def on_account_scrape_end(self, social_media: SocialMedia, account: Account) -> None:
        logger.info(f'{social_media.value} END Scraped account {account.id}')

    def on_new_post(self, social_media: SocialMedia, post: Post) -> None:
        logger.info(f'{social_media.value} New post: {post.url}')

    def on_get_comments_start(self, social_media: SocialMedia, post_id: str, page: int = 0) -> None:
        logger.info(f'{social_media.value} START Getting comments for post(page:{page}) {post_id} ')

    def on_get_comments_ends(self, social_media: SocialMedia, post_id: str, comments: List[Comment]) -> None:
        logger.info(f'{social_media.value} Got {len(comments)} END comments for post {post_id}')


def build_default_opts() -> ScraperOptions:
    cache_path = '../../../cache'
    try:
        os.mkdir(cache_path)
    except FileExistsError:
        pass
    return ScraperOptions(
        most_old_date=datetime.now() - timedelta(days=3 * 30),
        max_comments_per_post=1000,
        callbacks=LogCallbacks(),
        check_account_in_storage=True,
    )
