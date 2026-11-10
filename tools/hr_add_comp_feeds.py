"""Four competitor feeds side by side with Jan-Oct 2026 stats, after the competitors table.
Usage: python3 -I tools/hr_add_comp_feeds.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-comp-feeds"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

FEEDS = [
    ("אסטרל", "work_at_astral", "media/f4a18ca23d.jpg", "536", "78", "31", "5.8%", True),
    ("ישרוטל", "isrotel_jobs", "media/94d86ad681.jpg", "3,160", "92", "35", "1.1%", False),
    ("דן", "work_at_dan", "media/18eb4d3152.jpg", "1,395", "3", "33", "2.4%", False),
    ("פתאל · בידור", "bidur_fattal", "media/81df80b148.jpg", "3,741", "31", "75", "2.0%", False),
]

def card(name, handle, img, fol, posts, inter, er, me):
    return (f'<figure class="cf{" cf-me" if me else ""}"><figcaption><b>{name}</b><span>@{handle}</span></figcaption>'
            f'<div class="cf-phone"><img src="{img}" alt="הפיד של {name} באינסטגרם"></div>'
            f'<dl><div><dt>עוקבים</dt><dd>{fol}</dd></div><div><dt>פוסטים</dt><dd>{posts}</dd></div>'
            f'<div><dt>אינטראקציות לפוסט</dt><dd>{inter}</dd></div><div class="cf-er"><dt>מעורבות</dt><dd>{er}</dd></div></dl></figure>')

cards = "".join(card(*f) for f in FEEDS)
slide = f'''<section class="slide sand hrx" id="hr-comp-feeds" data-dot="הפידים של המתחרים">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">המתחרים · הפידים זה לצד זה · ינואר–אוקטובר 2026</div>
<h2 class="reveal d1">ככה נראים עמודי הגיוס של הרשתות</h2>
<div class="cf-row reveal d2">{cards}</div>
<p class="org-src reveal d3">צילומי מסך מאינסטגרם, נובמבר 2026. מעורבות: אינטראקציות ממוצעות לפוסט חלקי מספר העוקבים.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · competitor feeds ===== */
#hr-comp-feeds{padding-top:92px;padding-bottom:36px}
#hr-comp-feeds h2{font-size:clamp(26px,2.8vw,40px)}
.hrx .cf-row{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,1.8vw,26px);margin-top:16px;align-items:start}
.hrx .cf{margin:0;display:flex;flex-direction:column;gap:8px}
.hrx .cf figcaption{display:flex;align-items:baseline;justify-content:space-between;gap:6px}
.hrx .cf figcaption b{font-size:17px;color:#0b1622}
.hrx .cf figcaption span{font-size:11.5px;color:#7C90A2;direction:ltr}
.hrx .cf-phone{border:5px solid #0b1622;border-radius:16px;overflow:hidden;line-height:0;background:#fff;box-shadow:0 10px 26px rgba(11,22,34,.14)}
.hrx .cf-me .cf-phone{border-color:#C9A86A}
.hrx .cf-phone img{display:block;width:100%;height:auto;max-height:44vh;object-fit:cover;object-position:top}
.hrx .cf dl{display:grid;grid-template-columns:1fr 1fr;gap:4px 10px;background:#fff;border:1px solid #e6dfcf;border-radius:12px;padding:10px 12px}
.hrx .cf-me dl{border-color:rgba(201,168,106,.6);background:rgba(201,168,106,.10)}
.hrx .cf dl div{display:flex;flex-direction:column}
.hrx .cf dt{font-size:11px;color:#7C90A2}
.hrx .cf dd{margin:0;font-size:16px;font-weight:800;color:#0b1622}
.hrx .cf-er dd{color:#95743b}
@media(max-width:768px){.hrx .cf-row{grid-template-columns:1fr 1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-competitors".*?</section>', s, re.S)
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
