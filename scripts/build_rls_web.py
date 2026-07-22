# -*- coding: utf-8 -*-
"""하지불안증후군(RLS) 근거 기반 치료 — 자체 완결형 웹 슬라이드 덱 생성기.
Artifact로 게시 가능한 단일 HTML(외부 리소스 0). 라이트/다크 테마·키보드 네비·인쇄 지원.
콘텐츠는 02_RLS 문헌고찰 근거 기반, 프리미엄 PPT(build_rls_ppt.py)와 동일 규격."""
import html as _h

OUT = "/home/user/ppt-work/하지불안증후군_치료_발표.html"
slides = []   # list of inner-HTML strings for each .slide

def esc(t):
    return _h.escape(str(t), quote=False)

# ---------------------------------------------------------------- blocks
def bullets(items):
    """items: (level, text, tone, bold). level: 0=●, 1=–(sub), -1=(no mark, lead-out)."""
    out = ['<ul class="bl">']
    for it in items:
        lv = it[0]; tx = it[1]
        if lv < 0 and tx.startswith("→"):   # arrow is drawn by CSS for lead-out rows
            tx = tx[1:].lstrip()
        tone = it[2] if len(it) > 2 and it[2] else "ink"
        bold = it[3] if len(it) > 3 else False
        cls = f"lv{lv if lv>=0 else 'x'} t-{tone}" + (" b" if bold else "")
        out.append(f'<li class="{cls}"><span>{tx}</span></li>')
    out.append("</ul>")
    return "".join(out)

def statcard(title, stats, tone="light"):
    """stats: list of (big, label). tone: light|navy"""
    rows = "".join(
        f'<div class="st-row"><div class="st-num">{b}</div><div class="st-lab">{l}</div></div>'
        for b, l in stats)
    return f'<div class="statcard {tone}"><div class="st-title">{title}</div>{rows}</div>'

def whycard(title, lines, tone="navy"):
    """dark accent card. lines: (text, highlight?)"""
    body = "".join(
        f'<p class="{"hi" if (len(x)>1 and x[1]) else ""}">{x[0]}</p>' for x in lines)
    return f'<div class="whycard {tone}"><div class="wc-title">{title}</div>{body}</div>'

def sidecard(title, items, title_tone="teal"):
    """light bordered card with a title and bullets."""
    return f'<div class="sidecard"><div class="sc-title t-{title_tone}">{title}</div>{bullets(items)}</div>'

def compare3(cols, note=None, note_tone="ink"):
    """cols: (title, [lines], color). color in fill palette."""
    cards = ""
    for t, lines, c in cols:
        body = "".join(f"<p>{ln}</p>" for ln in lines)
        cards += f'<div class="cmp-card"><div class="cmp-head fill-{c}">{t}</div><div class="cmp-body">{body}</div></div>'
    n = f'<div class="strip"><span class="t-{note_tone}">{note}</span></div>' if note else ""
    return f'<div class="cmp3">{cards}</div>{n}'

def table(headers, rows, widths=None, small=False):
    ws = widths or [None]*len(headers)
    cg = "".join(f'<col style="width:{w}%">' if w else "<col>" for w in ws)
    th = "".join(f"<th>{h}</th>" for h in headers)
    trs = ""
    for r in rows:
        tds = ""
        for ci, cell in enumerate(r):
            if isinstance(cell, tuple):
                txt, tone = cell[0], cell[1]
            else:
                txt, tone = cell, None
            cls = f' class="t-{tone}"' if tone else ""
            first = ' class="lead"' if ci == 0 and not tone else (f' class="lead t-{tone}"' if ci==0 else cls)
            tds += f"<td{first if ci==0 else cls}>{txt}</td>"
        trs += f"<tr>{tds}</tr>"
    sc = " small" if small else ""
    return f'<table class="tbl{sc}"><colgroup>{cg}</colgroup><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'

def numbered(items, note=None):
    """items: (n, title, desc, color)"""
    rows = ""
    for n, t, d, c in items:
        rows += (f'<div class="num-row"><div class="num-badge fill-{c}">{n}</div>'
                 f'<div class="num-card"><div class="num-t t-{c}">{t}</div>'
                 f'<div class="num-d">{d}</div></div></div>')
    n2 = f'<div class="strip"><span class="t-teal">{note}</span></div>' if note else ""
    return f'<div class="numbered">{rows}</div>{n2}'

def steps(items, strip=None):
    """items: (label, desc, color)"""
    rows = ""
    for lab, d, c in items:
        rows += (f'<div class="step-row"><div class="step-lab fill-{c}">{lab}</div>'
                 f'<div class="step-card">{d}</div></div>')
    st = f'<div class="strip navy"><span>{strip}</span></div>' if strip else ""
    return f'<div class="steps">{rows}</div>{st}'

def flow(nodes):
    cells = ""
    for i, n in enumerate(nodes):
        cells += f'<div class="flow-node">{"<br>".join(n.split("|"))}</div>'
        if i < len(nodes)-1:
            cells += '<div class="flow-arw">▶</div>'
    return f'<div class="flow">{cells}</div>'

def twocards(cards):
    """cards: (title, color, [lines])"""
    out = ""
    for t, c, lines in cards:
        body = "".join(f"<li>{ln}</li>" for ln in lines)
        out += f'<div class="bigcard"><div class="bc-head fill-{c}">{t}</div><ul class="bc-list">{body}</ul></div>'
    return f'<div class="two">{out}</div>'

def threecards(cards):
    out = ""
    for t, c, lines in cards:
        body = "".join(f"<li>{ln}</li>" for ln in lines)
        out += f'<div class="minicard"><div class="mc-head fill-{c}">{t}</div><ul class="mc-list">{body}</ul></div>'
    return f'<div class="three">{out}</div>'

def split(left, right, ratio="1.25fr 1fr"):
    return f'<div class="split" style="grid-template-columns:{ratio}">{left}<div class="col-r">{right}</div></div>'

# ---------------------------------------------------------------- slide shell
TAG_KIND = {  # tag -> fill class
    "배경":"teal","감별":"teal","진단":"teal","철분 평가":"teald","핵심 기전":"teal","기전":"teal",
    "위험요인":"teal","요약":"navy","개관":"navy","효과 있음":"green","기법":"teald","연구 단계":"amber",
    "표현형 한정":"amber","약제":"navy","1차":"green","후순위":"red","조건부":"amber","난치성":"navy2",
    "근거 없음":"red","정리":"navy","References":"navy2",
}

def slide(eyebrow, title, tag, body, src, kind="std"):
    tagfill = TAG_KIND.get(tag, "teal")
    taghtml = f'<div class="tag fill-{tagfill}">{tag}</div>' if tag else ""
    n = len(slides)+1
    head = (f'<header class="s-head"><div class="s-eyebrow">{eyebrow}</div>'
            f'<h2 class="s-title">{title}</h2>{taghtml}</header>')
    foot = (f'<footer class="s-foot"><span class="src">근거: {src}</span>'
            f'<span class="pg">{n:02d}</span></footer>')
    slides.append(f'<section class="slide {kind}" data-i="{len(slides)}">{head}'
                  f'<div class="s-body">{body}</div>{foot}</section>')

def title_slide(inner):
    slides.append(f'<section class="slide title" data-i="{len(slides)}">{inner}</section>')

def key_slide(inner):
    slides.append(f'<section class="slide key" data-i="{len(slides)}">{inner}</section>')

# ================================================================ SLIDE 1 — TITLE
title_slide('''
<div class="ttl-hero">
  <div class="ttl-eyebrow">하지불안증후군 · Willis–Ekbom Disease</div>
  <h1 class="ttl-h1">철분 교정을 기반으로 한<br>근거 기반 치료 정리</h1>
  <div class="ttl-sub">Restless Legs Syndrome — Evidence-based Iron · Injection · Pharmacotherapy (AASM 2025)</div>
</div>
<div class="ttl-foot">
  <div class="ttl-scope">구성: 진단·감별 → 병태생리 → 치료(철분 · 주사 · 경구약제 · ESWT) → 알고리즘</div>
  <div class="ttl-note">직접 근거와 인접 근거를 구분해 정리 · 근거 없는 항목은 ‘없음’으로 정직하게 명시</div>
  <div class="ttl-disc">교육·연구 참고용 문헌고찰. 개별 환자의 진단·처방 결정은 담당 의사(신경과/수면의학 등)의 판단에 따릅니다.&nbsp;&nbsp;|&nbsp;&nbsp;작성 2026-07</div>
</div>''')

