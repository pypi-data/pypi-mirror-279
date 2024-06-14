import json
from typing import Dict

import requests

from tiktok_simple_scraper.entities import Account


def get_account_info(account_name: str) -> Account:
    url = f"https://www.tiktok.com/@{account_name}"

    payload = {}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'es,en-US;q=0.9,en;q=0.8,pt;q=0.7',
        'cache-control': 'max-age=0',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    j = _extract_json_html(response.text, "__UNIVERSAL_DATA_FOR_REHYDRATION__")
    # /__DEFAULT_SCOPE__/webapp.user-detail/userInfo/user/id
    ui = j["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]
    user: Dict = ui["user"]
    stats: Dict[str, int] = ui["stats"]
    return Account(
        name_to_show=user["uniqueId"],
        id=user["id"],
        sec_uid=user["secUid"],
        followers_count=stats["followerCount"],
        following_count=stats["followingCount"],
        heart_count=stats["heartCount"],
        video_count=stats["videoCount"],
        friend_count=stats["friendCount"],
        posts=[],
        title=user["nickname"],
        language=user["language"],
        url=f"https://www.tiktok.com/@{user['uniqueId']}",
        metadata=user,
        signature=user["signature"],
        avatar=user["avatarLarger"],
        bio_link=user.get("bio", {}).get("link", ""),
        region=user.get("region", "")
    )


def _extract_json_html(response: str, start_tag) -> dict:
    start_idx = response.find(start_tag)
    if start_idx == -1:
        return {}
    for _ in range(3):
        start_idx = response.find("{", start_idx)
        if start_idx == -1:
            return {}
    end_tag = "}</script>"
    end_idx = response.find(end_tag, start_idx)
    if end_idx == -1:
        return {}
    json_str = response[start_idx:end_idx+1].strip()
    return json.loads(json_str)
