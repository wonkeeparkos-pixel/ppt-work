# -*- coding: utf-8 -*-
"""하지불안증후군(RLS) 치료 PPT 생성기. 02_RLS 문헌고찰 근거 기반.
디자인 시스템은 야간 하지경련 프리미엄 덱(build_ppt.py)과 동일 규격."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- palette ----------
NAVY   = RGBColor(0x1B, 0x35, 0x5E)
NAVY2  = RGBColor(0x24, 0x47, 0x74)
TEAL   = RGBColor(0x2C, 0x89, 0x8A)
TEALD  = RGBColor(0x1F, 0x6E, 0x70)
INK    = RGBColor(0x1A, 0x20, 0x2C)
MUTE   = RGBColor(0x5A, 0x6B, 0x7B)
LGRAY  = RGBColor(0xEE, 0xF2, 0xF6)
CARD   = RGBColor(0xF5, 0xF8, 0xFB)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
GREEN  = RGBColor(0x2E, 0x7D, 0x32)
AMBER  = RGBColor(0xB9, 0x7A, 0x0C)
RED    = RGBColor(0xB0, 0x3A, 0x2E)
LINE   = RGBColor(0xD5, 0xDE, 0xE7)
SKY    = RGBColor(0xBF, 0xD3, 0xE6)
MINT   = RGBColor(0x9F, 0xE0, 0xD8)

FONT = "NanumGothic"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
SW, SH = prs.slide_width, prs.slide_height

def slide():
    return prs.slides.add_slide(BLANK)

def _set_font(run, size, color, bold=False, italic=False, font=FONT):
    run.font.size = Pt(size); run.font.color.rgb = color
    run.font.bold = bold; run.font.italic = italic; run.font.name = font
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {}); rPr.append(ea)
    ea.set('typeface', font)

def rect(s, x, y, w, h, fill, line=None, line_w=0.75, shadow=False, round_=False):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
                             x, y, w, h)
    if round_:
        try: shp.adjustments[0] = 0.08
        except Exception: pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp

def text(s, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         space_after=4, line_spacing=1.06, wrap=True):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = wrap; tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, para in enumerate(runs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = para.get('align', align) if isinstance(para, dict) else align
        p.space_after = Pt(para.get('space_after', space_after) if isinstance(para, dict) else space_after)
        p.space_before = Pt(para.get('space_before', 0) if isinstance(para, dict) else 0)
        p.line_spacing = para.get('ls', line_spacing) if isinstance(para, dict) else line_spacing
        items = para['runs'] if isinstance(para, dict) else para
        if para.get('level') if isinstance(para, dict) else None:
            p.level = para['level']
        for it in items:
            r = p.add_run(); r.text = it[0]
            _set_font(r, it[1], it[2], bool(it[3]) if len(it) > 3 else False,
                      bool(it[4]) if len(it) > 4 else False,
                      it[5] if len(it) > 5 else FONT)
    return tb

def header(s, title, eyebrow=None, tag=None, tag_color=TEAL):
    rect(s, 0, 0, SW, Inches(1.18), WHITE)
    rect(s, Inches(0.55), Inches(0.34), Inches(0.12), Inches(0.5), TEAL)
    text(s, Inches(0.8), Inches(0.26), Inches(10.6), Inches(0.75),
         [[(title, 25, NAVY, True)]], anchor=MSO_ANCHOR.MIDDLE)
    if eyebrow:
        text(s, Inches(0.82), Inches(0.12), Inches(8), Inches(0.24),
             [[(eyebrow, 11, TEALD, True)]])
    rect(s, Inches(0.8), Inches(1.06), Inches(11.9), Pt(1.4), LINE)
    if tag:
        w = Inches(0.28 + 0.115*len(tag))
        rect(s, SW - w - Inches(0.55), Inches(0.4), w, Inches(0.38), tag_color, round_=True)
        text(s, SW - w - Inches(0.55), Inches(0.4), w, Inches(0.38),
             [[(tag, 11.5, WHITE, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

def footer(s, src, idx=None):
    page = len(prs.slides._sldIdLst)
    text(s, Inches(0.8), Inches(7.06), Inches(10.8), Inches(0.32),
         [[("근거: " + src, 9, MUTE)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(12.1), Inches(7.06), Inches(0.9), Inches(0.32),
         [[(str(page), 10, MUTE, True)]], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def bullets(s, x, y, w, h, items, size=15, gap=7, color=INK):
    tb = s.shapes.add_textbox(x, y, w, h); tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    for i, it in enumerate(items):
        lv = it[0]; tx = it[1]
        c = it[2] if len(it) > 2 and it[2] else color
        b = it[3] if len(it) > 3 else False
        sz = it[4] if len(it) > 4 else size
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = 1.08
        p.alignment = PP_ALIGN.LEFT
        mark = "" if lv < 0 else ("●  " if lv == 0 else ("–  " if lv == 1 else "·  "))
        indent = "" if lv <= 0 else ("      " * lv)
        r = p.add_run(); r.text = indent + mark
        _set_font(r, sz*0.7 if lv == 0 else sz, TEAL if lv == 0 else MUTE, True)
        r2 = p.add_run(); r2.text = tx
        _set_font(r2, sz, c, b)
    return tb

def card(s, x, y, w, h, fill=CARD, line=LINE):
    return rect(s, x, y, w, h, fill, line=line, line_w=1.0, round_=True)

def table(s, x, y, w, rows, col_w, header_fill=NAVY, size=12, row_h=Inches(0.42),
          head_size=12.5, zebra=True, align_first_left=True):
    n_rows = len(rows); n_cols = len(col_w)
    total_w = sum(col_w, Emu(0))
    gtbl = s.shapes.add_table(n_rows, n_cols, x, y, total_w, row_h*n_rows).table
    gtbl.first_row = False; gtbl.horz_banding = False
    for ci, cw in enumerate(col_w):
        gtbl.columns[ci].width = cw
    for ri, row in enumerate(rows):
        gtbl.rows[ri].height = Inches(0.5) if ri == 0 else row_h
        for ci, val in enumerate(row):
            cell = gtbl.cell(ri, ci)
            cell.margin_left = Inches(0.08); cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02); cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if ri == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = header_fill
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if (not zebra or ri % 2 == 1) else LGRAY
            tf = cell.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if (ci == 0 and align_first_left) else PP_ALIGN.CENTER
            txt = val[0] if isinstance(val, tuple) else val
            col = val[1] if isinstance(val, tuple) else (WHITE if ri == 0 else INK)
            bold = val[2] if (isinstance(val, tuple) and len(val) > 2) else (ri == 0)
            r = p.add_run(); r.text = txt
            _set_font(r, head_size if ri == 0 else size, col, bold)
    return gtbl

# ============================================================ SLIDE 1 — TITLE
s = slide()
rect(s, 0, 0, SW, SH, WHITE)
rect(s, 0, 0, SW, Inches(4.55), NAVY)
rect(s, 0, Inches(4.55), SW, Inches(0.09), TEAL)
rect(s, Inches(0.0), Inches(0.0), Inches(0.22), Inches(4.55), TEAL)
text(s, Inches(0.9), Inches(1.02), Inches(11.5), Inches(0.4),
     [[("하지불안증후군 · Willis–Ekbom Disease", 15, SKY, True)]])
text(s, Inches(0.9), Inches(1.55), Inches(11.6), Inches(2.0),
     [[("철분 교정을 기반으로 한", 33, WHITE, True)],
      [("근거 기반 치료 정리", 33, WHITE, True)]], line_spacing=1.12)
text(s, Inches(0.9), Inches(3.5), Inches(11.5), Inches(0.55),
     [[("Restless Legs Syndrome — Evidence-based Iron · Injection · Pharmacotherapy (AASM 2025)",
        13, RGBColor(0xAF,0xC6,0xDF), False, True)]])
text(s, Inches(0.9), Inches(4.95), Inches(11.5), Inches(1.2),
     [[("구성: 진단·감별 → 병태생리 → 치료(철분 · 주사 · 경구약제 · ESWT) → 알고리즘",
        13.5, INK, True)],
      [("직접 근거와 인접 근거를 구분해 정리 · 근거 없는 항목은 '없음'으로 정직하게 명시", 12.5, MUTE)]], space_after=6)
text(s, Inches(0.9), Inches(6.62), Inches(11.5), Inches(0.5),
     [[("교육·연구 참고용 문헌고찰. 개별 환자의 진단·처방 결정은 담당 의사(신경과/수면의학 등)의 판단에 따릅니다.   |   작성 2026-07",
        11, MUTE, False, True)]])

# ============================================================ SLIDE 2 — RLS란
s = slide()
header(s, "하지불안증후군(RLS)이란 무엇인가", eyebrow="배경 · 임상 문제", tag="배경")
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(5.2), [
    (0, "정의: 다리를 '움직이고 싶은 충동'을 핵심으로 하는 감각-운동 신경질환. 대개 불쾌한 다리 이상감각을 동반한다.", INK, True),
    (0, "특징: 통증보다 '불편·안절부절·벌레가 기어가는 느낌' 등 이상감각이 주. 만져지는 근경직은 없다.", INK),
    (0, "유병률: 성인 약 5~10%(여성·고령에서 증가). 수면개시·유지 장애로 삶의 질을 크게 떨어뜨린다.", INK),
    (0, "동반: 수면 중 주기성 사지운동(PLMS)이 흔히 동반된다.", INK),
    (1, "→ 관리의 성패는 정확한 진단(IRLSSG 5기준)과 철분 상태 평가에서 시작된다.", TEALD, True),
], size=15, gap=12)
card(s, Inches(8.05), Inches(1.6), Inches(4.55), Inches(4.9))
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4),
     [[("핵심 수치", 13, TEALD, True)]])
for i,(num,lab) in enumerate([("5–10%","성인 유병률"),
                              ("여성·고령","유병 위험 증가군"),
                              ("5가지","IRLSSG 필수 진단기준"),
                              ("저녁·밤","증상 악화(일주기)")]):
    yy = Inches(2.35 + i*1.0)
    text(s, Inches(8.35), yy, Inches(4.0), Inches(0.55),
         [[(num, 25, NAVY, True)]])
    text(s, Inches(8.35), yy+Inches(0.52), Inches(4.0), Inches(0.3),
         [[(lab, 12, MUTE)]])
footer(s, "Allen 2014(Sleep Med, IRLSSG); AASM 2025(J Clin Sleep Med)")

# ============================================================ SLIDE 3 — 왜 감별 먼저 (3갈래)
s = slide()
header(s, "왜 감별이 먼저인가 — 세 갈래 병태", eyebrow="진단 · 감별", tag="감별")
cols = [("하지불안증후군(RLS)", "'움직이고 싶은 충동'\n안정 시 악화·움직이면 완화\n통증보다 불쾌한 이상감각\n저녁~밤 뚜렷한 일주기", NAVY2),
        ("야간 하지경련(NLC)", "수면 중 통증성 근수축\n만져지는 근경직(+)\n족배굴곡으로 완화\n종아리·발이 대부분", TEAL),
        ("이차성 · mimic", "철결핍·말기신부전·임신\n말초신경병증·정맥울혈\n약물유발(항히스타민 등)\n'다리 불편'으로 위장", TEALD)]
for i,(t,b,c) in enumerate(cols):
    x = Inches(0.8 + i*4.05)
    card(s, x, Inches(1.55), Inches(3.8), Inches(3.55), WHITE, LINE)
    rect(s, x, Inches(1.55), Inches(3.8), Inches(0.7), c, round_=True)
    rect(s, x, Inches(2.05), Inches(3.8), Inches(0.2), c)
    text(s, x, Inches(1.55), Inches(3.8), Inches(0.7), [[(t,14.5,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+Inches(0.25), Inches(2.45), Inches(3.35), Inches(2.5),
         [[(ln,13,INK)] for ln in b.split("\n")], space_after=8, line_spacing=1.1)
card(s, Inches(0.8), Inches(5.35), Inches(11.85), Inches(1.25), CARD)
text(s, Inches(1.05), Inches(5.55), Inches(11.4), Inches(0.9),
     [[("임상 단서: ", 14, RED, True), ("RLS는 '움직이면 완화'가 결정적이며 근경직이 없다. IRLSSG 2014 기준은 진단 시 '다리경련(NLC) 등 mimic를 반드시 감별·배제'하도록 명문화한다. ",14,INK)],
      [("도파민제(pramipexole)·pregabalin에 반응한다면 임상상이 RLS임을 강하게 시사한다.", 13, MUTE, False, True)]],
     space_after=6)
footer(s, "Allen 2014(Sleep Med, IRLSSG); 02_RLS 문헌고찰 서론")

# ============================================================ SLIDE 4 — RLS vs NLC 표
s = slide()
header(s, "RLS vs NLC 상세 감별표", eyebrow="진단 · 감별", tag="감별")
rows = [("항목","하지불안증후군(RLS)","야간 하지경련(NLC)"),
        ("핵심 증상","움직이고 싶은 충동 + 이상감각","통증성 근수축, 만져지는 근경직"),
        ("주 증상","불편·안절부절(통증 아님)","강한 통증"),
        ("완화 방법","걷기·움직임(멈추면 재발)","스트레칭·족배굴곡"),
        ("만져지는 근경직","없음","있음"),
        ("일주기·가족력","저녁~밤 악화 / 가족력 흔함","야간·수면 초반 / 가족력 드묾"),
        ("1차 치료","철분 교정 + α2δ 리간드","비약물·원인교정 · 개별 약물")]
table(s, Inches(0.8), Inches(1.55), Inches(11.85), rows,
      [Inches(2.5), Inches(4.7), Inches(4.65)], size=12.5, row_h=Inches(0.62))
footer(s, "Allen 2014(IRLSSG); AASM 2025(J Clin Sleep Med); 문헌고찰 감별")

# ============================================================ SLIDE 5 — IRLSSG 5기준
s = slide()
header(s, "진단 — IRLSSG 2014 필수 5기준", eyebrow="진단 · 기준", tag="진단")
crit = [
    ("1", "움직이고 싶은 충동", "다리를 움직이고 싶은 강한 충동, 대개 불쾌한 다리 감각을 동반한다.", NAVY),
    ("2", "안정·비활동 시 악화", "앉거나 누워 쉴 때 증상이 시작되거나 악화된다.", NAVY2),
    ("3", "움직이면 완화", "걷기·스트레칭 등 움직임으로 부분적·일시적으로 완화된다(움직이는 동안 지속).", TEAL),
    ("4", "저녁·밤 악화(일주기)", "저녁·밤에 뚜렷하게 악화되는 circadian 패턴을 보인다.", TEALD),
    ("5", "mimic 배제", "다리경련·자세성 불편·근육통·정맥울혈 등 다른 질환으로 더 잘 설명되지 않는다.", GREEN),
]
for i,(n,t,d,c) in enumerate(crit):
    y = Inches(1.5 + i*0.98)
    rect(s, Inches(0.8), y, Inches(0.8), Inches(0.84), c, round_=True)
    text(s, Inches(0.8), y, Inches(0.8), Inches(0.84), [[(n,26,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    card(s, Inches(1.75), y, Inches(10.9), Inches(0.84), CARD)
    text(s, Inches(2.05), y+Inches(0.1), Inches(3.5), Inches(0.66), [[(t,14,c,True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(5.35), y+Inches(0.08), Inches(7.1), Inches(0.7), [[(d,12.3,INK)]],
         anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
text(s, Inches(0.8), Inches(6.55), Inches(11.8), Inches(0.4),
     [[("요점: 5가지를 모두 충족해야 진단. 통증보다 이상감각이 주이며 촉지되는 근경직은 없다.",12,TEALD,True)]])
footer(s, "Allen RP, et al. IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73.")

# ============================================================ SLIDE 6 — 진단 후 워크업
s = slide()
header(s, "진단 확정 후 — 철분 평가와 악화요인 검토", eyebrow="진단 · workup", tag="철분 평가", tag_color=TEALD)
steps = [("혈청 철분","ferritin · TSAT(트랜스페린포화도) 측정 — 모든 RLS 치료의 출발점이자 기반.",NAVY),
         ("철분 판정","ferritin ≤75 → 경구 철분 고려 / ferritin ≤100(또는 경구 부적절) → 정맥 철분.",NAVY2),
         ("악화요인","철결핍·임신·말기신부전 및 악화 약물(항히스타민·항우울제·도파민 차단제) 확인·조정.",TEAL),
         ("동반평가","수면장애·PLMS·복용약 평가로 이차성 RLS를 감별한다.",TEALD)]
for i,(t,d,c) in enumerate(steps):
    y = Inches(1.6 + i*1.18)
    rect(s, Inches(0.8), y, Inches(2.3), Inches(0.95), c, round_=True)
    text(s, Inches(0.8), y, Inches(2.3), Inches(0.95), [[(t,15,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    card(s, Inches(3.25), y, Inches(9.4), Inches(0.95), CARD)
    text(s, Inches(3.55), y+Inches(0.12), Inches(8.9), Inches(0.72), [[(d,13,INK)]],
         anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.08)
card(s, Inches(0.8), Inches(6.35), Inches(11.85), Inches(0.6), NAVY)
text(s, Inches(1.05), Inches(6.35), Inches(11.4), Inches(0.6),
     [[("요점: 진단은 IRLSSG 5기준(임상)으로 내리고, 검사(ferritin/TSAT)는 치료 방향(철분 보충)을 정하기 위한 것.",12.5,WHITE,True)]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Allen 2018(IRLSSG iron task force); AASM 2025")

# ============================================================ SLIDE 7 — 병태생리 ① 뇌 철분
s = slide()
header(s, "병태생리 ① 뇌 철분 결핍 — 핵심", eyebrow="병태생리 · 기전", tag="핵심 기전", tag_color=TEAL)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"혈청 철분이 정상이어도 흑질·기저핵 등 뇌 국소 철분이 부족하여 도파민 신호 이상을 초래한다.",INK,True),
    (0,"이것이 '철분 보충'이라는 치료의 생물학적 근거 — RLS는 전신 빈혈이 아니라 뇌 국소 철분 문제일 수 있다.",INK),
    (0,"철결핍이 동반되면 증상이 악화되고, 철분 교정으로 호전되는 경우가 많다.",INK),
    (0,"뇌 철분 결핍은 이어서 도파민·아데노신 신호 이상으로 연결된다(다음 장).",INK),
    (-1,"→ 그래서 치료의 기반은 언제나 ferritin/TSAT 평가와 철분 교정이다.",TEALD,True),
], size=14, gap=11)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("왜 철분인가 (기전)",13,SKY,True)]])
text(s, Inches(8.4), Inches(2.5), Inches(3.95), Inches(3.8),
     [[("혈청 ferritin이 정상이어도 뇌 국소(흑질) 철분은 부족할 수 있다.",13.5,WHITE)],
      [("철분은 도파민 합성 효소(tyrosine hydroxylase)의 보조인자다.",13.5,WHITE)],
      [("뇌 철분 부족 → 도파민 신호 이상 → 야간 감각-운동 증상.",13.5,WHITE)],
      [("→ 철분 교정이 이 상류(上流) 병태를 직접 겨냥한다.",13.5,MINT,True)]],
     space_after=12, line_spacing=1.12)
footer(s, "IRLSSG; Allen 2018(Sleep Med); 문헌고찰 Part 1-1")

# ============================================================ SLIDE 8 — 병태생리 ② 도파민·아데노신
s = slide()
header(s, "병태생리 ② 도파민 · 아데노신 가설", eyebrow="병태생리 · 기전", tag="기전")
card(s, Inches(0.8), Inches(1.5), Inches(11.85), Inches(1.75), CARD)
text(s, Inches(1.05), Inches(1.68), Inches(11), Inches(0.35),
     [[("뇌 철분 결핍이 하류(下流)의 신경전달 이상으로 이어진다",13.5,NAVY,True)]])
flow = ["뇌 국소\n철분 결핍","도파민 신호 이상\n아데노신 신호 ↓","글루타메이트·도파민\n과흥분","야간 감각-운동\n증상 · PLMS"]
for i,st in enumerate(flow):
    x = Inches(1.15 + i*2.75)
    rect(s, x, Inches(2.2), Inches(2.3), Inches(0.86), NAVY2, round_=True)
    text(s, x, Inches(2.2), Inches(2.3), Inches(0.86), [[(ln,11.5,WHITE,True)] for ln in st.split("\n")],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0, line_spacing=1.0)
    if i < 3:
        text(s, x+Inches(2.32), Inches(2.2), Inches(0.4), Inches(0.86), [[("▶",15,TEAL,True)]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
card(s, Inches(0.8), Inches(3.5), Inches(5.85), Inches(3.1), WHITE, LINE)
text(s, Inches(1.05), Inches(3.7), Inches(5.4), Inches(0.4), [[("도파민 이상",13,TEALD,True)]])
bullets(s, Inches(1.05), Inches(4.2), Inches(5.3), Inches(2.3), [
    (0,"야간 도파민 기능 저하 가설.",INK),
    (0,"도파민제는 단기 효과가 뚜렷하다.",INK),
    (0,"그러나 장기 사용 시 augmentation(증상 악화·전이)을 유발 → 후순위.",RED),
], size=12.5, gap=10)
card(s, Inches(6.8), Inches(3.5), Inches(5.85), Inches(3.1), WHITE, LINE)
text(s, Inches(7.05), Inches(3.7), Inches(5.4), Inches(0.4), [[("아데노신 저하 가설(최근)",13,TEALD,True)]])
bullets(s, Inches(7.05), Inches(4.2), Inches(5.3), Inches(2.3), [
    (0,"뇌 철분 결핍이 아데노신 신호를 낮춘다.",INK),
    (0,"→ 글루타메이트·도파민 과흥분을 유발한다는 가설.",INK),
    (0,"dipyridamole 등 새로운 표적 치료의 이론적 근거.",GREEN),
], size=12.5, gap=10)
footer(s, "IRLSSG; Garcia-Borreguero 2021(아데노신 가설); 문헌고찰 Part 1-2·1-3")

# ============================================================ SLIDE 9 — 유전·이차·악화약물
s = slide()
header(s, "병태생리 ③ 유전 · 이차 요인 · 악화 약물", eyebrow="병태생리 · 위험요인", tag="위험요인")
bullets(s, Inches(0.8), Inches(1.5), Inches(6.6), Inches(2.0), [
    (0,"가족력이 흔하다(상염색체 우성 경향) — 조기 발병일수록 유전 기여가 크다.",INK,True),
    (0,"이차성 RLS는 원인 교정으로 호전될 수 있어 반드시 선별한다.",INK),
], size=13.5, gap=10)
rows = [("범주","대표 요인"),
        ("철 대사","철결핍(기반 병태) — ferritin/TSAT 확인·교정"),
        ("생리·전신","임신, 말기신부전(투석), 갑상선 이상"),
        ("악화 약물","항히스타민, 항우울제(SSRI/SNRI 등), 도파민 차단제(항구토·항정신병)"),
        ("생활요인","카페인·알코올·수면부족 — 악화 유발 가능")]
table(s, Inches(0.8), Inches(3.55), Inches(6.6), rows,
      [Inches(1.7), Inches(4.9)], size=12, row_h=Inches(0.62), head_size=12)
card(s, Inches(7.7), Inches(1.55), Inches(4.95), Inches(5.0), NAVY)
text(s, Inches(8.0), Inches(1.85), Inches(4.3), Inches(0.4), [[("실무 포인트",13,SKY,True)]])
bullets(s, Inches(8.0), Inches(2.45), Inches(4.35), Inches(4.0), [
    (0,"이차 요인·악화 약물을 먼저 교정하면 약물 없이도 호전될 수 있다.",WHITE,True),
    (0,"항우울제가 꼭 필요하면 RLS 악화가 적은 약제(예: bupropion 계열)를 고려.",WHITE),
    (0,"임신·신부전 동반 RLS는 안전한 치료(철분 등)를 우선.",WHITE),
    (0,"→ '원인 교정'이 약물치료보다 앞선다.",MINT,True),
], size=12.5, gap=12)
footer(s, "IRLSSG; 문헌고찰 Part 1-4")

# ============================================================ SLIDE 10 — 치료 근거 한눈에
s = slide()
header(s, "치료 근거 한눈에 — 무엇이 되고 무엇이 안 되나", eyebrow="총괄", tag="요약")
rows = [("치료","RLS 직접 근거","근거·권고","위치"),
        ("철분 교정(경구/정맥)","Earley 2024 RCT · IRLSSG 2018","강한 권고","기반 · 필수"),
        ("α2δ 리간드","Allen 2014 등 RCT","강한 권고(1차)","1차 약물"),
        ("IV 철분(FCM)","Earley 2024 RCT · 메타분석","강한 권고","철결핍 시"),
        ("dipyridamole","Garcia-Borreguero 2021 교차RCT","조건부","신규 · 아데노신"),
        ("비골신경 자극(TOMAC)","Charlesworth 2023 sham 대조","조건부","비약물 대안"),
        ("도파민 작용제","Winkelman 2006 RCT","장기 권고 안 함","augmentation로 후순위"),
        ("보툴리눔독소","Mittal 2018 교차RCT(소규모)","근거 약함","연구 단계"),
        ("체외충격파(ESWT)","없음","—","RLS 근거 없음")]
table(s, Inches(0.8), Inches(1.5), Inches(11.85), rows,
      [Inches(3.5), Inches(4.0), Inches(2.2), Inches(2.15)], size=11, row_h=Inches(0.5), head_size=12)
footer(s, "AASM 2025 지침 종합 · 02_RLS 문헌고찰 근거표")

# ============================================================ SLIDE 11 — 치료 3축 개관
s = slide()
header(s, "치료 3축 개관 — 기반 · 1차 · 보조", eyebrow="총괄 · 지형", tag="개관")
cols = [("기반 · 철분 교정", "뇌 철분 결핍을 직접 교정\n경구(ferritin≤75)/정맥(≤100)\nEarley 2024 RCT · IRLSSG 2018\nAASM 2025 강한 권고", TEAL),
        ("1차 · 경구약제", "α2δ 리간드 = 1차(강한 권고)\n도파민제는 augmentation로 후순위\ndipyridamole 조건부(신규)\n오피오이드는 난치성에 조건부", NAVY2),
        ("보조 · 주사/비약물", "IV 철분 = 주사 중 근거 최강\n보툴리눔 연구단계 · 정맥경화 표현형\n비골신경 자극(TOMAC) 조건부\nESWT는 RLS 근거 없음", TEALD)]
for i,(t,b,c) in enumerate(cols):
    x = Inches(0.8 + i*4.05)
    card(s, x, Inches(1.55), Inches(3.8), Inches(3.9), WHITE, LINE)
    rect(s, x, Inches(1.55), Inches(3.8), Inches(0.7), c, round_=True)
    rect(s, x, Inches(2.05), Inches(3.8), Inches(0.2), c)
    text(s, x, Inches(1.55), Inches(3.8), Inches(0.7), [[(t,14,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+Inches(0.25), Inches(2.45), Inches(3.35), Inches(2.9),
         [[(ln,12.5,INK)] for ln in b.split("\n")], space_after=9, line_spacing=1.12)
card(s, Inches(0.8), Inches(5.7), Inches(11.85), Inches(0.95), NAVY)
text(s, Inches(1.05), Inches(5.7), Inches(11.4), Inches(0.95),
     [[("2024/2025 AASM 지침의 핵심 변화: 1차 약물을 도파민제에서 α2δ 리간드로 전환 — augmentation 위험 때문.",13,WHITE,True)]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Winkelman 2025(AASM); 문헌고찰 치료 3축")

# ============================================================ SLIDE 12 — 철분 교정 기반(경구/정맥)
s = slide()
header(s, "기반 치료: 철분 교정 — 경구와 정맥의 분기", eyebrow="치료 · 기반", tag="효과 있음", tag_color=GREEN)
cards_data = [
    ("경구 철분", TEAL, [
        "적응: ferritin ≤75(흡수 여지가 있을 때)",
        "ferrous sulfate + 비타민 C(흡수↑)",
        "격일 투여가 흡수·내약성에 유리할 수 있음",
        "한계: ferritin ≥75에서는 흡수가 미미",
        "부작용: 위장장애·변비"]),
    ("정맥 철분 (FCM)", NAVY2, [
        "적응: ferritin ≤100 또는 경구 부적절/불내",
        "FCM 1000 mg 단회(또는 750 mg×2)",
        "1시간 이내 점적",
        "중등도~중증에 FCM 1000 mg은 Level A",
        "안전: 일과성 저인산혈증 모니터링"])]
xs = [Inches(0.8), Inches(6.8)]
for (t,c,lines),x in zip(cards_data, xs):
    card(s, x, Inches(1.55), Inches(5.85), Inches(4.35), WHITE, LINE)
    rect(s, x, Inches(1.55), Inches(5.85), Inches(0.62), c, round_=True)
    text(s, x, Inches(1.55), Inches(5.85), Inches(0.62), [[(t,14,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+Inches(0.32), Inches(2.45), Inches(5.25), Inches(3.3),
         [[("•  "+ln,13,INK)] for ln in lines], space_after=11, line_spacing=1.08)
card(s, Inches(0.8), Inches(6.15), Inches(11.85), Inches(0.75), CARD)
text(s, Inches(1.05), Inches(6.15), Inches(11.4), Inches(0.75),
     [[("원칙: ",13.5,TEALD,True),("철분 교정은 약물치료의 대안이 아니라 '기반'이다. 경구로 목표에 못 미치거나 흡수가 부족하면 정맥으로 전환한다.",13,INK)]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Allen 2018(IRLSSG iron); Earley 2024(Sleep); AASM 2025")

# ============================================================ SLIDE 13 — IV 철분 근거
s = slide()
header(s, "주사 ① 정맥 철분(IV FCM) — 근거 최강", eyebrow="치료 · 주사", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(4.9), [
    (0,"뇌 철분 결핍이라는 핵심 병태를 직접 교정하는, RLS 주사 치료 중 근거가 가장 확실하다.",INK,True),
    (0,"Earley 2024(Sleep) 다기관 RCT: IRLS ≥15인 209명, FCM 750 mg(0일·5일 2회) vs 위약.",INK),
    (1,"42일째 IRLS·CGI가 위약 대비 유의하게 개선.",GREEN,True),
    (0,"메타분석 2024(537명)도 효과·안전성을 확인.",INK),
    (0,"경구 철분은 ferritin ≥75에서 흡수가 미미 → 정맥 투여가 유리한 경우가 많다.",INK),
    (-1,"→ 철결핍(또는 경구 부적절) 동반 RLS에서 AASM 2025 강한 권고.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.05), Inches(1.55), Inches(4.55), Inches(4.95), NAVY)
text(s, Inches(8.35), Inches(1.8), Inches(4.0), Inches(0.4), [[("Earley 2024 (RCT 핵심)",13,SKY,True)]])
for i,(a,b) in enumerate([("설계","다기관 RCT · n=209"),
                          ("용법","FCM 750 mg (0·5일)"),
                          ("결과(42일)","IRLS·CGI 유의 개선"),
                          ("메타분석","537명 효과·안전 확인")]):
    yy = Inches(2.4 + i*1.0)
    text(s, Inches(8.35), yy, Inches(4.0), Inches(0.3), [[(a,12,RGBColor(0x9F,0xB8,0xD6),True)]])
    text(s, Inches(8.35), yy+Inches(0.28), Inches(4.0), Inches(0.5), [[(b,17,WHITE,True)]])
footer(s, "Earley CJ, et al. Sleep. 2024;47(7):zsae095. PMID 38625730; 메타분석 2024")

# ============================================================ SLIDE 14 — IV 철분 용량·적응·안전
s = slide()
header(s, "정맥 철분 — 용량 · 적응 · 안전", eyebrow="치료 · 주사 · 기법", tag="기법", tag_color=TEALD)
rows = [("항목","권고 요지"),
        ("대표 약제","Ferric carboxymaltose (FCM)"),
        ("용량","FCM 1000 mg 단회 (또는 750 mg×2)"),
        ("투여","정맥 점적 · 1시간 이내"),
        ("적응(IRLSSG 2018)","정맥: ferritin ≤100 또는 경구 부적절 / 경구: ferritin ≤75"),
        ("근거수준","중등도~중증 FCM 1000 mg = Level A"),
        ("권고","AASM 2025 강한 권고")]
table(s, Inches(0.8), Inches(1.5), Inches(7.5), rows,
      [Inches(2.5), Inches(5.0)], size=12, row_h=Inches(0.56))
card(s, Inches(8.6), Inches(1.55), Inches(4.0), Inches(5.0), CARD)
text(s, Inches(8.85), Inches(1.8), Inches(3.5), Inches(0.4), [[("안전 · 주의",13,RED,True)]])
bullets(s, Inches(8.85), Inches(2.3), Inches(3.55), Inches(4.0), [
    (0,"일과성 저인산혈증 — 반복·고용량 시 모니터링.",RED),
    (0,"드물게 주입반응·과민반응 — 투여 중 관찰.",INK),
    (0,"활동성 감염 시 정맥 철분은 신중.",INK),
    (0,"경구 실패·불내·흡수부족에서 특히 유용.",GREEN),
    (-1,"→ 철분 상태(ferritin/TSAT) 재평가로 반복 여부 결정.",TEALD,True),
], size=12, gap=10)
footer(s, "Allen 2018(IRLSSG iron task force, Sleep Med); Earley 2024")

# ============================================================ SLIDE 15 — 보툴리눔
s = slide()
header(s, "주사 ② 보툴리눔독소(BoNT-A) — 근거 약함·혼재", eyebrow="치료 · 주사", tag="연구 단계", tag_color=AMBER)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.9), [
    (0,"Mittal 2018(Toxins) 이중맹검 교차(n=24): incobotulinumtoxinA 100단위를 전경골근·비복근·대퇴이두근에 주사.",INK,True),
    (1,"4·6주에 IRLS 점수·통증(VAS)이 유의하게 개선.",GREEN),
    (0,"SR/MA(Healthcare 2021): RCT 2편·27명, IRLS SMD −0.819.",INK),
    (1,"표본이 매우 작아 확정 불가 → 대규모 RCT 필요.",MUTE,True),
    (-1,"위치: 표준치료가 아니다. 특정 표현형·연구단계 옵션으로 본다.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("요점",13,TEALD,True)]])
bullets(s, Inches(8.35), Inches(2.35), Inches(4.0), Inches(4.0), [
    (0,"표적: 전경골근·비복근·대퇴이두근.",INK),
    (0,"용량: incoA 100U(Mittal 프로토콜).",INK),
    (0,"근거: RCT 2편·소표본(Level 낮음).",INK),
    (0,"기전은 국소적이며 RLS 중추 병태를 겨냥하지 않음.",MUTE),
    (-1,"→ 근거 확립 전까지 표준치료 아님.",TEALD,True),
], size=12.5, gap=9)
footer(s, "Mittal 2018(Toxins 10(10):401); SR/MA Healthcare 2021;9(11):1538")

# ============================================================ SLIDE 16 — 정맥 경화요법
s = slide()
header(s, "주사 ③ 정맥 경화요법 — 정맥질환 동반 표현형", eyebrow="치료 · 주사", tag="표현형 한정", tag_color=AMBER)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.9), [
    (0,"정맥류·만성정맥부전(CVI)이 동반된 RLS 표현형을 표적으로 하는 접근.",INK,True),
    (0,"Pyne 2023(JVIR)·Sundaresan 2019(Cureus): 하지정맥 치료 후 IRLS 점수 개선.",INK),
    (1,"IRLS 19.83 → 7.89 (약 63% 호전).",GREEN,True),
    (0,"기전: 정맥울혈·측부 자극이라는 말초 유발요인을 제거한다는 해석.",INK),
    (-1,"위치: 정맥질환이 확인된 특정 표현형에서 의미. 특발성 RLS 전반의 표준은 아니다.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("핵심 수치",13,SKY,True)]])
text(s, Inches(8.4), Inches(2.55), Inches(4.0), Inches(0.4), [[("IRLS 점수 변화",12,RGBColor(0x9F,0xB8,0xD6),True)]])
text(s, Inches(8.4), Inches(2.9), Inches(4.0), Inches(0.6), [[("19.83 → 7.89",26,WHITE,True)]])
text(s, Inches(8.4), Inches(3.65), Inches(4.0), Inches(0.4), [[("약 63% 호전",14,MINT,True)]])
text(s, Inches(8.4), Inches(4.45), Inches(4.0), Inches(1.8),
     [[("적응: 정맥류·CVI가 확인된 RLS.",13,WHITE)],
      [("표적: 하지 표재정맥 치료(경화·소작).",13,WHITE)],
      [("→ 원인(정맥질환) 표적치료로서 의미.",13,MINT,True)]], space_after=10, line_spacing=1.12)
footer(s, "Pyne 2023(JVIR 34(4):534-42); Sundaresan 2019(Cureus 11(4):e4368)")

# ============================================================ SLIDE 17 — 경구약제 개관
s = slide()
header(s, "경구약제 개관 — 1차 패러다임의 전환", eyebrow="치료 · 경구약제", tag="약제")
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(5.0), [
    (0,"2024/2025 AASM 지침의 핵심: 1차 약물을 도파민제에서 α2δ 리간드로 전환.",INK,True),
    (0,"이유: 도파민제의 장기 augmentation(연 7~10%) 위험이 α2δ 리간드보다 크다.",INK),
    (0,"철분 교정을 기반으로 하고, 그 위에 경구약제를 얹는다.",INK),
    (0,"고령·신기능 저하: 낙상·진정·부종을 고려해 저용량에서 서서히 적정.",INK),
], size=14, gap=11)
card(s, Inches(8.05), Inches(1.6), Inches(4.55), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("약물군 · 권고 요지",13,TEALD,True)]])
data = [("α2δ 리간드","1차 · 강한 권고",GREEN),
        ("철분(경구)","기반 · 필수",GREEN),
        ("dipyridamole","조건부 · 신규",AMBER),
        ("오피오이드(서방형)","난치성 · 조건부",AMBER),
        ("도파민 작용제","장기 권고 안 함",RED)]
for i,(a,b,c) in enumerate(data):
    yy = Inches(2.4 + i*0.78)
    rect(s, Inches(8.35), yy+Inches(0.05), Inches(0.16), Inches(0.44), c)
    text(s, Inches(8.62), yy, Inches(4.0), Inches(0.6),
         [[(a+"  ",13,NAVY,True),(b,11.5,MUTE)]], anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Winkelman 2025(AASM, J Clin Sleep Med); 문헌고찰 Part 5")

# ============================================================ SLIDE 18 — α2δ 리간드 1차
s = slide()
header(s, "경구약제 ① α2δ 리간드 — 1차", eyebrow="치료 · 경구약제", tag="1차", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"gabapentin enacarbil · gabapentin · pregabalin. AASM 2025 1차 강한 권고.",INK,True),
    (0,"Allen 2014(NEJM) 52주 RCT: pregabalin 300 mg이 효과적이며,",INK),
    (1,"augmentation 1.7% vs pramipexole 0.5 mg 9.0%로 유의하게 낮음.",GREEN,True),
    (0,"Gabapentin enacarbil: Winkelman 2011(PSG) 각성·PLM 감소, Bogan 2010 장기 유지.",INK),
    (0,"부작용: 어지럼·졸림·부종·체중증가. 고령·신기능 저하 시 감량.",INK),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("왜 1차인가",13,SKY,True)]])
text(s, Inches(8.4), Inches(2.5), Inches(3.95), Inches(3.8),
     [[("도파민제보다 augmentation이 유의하게 적다(1.7% vs 9.0%).",13.5,WHITE)],
      [("수면과 감각증상을 함께 개선한다.",13.5,WHITE)],
      [("철분 교정과 병행하는 것이 기반이다.",13.5,WHITE)],
      [("→ 장기 관리에 유리한 프로파일.",13.5,MINT,True)]],
     space_after=13, line_spacing=1.12)
footer(s, "Allen 2014(NEJM 370(7):621-31); Winkelman 2011(Mov Disord); AASM 2025")

# ============================================================ SLIDE 19 — α2δ 상세
s = slide()
header(s, "α2δ 리간드 — 약물 · 특징 · 주의", eyebrow="치료 · 경구약제 · 기법", tag="기법", tag_color=TEALD)
rows = [("약물","특징 · 근거"),
        ("Gabapentin enacarbil","전구약물로 흡수 안정적. PSG상 각성·PLM 감소(Winkelman 2011), 장기 유지(Bogan 2010)"),
        ("Pregabalin","Allen 2014 NEJM 52주: 300 mg 효과적, augmentation 1.7%"),
        ("Gabapentin","저비용·범용. 흡수 변동 있어 분할·적정 필요"),
        ("공통 부작용","어지럼 · 졸림 · 말초부종 · 체중증가"),
        ("고령·신기능","용량 감량 · 저용량에서 서서히 적정 · 낙상 주의")]
table(s, Inches(0.8), Inches(1.5), Inches(11.85), rows,
      [Inches(3.2), Inches(8.65)], size=12, row_h=Inches(0.68), align_first_left=True)
text(s, Inches(0.8), Inches(6.35), Inches(11.8), Inches(0.5),
     [[("소결: α2δ 리간드는 augmentation 위험이 낮고 수면·감각증상을 함께 개선 → 철분 교정 위의 1차 약물.",12,TEALD,True)]])
footer(s, "Allen 2014(NEJM); Winkelman 2011(Mov Disord); Bogan 2010(Mayo Clin Proc)")

# ============================================================ SLIDE 20 — 도파민 작용제
s = slide()
header(s, "경구약제 ② 도파민 작용제 — augmentation 위험", eyebrow="치료 · 경구약제", tag="후순위", tag_color=RED)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"pramipexole · ropinirole · rotigotine. 단기 효능은 확립되어 있다.",INK,True),
    (0,"Winkelman 2006(Neurology): pramipexole 12주 IRLS·CGI 개선.",INK),
    (0,"그러나 수개월~수년 후 augmentation(증상 악화·전이, 연 7~10%)이 문제.",RED,True),
    (0,"AASM 2025는 도파민제의 장기 표준 사용을 '권고하지 않음(against)'.",RED),
    (-1,"복용 중이면 정기 점검 · 철분 재평가 · α2δ 리간드로 단계적 전환을 고려.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), RED)
text(s, Inches(8.4), Inches(2.0), Inches(3.9), Inches(0.5), [[("⚠ Augmentation",15,WHITE,True)]])
bullets(s, Inches(8.4), Inches(2.7), Inches(3.9), Inches(3.6), [
    (0,"증상이 더 이르게·더 넓은 부위로 악화.",WHITE),
    (0,"도파민제 용량을 올릴수록 악화되는 악순환.",WHITE),
    (0,"연 7~10%에서 발생.",WHITE),
    (0,"→ 장기 1차로 권고되지 않음.",WHITE),
], size=13.5, gap=13)
footer(s, "Winkelman 2006(Neurology 67(6):1034-9); Allen 2014(NEJM); AASM 2025")

# ============================================================ SLIDE 21 — dipyridamole
s = slide()
header(s, "경구약제 ③ Dipyridamole — 신규·아데노신", eyebrow="치료 · 경구약제", tag="조건부", tag_color=AMBER)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.9), [
    (0,"아데노신 저하 가설에 기반한 새로운 표적 — 아데노신 재흡수를 억제한다.",INK,True),
    (0,"Garcia-Borreguero 2021(Mov Disord) 교차 RCT.",INK),
    (1,"IRLS 24.1 → 11.1 (위약군 18.7)로 유의한 개선.",GREEN,True),
    (0,"도파민 경로가 아니므로 augmentation 우려가 상대적으로 적다는 이론적 장점.",INK),
    (-1,"위치: 조건부(신규). 표본·추적이 제한적이라 추가 근거가 필요.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("Garcia-Borreguero 2021",13,SKY,True)]])
text(s, Inches(8.4), Inches(2.55), Inches(4.0), Inches(0.4), [[("IRLS (약물군)",12,RGBColor(0x9F,0xB8,0xD6),True)]])
text(s, Inches(8.4), Inches(2.9), Inches(4.0), Inches(0.6), [[("24.1 → 11.1",26,WHITE,True)]])
text(s, Inches(8.4), Inches(3.7), Inches(4.0), Inches(0.4), [[("위약군 18.7",13,MINT,True)]])
text(s, Inches(8.4), Inches(4.5), Inches(4.0), Inches(1.8),
     [[("설계: 위약대조 교차 RCT.",13,WHITE)],
      [("기전: 아데노신 신호 회복 가설.",13,WHITE)],
      [("→ 도파민 비의존 표적의 첫 근거.",13,MINT,True)]], space_after=10, line_spacing=1.12)
footer(s, "Garcia-Borreguero D, et al. Mov Disord. 2021;36(10):2387-92. PMID 34137476")

# ============================================================ SLIDE 22 — 오피오이드
s = slide()
header(s, "경구약제 ④ 오피오이드 — 난치성·조건부", eyebrow="치료 · 경구약제", tag="난치성", tag_color=NAVY2)
bullets(s, Inches(0.8), Inches(1.5), Inches(11.8), Inches(2.2), [
    (0,"저용량 서방형 oxycodone 등 μ-오피오이드는 난치성 RLS 및 도파민제 augmentation 상황에서 조건부로 사용된다.",INK,True),
    (0,"부프레노르핀은 상대적으로 위험이 낮은 선택지로 거론된다. 다만 진정·호흡 억제 위험으로 신중한 적응·감시가 필요하다.",INK),
], size=13.5, gap=10)
cards_data = [
    ("적응 (조건부)", TEALD, [
        "α2δ 리간드·철분 교정에 불응",
        "도파민제 augmentation 발생·전환기",
        "중증·삶의 질 저하가 뚜렷한 경우"]),
    ("약물 · 원칙", NAVY2, [
        "저용량 서방형 oxycodone/μ-오피오이드",
        "부프레노르핀은 상대적 저위험",
        "최소 유효용량 · 정기 재평가"]),
    ("주의 · 안전", RED, [
        "진정 · 호흡 억제 · 변비",
        "의존·오남용 위험 평가 필수",
        "고령·수면무호흡 동반 시 특히 신중"])]
xs = [Inches(0.8), Inches(4.85), Inches(8.9)]
for (t,c,lines),x in zip(cards_data, xs):
    card(s, x, Inches(4.05), Inches(3.75), Inches(2.55), WHITE, LINE)
    rect(s, x, Inches(4.05), Inches(3.75), Inches(0.55), c, round_=True)
    text(s, x, Inches(4.05), Inches(3.75), Inches(0.55), [[(t,13,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+Inches(0.28), Inches(4.78), Inches(3.25), Inches(1.7),
         [[("•  "+ln,12,INK)] for ln in lines], space_after=8, line_spacing=1.08)
footer(s, "AASM 2025(J Clin Sleep Med); 문헌고찰 Part 5-5")

# ============================================================ SLIDE 23 — ESWT RLS 근거 없음
s = slide()
header(s, "체외충격파(ESWT) — RLS 직접 근거 없음", eyebrow="치료 · ESWT", tag="근거 없음", tag_color=RED)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.9), [
    (0,"RLS를 결과변수로 ESWT를 평가한 RCT·전향연구·증례는 검색되지 않는다(2026-07 기준).",RED,True),
    (0,"ESWT의 확립된 근거는 근골격계 통증·경직 영역으로, RLS(뇌 철분·도파민·아데노신)와 병태가 다르다.",INK),
    (0,"미세순환·NO·운동신경원 조절이 이론상 거론되나 RLS 핵심 병태와 직접 연결하는 근거는 없다.",INK),
    (-1,"근거를 창작하지 않는다 → RLS에 ESWT는 권고할 수 없다.",TEALD,True),
], size=14, gap=11)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("근거 있는 대안",13,SKY,True)]])
text(s, Inches(8.4), Inches(2.5), Inches(3.95), Inches(3.8),
     [[("비약물이 필요하면 충격파가 아니라 '말초 비골신경 자극'.",13.5,WHITE)],
      [("Charlesworth 2023: sham 대조에서 증상 개선·수면 무방해.",13.5,WHITE)],
      [("AASM 2025 조건부 권고.",13.5,WHITE)],
      [("→ 다음 장에서 상술.",13.5,MINT,True)]],
     space_after=13, line_spacing=1.12)
footer(s, "문헌고찰 Part 3(직접 근거 부재); Charlesworth 2023(대안)")

# ============================================================ SLIDE 24 — 비골신경 자극
s = slide()
header(s, "근거 있는 비약물 — 말초 비골신경 자극(TOMAC)", eyebrow="비약물 · 기기", tag="조건부", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.9), [
    (0,"Charlesworth 2023(J Clin Sleep Med): 양측 고빈도 비침습적 비골신경 자극(NPNS/TOMAC).",INK,True),
    (0,"중등도~중증 RLS에서 sham(가짜자극) 대조로 평가.",INK),
    (1,"다리 근육의 긴장성 활성을 유발하여, 수면을 방해하지 않고 증상을 개선.",GREEN,True),
    (0,"약물 부작용(augmentation·진정)이 없는 비약물 옵션.",INK),
    (-1,"AASM 2025 조건부 권고 → 비약물이 필요할 때의 우선 고려 대상.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("요점",13,TEALD,True)]])
bullets(s, Inches(8.35), Inches(2.35), Inches(4.0), Inches(4.0), [
    (0,"방식: 양측 비골신경 고빈도 자극.",INK),
    (0,"대상: 중등도~중증 RLS.",INK),
    (0,"근거: sham 대조 시험(Charlesworth 2023).",INK),
    (0,"장점: 수면 무방해 · 전신 부작용 없음.",GREEN),
    (-1,"→ ESWT의 자리를 대신하는 비약물 대안.",TEALD,True),
], size=12.5, gap=9)
footer(s, "Charlesworth JD, et al. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064")

# ============================================================ SLIDE 25 — 알고리즘
s = slide()
header(s, "종합 치료 알고리즘 / 사다리", eyebrow="종합", tag="정리")
steps = [
    ("1", "진단 확정 (IRLSSG 5기준)", "움직임 충동·안정 시 악화·움직이면 완화·저녁 악화·mimic 배제. NLC 등 감별.", NAVY),
    ("2", "철분 평가·교정 (기반)", "ferritin/TSAT. 경구(≤75)/정맥(≤100 또는 경구 부적절, FCM 1000 mg). 악화약물 조정.", NAVY2),
    ("3", "1차 약물 — α2δ 리간드", "gabapentin enacarbil·gabapentin·pregabalin. 수면·감각 개선, augmentation 적음.", TEAL),
    ("4", "도파민제는 후순위", "단기 효과 O이나 augmentation(연 7~10%)로 장기 권고 안 함. 복용 중이면 전환 고려.", TEALD),
    ("5", "난치성 옵션 (선택)", "dipyridamole(조건부)·오피오이드(서방형)·비골신경 자극(TOMAC). ESWT는 RLS 근거 없음.", GREEN)]
for i,(n,t,d,c) in enumerate(steps):
    y = Inches(1.5 + i*1.04)
    rect(s, Inches(0.8), y, Inches(0.75), Inches(0.9), c, round_=True)
    text(s, Inches(0.8), y, Inches(0.75), Inches(0.9), [[(n,26,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    card(s, Inches(1.7), y, Inches(10.95), Inches(0.9), CARD)
    text(s, Inches(2.0), y+Inches(0.12), Inches(3.4), Inches(0.7), [[(t,14,c,True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(5.35), y+Inches(0.1), Inches(7.1), Inches(0.72), [[(d,11.8,INK)]],
         anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
footer(s, "AASM 2025 지침 · 문헌고찰 종합 결론(치료 사다리)")

# ============================================================ SLIDE 26 — 근거 요약표
s = slide()
header(s, "근거 요약표 — RLS 치료", eyebrow="종합 · 근거표", tag="요약")
rows = [("영역","대표 문헌","설계","핵심 결과"),
        ("IV 철분","Earley 2024","다기관 RCT n=209","42일 IRLS·CGI 개선"),
        ("IV 철분","메타분석 2024","SR/MA 537명","효과·안전 확인"),
        ("α2δ 리간드","Allen 2014","RCT n=719","augmentation 1.7% vs 9.0%"),
        ("도파민제","Winkelman 2006","RCT n=344","단기 IRLS 개선(장기 augmentation)"),
        ("dipyridamole","Garcia-Borreguero 2021","교차 RCT","IRLS 24.1 → 11.1"),
        ("보툴리눔","Mittal 2018","교차 RCT n=24","4·6주 IRLS·VAS 개선(소표본)"),
        ("비골신경 자극","Charlesworth 2023","sham 대조","증상 개선·수면 무방해"),
        ("ESWT","—","RLS 표적 연구 없음","직접 근거 없음")]
table(s, Inches(0.8), Inches(1.5), Inches(11.85), rows,
      [Inches(2.5), Inches(3.1), Inches(2.85), Inches(3.4)], size=11, row_h=Inches(0.5), head_size=11.5)
footer(s, "02_RLS 참고문헌 근거 요약표 · PubMed 대조")

# ============================================================ SLIDE 27 — 핵심 메시지
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, Inches(0.22), SH, TEAL)
text(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(0.6), [[("핵심 메시지",13,MINT,True)]])
text(s, Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.8),
     [[("철분 교정이 기반, α2δ 리간드가 1차 — 도파민제는 후순위",23,WHITE,True)]])
msgs = [
    ("병태생리","뇌 국소 철분 결핍 → 도파민·아데노신 신호 이상. 유전·이차요인이 악화."),
    ("진단·감별","IRLSSG 5기준(움직임 충동·안정 시 악화·움직이면 완화·저녁 악화·mimic 배제). NLC와 감별."),
    ("기반·1차","철분 교정(경구≤75/정맥≤100)이 기반, α2δ 리간드가 1차 강한 권고."),
    ("주사·비약물","IV 철분(FCM)이 근거 최강. 보툴리눔·정맥경화는 표현형·연구단계. 비약물은 비골신경 자극."),
    ("주의","도파민제는 augmentation로 장기 후순위. ESWT는 RLS 근거 없음 — 근거를 창작하지 않는다.")]
for i,(t,d) in enumerate(msgs):
    y = Inches(2.35 + i*0.92)
    rect(s, Inches(0.9), y+Inches(0.04), Inches(0.16), Inches(0.66), TEAL)
    text(s, Inches(1.25), y, Inches(3.0), Inches(0.8), [[(t,14.5,MINT,True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(4.3), y, Inches(8.3), Inches(0.8), [[(d,13,WHITE)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.06)

# ============================================================ SLIDES 28-29 — 참고문헌
def ref_slide(title, refs):
    s = slide()
    header(s, title, eyebrow="참고문헌", tag="References")
    half = (len(refs)+1)//2
    for col,chunk in enumerate([refs[:half], refs[half:]]):
        x = Inches(0.8 + col*6.0)
        text(s, x, Inches(1.5), Inches(5.75), Inches(5.3),
             [{'runs':[(r, 10.5, INK)], 'space_after':7, 'ls':1.06} for r in chunk])
    footer(s, "PubMed/PMC 대조 검증 — RLS 표적 ESWT 임상연구는 확인되지 않아 '직접 근거 없음'으로 명시")
    return s

refs1 = [
 "Allen RP, et al. RLS/WED diagnostic criteria: updated IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73. PMID 25023924.",
 "Winkelman JW, et al. Treatment of RLS/PLMD: AASM clinical practice guideline. J Clin Sleep Med. 2025;21(1):137-52. PMID 39324694.",
 "Allen RP, et al. IRLSSG task force: iron treatment of RLS/WED. Sleep Med. 2018;41:27-44. PMID 29425576.",
 "Earley CJ, et al. IV ferric carboxymaltose for RLS: multicenter RCT. Sleep. 2024;47(7):zsae095. PMID 38625730.",
 "Clinical efficacy and safety of IV ferric carboxymaltose in RLS: meta-analysis of 537 patients. Sleep Med. 2024. PMID 39326219.",
 "Mittal SO, et al. Botulinum toxin in RLS: double-blind placebo-controlled crossover study. Toxins (Basel). 2018;10(10):401. PMC6215171.",
 "Effectiveness and safety of botulinum toxin type A in RLS: systematic review & meta-analysis. Healthcare (Basel). 2021;9(11):1538. PMC8623507.",
 "Pyne R, et al. Varicose veins with RLS and nocturnal leg cramps. J Vasc Interv Radiol. 2023;34(4):534-42. PMID 36526075.",
]
ref_slide("참고문헌 (1/2) — 진단 · 병태 · 철분 · 주사", refs1)

refs2 = [
 "Sundaresan S, et al. Treatment of leg veins for restless leg syndrome: retrospective review. Cureus. 2019;11(4):e4368. PMID 31192073.",
 "Charlesworth JD, et al. Bilateral high-frequency noninvasive peroneal nerve stimulation for RLS. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064.",
 "Allen RP, et al. Comparison of pregabalin with pramipexole for RLS. N Engl J Med. 2014;370(7):621-31. PMID 24521108.",
 "Winkelman JW, et al. Efficacy and safety of pramipexole in RLS. Neurology. 2006;67(6):1034-9. PMID 16931507.",
 "Winkelman JW, et al. Randomized polysomnography study of gabapentin enacarbil in RLS. Mov Disord. 2011;26(11):2065-72. PMID 21611981.",
 "Bogan RK, et al. Long-term maintenance treatment of RLS with gabapentin enacarbil: RCT. Mayo Clin Proc. 2010;85(6):512-21. PMID 20511481.",
 "Garcia-Borreguero D, et al. Dipyridamole for RLS: placebo-controlled crossover study. Mov Disord. 2021;36(10):2387-92. PMID 34137476.",
]
ref_slide("참고문헌 (2/2) — 비약물 · 경구약제 · 신규 표적", refs2)

out = "/home/user/ppt-work/하지불안증후군_치료_PPT.pptx"
prs.save(out)
print("saved:", out, "/", len(prs.slides._sldIdLst), "slides")