# ================================================================ SLIDE 2 — RLS란
slide("배경 · 임상 문제", "하지불안증후군(RLS)이란 무엇인가", "배경",
    split(
        bullets([
            (0,"정의: 다리를 ‘움직이고 싶은 충동’을 핵심으로 하는 감각-운동 신경질환. 대개 불쾌한 다리 이상감각을 동반한다.","ink",True),
            (0,"특징: 통증보다 ‘불편·안절부절·벌레가 기어가는 느낌’ 등 이상감각이 주. 만져지는 근경직은 없다.","ink"),
            (0,"유병률: 성인 약 5~10%(여성·고령에서 증가). 수면개시·유지 장애로 삶의 질을 크게 떨어뜨린다.","ink"),
            (0,"동반: 수면 중 주기성 사지운동(PLMS)이 흔히 동반된다.","ink"),
            (-1,"→ 관리의 성패는 정확한 진단(IRLSSG 5기준)과 철분 상태 평가에서 시작된다.","teal",True),
        ]),
        statcard("핵심 수치", [("5–10%","성인 유병률"),("여성·고령","유병 위험 증가군"),
                              ("5가지","IRLSSG 필수 진단기준"),("저녁·밤","증상 악화(일주기)")]),
    ),
    "Allen 2014(Sleep Med, IRLSSG); AASM 2025(J Clin Sleep Med)")

# ================================================================ SLIDE 3 — 3갈래
slide("진단 · 감별", "왜 감별이 먼저인가 — 세 갈래 병태", "감별",
    compare3([
        ("하지불안증후군(RLS)", ["‘움직이고 싶은 충동’","안정 시 악화·움직이면 완화","통증보다 불쾌한 이상감각","저녁~밤 뚜렷한 일주기"], "navy2"),
        ("야간 하지경련(NLC)", ["수면 중 통증성 근수축","만져지는 근경직(+)","족배굴곡으로 완화","종아리·발이 대부분"], "teal"),
        ("이차성 · mimic", ["철결핍·말기신부전·임신","말초신경병증·정맥울혈","약물유발(항히스타민 등)","‘다리 불편’으로 위장"], "teald"),
    ], note="<b>임상 단서:</b> RLS는 ‘움직이면 완화’가 결정적이며 근경직이 없다. IRLSSG 2014 기준은 진단 시 NLC 등 mimic를 반드시 감별·배제하도록 명문화한다. 도파민제·pregabalin에 반응하면 RLS를 강하게 시사."),
    "Allen 2014(Sleep Med, IRLSSG); 02_RLS 문헌고찰 서론")

# ================================================================ SLIDE 4 — RLS vs NLC 표
slide("진단 · 감별", "RLS vs NLC 상세 감별표", "감별",
    table(["항목","하지불안증후군(RLS)","야간 하지경련(NLC)"], [
        ["핵심 증상","움직이고 싶은 충동 + 이상감각","통증성 근수축, 만져지는 근경직"],
        ["주 증상","불편·안절부절(통증 아님)","강한 통증"],
        ["완화 방법","걷기·움직임(멈추면 재발)","스트레칭·족배굴곡"],
        ["만져지는 근경직",("없음","teal"),("있음","navy")],
        ["일주기·가족력","저녁~밤 악화 / 가족력 흔함","야간·수면 초반 / 가족력 드묾"],
        ["1차 치료",("철분 교정 + α2δ 리간드","teal"),"비약물·원인교정 · 개별 약물"],
    ], widths=[22,40,38]),
    "Allen 2014(IRLSSG); AASM 2025(J Clin Sleep Med); 문헌고찰 감별")

# ================================================================ SLIDE 5 — IRLSSG 5기준
slide("진단 · 기준", "진단 — IRLSSG 2014 필수 5기준", "진단",
    numbered([
        ("1","움직이고 싶은 충동","다리를 움직이고 싶은 강한 충동, 대개 불쾌한 다리 감각을 동반한다.","navy"),
        ("2","안정·비활동 시 악화","앉거나 누워 쉴 때 증상이 시작되거나 악화된다.","navy2"),
        ("3","움직이면 완화","걷기·스트레칭 등 움직임으로 부분적·일시적으로 완화된다(움직이는 동안 지속).","teal"),
        ("4","저녁·밤 악화(일주기)","저녁·밤에 뚜렷하게 악화되는 circadian 패턴을 보인다.","teald"),
        ("5","mimic 배제","다리경련·자세성 불편·근육통·정맥울혈 등 다른 질환으로 더 잘 설명되지 않는다.","green"),
    ], note="요점: 5가지를 모두 충족해야 진단. 통증보다 이상감각이 주이며 촉지되는 근경직은 없다."),
    "Allen RP, et al. IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73.")

# ================================================================ SLIDE 6 — 워크업
slide("진단 · workup", "진단 확정 후 — 철분 평가와 악화요인 검토", "철분 평가",
    steps([
        ("혈청 철분","ferritin · TSAT(트랜스페린포화도) 측정 — 모든 RLS 치료의 출발점이자 기반.","navy"),
        ("철분 판정","ferritin ≤75 → 경구 철분 고려 / ferritin ≤100(또는 경구 부적절) → 정맥 철분.","navy2"),
        ("악화요인","철결핍·임신·말기신부전 및 악화 약물(항히스타민·항우울제·도파민 차단제) 확인·조정.","teal"),
        ("동반평가","수면장애·PLMS·복용약 평가로 이차성 RLS를 감별한다.","teald"),
    ], strip="요점: 진단은 IRLSSG 5기준(임상)으로 내리고, 검사(ferritin/TSAT)는 치료 방향(철분 보충)을 정하기 위한 것."),
    "Allen 2018(IRLSSG iron task force); AASM 2025")

# ================================================================ SLIDE 7 — 병태 ① 철분
slide("병태생리 · 기전", "병태생리 ① 뇌 철분 결핍 — 핵심", "핵심 기전",
    split(
        bullets([
            (0,"혈청 철분이 정상이어도 흑질·기저핵 등 뇌 국소 철분이 부족하여 도파민 신호 이상을 초래한다.","ink",True),
            (0,"이것이 ‘철분 보충’이라는 치료의 생물학적 근거 — RLS는 전신 빈혈이 아니라 뇌 국소 철분 문제일 수 있다.","ink"),
            (0,"철결핍이 동반되면 증상이 악화되고, 철분 교정으로 호전되는 경우가 많다.","ink"),
            (0,"뇌 철분 결핍은 이어서 도파민·아데노신 신호 이상으로 연결된다(다음 장).","ink"),
            (-1,"→ 그래서 치료의 기반은 언제나 ferritin/TSAT 평가와 철분 교정이다.","teal",True),
        ]),
        whycard("왜 철분인가 (기전)", [
            ("혈청 ferritin이 정상이어도 뇌 국소(흑질) 철분은 부족할 수 있다.",),
            ("철분은 도파민 합성 효소(tyrosine hydroxylase)의 보조인자다.",),
            ("뇌 철분 부족 → 도파민 신호 이상 → 야간 감각-운동 증상.",),
            ("→ 철분 교정이 이 상류(上流) 병태를 직접 겨냥한다.", True),
        ]),
    ),
    "IRLSSG; Allen 2018(Sleep Med); 문헌고찰 Part 1-1")

# ================================================================ SLIDE 8 — 병태 ② 도파민·아데노신
slide("병태생리 · 기전", "병태생리 ② 도파민 · 아데노신 가설", "기전",
    '<div class="flow-wrap"><div class="flow-cap">뇌 철분 결핍이 하류(下流)의 신경전달 이상으로 이어진다</div>' +
    flow(["뇌 국소|철분 결핍","도파민 신호 이상|아데노신 신호 ↓","글루타메이트·도파민|과흥분","야간 감각-운동|증상 · PLMS"]) +
    '</div>' +
    '<div class="two">' +
    sidecard("도파민 이상", [
        (0,"야간 도파민 기능 저하 가설.","ink"),
        (0,"도파민제는 단기 효과가 뚜렷하다.","ink"),
        (0,"그러나 장기 사용 시 augmentation(증상 악화·전이)을 유발 → 후순위.","red"),
    ], title_tone="teald") +
    sidecard("아데노신 저하 가설(최근)", [
        (0,"뇌 철분 결핍이 아데노신 신호를 낮춘다.","ink"),
        (0,"→ 글루타메이트·도파민 과흥분을 유발한다는 가설.","ink"),
        (0,"dipyridamole 등 새로운 표적 치료의 이론적 근거.","green"),
    ], title_tone="teald") +
    '</div>',
    "IRLSSG; Garcia-Borreguero 2021(아데노신 가설); 문헌고찰 Part 1-2·1-3")

