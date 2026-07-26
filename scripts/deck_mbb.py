# -*- coding: utf-8 -*-
"""
요추 내측지차단(MBB) / 후관절차단(FJB) 덱 렌더러 — "Atlas & Console"

디자인 원칙
  · 중립색은 청색 편향(bone-window grey). 순회색·크림 배제.
  · 강조색 2개는 '의미'를 갖는다: nerve-gold = 신경/내측지/MBB, joint-slate = 관절/관절강내 주사.
    색이 곧 정보이므로 장식 목적으로 두 색을 섞어 쓰지 않는다.
  · 숫자·레벨코드·계측치는 전부 IBM Plex Mono (투시 판독 주석의 목소리).
  · 레벨별 내용을 다루는 슬라이드에는 L1-2 ~ L5-S1 레일을 붙여 위치를 고정한다.
"""
import html as _h

def esc(s):
    return _h.escape(str(s), quote=True)


CSS = r"""
@font-face{font-family:Pretendard;font-weight:900;font-display:swap;src:url(__P900__) format("woff2")}
@font-face{font-family:Pretendard;font-weight:800;font-display:swap;src:url(__P800__) format("woff2")}
@font-face{font-family:Pretendard;font-weight:600;font-display:swap;src:url(__P600__) format("woff2")}
@font-face{font-family:Pretendard;font-weight:400;font-display:swap;src:url(__P400__) format("woff2")}
@font-face{font-family:Pretendard;font-weight:300;font-display:swap;src:url(__P300__) format("woff2")}
@font-face{font-family:PlexM;font-weight:500;font-display:swap;src:url(__M500__) format("woff2")}
@font-face{font-family:PlexM;font-weight:600;font-display:swap;src:url(__M600__) format("woff2")}

:root{
  --room:#D9DFE3;        /* 판독실 배경 */
  --stage:#F7F9FA;       /* 슬라이드 지면 */
  --panel:#EDF1F3;       /* 보조 패널 */
  --ink:#141A1F;         /* 방사선 흑 (청색 편향) */
  --ink2:#33404A;
  --muted:#6B7883;
  --line:#DAE1E6;
  --line2:#C6D0D7;
  --nerve:#9C7010;       /* 신경 = 해부도감 황색 계열, 밝은 배경용 심도 */
  --nerveB:#E0AE33;      /* 어두운 배경/도해용 */
  --nerveW:#FBF3DF;      /* 신경 계열 wash */
  --joint:#25647F;       /* 관절 = 슬레이트 블루 */
  --jointB:#6FB6D6;
  --jointW:#E6EFF4;
  --crit:#A8382B;
  --critW:#F8EBE8;
  --good:#2C6A4C;
  --goodW:#E7F1EB;
  --shadow:0 12px 44px rgba(16,26,33,.20);
  /* 표지·섹션·요약 슬라이드는 두 테마 모두에서 어둡게 유지한다 — 아래 토큰은 재정의하지 않는다 */
  --dbg:#141A1F; --dfg:#F2F7F9; --dfg2:#CBD8E0; --dline:#26333D; --dmuted:#7B8A96;
}
@media (prefers-color-scheme:dark){
  :root{
    --room:#0B1116;--stage:#151D24;--panel:#1D262E;--ink:#E8EFF3;--ink2:#C2CED6;--muted:#8B99A4;
    --line:#2A353E;--line2:#3A4753;--nerve:#E7B843;--nerveB:#F0C75A;--nerveW:#2A2413;
    --joint:#79BFDD;--jointB:#8CCBE6;--jointW:#12262F;--crit:#E38073;--critW:#2E1A17;
    --good:#6FBE93;--goodW:#12261C;--shadow:0 12px 44px rgba(0,0,0,.55);
  }
}
:root[data-theme="dark"]{
  --room:#0B1116;--stage:#151D24;--panel:#1D262E;--ink:#E8EFF3;--ink2:#C2CED6;--muted:#8B99A4;
  --line:#2A353E;--line2:#3A4753;--nerve:#E7B843;--nerveB:#F0C75A;--nerveW:#2A2413;
  --joint:#79BFDD;--jointB:#8CCBE6;--jointW:#12262F;--crit:#E38073;--critW:#2E1A17;
  --good:#6FBE93;--goodW:#12261C;--shadow:0 12px 44px rgba(0,0,0,.55);
}
:root[data-theme="light"]{
  --room:#D9DFE3;--stage:#F7F9FA;--panel:#EDF1F3;--ink:#141A1F;--ink2:#33404A;--muted:#6B7883;
  --line:#DAE1E6;--line2:#C6D0D7;--nerve:#9C7010;--nerveB:#E0AE33;--nerveW:#FBF3DF;
  --joint:#25647F;--jointB:#6FB6D6;--jointW:#E6EFF4;--crit:#A8382B;--critW:#F8EBE8;
  --good:#2C6A4C;--goodW:#E7F1EB;--shadow:0 12px 44px rgba(16,26,33,.20);
}

*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--room);color:var(--ink);
  font-family:Pretendard,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
  font-weight:300;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}

.deck{height:100vh;overflow-y:scroll;scroll-snap-type:y mandatory;scroll-behavior:smooth}
@media (prefers-reduced-motion:reduce){.deck{scroll-behavior:auto}}
.snap{height:100vh;scroll-snap-align:center;display:flex;align-items:center;justify-content:center;padding:2vh 1.8vw}
.stage{width:min(95vw,1240px);aspect-ratio:16/9;container-type:inline-size;position:relative;
  background:var(--stage);border-radius:10px;overflow:hidden;box-shadow:var(--shadow)}
.pad{position:absolute;inset:0;padding:4.9cqw 5.8cqw;display:flex;flex-direction:column;overflow:hidden}

/* ---- 공통 타이포 ---- */
.eb{font-family:PlexM,ui-monospace,monospace;font-weight:600;font-size:1.72cqw;letter-spacing:.17em;
  text-transform:uppercase;color:var(--nerve)}
.eb.j{color:var(--joint)}
.eb.n{color:var(--muted)}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:2cqw;flex:none}
.tag{font-family:PlexM,monospace;font-weight:600;font-size:1.62cqw;letter-spacing:.06em;color:var(--stage);
  padding:.62cqw 1.35cqw;border-radius:3px;background:var(--ink);white-space:nowrap}
.tag.nerve{background:var(--nerve)}.tag.joint{background:var(--joint)}
.tag.crit{background:var(--crit)}.tag.good{background:var(--good)}
.tag.ghost{background:transparent;color:var(--muted);border:1.4px solid var(--line2)}
h2.ct{margin:.8cqw 0 0;font-weight:800;font-size:3.44cqw;line-height:1.14;letter-spacing:-.022em;
  color:var(--ink);text-wrap:balance}
.kick{font-weight:600;font-size:1.94cqw;line-height:1.28;color:var(--nerve);margin-top:.85cqw;text-wrap:balance}
.kick.j{color:var(--joint)}
.hr{height:1.4px;background:var(--line);margin:1.25cqw 0 1.6cqw;flex:none}

/* ---- 리스트 ---- */
ul.b{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:1.1cqw}
ul.b li{font-weight:300;font-size:2.0cqw;line-height:1.3;color:var(--ink2);padding-left:2.9cqw;position:relative}
ul.b li::before{content:"";position:absolute;left:.2cqw;top:.86cqw;width:1.0cqw;height:1.0cqw;
  background:var(--nerve);border-radius:1px;transform:rotate(45deg)}
ul.b li.j::before{background:var(--joint)}
ul.b li.s{padding-left:5.2cqw;font-size:1.84cqw;color:var(--muted)}
ul.b li.s::before{left:2.9cqw;top:1.5cqw;width:1.35cqw;height:.16cqw;border-radius:0;transform:none;background:var(--line2)}
ul.b li.n{padding-left:0}
ul.b li.n::before{display:none}
ul.b li b{font-weight:700;color:var(--ink)}
ul.b li code,code.m{font-family:PlexM,monospace;font-weight:600;font-size:.94em;letter-spacing:-.01em;
  background:var(--panel);padding:.06em .4em;border-radius:3px;color:var(--ink)}
li.hi,li.hi b{color:var(--nerve)}
li.hj,li.hj b{color:var(--joint)}
li.hr_,li.hr_ b{color:var(--crit)}
li.hg,li.hg b{color:var(--good)}

/* ---- 레이아웃 ---- */
.row{display:flex;gap:3.2cqw;flex:1;min-height:0}
.col{flex:1;min-width:0;display:flex;flex-direction:column}
.aside{width:30cqw;flex:none;background:var(--panel);border:1.4px solid var(--line);border-radius:8px;
  padding:1.95cqw 2.1cqw;display:flex;flex-direction:column;min-height:0}
.aside.nerve{background:var(--nerveW);border-color:color-mix(in srgb,var(--nerve) 30%,transparent)}
.aside.joint{background:var(--jointW);border-color:color-mix(in srgb,var(--joint) 30%,transparent)}
.aside.crit{background:var(--critW);border-color:color-mix(in srgb,var(--crit) 30%,transparent)}
.aside .at{font-family:PlexM,monospace;font-weight:600;font-size:1.58cqw;letter-spacing:.12em;
  text-transform:uppercase;color:var(--muted);margin-bottom:1.15cqw;flex:none}
.aside ul.b{gap:.88cqw}
.aside ul.b li{font-size:1.8cqw;line-height:1.28}

/* ---- 수치 스트립 ---- */
.stat{display:flex;gap:3.2cqw;border-top:1.4px solid var(--line);padding-top:1.7cqw;margin-top:auto;flex:none}
.stat .it{display:flex;flex-direction:column;gap:.35cqw}
.stat .it b{font-family:PlexM,monospace;font-weight:600;font-size:3.1cqw;letter-spacing:-.035em;
  color:var(--nerve);line-height:1;font-variant-numeric:tabular-nums}
.stat .it.j b{color:var(--joint)}.stat .it.r b{color:var(--crit)}.stat .it.g b{color:var(--good)}
.stat .it span{font-weight:600;font-size:1.54cqw;color:var(--muted);letter-spacing:.01em}
.astat{display:flex;flex-direction:column;gap:1.15cqw;margin-top:.2cqw}
.astat .it b{font-family:PlexM,monospace;font-weight:600;font-size:2.6cqw;color:var(--nerve);
  letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums;display:block}
.astat .it.j b{color:var(--joint)}.astat .it.r b{color:var(--crit)}
.astat .it span{font-weight:600;font-size:1.52cqw;color:var(--muted);display:block;margin-top:.3cqw}

/* ---- 표 ---- */
.tw{flex:1;min-height:0;overflow:hidden;display:flex}
table.t{width:100%;border-collapse:collapse;margin-top:.6cqw;font-variant-numeric:tabular-nums;align-self:flex-start}
table.t th{background:var(--ink);color:var(--stage);font-weight:700;font-size:1.72cqw;text-align:left;
  padding:1.12cqw 1.25cqw;letter-spacing:-.005em;line-height:1.2}
table.t th:not(:first-child){text-align:center}
table.t th.nerve{background:var(--nerve)}table.t th.joint{background:var(--joint)}
table.t td{font-weight:300;font-size:1.71cqw;color:var(--ink2);padding:.92cqw 1.25cqw;
  border-bottom:1.2px solid var(--line);text-align:center;line-height:1.26}
table.t td:first-child{text-align:left;font-weight:700;color:var(--ink)}
table.t tr:nth-child(even) td{background:color-mix(in srgb,var(--panel) 62%,transparent)}
table.t td b{font-weight:700;color:var(--ink)}
table.t td .lv,table.t td code,td.mono{font-family:PlexM,monospace;font-weight:600;font-size:.97em;letter-spacing:-.02em}
table.t td.nv{color:var(--nerve);font-weight:600}
table.t td.jv{color:var(--joint);font-weight:600}
table.t tr.hl td{background:var(--nerveW)}
table.t tr.hl td:first-child{box-shadow:inset 3px 0 0 var(--nerve)}
table.t tr.hlj td{background:var(--jointW)}
table.t tr.hlj td:first-child{box-shadow:inset 3px 0 0 var(--joint)}
table.t.dense td{font-size:1.55cqw;padding:.72cqw 1.05cqw}
table.t.dense th{font-size:1.58cqw;padding:.92cqw 1.05cqw}
table.t.xdense td{font-size:1.38cqw;padding:.5cqw .82cqw;line-height:1.22}
table.t.xdense th{font-size:1.4cqw;padding:.66cqw .82cqw}
.tableS .note{font-size:1.5cqw}

.note{font-weight:600;font-size:1.6cqw;color:var(--muted);margin-top:1.1cqw;line-height:1.32;flex:none}
.note b{color:var(--nerve);font-weight:700}
.note.j b{color:var(--joint)}
.note.warn{color:var(--crit)}.note.warn b{color:var(--crit)}

.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;gap:2cqw;
  color:var(--muted);border-top:1.4px solid var(--line);padding-top:1.5cqw;flex:none}
.content .foot,.split .foot,.tableS .foot,.figure .foot,.cmp .foot{margin-top:1.4cqw}
.foot .src{font-weight:300;font-size:1.56cqw;line-height:1.25}
.foot .pg{font-family:PlexM,monospace;font-weight:600;font-size:1.72cqw;font-variant-numeric:tabular-nums;flex:none}

/* ---- 표지 ---- */
.title .stage{background:var(--dbg)}
.title .pad{padding:6.2cqw 6.6cqw}
.title .tick{position:absolute;left:0;top:0;width:.85cqw;height:100%;background:#E0AE33}
.title .teb{font-family:PlexM,monospace;font-weight:600;font-size:1.7cqw;letter-spacing:.2em;
  text-transform:uppercase;color:#E0AE33}
.title h1{margin:2.4cqw 0 0;font-weight:900;font-size:5.6cqw;line-height:1.06;letter-spacing:-.032em;
  color:var(--dfg);text-wrap:balance;max-width:74cqw}
.title .en{font-family:PlexM,monospace;font-weight:500;font-size:1.56cqw;color:var(--dmuted);margin-top:1.5cqw;
  letter-spacing:0;line-height:1.5;max-width:62cqw}
.title .rule{height:1.4px;background:var(--dline);margin:3.1cqw 0 2.5cqw;width:34cqw}
.title .sub{font-weight:300;font-size:2.32cqw;color:var(--dfg2);line-height:1.4;max-width:66cqw}
.title .meta{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;
  border-top:1.4px solid var(--dline);padding-top:1.9cqw}
.title .meta .l{font-weight:600;font-size:1.66cqw;color:var(--dmuted);line-height:1.5}
.title .meta .r{font-family:PlexM,monospace;font-weight:600;font-size:1.66cqw;color:var(--nerveB);
  letter-spacing:.06em;text-align:right;line-height:1.5}

/* ---- 섹션 구분 ---- */
.sec .stage{background:var(--dbg)}
.sec .pad{padding:6cqw 6.6cqw;justify-content:center}
.sec .no{font-family:PlexM,monospace;font-weight:600;font-size:9.5cqw;line-height:.9;color:var(--dline);
  letter-spacing:-.05em;font-variant-numeric:tabular-nums}
.sec h2{margin:1.4cqw 0 0;font-weight:900;font-size:4.5cqw;line-height:1.1;letter-spacing:-.028em;color:var(--dfg);text-wrap:balance}
.sec .d{font-weight:300;font-size:2.15cqw;color:var(--dfg2);margin-top:1.5cqw;line-height:1.38;max-width:62cqw}
.sec .sline{height:1.4px;background:#E0AE33;width:12cqw;margin-top:2.6cqw}
.sec .pg{position:absolute;right:6.6cqw;bottom:5.4cqw;font-family:PlexM,monospace;font-weight:600;
  font-size:1.72cqw;color:var(--dmuted)}

/* ---- 핵심 정리(다크) ---- */
.key .stage{background:var(--dbg)}
.key .pad{padding:4.4cqw 5.6cqw}
.key .keb{font-family:PlexM,monospace;font-weight:600;font-size:1.7cqw;letter-spacing:.18em;
  text-transform:uppercase;color:#E0AE33}
.key h2{margin:1.1cqw 0 1.5cqw;font-weight:900;font-size:3.4cqw;line-height:1.12;letter-spacing:-.026em;
  color:var(--dfg);text-wrap:balance}
.key .msg{display:flex;gap:2.2cqw;align-items:flex-start;padding:.82cqw 0;border-top:1.2px solid var(--dline)}
.key .msg .ml{flex:none;width:17cqw;font-family:PlexM,monospace;font-weight:600;font-size:1.6cqw;
  color:#E0AE33;letter-spacing:.02em;padding-top:.22cqw}
.key .msg .ml.j{color:#6FB6D6}
.key .msg .md{font-weight:300;font-size:1.72cqw;line-height:1.28;color:var(--dfg2)}
.key .msg .md b{font-weight:700;color:var(--dfg)}
.key .foot{border-top:1.2px solid var(--dline);color:var(--dmuted)}

/* ---- 비교(2단) ---- */
.cmp .cols{display:flex;gap:2.6cqw;flex:1;min-height:0}
.cmp .cd{flex:1;border-radius:8px;padding:1.8cqw 1.9cqw;display:flex;flex-direction:column;min-width:0;
  border:1.4px solid var(--line)}
.cmp .cd.n{background:var(--nerveW);border-color:color-mix(in srgb,var(--nerve) 34%,transparent)}
.cmp .cd.j{background:var(--jointW);border-color:color-mix(in srgb,var(--joint) 34%,transparent)}
.cmp .cd .h{display:flex;align-items:baseline;gap:.9cqw;margin-bottom:.4cqw;flex-wrap:wrap}
.cmp .cd .h .hn{font-weight:800;font-size:2.42cqw;letter-spacing:-.02em;color:var(--nerve)}
.cmp .cd.j .h .hn{color:var(--joint)}
.cmp .cd .h .he{font-family:PlexM,monospace;font-weight:500;font-size:1.42cqw;color:var(--muted);
  white-space:nowrap}
.cmp .cd .sl{font-weight:600;font-size:1.7cqw;color:var(--ink2);margin-bottom:1.15cqw;line-height:1.28}
.cmp .cd ul.b{gap:.86cqw}
.cmp .cd ul.b li{font-size:1.76cqw;line-height:1.29;padding-left:2.4cqw}
.cmp .cd ul.b li::before{width:.85cqw;height:.85cqw;top:.78cqw;background:var(--nerve)}
.cmp .cd.j ul.b li::before{background:var(--joint)}
.cmp .cd ul.b li.s{padding-left:4.6cqw;font-size:1.62cqw}
.cmp .cd ul.b li.s::before{width:1.2cqw;height:.15cqw;top:1.3cqw;left:2.4cqw;border-radius:0;
  transform:none;background:var(--line2)}
.cmp .cd .cf{margin-top:auto;padding-top:1.2cqw;border-top:1.2px solid color-mix(in srgb,var(--ink) 12%,transparent);
  font-family:PlexM,monospace;font-weight:600;font-size:1.5cqw;color:var(--nerve);line-height:1.35}
.cmp .cd.j .cf{color:var(--joint)}

/* ---- 도해 ---- */
.figure .pad,.bigfig .pad{padding-top:3.9cqw;padding-bottom:3.6cqw}
.figure h2.ct,.bigfig h2.ct{font-size:3.32cqw}
.figure .kick,.bigfig .kick{font-size:1.92cqw;margin-top:.6cqw}
.figure .fb{flex:1;display:flex;align-items:stretch;justify-content:center;gap:2cqw;min-height:0;margin:.9cqw 0 .8cqw}
.figure .fb.one{padding:0 13cqw}
.fp{flex:1;background:var(--panel);border:1.4px solid var(--line);border-radius:8px;
  padding:1.3cqw 1.3cqw 1.1cqw;display:flex;flex-direction:column;align-items:stretch;gap:.6cqw;min-width:0;min-height:0}
.fp.n{background:var(--nerveW);border-color:color-mix(in srgb,var(--nerve) 28%,transparent)}
.fp.j{background:var(--jointW);border-color:color-mix(in srgb,var(--joint) 28%,transparent)}
.fp.bad{background:var(--critW);border-color:color-mix(in srgb,var(--crit) 28%,transparent)}
.fp.ok{background:var(--goodW);border-color:color-mix(in srgb,var(--good) 28%,transparent)}
.fp .pt{font-family:PlexM,monospace;font-weight:600;font-size:1.52cqw;letter-spacing:.05em;color:var(--ink);flex:none;text-align:center}
.fp.bad .pt{color:var(--crit)}.fp.ok .pt{color:var(--good)}
.fsvg{flex:1;min-height:0;position:relative;width:100%}
.fsvg svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.fp .pl{font-weight:300;font-size:1.5cqw;color:var(--ink2);text-align:center;line-height:1.28;flex:none}
.fp .pl b{color:var(--ink);font-weight:700}
.figcap{font-weight:600;font-size:1.66cqw;color:var(--ink2);text-align:center;line-height:1.32;flex:none}
.figcap b{color:var(--nerve);font-weight:700}
.bigfig .bw{flex:1;min-height:0;position:relative;width:100%;margin:1cqw 0 .7cqw}
.bigfig .bw svg{position:absolute;inset:0;width:100%;height:100%;display:block}
.bigfig .foot{margin-top:.7cqw}
svg text{font-family:Pretendard,-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif}
svg text.m{font-family:PlexM,ui-monospace,monospace;letter-spacing:-.02em}

/* ---- 레벨 레일 ---- */
.rail{position:absolute;right:1.9cqw;top:50%;transform:translateY(-50%);display:flex;flex-direction:column;
  gap:.55cqw;align-items:flex-end}
.rail .lv{font-family:PlexM,monospace;font-weight:600;font-size:1.28cqw;color:var(--line2);
  letter-spacing:.02em;padding:.24cqw .5cqw;border-radius:3px;line-height:1}
.rail .lv.on{color:var(--stage);background:var(--nerve)}
.rail .lv.onj{color:var(--stage);background:var(--joint)}
.rail .lv.dim{color:var(--muted)}
.hasrail .pad{padding-right:8.4cqw}

/* ---- 참고문헌 ---- */
.refs .cols{display:flex;gap:3.2cqw;flex:1;min-height:0}
.refs .cols .c{flex:1;display:flex;flex-direction:column;gap:.6cqw;min-width:0}
.refs .r{font-weight:300;font-size:1.2cqw;line-height:1.24;color:var(--ink2);display:flex;gap:.7cqw}
.refs .r .n{font-family:PlexM,monospace;font-weight:600;color:var(--nerve);flex:none;font-size:1.2cqw;padding-top:.06cqw}
.refs .r b{font-weight:700;color:var(--ink)}

/* ---- UI 크롬 ---- */
.bar{position:fixed;top:0;left:0;height:3px;background:var(--nerve);width:0;z-index:10;transition:width .18s}
.count{position:fixed;right:14px;bottom:12px;z-index:10;background:color-mix(in srgb,var(--ink) 88%,transparent);
  color:var(--stage);font-family:PlexM,monospace;font-weight:600;font-size:12px;padding:5px 11px;
  border-radius:4px;font-variant-numeric:tabular-nums;letter-spacing:.03em}
.hint{position:fixed;left:50%;transform:translateX(-50%);bottom:14px;z-index:10;color:var(--muted);
  font-family:PlexM,monospace;font-weight:500;font-size:11.5px;letter-spacing:.04em;
  background:color-mix(in srgb,var(--stage) 92%,transparent);padding:5px 13px;border-radius:4px;border:1.2px solid var(--line)}
.dt{position:fixed;left:14px;bottom:12px;z-index:10;color:var(--muted);font-family:PlexM,monospace;
  font-weight:600;font-size:11.5px;letter-spacing:.03em}
:focus-visible{outline:2.5px solid var(--nerve);outline-offset:2px}

@media print{
  @page{size:landscape;margin:0}
  body{background:#fff}
  .deck{height:auto;overflow:visible;display:block}
  .snap{height:auto;page-break-after:always;padding:0}
  .stage{width:100%;box-shadow:none;border-radius:0}
  .bar,.count,.hint,.dt{display:none}
}
@media (max-width:640px){
  .snap{padding:1.2vh 1.2vw}
  .hint{display:none}
}
"""

