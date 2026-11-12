"""Replace the hr-signs slide body with real comment screenshots (no small counts).
Usage: python3 -I tools/hr_signs_v2.py "<deck html>"
Images: media/cm-*.png, screenshots of public Instagram comments, Nov 2026.
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'

SHOTS = [
    ("media/cm-ayala.png", "רילס עם איילה חן מועלם, מנכ״לית אריאה"),
    ("media/cm-adi.png", "הכוכבים של אסטרל: עדי פלד, מנהלת הדרכה ורווחה"),
    ("media/cm-galina.png", "גלינה, שעלתה מקזחסטן לאילת"),
    ("media/cm-kim.png", "רילס שגרירים, הפוסט המוביל של השנה"),
]
shots = "".join(
    f'<figure class="cm reveal d{i+2}"><figcaption>{c}</figcaption><div class="cm-shot"><img src="{src}" alt="צילום מסך של תגובות: {c}"></div></figure>'
    for i, (src, c) in enumerate(SHOTS))

slide = f'''<section class="slide sand hrx" id="hr-signs" data-dot="גאוות יחידה · התגובות">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">גאוות יחידה · מהתגובות בפיד</div>
<h2 class="reveal d1">ככה מגיבים לתוכן שלנו</h2>
<p class="cm-lead reveal d1">עמיתים ובני משפחה מפרגנים, ומועמדים שואלים איך מצטרפים.</p>
<div class="cm-row">{shots}</div>
<p class="org-src reveal d6">צילומי מסך של תגובות ציבוריות בעמוד @work_at_astral, 2026.</p>
</div></section>'''

CSS = '''<style>
/* ===== HR · signs v2: comment screenshots ===== */
.hrx .cm-lead{font-size:clamp(16px,1.4vw,19px);color:#4a5965;margin-top:8px}
.hrx .cm-row{display:grid;grid-template-columns:repeat(4,1fr);gap:clamp(14px,1.6vw,24px);margin-top:22px;align-items:start}
.hrx .cm{margin:0;display:flex;flex-direction:column;gap:8px}
.hrx .cm figcaption{font-size:14px;font-weight:700;color:#0b1622;line-height:1.35;min-height:2.7em}
.hrx .cm-shot{background:#fff;border:1px solid #e6dfcf;border-radius:14px;overflow:hidden;line-height:0;box-shadow:0 10px 26px rgba(11,22,34,.12)}
.hrx .cm-shot img{display:block;width:100%;height:auto;max-height:52vh;object-fit:cover;object-position:top}
@media(max-width:900px){.hrx .cm-row{grid-template-columns:1fr 1fr}}
@media(max-width:560px){.hrx .cm-row{grid-template-columns:1fr}}
</style>'''

m = re.search(r'<section\b[^>]*id="hr-signs".*?</section>', s, re.S)
num = re.search(r'<span class="slide-page-number".*?</span>', m.group(0)).group(0)
s = s[:m.start()] + slide[:-len("</section>")] + num + "</section>" + s[m.end():]
s = s.replace("</head>", CSS + "\n</head>", 1)
open(path, "w", encoding="utf-8").write(s)
print("ok")