# ================================================================ SLIDE 9 — 병태 ③ 유전·이차·약물
slide("병태생리 · 위험요인", "병태생리 ③ 유전 · 이차 요인 · 악화 약물", "위험요인",
    split(
        bullets([
            (0,"가족력이 흔하다(상염색체 우성 경향) — 조기 발병일수록 유전 기여가 크다.","ink",True),
            (0,"이차성 RLS는 원인 교정으로 호전될 수 있어 반드시 선별한다.","ink"),
        ]) +
        table(["범주","대표 요인"], [
            ["철 대사","철결핍(기반 병태) — ferritin/TSAT 확인·교정"],
            ["생리·전신","임신, 말기신부전(투석), 갑상선 이상"],
            ["악화 약물","항히스타민, 항우울제, 도파민 차단제(항구토·항정신병)"],
            ["생활요인","카페인·알코올·수면부족 — 악화 유발 가능"],
        ], widths=[24,76], small=True),
        whycard("실무 포인트", [
            ("이차 요인·악화 약물을 먼저 교정하면 약물 없이도 호전될 수 있다.", True),
            ("항우울제가 꼭 필요하면 RLS 악화가 적은 약제를 고려.",),
            ("임신·신부전 동반 RLS는 안전한 치료(철분 등)를 우선.",),
            ("→ ‘원인 교정’이 약물치료보다 앞선다.", True),
        ]),
        ratio="1.35fr 1fr"),
    "IRLSSG; 문헌고찰 Part 1-4")

# ================================================================ SLIDE 10 — 근거 한눈에
slide("총괄", "치료 근거 한눈에 — 무엇이 되고 무엇이 안 되나", "요약",
    table(["치료","RLS 직접 근거","근거·권고","위치"], [
        ["철분 교정(경구/정맥)","Earley 2024 RCT · IRLSSG 2018",("강한 권고","green"),"기반 · 필수"],
        ["α2δ 리간드","Allen 2014 등 RCT",("강한 권고(1차)","green"),"1차 약물"],
        ["IV 철분(FCM)","Earley 2024 RCT · 메타분석",("강한 권고","green"),"철결핍 시"],
        ["dipyridamole","Garcia-Borreguero 2021 교차RCT",("조건부","amber"),"신규 · 아데노신"],
        ["비골신경 자극(TOMAC)","Charlesworth 2023 sham 대조",("조건부","amber"),"비약물 대안"],
        ["도파민 작용제","Winkelman 2006 RCT",("장기 권고 안 함","red"),"augmentation로 후순위"],
        ["보툴리눔독소","Mittal 2018 교차RCT(소규모)",("근거 약함","amber"),"연구 단계"],
        ["체외충격파(ESWT)",("없음","red"),("—","muted"),("RLS 근거 없음","red")],
    ], widths=[26,32,20,22], small=True),
    "AASM 2025 지침 종합 · 02_RLS 문헌고찰 근거표")

# ================================================================ SLIDE 11 — 3축 개관
slide("총괄 · 지형", "치료 3축 개관 — 기반 · 1차 · 보조", "개관",
    compare3([
        ("기반 · 철분 교정", ["뇌 철분 결핍을 직접 교정","경구(ferritin≤75)/정맥(≤100)","Earley 2024 RCT · IRLSSG 2018","AASM 2025 강한 권고"], "teal"),
        ("1차 · 경구약제", ["α2δ 리간드 = 1차(강한 권고)","도파민제는 augmentation로 후순위","dipyridamole 조건부(신규)","오피오이드는 난치성에 조건부"], "navy2"),
        ("보조 · 주사/비약물", ["IV 철분 = 주사 중 근거 최강","보툴리눔 연구단계 · 정맥경화 표현형","비골신경 자극(TOMAC) 조건부","ESWT는 RLS 근거 없음"], "teald"),
    ], note="<b>2024/2025 AASM 지침의 핵심 변화:</b> 1차 약물을 도파민제에서 α2δ 리간드로 전환 — augmentation 위험 때문.", note_tone="ink"),
    "Winkelman 2025(AASM); 문헌고찰 치료 3축")

# ================================================================ SLIDE 12 — 철분 교정
slide("치료 · 기반", "기반 치료: 철분 교정 — 경구와 정맥의 분기", "효과 있음",
    twocards([
        ("경구 철분","teal", ["적응: ferritin ≤75(흡수 여지가 있을 때)","ferrous sulfate + 비타민 C(흡수↑)",
            "격일 투여가 흡수·내약성에 유리할 수 있음","한계: ferritin ≥75에서는 흡수가 미미","부작용: 위장장애·변비"]),
        ("정맥 철분 (FCM)","navy2", ["적응: ferritin ≤100 또는 경구 부적절/불내","FCM 1000 mg 단회(또는 750 mg×2)",
            "1시간 이내 점적","중등도~중증에 FCM 1000 mg은 Level A","안전: 일과성 저인산혈증 모니터링"]),
    ]) +
    '<div class="strip"><span><b class="t-teal">원칙:</b> 철분 교정은 약물치료의 대안이 아니라 ‘기반’이다. 경구로 목표에 못 미치거나 흡수가 부족하면 정맥으로 전환한다.</span></div>',
    "Allen 2018(IRLSSG iron); Earley 2024(Sleep); AASM 2025")

# ================================================================ SLIDE 13 — IV 철분 근거
slide("치료 · 주사", "주사 ① 정맥 철분(IV FCM) — 근거 최강", "효과 있음",
    split(
        bullets([
            (0,"뇌 철분 결핍이라는 핵심 병태를 직접 교정하는, RLS 주사 치료 중 근거가 가장 확실하다.","ink",True),
            (0,"Earley 2024(Sleep) 다기관 RCT: IRLS ≥15인 209명, FCM 750 mg(0일·5일 2회) vs 위약.","ink"),
            (1,"42일째 IRLS·CGI가 위약 대비 유의하게 개선.","green",True),
            (0,"메타분석 2024(537명)도 효과·안전성을 확인.","ink"),
            (0,"경구 철분은 ferritin ≥75에서 흡수가 미미 → 정맥 투여가 유리한 경우가 많다.","ink"),
            (-1,"→ 철결핍(또는 경구 부적절) 동반 RLS에서 AASM 2025 강한 권고.","teal",True),
        ]),
        statcard("Earley 2024 (RCT 핵심)", [("n=209","다기관 RCT"),("FCM 750mg","0일·5일 2회 정맥"),
                              ("42일","IRLS·CGI 유의 개선"),("537명","메타분석 효과·안전 확인")], tone="navy"),
    ),
    "Earley CJ, et al. Sleep. 2024;47(7):zsae095. PMID 38625730; 메타분석 2024")

# ================================================================ SLIDE 14 — IV 철분 용량·안전
slide("치료 · 주사 · 기법", "정맥 철분 — 용량 · 적응 · 안전", "기법",
    split(
        table(["항목","권고 요지"], [
            ["대표 약제","Ferric carboxymaltose (FCM)"],
            ["용량","FCM 1000 mg 단회 (또는 750 mg×2)"],
            ["투여","정맥 점적 · 1시간 이내"],
            ["적응(IRLSSG 2018)","정맥: ferritin ≤100 또는 경구 부적절 / 경구: ferritin ≤75"],
            ["근거수준",("중등도~중증 FCM 1000 mg = Level A","green")],
            ["권고",("AASM 2025 강한 권고","green")],
        ], widths=[26,74], small=True),
        sidecard("안전 · 주의", [
            (0,"일과성 저인산혈증 — 반복·고용량 시 모니터링.","red"),
            (0,"드물게 주입반응·과민반응 — 투여 중 관찰.","ink"),
            (0,"활동성 감염 시 정맥 철분은 신중.","ink"),
            (0,"경구 실패·불내·흡수부족에서 특히 유용.","green"),
            (-1,"→ 철분 상태(ferritin/TSAT) 재평가로 반복 여부 결정.","teal",True),
        ], title_tone="red"),
        ratio="1.3fr 1fr"),
    "Allen 2018(IRLSSG iron task force, Sleep Med); Earley 2024")

# ================================================================ SLIDE 15 — 보툴리눔
slide("치료 · 주사", "주사 ② 보툴리눔독소(BoNT-A) — 근거 약함·혼재", "연구 단계",
    split(
        bullets([
            (0,"Mittal 2018(Toxins) 이중맹검 교차(n=24): incobotulinumtoxinA 100단위를 전경골근·비복근·대퇴이두근에 주사.","ink",True),
            (1,"4·6주에 IRLS 점수·통증(VAS)이 유의하게 개선.","green"),
            (0,"SR/MA(Healthcare 2021): RCT 2편·27명, IRLS SMD −0.819.","ink"),
            (1,"표본이 매우 작아 확정 불가 → 대규모 RCT 필요.","muted",True),
            (-1,"위치: 표준치료가 아니다. 특정 표현형·연구단계 옵션으로 본다.","teal",True),
        ]),
        sidecard("요점", [
            (0,"표적: 전경골근·비복근·대퇴이두근.","ink"),
            (0,"용량: incoA 100U(Mittal 프로토콜).","ink"),
            (0,"근거: RCT 2편·소표본(Level 낮음).","ink"),
            (0,"기전은 국소적이며 RLS 중추 병태를 겨냥하지 않음.","muted"),
            (-1,"→ 근거 확립 전까지 표준치료 아님.","teal",True),
        ]),
    ),
    "Mittal 2018(Toxins 10(10):401); SR/MA Healthcare 2021;9(11):1538")

