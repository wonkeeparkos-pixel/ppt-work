# -*- coding: utf-8 -*-
"""Clinical Ledger 웹 슬라이드 덱 생성기 (Pretendard 임베드). NLC/RLS/LSB 3개 덱."""
import html as _h

def esc(s): return _h.escape(str(s), quote=True)

CSS = r"""
@font-face{font-family:Pretendard;font-weight:900;src:url(__F900__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:800;src:url(__F800__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:700;src:url(__F700__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:300;src:url(__F300__) format("woff2");font-display:swap}
:root{--paper:#F7F8F6;--ink:#17232C;--muted:#6B7680;--teal:#0E7C7B;--tealD:#0B5F5E;
  --line:#E4E9E8;--bg:#DDE2DE;--green:#2E7D32;--amber:#9A6800;--red:#A8352A;--card:#FFFFFF}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:Pretendard,system-ui,sans-serif;font-weight:300;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.deck{height:100vh;overflow-y:scroll;scroll-snap-type:y mandatory;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){.deck{scroll-behavior:auto}}
.snap{height:100vh;scroll-snap-align:center;display:flex;align-items:center;justify-content:center;padding:2.2vh 2vw}
.stage{width:min(94vw,1200px);aspect-ratio:16/9;container-type:inline-size;position:relative;
  background:var(--paper);border-radius:12px;overflow:hidden;box-shadow:0 10px 40px rgba(20,28,24,.18)}
.pad{position:absolute;inset:0;padding:5.3cqw 6.4cqw;display:flex;flex-direction:column;overflow:hidden}
.eb{font-weight:700;font-size:2.15cqw;letter-spacing:.15em;text-transform:uppercase;color:var(--teal)}
.tag{font-weight:700;font-size:1.95cqw;letter-spacing:.02em;color:#fff;padding:.7cqw 1.6cqw;border-radius:999px;background:var(--teal)}
.tag.green{background:var(--green)}.tag.amber{background:var(--amber)}.tag.red{background:var(--red)}.tag.ink{background:var(--ink)}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:2cqw}
h1.t{margin:0;font-weight:900;font-size:8.6cqw;line-height:1.02;letter-spacing:-.03em;color:var(--ink);text-wrap:balance}
h2.ct{margin:1cqw 0 0;font-weight:800;font-size:3.95cqw;line-height:1.12;letter-spacing:-.02em;color:var(--ink);text-wrap:balance}
.rule{height:1.5px;background:var(--line);margin:3.2cqw 0 2.8cqw;width:40cqw}
.hr{height:1.5px;background:var(--line);margin:1.5cqw 0 2.1cqw}
.sub{font-weight:300;font-size:3.1cqw;color:#3A4750}
.order{font-weight:700;font-size:2.3cqw;color:var(--teal);margin-top:1.4cqw;letter-spacing:.01em}
ul.b{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.5cqw}
ul.b li{font-weight:300;font-size:2.46cqw;line-height:1.26;color:#33403B;padding-left:3.2cqw;position:relative}
ul.b li::before{content:"";position:absolute;left:0;top:.95cqw;width:1.25cqw;height:1.25cqw;border-radius:50%;background:var(--teal)}
ul.b li.sub2{padding-left:6cqw;font-size:2.28cqw;color:#55615B}
ul.b li.sub2::before{left:3cqw;width:1.5cqw;height:.25cqw;border-radius:0;top:1.7cqw;background:var(--muted)}
ul.b li.none{padding-left:0}
ul.b li.none::before{display:none}
ul.b li b{font-weight:800;color:var(--ink)}
li.accent,li.accent b{color:var(--tealD)!important}
li.green,li.green b{color:var(--green)!important}
li.red,li.red b{color:var(--red)!important}
li.muted{color:var(--muted)!important}
.row{display:flex;gap:4cqw;flex:1;min-height:0}
.col{flex:1;min-width:0}
.aside{width:33cqw;flex:none;background:#F0F4F3;border:1.5px solid #DDE6E4;border-radius:2.4cqw;padding:2.6cqw 2.9cqw;display:flex;flex-direction:column}
.aside.dark{background:var(--ink);border-color:var(--ink)}
.aside .at{font-weight:800;font-size:2.3cqw;color:var(--tealD);margin-bottom:1.5cqw}
.aside.dark .at{color:#7FD8CF}
.aside ul.b li{font-size:2.18cqw;color:#33403B;line-height:1.24}
.aside.dark ul.b li{color:#D6E0DE}
.aside.dark ul.b li b{color:#EAF3F1}
.stat{display:flex;gap:2.8cqw;border-top:1.5px solid var(--line);padding-top:2.1cqw;margin-top:auto}
.stat .it{display:flex;flex-direction:column;gap:.5cqw}
.stat .it b{font-weight:900;font-size:4.2cqw;letter-spacing:-.03em;color:var(--teal);line-height:1;font-variant-numeric:tabular-nums}
.stat .it span{font-weight:700;font-size:1.78cqw;color:var(--muted)}
.astat{display:flex;flex-direction:column;gap:1.7cqw;margin-top:.6cqw}
.astat .it b{font-weight:900;font-size:3.35cqw;color:var(--tealD);letter-spacing:-.02em;line-height:1;font-variant-numeric:tabular-nums}
.aside.dark .astat .it b{color:#7FE3D9}
.astat .it span{font-weight:700;font-size:1.8cqw;color:var(--muted)}
.aside.dark .astat .it span{color:#9FB0AD}
table.t{width:100%;border-collapse:collapse;margin-top:1cqw;font-variant-numeric:tabular-nums}
table.t th{background:var(--ink);color:#fff;font-weight:800;font-size:2.05cqw;text-align:left;padding:1.4cqw 1.7cqw;letter-spacing:-.01em}
table.t th:not(:first-child){text-align:center}
table.t td{font-weight:300;font-size:1.98cqw;color:#33403B;padding:1.25cqw 1.7cqw;border-bottom:1.5px solid var(--line);text-align:center;line-height:1.26}
table.t td:first-child{text-align:left;font-weight:700;color:var(--ink)}
table.t tr:nth-child(even) td{background:#EFF3F2}
table.t td b{font-weight:800;color:var(--tealD)}
table.t tr.hl td{background:#FBEAE6;border-top:2px solid var(--red);border-bottom:2px solid var(--red)}
table.t tr.hl td:first-child{border-left:2px solid var(--red)}
table.t tr.hl td:last-child{border-right:2px solid var(--red)}
table.t tr.hl td:first-child{color:var(--red)}
.note{font-weight:700;font-size:1.92cqw;color:var(--tealD);margin-top:1.8cqw;line-height:1.28}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:#7A868C;
  border-top:1.5px solid var(--line);padding-top:2.2cqw}
.content .foot,.split .foot,.tableS .foot{margin-top:1.6cqw}
.foot .src{font-weight:300;font-size:1.95cqw}
.foot .pg{font-weight:800;font-size:2.2cqw;font-variant-numeric:tabular-nums}
.title .tick{position:absolute;left:0;top:0;width:2cqw;height:100%;background:var(--teal)}
.title .pad{padding-left:8.6cqw}
.title .foot{color:#7A868C}
/* key slide */
.key .stage{background:var(--ink)}
.key .pad{padding:6.4cqw 7cqw}
.key .keb{font-weight:700;font-size:2.1cqw;letter-spacing:.14em;text-transform:uppercase;color:#5FD6CC}
.key h2.kh{margin:1.6cqw 0 2.6cqw;font-weight:900;font-size:4.9cqw;line-height:1.1;letter-spacing:-.02em;color:#F4F7F5;text-wrap:balance}
.key .msg{display:flex;gap:3cqw;align-items:flex-start;padding:1.35cqw 0;border-top:1px solid #2A3942}
.key .msg .ml{flex:none;width:22cqw;font-weight:800;font-size:2.5cqw;color:#5FD6CC}
.key .msg .md{font-weight:300;font-size:2.22cqw;line-height:1.3;color:#D3DBD8}
/* refs */
.refs .stage{background:var(--paper)}
.refs .cols{display:flex;gap:4cqw;flex:1;min-height:0}
.refs .cols .c{flex:1;display:flex;flex-direction:column;gap:1.02cqw}
.refs .cols a,.refs .cols div.r{font-weight:300;font-size:1.55cqw;line-height:1.22;color:#33403B;text-decoration:none}
.refs .cols a b{color:var(--tealD);font-weight:700}
/* figure slides */
.figure .figbox{flex:1;display:flex;align-items:stretch;justify-content:center;gap:2.6cqw;min-height:0;margin:1.8cqw 0 1cqw}
.figpanel{flex:1;background:#FBFCFB;border:1.5px solid var(--line);border-radius:2.2cqw;padding:1.8cqw 1.6cqw 1.4cqw;display:flex;flex-direction:column;align-items:center;gap:.8cqw;min-width:0}
.figpanel .pt{font-weight:800;font-size:2.05cqw;letter-spacing:-.01em}
.figpanel.warn{background:#FCF4F2;border-color:#E7CFC9}.figpanel.warn .pt{color:var(--red)}
.figpanel.good{background:#EFF6F0;border-color:#CFE3D2}.figpanel.good .pt{color:var(--green)}
.figpanel svg{width:auto;height:auto;max-width:100%;max-height:30cqw;flex:1}
.figpanel .pl{font-weight:700;font-size:1.72cqw;color:#55615B;text-align:center;line-height:1.28}
.figpanel .pl b{color:var(--ink);font-weight:800}
.figcap{font-weight:700;font-size:1.95cqw;color:var(--tealD);text-align:center;line-height:1.32}
.figcap b{color:var(--ink);font-weight:800}
.figure .foot{margin-top:.9cqw}
/* big image-focused figure */
.bigfig h2.ct{margin:.4cqw 0 0;font-size:3.4cqw}
.bigfig .bigimg{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin:1.3cqw 0 .5cqw}
.bigfig .bigimg img{max-height:100%;max-width:100%;object-fit:contain;border-radius:1.4cqw;border:1.5px solid var(--line)}
.bigfig .foot{margin-top:.4cqw}
/* 텍스트 + 그림 2단 */
.figsplit .figcol{width:41cqw;flex:none;display:flex;align-items:center;justify-content:center;min-height:0;
  background:#FBFCFB;border:1.5px solid var(--line);border-radius:2.2cqw;padding:1.2cqw}
.figsplit .figcol svg{max-width:100%;max-height:100%;width:100%;height:100%}
.figsplit ul.b{gap:1.15cqw}
.figsplit ul.b li{font-size:2.08cqw}
.bigfig .bigimg{margin:.7cqw 0 .3cqw}
.bigfig .bigimg svg{max-width:100%;max-height:100%;width:100%;height:100%}
svg text{font-family:Pretendard,sans-serif}
@keyframes cramp{0%,100%{transform:scale(1)}50%{transform:scale(.93)}}
@keyframes spark{0%,100%{opacity:.35;transform:scale(.9)}50%{opacity:1;transform:scale(1.15)}}
@keyframes sway{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes brk{0%,100%{opacity:.4}50%{opacity:.14}}
@keyframes flow{to{stroke-dashoffset:-22}}
.a-cramp{transform-box:fill-box;transform-origin:center;animation:cramp 1.5s ease-in-out infinite}
.a-spark{transform-box:fill-box;transform-origin:center;animation:spark 1.5s ease-in-out infinite}
.a-sway{transform-box:fill-box;transform-origin:center;animation:sway 2.8s ease-in-out infinite}
.a-brk{animation:brk 1.5s ease-in-out infinite}
.a-flow{stroke-dasharray:6 6;animation:flow 1s linear infinite}
@media (prefers-reduced-motion:reduce){.a-cramp,.a-spark,.a-sway,.a-brk,.a-flow{animation:none}}
/* UI chrome */
.bar{position:fixed;top:0;left:0;height:4px;background:var(--teal);width:0;z-index:10;transition:width .2s}
.count{position:fixed;right:16px;bottom:14px;z-index:10;background:rgba(23,35,44,.86);color:#EAF1EF;
  font-family:Pretendard;font-weight:700;font-size:13px;padding:6px 12px;border-radius:999px;font-variant-numeric:tabular-nums;letter-spacing:.02em}
.hint{position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:10;color:#5C665F;font-family:Pretendard;
  font-weight:700;font-size:12.5px;letter-spacing:.03em;background:rgba(247,248,246,.9);padding:6px 14px;border-radius:999px;border:1.4px solid var(--line)}
.deckttl{position:fixed;left:16px;bottom:14px;z-index:10;color:#5C665F;font-family:Pretendard;font-weight:700;font-size:12.5px;letter-spacing:.02em}
@media print{
  @page{size:landscape;margin:0}
  body{background:#fff}
  .deck{height:auto;overflow:visible;display:block}
  .snap{height:auto;page-break-after:always;padding:0}
  .stage{width:100%;box-shadow:none;border-radius:0}
  .bar,.count,.hint,.deckttl{display:none}
}
"""

