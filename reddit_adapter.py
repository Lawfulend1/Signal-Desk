"""Review excerpt from Signal Desk. Read-only; disabled without approved permission."""
import json
import os
import time
from datetime import datetime
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from features import UTC, stamp

def get_json(url, headers):
    # Never log authentication headers or response bodies on failures.
    for attempt in range(3):
        try:
            with urlopen(Request(url, headers=headers), timeout=30) as response:
                return json.load(response)
        except HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 2:
                delay = e.headers.get("Retry-After", "2")
                time.sleep(min(10, float(delay) if delay.isdigit() else 2**attempt))
                continue
            raise RuntimeError(f"Data provider HTTP {e.code}; check access and quota") from None
    raise RuntimeError("Data provider unavailable")

class Reddit:
    def collect(self, config):
        if not config.get("reddit_permitted"):
            raise ValueError("Reddit disabled: obtain approved API access and permitted research use before enabling")
        token, user_agent = os.environ.get("REDDIT_ACCESS_TOKEN"), os.environ.get("REDDIT_USER_AGENT")
        if not token or not user_agent:
            raise ValueError("Set REDDIT_ACCESS_TOKEN and identifying REDDIT_USER_AGENT")
        posts = []
        for subreddit in config["subreddits"]:
            if not subreddit.replace("_", "").isalnum():
                raise ValueError("Invalid subreddit")
            result = get_json("https://oauth.reddit.com/r/"+subreddit+"/new?limit=100&raw_json=1",
                              {"Authorization": "Bearer "+token, "User-Agent": user_agent})
            observed = stamp(datetime.now(UTC))
            for item in result["data"]["children"]:
                p = item["data"]
                if p.get("removed_by_category") or p.get("selftext") in ("[removed]", "[deleted]"):
                    continue
                posts.append({"id": p["name"], "source": "reddit:"+subreddit,
                              "text": p.get("title", "")+" "+p.get("selftext", ""),
                              "created_at": stamp(datetime.fromtimestamp(p["created_utc"], UTC)), "observed_at": observed})
            time.sleep(2)
        return posts
