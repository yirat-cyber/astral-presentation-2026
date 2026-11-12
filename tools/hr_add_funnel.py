"""Facebook/Instagram candidate inquiries, Jan-Oct 2025 vs 2026 (inquiries only, no hiring data), after hr-results.
Usage: python3 -I tools/hr_add_funnel.py "<deck html>"   (rebuilds the slide if it already exists)
Data: Astral HR report "דוחות שיווק לשנת 2026", sheets ריכוז פניות / ריכוז פניות 2025,
row "פייסבוק/אינסטגרם" only (per client instruction). Jan-Apr 2025 row also includes the company site.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()
if 'id="hr-funnel"' in s:  # rebuild: drop the old slide and its CSS
    s = re.sub(r'<section\b[^>]*id="hr-funnel".*?</section>\s*', '', s, flags=re.S)
    s = re.sub(r'<style>\s*/\* ===== HR · funnel.*?</style>\s*', '', s, flags=re.S)

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

# month, inquiries 2025, inquiries 2026 (None = not reported)
MONTHS = [
    ("ינואר", 52, 512), ("פברואר", 79, 289), ("מרץ", 82, None), ("אפריל", 24, 366),
    ("מאי", 71, 449), ("יוני", 126, 334), ("יולי", 223, 328), ("אוגוסט", 136, 362),
    ("ספטמבר", 62, 176), ("אוקטובר", 104, 159),
]
t25 = sum(a for _, a, _ in MONTHS)
t26 = sum(b or 0 for _, _, b in MONTHS)
peak = max(max(a, b or 0) for _, a, b in MONTHS)
f = lambda v: '<span class="fn-na">לא דווח</span>' if v is None else f"{v:,}"

def bar(v, cls):
    return f'<div class="fn-bar {cls}" style="width:{(v or 0) / peak * 100:.1f}%"></div>'

rows = "".join(
    f'<tr><th>{n}</th><td class="y25">{f(a)}</td><td class="y26">{f(b)}</td>'
    f'<td class="fn-bars">{bar(a, "b25")}{bar(b, "b26")}</td></tr>'
    for n, a, b in MONTHS)
rows += (f'<tr class="hl"><th>סה״כ</th><td class="y25">{t25:,}</td><td class="y26">{t26:,}</td>'
         f'<td><span class="chg">פי {t26 / t25:.1f}</span></td></tr>')

slide = f'''<section class="slide sand hrx" id="hr-funnel" data-dot="פניות מהסושיאל">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">פניות של מועמדים · פייסבוק ואינסטגרם · ינואר–אוקטובר</div>
<h2 class="reveal d1">פי 3 יותר מועמדים פנו אלינו דרך הסושיאל</h2>
<div class="fn-grid">
<table class="org-t fn-t reveal d2">
<thead><tr><th></th><th>2025</th><th>2026</th><th class="fn-legend"><i class="b25"></i>2025 <i class="b26"></i>2026</th></tr></thead>
<tbody>{rows}</tbody>
</table>
<div class="fn-yoy reveal d3"><b>ינואר–אוקטובר · 2025 מול 2026</b>
<div class="fn-big"><bdi>{t26:,}</bdi></div>
<div class="fn-lbl">פניות של מועמדים ב־2026</div>
<div class="fn-was">לעומת <bdi>{t25:,}</bdi> ב־2025</div>
<span class="chg">פי {t26 / t25:.1f}</span>
</div>
</div>
<p class="org-src reveal d4">מקור: דוח הגיוס של אסטרל, שורת ״פייסבוק/אינסטגרם״ בלבד. ינואר–אפריל 2025 כולל גם פניות מאתר החברה. במרץ 2026 לא דווחו נתונים.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · funnel (FB/IG inquiries, year over year) ===== */
#hr-funnel{padding-top:88px;padding-bottom:30px}
#hr-funnel h2{font-size:clamp(28px,3vw,44px)}
.hrx .fn-grid{display:grid;grid-template-columns:1.6fr 1fr;gap:24px;margin-top:22px;align-items:stretch}
.hrx .fn-t{margin-top:0}
.hrx .fn-t thead th{padding:10px 12px}
.hrx .fn-t tbody th,.hrx .fn-t td{padding:6px 12px}
.hrx .fn-t .y26{font-size:15px}.hrx .fn-t .y25{font-size:14px}
.hrx .fn-na{font-size:12px;font-weight:400;color:#9aa8b5}
.hrx .fn-t td.fn-bars{width:42%;text-align:right}
.hrx .fn-bar{height:7px;border-radius:4px;margin:2px 0}
.hrx .fn-bar.b25,.hrx .fn-legend i.b25{background:#cfd7de}
.hrx .fn-bar.b26,.hrx .fn-legend i.b26{background:#C9A86A}
.hrx .fn-legend{font-weight:400}
.hrx .fn-legend i{display:inline-block;width:10px;height:10px;border-radius:3px;margin:0 10px 0 4px;vertical-align:middle}
.hrx .fn-yoy{background:#0b1622;color:#fff;border-radius:16px;padding:26px 28px;display:flex;flex-direction:column;justify-content:center;gap:8px}
.hrx .fn-yoy b{font-size:13px;color:#C9A86A;font-weight:700}
.hrx .fn-big{font-size:clamp(64px,7vw,110px);font-weight:800;line-height:1;color:#C9A86A}
.hrx .fn-lbl{font-size:20px;font-weight:700}
.hrx .fn-was{font-size:16px;color:#c9d3dc}
.hrx .fn-yoy .chg{align-self:flex-start;margin-top:6px}
@media(max-width:900px){.hrx .fn-grid{grid-template-columns:1fr}.hrx .fn-t td.fn-bars,.hrx .fn-legend{display:none}}
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
print("slides:", total, "totals:", t25, t26)
