# -*- coding: utf-8 -*-
"""보툴리눔 덱 전용 렌더러 — 테마 "차단 / Blockade".

deck_html.py(Clinical Ledger)와 슬라이드 스키마는 같지만 시각 정체성이 다르다.
NLC/RLS/LSB 덱은 deck_html.py를 계속 쓴다 — 이 파일은 건드리지 않는다.

정체성
  · 색   신경계 인디고를 구조색으로, 100 U 바이알 유리를 닮은 차가운 바탕.
         근거등급이 색이다 — 모스(A·B) / 인디고(기본) / 앰버(C) / 슬레이트(U) / 벽돌(경고)
  · 서체 본문 Pretendard, 용량·단위·라벨은 JetBrains Mono로 분리
  · 장치 슬라이드 최상단 2px 라인 = 그 쪽의 근거등급 색
         표지·요약의 100칸 단위 게이지 = 한 바이알 100 U
"""
import html as _h


def esc(s):
    return _h.escape(str(s), quote=True)


CSS = r"""
@font-face{font-family:Pretendard;font-weight:900;src:url(__F900__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:800;src:url(__F800__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:700;src:url(__F700__) format("woff2");font-display:swap}
@font-face{font-family:Pretendard;font-weight:300;src:url(__F300__) format("woff2");font-display:swap}
@font-face{font-family:JBMono;font-weight:400;src:url(__M400__) format("woff2");font-display:swap}
@font-face{font-family:JBMono;font-weight:700;src:url(__M700__) format("woff2");font-display:swap}
:root{
  --paper:#F4F3F8;      /* 바이알 유리 */
  --card:#FFFFFF;
  --band:#EBE9F4;       /* aside 패널 */
  --bandLine:#DAD6EA;
  --ink:#181A2E;        /* 인디고블랙 */
  --ink2:#33355A;       /* 본문 */
  --muted:#6E6E88;
  --line:#E0DEEC;
  --indigo:#463A96;     /* 구조색 */
  --indigoD:#332876;
  --indigoL:#8B7BE8;    /* 짙은 바탕 위 */
  --brick:#A8352A;      /* 독소·차단·경고 */
  --moss:#2E6B3E;       /* 검증된 근거 */
  --amber:#B0701A;      /* 근거 상충 */
  --slate:#6B7280;      /* 근거 없음 */
  --bg:#23244A;         /* 페이지 바닥 */
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:Pretendard,system-ui,sans-serif;font-weight:300;
  -webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
.deck{height:100vh;overflow-y:scroll;scroll-snap-type:y mandatory;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){.deck{scroll-behavior:auto}}
.snap{height:100vh;scroll-snap-align:center;display:flex;align-items:center;justify-content:center;padding:2.2vh 2vw}
.stage{width:min(94vw,1200px);aspect-ratio:16/9;container-type:inline-size;position:relative;
  background:var(--paper);border-radius:6px;overflow:hidden;box-shadow:0 14px 44px rgba(10,10,30,.42)}
/* 최상단 2px = 근거등급 색 */
.grade{position:absolute;left:0;top:0;height:.34cqw;width:100%;background:var(--indigo);z-index:3}
.grade.g-green{background:var(--moss)}
.grade.g-amber{background:var(--amber)}
.grade.g-red{background:var(--brick)}
.grade.g-ink{background:var(--ink)}
.grade.g-slate{background:var(--slate)}
.pad{position:absolute;inset:0;padding:5.3cqw 6.4cqw;display:flex;flex-direction:column;overflow:hidden}
/* 라벨·단위는 모노 */
.eb{font-family:JBMono,monospace;font-weight:700;font-size:1.76cqw;letter-spacing:.1em;
  text-transform:uppercase;color:var(--indigo)}
.mono{font-family:JBMono,monospace;font-variant-numeric:tabular-nums}
.tag{font-family:JBMono,monospace;font-weight:700;font-size:1.68cqw;letter-spacing:.06em;color:#fff;
  padding:.62cqw 1.5cqw;border-radius:.5cqw;background:var(--indigo);text-transform:uppercase}
.tag.green{background:var(--moss)}.tag.amber{background:var(--amber)}
.tag.red{background:var(--brick)}.tag.ink{background:var(--ink)}.tag.slate{background:var(--slate)}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:2cqw}
h1.t{margin:0;font-weight:900;font-size:8.2cqw;line-height:1.0;letter-spacing:-.035em;color:var(--ink);text-wrap:balance}
h2.ct{margin:1cqw 0 0;font-weight:800;font-size:3.5cqw;line-height:1.12;letter-spacing:-.022em;color:var(--ink);text-wrap:balance}
.rule{height:1.5px;background:var(--line);margin:2.8cqw 0 2.4cqw;width:40cqw}
.hr{height:1.5px;background:var(--line);margin:1.5cqw 0 2.0cqw}
.sub{font-weight:300;font-size:2.9cqw;color:var(--ink2)}
.order{font-family:JBMono,monospace;font-weight:700;font-size:1.86cqw;color:var(--indigo);
  margin-top:1.4cqw;letter-spacing:.04em}
ul.b{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.0cqw}
ul.b li{font-weight:300;font-size:2.0cqw;line-height:1.2;color:var(--ink2);padding-left:2.9cqw;position:relative}
ul.b li::before{content:"";position:absolute;left:0;top:.66cqw;width:1.0cqw;height:1.0cqw;background:var(--indigo)}
ul.b li.sub2{padding-left:5.4cqw;font-size:1.88cqw;color:#565782}
ul.b li.sub2::before{left:2.8cqw;width:1.24cqw;height:.2cqw;top:1.34cqw;background:var(--muted)}
ul.b li.none{padding-left:0}
ul.b li.none::before{display:none}
ul.b li b{font-weight:800;color:var(--ink)}
li.accent,li.accent b{color:var(--indigoD)!important}
li.green,li.green b{color:var(--moss)!important}
li.red,li.red b{color:var(--brick)!important}
li.muted{color:var(--muted)!important}
.row{display:flex;gap:3.6cqw;flex:1;min-height:0}
.col{flex:1;min-width:0}
.aside{width:33cqw;flex:none;background:var(--band);border:1.5px solid var(--bandLine);
  border-radius:.8cqw;padding:2.1cqw 2.3cqw;display:flex;flex-direction:column}
.aside.dark{background:var(--ink);border-color:var(--ink)}
.aside .at{font-family:JBMono,monospace;font-weight:700;font-size:1.72cqw;letter-spacing:.04em;
  text-transform:uppercase;color:var(--indigoD);margin-bottom:1.2cqw}
.aside.dark .at{color:var(--indigoL)}
.aside ul.b li{font-size:1.84cqw;color:var(--ink2);line-height:1.2}
.aside ul.b li::before{background:var(--indigoD)}
.aside.dark ul.b li{color:#CFCEE4}
.aside.dark ul.b li b{color:#EEEDF8}
.stat{display:flex;gap:2.6cqw;border-top:1.5px solid var(--line);padding-top:1.4cqw;margin-top:auto}
.stat .it{display:flex;flex-direction:column;gap:.5cqw}
.astat .it{display:flex;flex-direction:column;gap:.28cqw}
.stat .it b{font-family:JBMono,monospace;font-weight:700;font-size:3.3cqw;letter-spacing:-.02em;
  color:var(--indigo);line-height:1;font-variant-numeric:tabular-nums}
.stat .it span{font-weight:700;font-size:1.62cqw;color:var(--muted)}
.astat{display:flex;flex-direction:column;gap:.9cqw;margin-top:.5cqw}
.astat .it b{font-family:JBMono,monospace;font-weight:700;font-size:2.45cqw;color:var(--indigoD);
  letter-spacing:-.02em;line-height:1;font-variant-numeric:tabular-nums}
.aside.dark .astat .it b{color:var(--indigoL)}
.astat .it span{font-weight:700;font-size:1.5cqw;color:var(--muted);line-height:1.2}
.aside.dark .astat .it span{color:#9C9CBC}
table.t{width:100%;border-collapse:collapse;margin-top:1cqw;font-variant-numeric:tabular-nums}
table.t th{background:var(--ink);color:#fff;font-family:JBMono,monospace;font-weight:700;font-size:1.72cqw;
  letter-spacing:.03em;text-align:left;padding:1.15cqw 1.5cqw;text-transform:uppercase}
table.t th:not(:first-child){text-align:center}
table.t td{font-weight:300;font-size:1.94cqw;color:var(--ink2);padding:1.1cqw 1.5cqw;
  border-bottom:1.5px solid var(--line);text-align:center;line-height:1.24}
table.t td:first-child{text-align:left;font-weight:700;color:var(--ink)}
table.t tr:nth-child(even) td{background:#ECEAF5}
table.t td b{font-weight:800;color:var(--indigoD)}
table.t tr.hl td{background:#F8E9E6;border-top:2px solid var(--brick);border-bottom:2px solid var(--brick)}
table.t tr.hl td:first-child{border-left:2px solid var(--brick);color:var(--brick)}
table.t tr.hl td:last-child{border-right:2px solid var(--brick)}
.note{font-weight:700;font-size:1.7cqw;color:var(--indigoD);margin-top:1.2cqw;line-height:1.28}
/* dense: 행이 많은 표 */
.tableS.dense h2.ct{font-size:3.2cqw}
.tableS.dense table.t{margin-top:.5cqw}
.tableS.dense table.t th{font-size:1.5cqw;padding:.58cqw 1.05cqw}
.tableS.dense table.t td{font-size:1.54cqw;padding:.42cqw 1.05cqw;line-height:1.18}
.tableS.dense .note{font-size:1.6cqw;margin-top:1cqw;line-height:1.24}
.tableS.dense .foot{margin-top:1cqw;padding-top:1.4cqw}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:center;color:var(--muted);
  border-top:1.5px solid var(--line);padding-top:1.5cqw}
.content .foot,.split .foot,.tableS .foot{margin-top:1.1cqw}
.foot .src{font-weight:300;font-size:1.72cqw}
.foot .pg{font-family:JBMono,monospace;font-weight:700;font-size:1.9cqw;color:var(--indigo);
  font-variant-numeric:tabular-nums;letter-spacing:.06em}
/* ── 표지: 인디고 바탕 + 100칸 단위 게이지 ───────────────── */
.title .stage{background:var(--ink)}
.title .grade{background:var(--indigoL);height:.5cqw}
.title .pad{padding:5.6cqw 6.4cqw}
.title .eb{color:var(--indigoL)}
.title h1.t{color:#F6F5FB}
.title .rule{background:#3A3C63;width:26cqw}
.title .sub{color:#C6C5DE}
.title .order{color:var(--indigoL)}
.title .foot{color:#8A8AAC;border-top-color:#33355A}
.title .foot .pg{color:var(--indigoL)}
.titlerow{display:flex;gap:5cqw;align-items:flex-end;flex:1;min-height:0}
.titlerow .tl{flex:1;min-width:0;display:flex;flex-direction:column;justify-content:center}
.vial{flex:none;width:22cqw;display:flex;flex-direction:column;gap:1.0cqw;padding-bottom:1cqw}
.vial .vh{font-family:JBMono,monospace;font-weight:700;font-size:1.62cqw;letter-spacing:.14em;
  text-transform:uppercase;color:var(--indigoL)}
.gauge{display:grid;grid-template-columns:repeat(10,1fr);gap:.34cqw}
.gauge i{display:block;aspect-ratio:1;background:#3E4068;border-radius:.08cqw}
.gauge i.on{background:#4E4F80}
.vial .vc{font-weight:300;font-size:1.36cqw;line-height:1.36;color:#9C9CBC}
.vial .vc b{font-weight:800;color:#DAD8EE}
/* ── 요약(key) ────────────────────────────────────────── */
.key .stage{background:var(--ink)}
.key .grade{background:var(--indigoL)}
.key .pad{padding:5.2cqw 6.4cqw}
.key .keb{font-family:JBMono,monospace;font-weight:700;font-size:1.74cqw;letter-spacing:.13em;
  text-transform:uppercase;color:var(--indigoL)}
.key h2.kh{margin:1.1cqw 0 2.0cqw;font-weight:900;font-size:4.2cqw;line-height:1.08;
  letter-spacing:-.025em;color:#F6F5FB;text-wrap:balance}
.key .msg{display:flex;gap:2.4cqw;align-items:flex-start;padding:1.0cqw 0;border-top:1px solid #33355A}
.key .msg .ml{flex:none;width:19cqw;font-family:JBMono,monospace;font-weight:700;font-size:1.86cqw;
  letter-spacing:.05em;text-transform:uppercase;color:var(--indigoL);padding-top:.2cqw}
.key .msg .md{font-weight:300;font-size:1.92cqw;line-height:1.26;color:#CFCEE4}
.key .msg .md b{font-weight:800;color:#F1F0FA}
/* ── 참고문헌 ─────────────────────────────────────────── */
.refs .cols{display:flex;gap:3.6cqw;flex:1;min-height:0}
.refs .cols .c{flex:1;display:flex;flex-direction:column;gap:.74cqw}
.refs .cols a,.refs .cols div.r{font-weight:300;font-size:1.32cqw;line-height:1.17;
  color:var(--ink2);text-decoration:none}
.refs .cols a b,.refs .cols div.r b{color:var(--indigoD);font-weight:700}
.refs .cols a:hover{color:var(--indigo)}
.refs .cols a:focus-visible{outline:2px solid var(--indigo);outline-offset:2px}
/* ── 그림 ────────────────────────────────────────────── */
.figure .figbox{flex:1;display:flex;align-items:stretch;justify-content:center;gap:2.4cqw;
  min-height:0;margin:1.6cqw 0 1cqw}
.figpanel{flex:1;background:var(--card);border:1.5px solid var(--line);border-radius:.8cqw;
  padding:1.7cqw 1.5cqw 1.3cqw;display:flex;flex-direction:column;align-items:center;gap:.8cqw;min-width:0}
.figpanel .pt{font-weight:800;font-size:1.78cqw;letter-spacing:-.01em;color:var(--indigoD)}
.figpanel.warn{background:#FBF1EF;border-color:#EBD2CC}.figpanel.warn .pt{color:var(--brick)}
.figpanel.good{background:#EEF4EF;border-color:#CFE0D3}.figpanel.good .pt{color:var(--moss)}
.figpanel svg{width:auto;height:auto;max-width:100%;max-height:30cqw;flex:1}
.figpanel .pl{font-weight:700;font-size:1.66cqw;color:#585976;text-align:center;line-height:1.28}
.figpanel .pl b{color:var(--ink);font-weight:800}
.figcap{font-weight:700;font-size:1.82cqw;color:var(--indigoD);text-align:center;line-height:1.32}
.figcap b{color:var(--ink);font-weight:800}
.figure .foot{margin-top:.9cqw}
.bigfig h2.ct{margin:.4cqw 0 0;font-size:3.2cqw}
.bigfig .bigimg{flex:1;display:flex;align-items:center;justify-content:center;min-height:0;margin:1.2cqw 0 .5cqw}
.bigfig .foot{margin-top:.4cqw}
svg text{font-family:Pretendard,sans-serif}
svg .u{font-family:JBMono,monospace;font-weight:700}
@keyframes spark{0%,100%{opacity:.35;transform:scale(.9)}50%{opacity:1;transform:scale(1.15)}}
@keyframes sway{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes brk{0%,100%{opacity:.4}50%{opacity:.14}}
@keyframes flow{to{stroke-dashoffset:-22}}
.a-spark{transform-box:fill-box;transform-origin:center;animation:spark 1.6s ease-in-out infinite}
.a-sway{transform-box:fill-box;transform-origin:center;animation:sway 2.8s ease-in-out infinite}
.a-brk{animation:brk 1.6s ease-in-out infinite}
.a-flow{stroke-dasharray:6 6;animation:flow 1s linear infinite}
@media (prefers-reduced-motion:reduce){.a-spark,.a-sway,.a-brk,.a-flow{animation:none}}
/* ── 화면 크롬 ────────────────────────────────────────── */
.bar{position:fixed;top:0;left:0;height:3px;background:var(--indigoL);width:0;z-index:10;transition:width .2s}
.count{position:fixed;right:16px;bottom:14px;z-index:10;background:rgba(24,26,46,.92);color:#DAD8EE;
  font-family:JBMono,monospace;font-weight:700;font-size:12.5px;padding:6px 12px;border-radius:4px;
  font-variant-numeric:tabular-nums;letter-spacing:.06em;border:1px solid #3A3C63}
.hint{position:fixed;left:50%;transform:translateX(-50%);bottom:16px;z-index:10;color:#A8A7C4;
  font-family:JBMono,monospace;font-weight:400;font-size:11.5px;letter-spacing:.06em;
  background:rgba(24,26,46,.8);padding:6px 14px;border-radius:4px;border:1px solid #3A3C63}
.deckttl{position:fixed;left:16px;bottom:14px;z-index:10;color:#A8A7C4;font-family:Pretendard;
  font-weight:700;font-size:12.5px;letter-spacing:.02em}
.deckttl b{color:#DAD8EE}
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
function upd(){const i=cur();count.textContent=String(i+1).padStart(2,'0')+' / '+total;bar.style.width=((i+1)/total*100)+'%';}
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


# ── 부품 ────────────────────────────────────────────────
def _items(items):
    out = []
    for it in items:
        lvl = it[0]
        txt = it[1]
        cls = it[2] if len(it) > 2 and it[2] else ""
        c = "none" if lvl < 0 else ("sub2" if lvl >= 1 else "")
        out.append(f'<li class="{c} {cls}">{txt}</li>')
    return '<ul class="b">' + ''.join(out) + '</ul>'


def _stat(stat):
    its = ''.join(f'<div class="it"><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b, s in stat)
    return f'<div class="stat">{its}</div>'


def _astat(stat):
    its = ''.join(f'<div class="it"><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b, s in stat)
    return f'<div class="astat">{its}</div>'


def _foot(src, pg):
    return f'<div class="foot"><span class="src">{esc(src)}</span><span class="pg">{pg:02d}</span></div>'


def _tagcls(tag):
    """태그 색이 곧 근거등급 색 — 상단 2px 라인과 같은 값을 쓴다."""
    if not tag:
        return ""
    return (tag[1] if isinstance(tag, tuple) else "") or ""


def _tag(tag):
    if not tag:
        return ""
    t, c = tag if isinstance(tag, tuple) else (tag, "")
    return f'<span class="tag {c}">{esc(t)}</span>'


def _grade(tag):
    c = _tagcls(tag)
    return f'<div class="grade{(" g-" + c) if c else ""}"></div>'


def _gauge(on=100):
    """100칸 = 한 바이알 100 U."""
    cells = ''.join(f'<i class="{"on" if i < on else ""}"></i>' for i in range(100))
    return f'<div class="gauge">{cells}</div>'


# ── 슬라이드 ────────────────────────────────────────────
def slide(s, pg):
    T = s['t']
    g = _grade(s.get('tag'))

    if T == 'title':
        return f'''<section class="snap title"><div class="stage">{g}<div class="pad">
<div class="eb">{esc(s['eyebrow'])}</div>
<div class="titlerow"><div class="tl"><h1 class="t">{s['title']}</h1><div class="rule"></div>
<div class="sub">{esc(s['sub'])}</div><div class="order">{esc(s['order'])}</div></div>
<div class="vial"><div class="vh">1 vial = 100 U</div>{_gauge(100)}
<div class="vc">모든 용량은 <b>onabotulinumtoxinA</b> 기준 — 제제 간 단위 교환 불가</div></div></div>
{_foot(s['series'], pg)}</div></div></section>'''

    if T == 'bullets':
        stat = _stat(s['stat']) if s.get('stat') else ''
        note = f'<div class="note">{s["note"]}</div>' if s.get('note') else ''
        return f'''<section class="snap content"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>{_items(s['items'])}{note}{stat}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'split':
        a = s['aside']
        inner = _astat(a['stat']) if a.get('stat') else _items(a['items'])
        dark = ' dark' if a.get('dark') else ''
        return f'''<section class="snap split"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>
<div class="row"><div class="col">{_items(s['items'])}</div>
<div class="aside{dark}"><div class="at">{esc(a['title'])}</div>{inner}</div></div>
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'table':
        head = '<tr>' + ''.join(f'<th>{esc(h)}</th>' for h in s['headers']) + '</tr>'
        hl = set(s.get('hlrows', []))
        body = ''
        for ri, r in enumerate(s['rows']):
            cls = ' class="hl"' if ri in hl else ''
            body += f'<tr{cls}>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
        note = f'<div class="note">{s["note"]}</div>' if s.get('note') else ''
        dense = ' dense' if s.get('dense') else ''
        return f'''<section class="snap tableS{dense}"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2><table class="t">{head}{body}</table>{note}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'figure':
        cap = f'<div class="figcap">{s["caption"]}</div>' if s.get('caption') else ''
        return f'''<section class="snap figure"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2>
<div class="figbox">{s['svg']}</div>{cap}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'bigfig':
        return f'''<section class="snap bigfig"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">{esc(s['eyebrow'])}</div>{_tag(s.get('tag'))}</div>
<h2 class="ct">{s['title']}</h2>
<div class="bigimg">{s['svg']}</div>
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'key':
        msgs = ''.join(
            f'<div class="msg"><div class="ml">{esc(l)}</div><div class="md">{d}</div></div>'
            for l, d in s['msgs'])
        return f'''<section class="snap key"><div class="stage">{g}<div class="pad">
<div class="keb">{esc(s['eyebrow'])}</div><h2 class="kh">{s['headline']}</h2>
{msgs}</div></div></section>'''

    if T == 'refs':
        n = len(s['refs'])
        half = (n + 1) // 2

        def col(rs):
            return '<div class="c">' + ''.join(rs) + '</div>'

        mk = [f'<a href="{u}" target="_blank" rel="noopener">{t}</a>' if u
              else f'<div class="r">{t}</div>' for t, u in s['refs']]
        return f'''<section class="snap refs"><div class="stage">{g}<div class="pad">
<div class="topbar"><div class="eb">references</div><span class="tag ink">PubMed</span></div>
<h2 class="ct">{s['title']}</h2><div class="hr"></div>
<div class="cols">{col(mk[:half])}{col(mk[half:])}</div>
{_foot("제목 클릭 시 PubMed로 이동", pg)}</div></div></section>'''
    return ''


def render_deck(title, slides):
    body = ''.join(slide(s, i + 1) for i, s in enumerate(slides))
    return f'''<title>{esc(title)}</title>
<style>{CSS}</style>
<div class="bar"></div><div class="count"></div><div class="deckttl">{esc(title)}</div>
<div class="hint">← → · scroll</div>
<div class="deck">{body}</div>
<script>{JS}</script>'''
