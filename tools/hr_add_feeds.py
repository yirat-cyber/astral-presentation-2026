"""Insert an Instagram feed before/after slide right after the hero (slide 2).
Usage: python3 -I tools/hr_add_feeds.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-feeds"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

def col(tag, handle, img, alt, points, cls):
    lis = "".join(f"<li>{p}</li>" for p in points)
    return (f'<figure class="feed-col {cls}"><figcaption><span class="feed-tag">{tag}</span>'
            f'<span class="feed-handle">@{handle}</span></figcaption>'
            f'<div class="feed-phone"><img src="{img}" alt="{alt}"></div><ul>{lis}</ul></figure>')

old = col("לפני", "astral_eilat_careers", "media/9ca888fa6c.jpg", "הפיד הקודם באינסטגרם",
          ["תמונות סטוק ותוכן כללי", "ימים בינלאומיים וברכות יום הולדת", "כמעט בלי עובדים אמיתיים"], "feed-old")
new = col("היום", "work_at_astral", "media/266e9ea726.jpg", "הפיד הנוכחי באינסטגרם",
          ["עובדים אמיתיים כמעט בכל פוסט", "סיפורי קידום והכוכבים של אסטרל", "רילס ותוכן מהשטח"], "feed-new")

slide = f'''<section class="slide sand hrx" id="hr-feeds" data-dot="יישור קו · הפיד">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">יישור קו · האינסטגרם</div>
<h2 class="reveal d1">מאיפה התחלנו</h2>
<div class="feeds reveal d2">{new}<span class="feeds-arrow" aria-hidden="true">←</span>{old}</div>
</div></section>'''

CSS = '''<style>
/* ===== HR · feeds before/after ===== */
#hr-feeds{padding-top:96px;padding-bottom:40px}
#hr-feeds h2{font-size:clamp(30px,3.2vw,46px)}
.hrx .feeds{display:flex;flex-direction:row-reverse;justify-content:center;align-items:flex-start;gap:clamp(24px,4vw,64px);margin-top:18px}
.hrx .feed-col{margin:0;display:flex;flex-direction:column;align-items:center;gap:10px}
.hrx .feed-col figcaption{display:flex;align-items:baseline;gap:10px}
.hrx .feed-tag{font-weight:800;font-size:18px;color:#0b1622}
.hrx .feed-new .feed-tag{color:#95743b}
.hrx .feed-handle{font-size:13px;color:#7C90A2;direction:ltr}
.hrx .feed-phone{border-radius:18px;overflow:hidden;border:6px solid #0b1622;box-shadow:0 14px 34px rgba(11,22,34,.18);line-height:0;background:#fff}
.hrx .feed-new .feed-phone{border-color:#C9A86A}
.hrx .feed-phone img{display:block;height:min(52vh,470px);width:auto}
.hrx .feed-col ul{list-style:none;display:flex;flex-direction:column;gap:4px;text-align:center}
.hrx .feed-col li{font-size:14.5px;color:#4a5965}
.hrx .feed-new li{color:#0b1622;font-weight:600}
.hrx .feeds-arrow{align-self:center;font-size:34px;color:#C9A86A}
@media(max-width:768px){.hrx .feeds{flex-direction:column-reverse;align-items:center}.hrx .feeds-arrow{transform:rotate(90deg)}.hrx .feed-phone img{height:auto;width:min(80vw,340px)}}
</style>'''

m = re.search(r'<section\b[^>]*id="hero".*?</section>', s, re.S)
s = s[:m.end()] + "\n\n" + slide + s[m.end():]

secs = list(re.finditer(r'<section\b.*?</section>', s, re.S))
total = len(secs)
out, last = [], 0
for i, m in enumerate(secs, 1):
    t = re.sub(r'<span class="slide-page-number"[^>]*>.*?</span>', '', m.group(0))
    t = t[:-len("</section>")] + f'<span class="slide-page-number" aria-label="שקף {i} מתוך {total}">{i} / {total}</span></section>'
    out.append(s[last:m.start()] + t)
    last = m.end()
s = "".join(out) + s[last:]
s = s.replace("</head>", CSS + "\n</head>", 1)
open(path, "w", encoding="utf-8").write(s)
print("slides:", total)