# ================================================================ SLIDE 16 — 정맥 경화
slide("치료 · 주사", "주사 ③ 정맥 경화요법 — 정맥질환 동반 표현형", "표현형 한정",
    split(
        bullets([
            (0,"정맥류·만성정맥부전(CVI)이 동반된 RLS 표현형을 표적으로 하는 접근.","ink",True),
            (0,"Pyne 2023(JVIR)·Sundaresan 2019(Cureus): 하지정맥 치료 후 IRLS 점수 개선.","ink"),
            (1,"IRLS 19.83 → 7.89 (약 63% 호전).","green",True),
            (0,"기전: 정맥울혈·측부 자극이라는 말초 유발요인을 제거한다는 해석.","ink"),
            (-1,"위치: 정맥질환이 확인된 특정 표현형에서 의미. 특발성 RLS 전반의 표준은 아니다.","teal",True),
        ]),
        whycard("핵심 수치", [
            ('<span class="wc-lab">IRLS 점수 변화</span>',),
            ('<span class="wc-big">19.83 → 7.89</span>',),
            ("약 63% 호전", True),
            ("적응: 정맥류·CVI가 확인된 RLS.",),
            ("→ 원인(정맥질환) 표적치료로서 의미.", True),
        ]),
    ),
    "Pyne 2023(JVIR 34(4):534-42); Sundaresan 2019(Cureus 11(4):e4368)")

# ================================================================ SLIDE 17 — 경구 개관
slide("치료 · 경구약제", "경구약제 개관 — 1차 패러다임의 전환", "약제",
    split(
        bullets([
            (0,"2024/2025 AASM 지침의 핵심: 1차 약물을 도파민제에서 α2δ 리간드로 전환.","ink",True),
            (0,"이유: 도파민제의 장기 augmentation(연 7~10%) 위험이 α2δ 리간드보다 크다.","ink"),
            (0,"철분 교정을 기반으로 하고, 그 위에 경구약제를 얹는다.","ink"),
            (0,"고령·신기능 저하: 낙상·진정·부종을 고려해 저용량에서 서서히 적정.","ink"),
        ]),
        '<div class="legend"><div class="lg-title t-teald">약물군 · 권고 요지</div>' +
        "".join(f'<div class="lg-row"><span class="lg-dot d-{c}"></span><b>{a}</b><span class="lg-note">{b}</span></div>'
                for a,b,c in [("α2δ 리간드","1차 · 강한 권고","green"),("철분(경구)","기반 · 필수","green"),
                              ("dipyridamole","조건부 · 신규","amber"),("오피오이드(서방형)","난치성 · 조건부","amber"),
                              ("도파민 작용제","장기 권고 안 함","red")]) + '</div>',
    ),
    "Winkelman 2025(AASM, J Clin Sleep Med); 문헌고찰 Part 5")

# ================================================================ SLIDE 18 — α2δ 1차
slide("치료 · 경구약제", "경구약제 ① α2δ 리간드 — 1차", "1차",
    split(
        bullets([
            (0,"gabapentin enacarbil · gabapentin · pregabalin. AASM 2025 1차 강한 권고.","ink",True),
            (0,"Allen 2014(NEJM) 52주 RCT: pregabalin 300 mg이 효과적이며,","ink"),
            (1,"augmentation 1.7% vs pramipexole 0.5 mg 9.0%로 유의하게 낮음.","green",True),
            (0,"Gabapentin enacarbil: Winkelman 2011(PSG) 각성·PLM 감소, Bogan 2010 장기 유지.","ink"),
            (0,"부작용: 어지럼·졸림·부종·체중증가. 고령·신기능 저하 시 감량.","ink"),
        ]),
        whycard("왜 1차인가", [
            ("도파민제보다 augmentation이 유의하게 적다(1.7% vs 9.0%).",),
            ("수면과 감각증상을 함께 개선한다.",),
            ("철분 교정과 병행하는 것이 기반이다.",),
            ("→ 장기 관리에 유리한 프로파일.", True),
        ]),
    ),
    "Allen 2014(NEJM 370(7):621-31); Winkelman 2011(Mov Disord); AASM 2025")

# ================================================================ SLIDE 19 — α2δ 상세
slide("치료 · 경구약제 · 기법", "α2δ 리간드 — 약물 · 특징 · 주의", "기법",
    table(["약물","특징 · 근거"], [
        ["Gabapentin enacarbil","전구약물로 흡수 안정적. PSG상 각성·PLM 감소(Winkelman 2011), 장기 유지(Bogan 2010)"],
        ["Pregabalin",("Allen 2014 NEJM 52주: 300 mg 효과적, augmentation 1.7%","green")],
        ["Gabapentin","저비용·범용. 흡수 변동 있어 분할·적정 필요"],
        ["공통 부작용","어지럼 · 졸림 · 말초부종 · 체중증가"],
        ["고령·신기능",("용량 감량 · 저용량에서 서서히 적정 · 낙상 주의","red")],
    ], widths=[26,74]) +
    '<div class="strip"><span class="t-teal">소결: α2δ 리간드는 augmentation 위험이 낮고 수면·감각증상을 함께 개선 → 철분 교정 위의 1차 약물.</span></div>',
    "Allen 2014(NEJM); Winkelman 2011(Mov Disord); Bogan 2010(Mayo Clin Proc)")

# ================================================================ SLIDE 20 — 도파민제
slide("치료 · 경구약제", "경구약제 ② 도파민 작용제 — augmentation 위험", "후순위",
    split(
        bullets([
            (0,"pramipexole · ropinirole · rotigotine. 단기 효능은 확립되어 있다.","ink",True),
            (0,"Winkelman 2006(Neurology): pramipexole 12주 IRLS·CGI 개선.","ink"),
            (0,"그러나 수개월~수년 후 augmentation(증상 악화·전이, 연 7~10%)이 문제.","red",True),
            (0,"AASM 2025는 도파민제의 장기 표준 사용을 ‘권고하지 않음(against)’.","red"),
            (-1,"복용 중이면 정기 점검 · 철분 재평가 · α2δ 리간드로 단계적 전환을 고려.","teal",True),
        ]),
        whycard("⚠ Augmentation", [
            ("증상이 더 이르게·더 넓은 부위로 악화.",),
            ("도파민제 용량을 올릴수록 악화되는 악순환.",),
            ("연 7~10%에서 발생.",),
            ("→ 장기 1차로 권고되지 않음.", True),
        ], tone="red"),
    ),
    "Winkelman 2006(Neurology 67(6):1034-9); Allen 2014(NEJM); AASM 2025")

# ================================================================ SLIDE 21 — dipyridamole
slide("치료 · 경구약제", "경구약제 ③ Dipyridamole — 신규·아데노신", "조건부",
    split(
        bullets([
            (0,"아데노신 저하 가설에 기반한 새로운 표적 — 아데노신 재흡수를 억제한다.","ink",True),
            (0,"Garcia-Borreguero 2021(Mov Disord) 교차 RCT.","ink"),
            (1,"IRLS 24.1 → 11.1 (위약군 18.7)로 유의한 개선.","green",True),
            (0,"도파민 경로가 아니므로 augmentation 우려가 상대적으로 적다는 이론적 장점.","ink"),
            (-1,"위치: 조건부(신규). 표본·추적이 제한적이라 추가 근거가 필요.","teal",True),
        ]),
        whycard("Garcia-Borreguero 2021", [
            ('<span class="wc-lab">IRLS (약물군)</span>',),
            ('<span class="wc-big">24.1 → 11.1</span>',),
            ("위약군 18.7", True),
            ("설계: 위약대조 교차 RCT.",),
            ("→ 도파민 비의존 표적의 첫 근거.", True),
        ]),
    ),
    "Garcia-Borreguero D, et al. Mov Disord. 2021;36(10):2387-92. PMID 34137476")