JS = r"""
const deck=document.querySelector('.deck');
const snaps=[...document.querySelectorAll('.snap')];
const bar=document.querySelector('.bar');
const count=document.querySelector('.count');
const total=snaps.length;
function cur(){return Math.max(0,Math.min(total-1,Math.round(deck.scrollTop/window.innerHeight)));}
function upd(){const i=cur();count.textContent=String(i+1).padStart(2,'0')+' / '+total;bar.style.width=((i+1)/total*100)+'%';}
function go(i){i=Math.max(0,Math.min(total-1,i));snaps[i].scrollIntoView();setTimeout(upd,60);}
deck.addEventListener('scroll',()=>window.requestAnimationFrame(upd),{passive:true});
addEventListener('keydown',e=>{
  if(e.metaKey||e.ctrlKey||e.altKey)return;
  if(['ArrowDown','ArrowRight','PageDown',' '].includes(e.key)){e.preventDefault();go(cur()+1);}
  else if(['ArrowUp','ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(cur()-1);}
  else if(e.key==='Home'){e.preventDefault();go(0);}
  else if(e.key==='End'){e.preventDefault();go(total-1);}
});
/* 내용이 슬라이드를 넘치면 균일 축소로 맞춘다.
   cqw 기반 레이아웃이라 transform 배율이 글자·간격·도해에 동일하게 적용된다. */
function over(pad){
  /* 바깥 여백뿐 아니라 카드·사이드패널 내부 넘침까지 본다 —
     .cd 안에서 넘치면 글이 카드 밖으로 새어 각주와 겹친다. */
  let o=pad.scrollHeight-pad.clientHeight;
  pad.querySelectorAll('.cd,.aside,.col,.fp').forEach(el=>{
    o=Math.max(o, el.scrollHeight-el.clientHeight);
  });
  return o;
}
function fit(){
  document.querySelectorAll('.stage').forEach(st=>{
    const pad=st.querySelector('.pad'); if(!pad) return;
    pad.style.width=''; pad.style.height=''; pad.style.transform='';
    let k=1;
    while(over(pad)>1 && k>0.84){
      k=Math.round((k-0.02)*100)/100;
      pad.style.width=(100/k)+'%';
      pad.style.height=(100/k)+'%';
      pad.style.transformOrigin='top left';
      pad.style.transform='scale('+k+')';
    }
  });
}
fit();
addEventListener('resize',()=>{clearTimeout(window.__ft);window.__ft=setTimeout(fit,140);});
if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);

const hint=document.querySelector('.hint');
if(hint){setTimeout(()=>{hint.style.transition='opacity .55s';hint.style.opacity='0';},4500);}
upd();
"""

