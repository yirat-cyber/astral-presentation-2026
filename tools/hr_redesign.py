"""Editorial redesign of the HR summary slides (replaces the .hrx slides + their CSS).
Usage: python3 -I tools/hr_redesign.py "<deck html>"
"""
import re, sys

path = sys.argv[1]
s = open(path, encoding="utf-8").read()

SIG = '<img class="agency-signature" src="media/8974e87165.svg" alt="לוגו משרד הפרסום">'
HRLOGO = '<img class="brand hr-brand" alt="Work at Astral Hotels" src="media/411ad1fcab.svg">'
ASTRAL = '<img class="brand" src="media/aef607b7d4.png" alt="Astral Hotels">'

IMG = {
    "board_woman": "media/8692a76b92.jpg",
    "board_cap": "media/c69f3472f4.jpg",
    "board_man": "media/975d630e41.jpg",
    "board_woman2": "media/229c3f35e8.jpg",
    "lobby": "media/cc57f86409.jpg",
    "ambassador": "media/ddcd4d7fff.jpg",
    "team_table": "media/e26c3178b3.jpg",
    "office": "media/8e383774e7.jpg",
}

def ph(text):
    return f'<span class="ph">{text}</span>'

def photo(key, cap="", pos="50% 30%", cls=""):
    c = f'<figcaption>{cap}</figcaption>' if cap else ""
    return f'<figure class="ed-photo {cls}"><img src="{IMG[key]}" alt="{cap or "עובדי אסטרל"}" style="object-position:{pos}">{c}</figure>'

SLIDES = {}

SLIDES["hr-problem"] = f'''<section class="slide sand hrx" id="hr-problem" data-dot="האתגר · סוף 2024">{HRLOGO}{SIG}<div class="wrap ed-split">
<div class="ed-text">
<p class="ed-tag reveal">סוף 2024. נקודת הפתיחה.</p>
<h2 class="reveal d1">עובדים באים<br>והולכים.</h2>
<p class="ed-lead reveal d2">כשהתחלנו לעבוד עם אסטרל, הבנו מה הכי כואב לצוות משאבי האנוש. באילת עובדי מלונות מחליפים מקום עבודה בלי לחשוב פעמיים. גם עובדי אסטרל.</p>
<div class="ed-facts reveal d3">
<div><b>שוק פתוח</b><span>עשרות מלונות במרחק הליכה. הצעה טובה יותר, ועוברים.</span></div>
<div><b>אין גאוות יחידה</b><span>עובדים הרגישו שהם עובדים ״במלון״, לא ״באסטרל״.</span></div>
<div><b>שימור</b><span>כל עזיבה מחזירה את הגיוס לנקודת ההתחלה.</span></div>
</div>
<p class="ed-goal reveal d4">המטרה שלנו: לתת לעובדים סיבה להישאר.</p>
</div>
<div class="ed-media reveal d2">{photo("team_table", "צוות אסטרל, אילת", "50% 60%")}</div>
</div></section>'''

SLIDES["hr-shift"] = f'''<section class="slide dark hrx hrx-dark" id="hr-shift" data-dot="השינוי האסטרטגי">{ASTRAL}{SIG}<div class="wrap ed-split ed-split-wide">
<div class="ed-text">
<p class="ed-tag reveal">השינוי האסטרטגי</p>
<h2 class="reveal d1">הפסקנו לפרסם משרות.<br><em>התחלנו לספר על האנשים.</em></h2>
<table class="ed-ft reveal d3">
<thead><tr><th>פעם</th><th>היום</th></tr></thead>
<tbody>
<tr><td>מודעת ״דרושים״</td><td>סיפור של עובד אמיתי</td></tr>
<tr><td>״יש משרה פנויה״</td><td>״יש פה קריירה״</td></tr>
<tr><td>עבודה במלון</td><td>שייכות לרשת</td></tr>
<tr><td>קמפיין גיוס חד־פעמי</td><td>מותג מעסיק, כל השנה</td></tr>
</tbody></table>
</div>
<div class="ed-mosaic reveal d2">
{photo("board_woman", "", "50% 70%")}{photo("board_cap", "", "50% 60%")}{photo("board_man", "", "50% 65%")}{photo("board_woman2", "", "50% 70%")}
</div>
</div></section>'''

