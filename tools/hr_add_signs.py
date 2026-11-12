"""Add two slides: 'signs of connection' (after hr-results) and 'what we measure in 2027' (before hr-next).
Usage: python3 -I tools/hr_add_signs.py "<deck html>"
Data: @work_at_astral posts Jan-Oct 2026 (77 posts) and their public comments, collected Nov 2026.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-signs"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

STATS = [
    ("9", "עובדים ומנהלים קיבלו פוסט אישי, עם שם וסיפור", "מנגר במלון אריאה ועד מנהלת ההדרכה של הרשת"),
    ("3", "סיפורי קידום אמיתיים", "אודליה ממלצרית למנהלת משאבי אנוש, ריטה מפקידת קבלה למנהלת קבלה, ועדן"),
    ("2", "רילס עם מנכ״לי המלונות מול המצלמה", "ההנהלה משתתפת בתוכן, לא רק מאשרת אותו"),
    ("פי 17", "יותר שיתופים אורגניים מאשר ב־2025", "התוכן עובר מיד ליד, בלי תקציב קידום"),
]
QUOTES = [
    ("אין ולא יהיה עלייך, והיא גם הייתה מצטיינת השנה", "על הפוסט של עדי פלד, הכוכבים של אסטרל"),
    ("אין מנכ״ליות כאלה בשום מקום בעולם!", "על הרילס עם איילה חן מועלם, מנכ״לית אריאה"),
    ("עושים חשק לבוא לעבוד באריאה", "על רילס על עובדים ותיקים ברשת"),
    ("לאיפה מגישים קורות חיים?", "על רילס השגרירים, הפוסט המוביל של השנה"),
]

stats = "".join(
    f'<div class="sg-stat reveal d{i+2}"><div class="sg-v">{v}</div><div class="sg-l">{l}</div><p>{p}</p></div>'
    for i, (v, l, p) in enumerate(STATS))
quotes = "".join(f'<figure class="sg-q"><blockquote>״{q}״</blockquote><figcaption>{c}</figcaption></figure>' for q, c in QUOTES)

signs = f'''<section class="slide sand hrx" id="hr-signs" data-dot="גאוות יחידה · הסימנים">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">גאוות יחידה · ינואר–אוקטובר 2026</div>
<h2 class="reveal d1">הסימנים שהחיבור לרשת קורה</h2>
<div class="sg-stats">{stats}</div>
<div class="sg-quotes reveal d6">{quotes}</div>
<p class="org-src reveal d6">מקור: 77 הפוסטים של @work_at_astral בינואר–אוקטובר 2026 והתגובות הציבוריות עליהם. שיתופים: Meta Business Suite, אינסטגרם ופייסבוק, אורגני בלבד.</p>
</div></section>'''

MEASURE = [
    ("01", "מאיפה הגיעו העובדים", "שאלת ״איך שמעת עלינו?״ בשיחת הוואטסאפ ובטופס הקליטה. כך נדע כמה מהעובדים שנקלטו הגיעו דרך הסושיאל."),
    ("02", "כמה העובדים גאים במקום", "סקר דופק קצר פעמיים בשנה: האם אתה גאה לעבוד באסטרל, והאם היית ממליץ לחבר."),
    ("03", "כמה זמן העובדים נשארים", "נתוני תחלופה וותק מה־HR בכל רבעון. הרבעון הראשון של 2027 יהיה נקודת הבסיס."),
]
mcards = "".join(
    f'<article class="card reveal d{i+2}"><span class="n">{n}</span><h3>{h}</h3><p>{p}</p></article>'
    for i, (n, h, p) in enumerate(MEASURE))

measure = f'''<section class="slide sand hrx" id="hr-measure" data-dot="מה נמדוד ב־2027">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">2027 · מדידה</div>
<h2 class="reveal d1">מ־2027 נמדוד גם את ההשפעה על העובדים</h2>
<p class="ms-lead reveal d1">הסושיאל בנה גאוות יחידה. השלב הבא הוא לחבר את זה לנתונים של שימור וקליטה.</p>
<div class="cards ms-cards">{mcards}</div>
<div class="ms-ask reveal d5"><b>מה אנחנו צריכים מכם</b><span>שותף ב־HR שירכז את נתוני הקליטה והתחלופה, ואישור להוסיף את השאלות לתהליך הגיוס ולסקר העובדים.</span></div>
</div></section>'''

CSS = '''<style>
/* ===== HR · signs of connection + 2027 measurement ===== */
#hr-signs,#hr-measure{padding-top:96px;padding-bottom:40px}
#hr-signs h2,#hr-measure h2{font-size:clamp(28px,3vw,44px)}
.hrx .sg-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:22px}
.hrx .sg-stat{background:#fff;border:1px solid #e6dfcf;border-top:3px solid #C9A86A;border-radius:14px;padding:16px 18px;display:flex;flex-direction:column;gap:6px}
.hrx .sg-v{font-size:clamp(38px,4vw,56px);font-weight:800;line-height:1;color:#95743b;text-align:right;unicode-bidi:plaintext}
.hrx .sg-l{font-size:16px;font-weight:700;color:#0b1622;line-height:1.35}
.hrx .sg-stat p{font-size:13.5px;color:#4a5965;line-height:1.5;margin:0}
.hrx .sg-quotes{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:18px}
.hrx .sg-q{margin:0;padding:4px 16px 4px 0;border-right:3px solid rgba(201,168,106,.7)}
.hrx .sg-q blockquote{margin:0;font-size:17px;font-weight:700;color:#0b1622;line-height:1.4}
.hrx .sg-q figcaption{font-size:12.5px;color:#7C90A2;margin-top:6px;line-height:1.4}
.hrx .ms-lead{font-size:clamp(16px,1.4vw,19px);color:#4a5965;margin-top:8px;max-width:760px}
.hrx .ms-cards{margin-top:22px}
.hrx .ms-ask{margin-top:20px;background:linear-gradient(150deg,rgba(201,168,106,.22),rgba(201,168,106,.06));border:1px solid rgba(166,134,79,.45);border-radius:14px;padding:16px 20px;display:flex;flex-direction:column;gap:6px}
.hrx .ms-ask b{font-size:17px;color:#0b1622}
.hrx .ms-ask span{font-size:15px;color:#4a5965;line-height:1.55}
@media(max-width:900px){.hrx .sg-stats,.hrx .sg-quotes{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.hrx .sg-stats,.hrx .sg-quotes{grid-template-columns:1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-results".*?</section>', s, re.S)
s = s[:m.end()] + "\n\n" + signs + s[m.end():]
m = re.search(r'<section\b[^>]*id="hr-next"', s)
s = s[:m.start()] + measure + "\n\n" + s[m.start():]

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
