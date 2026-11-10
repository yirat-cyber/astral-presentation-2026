"""Add 'what we did' + 'organic results' slides to the HR deck and renumber.
Usage: python3 -I tools/hr_add_organic.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-actions"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

ACTIONS = [
    ("העובדים מול המצלמה", "רילס שבהם עובדים מכל המחלקות הם הכוכבים: מצלמה נסתרת, טרנדים והומור מהמשמרת."),
    ("״הכוכבים של אסטרל״", "פינה קבועה שמכירה לקהל עובדים ומנהלים, כמו עדי פלד, מנהלת ההדרכה והרווחה של הרשת."),
    ("סיפורי קידום אמיתיים", "ריטה שהתחילה כפקידת קבלה, רמי, גלינה שעלתה מקזחסטן. הוכחה שבאסטרל מתקדמים."),
    ("נבחרת שגרירים", "סדנת וידאו לעובדים, שמצלמים ומספרים בעצמם איך זה לעבוד באסטרל."),
    ("מרימים לעובדים", "מסיבת השנה, הרמות כוסית, ימי פינוק לצוותים והוקרה למנהלים המצטיינים של הרשת."),
    ("גם המשפחות בתמונה", "הפנינג ל״ג בעומר, פורים וט״ו בשבט לילדי העובדים, ויום כיף לילדים שעולים לכיתה א׳."),
]

cards = "".join(
    f'<article class="card reveal d{i % 3 + 2}"><span class="n">{i + 1:02d}</span><h3>{t}</h3><p>{d}</p></article>'
    for i, (t, d) in enumerate(ACTIONS)
)

actions = f'''<section class="slide sand hrx" id="hr-actions" data-dot="מה עשינו">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">מאז 2024</div>
<h2 class="reveal d1">העובדים במרכז, בכל פוסט</h2>
<p class="lead reveal d2">המטרה הייתה לחבר את העובדים רגשית לרשת. אז שמנו אותם בפרונט, וחגגנו אותם בכל הזדמנות.</p>
<div class="cards cards-6">{cards}</div>
</div></section>'''

ROWS = [
    ("אנשים שראו את התוכן בלי פרסום", "Reach אורגני", "33 אלף", "163 אלף", "פי 4.9", False),
    ("צפיות בתוכן בלי פרסום", "צפיות אורגניות", "168 אלף", "446 אלף", "פי 2.6", False),
    ("לייקים, תגובות, שיתופים ושמירות", "אינטראקציות אורגניות", "950", "7,130", "פי 7.5", False),
    ("שיתופים של התוכן לחברים", "", "178", "3,242", "פי 18", True),
    ("עוקבים חדשים בזכות התוכן", "", "57", "150", "פי 2.6", False),
    ("שיעור מעורבות", "אינטראקציות מתוך צפיות", "0.56%", "1.60%", "פי 2.9", False),
]

rows = "".join(
    f'<tr class="{"hl" if hl else ""}"><th>{a}{f"<small>{b}</small>" if b else ""}</th>'
    f'<td class="y25">{c}</td><td class="y26">{d}</td><td><span class="chg">{e}</span></td></tr>'
    for a, b, c, d, e, hl in ROWS
)

organic = f'''<section class="slide sand hrx" id="hr-organic" data-dot="התוצאה · אורגני">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">התוצאה · יותר משנתיים אחרי</div>
<h2 class="reveal d1">התוכן על העובדים עובד, גם בלי לשלם עליו</h2>
<p class="lead reveal d2">ב־2026 הגענו כמעט לפי 5 אנשים בלי פרסום. הקהל מגיב פי 7.5 יותר, ומשתף את התוכן עם חברים פי 18 יותר. וכשעובד שולח סרטון לחבר, שם בדיוק נולד מועמד חדש.</p>
<table class="org-t reveal d3">
<thead><tr><th></th><th>ינואר–אוקטובר 2025</th><th>ינואר–אוקטובר 2026</th><th>שינוי</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p class="org-src reveal d4">מקור: Meta Business Suite · אינסטגרם · נתונים אורגניים בלבד, בלי קידום ממומן.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · actions + organic table ===== */
.hrx .cards.cards-6{grid-template-columns:repeat(3,1fr);gap:18px;margin-top:30px}
.hrx .cards-6 .card{padding:22px 22px 24px}
.hrx .cards-6 .card h3{font-size:19px;margin:10px 0 8px}
.hrx .cards-6 .card p{font-size:14.5px}
#hr-organic .lead{max-width:900px}
.hrx .org-t{width:100%;margin-top:28px;border-collapse:separate;border-spacing:0;background:#fff;border:1px solid #e6dfcf;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(11,22,34,.06)}
.hrx .org-t thead th{font-size:13px;font-weight:700;color:#7C90A2;padding:14px 22px;text-align:center;background:#faf7f0;border-bottom:1px solid #e6dfcf}
.hrx .org-t thead th:first-child{text-align:right}
.hrx .org-t tbody th{text-align:right;font-size:17px;font-weight:700;color:#0b1622;padding:14px 22px;border-top:1px solid #efe9dc}
.hrx .org-t tbody th small{display:block;font-size:12px;font-weight:400;color:#7C90A2;margin-top:2px}
.hrx .org-t td{text-align:center;padding:14px 22px;border-top:1px solid #efe9dc;unicode-bidi:plaintext;white-space:nowrap}
.hrx .org-t tbody tr:first-child th,.hrx .org-t tbody tr:first-child td{border-top:0}
.hrx .org-t .y25{font-size:17px;color:#7C90A2}
.hrx .org-t .y26{font-size:21px;font-weight:800;color:#0b1622}
.hrx .org-t .chg{display:inline-block;font-weight:700;font-size:14px;color:#95743b;background:rgba(201,168,106,.15);border:1px solid rgba(201,168,106,.45);border-radius:100px;padding:4px 12px}
.hrx .org-t tr.hl{background:rgba(201,168,106,.10)}
.hrx .org-t tr.hl .y26{color:#95743b}
.hrx .org-src{margin-top:12px;font-size:12px;color:#7C90A2}
@media(max-width:768px){
  .hrx .cards.cards-6{grid-template-columns:1fr}
  .hrx .org-t thead th,.hrx .org-t tbody th,.hrx .org-t td{padding:10px 8px}
  .hrx .org-t tbody th{font-size:14px}
  .hrx .org-t .y26{font-size:16px}
}
</style>'''

def insert_after(html, sid, new):
    m = re.search(r'<section\b[^>]*id="' + sid + r'".*?</section>', html, re.S)
    if not m:
        sys.exit("missing " + sid)
    return html[:m.end()] + "\n\n" + new + html[m.end():]

s = insert_after(s, "hr-pillars", actions)
s = insert_after(s, "hr-ambassadors", organic)

# renumber every slide
secs = list(re.finditer(r'<section\b.*?</section>', s, re.S))
total = len(secs)
out, last = [], 0
for i, m in enumerate(secs, 1):
    sec = re.sub(r'<span class="slide-page-number"[^>]*>.*?</span>', '', m.group(0))
    sec = sec[:-len("</section>")] + f'<span class="slide-page-number" aria-label="שקף {i} מתוך {total}">{i} / {total}</span></section>'
    out.append(s[last:m.start()] + sec)
    last = m.end()
s = "".join(out) + s[last:]
s = s.replace("</head>", CSS + "\n</head>", 1)

open(path, "w", encoding="utf-8").write(s)
print("slides:", total)