SLIDES["hr-pillars"] = f'''<section class="slide sand hrx" id="hr-pillars" data-dot="איך עשינו את זה">{HRLOGO}{SIG}<div class="wrap">
<div class="ed-head"><p class="ed-tag reveal">איך עשינו את זה</p><h2 class="reveal d1">שלושה דברים שחזרנו עליהם כל השנה</h2></div>
<div class="ed-cols">
<article class="reveal d2">{photo("lobby", "", "50% 35%")}<h3>העובדים בפרונט</h3><p>הפנים של הפיד הן העובדים עצמם: חדרניות, טבחים, מלצרים ומנהלים. בלי דוגמנים ובלי סטוק.</p></article>
<article class="reveal d3">{photo("board_man", "", "50% 55%")}<h3>קידום ברשת</h3><p>דיברנו הרבה ובקול על מסלולי ההתקדמות. באסטרל אפשר להתחיל מלמטה ולהגיע רחוק.</p></article>
<article class="reveal d4">{photo("ambassador", "", "50% 30%")}<h3>הוכחות מהשטח</h3><p>לא הבטחות. עשרות עובדים שהתחילו בתפקידים זוטרים ומכהנים היום בתפקידים בכירים.</p></article>
</div>
</div></section>'''

def row(i):
    return (f'<li class="reveal d{i+1}"><span class="st-photo">תמונה</span>'
            f'<span class="st-name">{ph("שם העובד/ת")}<small>{ph("X")} שנים ברשת</small></span>'
            f'<span class="st-path"><span class="st-from">{ph("תפקיד התחלתי")}</span><span class="st-ar">←</span>'
            f'<span class="st-to">{ph("התפקיד היום")}</span></span></li>')

SLIDES["hr-stories"] = f'''<section class="slide sand hrx" id="hr-stories" data-dot="מזוטר לבכיר">{HRLOGO}{SIG}<div class="wrap">
<div class="ed-head ed-head-row"><div><p class="ed-tag reveal">הוכחות מהשטח</p><h2 class="reveal d1">מזוטר לבכיר</h2></div>
<p class="ed-lead reveal d2">עשרות עובדים התחילו בתפקידים זוטרים ומנהלים היום ברשת. אלה כמה מהסיפורים שהבאנו לפיד.</p></div>
<ol class="ed-stories">{''.join(row(i) for i in range(1, 5))}</ol>
</div></section>'''

SLIDES["hr-results"] = f'''<section class="slide sand hrx" id="hr-results" data-dot="התוצאה · גיוס">{HRLOGO}{SIG}<div class="wrap">
<p class="ed-tag reveal">התוצאה · ינואר–אוקטובר 2026</p>
<div class="ed-big reveal d1"><span class="num">{ph("X,XXX")}</span><span class="what">פניות של מועמדים<br>לעבודה באסטרל</span></div>
<p class="ed-lead reveal d2">יכולת הגיוס של אסטרל השתפרה פלאים. התוכן בולט בפיד, ומועמדים פונים כי הם רוצים להיות חלק מהרשת.</p>
<div class="ed-stats reveal d3">
<div><b>{ph("X,XXX")}</b><span>שיחות וואטסאפ עם מועמדים</span></div>
<div><b>{ph("+XX%")}</b><span>פניות לעומת 2024</span></div>
<div><b>{ph("נתון שימור")}</b><span>תחלופה או ותק ממוצע</span></div>
</div>
</div></section>'''

SLIDES["hr-next"] = f'''<section class="slide sand hrx" id="hr-next" data-dot="סיכום ומה הלאה">{HRLOGO}{SIG}<div class="wrap">
<div class="ed-head"><p class="ed-tag reveal">לסיכום</p><h2 class="reveal d1">מותג מעסיק<br>שעובדים גאים בו.</h2></div>
<div class="ed-two">
<div class="reveal d2"><h3>מה בנינו ב־2026</h3><ol>
<li>העובדים הפכו לפנים של Astral HR.</li>
<li>הקידום ברשת הוא כבר לא הבטחה. יש לו שמות ופנים.</li>
<li>הפיד מביא אלפי מועמדים שרוצים לעבוד באסטרל.</li>
</ol></div>
<div class="reveal d3"><h3>ב־2027</h3><ol>
<li>״מזוטר לבכיר״ הופכת לסדרה קבועה.</li>
<li>תוכנית השגרירים מתרחבת לכל מלונות הרשת.</li>
<li>מודדים יחד עם HR את ההשפעה על שימור העובדים.</li>
</ol></div>
</div>
</div></section>'''

