# Paws for MsNyx – project notes

Single-file static site (`index.html`) published with GitHub Pages from `main` (repo aq027a/paws-for-msnyx). The owner talks German; the site itself is English with a Romanian (RO) switch.

## What it is
- Gift page for "MsNyx": swipe cards (right = favourite, left = next), undo, Dogs/Cats filter, favourites sheet, EN/RO language switch (remembered in localStorage).
- First card is always a personal welcome card (`__intro`, photo `intro.jpg`) with a message for the days she feels down. It never becomes a favourite and only appears on page load.
- Look: single dark theme, dark purple + dark green (her colours), crescent-moon logo (Nyx = goddess of night). Fonts: Fraunces (display), Nunito (body).

## Videos
- 98 videos (29 dogs, 69 cats) from top-of-all-time posts in r/aww, r/rarepuppers, r/puppies, r/IllegallySmolCats, r/Catswhoyell (r/kittens top 100 had no videos). Non-dog/cat posts were removed by hand.
- Data is inline in `index.html` as `const VIDEOS = [...]` with `id` (v.redd.it id), `type` (dog/cat), `title` (original Reddit title, not translated), `sub`, `score`, `post`.
- Playback: `https://v.redd.it/<id>/HLSPlaylist.m3u8` via hls.js 1.5.13 from cdnjs (native HLS on Safari). v.redd.it sends `Access-Control-Allow-Origin: *`.
- The list was fetched with the Apify actor `automation-lab/reddit-scraper` (sort=top, timeFilter=all, 100 per subreddit). Direct reddit.com requests are blocked without login/API token; Agent Reach did not work either.
- Videos belong to their Reddit uploaders: hotlink only, never download and re-host them.

## Editing
- Preview: open `index.html` directly or run `py -m http.server 8765` (Windows) / `python3 -m http.server 8765`.
- UI strings live in the `T` object (`en` / `ro`). Keep both languages in sync.
- Favourites are stored under localStorage key `nyx-favs-reddit`.
- The repo is public: don't commit anything private. Strip EXIF from any new photo before committing.