JS = r"""
const deck=document.querySelector('.deck');
const snaps=[...document.querySelectorAll('.snap')];
const bar=document.querySelector('.bar');
const count=document.querySelector('.count');
const total=snaps.length;
function cur(){let i=Math.round(deck.scrollTop/window.innerHeight);return Math.max(0,Math.min(total-1,i));}
function upd(){const i=cur();count.textContent=(i+1)+' / '+total;bar.style.width=((i+1)/total*100)+'%';}
function go(i){i=Math.max(0,Math.min(total-1,i));snaps[i].scrollIntoView();setTimeout(upd,60);}
deck.addEventListener('scroll',()=>{window.requestAnimationFrame(upd);},{passive:true});
addEventListener('keydown',e=>{
  if(['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(cur()+1);}
  else if(['ArrowUp','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(cur()-1);}
  else if(e.key==='Home'){e.preventDefault();go(0);}
  else if(e.key==='End'){e.preventDefault();go(total-1);}
});
const hint=document.querySelector('.hint');
if(hint){setTimeout(()=>{hint.style.transition='opacity .6s';hint.style.opacity='0';},4200);}
upd();
"""

# ---------- slide renderers ----------
def _items(items):
    out=[]
    for it in items:
        lvl=it[0]; txt=it[1]; cls=it[2] if len(it)>2 and it[2] else ""
        c="none" if lvl<0 else ("sub2" if lvl>=1 else "")
        out.append(f'<li class="{c} {cls}">{txt}</li>')
    return '<ul class="b">'+''.join(out)+'</ul>'

