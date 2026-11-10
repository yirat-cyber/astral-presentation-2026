"""Add the paid-media budget slide (Jan-Oct 2025 vs 2026) after the organic slide.
Usage: python3 -I tools/hr_add_budget.py "<deck html>"
Source: Ads Manager, account Astral - HR.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-budget"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

ROWS = [
    ("תקציב מדיה", "", "79 אלף ₪", "104 אלף ₪", "‎+31%", False),
    ("אנשים שנחשפו לקמפיינים", "Reach", "1.42 מיליון", "1.93 מיליון", "‎+36%", False),
    ("שיחות וואטסאפ עם מועמדים", "", "3,630", "5,375", "‎+48%", True),
    ("כניסות לאתר המשרות", "קליקים על קישור", "28 אלף", "89 אלף", "פי 3.1", True),
    ("עלות לכניסה לאתר", "", "₪2.79", "₪1.17", "‎-58%", False),
    ("עלות ל־1,000 חשיפות", "", "₪15.30", "₪11.68", "‎-24%", False),
]
rows = "".join(
    f'<tr class="{"hl" if hl else ""}"><th>{a}{f"<small>{b}</small>" if b else ""}</th>'
    f'<td class="y25">{c}</td><td class="y26">{d}</td><td><span class="chg">{e}</span></td></tr>'
    for a, b, c, d, e, hl in ROWS
)

budget = f'''<section class="slide sand hrx" id="hr-budget" data-dot="התקציב">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">המדיה הממומנת · ינואר–אוקטובר</div>
<h2 class="reveal d1">פחות כסף על קידום פוסטים, יותר כסף על גיוס</h2>
<div class="split-bars reveal d2">
<div class="sb-row"><span class="sb-y">2025</span><div class="sb-bar"><span class="sb-boost" style="width:51%">קידום פוסטים 51%</span><span class="sb-rec" style="width:49%">גיוס 49%</span></div></div>
<div class="sb-row"><span class="sb-y">2026</span><div class="sb-bar"><span class="sb-boost" style="width:28%">קידום פוסטים 28%</span><span class="sb-rec" style="width:72%">גיוס 72%</span></div></div>
</div>
<table class="org-t reveal d3">
<thead><tr><th></th><th>ינואר–אוקטובר 2025</th><th>ינואר–אוקטובר 2026</th><th>שינוי</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<p class="org-src reveal d4">מקור: Meta Ads Manager · חשבון Astral - HR. הקידום לפוסט ירד בממוצע מ־₪358 ל־₪214, והמעורבות הכוללת עלתה.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · budget slide ===== */
#hr-budget h2{font-size:clamp(30px,3.2vw,46px)}
.hrx .split-bars{margin-top:22px;display:flex;flex-direction:column;gap:10px;max-width:900px}
.hrx .sb-row{display:grid;grid-template-columns:48px 1fr;align-items:center;gap:12px}
.hrx .sb-y{font-weight:800;font-size:15px;color:#0b1622}
.hrx .sb-bar{display:flex;height:34px;border-radius:10px;overflow:hidden;font-size:13px;font-weight:700}
.hrx .sb-bar span{display:flex;align-items:center;justify-content:center;white-space:nowrap}
.hrx .sb-boost{background:#d9d2c3;color:#4a5965}
.hrx .sb-rec{background:linear-gradient(90deg,#C9A86A,#DEC48A);color:#0b1622}
#hr-budget .org-t{margin-top:20px}
#hr-budget .org-t tbody th,#hr-budget .org-t td{padding-top:11px;padding-bottom:11px}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-organic".*?</section>', s, re.S)
s = s[:m.end()] + "\n\n" + budget + s[m.end():]

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
