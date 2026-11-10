"""Slide 10 v2 (boosts vs recruitment, with engagement) + creative slide placeholders.
Usage: python3 -I tools/hr_budget_v2.py "<deck html>"
Sources: Ads Manager (Astral - HR) and Business Suite, Jan-Oct 2025 vs 2026.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
LRM = "‎"

def table(rows):
    body = "".join(
        f'<tr class="{"hl" if hl else ""}"><th>{a}</th><td class="y25">{c}</td><td class="y26">{d}</td>'
        f'<td><span class="chg">{e}</span></td></tr>'
        for a, c, d, e, hl in rows
    )
    return ('<table class="org-t bud-t"><thead><tr><th></th><th>2025</th><th>2026</th><th>שינוי</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')

BOOST = [
    ("תקציב", "40 אלף ₪", "30 אלף ₪", LRM + "-27%", False),
    ("פוסטים שקודמו", "113", "138", LRM + "+22%", False),
    ("תקציב ממוצע לפוסט", "₪358", "₪214", LRM + "-40%", False),
    ("מעורבות (לייקים, תגובות, שיתופים)", "24,003", "28,081", LRM + "+17%", True),
    ("עלות לאינטראקציה ממומנת", "₪1.80", "₪1.41", LRM + "-22%", False),
]
RECRUIT = [
    ("תקציב", "39 אלף ₪", "75 אלף ₪", LRM + "+93%", False),
    ("שיחות וואטסאפ עם מועמדים", "3,630", "5,375", LRM + "+48%", True),
    ("כניסות לאתר המשרות", "28 אלף", "89 אלף", "פי 3.1", True),
    ("עלות לכניסה לאתר", "₪2.79", "₪1.17", LRM + "-58%", False),
]

m = re.search(r'<section\b[^>]*id="hr-budget".*?</section>', s, re.S)
sec = m.group(0)
num = re.search(r'<span class="slide-page-number".*?</span>', sec).group(0)
head = sec[:sec.index('<div class="wrap">')]
new = head + f'''<div class="wrap">
<div class="kick reveal">המדיה הממומנת · ינואר–אוקטובר</div>
<h2 class="reveal d1">פחות כסף על קידום פוסטים, יותר כסף על גיוס</h2>
<p class="bud-total reveal d1">סך התקציב: 79 אלף ₪ ב־2025, 104 אלף ₪ ב־2026</p>
<div class="split-bars reveal d2">
<div class="sb-row"><span class="sb-y">2025</span><div class="sb-bar"><span class="sb-boost" style="width:51%">קידום פוסטים 51%</span><span class="sb-rec" style="width:49%">גיוס 49%</span></div></div>
<div class="sb-row"><span class="sb-y">2026</span><div class="sb-bar"><span class="sb-boost" style="width:28%">קידום פוסטים 28%</span><span class="sb-rec" style="width:72%">גיוס 72%</span></div></div>
</div>
<div class="bud-grid">
<div class="bud-col reveal d3"><h3><span class="dot dot-boost"></span>קידום פוסטים</h3>{table(BOOST)}</div>
<div class="bud-col reveal d4"><h3><span class="dot dot-rec"></span>קמפייני גיוס</h3>{table(RECRUIT)}</div>
</div>
<p class="org-src reveal d4">מקור: Meta Ads Manager (חשבון Astral - HR) ו־Meta Business Suite. מעורבות: אורגני וממומן יחד.</p>
</div>{num}</section>'''
s = s[:m.start()] + new + s[m.end():]

CSS = '''<style>
/* ===== HR · budget v2 ===== */
#hr-budget{padding-top:100px}
#hr-budget h2{font-size:clamp(28px,3vw,42px)}
.hrx .bud-total{margin-top:6px;font-size:16px;color:#4a5965}
#hr-budget .split-bars{margin-top:14px}
#hr-budget .sb-bar{height:28px}
.hrx .bud-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px;margin-top:18px}
.hrx .bud-col h3{display:flex;align-items:center;gap:8px;font-size:18px;color:#0b1622;margin-bottom:8px}
.hrx .bud-col .dot{width:12px;height:12px;border-radius:3px}
.hrx .dot-boost{background:#bfb6a4}
.hrx .dot-rec{background:#C9A86A}
.hrx .bud-t{margin-top:0}
.hrx .bud-t thead th{padding:9px 12px}
.hrx .bud-t tbody th{font-size:14.5px;padding:9px 12px}
.hrx .bud-t td{padding:9px 10px}
.hrx .bud-t .y25{font-size:14.5px}
.hrx .bud-t .y26{font-size:17px}
.hrx .bud-t .chg{font-size:12.5px;padding:3px 9px}
@media(max-width:768px){.hrx .bud-grid{grid-template-columns:1fr}}
#hr-creatives .vid-soon{display:flex;align-items:center;justify-content:center;text-align:center;aspect-ratio:9/16;max-height:62vh;border:1.5px dashed #C9A86A;border-radius:14px;background:rgba(201,168,106,.08);color:#95743b;font-weight:700;font-size:14px;padding:16px}
</style>'''
s = s.replace("</head>", CSS + "\n</head>", 1)

# creative slide: remove old videos, leave labelled frames for the chosen reels
REELS = ["מי חייב להצטרף למוקד של אסטרל", "כל אחת והמקורות שלה", "השאלות שמורות במערכת", "כולם אומרים את זה בהתחלה"]
m = re.search(r'<section\b[^>]*id="hr-creatives".*?</section>', s, re.S)
sec = m.group(0)
frames = "".join(f'<figure class="vcard"><div class="vid-soon">הסרטון יעלה בקרוב</div><figcaption class="hr-creative-label">{t}</figcaption></figure>' for t in REELS)
sec2 = re.sub(r'<div class="vrow">.*?</div></div><span', f'<div class="vrow">{frames}</div></div><span', sec, flags=re.S)
assert sec2 != sec
s = s[:m.start()] + sec2 + s[m.end():]

open(path, "w", encoding="utf-8").write(s)
print("ok")