# ================================================================ SLIDE 22 — 오피오이드
slide("치료 · 경구약제", "경구약제 ④ 오피오이드 — 난치성·조건부", "난치성",
    bullets([
        (0,"저용량 서방형 oxycodone 등 μ-오피오이드는 난치성 RLS 및 도파민제 augmentation 상황에서 조건부로 사용된다.","ink",True),
        (0,"부프레노르핀은 상대적으로 위험이 낮은 선택지로 거론된다. 다만 진정·호흡 억제 위험으로 신중한 적응·감시가 필요하다.","ink"),
    ]) +
    threecards([
        ("적응 (조건부)","teald", ["α2δ 리간드·철분 교정에 불응","도파민제 augmentation 발생·전환기","중증·삶의 질 저하가 뚜렷한 경우"]),
        ("약물 · 원칙","navy2", ["저용량 서방형 oxycodone/μ-오피오이드","부프레노르핀은 상대적 저위험","최소 유효용량 · 정기 재평가"]),
        ("주의 · 안전","red", ["진정 · 호흡 억제 · 변비","의존·오남용 위험 평가 필수","고령·수면무호흡 동반 시 특히 신중"]),
    ]),
    "AASM 2025(J Clin Sleep Med); 문헌고찰 Part 5-5")

# ================================================================ SLIDE 23 — ESWT
slide("치료 · ESWT", "체외충격파(ESWT) — RLS 직접 근거 없음", "근거 없음",
    split(
        bullets([
            (0,"RLS를 결과변수로 ESWT를 평가한 RCT·전향연구·증례는 검색되지 않는다(2026-07 기준).","red",True),
            (0,"ESWT의 확립된 근거는 근골격계 통증·경직 영역으로, RLS(뇌 철분·도파민·아데노신)와 병태가 다르다.","ink"),
            (0,"미세순환·NO·운동신경원 조절이 이론상 거론되나 RLS 핵심 병태와 직접 연결하는 근거는 없다.","ink"),
            (-1,"근거를 창작하지 않는다 → RLS에 ESWT는 권고할 수 없다.","teal",True),
        ]),
        whycard("근거 있는 대안", [
            ("비약물이 필요하면 충격파가 아니라 ‘말초 비골신경 자극’.",),
            ("Charlesworth 2023: sham 대조에서 증상 개선·수면 무방해.",),
            ("AASM 2025 조건부 권고.",),
            ("→ 다음 장에서 상술.", True),
        ]),
    ),
    "문헌고찰 Part 3(직접 근거 부재); Charlesworth 2023(대안)")

# ================================================================ SLIDE 24 — 비골신경 자극
slide("비약물 · 기기", "근거 있는 비약물 — 말초 비골신경 자극(TOMAC)", "조건부",
    split(
        bullets([
            (0,"Charlesworth 2023(J Clin Sleep Med): 양측 고빈도 비침습적 비골신경 자극(NPNS/TOMAC).","ink",True),
            (0,"중등도~중증 RLS에서 sham(가짜자극) 대조로 평가.","ink"),
            (1,"다리 근육의 긴장성 활성을 유발하여, 수면을 방해하지 않고 증상을 개선.","green",True),
            (0,"약물 부작용(augmentation·진정)이 없는 비약물 옵션.","ink"),
            (-1,"AASM 2025 조건부 권고 → 비약물이 필요할 때의 우선 고려 대상.","teal",True),
        ]),
        sidecard("요점", [
            (0,"방식: 양측 비골신경 고빈도 자극.","ink"),
            (0,"대상: 중등도~중증 RLS.","ink"),
            (0,"근거: sham 대조 시험(Charlesworth 2023).","ink"),
            (0,"장점: 수면 무방해 · 전신 부작용 없음.","green"),
            (-1,"→ ESWT의 자리를 대신하는 비약물 대안.","teal",True),
        ]),
    ),
    "Charlesworth JD, et al. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064")

# ================================================================ SLIDE 25 — 알고리즘
slide("종합", "종합 치료 알고리즘 / 사다리", "정리",
    numbered([
        ("1","진단 확정 (IRLSSG 5기준)","움직임 충동·안정 시 악화·움직이면 완화·저녁 악화·mimic 배제. NLC 등 감별.","navy"),
        ("2","철분 평가·교정 (기반)","ferritin/TSAT. 경구(≤75)/정맥(≤100 또는 경구 부적절, FCM 1000 mg). 악화약물 조정.","navy2"),
        ("3","1차 약물 — α2δ 리간드","gabapentin enacarbil·gabapentin·pregabalin. 수면·감각 개선, augmentation 적음.","teal"),
        ("4","도파민제는 후순위","단기 효과 O이나 augmentation(연 7~10%)로 장기 권고 안 함. 복용 중이면 전환 고려.","teald"),
        ("5","난치성 옵션 (선택)","dipyridamole(조건부)·오피오이드(서방형)·비골신경 자극(TOMAC). ESWT는 RLS 근거 없음.","green"),
    ]),
    "AASM 2025 지침 · 문헌고찰 종합 결론(치료 사다리)")

# ================================================================ SLIDE 26 — 근거 요약표
slide("종합 · 근거표", "근거 요약표 — RLS 치료", "요약",
    table(["영역","대표 문헌","설계","핵심 결과"], [
        ["IV 철분","Earley 2024","다기관 RCT n=209","42일 IRLS·CGI 개선"],
        ["IV 철분","메타분석 2024","SR/MA 537명","효과·안전 확인"],
        ["α2δ 리간드","Allen 2014","RCT n=719",("augmentation 1.7% vs 9.0%","green")],
        ["도파민제","Winkelman 2006","RCT n=344","단기 IRLS 개선(장기 augmentation)"],
        ["dipyridamole","Garcia-Borreguero 2021","교차 RCT","IRLS 24.1 → 11.1"],
        ["보툴리눔","Mittal 2018","교차 RCT n=24","4·6주 IRLS·VAS 개선(소표본)"],
        ["비골신경 자극","Charlesworth 2023","sham 대조","증상 개선·수면 무방해"],
        ["ESWT",("—","muted"),("RLS 표적 연구 없음","muted"),("직접 근거 없음","red")],
    ], widths=[20,26,26,28], small=True),
    "02_RLS 참고문헌 근거 요약표 · PubMed 대조")

# ================================================================ SLIDE 27 — 핵심 메시지
key_slide('''
<div class="key-eyebrow">핵심 메시지</div>
<h2 class="key-h">철분 교정이 기반, α2δ 리간드가 1차 — 도파민제는 후순위</h2>
<div class="key-list">''' + "".join(
    f'<div class="key-row"><div class="key-t">{t}</div><div class="key-d">{d}</div></div>'
    for t,d in [
        ("병태생리","뇌 국소 철분 결핍 → 도파민·아데노신 신호 이상. 유전·이차요인이 악화."),
        ("진단·감별","IRLSSG 5기준(움직임 충동·안정 시 악화·움직이면 완화·저녁 악화·mimic 배제). NLC와 감별."),
        ("기반·1차","철분 교정(경구≤75/정맥≤100)이 기반, α2δ 리간드가 1차 강한 권고."),
        ("주사·비약물","IV 철분(FCM)이 근거 최강. 보툴리눔·정맥경화는 표현형·연구단계. 비약물은 비골신경 자극."),
        ("주의","도파민제는 augmentation로 장기 후순위. ESWT는 RLS 근거 없음 — 근거를 창작하지 않는다."),
    ]) + '</div>')

# ================================================================ SLIDES 28-29 — 참고문헌
def refs_slide(title, refs):
    half = (len(refs)+1)//2
    cols = ""
    for chunk in (refs[:half], refs[half:]):
        cols += '<ol class="refcol">' + "".join(f"<li>{r}</li>" for r in chunk) + "</ol>"
    slide("참고문헌", title, "References",
          f'<div class="refs">{cols}</div>',
          "PubMed/PMC 대조 검증 — RLS 표적 ESWT 임상연구는 확인되지 않아 ‘직접 근거 없음’으로 명시")

