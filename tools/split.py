"""Split a single-file HTML (with base64 data URIs) into index.html + media/ files.
Usage: python3 -I split.py <source.html> <out_dir>
"""
import base64, hashlib, os, re, sys

EXT = {"image/jpeg": "jpg", "image/png": "png", "image/svg+xml": "svg", "video/mp4": "mp4",
       "image/webp": "webp", "image/gif": "gif"}

src, out = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(out, "media"), exist_ok=True)
data = open(src, "rb").read().decode("utf-8")
pat = re.compile(r'data:([a-z]+/[a-z0-9+.-]+);base64,([A-Za-z0-9+/=\s]+)')
seen = {}

def repl(m):
    mime, b64 = m.group(1), m.group(2)
    if len(b64) < 2000:  # keep tiny inline assets inline
        return m.group(0)
    raw = base64.b64decode(re.sub(r"\s", "", b64))
    h = hashlib.sha1(raw).hexdigest()[:10]
    if h not in seen:
        name = f"media/{h}.{EXT.get(mime, 'bin')}"
        open(os.path.join(out, name), "wb").write(raw)
        seen[h] = name
    return seen[h]

html = pat.sub(repl, data)
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(html)
print(f"index.html: {len(html.encode())/1024:.0f} KB, media files: {len(seen)}")