LEVELS = ["L1-2", "L2-3", "L3-4", "L4-5", "L5-S1"]


# ---------------- 조각 렌더러 ----------------
def _items(items):
    """items: (level, text, cls) — level -1 = 불릿 없음, 0 = 기본, 1 = 하위"""
    out = []
    for it in items:
        lvl, txt = it[0], it[1]
        cls = it[2] if len(it) > 2 and it[2] else ""
        base = "n" if lvl < 0 else ("s" if lvl >= 1 else "")
        out.append(f'<li class="{base} {cls}">{txt}</li>')
    return '<ul class="b">' + ''.join(out) + '</ul>'


def _stat(stat):
    its = ''.join(f'<div class="it {c}"><b>{esc(b)}</b><span>{esc(s)}</span></div>'
                  for b, s, *rest in stat for c in [rest[0] if rest else ""])
    return f'<div class="stat">{its}</div>'


def _astat(stat):
    its = ''.join(f'<div class="it {c}"><b>{esc(b)}</b><span>{esc(s)}</span></div>'
                  for b, s, *rest in stat for c in [rest[0] if rest else ""])
    return f'<div class="astat">{its}</div>'


def _foot(src, pg):
    return f'<div class="foot"><span class="src">{src}</span><span class="pg">{pg:02d}</span></div>'