refs_slide("참고문헌 (1/2) — 진단 · 병태 · 철분 · 주사", [
 "Allen RP, et al. RLS/WED diagnostic criteria: updated IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73. PMID 25023924.",
 "Winkelman JW, et al. Treatment of RLS/PLMD: AASM clinical practice guideline. J Clin Sleep Med. 2025;21(1):137-52. PMID 39324694.",
 "Allen RP, et al. IRLSSG task force: iron treatment of RLS/WED. Sleep Med. 2018;41:27-44. PMID 29425576.",
 "Earley CJ, et al. IV ferric carboxymaltose for RLS: multicenter RCT. Sleep. 2024;47(7):zsae095. PMID 38625730.",
 "IV ferric carboxymaltose in RLS: meta-analysis of 537 patients. Sleep Med. 2024. PMID 39326219.",
 "Mittal SO, et al. Botulinum toxin in RLS: double-blind placebo-controlled crossover study. Toxins (Basel). 2018;10(10):401. PMC6215171.",
 "Botulinum toxin type A in RLS: systematic review & meta-analysis. Healthcare (Basel). 2021;9(11):1538. PMC8623507.",
 "Pyne R, et al. Varicose veins with RLS and nocturnal leg cramps. J Vasc Interv Radiol. 2023;34(4):534-42. PMID 36526075.",
])
refs_slide("참고문헌 (2/2) — 비약물 · 경구약제 · 신규 표적", [
 "Sundaresan S, et al. Treatment of leg veins for restless leg syndrome: retrospective review. Cureus. 2019;11(4):e4368. PMID 31192073.",
 "Charlesworth JD, et al. Bilateral high-frequency noninvasive peroneal nerve stimulation for RLS. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064.",
 "Allen RP, et al. Comparison of pregabalin with pramipexole for RLS. N Engl J Med. 2014;370(7):621-31. PMID 24521108.",
 "Winkelman JW, et al. Efficacy and safety of pramipexole in RLS. Neurology. 2006;67(6):1034-9. PMID 16931507.",
 "Winkelman JW, et al. Randomized polysomnography study of gabapentin enacarbil in RLS. Mov Disord. 2011;26(11):2065-72. PMID 21611981.",
 "Bogan RK, et al. Long-term maintenance treatment of RLS with gabapentin enacarbil: RCT. Mayo Clin Proc. 2010;85(6):512-21. PMID 20511481.",
 "Garcia-Borreguero D, et al. Dipyridamole for RLS: placebo-controlled crossover study. Mov Disord. 2021;36(10):2387-92. PMID 34137476.",
])

