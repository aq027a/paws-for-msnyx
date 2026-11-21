# Paws for MsNyx – project notes

Single-file static site (`index.html`) published with GitHub Pages from `main` (repo aq027a/paws-for-msnyx). The owner talks German; the site itself is English with a Romanian (RO) switch.

## What it is
- Gift page for "MsNyx": swipe cards (right = favourite, left = next), undo, Dogs/Cats/Birds filter, favourites sheet, EN/RO language switch (remembered in localStorage).
- First card is always a personal welcome card (`__intro`, photo `intro.jpg`) with a message for the days she feels down. It never becomes a favourite and only appears on page load.
- Look: single dark theme, dark purple + dark green (her colours), crescent-moon logo (Nyx = goddess of night). Fonts: Fraunces (display), Nunito (body).

## Videos
- 409 videos (98 dogs, 182 cats, 129 birds), all top-of-all-time posts. Filters: All / Dogs / Cats / Birds.
  - Dogs: r/aww, r/rarepuppers, r/puppies, r/WhatsWrongWithYourDog, r/dogswithjobs, r/goldenretrievers, r/corgi
  - Cats: r/IllegallySmolCats, r/Catswhoyell, r/StartledCats (top 40 only), r/catvideos (top 35 only), r/MEOW_IRL
  - Birds: r/parrots, r/PartyParrot, r/budgies, r/BirdsBeingDicks, r/cockatiel (r/Corvids and r/birding were not reached by the run)
  - Removed by hand: sad posts (RIP, last video, abandoned/kicked out), wrong animal, ads, rude titles. Every video was checked to still play.
- Data is inline in `index.html` as `const VIDEOS = [...]` with `id` (v.redd.it id), `type` (dog/cat/bird), `title` (original Reddit title, not translated), `sub`, `score`, `post`.
- Playback: `https://v.redd.it/<id>/HLSPlaylist.m3u8` via hls.js 1.5.13 from cdnjs (native HLS on Safari). v.redd.it sends `Access-Control-Allow-Origin: *`.
- How the list is fetched: Apify actor `automation-lab/reddit-scraper` (sort=top, timeFilter=all, 100 per subreddit, NSFW off, ~$2 per run of 18 subreddits).
- What does NOT work (tested 2026-11-21 on Windows): Agent Reach / rdt-cli (Reddit answers "403 Blocked" even with a fresh Firefox login; Chrome cookies need admin and still fail), Reddit RSS feeds (404 "Not Found" for scripts), opening reddit.com in Claude in Chrome or the app browser (blocked by safety rules).
- Work in progress: `tools/fetch_videos.py` gets videos from the Arctic Shift archive API instead (no Reddit access needed). Arctic Shift cannot sort by score, so it pages through all v.redd.it posts of a subreddit (100 per page) and sorts locally; it is slow and the API often times out on deep pages. Scores of recent posts are frozen at archive time (often 1). Not used for the current list yet.
- Videos belong to their Reddit uploaders: hotlink only, never download and re-host them.

## Editing
- Preview: open `index.html` directly or run `py -m http.server 8765` (Windows) / `python3 -m http.server 8765`.
- UI strings live in the `T` object (`en` / `ro`). Keep both languages in sync.
- Favourites are stored under localStorage key `nyx-favs-reddit`.
- The repo is public: don't commit anything private. Strip EXIF from any new photo before committing.