def _tag(tag):
    if not tag:
        return ""
    t, c = tag if isinstance(tag, tuple) else (tag, "")
    return f'<span class="tag {c}">{esc(t)}</span>'


def _rail(active, tone="on"):
    """
    active: 강조할 레벨 리스트, 또는 'all'.
    'all'은 전 레벨 공통 내용이라는 뜻이므로 채우지 않고 은은하게만 표시한다 —
    특정 레벨을 지목할 때에만 색이 들어가야 색이 정보로 작동한다.
    """
    if not active:
        return ""
    rows = []
    for lv in LEVELS:
        if active == "all":
            rows.append(f'<div class="lv dim">{lv}</div>')
        elif lv in active:
            rows.append(f'<div class="lv {tone}">{lv}</div>')
        else:
            rows.append(f'<div class="lv">{lv}</div>')
    return '<div class="rail">' + ''.join(rows) + '</div>'


def _head(s):
    return (f'<div class="topbar"><div class="eb {s.get("ebc","")}">{esc(s["eyebrow"])}</div>'
            f'{_tag(s.get("tag"))}</div><h2 class="ct">{s["title"]}</h2>'
            + (f'<div class="kick {s.get("kickc","")}">{s["kick"]}</div>' if s.get("kick") else ''))


# ---------------- 슬라이드 ----------------
def slide(s, pg):
    T = s['t']
    rail = _rail(s.get('rail'), s.get('railtone', 'on'))
    hr = ' hasrail' if rail else ''

    if T == 'title':
        return f'''<section class="snap title"><div class="stage"><div class="tick"></div><div class="pad">
<div class="teb">{esc(s['eyebrow'])}</div><h1>{s['title']}</h1>
<div class="en">{s['en']}</div><div class="rule"></div><div class="sub">{s['sub']}</div>
<div class="meta"><div class="l">{s['metaL']}</div><div class="r">{s['metaR']}</div></div>
</div></div></section>'''

    if T == 'sec':
        return f'''<section class="snap sec"><div class="stage"><div class="pad">
<div class="no">{esc(s['no'])}</div><h2>{s['title']}</h2><div class="d">{s['desc']}</div>
<div class="sline"></div></div><div class="pg">{pg:02d}</div></div></section>'''

    if T == 'bullets':
        stat = _stat(s['stat']) if s.get('stat') else ''
        note = f'<div class="note {s.get("notec","")}">{s["note"]}</div>' if s.get('note') else ''
        return f'''<section class="snap content{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="hr"></div>{_items(s['items'])}{note}{stat}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'split':
        a = s['aside']
        inner = _astat(a['stat']) if a.get('stat') else _items(a['items'])
        extra = f'<div class="note {a.get("notec","")}" style="margin-top:1.2cqw">{a["note"]}</div>' if a.get('note') else ''
        note = f'<div class="note {s.get("notec","")}">{s["note"]}</div>' if s.get('note') else ''
        return f'''<section class="snap split{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="hr"></div>
