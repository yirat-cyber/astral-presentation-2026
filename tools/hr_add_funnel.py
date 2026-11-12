"""Facebook/Instagram inquiries vs hires, May-Sep 2025 vs 2026, inserted after hr-results.
Usage: python3 -I tools/hr_add_funnel.py "<deck html>"
Data: Astral HR report "דוחות שיווק לשנת 2026", sheets ריכוז פניות / ריכוז פניות 2025 / ניתוח מקורות,
row "פייסבוק/אינסטגרם" only (per client instruction).
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-funnel"' in s:
    sys.exit("already applied")

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

# month, inquiries 2025, inquiries 2026, hired 2025, hired 2026
MONTHS = [
    ("מאי", 71, 449, 2, 6),
    ("יוני", 126, 334, 6, 2),
    ("יולי", 223, 328, 20, 5),
    ("אוגוסט", 136, 362, 1, 3),
    ("ספטמבר", 62, 176, 5, 2),
]
t = [sum(m[i] for m in MONTHS) for i in range(1, 5)]
rows = "".join(
    f'<tr><th>{n}</th><td class="y25">{a:,}</td><td class="y26">{b:,}</td><td class="y25">{c}</td><td class="y26">{d}</td></tr>'
    for n, a, b, c, d in MONTHS)
rows += (f'<tr class="hl"><th>סה״כ</th><td class="y25">{t[0]:,}</td><td class="y26">{t[1]:,}</td>'
         f'<td class="y25">{t[2]}</td><td class="y26">{t[3]}</td></tr>')

slide = f'''<section class="slide sand hrx" id="hr-funnel" data-dot="מהפנייה לקליטה">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">מהפנייה לקליטה · פייסבוק ואינסטגרם · מאי–ספטמבר</div>
<h2 class="reveal d1">פי 2.7 יותר פניות מהסושיאל. האתגר הבא: להפוך אותן לעובדים</h2>
<div class="fn-grid">
<table class="org-t fn-t reveal d2">
<thead><tr><th></th><th>פניות 2025</th><th>פניות 2026</th><th>התקבלו 2025</th><th>התקבלו 2026</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<div class="fn-side">
<div class="fn-box reveal d3"><b>למה רוב הפניות לא מגיעות לקליטה</b>
<ol><li><span>מרחק</span>המועמד לא גר באילת ולא מוכן לעבור. זו סיבת הפסילה הנפוצה ביותר.</li>
<li><span>הסרת מועמדות</span>המועמד פנה, ובהמשך התהליך ירד מזה.</li>
<li><span>קורות חיים</span>הניסיון לא מתאים למשרה.</li></ol></div>
<div class="fn-box fn-next reveal d4"><b>מה עושים ב־2027</b>
<ul><li>סינון כבר במודעה: עבודה באילת, מגורים מסובסדים, משמרות</li>
<li>שאלות סינון אוטומטיות בוואטסאפ, לפני שהפנייה מגיעה לרכזת</li>
<li>מעקב משותף עם HR על זמן החזרה למועמד</li></ul></div>
</div>
</div>
<p class="org-src reveal d5">מקור: דוח הגיוס של אסטרל, שורת ״פייסבוק/אינסטגרם״ בלבד. אחוז קליטה: <bdi>{t[2]/t[0]:.1%}</bdi> ב־2025, <bdi>{t[3]/t[1]:.1%}</bdi> ב־2026. סיבות הפסילה: גיליון ניתוח המקורות, 2026.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · funnel (FB/IG inquiries vs hires) ===== */
#hr-funnel{padding-top:96px;padding-bottom:36px}
#hr-funnel h2{font-size:clamp(26px,2.8vw,40px);max-width:980px}
.hrx .fn-grid{display:grid;grid-template-columns:1.15fr 1fr;gap:24px;margin-top:22px;align-items:start}
.hrx .fn-t{margin-top:0}
.hrx .fn-t thead th{padding:11px 12px}
.hrx .fn-t tbody th,.hrx .fn-t td{padding:10px 12px}
.hrx .fn-side{display:flex;flex-direction:column;gap:14px}
.hrx .fn-box{background:#fff;border:1px solid #e6dfcf;border-top:3px solid #C9A86A;border-radius:14px;padding:16px 18px}
.hrx .fn-box b{display:block;font-size:16px;color:#0b1622;margin-bottom:8px}
.hrx .fn-box ol,.hrx .fn-box ul{margin:0;padding-inline-start:20px;display:flex;flex-direction:column;gap:6px}
.hrx .fn-box li{font-size:14px;color:#4a5965;line-height:1.5}
.hrx .fn-box li span{font-weight:700;color:#0b1622;margin-inline-end:6px}
.hrx .fn-next{background:linear-gradient(150deg,rgba(201,168,106,.20),rgba(201,168,106,.05));border-color:rgba(166,134,79,.45)}
@media(max-width:900px){.hrx .fn-grid{grid-template-columns:1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-results".*?</section>', s, re.S)
s = s[:m.end()] + "\n\n" + slide + s[m.end():]

secs = list(re.finditer(r'<section\b.*?</section>', s, re.S))
total = len(secs)
out, last = [], 0
for i, m in enumerate(secs, 1):
    tx = re.sub(r'<span class="slide-page-number"[^>]*>.*?</span>', '', m.group(0))
    tx = tx[:-len("</section>")] + f'<span class="slide-page-number" aria-label="שקף {i} מתוך {total}">{i} / {total}</span></section>'
    out.append(s[last:m.start()] + tx)
    last = m.end()
s = "".join(out) + s[last:]
s = s.replace("</head>", CSS + "\n</head>", 1)
open(path, "w", encoding="utf-8").write(s)
print("slides:", total, "totals:", t)
