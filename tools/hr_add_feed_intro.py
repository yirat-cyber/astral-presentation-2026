"""Intro slide to the feed creative, inserted before hr-stars: six static posts from 2026.
Usage: python3 -I tools/hr_add_feed_intro.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-feed-intro"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

POSTS = [
    ("media/feed-whatsapp.jpg", "קבוצת הוואטסאפ של הצוות", "״נו, אמרנו אווירה משפחתית״"),
    ("media/feed-milon.jpg", "מילון עברית־אסטרלית", "השפה שמבינים רק מבפנים"),
    ("media/feed-room.jpg", "החדר שלכם, החדר שלנו", "החיים של עובדי המלון, בלי פילטר"),
    ("media/feed-love.jpg", "מכתב האהבה הכי יפה", "״אני אחליף אותך במשמרת ערב״"),
    ("media/feed-atzmaut.jpg", "יום העצמאות", "החג, מנקודת המבט של הצוות"),
    ("media/feed-odelia.jpg", "יום ראשון שמח!", "אודליה, מנהלת משאבי אנוש, ביום האישה"),
]
cards = "".join(
    f'<figure class="fi-post reveal d{min(i + 2, 6)}"><div class="fi-img"><img src="{src}" alt="פוסט מהפיד: {t}"></div>'
    f'<figcaption><b>{t}</b><span>{d}</span></figcaption></figure>'
    for i, (src, t, d) in enumerate(POSTS))

slide = f'''<section class="slide sand hrx" id="hr-feed-intro" data-dot="מה עלה לפיד">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">הפיד · 2026</div>
<h2 class="reveal d1">בואו נראה מה עלה לפיד שלנו</h2>
<div class="fi-row">{cards}</div>
</div></section>'''

CSS = '''<style>
/* ===== HR · feed intro ===== */
#hr-feed-intro{padding-top:96px;padding-bottom:40px}
#hr-feed-intro h2{font-size:clamp(30px,3.4vw,50px)}
.hrx .fi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:clamp(12px,1.4vw,22px);margin-top:26px;align-items:start}
.hrx .fi-post{margin:0;display:flex;flex-direction:column;gap:10px}
.hrx .fi-img{border-radius:14px;overflow:hidden;line-height:0;background:#fff;box-shadow:0 12px 28px rgba(11,22,34,.16);border:1px solid #e6dfcf}
.hrx .fi-img img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}
.hrx .fi-post figcaption{display:flex;flex-direction:column;gap:3px}
.hrx .fi-post b{font-size:15px;color:#0b1622;line-height:1.3}
.hrx .fi-post span{font-size:13px;color:#4a5965;line-height:1.4}
@media(max-width:1100px){.hrx .fi-row{grid-template-columns:repeat(3,1fr)}}
@media(max-width:560px){.hrx .fi-row{grid-template-columns:1fr 1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-stars"', s)
s = s[:m.start()] + slide + "\n\n" + s[m.start():]

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
