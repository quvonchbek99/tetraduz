"""TOG lug'ati PDF: tog.json + tog.html grammatika bo'limi -> A4 PDF (Chromium orqali)."""
import json, re, sys, html, os
from playwright.sync_api import sync_playwright

B = os.path.dirname(os.path.abspath(__file__))
cats = json.load(open(B + '/tog.json', encoding='utf-8'))
page_src = open(sys.argv[1], encoding='utf-8').read()
out_pdf = sys.argv[2]
e = html.escape

gram = re.search(r'<section id="tab-gram"[^>]*>(.*?)</section>', page_src, re.S).group(1)
gram = re.sub(r'<p class="lead".*?</p>', '', gram, count=1, flags=re.S)
gram = gram.replace('href="padejlar.html"', 'href="https://quvonchbek99.github.io/tetraduz/padejlar.html"')
method = re.search(r'<section id="tab-method"[^>]*>(.*?)</section>', page_src, re.S).group(1)

total = sum(len(c['w']) for c in cats)
st = sorted({w['b'] for c in cats for w in c['w']})
stage_txt = (f"{st[0]}–{st[-1]}-bosqich" if len(st) > 1 else f"{st[0]}-bosqich") + ' · ' + ', '.join(f"{b}-bosqich: {sum(1 for c in cats for w in c['w'] if w['b']==b)} so'z" for b in st)

def word(w, n):
    return f'''<div class="w">
  <div class="top"><span class="em">{e(w['em'])}</span><div class="t"><div class="ru">{e(w['ru'])}</div><div class="uz">{e(w['uz'])}</div></div><span class="n">{n}{' · ' + str(w['b']) + '-b' if w['b'] > 1 else ''}</span></div>
  <div class="g">{e(w['g'])}</div>
  <div class="h"><b>{e(w['h'])}</b> — {e(w['s'])}</div>
  <div class="ex"><span class="er">{e(w['er'])}</span> — <span class="eu">{e(w['eu'])}</span></div>
</div>'''

toc = ''.join(f'<tr><td>{i+1}. {e(c["uz"])}</td><td class="r">{e(c["ru"])}</td><td class="c">{len(c["w"])}</td></tr>' for i, c in enumerate(cats))
sections = ''
for i, c in enumerate(cats):
    sections += f'<section class="cat"><h2><span class="num">{i+1}</span>{e(c["uz"])} <small>{e(c["ru"])} · {len(c["w"])} so\'z</small></h2><div class="grid">'
    sections += ''.join(word(w, j + 1) for j, w in enumerate(c['w']))
    sections += '</div></section>'

