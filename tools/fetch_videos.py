"""Collect the best-scoring Reddit videos per subreddit from the Arctic Shift archive.

Reddit itself blocks scripts (JSON and RSS both fail), so this uses the public
Arctic Shift API (https://github.com/ArthurHeitmann/arctic_shift). It pages
through every v.redd.it post of a subreddit, keeps the top ones by score and
checks that each video still plays.

Usage:
    py tools/fetch_videos.py out.json            # all subreddits below
    py tools/fetch_videos.py out.json parrots    # only some
Output: list of {id, type, title, sub, score, post} sorted by score,
the same shape as VIDEOS in index.html.
"""

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://arctic-shift.photon-reddit.com/api/posts/search"
UA = "paws-video-list/1.0 (+https://github.com/aq027a/paws-for-msnyx)"

SUBREDDITS = {
    "dog": ["rarepuppers", "puppies", "dogswithjobs", "corgi", "goldenretrievers", "WhatsWrongWithYourDog"],
    "cat": ["IllegallySmolCats", "Catswhoyell", "StartledCats", "kittens", "catvideos"],
    "bird": ["parrots", "budgies", "BirdsBeingDicks", "partyparrot", "cockatiel", "Corvids", "birding"],
}
TOP_PER_SUB = 25      # keep this many best videos per subreddit
MAX_PAGES = 400       # safety cap per subreddit (100 posts per page)
FIELDS = "id,score,title,created_utc,url,over_18,subreddit"


class GiveUp(Exception):
    pass


def get_json(url, tries=6):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
            if data.get("error"):
                raise RuntimeError(data["error"])
            return data["data"] or []
        except urllib.error.HTTPError as e:
            try:
                msg = json.load(e).get("error")
            except Exception:
                msg = e.reason
            if e.code == 400:  # bad parameter: retrying will not help
                raise GiveUp(msg)
            err = f"{e.code} {msg}"
        except (urllib.error.URLError, RuntimeError, TimeoutError, OSError) as e:
            err = str(e)
        wait = 10 * (i + 1)
        print(f"    retry in {wait}s ({err})", file=sys.stderr)
        time.sleep(wait)
    raise GiveUp(f"no answer for {url}")


def video_posts(sub):
    """Yield every v.redd.it post of a subreddit, newest first."""
    before = None
    for _ in range(MAX_PAGES):
        q = {"subreddit": sub, "url": "https://v.redd.it/", "limit": 100,
             "sort": "desc", "fields": FIELDS}
        if before:
            q["before"] = before
        try:
            page = get_json(API + "?" + urllib.parse.urlencode(q, safe=":/,"))
        except GiveUp as e:
            print(f"    stopped early in r/{sub}: {e}", file=sys.stderr)
            return
        if not page:
            return
        yield from page
        before = page[-1]["created_utc"]
        time.sleep(1.5)


def still_plays(vid):
    url = f"https://v.redd.it/{vid}/HLSPlaylist.m3u8"
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def best_of(sub, kind):
    seen = {}
    for p in video_posts(sub):
        if p.get("over_18"):
            continue
        vid = p["url"].rstrip("/").split("/")[-1]
        if vid not in seen or p["score"] > seen[vid]["score"]:
            seen[vid] = p
    print(f"  r/{sub}: {len(seen)} video posts", file=sys.stderr)
    out = []
    for p in sorted(seen.values(), key=lambda p: -p["score"]):
        vid = p["url"].rstrip("/").split("/")[-1]
        if not still_plays(vid):
            continue
        out.append({"id": vid, "type": kind, "title": p["title"], "sub": p["subreddit"],
                    "score": p["score"], "post": f"https://www.reddit.com/r/{p['subreddit']}/comments/{p['id']}/"})
        if len(out) >= TOP_PER_SUB:
            break
    return out


def main():
    out_path = sys.argv[1]
    only = set(a.lower() for a in sys.argv[2:])
    result = []
    for kind, subs in SUBREDDITS.items():
        for sub in subs:
            if only and sub.lower() not in only:
                continue
            print(f"{kind}: r/{sub}", file=sys.stderr)
            result += best_of(sub, kind)
    result.sort(key=lambda v: -v["score"])
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"saved {len(result)} videos to {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