CSS = '''<style id="hr-editorial">
/* ===== HR summary · editorial ===== */
.hrx{background:#f3efe6;color:#14202b;padding:clamp(96px,12vh,124px) 7vw 64px}
.hrx .wrap{max-width:1240px}
.hrx h2,.hrx h3,.hrx .ed-big .num,.hrx .ed-stats b,.hrx .st-to,#hr-creatives h2,#hr-ambassadors h2{font-family:"Frank Ruhl Libre",Georgia,serif!important;letter-spacing:-.01em}
.hrx h2{font-size:clamp(40px,4.6vw,72px);line-height:1.02;font-weight:500!important;color:#14202b}
.hrx h2 em{font-style:normal;color:#9a7a42}
.hrx .ed-tag{font-size:14px;color:#6f6553;margin-bottom:18px}
.hrx .ed-lead{font-size:clamp(17px,1.45vw,20px);line-height:1.65;color:#3d4852;max-width:560px;margin-top:22px}
/* split text / photo */
.hrx .ed-split{display:grid;grid-template-columns:1.25fr .75fr;gap:clamp(30px,5vw,80px);align-items:center}
.hrx .ed-split-wide{grid-template-columns:1.2fr .8fr}
.hrx .ed-photo{margin:0;position:relative;overflow:hidden;background:#ddd5c5}
.hrx .ed-photo img{display:block;width:100%;height:100%;object-fit:cover;filter:saturate(.9) contrast(1.03)}
.hrx .ed-photo figcaption{font-size:12.5px;color:#6f6553;padding-top:10px;background:#f3efe6}
.hrx .ed-media{padding-top:40px}.hrx .ed-media .ed-photo img{height:min(58vh,540px)}
.hrx .ed-facts{display:grid;grid-template-columns:repeat(3,1fr);margin-top:38px;border-top:1px solid #cfc6b3}
.hrx .ed-facts div{padding:16px 0 0 18px;display:flex;flex-direction:column;gap:6px}
.hrx .ed-facts div+div{border-right:1px solid #cfc6b3;padding-right:18px}
.hrx .ed-facts b{font-size:16px;font-weight:700}
.hrx .ed-facts div>span{font-size:14.5px;line-height:1.55;color:#4b5560}
.hrx .ed-goal{margin-top:34px;font-family:"Frank Ruhl Libre",Georgia,serif!important;font-size:clamp(22px,2vw,28px);color:#9a7a42}
/* dark statement */
.hrx.hrx-dark{background:#0d1822;color:#e9e2d4}
.hrx-dark .ed-tag{color:#a89a80}
.hrx-dark h2{color:#f4efe5;font-size:clamp(40px,4.4vw,68px)}
.hrx-dark h2 em{color:#d4b47a}
.hrx .ed-ft{margin-top:40px;width:100%;max-width:640px;border-collapse:collapse}
.hrx .ed-ft th{font-size:13px;font-weight:600;color:#8d99a3;text-align:right;padding:0 0 10px}
.hrx .ed-ft td{padding:13px 0;border-top:1px solid rgba(233,226,212,.16);font-size:clamp(16px,1.35vw,19px);vertical-align:top}
.hrx .ed-ft td:first-child{color:#7d8992;width:44%;text-decoration:line-through;text-decoration-color:rgba(125,137,146,.55)}
.hrx .ed-ft td:last-child{color:#f4efe5}
.hrx .ed-mosaic{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.hrx .ed-mosaic .ed-photo img{height:min(32vh,300px)}
.hrx .ed-mosaic .ed-photo:nth-child(2),.hrx .ed-mosaic .ed-photo:nth-child(4){transform:translateY(28px)}
/* three columns with photos */
.hrx .ed-head h2{max-width:900px}
.hrx .ed-cols{display:grid;grid-template-columns:repeat(3,1fr);gap:clamp(20px,2.6vw,40px);margin-top:40px}
.hrx .ed-cols .ed-photo img{height:min(34vh,330px)}
.hrx .ed-cols h3{font-size:clamp(22px,1.9vw,28px);font-weight:500!important;margin:18px 0 8px}
.hrx .ed-cols p{font-size:15.5px;line-height:1.6;color:#4b5560}
/* stories list */
.hrx .ed-head-row{display:flex;justify-content:space-between;align-items:flex-end;gap:40px}
.hrx .ed-head-row .ed-lead{margin:0;max-width:440px}
.hrx .ed-stories{list-style:none;margin-top:36px;border-top:1px solid #14202b}
.hrx .ed-stories li{display:grid;grid-template-columns:72px 1fr 2fr;align-items:center;gap:26px;padding:16px 0;border-bottom:1px solid #cfc6b3}
.hrx .st-photo{width:72px;height:72px;border-radius:50%;border:1.5px dashed #b39760;display:flex;align-items:center;justify-content:center;font-size:11px;color:#9a7a42}
.hrx .st-name{font-size:18px;font-weight:700;display:flex;flex-direction:column;gap:4px}
.hrx .st-name small{font-size:13px;font-weight:400;color:#6f6553}
.hrx .st-path{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
.hrx .st-from{font-size:16px;color:#6f6553}
.hrx .st-ar{color:#9a7a42}
.hrx .st-to{font-size:clamp(22px,2vw,28px)}
/* results */
.hrx .ed-big{display:flex;align-items:flex-end;gap:clamp(20px,3vw,44px);flex-wrap:wrap;margin-top:6px}
.hrx .ed-big .num{font-size:clamp(110px,15vw,230px);line-height:.85;font-weight:500!important;color:#14202b;direction:ltr}
.hrx .ed-big .what{font-size:clamp(22px,2.2vw,32px);line-height:1.25;padding-bottom:14px;font-weight:600}
.hrx .ed-stats{display:grid;grid-template-columns:repeat(3,1fr);margin-top:44px;border-top:1px solid #14202b}
.hrx .ed-stats div{padding:18px 0 0;display:flex;flex-direction:column;gap:6px}
.hrx .ed-stats div+div{border-right:1px solid #cfc6b3;padding-right:24px}
.hrx .ed-stats b{font-size:clamp(30px,3vw,44px);font-weight:500!important;direction:ltr;text-align:right}
.hrx .ed-stats div>span{font-size:14.5px;color:#4b5560}
/* summary */
.hrx .ed-two{display:grid;grid-template-columns:1fr 1fr;gap:clamp(30px,5vw,80px);margin-top:44px;border-top:1px solid #14202b;padding-top:26px}
.hrx .ed-two h3{font-size:clamp(22px,1.9vw,28px);font-weight:500!important;margin-bottom:16px}
.hrx .ed-two ol{list-style:none;counter-reset:n;display:flex;flex-direction:column;gap:14px}
.hrx .ed-two li{counter-increment:n;font-size:17px;line-height:1.55;display:grid;grid-template-columns:28px 1fr}
.hrx .ed-two li::before{content:counter(n);color:#9a7a42;font-weight:700;font-size:14px;padding-top:3px}
.hrx .ed-two > div + div{border-right:1px solid #cfc6b3;padding-right:clamp(30px,5vw,80px);margin-right:calc(-1 * clamp(15px,2.5vw,40px))}
/* placeholders still to fill */
.ph{border-bottom:1.5px dashed #b39760;color:#9a7a42}
.hrx-dark .ph{color:#d4b47a}
#hr-creatives h2,#hr-ambassadors h2{font-weight:500!important}
@media(max-width:768px){
  .hrx{padding:84px 22px 76px}
  .hrx .ed-split,.hrx .ed-cols,.hrx .ed-two,.hrx .ed-facts,.hrx .ed-stats{grid-template-columns:1fr}
  .hrx .ed-facts div+div,.hrx .ed-stats div+div,.hrx .ed-two > div + div{border-right:0;padding-right:0;margin-right:0;border-top:1px solid #cfc6b3}
  .hrx .ed-media .ed-photo img{height:44vh}
  .hrx .ed-head-row{flex-direction:column;align-items:flex-start;gap:12px}
  .hrx .ed-stories li{grid-template-columns:52px 1fr;gap:14px}
  .hrx .st-photo{width:52px;height:52px}
  .hrx .st-path{grid-column:1/-1}
}
</style>'''

# swap slides by id, keeping each slide's existing page number
for sid, new in SLIDES.items():
    m = re.search(r'<section\b[^>]*id="' + sid + r'".*?</section>', s, re.S)
    if not m:
        sys.exit("missing slide " + sid)
    num = re.search(r'<span class="slide-page-number".*?</span>', m.group(0)).group(0)
    s = s[:m.start()] + new[:-len("</section>")] + num + "</section>" + s[m.end():]

# replace previous HR CSS block
s, n = re.subn(r'<style>\s*/\* ===== HR year summary slides ===== \*/.*?</style>', CSS, s, flags=re.S)
if n == 0:
    s, n = re.subn(r'<style id="hr-editorial">.*?</style>', CSS, s, flags=re.S)
assert n == 1, n
font = '<link href="https://fonts.googleapis.com/css2?family=Frank+Ruhl+Libre:wght@400;500;700&display=swap" rel="stylesheet">'
if "Frank+Ruhl+Libre" not in s:
    s = s.replace("</head>", font + "\n</head>", 1)

open(path, "w", encoding="utf-8").write(s)
print("ok")
