import os
import time
from typing import List, Dict, Optional

import pandas as pd
import praw
from dotenv import load_dotenv

# settings you can change 
SUBREDDITS: List[str] = ["personalfinance", "investing", "stocks"]
PER_SUBREDDIT_LIMIT: int = 50
SEARCH_KEYWORD: Optional[str] = "index fund"   # set to None to skip search
ENV_CANDIDATES = [
    "reddit.env",  
    "/content/drive/MyDrive/Reddit_API/reddit.env",  
]
# -------------------------------------------

REQUIRED_COLUMNS = [
    "title","score","upvote_ratio","num_comments","author","subreddit",
    "url","permalink","created_utc","is_self","selftext","flair","domain","search_query"
]

def load_credentials() -> None:
    """Try loading env from common locations."""
    loaded = False
    for path in ENV_CANDIDATES:
        if os.path.exists(path):
            if load_dotenv(path, override=True):
                loaded = True
                print(f"[INFO] Loaded credentials from: {path}")
                break
    if not loaded:
        
        load_dotenv(override=True)
        print("[WARN] Could not find reddit.env file. "
              "Make sure to upload your real env in Colab or place it in the project folder.")

def get_reddit() -> praw.Reddit:
    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    missing = [k for k, v in {
        "REDDIT_CLIENT_ID": client_id,
        "REDDIT_CLIENT_SECRET": client_secret,
        "REDDIT_USER_AGENT": user_agent,
    }.items() if not v]
    if missing:
        raise RuntimeError(f"Missing required env vars: {', '.join(missing)}. "
                           f"Upload your real reddit.env and try again.")

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent,
    )
    return reddit

def row_from_submission(sub, search_query: Optional[str] = None) -> Dict:
    author_name = getattr(sub.author, "name", None) if sub.author else None
    selftext = (getattr(sub, "selftext", None) or "")
    selftext = selftext[:500] if selftext else None
    flair = getattr(sub, "link_flair_text", None)
    return {
        "title": getattr(sub, "title", None),
        "score": getattr(sub, "score", None),
        "upvote_ratio": getattr(sub, "upvote_ratio", None),
        "num_comments": getattr(sub, "num_comments", None),
        "author": author_name,
        "subreddit": str(getattr(sub, "subreddit", "")) if getattr(sub, "subreddit", None) else None,
        "url": getattr(sub, "url", None),
        "permalink": f"https://www.reddit.com{getattr(sub, 'permalink', '')}" if getattr(sub, "permalink", None) else None,
        "created_utc": int(getattr(sub, "created_utc", 0)) if getattr(sub, "created_utc", None) else None,
        "is_self": getattr(sub, "is_self", None),
        "selftext": selftext,
        "flair": flair,
        "domain": getattr(sub, "domain", None),
        "search_query": search_query,
    }

def ensure_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    for c in REQUIRED_COLUMNS:
        if c not in df.columns:
            df[c] = None
    return df[REQUIRED_COLUMNS]

def main():
    # 0) creds
    load_credentials()
    reddit = get_reddit()

    rows: List[Dict] = []

    # 1) Task 1 — fetch hot posts
    for sr in SUBREDDITS:
        try:
            for s in reddit.subreddit(sr).hot(limit=PER_SUBREDDIT_LIMIT):
                rows.append(row_from_submission(s))
            print(f"[INFO] Collected hot posts from r/{sr}")
        except Exception as e:
            print(f"[WARN] r/{sr} failed: {e}")
            time.sleep(2)

    # 2) Task 2 — keyword search with provenance
    if SEARCH_KEYWORD:
        target = "+".join(SUBREDDITS)
        try:
            for s in reddit.subreddit(target).search(SEARCH_KEYWORD, sort="relevance", limit=100):
                rows.append(row_from_submission(s, search_query=SEARCH_KEYWORD))
            print(f"[INFO] Search added results for '{SEARCH_KEYWORD}' across {target}")
        except Exception as e:
            print(f"[WARN] search failed: {e}")

    # 3) Task 3 — DataFrame, dedupe, save CSV
    df = pd.DataFrame(rows)
    df = ensure_required_columns(df)

    before = len(df)
    if "permalink" in df.columns:
        df = df.drop_duplicates(subset=["permalink"])
    else:
        df = df.drop_duplicates()
    after = len(df)
    print(f"[INFO] Deduplicated: {before - after} rows removed. Final rows: {after}")

    out_path = "/content/drive/MyDrive/Reddit_API/reddit_data.csv"
    df.to_csv(out_path, index=False)
    print(f"[INFO] Wrote {len(df)} rows to {out_path}")

if __name__ == "__main__":
    main()