def _stat(stat):
    its=''.join(f'<div class="it"><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b,s in stat)
    return f'<div class="stat">{its}</div>'

def _astat(stat):
    its=''.join(f'<div class="it"><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b,s in stat)
    return f'<div class="astat">{its}</div>'

def _foot(src,pg): return f'<div class="foot"><span class="src">{esc(src)}</span><span class="pg">{pg:02d}</span></div>'

def _tag(tag):
    if not tag: return ""
    t,c=tag if isinstance(tag,tuple) else (tag,"")
    return f'<span class="tag {c}">{esc(t)}</span>'

def slide(s, pg):
    T=s['t']
    if T=='title':
        return f'''<section class="snap title"><div class="stage"><div class="tick"></div><div class="pad">
<div class="eb">{esc(s['eyebrow'])}</div><h1 class="t">{s['title']}</h1><div class="rule"></div>
<div class="sub">{esc(s['sub'])}</div><div class="order">{esc(s['order'])}</div>
{_foot(s['series'],pg)}</div></div></section>'''
    if T=='bullets':
        stat=_stat(s['stat']) if s.get('stat') else ''
        note=f'<div class="note">{s["note"]}</div>' if s.get('note') else ''
        return f'''<section class="snap content"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>{_items(s['items'])}{note}{stat}
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='split':
        a=s['aside']
        inner=_astat(a['stat']) if a.get('stat') else _items(a['items'])
        dark=' dark' if a.get('dark') else ''
        return f'''<section class="snap split"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>
<div class="row"><div class="col">{_items(s['items'])}</div>
<div class="aside{dark}"><div class="at">{esc(a['title'])}</div>{inner}</div></div>
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='figsplit':
        return f'''<section class="snap split figsplit"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>
<div class="row"><div class="col">{_items(s['items'])}</div>
<div class="figcol">{s['svg']}</div></div>
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='table':
        head='<tr>'+''.join(f'<th>{esc(h)}</th>' for h in s['headers'])+'</tr>'
        hl=set(s.get('hlrows',[]))
        body=''
        for ri,r in enumerate(s['rows']):
            cls=' class="hl"' if ri in hl else ''
            body+=f'<tr{cls}>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>'
        note=f'<div class="note">{s["note"]}</div>' if s.get('note') else ''
        return f'''<section class="snap tableS"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><table class="t">{head}{body}</table>{note}
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='figure':
        cap=f'<div class="figcap">{s["caption"]}</div>' if s.get('caption') else ''
        return f'''<section class="snap figure"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2>
<div class="figbox">{s['svg']}</div>{cap}
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='bigfig':
        return f'''<section class="snap bigfig"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2>
<div class="bigimg">{s['svg']}</div>
{_foot(s['foot'],pg)}</div></div></section>'''
    if T=='key':
        msgs=''.join(f'<div class="msg"><div class="ml">{esc(l)}</div><div class="md">{d}</div></div>' for l,d in s['msgs'])
        return f'''<section class="snap key"><div class="stage"><div class="pad">
<div class="keb">{esc(s['eyebrow'])}</div><h2 class="kh">{s['headline']}</h2>{msgs}</div></div></section>'''
    if T=='refs':
        n=len(s['refs']); half=(n+1)//2
        def col(rs): return '<div class="c">'+''.join(rs)+'</div>'
        left=[f'<a href="{u}" target="_blank" rel="noopener">{txt}</a>' if u else f'<div class="r">{txt}</div>' for txt,u in s['refs'][:half]]
        right=[f'<a href="{u}" target="_blank" rel="noopener">{txt}</a>' if u else f'<div class="r">{txt}</div>' for txt,u in s['refs'][half:]]
        return f'''<section class="snap refs"><div class="stage"><div class="pad">
<div class="topbar"><div class="eb">참고문헌 · References</div><span class="tag ink">PubMed</span></div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div><div class="cols">{col(left)}{col(right)}</div>
{_foot("제목 클릭 시 PubMed로 이동",pg)}</div></div></section>'''
    return ''

def render_deck(title, slides):
    body=''.join(slide(s,i+1) for i,s in enumerate(slides))
    return f'''<title>{esc(title)}</title>
<style>{CSS}</style>
<div class="bar"></div><div class="count"></div><div class="deckttl">{esc(title)}</div>
<div class="hint">← → · 스크롤 · 방향키로 이동</div>
<div class="deck">{body}</div>
<script>{JS}</script>'''
