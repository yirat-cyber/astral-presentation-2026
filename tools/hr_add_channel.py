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

# May-Sep totals, row "פייסבוק/אינסטגרם"
WA_INQ, WA_HIRED = 618, 34      # 2025, campaigns to WhatsApp
AD_INQ, AD_HIRED = 1649, 18     # 2026, campaigns to the Adam system

per_wa = WA_INQ / WA_HIRED      # inquiries needed per hire
per_ad = AD_INQ / AD_HIRED
rate_wa = WA_HIRED / WA_INQ
rate_ad = AD_HIRED / AD_INQ

def row(label, wa, ad, wa_w, ad_w, badge, note):
    return (f'<div class="cw-row reveal"><div class="cw-head"><b>{label}</b><span class="chg">{badge}</span></div>'
            f'<div class="cw-bars">'
            f'<div class="cw-line wa"><span class="cw-name">וואטסאפ</span><div class="cw-track"><div class="cw-fill" style="width:{wa_w:.0f}%"></div></div><span class="cw-val"><bdi>{wa}</bdi></span></div>'
            f'<div class="cw-line ad"><span class="cw-name">מערכת אדם</span><div class="cw-track"><div class="cw-fill" style="width:{ad_w:.0f}%"></div></div><span class="cw-val"><bdi>{ad}</bdi></span></div>'
            f'</div><p>{note}</p></div>')

rows = (
    row("עובדים שגויסו", WA_HIRED, AD_HIRED, 100, AD_HIRED / WA_HIRED * 100,
        "כמעט פי 2", f"יותר עובדים, משליש מהפניות ({WA_INQ:,} מול {AD_INQ:,})")
    + row("מכל 100 פונים, כמה גויסו", f"{rate_wa * 100:.1f}", f"{rate_ad * 100:.1f}", 100, rate_ad / rate_wa * 100,
          f"פי {rate_wa / rate_ad:.0f}", "פונה מוואטסאפ הוא מועמד רציני יותר")
    + row("כמה פניות צריך לכל עובד אחד", f"{per_wa:.0f}", f"{per_ad:.0f}", per_wa / per_ad * 100, 100,
          f"פי {per_ad / per_wa:.0f} פחות", "פחות זמן של רכזות הגיוס על פניות שלא מתקדמות")
)

slide = f'''<section class="slide sand hrx" id="hr-channel" data-dot="וואטסאפ מול מערכת אדם">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">לאן הקמפיין מוביל · פייסבוק ואינסטגרם · מאי–ספטמבר</div>
<h2 class="reveal d1">וואטסאפ מביא עובדים. טופס מביא פניות.</h2>
<p class="cw-lead reveal d1">אותם חודשים, אותו ערוץ פרסום. ב־2025 הקמפיינים הובילו לשיחה בוואטסאפ, וב־2026 לטופס במערכת אדם.</p>
<div class="cw-grid">{rows}</div>
<p class="ch-note reveal d5">למה זה עובד: בוואטסאפ המועמד כותב, שואל ומקבל תשובה מאדם. זו כבר תחילת ראיון, ואפשר לסנן בה מרחק, זמינות וניסיון. טופס ממלאים בלחיצה, בלי מחויבות.</p>
<p class="org-src reveal d5">מקור: דוח הגיוס של אסטרל, שורת ״פייסבוק/אינסטגרם״, מאי–ספטמבר 2025 (וואטסאפ) מול מאי–ספטמבר 2026 (מערכת אדם). ההשוואה בין שנים שונות, ולכן גם שוק העבודה והמשרות הפתוחות יכולים להשפיע.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · channel (WhatsApp vs Adam) ===== */
#hr-channel{padding-top:88px;padding-bottom:30px}
#hr-channel h2{font-size:clamp(30px,3.3vw,48px)}
.hrx .cw-lead{font-size:clamp(15px,1.3vw,18px);color:#4a5965;margin-top:6px}
.hrx .cw-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:28px}
.hrx .cw-row{background:#fff;border:1px solid #e6dfcf;border-top:3px solid #C9A86A;border-radius:16px;padding:26px 24px;display:flex;flex-direction:column;gap:22px}
.hrx .cw-head{display:flex;justify-content:space-between;align-items:center;gap:10px}
.hrx .cw-head b{font-size:20px;color:#0b1622;line-height:1.3}
.hrx .cw-head .chg{white-space:nowrap}
.hrx .cw-bars{display:flex;flex-direction:column;gap:16px}
.hrx .cw-line{display:grid;grid-template-columns:84px 1fr 70px;align-items:center;gap:10px}
.hrx .cw-name{font-size:15px;color:#4a5965}
.hrx .cw-line.wa .cw-name{color:#0b1622;font-weight:700}
.hrx .cw-track{height:40px;background:#f3efe6;border-radius:6px;overflow:hidden}
.hrx .cw-fill{height:100%;border-radius:6px}
.hrx .cw-line.wa .cw-fill{background:#C9A86A}
.hrx .cw-line.ad .cw-fill{background:#cfd7de}
.hrx .cw-val{font-size:36px;font-weight:800;color:#0b1622;text-align:left}
.hrx .cw-line.ad .cw-val{font-size:24px;color:#7C90A2}
.hrx .cw-row p{margin:0;font-size:15px;color:#4a5965;line-height:1.5;border-top:1px solid #efe9dc;padding-top:10px}
.hrx .ch-note{margin-top:18px;font-size:15px;color:#4a5965;line-height:1.6;max-width:1000px;border-right:3px solid #C9A86A;padding-right:12px}
@media(max-width:1000px){.hrx .cw-grid{grid-template-columns:1fr}}
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
print("slides:", total, f"per hire {per_wa:.1f} vs {per_ad:.1f}; rate {rate_wa:.3f} vs {rate_ad:.3f}")
