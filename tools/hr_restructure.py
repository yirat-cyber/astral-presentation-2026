"""One-off: turn the HR copy of the deck into an HR-only year summary.
Usage: python3 -I tools/hr_restructure.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'
ASTRAL = '<img class="brand" src="media/aef607b7d4.png" alt="Astral Hotels">'

def ph(text):
    """Visible placeholder for data still missing."""
    return f'<span class="ph">[{text}]</span>'

# ---------- new slides ----------
problem = f'''<section class="slide sand hrx" id="hr-problem" data-dot="האתגר · סוף 2024">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">נקודת הפתיחה · סוף 2024</div>
<h2 class="reveal d1">האתגר: עובדים באים והולכים</h2>
<p class="lead reveal d2">כשהתחלנו לעבוד עם אסטרל, הבנו מה הכי כואב לצוות משאבי האנוש: באילת עובדי מלונות מחליפים מקום עבודה בלי לחשוב פעמיים — וגם עובדי אסטרל.</p>
<div class="cards">
<article class="card reveal d2"><span class="n">01</span><h3>שוק פתוח, מעבר בלי חיכוך</h3><p>עשרות מלונות במרחק הליכה. עובד שמקבל הצעה טובה יותר — פשוט עובר.</p></article>
<article class="card reveal d3"><span class="n">02</span><h3>אין גאוות יחידה</h3><p>עובדים הרגישו שהם עובדים ״במלון״, לא ״באסטרל״. לא היה חיבור רגשי לרשת.</p></article>
<article class="card reveal d4"><span class="n">03</span><h3>שימור הוא הבעיה האמיתית</h3><p>כל עזיבה מחזירה את הגיוס לנקודת אפס — ועולה לרשת בזמן, בכסף ובאיכות השירות.</p></article>
</div>
<p class="strip reveal d5">המטרה שלנו הייתה ברורה: <b>לבנות לעובדים סיבה להישאר.</b></p>
</div></section>'''

shift = f'''<section class="slide dark hrx hrx-dark" id="hr-shift" data-dot="השינוי האסטרטגי">{ASTRAL}{SIG}<div class="wrap">
<div class="kick reveal">השינוי האסטרטגי</div>
<h2 class="reveal d1">הפסקנו לפרסם משרות.<br><span class="gold">התחלנו לספר את הסיפור של האנשים.</span></h2>
<p class="lead reveal d2">הסושיאל של Astral HR הפך מלוח דרושים למותג מעסיק — שבו העובדים הם הגיבורים.</p>
<div class="fromto">
<div class="ft-head reveal d2"><span>פעם</span><span></span><span>היום</span></div>
<div class="ft-row reveal d3"><span class="old">מודעת ״דרושים״</span><span class="ar">←</span><span class="new">סיפור של עובד אמיתי</span></div>
<div class="ft-row reveal d4"><span class="old">״יש משרה פנויה״</span><span class="ar">←</span><span class="new">״יש פה קריירה״</span></div>
<div class="ft-row reveal d5"><span class="old">עבודה במלון</span><span class="ar">←</span><span class="new">שייכות לרשת אחת גדולה</span></div>
<div class="ft-row reveal d6"><span class="old">גיוס חד־פעמי</span><span class="ar">←</span><span class="new">מותג מעסיק שעובד כל השנה</span></div>
</div>
</div></section>'''

pillars = f'''<section class="slide sand hrx" id="hr-pillars" data-dot="שלושת עמודי התוכן">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">איך עשינו את זה</div>
<h2 class="reveal d1">שלושה עמודי תוכן</h2>
<div class="cards">
<article class="card reveal d2"><span class="n">01</span><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17.5" cy="9" r="2.4"/><path d="M16 14.2c2.9.3 5 2.6 5 5.8"/></svg></div><h3>העובדים בפרונט</h3><p>הפנים של הפיד הן העובדים עצמם — חדרניות, טבחים, מלצרים ומנהלים. לא דוגמנים, לא סטוק.</p></article>
<article class="card reveal d3"><span class="n">02</span><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4v-6H4zM10 20h4V9h-4zM16 20h4V4h-4z"/></svg></div><h3>קידום ברשת</h3><p>דיברנו הרבה ובקול על מסלולי ההתקדמות באסטרל: אפשר להתחיל מלמטה ולהגיע רחוק.</p></article>
<article class="card reveal d4"><span class="n">03</span><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l2.6 5.3 5.9.9-4.3 4.1 1 5.8L12 16.4 6.8 19.1l1-5.8L3.5 9.2l5.9-.9z"/></svg></div><h3>הוכחות מהשטח</h3><p>לא הבטחות — סיפורים אמיתיים של עשרות עובדים שהתחילו בתפקידים זוטרים ומכהנים היום בתפקידים בכירים.</p></article>
</div>
</div></section>'''

def story(i):
    return (f'<article class="story reveal d{i+1}"><div class="avatar ph-box">תמונה</div>'
            f'<h3>{ph("שם העובד/ת")}</h3>'
            f'<div class="path"><span class="from">{ph("תפקיד התחלתי")}</span><span class="down">↓</span>'
            f'<span class="to">{ph("תפקיד היום")}</span></div>'
            f'<div class="yrs">{ph("X שנים")} ברשת</div></article>')

stories = f'''<section class="slide sand hrx" id="hr-stories" data-dot="מזוטר לבכיר">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">הוכחות מהשטח</div>
<h2 class="reveal d1">מזוטר לבכיר</h2>
<p class="lead reveal d2">עשרות עובדים שהתחילו בתפקידים זוטרים — ומנהלים היום ברשת. אלה הסיפורים שהבאנו לפיד.</p>
<div class="stories">{''.join(story(i) for i in range(1, 5))}</div>
</div></section>'''

results = f'''<section class="slide sand hrx" id="hr-results" data-dot="התוצאה · גיוס">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">התוצאה · ינואר–אוקטובר 2026</div>
<h2 class="reveal d1">יכולת הגיוס של אסטרל השתפרה פלאים</h2>
<div class="res">
<div class="res-hero reveal d2"><div class="big">{ph("X,XXX")}</div><div class="big-lbl">פניות של מועמדים</div><p>התוכן הקריאייטיבי בולט בפיד — ומביא אלפי מועמדים לפנות לאסטרל.</p></div>
<div class="res-side">
<div class="mini reveal d3"><div class="mv">{ph("X,XXX")}</div><div class="ml">שיחות וואטסאפ שנפתחו עם מועמדים</div></div>
<div class="mini reveal d4"><div class="mv">{ph("+XX%")}</div><div class="ml">שינוי בכמות הפניות מול 2024</div></div>
<div class="mini reveal d5"><div class="mv">{ph("נתון שימור")}</div><div class="ml">תחלופה / ותק ממוצע של עובדים</div></div>
</div>
</div>
</div></section>'''

summary = f'''<section class="slide sand hrx" id="hr-next" data-dot="סיכום ומה הלאה">{HRLOGO}{SIG}<div class="wrap">
<div class="kick reveal">לסיכום</div>
<h2 class="reveal d1">מותג מעסיק שעובדים גאים בו</h2>
<div class="two">
<div class="col reveal d2"><h3>מה בנינו ב־2026</h3><ul>
<li>העובדים הפכו לפנים של Astral HR</li>
<li>הקידום ברשת הוא כבר לא הבטחה — הוא סיפור עם שמות ופנים</li>
<li>הפיד מביא אלפי מועמדים שרוצים להיות חלק מהרשת</li>
</ul></div>
<div class="col accent reveal d3"><h3>מה הלאה · 2027</h3><ul>
<li>להפוך את ״מזוטר לבכיר״ לסדרה קבועה</li>
<li>להרחיב את תוכנית השגרירים לכל מלונות הרשת</li>
<li>למדוד יחד עם HR את ההשפעה על שימור העובדים</li>
</ul></div>
</div>
</div></section>'''

css = '''<style>
/* ===== HR year summary slides ===== */
.hrx{background:#f5f4f0;color:#0b1622;padding:clamp(90px,11vh,120px) 7vw 70px}
.hrx .wrap{max-width:1180px}
.hrx .kick{color:#95743b;font-size:14px;letter-spacing:.06em;font-weight:700;display:flex;align-items:center;gap:11px;margin-bottom:14px}
.hrx .kick::before{content:"";width:28px;height:2px;background:currentColor}
.hrx h2{font-size:clamp(32px,3.6vw,52px);line-height:1.18;color:#0b1622;font-weight:800}
.hrx .lead{font-size:clamp(17px,1.5vw,21px);color:#4a5965;line-height:1.6;margin-top:16px;max-width:820px}
.hrx .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:22px;margin-top:36px}
.hrx .card{background:#fff;border:1px solid #e6dfcf;border-radius:18px;padding:26px 26px 28px;position:relative;overflow:hidden;box-shadow:0 10px 30px rgba(11,22,34,.06)}
.hrx .card::before{content:"";position:absolute;top:0;right:0;width:100%;height:3px;background:linear-gradient(90deg,#C9A86A,transparent)}
.hrx .card .n{font-weight:800;color:#A6864F;font-size:20px}
.hrx .card .ic{width:46px;height:46px;color:#A6864F;margin:16px 0 4px}
.hrx .card .ic svg{width:100%;height:100%}
.hrx .card h3{font-size:22px;margin:12px 0 10px;color:#0b1622}
.hrx .card p{font-size:15.5px;line-height:1.6;color:#4a5965}
.hrx .strip{margin-top:30px;border-right:3px solid #C9A86A;padding:8px 20px;font-size:clamp(18px,1.6vw,22px);line-height:1.6}
.hrx .strip b{color:#95743b}
/* dark emphasis slide */
.hrx.hrx-dark{background:radial-gradient(120% 80% at 88% -8%,rgba(201,168,106,.18),transparent 52%),linear-gradient(160deg,#0B1622,#0E1E2E 60%,#0B1826);color:#EDE4D3}
.hrx-dark .kick{color:#C9A86A}
.hrx-dark h2{color:#fff;font-size:clamp(34px,4.2vw,60px)}
.hrx-dark h2 .gold{color:#DEC48A;font-weight:400}
.hrx-dark .lead{color:#9DB0C0}
.hrx .fromto{margin-top:34px;display:flex;flex-direction:column;max-width:900px}
.hrx .ft-head,.hrx .ft-row{display:grid;grid-template-columns:1fr 50px 1.3fr;align-items:center;gap:14px}
.hrx .ft-head span{font-size:13px;letter-spacing:.06em;font-weight:700;color:#7C90A2;padding-bottom:10px}
.hrx .ft-row{padding:15px 0;border-top:1px solid #22405A}
.hrx .ft-row .old{font-size:clamp(16px,1.4vw,19px);color:#7C90A2;text-decoration:line-through;text-decoration-color:rgba(124,144,162,.5)}
.hrx .ft-row .ar{color:#C9A86A;font-size:20px;text-align:center}
.hrx .ft-row .new{font-size:clamp(18px,1.7vw,23px);color:#DEC48A;font-weight:700}
/* stories */
.hrx .stories{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-top:34px}
.hrx .story{background:#fff;border:1px solid #e6dfcf;border-radius:18px;padding:24px 20px;text-align:center;box-shadow:0 10px 30px rgba(11,22,34,.06)}
.hrx .story .avatar{width:96px;height:96px;border-radius:50%;margin:0 auto 14px;display:flex;align-items:center;justify-content:center;font-size:13px;color:#95743b}
.hrx .story h3{font-size:18px;margin-bottom:12px}
.hrx .story .path{display:flex;flex-direction:column;align-items:center;gap:4px;font-size:15px}
.hrx .story .from{color:#7C90A2}
.hrx .story .down{color:#C9A86A;font-size:18px}
.hrx .story .to{color:#0b1622;font-weight:800}
.hrx .story .yrs{margin-top:12px;font-size:13px;color:#7C90A2}
/* results */
.hrx .res{display:grid;grid-template-columns:1.2fr 1fr;gap:24px;margin-top:34px;align-items:stretch}
.hrx .res-hero{background:linear-gradient(150deg,rgba(201,168,106,.22),rgba(201,168,106,.06));border:1px solid rgba(166,134,79,.45);border-radius:20px;padding:34px;display:flex;flex-direction:column;justify-content:center}
.hrx .res-hero .big{font-size:clamp(70px,9vw,140px);font-weight:800;line-height:1;color:#95743b;direction:ltr;text-align:right}
.hrx .res-hero .big-lbl{font-size:clamp(20px,1.9vw,26px);font-weight:700;margin-top:12px}
.hrx .res-hero p{font-size:16px;color:#4a5965;margin-top:12px;line-height:1.6}
.hrx .res-side{display:flex;flex-direction:column;gap:14px}
.hrx .mini{background:#fff;border:1px solid #e6dfcf;border-radius:14px;padding:18px 22px;flex:1;display:flex;flex-direction:column;justify-content:center}
.hrx .mini .mv{font-size:clamp(26px,2.6vw,36px);font-weight:800;color:#0b1622;direction:ltr;text-align:right}
.hrx .mini .ml{font-size:14.5px;color:#4a5965;margin-top:4px}
/* summary */
.hrx .two{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:34px}
.hrx .col{background:#fff;border:1px solid #e6dfcf;border-radius:18px;padding:28px 30px}
.hrx .col.accent{background:#0b1622;border-color:#0b1622;color:#EDE4D3}
.hrx .col h3{font-size:22px;margin-bottom:16px;color:inherit}
.hrx .col.accent h3{color:#DEC48A}
.hrx .col ul{list-style:none;display:flex;flex-direction:column;gap:12px}
.hrx .col li{font-size:17px;line-height:1.5;padding-right:22px;position:relative}
.hrx .col li::before{content:"✦";position:absolute;right:0;color:#C9A86A;font-size:13px;top:3px}
/* placeholders for data still to come */
.ph{background:rgba(201,168,106,.16);outline:1.5px dashed #C9A86A;outline-offset:2px;border-radius:6px;padding:0 6px;color:#95743b}
.ph-box{background:rgba(201,168,106,.12);border:1.5px dashed #C9A86A}
@media(max-width:768px){
  .hrx{padding:84px 22px 76px}
  .hrx .cards,.hrx .res,.hrx .two{grid-template-columns:1fr}
  .hrx .stories{grid-template-columns:1fr 1fr;gap:12px}
  .hrx .ft-head,.hrx .ft-row{grid-template-columns:1fr 30px 1.2fr}
}
</style>'''

# ---------- restructure ----------
sections = list(re.finditer(r'<section\b.*?</section>', s, re.S))
by_id = {re.search(r'id="([^"]+)"', m.group(0)).group(1): m.group(0) for m in sections}

hero = by_id["hero"]
hero = hero.replace('<div class="hero-period">מחצית ראשונה 2026</div>', '<div class="hero-period">סיכום שנה · ינואר–אוקטובר 2026</div>')
hero = hero.replace('<span class="hero-title-line">בואו נסכם חציון מהמם</span>', '<span class="hero-title-line">שנה של שינוי אסטרטגי</span>')
hero = hero.replace('<span class="hero-subtitle-line">בפעילות הסושיאל של אסטרל</span>', '<span class="hero-subtitle-line">Astral HR · מגייסים לעבודה, בונים בית</span>')
hero = hero.replace('<div class="hero-bottom-period">ינואר–יוני 2026 מול התקופה המקבילה ב־2025</div>', '<div class="hero-bottom-period">ינואר–אוקטובר 2026 · מצגת לסיכום שנה</div>')
assert "שנה של שינוי" in hero and "ינואר–אוקטובר" in hero

creatives = by_id["hr-creatives"].replace('data-dot="ועכשו קצת קריאייטיבים"', 'data-dot="הקריאייטיב בפיד"')
creatives = creatives.replace('<div class="shead"><h2>ועכשו קצת קריאייטיבים</h2></div>',
    '<div class="shead"><h2>הקריאייטיב שבולט בפיד</h2></div>')
assert "הקריאייטיב שבולט" in creatives

new_order = [by_id["partnership-open"], hero, problem, shift, pillars, stories,
             creatives, by_id["hr-ambassadors"], results, summary, by_id["partnership-close"]]

total = len(new_order)
numbered = []
for i, sec in enumerate(new_order, 1):
    sec = re.sub(r'<span class="slide-page-number"[^>]*>.*?</span>', '', sec)
    sec = sec[:-len('</section>')] + f'<span class="slide-page-number" aria-label="שקף {i} מתוך {total}">{i} / {total}</span></section>'
    numbered.append(sec)

start, end = sections[0].start(), sections[-1].end()
s = s[:start] + "\n\n".join(numbered) + s[end:]

# drop scripts / dialog tied to removed slides
for sid in ["journey-bridge", "guest-comments", "paid-key-metrics"]:
    s, n = re.subn(r"<script>\(\(\)=>\{const s=document\.getElementById\('" + sid + r"'\).*?</script>", "", s, flags=re.S)
    if n == 0:
        s = re.sub(r"<script>(?:(?!</script>).)*getElementById\('" + sid + r"'\)(?:(?!</script>).)*</script>", "", s, flags=re.S)
s = re.sub(r'<dialog class="couple-dialog">.*?</dialog><script>.*?</script>', "", s, flags=re.S)

s = s.replace("</head>", css + "\n</head>", 1)
s = s.replace("<title>אסטרל · מצגת ביצועי סושיאל 2026</title>", "<title>סיכום 2026 · Astral HR</title>")

open(path, "w", encoding="utf-8").write(s)
print("slides:", total)