# ================================================================ ASSEMBLE
CSS = r"""
:root{
  --bg:#e7edf3; --paper:#ffffff; --ink:#16202c; --muted:#5a6b7b;
  --line:#dbe3ec; --card:#f4f7fb; --card-line:#e2e9f1;
  --navy:#1b355e; --navy2:#24476e; --teal:#2c898a; --teald:#1f6e70;
  --sky:#bfd3e6; --mint:#9fe0d8;
  --c-teal:#1f6e70; --c-green:#2e7d32; --c-amber:#9a6a08; --c-red:#b03a2e; --c-navy:#1b355e; --c-navy2:#24476e; --c-muted:#5a6b7b;
  --shadow:0 10px 34px rgba(20,40,70,.16), 0 2px 8px rgba(20,40,70,.08);
  --fs:1.46cqw;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#070d14; --paper:#101b28; --ink:#e8eef4; --muted:#9db0c0;
    --line:#22303f; --card:#17232f; --card-line:#25333f;
    --c-teal:#54c2c2; --c-green:#79c47d; --c-amber:#e0aa46; --c-red:#ec8a80; --c-navy:#8fb3e0; --c-navy2:#7ea8d8; --c-muted:#9db0c0;
    --shadow:0 12px 40px rgba(0,0,0,.5), 0 2px 10px rgba(0,0,0,.4);
  }
}
:root[data-theme="light"]{
  --bg:#e7edf3; --paper:#ffffff; --ink:#16202c; --muted:#5a6b7b;
  --line:#dbe3ec; --card:#f4f7fb; --card-line:#e2e9f1;
  --c-teal:#1f6e70; --c-green:#2e7d32; --c-amber:#9a6a08; --c-red:#b03a2e; --c-navy:#1b355e; --c-navy2:#24476e; --c-muted:#5a6b7b;
  --shadow:0 10px 34px rgba(20,40,70,.16), 0 2px 8px rgba(20,40,70,.08);
}
:root[data-theme="dark"]{
  --bg:#070d14; --paper:#101b28; --ink:#e8eef4; --muted:#9db0c0;
  --line:#22303f; --card:#17232f; --card-line:#25333f;
  --c-teal:#54c2c2; --c-green:#79c47d; --c-amber:#e0aa46; --c-red:#ec8a80; --c-navy:#8fb3e0; --c-navy2:#7ea8d8; --c-muted:#9db0c0;
  --shadow:0 12px 40px rgba(0,0,0,.5), 0 2px 10px rgba(0,0,0,.4);
}
*{box-sizing:border-box}
#rls-deck{
  position:fixed; inset:0; background:
    radial-gradient(120% 90% at 50% -10%, color-mix(in srgb, var(--navy) 8%, var(--bg)), var(--bg));
  color:var(--ink); overflow:hidden;
  font-family:"Pretendard","Pretendard Variable",-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR","Segoe UI",Roboto,sans-serif;
  -webkit-font-smoothing:antialiased; text-rendering:optimizeLegibility;
  display:flex; align-items:center; justify-content:center;
}
.stage{ width:100%; height:100%; display:flex; align-items:center; justify-content:center; padding:2.2vh 1vw; }
.slide{
  position:relative; width:min(95vw, calc(90vh * 16/9)); aspect-ratio:16/9;
  background:var(--paper); border-radius:.7em; box-shadow:var(--shadow);
  container-type:inline-size; overflow:hidden; display:none;
  border:1px solid var(--card-line);
}
.slide.active{ display:block; }
.slide{ font-size:var(--fs); }
@container (min-width:0){ .slide{ line-height:1.5; } }

/* ---- header/footer ---- */
.s-head{ position:relative; padding:1.5em 2.4em .0em 2.4em; }
.s-eyebrow{ color:var(--c-teal); font-weight:800; font-size:.76em; letter-spacing:.02em; }
.s-title{ color:var(--c-navy); font-weight:800; font-size:1.72em; line-height:1.12; margin:.12em 0 0; text-wrap:balance; letter-spacing:-.01em; padding-right:6em; }
.s-head:after{ content:""; display:block; height:1px; background:var(--line); margin:.7em 0 0; }
.s-head:before{ content:""; position:absolute; left:1.55em; top:1.6em; width:.28em; height:1.5em; background:var(--teal); border-radius:2px; }
.tag{ position:absolute; top:1.75em; right:2.4em; color:#fff; font-weight:800; font-size:.72em; padding:.4em .9em; border-radius:2em; letter-spacing:.01em; }
.s-body{ padding:1.05em 2.4em 1em; height:calc(100% - 6.0em); position:relative; display:flex; flex-direction:column; justify-content:center; }
.s-foot{ position:absolute; left:2.4em; right:2.4em; bottom:.75em; display:flex; justify-content:space-between; align-items:center;
  color:var(--muted); font-size:.62em; border-top:1px solid var(--line); padding-top:.5em; }
.s-foot .src{ opacity:.92; } .s-foot .pg{ font-weight:800; font-variant-numeric:tabular-nums; letter-spacing:.05em; }

/* ---- fills ---- */
.fill-navy{background:var(--navy)} .fill-navy2{background:var(--navy2)} .fill-teal{background:var(--teal)}
.fill-teald{background:var(--teald)} .fill-green{background:#2e7d32} .fill-amber{background:#b97a0c} .fill-red{background:#b03a2e}
.t-ink{color:var(--ink)} .t-muted{color:var(--c-muted)} .t-teal{color:var(--c-teal)} .t-teald{color:var(--c-teal)}
.t-green{color:var(--c-green)} .t-amber{color:var(--c-amber)} .t-red{color:var(--c-red)} .t-navy{color:var(--c-navy)} .t-navy2{color:var(--c-navy2)}

/* ---- split ---- */
.split{ display:grid; gap:1.3em; align-items:stretch; width:100%; }
.split.one{grid-template-columns:1fr}
.col-r{ min-width:0; }

/* ---- bullets ---- */
ul.bl{ list-style:none; margin:0; padding:0; display:flex; flex-direction:column; gap:.62em; }
ul.bl li{ position:relative; padding-left:1.35em; font-size:.94em; line-height:1.44; }
ul.bl li.lv0:before{ content:"●"; position:absolute; left:0; top:.06em; color:var(--teal); font-size:.62em; line-height:1.6; }
ul.bl li.lv1{ padding-left:2.4em; font-size:.9em; }
ul.bl li.lv1:before{ content:"–"; position:absolute; left:1.35em; color:var(--c-muted); font-weight:800; }
ul.bl li.lvx{ padding-left:1.35em; }
ul.bl li.lvx:before{ content:"→"; position:absolute; left:0; color:var(--c-teal); font-weight:800; }
ul.bl li.lvx{ background:color-mix(in srgb,var(--teal) 9%, transparent); border-radius:.35em; padding:.5em .7em .5em 1.7em; }
ul.bl li.lvx:before{ left:.6em; top:.5em; }
ul.bl li.b span{ font-weight:700; }

/* ---- statcard ---- */
.statcard{ border-radius:.6em; padding:1.15em 1.25em; height:100%; }
.statcard.light{ background:var(--card); border:1px solid var(--card-line); }
.statcard.navy{ background:linear-gradient(160deg,var(--navy),#16294a); color:#fff; }
.statcard .st-title{ font-weight:800; font-size:.82em; margin-bottom:.55em; }
.statcard.light .st-title{ color:var(--c-teal); } .statcard.navy .st-title{ color:var(--sky); }
.st-row{ padding:.42em 0; border-top:1px solid color-mix(in srgb,var(--line) 80%, transparent); }
.statcard.navy .st-row{ border-top-color:rgba(255,255,255,.14); }
.st-row:first-of-type{ border-top:none; }
.st-num{ font-size:1.5em; font-weight:800; line-height:1.1; letter-spacing:-.01em; font-variant-numeric:tabular-nums; }
.statcard.light .st-num{ color:var(--navy); } .statcard.navy .st-num{ color:#fff; }
.st-lab{ font-size:.72em; color:var(--muted); margin-top:.05em; }
.statcard.navy .st-lab{ color:var(--sky); opacity:.9; }

/* ---- whycard ---- */
.whycard{ border-radius:.6em; padding:1.2em 1.3em; height:100%; color:#fff; }
.whycard.navy{ background:linear-gradient(160deg,var(--navy),#152645); }
.whycard.red{ background:linear-gradient(160deg,#a5352a,#7f2a22); }
.wc-title{ font-weight:800; font-size:.86em; color:var(--sky); margin-bottom:.7em; }
.whycard.red .wc-title{ color:#ffd9d3; }
.whycard p{ margin:0 0 .62em; font-size:.87em; line-height:1.4; opacity:.97; }
.whycard p.hi{ color:var(--mint); font-weight:700; }
.whycard.red p.hi{ color:#fff; font-weight:800; }
.wc-lab{ color:var(--sky); font-weight:700; font-size:.92em; }
.wc-big{ font-size:1.7em; font-weight:800; color:#fff; display:block; letter-spacing:-.01em; }

/* ---- sidecard ---- */
.sidecard{ background:var(--card); border:1px solid var(--card-line); border-radius:.6em; padding:1.1em 1.2em; height:100%; }
.sc-title{ font-weight:800; font-size:.84em; margin-bottom:.6em; }
.sidecard ul.bl li{ font-size:.86em; }

/* ---- compare3 ---- */
.cmp3{ display:grid; grid-template-columns:repeat(3,1fr); gap:1.1em; }
.cmp-card{ background:var(--paper); border:1px solid var(--card-line); border-radius:.6em; overflow:hidden; box-shadow:0 2px 8px rgba(20,40,70,.05); }
.cmp-head{ color:#fff; font-weight:800; font-size:.92em; text-align:center; padding:.7em .5em; }
.cmp-body{ padding:.85em 1em 1em; }
.cmp-body p{ margin:0 0 .5em; font-size:.84em; line-height:1.35; padding-left:.9em; position:relative; }
.cmp-body p:before{ content:""; position:absolute; left:0; top:.55em; width:.32em; height:.32em; border-radius:50%; background:var(--teal); }

/* ---- strip ---- */
.strip{ margin-top:1.05em; background:var(--card); border:1px solid var(--card-line); border-radius:.5em; padding:.75em 1.1em; font-size:.84em; line-height:1.4; }
.strip.navy{ background:linear-gradient(120deg,var(--navy),#1d3556); color:#fff; border:none; }
.strip.navy b{ color:var(--mint); }

/* ---- table ---- */
table.tbl{ width:100%; border-collapse:separate; border-spacing:0; border-radius:.5em; overflow:hidden; box-shadow:0 2px 10px rgba(20,40,70,.06); }
table.tbl th{ background:var(--navy); color:#fff; font-weight:800; font-size:.82em; text-align:center; padding:.7em .7em; }
table.tbl th:first-child{ text-align:left; }
table.tbl td{ font-size:.85em; padding:.62em .75em; text-align:center; border-top:1px solid var(--line); vertical-align:middle; line-height:1.32; }
table.tbl.small td{ font-size:.79em; padding:.5em .65em; }
table.tbl.small th{ font-size:.78em; padding:.6em .65em; }
table.tbl td.lead{ text-align:left; font-weight:700; color:var(--ink); }
table.tbl tbody tr:nth-child(even) td{ background:color-mix(in srgb,var(--card) 60%, var(--paper)); }
table.tbl tbody tr:nth-child(odd) td{ background:var(--paper); }

/* ---- numbered ---- */
.numbered{ display:flex; flex-direction:column; gap:.5em; }
.num-row{ display:flex; gap:.85em; align-items:stretch; }
.num-badge{ flex:0 0 auto; width:2.05em; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:800; font-size:1.15em; border-radius:.4em; }
.num-card{ flex:1; background:var(--card); border:1px solid var(--card-line); border-radius:.45em; padding:.5em .95em; display:flex; align-items:center; gap:1em; min-width:0; }
.num-t{ font-weight:800; font-size:.9em; flex:0 0 32%; }
.num-d{ font-size:.82em; color:var(--ink); line-height:1.3; }

/* ---- steps ---- */
.steps{ display:flex; flex-direction:column; gap:.6em; }
.step-row{ display:flex; gap:.9em; align-items:stretch; }
.step-lab{ flex:0 0 22%; color:#fff; font-weight:800; font-size:.92em; border-radius:.45em; display:flex; align-items:center; justify-content:center; padding:.7em; text-align:center; }
.step-card{ flex:1; background:var(--card); border:1px solid var(--card-line); border-radius:.45em; padding:.7em 1em; font-size:.85em; line-height:1.34; display:flex; align-items:center; }

/* ---- flow ---- */
.flow-wrap{ background:var(--card); border:1px solid var(--card-line); border-radius:.55em; padding:1em 1.2em 1.15em; margin-bottom:1.1em; }
.flow-cap{ color:var(--c-navy); font-weight:800; font-size:.86em; margin-bottom:.75em; }
.flow{ display:flex; align-items:stretch; gap:.15em; }
.flow-node{ flex:1; background:var(--navy2); color:#fff; border-radius:.45em; padding:.7em .5em; text-align:center; font-weight:700; font-size:.8em; line-height:1.25; display:flex; align-items:center; justify-content:center; }
.flow-arw{ display:flex; align-items:center; color:var(--teal); font-size:.9em; padding:0 .1em; }

/* ---- two / three / mini / big cards ---- */
.two{ display:grid; grid-template-columns:1fr 1fr; gap:1.2em; }
.three{ display:grid; grid-template-columns:repeat(3,1fr); gap:1em; margin-top:1em; }
.bigcard,.minicard{ background:var(--paper); border:1px solid var(--card-line); border-radius:.55em; overflow:hidden; box-shadow:0 2px 8px rgba(20,40,70,.05); }
.bc-head,.mc-head{ color:#fff; font-weight:800; text-align:center; }
.bc-head{ font-size:.92em; padding:.65em; } .mc-head{ font-size:.82em; padding:.55em; }
.bc-list,.mc-list{ list-style:none; margin:0; padding:.85em 1.15em 1em; display:flex; flex-direction:column; gap:.5em; }
.bc-list li,.mc-list li{ position:relative; padding-left:.95em; line-height:1.34; }
.bc-list li{ font-size:.85em; } .mc-list li{ font-size:.78em; }
.bc-list li:before,.mc-list li:before{ content:"·"; position:absolute; left:.1em; top:-.05em; color:var(--teal); font-weight:800; font-size:1.2em; }

/* ---- legend ---- */
.legend{ background:var(--card); border:1px solid var(--card-line); border-radius:.6em; padding:1.1em 1.25em; height:100%; }
.lg-title{ font-weight:800; font-size:.84em; margin-bottom:.75em; }
.lg-row{ display:flex; align-items:center; gap:.6em; padding:.5em 0; border-top:1px solid color-mix(in srgb,var(--line) 75%, transparent); font-size:.86em; }
.lg-row:first-of-type{ border-top:none; }
.lg-row b{ color:var(--c-navy); min-width:8.3em; }
.lg-note{ color:var(--muted); font-size:.92em; }
.lg-dot{ width:.55em; height:.9em; border-radius:2px; flex:0 0 auto; }
.d-green{background:#2e7d32}.d-amber{background:#b97a0c}.d-red{background:#b03a2e}

/* ---- refs ---- */
.refs{ display:grid; grid-template-columns:1fr 1fr; gap:1.4em; }
ol.refcol{ margin:0; padding-left:1.4em; display:flex; flex-direction:column; gap:.5em; counter-reset:none; }
ol.refcol li{ font-size:.72em; line-height:1.36; color:var(--ink); padding-left:.2em; }
ol.refcol li::marker{ color:var(--c-teal); font-weight:700; }

/* ---- title slide ---- */
.slide.title{ background:var(--paper); padding:0; overflow:hidden; }
.ttl-hero{ background:linear-gradient(150deg,var(--navy) 0%, #16294a 100%); color:#fff; padding:3.1em 3.2em 2.6em; position:relative; height:61%; display:flex; flex-direction:column; justify-content:center; }
.ttl-hero:before{ content:""; position:absolute; left:0; top:0; bottom:0; width:.5em; background:var(--teal); }
.ttl-hero:after{ content:""; position:absolute; left:0; right:0; bottom:0; height:.25em; background:var(--teal); }
.ttl-eyebrow{ color:var(--sky); font-weight:800; font-size:1.02em; margin-bottom:.9em; letter-spacing:.01em; }
.ttl-h1{ font-size:3.05em; font-weight:800; line-height:1.14; letter-spacing:-.015em; margin:0; text-wrap:balance; }
.ttl-sub{ color:#afc6df; font-style:italic; font-size:1.02em; margin-top:1.1em; max-width:34em; line-height:1.4; }
.ttl-foot{ padding:1.5em 3.2em; display:flex; flex-direction:column; gap:.5em; }
.ttl-scope{ color:var(--c-navy); font-weight:800; font-size:1.06em; }
.ttl-note{ color:var(--muted); font-size:.92em; }
.ttl-disc{ color:var(--muted); font-style:italic; font-size:.78em; margin-top:.35em; }

/* ---- key slide ---- */
.slide.key{ background:linear-gradient(155deg,var(--navy),#111f38); color:#fff; padding:2.6em 3em; position:relative; }
.slide.key.active{ display:flex; flex-direction:column; justify-content:center; }
.slide.key:before{ content:""; position:absolute; left:0; top:0; bottom:0; width:.5em; background:var(--teal); }
.key-eyebrow{ color:var(--mint); font-weight:800; font-size:.86em; }
.key-h{ font-size:1.72em; font-weight:800; margin:.3em 0 1.1em; line-height:1.2; text-wrap:balance; }
.key-list{ display:flex; flex-direction:column; gap:.72em; }
.key-row{ display:flex; gap:1.4em; align-items:flex-start; padding-left:.9em; position:relative; }
.key-row:before{ content:""; position:absolute; left:0; top:.15em; width:.28em; height:1.15em; background:var(--teal); }
.key-t{ color:var(--mint); font-weight:800; font-size:.98em; flex:0 0 8.2em; }
.key-d{ font-size:.92em; line-height:1.4; opacity:.96; }

/* ---- chrome (nav) ---- */
.chrome{ position:fixed; z-index:20; }
.rail{ top:0; left:0; right:0; height:.32vh; background:transparent; }
.rail .fill{ height:100%; background:linear-gradient(90deg,var(--teal),var(--navy2)); transition:width .3s ease; }
.nav{ bottom:1.4vh; left:50%; transform:translateX(-50%); display:flex; align-items:center; gap:.6vw;
  background:color-mix(in srgb,var(--paper) 86%, transparent); border:1px solid var(--card-line);
  border-radius:2em; padding:.5vh 1vw; box-shadow:var(--shadow); backdrop-filter:blur(8px); }
.nav button{ background:none; border:none; color:var(--ink); font-size:1.5vh; cursor:pointer; padding:.3vh .8vh; border-radius:.5em; display:flex; align-items:center; line-height:1; }
.nav button:hover{ background:color-mix(in srgb,var(--teal) 16%, transparent); color:var(--c-teal); }
.nav button:focus-visible{ outline:2px solid var(--teal); outline-offset:2px; }
.counter{ font-size:1.4vh; font-weight:700; color:var(--muted); font-variant-numeric:tabular-nums; min-width:4.6em; text-align:center; letter-spacing:.03em; }
.counter b{ color:var(--c-navy); }
.tbtn{ position:fixed; top:1.6vh; right:1.6vh; z-index:20; width:4.2vh; height:4.2vh; border-radius:50%;
  background:color-mix(in srgb,var(--paper) 86%, transparent); border:1px solid var(--card-line); color:var(--ink);
  cursor:pointer; box-shadow:var(--shadow); font-size:1.9vh; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(8px); }
.tbtn:hover{ color:var(--c-teal); }
.hint{ position:fixed; bottom:1.5vh; right:1.8vh; z-index:20; color:var(--muted); font-size:1.15vh; opacity:.7; }
.hint kbd{ background:var(--card); border:1px solid var(--card-line); border-radius:.35em; padding:.05em .4em; font-family:inherit; font-size:.95em; }

@media (max-width:760px){
  :root{ --fs:2.7vw; }
  .slide{ width:96vw; }
  .nav{ bottom:1vh; } .hint{ display:none; }
}
@media (prefers-reduced-motion:reduce){ *{ transition:none !important; } }

/* ---- print: all slides stacked ---- */
@media print{
  @page{ size:1280px 720px; margin:0; }
  #rls-deck{ position:static; display:block; background:#fff; }
  .stage{ display:block; padding:0; }
  .chrome,.tbtn,.hint{ display:none !important; }
  .slide{ display:block !important; width:1280px; height:720px; aspect-ratio:auto; page-break-after:always; break-after:page;
    border-radius:0; box-shadow:none; border:none; margin:0; font-size:18.7px; }
}
"""

