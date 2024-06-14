import logging
import os
import time
from datetime import datetime
from typing import List

import requests

from tiktok_simple_scraper.account import get_account_info
from tiktok_simple_scraper.entities import ScraperOptions, Account, SocialMedia, Post, Reaction, \
    ReactionType, PostType, Comment
from tiktok_simple_scraper.mstoken import MsTokenTikTok
from tiktok_simple_scraper.verify_fp import VerifyFp
from tiktok_simple_scraper.x_bogus import XBogus

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

logger = logging.getLogger(__name__)


class TikTokAccountScraper:

    def __init__(self, ms_token: str):
        self._ms_token = ms_token

    def scrape(self, account_id: str, options: ScraperOptions) -> Account:
        options.callbacks.on_account_scrape_start(SocialMedia.TIKTOK, account_id)
        os.environ['REQUESTS_CA_BUNDLE'] = ''  # Disable SSL verification
        raw_post_list = self._get_raw_posts(account_id, self._ms_token)
        posts: List[Post] = []
        for raw_post in raw_post_list["itemList"]:
            date = datetime.fromtimestamp(raw_post["createTime"])
            if date < options.most_old_date:
                break
            post_id = raw_post["id"]
            user_id = raw_post["author"]["id"]
            options.callbacks.on_get_comments_start(SocialMedia.TIKTOK, post_id)
            comments = self._get_post_comments(post_id, user_id)
            likes = int(raw_post["statsV2"]["diggCount"])
            options.callbacks.on_get_comments_ends(SocialMedia.TIKTOK, post_id, comments)
            post = Post(
                id=post_id,
                date=date,
                reactions=[
                    Reaction(
                        type=ReactionType.LIKE,
                        count=likes
                    )
                ],
                url=raw_post["id"],
                comments=comments,
                hashtags=[],
                type=PostType.VIDEO,
                reaction_count=likes,
                text=raw_post["desc"],
                view_count=int(raw_post["stats"]["playCount"]),
                share_count=int(raw_post["stats"]["shareCount"])
            )
            posts.append(post)
            options.callbacks.on_new_post(SocialMedia.TIKTOK, post)
        author = raw_post_list["itemList"][0]["author"]
        acc = get_account_info(author['uniqueId'])
        acc.posts = posts
        options.callbacks.on_account_scrape_end(SocialMedia.TIKTOK, acc)
        return acc

    def _get_raw_posts(self, company_id: str, ms_token: str, attempt: int = 1) -> dict:
        params = {
            "WebIdLastTime": int(time.time()),
            "aid": "1988",
            "app_language": "es",
            "app_name": "tiktok_web",
            "browser_language": "es",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "MacIntel",
            "browser_version": USER_AGENT,
            "channel": "tiktok_web",
            "cookie_enabled": "true",
            "count": "35",
            "coverFormat": "2",
            "cursor": "0",
            "device_id": "7365570092849071622",
            "device_platform": "web_pc",
            "focus_state": "true",
            "from_page": "user",
            "history_len": "5",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "language": "es",
            "os": "mac",
            "priority_region": "CL",
            "referer": "https//:www.tiktok.com/discover/santander-chile?lang=es",
            "region": "CL",
            "root_referer": "https//:www.google.com/",
            "screen_height": "1692", "screen_width": "3008",
            "secUid": company_id,
            "tz_name": "America%2FSantiago",
            "webcast_language": "es",
            "msToken": ms_token,
            "verifyFp": VerifyFp.get_verify_fp()
        }
        x_bogus = XBogus().get_x_bogus(query=params)
        params["X-Bogus"] = x_bogus
        url = "https://www.tiktok.com/api/post/item_list/"
        try:
            response = requests.request("GET", url, headers=MsTokenTikTok.HEADERS, params=params, verify=False)
            return response.json()
        except Exception as e:
            logger.error(f"TIKTOK: Error getting posts from TikTok: {e}")
            if attempt > 3:
                raise e
            time.sleep(60)
            self._get_raw_posts(company_id, ms_token, attempt + 1)

    @staticmethod
    def _get_post_comments(post_id: str, user_id: str) -> List[Comment]:
        url = f"https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={post_id}&count=9999999&cursor=0"
        payload = {}
        headers = {
            'user-agent': USER_AGENT,
            'referer': 'https://www.tiktok.com/@x/video/7356625715825036549'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        comments_resp = response.json()
        if "comments" not in comments_resp or comments_resp["comments"] is None:
            return []
        comments: List[Comment] = []
        for raw_comment in comments_resp["comments"]:
            comment_id = raw_comment["cid"]
            if comment_id == user_id:
                continue
            creation_date_epoch = raw_comment["create_time"]
            creation_date = datetime.fromtimestamp(creation_date_epoch)
            comment: Comment = Comment(
                text=raw_comment["text"],
                user=raw_comment["user"]['unique_id'],
                user_metadata={
                    "sec_uid": raw_comment["user"]['sec_uid'],
                    "id": raw_comment["user"]['uid'],
                },
                user_name=raw_comment["user"]['nickname'],
                url=raw_comment["cid"],
                date=creation_date,
                reactions=[
                    Reaction(
                        type=ReactionType.LIKE,
                        count=raw_comment["digg_count"]
                    )
                ],
                replies=[],
                sentiments=None
            )
            comments.append(comment)
        return comments
