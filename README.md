# Paws for MsNyx

A Tinder-style swipe page with the cutest dog and cat videos on Reddit, made as a gift for MsNyx.

Live: https://aq027a.github.io/paws-for-msnyx/

## Work on it on another computer

```bash
git clone https://github.com/aq027a/paws-for-msnyx.git
cd paws-for-msnyx
```

Look at it locally (any of these works):

- Double-click `index.html`, or
- Windows: `py -m http.server 8765`, macOS/Linux: `python3 -m http.server 8765`, then open http://localhost:8765

Publish a change: commit and push to `main`. GitHub Pages updates the live link within 1–2 minutes.

```bash
git add -A
git commit -m "Describe the change"
git push
```

## Files

- `index.html` – the whole app (HTML, CSS, JS and the video list in one file)
- `intro.jpg` – photo on the welcome card (metadata stripped)