JS = r"""
(function(){
  var deck=document.getElementById('rls-deck');
  var slides=Array.prototype.slice.call(deck.querySelectorAll('.slide'));
  var i=0, n=slides.length;
  var railFill=document.getElementById('railfill');
  var cur=document.getElementById('cur'), tot=document.getElementById('tot');
  tot.textContent=String(n).padStart(2,'0');
  function show(k){
    i=Math.max(0,Math.min(n-1,k));
    slides.forEach(function(s,j){ s.classList.toggle('active', j===i); });
    railFill.style.width=((i+1)/n*100)+'%';
    cur.textContent=String(i+1).padStart(2,'0');
    if(location.hash!=='#'+(i+1)) history.replaceState(null,'','#'+(i+1));
  }
  function next(){ show(i+1); } function prev(){ show(i-1); }
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowRight'||e.key==='PageDown'||e.key===' '){ e.preventDefault(); next(); }
    else if(e.key==='ArrowLeft'||e.key==='PageUp'){ e.preventDefault(); prev(); }
    else if(e.key==='Home'){ show(0); } else if(e.key==='End'){ show(n-1); }
  });
  deck.addEventListener('click',function(e){
    if(e.target.closest('.chrome')||e.target.closest('.tbtn')) return;
    var r=deck.getBoundingClientRect();
    if(e.clientX < r.left + r.width*0.32) prev();
    else if(e.clientX > r.left + r.width*0.68) next();
  });
  document.getElementById('prev').addEventListener('click',function(e){e.stopPropagation();prev();});
  document.getElementById('next').addEventListener('click',function(e){e.stopPropagation();next();});
  // theme toggle
  var tb=document.getElementById('theme');
  function sysDark(){ return window.matchMedia && window.matchMedia('(prefers-color-scheme:dark)').matches; }
  function curDark(){ var a=document.documentElement.getAttribute('data-theme'); return a? a==='dark' : sysDark(); }
  tb.addEventListener('click',function(){
    var d=!curDark(); document.documentElement.setAttribute('data-theme', d?'dark':'light');
    tb.textContent=d?'☾':'☀';
  });
  tb.textContent=curDark()?'☾':'☀';
  var h=parseInt((location.hash||'').replace('#',''),10);
  show(isFinite(h)&&h>=1? h-1 : 0);
  // touch swipe
  var x0=null;
  deck.addEventListener('touchstart',function(e){ x0=e.touches[0].clientX; },{passive:true});
  deck.addEventListener('touchend',function(e){ if(x0==null)return; var dx=e.changedTouches[0].clientX-x0;
    if(Math.abs(dx)>40){ dx<0?next():prev(); } x0=null; },{passive:true});
})();
"""

HTML = (f'<title>하지불안증후군(RLS) 근거 기반 치료</title>\n'
        f'<style>{CSS}</style>\n'
        f'<div id="rls-deck"><div class="stage">\n' + "\n".join(slides) + '\n</div>'
        f'<div class="chrome rail"><div class="fill" id="railfill"></div></div>'
        f'<button class="tbtn" id="theme" aria-label="테마 전환">☀</button>'
        f'<div class="chrome nav">'
        f'<button id="prev" aria-label="이전 슬라이드">‹</button>'
        f'<span class="counter"><b id="cur">01</b> / <span id="tot">30</span></span>'
        f'<button id="next" aria-label="다음 슬라이드">›</button></div>'
        f'<div class="hint"><kbd>←</kbd> <kbd>→</kbd> 이동 · <kbd>F</kbd> 전체화면</div>'
        f'</div>\n<script>{JS}</script>')

open(OUT, "w").write(HTML)
print("wrote", OUT, "|", len(slides), "slides |", len(HTML), "bytes")
