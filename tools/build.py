"""Pack index.html + media/ back into a single self-contained HTML file.
Usage: python3 -I build.py <deck_dir> <output.html>
"""
import base64, os, re, sys

MIME = {"jpg": "image/jpeg", "png": "image/png", "svg": "image/svg+xml", "mp4": "video/mp4",
        "webp": "image/webp", "gif": "image/gif"}

d, out = sys.argv[1], sys.argv[2]
html = open(os.path.join(d, "index.html"), encoding="utf-8").read()

def repl(m):
    path = m.group(0)
    raw = open(os.path.join(d, path), "rb").read()
    return f"data:{MIME[path.rsplit('.', 1)[1]]};base64," + base64.b64encode(raw).decode()

html = re.sub(r"media/[0-9a-f]{10}\.[a-z0-9]+", repl, html)
open(out, "w", encoding="utf-8").write(html)
print(f"{out}: {os.path.getsize(out)/1e6:.1f} MB")
