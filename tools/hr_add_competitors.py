"""Competitor HR Instagram pages slide, inserted before the summary slide.
Usage: python3 -I tools/hr_add_competitors.py "<deck html>"
Data: public Instagram figures, last 12 posts per account, collected Nov 2026.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-competitors"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

ROWS = [
    ("אסטרל", "work_at_astral", "536", "כ־2 בשבוע", "2.4%", "עובדים בפרונט, סיפורי קידום, שגרירים, הומור", True),
    ("ישרוטל", "isrotel_jobs", "3,160", "כ־3 בשבוע", "1.1%", "היכרות עם עובדים, טקסי ותק, הומור", False),
    ("דן", "work_at_dan", "1,395", "3 פוסטים ב־2026", "2.0%", "סדרת היכרות עם עובדים, שהופסקה", False),
    ("פתאל", "bidur_fattal", "3,741", "כ־2 בשבוע", "1.3%", "גיוס לצוותי בידור בלבד", False),
]
rows = "".join(
    f'<tr class="{"hl" if hl else ""}"><th>{n}<small>@{h}</small></th><td>{f}</td><td>{fr}</td>'
    f'<td class="y26">{er}</td><td class="txt">{c}</td></tr>'
    for n, h, f, fr, er, c, hl in ROWS
)

slide = f'''<section class="slide sand hrx" id="hr-competitors" data-dot="המתחרים">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">המתחרים · עמודי הגיוס באינסטגרם</div>
<h2 class="reveal d1">איך אנחנו נראים מול ישרוטל, דן ופתאל</h2>
<table class="org-t comp-t reveal d2">
<thead><tr><th></th><th>עוקבים</th><th>קצב פרסום</th><th>מעורבות ביחס לעוקבים</th><th>על מה התוכן</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<div class="comp-strong reveal d3">
<div><b>המעורבות הכי גבוהה ביחס לגודל הקהל</b><span>עמוד קטן יותר, אבל קהל שמגיב יותר מאשר אצל כל המתחרים.</span></div>
<div><b>עמוד גיוס של כל הרשת, שפעיל כל השנה</b><span>דן כמעט הפסיקה לפרסם, ופתאל מגייסת באינסטגרם רק לצוותי בידור.</span></div>
<div><b>תמהיל תוכן רחב סביב העובדים</b><span>סיפורי קידום, הכוכבים של אסטרל, תוכן שגרירים והומור מהשטח.</span></div>
</div>
<p class="org-src reveal d4">מקור: נתונים ציבוריים מאינסטגרם, נובמבר 2026. מעורבות: ממוצע לייקים ותגובות בפוסטים האחרונים (בלי פוסטים מוצמדים), חלקי מספר העוקבים. לפתאל אין עמוד גיוס כללי, ולכן מוצג עמוד צוות הבידור.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · competitors ===== */
#hr-competitors{padding-top:100px}
#hr-competitors h2{font-size:clamp(28px,3vw,42px)}
.hrx .comp-t{margin-top:18px}
.hrx .comp-t thead th{padding:10px 14px}
.hrx .comp-t tbody th{padding:10px 16px;font-size:16px}
.hrx .comp-t tbody th small{direction:ltr;text-align:right}
.hrx .comp-t td{padding:10px 12px;font-size:15px;color:#4a5965}
.hrx .comp-t td.y26{font-size:18px}
.hrx .comp-t td.txt{white-space:normal;text-align:right;font-size:13.5px;max-width:300px}
.hrx .comp-t tr.hl th,.hrx .comp-t tr.hl td{color:#0b1622;font-weight:700}
.hrx .comp-t tr.hl td.y26{color:#95743b}
.hrx .comp-strong{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:18px}
.hrx .comp-strong div{background:#fff;border:1px solid #e6dfcf;border-top:3px solid #C9A86A;border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.hrx .comp-strong b{font-size:15.5px;color:#0b1622}
.hrx .comp-strong span{font-size:13.5px;color:#4a5965;line-height:1.5}
@media(max-width:768px){.hrx .comp-strong{grid-template-columns:1fr}.hrx .comp-t td.txt{display:none}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-next".*?</section>', s, re.S)
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