<div class="row"><div class="col">{_items(s['items'])}{note}</div>
<div class="aside {a.get('tone','')}"><div class="at">{esc(a['title'])}</div>{inner}{extra}</div></div>
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'table':
        ths = []
        for h in s['headers']:
            if isinstance(h, tuple):
                ths.append(f'<th class="{h[1]}">{h[0]}</th>')
            else:
                ths.append(f'<th>{h}</th>')
        head = '<tr>' + ''.join(ths) + '</tr>'
        hl = dict(s.get('hlrows', {}))
        body = ''
        for ri, r in enumerate(s['rows']):
            cls = f' class="{hl[ri]}"' if ri in hl else ''
            body += f'<tr{cls}>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
        note = f'<div class="note {s.get("notec","")}">{s["note"]}</div>' if s.get('note') else ''
        n = len(s['rows'])
        dense = ' xdense' if (s.get('dense') and n >= 7) else (' dense' if s.get('dense') else '')
        return f'''<section class="snap tableS{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="tw"><table class="t{dense}">{head}{body}</table></div>{note}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'cmp':
        cds = ''
        for c in s['cards']:
            foot = f'<div class="cf">{c["cf"]}</div>' if c.get('cf') else ''
            cds += (f'<div class="cd {c["tone"]}"><div class="h"><span class="hn">{c["name"]}</span>'
                    f'<span class="he">{esc(c.get("en",""))}</span></div>'
                    f'<div class="sl">{c["sl"]}</div>{_items(c["items"])}{foot}</div>')
        return f'''<section class="snap cmp{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="hr"></div><div class="cols">{cds}</div>
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'figure':
        panels = ''
        for p in s['panels']:
            pl = f'<div class="pl">{p["pl"]}</div>' if p.get('pl') else ''
            panels += (f'<div class="fp {p.get("tone","")}"><div class="pt">{p["pt"]}</div>'
                       f'<div class="fsvg">{p["svg"]}</div>{pl}</div>')
        cap = f'<div class="figcap">{s["caption"]}</div>' if s.get('caption') else ''
        one = ' one' if len(s['panels']) == 1 else ''
        return f'''<section class="snap figure{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="fb{one}">{panels}</div>{cap}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'bigfig':
        cap = f'<div class="figcap">{s["caption"]}</div>' if s.get('caption') else ''
        return f'''<section class="snap bigfig{hr}"><div class="stage">{rail}<div class="pad">
{_head(s)}<div class="bw">{s['svg']}</div>{cap}
{_foot(s['foot'], pg)}</div></div></section>'''

    if T == 'key':
        msgs = ''.join(f'<div class="msg"><div class="ml {c}">{l}</div><div class="md">{d}</div></div>'
                       for l, d, *rest in s['msgs'] for c in [rest[0] if rest else ""])
        return f'''<section class="snap key"><div class="stage"><div class="pad">
<div class="keb">{esc(s['eyebrow'])}</div><h2>{s['title']}</h2>{msgs}
{_foot(s.get('foot', ''), pg)}</div></div></section>'''

    if T == 'refs':
        rs = s['refs']
        half = (len(rs) + 1) // 2
        def col(items, start):
            return '<div class="c">' + ''.join(
                f'<div class="r"><span class="n">{i + start:02d}</span><span>{t}</span></div>'
                for i, t in enumerate(items)) + '</div>'
        return f'''<section class="snap refs"><div class="stage"><div class="pad">
{_head(s)}<div class="hr"></div><div class="cols">{col(rs[:half], 1)}{col(rs[half:], half + 1)}</div>
{_foot(s['foot'], pg)}</div></div></section>'''

    raise ValueError(f"unknown slide type: {T}")


def render_deck(title, slides):
    body = ''.join(slide(s, i + 1) for i, s in enumerate(slides))
    return f'''<title>{esc(title)}</title>
<style>{CSS}</style>
<div class="bar"></div><div class="count"></div><div class="dt">{esc(title)}</div>
<div class="hint">← → · 스크롤 · 방향키 이동</div>
<div class="deck">{body}</div>
<script>{JS}</script>'''
