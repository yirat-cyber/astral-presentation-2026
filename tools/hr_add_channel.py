"""WhatsApp (May-Sep 2025) vs Adam system (May-Sep 2026) campaign destination, inserted after hr-funnel.
Usage: python3 -I tools/hr_add_channel.py "<deck html>"   (rebuilds the slide if it already exists)
Data: Astral HR report, row "פייסבוק/אינסטגרם". Per client: May-Sep 2026 campaigns led to the Adam system,
the same months in 2025 led to WhatsApp.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-channel"' in s:
    s = re.sub(r'<section\b[^>]*id="hr-channel".*?</section>\s*', '', s, flags=re.S)
    s = re.sub(r'<style>\s*/\* ===== HR · channel.*?</style>\s*', '', s, flags=re.S)

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

# month, WhatsApp 2025 (inquiries, hired), Adam 2026 (inquiries, hired)
MONTHS = [
    ("מאי", 71, 2, 449, 6),
    ("יוני", 126, 6, 334, 2),
    ("יולי", 223, 20, 328, 5),
    ("אוגוסט", 136, 1, 362, 3),
    ("ספטמבר", 62, 5, 176, 2),
]
wi, wh, ai, ah = (sum(m[i] for m in MONTHS) for i in range(1, 5))
pct = lambda h, i: f"{h / i:.1%}"

def card(cls, tag, title, inq, hired):
    return (f'<div class="ch-card {cls}"><span class="ch-tag">{tag}</span><h3>{title}</h3>'
            f'<div class="ch-big"><bdi>{pct(hired, inq)}</bdi></div><div class="ch-lbl">מהפונים גויסו לעבודה</div>'
            f'<dl><div><dt>פניות</dt><dd><bdi>{inq:,}</bdi></dd></div><div><dt>גויסו</dt><dd>{hired}</dd></div></dl></div>')

cards = (card("ch-wa reveal d2", "מאי–ספטמבר 2025", "קמפיין לוואטסאפ", wi, wh)
         + card("ch-adam reveal d3", "מאי–ספטמבר 2026", "קמפיין למערכת אדם", ai, ah))

rows = "".join(
    f'<tr><th>{n}</th><td class="y26">{a}</td><td class="y25">{b}</td><td class="y26"><bdi>{pct(b, a)}</bdi></td>'
    f'<td class="y25">{c}</td><td class="y25">{d}</td><td class="y25"><bdi>{pct(d, c)}</bdi></td></tr>'
    for n, a, b, c, d in MONTHS)

slide = f'''<section class="slide sand hrx" id="hr-channel" data-dot="וואטסאפ מול מערכת אדם">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">לאן הקמפיין מוביל · פייסבוק ואינסטגרם</div>
<h2 class="reveal d1">וואטסאפ הביא פחות פניות, אבל פי 5 יותר מהן הפכו לעובדים</h2>
<div class="ch-grid">
<div class="ch-cards">{cards}</div>
<table class="org-t ch-t reveal d4">
<thead><tr><th></th><th colspan="3">וואטסאפ · 2025</th><th colspan="3">מערכת אדם · 2026</th></tr>
<tr class="ch-sub"><th></th><th>פניות</th><th>גויסו</th><th>אחוז</th><th>פניות</th><th>גויסו</th><th>אחוז</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</div>
<p class="ch-note reveal d5">שיחה בוואטסאפ מחייבת את המועמד לכתוב ולהגיב, ומאפשרת לסנן כבר בשיחה. טופס במערכת אדם קל למלא בלחיצה, ולכן מגיעות יותר פניות עם פחות כוונה אמיתית.</p>
<p class="org-src reveal d5">מקור: דוח הגיוס של אסטרל, שורת ״פייסבוק/אינסטגרם״, מאי–ספטמבר. ההשוואה היא בין שנים שונות, ולכן גם גורמים אחרים (שוק העבודה, המשרות הפתוחות) יכולים להשפיע.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · channel (WhatsApp vs Adam) ===== */
#hr-channel{padding-top:88px;padding-bottom:30px}
#hr-channel h2{font-size:clamp(26px,2.8vw,40px)}
.hrx .ch-grid{display:grid;grid-template-columns:1fr 1.25fr;gap:24px;margin-top:20px;align-items:stretch}
.hrx .ch-cards{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.hrx .ch-card{border-radius:16px;padding:18px 18px 16px;display:flex;flex-direction:column;gap:4px}
.hrx .ch-wa{background:#0b1622;color:#fff}
.hrx .ch-adam{background:#fff;border:1px solid #e6dfcf;color:#0b1622}
.hrx .ch-tag{font-size:12px;font-weight:700;color:#C9A86A}
.hrx .ch-adam .ch-tag{color:#7C90A2}
.hrx .ch-card h3{font-size:17px;margin:0 0 6px}
.hrx .ch-big{font-size:clamp(44px,4.6vw,68px);font-weight:800;line-height:1;color:#C9A86A}
.hrx .ch-adam .ch-big{color:#7C90A2}
.hrx .ch-lbl{font-size:13.5px;opacity:.85}
.hrx .ch-card dl{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0 0;padding-top:12px;border-top:1px solid rgba(201,168,106,.35)}
.hrx .ch-adam dl{border-top-color:#e6dfcf}
.hrx .ch-card dl div{display:flex;flex-direction:column}
.hrx .ch-card dt{font-size:12px;opacity:.7}
.hrx .ch-card dd{margin:0;font-size:22px;font-weight:800}
.hrx .ch-t{margin-top:0}
.hrx .ch-t thead th{padding:8px 8px}
.hrx .ch-t tr.ch-sub th{font-size:12px;font-weight:400;background:#fff}
.hrx .ch-t tbody th,.hrx .ch-t td{padding:7px 8px}
.hrx .ch-t .y26{font-size:15px}.hrx .ch-t .y25{font-size:14px}
.hrx .ch-note{margin-top:16px;font-size:15px;color:#4a5965;line-height:1.6;max-width:1000px;border-right:3px solid #C9A86A;padding-right:12px}
@media(max-width:1000px){.hrx .ch-grid{grid-template-columns:1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-funnel".*?</section>', s, re.S)
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
print("slides:", total, "WA", wi, wh, "Adam", ai, ah)
