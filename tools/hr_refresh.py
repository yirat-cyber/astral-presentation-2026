"""Refresh of HR deck slides 2-7 per client feedback.
Usage: python3 -I tools/hr_refresh.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'
ASTRAL = '<img class="brand" src="media/aef607b7d4.png" alt="Astral Hotels">'

def sec(sid):
    m = re.search(r'<section\b[^>]*id="' + sid + r'".*?</section>', s, re.S)
    if not m:
        sys.exit("missing " + sid)
    return m

def replace_sec(sid, new):
    global s
    m = sec(sid)
    s = s[:m.start()] + new + s[m.end():]

def must(old, new):
    global s
    assert old in s, old[:60]
    s = s.replace(old, new, 1)

# --- slide 2: hero ---
must('<span class="hero-title-line">שנה של שינוי אסטרטגי</span>',
     '<span class="hero-title-line">שנה של קצירת פירות</span>')
must('<span class="hero-subtitle-line">Astral HR · מגייסים לעבודה, בונים בית</span>',
     '<span class="hero-subtitle-line">אחרי החלטה אסטרטגית מסוף 2024</span>')

# --- slide 3: goal line ---
must('<p class="strip reveal d5">המטרה שלנו הייתה ברורה: <b>לבנות לעובדים סיבה להישאר.</b></p>',
     '<p class="strip reveal d5">המטרה שלנו היתה ברורה: <b>לייצר גאוות יחידה סביב אסטרל כמקום עבודה</b>, בכלי הסושיאל שברשותנו.</p>')

# --- slide 4: strategy ---
replace_sec("hr-shift", f'''<section class="slide dark hrx hrx-dark" id="hr-shift" data-dot="האסטרטגיה">{ASTRAL}{SIG}<div class="wrap">
<div class="kick reveal">האסטרטגיה</div>
<h2 class="reveal d1">המשרות ממשיכות לרוץ.<br><span class="gold">הפיד מספר את הסיפור מהשטח.</span></h2>
<p class="lead reveal d2">פרסום המשרות הוא עדיין אחת המטרות שלנו. אבל בפיד אנחנו מעלים תוכן סושיאלי מהשטח, שגורם לעובדים להיות גאים ולאחרים לרצות להצטרף.</p>
<div class="two-ch">
<div class="ch reveal d3"><span class="ch-k">בקמפיינים הממומנים</span><h3>פרסום משרות</h3><ul><li>מודעות לפי תפקיד ומלון</li><li>הפניה לוואטסאפ ולאתר המשרות</li></ul></div>
<div class="ch ch-main reveal d4"><span class="ch-k">בפיד</span><h3>תוכן סושיאלי מהשטח</h3><ul><li>סרטונים מצחיקים של עובדים</li><li>הרמות לאנשים שקיבלו קידום</li><li>תוכן שעושה חשק לעבוד באילת</li></ul></div>
</div>
</div></section>''')

# --- slide 5: pillars ---
CAM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="13" height="11" rx="2"/><path d="M16 11l5-3v9l-5-3"/></svg>'
m = sec("hr-pillars")
p = m.group(0)
arts = re.findall(r'<article class="card.*?</article>', p, re.S)
assert len(arts) == 3
a2 = re.sub(r'<h3>.*?</h3><p>.*?</p>',
            '<h3>קידום ברשת, עם הוכחות מהשטח</h3><p>מסלולי ההתקדמות באסטרל, דרך סיפורים אמיתיים של עובדים שהתחילו בתפקידים זוטרים ומכהנים היום בתפקידים בכירים.</p>',
            arts[1], flags=re.S)
a3 = (f'<article class="card reveal d4"><span class="n">03</span><div class="ic">{CAM}</div>'
      '<h3>תוכן שגרירים</h3><p>תוכן שהעובדים מייצרים לנו מהשטח: הם מצלמים, מספרים ומראים איך זה באמת לעבוד באסטרל.</p></article>')
p2 = p.replace(arts[1], a2).replace(arts[2], a3)
s = s[:m.start()] + p2 + s[m.end():]

# --- slide 6: remove ---
m = sec("hr-actions")
s = s[:m.start()].rstrip() + s[m.end():]

# --- slide 7: stars series ---
STARS = [
    ("media/eefd151637.jpg", "הרצל סוגאוקר", "נגר במלון אריאה כבר 15 שנה. אחרי המשמרת: מוזיקאי וכוכב טיקטוק.", "יוני 2026"),
    ("media/ac8947dded.jpg", "קים ברנדס", "איש ביטחון במלון מלכת שבא ומטפל בעיסוי. חזר לאסטרל בזכות הקשר עם המנהל שלו.", "יולי 2026"),
    ("media/157346148f.jpg", "עדי פלד", "מנהלת הדרכה ורווחה רשתית, עם יותר מ־20 שנה במלונאות.", "אוקטובר 2026"),
]
posts = "".join(
    f'<figure class="star-post reveal d{i + 2}"><img src="{img}" alt="פוסט מסדרת הכוכבים של אסטרל: {n}">'
    f'<figcaption><b>{n}</b><span>{d}</span><small>{when}</small></figcaption></figure>'
    for i, (img, n, d, when) in enumerate(STARS)
)
replace_sec("hr-stories", f'''<section class="slide sand hrx" id="hr-stars" data-dot="הכוכבים של אסטרל">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">סדרת תוכן בפיד</div>
<h2 class="reveal d1">הכוכבים של אסטרל</h2>
<p class="lead reveal d2">פינה קבועה שמכירה לקהל את העובדים: מה הם עושים אצלנו, ומי הם מחוץ למשמרת.</p>
<div class="star-grid">{posts}</div>
</div></section>''')

CSS = '''<style>
/* ===== HR refresh: strategy + stars ===== */
.hrx .two-ch{display:grid;grid-template-columns:1fr 1.35fr;gap:20px;margin-top:34px;max-width:1000px}
.hrx .ch{border:1px solid rgba(237,228,211,.18);border-radius:16px;padding:22px 26px;background:rgba(255,255,255,.03)}
.hrx .ch-main{border-color:rgba(201,168,106,.55);background:linear-gradient(150deg,rgba(201,168,106,.16),rgba(201,168,106,.04))}
.hrx .ch-k{font-size:13px;font-weight:700;color:#9DB0C0;letter-spacing:.04em}
.hrx .ch-main .ch-k{color:#DEC48A}
.hrx .ch h3{font-size:24px;color:#fff;margin:6px 0 12px}
.hrx .ch ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.hrx .ch li{font-size:17px;color:#EDE4D3;padding-right:18px;position:relative}
.hrx .ch li::before{content:"";position:absolute;right:0;top:.6em;width:7px;height:7px;border-radius:50%;background:#C9A86A}
.hrx .star-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:24px;max-width:min(860px,calc((100vh - 400px) * 2.1))}
.hrx .star-post{margin:0;background:#fff;border:1px solid #e6dfcf;border-radius:16px;overflow:hidden;box-shadow:0 10px 30px rgba(11,22,34,.08)}
.hrx .star-post img{display:block;width:100%;aspect-ratio:4/5;object-fit:cover}
.hrx .star-post figcaption{padding:14px 18px 16px;display:flex;flex-direction:column;gap:4px}
.hrx .star-post b{font-size:18px;color:#0b1622}
.hrx .star-post span{font-size:14px;color:#4a5965;line-height:1.5}
.hrx .star-post small{font-size:12px;color:#95743b;font-weight:700;margin-top:2px}
@media(max-width:768px){.hrx .two-ch,.hrx .star-grid{grid-template-columns:1fr}.hrx .star-post img{max-height:none}}
</style>'''
s = s.replace("</head>", CSS + "\n</head>", 1)

# renumber
secs = list(re.finditer(r'<section\b.*?</section>', s, re.S))
total = len(secs)
out, last = [], 0
for i, m in enumerate(secs, 1):
    t = re.sub(r'<span class="slide-page-number"[^>]*>.*?</span>', '', m.group(0))
    t = t[:-len("</section>")] + f'<span class="slide-page-number" aria-label="שקף {i} מתוך {total}">{i} / {total}</span></section>'
    out.append(s[last:m.start()] + t)
    last = m.end()
s = "".join(out) + s[last:]

open(path, "w", encoding="utf-8").write(s)
print("slides:", total)