doc = f'''<!doctype html><html lang="uz"><head><meta charset="utf-8"><title>TOG lug'ati — ТЕТРАДЬ</title>
<style>
@page {{ size:A4; margin:16mm 13mm 16mm 13mm; }}
:root{{ --ink:#242F2A; --soft:#5B6960; --acc:#2F6F52; --accs:#DDEBE2; --gold:#9A7020; --goldbg:#F6EEDC; --rule:#5878A8; --rulebg:#E8EEF7; --margin:#B94A3D; --line:#E4E1D3; }}
*{{box-sizing:border-box}}
body{{font-family:Inter, 'DejaVu Sans', sans-serif; color:var(--ink); font-size:9.6pt; line-height:1.42; margin:0; -webkit-print-color-adjust:exact; print-color-adjust:exact;}}
h1,h2,h3{{font-family:'DejaVu Serif', serif; margin:0}}
.ru,.er,td.ru,span.ru{{font-family:'DejaVu Serif', serif}}
.cover{{height:262mm; display:flex; flex-direction:column; justify-content:center; padding:0 10mm; border-left:3px solid var(--margin); page-break-after:always; background:repeating-linear-gradient(#fff 0 7.4mm, #E3EAF5 7.4mm 7.6mm)}}
.cover .brand{{font-family:'DejaVu Serif'; letter-spacing:.08em; font-size:15pt; color:var(--acc); font-weight:700}}
.cover h1{{font-size:34pt; line-height:1.1; margin:6mm 0 4mm}}
.cover .sub{{font-size:13pt; color:var(--soft); max-width:150mm}}
.cover .tog{{display:flex; gap:4mm; margin:10mm 0}}
.cover .tog div{{background:#fff; border:1px solid var(--line); border-radius:3mm; padding:3mm 4mm; flex:1}}
.cover .tog b{{display:block; font-family:'DejaVu Serif'; font-size:20pt; color:var(--acc)}}
table.toc{{border-collapse:collapse; width:120mm; background:#fff}}
table.toc td{{padding:1.6mm 2mm; border-bottom:1px solid var(--line)}}
table.toc td.r{{color:var(--soft); font-family:'DejaVu Serif'}} table.toc td.c{{text-align:right; font-weight:700}}
.cover .foot{{margin-top:10mm; color:var(--soft); font-size:10pt}}
.pagebox{{page-break-after:always}}
.pagebox h2.big{{font-size:18pt; margin-bottom:4mm; color:var(--acc)}}
.rule-box{{border:1px solid var(--line); border-radius:3mm; padding:3.5mm 4.5mm; margin-bottom:4mm; break-inside:avoid}}
.rule-box h3{{font-size:12.5pt; margin-bottom:2mm}}
table.t{{border-collapse:collapse; width:100%; font-size:9pt; margin-top:1.5mm}}
table.t th,table.t td{{border:1px solid var(--line); padding:1.2mm 2mm; text-align:left; vertical-align:top}}
table.t th{{background:var(--accs)}}
.note{{margin-top:2mm; padding:2mm 3mm; border:1px dashed var(--gold); background:var(--goldbg); border-radius:2mm}}
ul,ol{{margin:1.5mm 0 0; padding-left:5mm}} li{{margin:.6mm 0}}
.tog-steps{{display:grid; grid-template-columns:1fr 1fr; gap:3mm; margin-top:3mm}}
.tog-step{{border:1px solid var(--line); border-radius:2.5mm; padding:2.5mm 3mm}}
.tog-step b.l{{display:inline-block; width:6mm; height:6mm; line-height:6mm; text-align:center; border-radius:50%; background:var(--acc); color:#fff; margin-right:2mm}}
.tog-step p{{margin:1mm 0 0; color:var(--soft)}}
.tbl-wrap{{}}
section.cat{{page-break-before:always}}
section.cat h2{{font-size:17pt; margin-bottom:4mm; padding-bottom:2mm; border-bottom:2px solid var(--acc)}}
section.cat h2 .num{{display:inline-block; width:9mm; height:9mm; line-height:9mm; text-align:center; background:var(--acc); color:#fff; border-radius:2mm; margin-right:3mm; font-size:13pt}}
section.cat h2 small{{font-size:10pt; color:var(--soft); font-weight:400; margin-left:2mm}}
.grid{{display:grid; grid-template-columns:1fr 1fr; gap:2.6mm}}
.w{{border:1px solid var(--line); border-left:2.5px solid var(--acc); border-radius:2mm; padding:2.2mm 2.8mm; break-inside:avoid; display:flex; flex-direction:column; gap:1.2mm}}
.w .top{{display:flex; align-items:center; gap:2.5mm}}
.w .em{{font-size:17pt; width:9mm; text-align:center; font-family:'Noto Color Emoji'}}
.w .t{{flex:1}}
.w .ru{{font-size:12.5pt; font-weight:700}}
.w .uz{{color:var(--acc); font-weight:600}}
.w .n{{color:var(--soft); font-size:8pt; align-self:flex-start}}
.w .g{{font-family:'DejaVu Serif'; font-size:8.2pt; background:var(--rulebg); border-radius:1.5mm; padding:1mm 1.8mm}}
.w .h{{font-size:8.8pt; background:var(--goldbg); border-radius:1.5mm; padding:1.1mm 1.8mm}}
.w .h b{{color:var(--gold)}}
.w .ex{{font-size:8.8pt}} .w .eu{{color:var(--soft)}}
a{{color:var(--acc)}}
</style></head><body>
<div class="cover">
  <div class="brand">ТЕТРАДЬ · Rus tili onlayn</div>
  <h1>TOG lug'ati:<br>eng kerakli ruscha so'zlar</h1>
  <p class="sub">{total} ta so'z — eng ko'p ishlatilishi bo'yicha kamayish tartibida. Har biri tarjima, rasm, grammatik shakllar, o'zbekcha ohangdosh so'z, kulgili manzara va misol gap bilan.</p>
  <div class="tog"><div><b>T</b>Tarjima</div><div><b>O</b>Obraz — rasm</div><div><b>G</b>Garmoniya — ohangdosh so'z</div><div><b>K</b>Kulgi — absurd manzara</div></div>
  <table class="toc">{toc}<tr><td><b>Jami</b></td><td></td><td class="c">{total}</td></tr></table>
  <p class="foot">{stage_txt} · Onlayn versiya (ovoz, kartochka, test): quvonchbek99.github.io/tetraduz/tog.html</p>
</div>
<div class="pagebox"><h2 class="big">TOG usuli</h2>{method}</div>
<div class="pagebox gram"><h2 class="big">Grammatika kalitlari</h2>{gram}</div>
{sections}
</body></html>'''

open(B + '/tog-print.html', 'w', encoding='utf-8').write(doc)
with sync_playwright() as p:
    br = p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg = br.new_page()
    pg.goto('file://' + B + '/tog-print.html'); pg.wait_for_timeout(500)
    pg.pdf(path=out_pdf, format='A4', print_background=True, display_header_footer=True,
           header_template='<span></span>',
           footer_template='<div style="font-size:8px;width:100%;text-align:center;color:#5B6960;font-family:Inter">TOG lug\'ati · ТЕТРАДЬ · <span class="pageNumber"></span> / <span class="totalPages"></span></div>',
           margin={'top':'14mm','bottom':'16mm','left':'13mm','right':'13mm'})
    br.close()
print('ok', out_pdf)
