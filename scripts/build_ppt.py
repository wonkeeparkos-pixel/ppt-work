# -*- coding: utf-8 -*-
"""야간 하지경련 치료 PPT 생성기. 문헌고찰(litreview) 근거 기반."""
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
    # east-asian font
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
    """runs: list of paragraphs; each paragraph is list of (txt,size,color,bold,italic) or dict."""
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
    """items: list of (level, text, [color], [bold]) ; level0 = •, level1 = –"""
    paras = []
    for it in items:
        lv = it[0]; tx = it[1]
        c = it[2] if len(it) > 2 and it[2] else color
        b = it[3] if len(it) > 3 else False
        mark = "" if lv < 0 else ("•  " if lv == 0 else "–  ")
        paras.append({'runs': [(mark + tx, size, c, b)], 'level': 0,
                      'space_after': gap, 'ls': 1.08,
                      'align': PP_ALIGN.LEFT})
    # indent for level1 by leading spaces handled via mark; add left pad per level
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

def tag_pill(s, x, y, label, color, tw=None):
    w = tw or Inches(0.3 + 0.1*len(label))
    rect(s, x, y, w, Inches(0.32), color, round_=True)
    text(s, x, y, w, Inches(0.32), [[(label, 10.5, WHITE, True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return w

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
# subtle accent block
rect(s, Inches(0.0), Inches(0.0), Inches(0.22), Inches(4.55), TEAL)
text(s, Inches(0.9), Inches(1.02), Inches(11.5), Inches(0.4),
     [[("고령 환자의 야간 하지경련 · 다리저림", 15, RGBColor(0xBF,0xD3,0xE6), True)]])
text(s, Inches(0.9), Inches(1.55), Inches(11.6), Inches(2.0),
     [[("효과가 입증된 치료 중심의", 33, WHITE, True)],
      [("근거 정리와 시술 기법", 33, WHITE, True)]], line_spacing=1.12)
text(s, Inches(0.9), Inches(3.5), Inches(11.5), Inches(0.55),
     [[("Nocturnal Leg Cramps in Older Adults — Evidence-based Injection · ESWT · Pharmacotherapy",
        13, RGBColor(0xAF,0xC6,0xDF), False, True)]])
text(s, Inches(0.9), Inches(4.95), Inches(11.5), Inches(1.2),
     [[("시술 순서: 보툴리눔(개요) → 주사 기법(상세) → 체외충격파(ESWT) → 약물 → 무효·비권고 → 기전상 타당(연구단계)",
        13.5, INK, True)],
      [("9개 항목 문헌고찰 기반 · 직접 근거와 인접 근거를 구분해 정리", 12.5, MUTE)]], space_after=6)
text(s, Inches(0.9), Inches(6.62), Inches(11.5), Inches(0.5),
     [[("교육·연구 참고용 문헌고찰. 개별 환자의 진료 결정은 담당 의사의 판단에 따릅니다.   |   작성 2026-07",
        11, MUTE, False, True)]])

# ============================================================ SLIDE 2 — 정의/유병률
s = slide()
header(s, "야간 하지경련(NLC)이란 무엇인가", eyebrow="배경 · 임상 문제", tag="배경")
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(5.2), [
    (0, "정의: 수면 중 종아리·발에 생기는 통증성 불수의 근수축. 만져지는 근경직이 있고 족배굴곡(발끝을 몸쪽으로)으로 완화된다.", INK, True),
    (0, "유병률: 50세 이상에서 흔함 — 경증 24~25%, 중등도~중증 약 6%(NHANES). 요추관협착증 동반 시 최대 65%까지 보고.", INK),
    (0, "결과: 수면 분절·각성으로 삶의 질 저하. '증상'이지 그 자체가 '진단'은 아니다.", INK),
    (0, "대부분 특발성이나, 고령에서는 이차성 원인(요추질환·신경병증·정맥부전·약물·전해질)이 흔하다.", INK),
    (1, "→ 치료 성패는 화려한 시술이 아니라 정확한 감별에서 갈린다.", TEALD, True),
], size=15, gap=12)
# right stat card
card(s, Inches(8.05), Inches(1.6), Inches(4.55), Inches(4.9))
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4),
     [[("핵심 수치", 13, TEALD, True)]])
for i,(num,lab) in enumerate([("24–25%","50세+ 경증 유병률"),
                              ("~6%","중등도–중증 유병률"),
                              ("최대 65%","요추관협착증 동반 시"),
                              ("수초–10분","경련 지속시간(+ 잔통)")]):
    yy = Inches(2.35 + i*1.0)
    text(s, Inches(8.35), yy, Inches(4.0), Inches(0.55),
         [[(num, 25, NAVY, True)]])
    text(s, Inches(8.35), yy+Inches(0.52), Inches(4.0), Inches(0.3),
         [[(lab, 12, MUTE)]])
footer(s, "Grandner & Winkelman 2017(PLoS One); Rabbitt 2016(Age Ageing); Handa 2022(IJGM)", 2)

# ============================================================ SLIDE 3 — 왜 감별 먼저
s = slide()
header(s, "왜 감별이 먼저인가 — 세 갈래 병태", eyebrow="진단 · 감별", tag="감별")
cols = [("야간 하지경련(NLC)", "수면 중 통증성 근수축\n만져지는 근경직(+)\n족배굴곡으로 완화\n종아리·발이 대부분", TEAL),
        ("하지불안증후군(RLS)", "'움직이고 싶은 충동'\n안정 시 악화·움직이면 완화\n통증보다 불쾌한 이상감각\n저녁~밤 뚜렷한 일주기", NAVY2),
        ("신경성 · 혈관성", "요추관협착·신경근병증\n말초신경병증(당뇨)\nPAD 허혈성 안정통·정맥부전\n'밤 다리증상'으로 위장", TEALD)]
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
     [[("임상 단서: ", 14, RED, True), ("환자가 pramipexole(미라펙스)·pregabalin(리리카)을 복용 중이라면 이는 전형적 RLS 치료제 → 실제 진단이 RLS(또는 NLC와 중복)일 가능성을 시사한다. ",14,INK)],
      [("IRLSSG 2014 기준은 진단 시 '다리경련(leg cramps)을 반드시 감별·배제'하도록 명문화하였다.", 13, MUTE, False, True)]],
     space_after=6)
footer(s, "IRLSSG 2014(Sleep Med); Hallegraeff 2017(BMC Fam Pract); 문헌고찰 서론", 3)

# ============================================================ SLIDE 4 — NLC vs RLS 표
s = slide()
header(s, "NLC vs RLS 상세 감별표", eyebrow="진단 · 감별", tag="감별")
rows = [("항목","야간 하지경련(NLC)","하지불안증후군(RLS)"),
        ("핵심 증상","통증성 근수축, 만져지는 근경직","움직이고 싶은 충동 + 이상감각"),
        ("주 증상","강한 통증","불편·안절부절(통증 아님)"),
        ("완화 방법","스트레칭·족배굴곡","걷기·움직임(멈추면 재발)"),
        ("만져지는 근경직","있음","없음"),
        ("일주기·가족력","야간·수면 초반 / 가족력 드묾","저녁~밤 악화 / 가족력 흔함"),
        ("1차 약물","(RLS약 아님) 비약물·개별 약물","α2δ 리간드 1차, 도파민제 신중")]
table(s, Inches(0.8), Inches(1.55), Inches(11.85), rows,
      [Inches(2.5), Inches(4.65), Inches(4.7)], size=12.5, row_h=Inches(0.62))
footer(s, "IRLSSG 2014; Hallegraeff 2017; AASM 지침 2025(J Clin Sleep Med)", 4)

# ============================================================ 이차 원인 감별·교정
s = slide()
header(s, "이차 원인 감별·교정 (원인 표적치료가 먼저)", eyebrow="진단 · 원인", tag="원인 교정", tag_color=TEALD)
rows = [("원인","임상 단서 · 감별","대응"),
        ("말초동맥질환(PAD)","파행·발냉감·맥박 약화·ABI 저하 (PAD 환자 ~75% 하지경련)","ABI·혈관평가·위험인자 관리"),
        ("요추관협착(LSS)","신경인성 파행·자세 의존성 증상","영상·재활, BTX/신경차단"),
        ("말초신경병증(당뇨)","저림·이상감각·야간 악화·감각 저하","혈당/HbA1c·신경학적 평가"),
        ("만성 정맥부전(CVI)","하지 부종·정맥류·오후 악화","압박스타킹·정맥 평가/치료"),
        ("갑상선기능저하","피로·서맥·건반사 지연","TSH"),
        ("전해질 이상·탈수","이뇨제·설사·신부전 (Na 저하 연관)","전해질·원인 교정"),
        ("약물 유발","이뇨제·statin·LABA·estrogen 등","원인 약물 검토·조정")]
table(s, Inches(0.8), Inches(1.5), Inches(11.85), rows,
      [Inches(3.0), Inches(5.55), Inches(3.3)], size=11.5, row_h=Inches(0.55), head_size=12)
footer(s, "Allen & Kirby 2012(AFP); Rabbitt 2016; Grandner & Winkelman 2017 (문헌고찰 Part 9-B)")

# ============================================================ 진단적 접근(workup)
s = slide()
header(s, "진단적 접근 — NLC는 '증상'이지 '진단'이 아니다", eyebrow="진단 · workup", tag="감별")
steps = [("병력","발생 시각·부위·지속시간, 이상감각 동반 여부, 파행 유무, 복용 약물, 투석·임신·간·갑상선·당뇨 병력",NAVY),
         ("진찰","하지 맥박·피부·부종·신경학적 검사, 건반사(patellar/achilles)",NAVY2),
         ("감별","RLS(움직임으로 완화)·간헐성 파행·근염·말초신경병증과 구분",TEAL),
         ("검사(선택적)","단서 있을 때만 — 전해질·신기능·TSH·혈당·ABI. 일상적 전해질 검사는 특발성에서 대개 정상·불필요",TEALD)]
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
     [[("요점: 병력·진찰로 대부분 감별 가능하며 광범위 검사는 대개 불필요. 특정 임상 단서가 있을 때만 표적 검사.",12.5,WHITE,True)]],
     anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Allen & Kirby 2012(AFP); Rabbitt 2016(Age Ageing)")

# ============================================================ SLIDE 5 — 근거 한눈에
s = slide()
header(s, "치료 근거 한눈에 — 무엇이 되고 무엇이 안 되나", eyebrow="총괄", tag="요약")
rows = [("치료","야간경련 직접 근거","근거수준","위치"),
        ("취침 전 스트레칭(비약물)","RCT(Hallegraeff 2012)","Level I~II","1차 · 최우선"),
        ("보툴리눔독소(비복근)","RCT 2편(Park 2017·Restivo 2018)","Level II","불응성 · 선택적"),
        ("국소마취제 유발점주사 / dry needling","소규모 RCT·관찰","Level III","MTrP 동반 시"),
        ("심비골신경 내측분지 차단","전향 비교 1편(Imura 2015)","Level III~IV","직접근거 · 선택적"),
        ("체외충격파(ESWT)","후향 1편+경직 RCT 다수","경직 I~II / 경련 III","보조 · 근거형성중"),
        ("약물(quinine·Vit B·diltiazem 등)","제한적(quinine은 효과·독성)","Level A~C","개별화"),
        ("마그네슘(특발성)","무효(Cochrane 2020)","—","권고 안 함"),
        ("혈관주위 스테로이드 / FGA / LSB","직접 근거 없음","Level V","비권고 · 연구단계")]
table(s, Inches(0.8), Inches(1.5), Inches(11.85), rows,
      [Inches(4.5), Inches(3.55), Inches(2.1), Inches(1.7)], size=11.5, row_h=Inches(0.5), head_size=12)
footer(s, "문헌고찰 9개 항목 근거 요약표 종합", 5)

# ============================================================ SLIDE 6 — 스트레칭
s = slide()
header(s, "1차·최고 근거: 취침 전 스트레칭", eyebrow="비약물 · 모든 환자", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.2), [
    (0,"Hallegraeff 2012 RCT (55세+ 80명, 은닉배정·ITT): 매일 취침 직전 종아리(비복근·가자미근)+햄스트링 스트레칭 6주.",INK,True),
    (1,"경련 빈도 감소 —평균차 1.2회/야간 (95% CI 0.6–1.8)",GREEN,True),
    (1,"경련 강도 감소 —평균차 1.3 cm VAS (95% CI 0.9–1.7)",GREEN,True),
    (0,"처방 예: 벽 밀기 자세 종아리 스트레칭 10–30초 × 2–3회, 취침 전 및 낮 시간 반복.",INK),
    (0,"급성 발작: 발을 발등 쪽으로 굽혀(dorsiflexion) 수동 신장, 걷기·마사지로 즉시 완화.",INK),
    (0,"자세·환경: 이불을 발 위로 팽팽히 덮지 않기, 발끝 중립 유지, 온열·수분.",INK),
    (-1,"근거는 혼재하나(일부 연구 효과 미미) 위험이 거의 없고 무비용 → 모든 고령 NLC 환자의 1차.",TEALD,True),
], size=14, gap=9)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("왜 스트레칭인가 (기전)",13,RGBColor(0xBF,0xD3,0xE6),True)]])
text(s, Inches(8.4), Inches(2.5), Inches(3.95), Inches(3.8),
     [[("경련은 근육이 '단축된' 위치에서 거의 배타적으로 발생한다.",13.5,WHITE)],
      [("단축 시 골지건기관(GTO)의 억제가 약해지고 운동종판 흥분 역치가 낮아진다.",13.5,WHITE)],
      [("신전(stretch)·건 자극은 Ib 구심성을 통해 경련을 반사적으로 억제한다 (Khan & Burne 2007).",13.5,WHITE)],
      [("→ 스트레칭이 이 반사 회로를 직접 겨냥한다.",13.5,RGBColor(0x9F,0xE0,0xD8),True)]],
     space_after=12, line_spacing=1.12)
footer(s, "Hallegraeff 2012(J Physiother); Khan & Burne 2007(J Neurophysiol); Allen & Kirby 2012", 6)

# ============================================================ SLIDE 7 — 유발약물
s = slide()
header(s, "원인 교정: 경련 유발 약물 검토", eyebrow="원인 교정 · 우선", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(6.7), Inches(5.0), [
    (0,"Garrison 2012(Arch Intern Med): 처방-대칭 분석으로 경련과 연관된 약물을 규명.",INK,True),
    (0,"흔한 이차 원인도 함께 감별·교정: PAD·요추관협착·신경병증·정맥부전·갑상선저하·전해질 이상.",INK),
    (0,"저림·이상감각 동반 시 carnitine 결핍·신경병증 등 추가 감별.",INK),
    (-1,"실무: 임상적으로 가능하면 대체·감량·투여시각 조정을 주치의와 검토.",TEALD,True),
], size=14, gap=10)
rows = [("유발 연관 약물","보정 연관비(sequence ratio)"),
        ("지속형 β2-작용제(LABA)","2.42  (가장 강한 연관)"),
        ("칼륨보존형 이뇨제","2.12"),
        ("Thiazide-유사 이뇨제","1.48"),
        ("Loop 이뇨제","1.20"),
        ("Statin","1.16  (약한 연관)")]
table(s, Inches(7.75), Inches(1.55), Inches(4.85), rows,
      [Inches(2.85), Inches(2.0)], size=12.5, row_h=Inches(0.52), align_first_left=True)
footer(s, "Garrison 2012 (sequence symmetry analysis, Arch Intern Med)", 7)

# ============================================================ 주사 지형 개요
s = slide()
header(s, "주사 치료 지형 — 무엇을 어디에 놓나", eyebrow="주사 · 개요", tag="주사")
text(s, Inches(0.8), Inches(1.4), Inches(11.8), Inches(0.5),
     [[("요청에 따라 보툴리눔은 개요(1페이지)로, 나머지 주사 기법은 논문 근거로 상세히 다룬다. 순서: BTX → 유발점 국소마취제 → dry needling → 신경차단.",12.5,MUTE,False,True)]])
inj = [("① 보툴리눔독소(BTX)","비복근 근육내","RCT 2편(Park·Restivo)","Level II",GREEN,"개요(1p)"),
       ("② 국소마취제 유발점주사","비복근 MTrP","소규모 RCT·관찰","Level III",TEAL,"상세"),
       ("③ Dry needling(건침)","비복근 MTrP","RCT·증례","Level III",TEAL,"상세"),
       ("④ 심비골신경 내측분지 차단","제1–2 중족골 간극","전향 비교(Imura 2015)","Level III~IV",NAVY2,"상세·직접근거"),
       ("(연구단계) FGA·신경간 차단","원위 MTJ 등","직접 근거 없음","Level V",MUTE,"뒤에서")]
rows = [("주사","표적","근거","수준","다룸")]
for t,tgt,ev,lv,c,how in inj:
    rows.append((t,tgt,ev,lv,how))
# render as table with color accent on first col via table then overlay bars
table(s, Inches(0.8), Inches(2.15), Inches(11.85),
      [("주사","표적","근거","근거수준","이 발표에서")] + [(t,tgt,ev,lv,how) for (t,tgt,ev,lv,c,how) in inj],
      [Inches(3.7), Inches(2.6), Inches(2.7), Inches(1.5), Inches(1.35)],
      size=11.5, row_h=Inches(0.62), head_size=12)
text(s, Inches(0.8), Inches(6.55), Inches(11.8), Inches(0.4),
     [[("모두 1차 치료가 아니다 — 비약물·원인교정 이후, 불응성·특정 표현형(MTrP·LSS·신경병증)에서 선택적으로 적용.",12,TEALD,True)]])
footer(s, "Park 2017; Restivo 2018; Kim 2015; Temel 2023; Imura 2015 종합")

# ============================================================ SLIDE 8 — 보툴리눔 1페이지
s = slide()
header(s, "주사 ① 보툴리눔독소(BTX) — 요약", eyebrow="주사 · 개요(1페이지)", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(4.4), [
    (0,"Park 2017 RCT(핵심): 요추관협착증 + 주1회↑ 야간 종아리경련 50명. 비복근 BTX-A vs gabapentin(평균 643mg).",INK,True),
    (1,"모든 추적시점(2주·1·3개월)에서 다리통증·경련 빈도·강도가 gabapentin 대비 유의 감소(P<0.01), 불면·기능 개선.",GREEN),
    (1,"BTX군 중대 합병증 없음 / gabapentin군 33% 전신 부작용.",INK),
    (0,"Restivo 2018 RCT(당뇨병성 신경병증): BTX-A(30~100U)가 위약 대비 경련 빈도·강도·역치 개선, 1주부터 16주 지속.",INK),
    (0,"기전: 신경근접합부 ACh 유리 억제 → 방추내·외 종판 입출력 감소, 근력은 상대 보존하며 경련만 감소.",INK),
], size=13.5, gap=9)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("실무 요점",13,TEALD,True)]])
bullets(s, Inches(8.35), Inches(2.35), Inches(4.0), Inches(4.0), [
    (0,"주사 계열 중 근거수준 최고(Level II RCT).",INK,True),
    (0,"효과 ~3개월 지속 → 반복 주사 필요, 고가.",INK),
    (0,"비복근은 보행 주근육 — 용량의존 근력약화·낙상 위험(고령) 고지.",RED),
    (0,"대상은 LSS·신경병증 등 특정군 — 일반 특발성 대규모 RCT는 부족.",INK),
    (-1,"위치: 불응성·특정 표현형에 선택적.",TEALD,True),
], size=12.5, gap=8)
footer(s, "Park 2017(Arch Phys Med Rehabil, NCT02444351); Restivo 2018(Ann Neurol); Bertolasi 1997", 8)

# ============================================================ SLIDE 9 — 유발점주사 개요
s = slide()
header(s, "주사 ② 국소마취제 유발점·근육내 주사 — 개념", eyebrow="주사 기법(상세)", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(11.8), Inches(2.4), [
    (0,"개념: 야간 종아리경련은 비복근 근막통증유발점(MTrP)과 연관될 수 있다. 유발점에 소량 국소마취제를 주사하면 ① 국소 근이완 ② 유발점 비활성화 ③ 구심성 되먹임 차단으로 경련이 완화된다.",INK),
    (0,"적응: 보존치료 불응 + 비복근 유발점(taut band·압통)이 뚜렷한 환자. 저침습·저비용 옵션.",INK,True),
], size=14, gap=10)
# two study cards
for i,(t,lines,c) in enumerate([
    ("Prateepavanich 1999 (무작위, n=24)",
     ["xylocaine(lidocaine) 유발점 주사 vs 경구 quinine 300mg","두 군 모두 빈도·지속·강도 유의 감소",
      "치료 종료 4주 후 추적에서 주사군이 대부분 지표 우월(지속효과)"], TEAL),
    ("Kim 2015 (전향 관찰, n=12, 평균 63세)",
     ["0.25% lidocaine 1–2 mL를 비복근 유발점에 주사","NRS·경련 빈도·불면지수(ISI) 모두 유의 개선(P<0.01)",
      "임상적 불면 10명 → 4주째 1명으로 감소"], NAVY2)]):
    x = Inches(0.8 + i*6.0)
    card(s, x, Inches(4.05), Inches(5.75), Inches(2.55), WHITE, LINE)
    rect(s, x, Inches(4.05), Inches(0.12), Inches(2.55), c)
    text(s, x+Inches(0.32), Inches(4.25), Inches(5.3), Inches(0.4), [[(t,13.5,c,True)]])
    text(s, x+Inches(0.32), Inches(4.75), Inches(5.25), Inches(1.7),
         [[("•  "+ln,12.5,INK)] for ln in lines], space_after=7, line_spacing=1.08)
footer(s, "Prateepavanich 1999(J Med Assoc Thai); Kim 2015(J Am Board Fam Med)", 9)

# ============================================================ SLIDE 10 — 유발점주사 기법
s = slide()
header(s, "주사 ② 기법 상세 — 유발점 국소마취제 주사", eyebrow="주사 기법(상세)", tag="기법", tag_color=TEALD)
rows = [("항목","Kim 2015 프로토콜"),
        ("표적","비복근 근막통증유발점(taut band 내 최대 압통점)"),
        ("약제·용량","0.25% lidocaine 1–2 mL / 유발점"),
        ("바늘·각도","25 G, 피부에서 약 30° 접근"),
        ("횟수","주 1회 · 1~4주 추적"),
        ("결과지표","NRS · 경련 빈도 · 불면지수(ISI) 유의 개선"),
        ("보조 원칙","급성 경련 시 소량 국소마취제로 국소 이완 + 유발점 비활성화")]
table(s, Inches(0.8), Inches(1.5), Inches(7.2), rows,
      [Inches(1.9), Inches(5.3)], size=12.5, row_h=Inches(0.56))
card(s, Inches(8.3), Inches(1.55), Inches(4.3), Inches(5.0), CARD)
text(s, Inches(8.55), Inches(1.8), Inches(3.8), Inches(0.4), [[("포인트 · 주의",13,TEALD,True)]])
bullets(s, Inches(8.55), Inches(2.3), Inches(3.85), Inches(4.1), [
    (0,"바늘 기계적 자극 효과도 완화에 기여(dry needling과 공유).",INK),
    (0,"quinine과 대등하거나 지속효과 면에서 우월(Prateepavanich).",GREEN),
    (0,"근거는 소표본·위약대조 부족 → Level III.",INK),
    (0,"항응고·항혈소판제 복용 고령자: 출혈·혈종 주의.",RED),
    (0,"무균술 · 혈관내 주입 회피(흡인 확인).",INK),
], size=12.5, gap=10)
footer(s, "Kim 2015(J Am Board Fam Med); Prateepavanich 1999(J Med Assoc Thai)", 10)

# ============================================================ SLIDE 11 — dry needling
s = slide()
header(s, "주사 ③ 건침(Dry Needling) — 기법·근거", eyebrow="주사 기법(상세)", tag="효과 있음", tag_color=GREEN)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"Temel 2023 RCT(n=42): 스트레칭 단독 vs 스트레칭 + 비복근 유발점 dry needling.",INK,True),
    (1,"두 군 모두 경련 횟수 유의 감소(P<0.001).",INK),
    (1,"DN 병용군이 3개월 추적 경련 횟수(P=0.016)·강도·압력통증역치·수면질(PSQI)에서 우월.",GREEN,True),
    (0,"Bagcier 2021 증례: 마그네슘·스트레칭 불응 환자에 주1회 3회기 DN + 스트레칭.",INK),
    (1,"경련 지속 60초→10초, 통증 VAS 8→1, 빈도 '매일'→'주간'으로 개선.",GREEN),
    (0,"기전: 약물 없이 바늘의 기계적 자극으로 국소연축반응 유도·소실, taut band 이완, 압력통증역치 상승.",INK),
    (-1,"저침습·저비용·무약물. 근거는 소규모 RCT·증례(Level III~).",TEALD,True),
], size=13.5, gap=9)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), NAVY)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("기법 요약",13,RGBColor(0xBF,0xD3,0xE6),True)]])
bullets(s, Inches(8.4), Inches(2.45), Inches(3.95), Inches(3.9), [
    (0,"표적: 비복근 근막통증유발점.",WHITE),
    (0,"방식: 유발점 직접 자침, 국소연축반응 유도.",WHITE),
    (0,"빈도: 주 1회 × 약 3회기.",WHITE),
    (0,"병용: 스트레칭과 함께 시행 시 단·중기 효과 우월.",RGBColor(0x9F,0xE0,0xD8),True),
    (0,"안전: 경미한 출혈·압통 외 중대 이상반응 없음. 초음파 유도 권장.",WHITE),
], size=12.5, gap=11)
footer(s, "Temel 2023(Turk J Osteoporos); Bagcier 2021(J Am Board Fam Med)", 11)

# ============================================================ SLIDE 12 — Imura 신경차단 (핵심 직접근거)
s = slide()
header(s, "주사 ④ 심비골신경 내측분지 차단 — 핵심 직접근거", eyebrow="주사 기법(상세) · 직접 근거", tag="직접 근거", tag_color=TEAL)
bullets(s, Inches(0.8), Inches(1.5), Inches(6.8), Inches(2.6), [
    (0,"Imura 2015: 야간경련에 말초 운동신경가지를 직접 표적한, 현재 확인 가능한 유일한 전향적 비교연구.",INK,True),
    (0,"대상: 요추수술(감압술) 후 야간경련이 지속된 66명(차단군 41 vs 대조 25), 평균 60.9세.",INK),
], size=13.5, gap=9)
# technique box
card(s, Inches(0.8), Inches(4.05), Inches(6.55), Inches(2.55), CARD)
text(s, Inches(1.05), Inches(4.25), Inches(6.0), Inches(0.4), [[("주사 기법",13,TEALD,True)]])
bullets(s, Inches(1.05), Inches(4.75), Inches(6.0), Inches(1.7), [
    (0,"표적: 제1–2 중족골 사이 간극의 원위 2/3 지점, 심비골신경 내측가지.",INK),
    (0,"약제: 1.0% lidocaine 5.0 mL (에피네프린 무첨가).",INK),
    (0,"깊이: 1.0–1.5 cm에 서서히 주입.",INK),
], size=12.5, gap=8)
# results box
card(s, Inches(7.6), Inches(1.55), Inches(5.0), Inches(5.05), WHITE, LINE)
rect(s, Inches(7.6), Inches(1.55), Inches(5.0), Inches(0.62), TEAL, round_=True)
text(s, Inches(7.6), Inches(1.55), Inches(5.0), Inches(0.62), [[("결과 (2주 시점)",13.5,WHITE,True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, Inches(7.9), Inches(2.4), Inches(4.5), Inches(4.0), [
    (0,"경련 빈도 1/4 미만으로 감소: 차단군 61.0% vs 대조 20.0%",GREEN,True),
    (0,"1/2 미만으로 감소: 80.5% vs ~28% (P<0.01)",GREEN),
    (0,"경련 강도 감소: 63.4% vs 8.0% (P<0.05)",GREEN),
    (0,"지속: 12주 이상 63.4%, 부작용 41명 전원 없음.",INK),
    (0,"성격상 감각가지 → 구심성 입력 차단으로 되먹임고리 억제로 해석.",MUTE),
    (0,"한계: 요추수술 후 특수집단, 비무작위(Level III~IV).",MUTE),
], size=12.5, gap=9)
footer(s, "Imura 2015 (Brain Behav; PMID 26445706)", 12)

# ============================================================ SLIDE 13 — 주사 기전·안전성
s = slide()
header(s, "주사 치료의 기전과 안전성 총괄", eyebrow="주사 · 종합", tag="안전성")
# mechanism mini-diagram
card(s, Inches(0.8), Inches(1.55), Inches(11.85), Inches(1.75), CARD)
text(s, Inches(1.05), Inches(1.72), Inches(11), Inches(0.35), [[("진성 근경련 = 운동신경(축삭 종말·척수 운동뉴런)의 폭발적 과흥분 (Minetto 2011; Miller-Layzer 2005)",13.5,NAVY,True)]])
steps = ["단축·피로한\n근육","α-운동뉴런\n과흥분·고빈도 방전","되먹임 루프\n(Ia↑ / Ib억제↓)","경련"]
for i,st in enumerate(steps):
    x = Inches(1.15 + i*2.75)
    rect(s, x, Inches(2.25), Inches(2.3), Inches(0.82), NAVY2, round_=True)
    text(s, x, Inches(2.25), Inches(2.3), Inches(0.82), [[(ln,11.5,WHITE,True)] for ln in st.split("\n")],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, space_after=0, line_spacing=1.0)
    if i < 3:
        text(s, x+Inches(2.32), Inches(2.25), Inches(0.4), Inches(0.82), [[("▶",15,TEAL,True)]],
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# how injections break the loop + safety
card(s, Inches(0.8), Inches(3.55), Inches(5.85), Inches(3.05), WHITE, LINE)
text(s, Inches(1.05), Inches(3.75), Inches(5.4), Inches(0.4), [[("주사는 이 고리를 어떻게 끊는가",13,TEALD,True)]])
bullets(s, Inches(1.05), Inches(4.25), Inches(5.3), Inches(2.2), [
    (0,"국소마취제: Na 통로 차단 → 구심·원심 신호 일시 차단.",INK),
    (0,"BTX-A: NMJ ACh 유리 억제 → 수주~수개월 화학적 탈신경.",INK),
    (0,"Dry needling: 유발점 비활성화·되먹임 차단.",INK),
], size=12.5, gap=9)
card(s, Inches(6.8), Inches(3.55), Inches(5.85), Inches(3.05), WHITE, LINE)
text(s, Inches(7.05), Inches(3.75), Inches(5.4), Inches(0.4), [[("고령 환자 안전 체크",13,RED,True)]])
bullets(s, Inches(7.05), Inches(4.25), Inches(5.3), Inches(2.2), [
    (0,"경골신경 표적 → 족저굴곡 약화 / 총비골신경 → 족하수 → 낙상.",RED),
    (0,"BTX 용량의존 근력약화, 항응고제 복용 시 출혈·혈종.",INK),
    (0,"역설적 경련 유발 사례도 보고(Ritt 2023).",INK),
    (0,"무균술·초음파 유도·혈관내 주입 회피.",INK),
], size=12.5, gap=8)
footer(s, "Minetto 2011(J Physiol); Miller & Layzer 2005(Muscle Nerve); Ritt 2023", 13)

# ============================================================ SLIDE 14 — ESWT 개요/직접근거
s = slide()
header(s, "체외충격파(ESWT) — 경련 직접 근거", eyebrow="충격파 · ESWT", tag="근거 형성중", tag_color=AMBER)
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(3.0), [
    (0,"Li 2021(후향, n=126): 요추퇴행성질환 동반 하지경련. ESWT군 78 vs 대조 물리치료 44, 평균 62.3세.",INK,True),
    (0,"프로토콜: 2,000 shocks/session, 8–10/sec, 2일 간격, 총 4주.",INK),
    (0,"경련을 '직접' 평가한 유일한 임상연구이나 후향·비무작위(Level III~IV).",MUTE),
    (0,"특발성 NLC만을 표적한 ESWT RCT는 아직 없음(직접 근거 공백).",RED),
], size=13.5, gap=10)
# results numbers
card(s, Inches(8.05), Inches(1.55), Inches(4.55), Inches(4.95), NAVY)
text(s, Inches(8.35), Inches(1.8), Inches(4.0), Inches(0.4), [[("Li 2021 결과 (ESWT군)",13,RGBColor(0xBF,0xD3,0xE6),True)]])
for i,(a,b) in enumerate([("경련 빈도","5.7 → 1.3 회/시간"),
                          ("경련 지속","57.6 → 10.6 초"),
                          ("통증(VAS)","7.6 → 1.7"),
                          ("대조군 대비","모두 P<0.001")]):
    yy = Inches(2.4 + i*1.0)
    text(s, Inches(8.35), yy, Inches(4.0), Inches(0.3), [[(a,12,RGBColor(0x9F,0xB8,0xD6),True)]])
    text(s, Inches(8.35), yy+Inches(0.28), Inches(4.0), Inches(0.5), [[(b,19,WHITE,True)]])
footer(s, "Li 2021 (Biomed Res Int; PMID 34734084)", 14)

# ============================================================ SLIDE 15 — ESWT 인접근거
s = slide()
header(s, "ESWT — 인접 근거(종아리 경직): 강한 편", eyebrow="충격파 · ESWT", tag="인접 근거", tag_color=TEAL)
bullets(s, Inches(0.8), Inches(1.5), Inches(11.8), Inches(1.3), [
    (0,"경직(spasticity)≠경련이나, 둘 다 불수의 근수축·근긴장 항진을 공유하고 표적 부위(비복근·가자미근)가 같아 기전상 가장 근접한 인접 근거.",INK),
], size=13.5, gap=8)
rows = [("연구","설계","핵심 결과"),
        ("Otero-Luis 2024 (SR/MA, 16 RCT)","메타분석","하지 MAS 평균차 −0.40; 즉시 최대, 12주까지 유지"),
        ("Mihai 2020 (SR/MA, 7 RCT)","메타분석","하지 후유증 경직 SMD 0.53, 12주 지속"),
        ("Yang 2024 (뇌졸중, n=39)","용량-반응 RCT","고용량(4,000 pulses)군 24주 MAS 개선"),
        ("Park 2015 (뇌성마비 소아)","pilot RCT","3회군이 1회군보다 MAS·ROM 유지 우수(세션수 의존)"),
        ("Özbek 2025 (SWE 객관화)","RCT","근경직 stiffness·MAS 감소(단, 원논문 표적은 상지)")]
table(s, Inches(0.8), Inches(2.95), Inches(11.85), rows,
      [Inches(3.9), Inches(2.5), Inches(5.45)], size=11.5, row_h=Inches(0.56), head_size=12)
text(s, Inches(0.8), Inches(6.5), Inches(11.8), Inches(0.4),
     [[("소결: 종아리 근긴장·SWE stiffness의 단기 감소는 RCT·메타분석(Level I~II)로 비교적 견고 → '근긴장 완화'라는 경련 치료 표적과 맞닿음.",12,TEALD,True)]])
footer(s, "Otero-Luis 2024·Mihai 2020·Yang 2024·Park 2015·Özbek 2025 (J Clin Med 등)", 15)

# ============================================================ SLIDE 16 — ESWT 기전
s = slide()
header(s, "ESWT 작용 기전 — 왜 근긴장이 낮아지나", eyebrow="충격파 · ESWT", tag="기전")
mechs = [("① Nitric Oxide↑","eNOS 인산화 → NO 증가. 신경전달 조절·항염(NF-κB 억제)·신생혈관형성."),
         ("② 신경근접합부(NMJ)","ACh 수용체 변성, CMAP 진폭 감소가 6–8주 지속 → 근긴장 완화."),
         ("③ 운동신경원 흥분성↓","건 압력 자극을 통한 반사 흥분성 저하(α-motor neuron)."),
         ("④ 유변학적·기계적","mechanotransduction으로 조직 재형성, 근경직 stiffness 감소."),
         ("⑤ 미세순환 개선","국소 혈류·조직 관류 증가 → 대사성 기능이상 회복.")]
for i,(t,d) in enumerate(mechs):
    col = i % 2; row = i // 2
    x = Inches(0.8 + col*6.0); y = Inches(1.55 + row*1.32)
    if i == 4:
        x = Inches(0.8 + 3.0)  # center last one
    card(s, x, y, Inches(5.75), Inches(1.16), CARD)
    rect(s, x, y, Inches(0.11), Inches(1.16), TEAL)
    text(s, x+Inches(0.3), y+Inches(0.14), Inches(5.3), Inches(0.4), [[(t,13.5,NAVY,True)]])
    text(s, x+Inches(0.3), y+Inches(0.56), Inches(5.35), Inches(0.55), [[(d,12,INK)]], line_spacing=1.05)
text(s, Inches(0.8), Inches(6.7), Inches(11.8), Inches(0.4),
     [[("야간경련 병태(운동신경원 과흥분·근방추 감작·국소순환 저하)와 개념적으로 중첩 → 경련 역치를 높일 생물학적 타당성(가설).",11.5,TEALD,True)]])
footer(s, "Yang 2021 (J Clin Med, ESWT 기전 리뷰)", 16)

# ============================================================ SLIDE 17 — ESWT 프로토콜
s = slide()
header(s, "ESWT 대표 프로토콜 (종아리 표적)", eyebrow="충격파 · ESWT", tag="기법", tag_color=TEALD)
rows = [("파라미터","대표 범위"),
        ("유형","Radial(rESWT) 다용 / 심부·정밀엔 Focused"),
        ("압력·에너지","Radial 1.5–2.5 bar / Focused ~0.10 mJ/mm²"),
        ("충격수","2,000–3,000 pulses / 근육 (비복근+가자미근 각 2,000)"),
        ("주파수","4–15 Hz (경직 4–10, MPS 12–15)"),
        ("세션","주 1~2회, 총 3–6회(2–4주) — 효과 세션수 의존"),
        ("표적","비복근 내·외측두·가자미근 운동점 (초음파 유도 권장)"),
        ("효과 지속","즉시~12주 단기 (이후 소실 경향)")]
table(s, Inches(0.8), Inches(1.5), Inches(7.6), rows,
      [Inches(2.3), Inches(5.3)], size=12, row_h=Inches(0.5))
card(s, Inches(8.7), Inches(1.55), Inches(3.9), Inches(5.0), CARD)
text(s, Inches(8.95), Inches(1.8), Inches(3.4), Inches(0.4), [[("안전 · 금기",13,RED,True)]])
bullets(s, Inches(8.95), Inches(2.3), Inches(3.45), Inches(4.0), [
    (0,"전반적으로 안전 — 일시적 국소 통증·발적 정도.",INK),
    (0,"상대 금기: 항응고제, 심부정맥혈전, 감염부위, 악성종양 부위, 임신.",RED),
    (0,"비침습 → quinine 등 약물 부작용 회피가 필요한 고령에 매력적.",GREEN),
    (-1,"위치: 표준치료 아님. 보조·실험적.",TEALD,True),
], size=12, gap=10)
footer(s, "문헌고찰 Part 3 프로토콜 종합 (Yang 2024·Di Giovanni 2026 등)", 17)

# ============================================================ SLIDE 18 — ESWT 한계
s = slide()
header(s, "ESWT — 근거 수준과 한계(정직한 평가)", eyebrow="충격파 · ESWT", tag="한계")
bullets(s, Inches(0.8), Inches(1.55), Inches(11.8), Inches(4.6), [
    (0,"직접 근거 공백: 특발성 야간경련에 대한 ESWT의 RCT·전향연구·증례는 아직 없음. Li 2021은 요추질환 이차성 경련의 후향 자료.",RED,True),
    (0,"경직 ≠ 경련: 인접 근거의 대상은 상위운동신경원 병변의 경직으로, 병태생리가 다르다(개념적 외삽).",INK),
    (0,"단기·소규모: 인접 근거 효과는 대부분 12주 이내, 표본 <50명, 프로토콜 이질성 큼.",INK),
    (0,"MPS 근거는 방향 불일치: 최근 이중맹검 위약대조에서 위약 대비 우월성 없음(비특이 효과 가능성).",INK),
    (-1,"종합: 생물학적 타당성은 높지만 직접 근거는 매우 제한적 → 난치성·약물부작용 회피가 필요한 환자의 보조요법으로 시도, 표적 RCT 필요.",TEALD,True),
], size=14.5, gap=14)
footer(s, "문헌고찰 Part 3 (D) 한계 종합", 18)

# ============================================================ SLIDE 19 — 약제 개관
s = slide()
header(s, "약물 치료 개관 — 근거는 전반적으로 약하다", eyebrow="약제 · 개관", tag="약제")
bullets(s, Inches(0.8), Inches(1.5), Inches(6.9), Inches(5.0), [
    (0,"AAN 근거기반 리뷰·Cochrane 종합: 일상적으로 권고할 만큼 근거가 강한 약제는 없다. 비약물 실패 시 위험/이득을 설명하고 개별화.",INK,True),
    (0,"두 축을 구분: NLC 특이 약물 vs RLS 약물(pramipexole/pregabalin).",INK),
    (0,"고령: 다약제·신기능·낙상·인지 위험을 고려해 감량·서서히 적정.",INK),
    (0,"NLC 약물 시험은 대개 취침 전 1회 투여 프로토콜.",INK),
], size=14, gap=11)
# grade legend
card(s, Inches(8.05), Inches(1.6), Inches(4.55), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("근거·권고 요지",13,TEALD,True)]])
data = [("Quinine","효과 O · 독성으로 일상 회피",RED),
        ("Vitamin B 복합","Level C · 안전, 시도가치",GREEN),
        ("Diltiazem 30mg","Level C · 소규모",AMBER),
        ("Naftidrofuryl","Level C",AMBER),
        ("Gabapentin/Baclofen","LSS 동반 시 제한적",AMBER),
        ("Magnesium(특발성)","무효(권고 안 함)",RED)]
for i,(a,b,c) in enumerate(data):
    yy = Inches(2.35 + i*0.68)
    rect(s, Inches(8.35), yy+Inches(0.05), Inches(0.16), Inches(0.4), c)
    text(s, Inches(8.62), yy, Inches(4.0), Inches(0.55),
         [[(a+"  ",13,NAVY,True),(b,11.5,MUTE)]], anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Katzberg 2010(AAN, Neurology); Allen & Kirby 2012(AFP)", 19)

# ============================================================ SLIDE 20 — quinine
s = slide()
header(s, "약물 ① Quinine — 효과 있으나 안전성 경고", eyebrow="약제", tag="주의", tag_color=RED)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"El-Tawil 2015 Cochrane(23개 시험): quinine(대개 취침 전 300mg)이 위약 대비 경련 빈도·강도·경련일수를 유의 감소(중등도 근거).",INK,True),
    (0,"AAN(Katzberg 2010): 'likely effective(Level A)'이나 독성 때문에 일상 사용은 피하고, 매우 불능화된 불응성에서만 개별 시도.",INK),
    (0,"FDA: 야간경련에 미승인. 혈소판감소증·혈전성혈소판감소성자반증(TTP) 등 치명적 혈액학적 반응 위험으로 경고·REMS 시행.",RED,True),
    (1,"FDA 유해사례(2005–2008) 중 quinine 중대사례의 ~66%가 야간경련 사용자.",INK),
    (-1,"결론: 최후 수단. 사용 시 부작용을 면밀히 감시할 수 있는 선별 환자에 한함.",TEALD,True),
], size=14, gap=12)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), RED)
text(s, Inches(8.4), Inches(2.0), Inches(3.9), Inches(0.5), [[("⚠ 안전성 요지",15,WHITE,True)]])
bullets(s, Inches(8.4), Inches(2.7), Inches(3.9), Inches(3.6), [
    (0,"혈소판감소증 · TTP/HUS",WHITE),
    (0,"QT 연장 · 중증 과민반응",WHITE),
    (0,"이명(tinnitus)",WHITE),
    (0,"FDA 반복 안전성 경고, 야간경련에 판매 제한.",WHITE),
], size=13.5, gap=13)
footer(s, "El-Tawil 2015(Cochrane CD005044); Katzberg 2010(AAN); FDA Qualaquin 경고", 20)

# ============================================================ SLIDE 21 — Vit B / diltiazem
s = slide()
header(s, "약물 ② 비교적 안전한 선택지", eyebrow="약제", tag="Level C")
cards_data = [
    ("Vitamin B 복합체", GREEN, [
        "Chan 1998 이중맹검 RCT(고혈압 고령 28명, 12주)",
        "fursulthiamine 50mg + hydroxocobalamin 250µg",
        "  + pyridoxal phosphate 30mg + riboflavin 5mg",
        "경련 빈도·강도·지속 유의 감소(치료군 86% 관해)",
        "AAN 'possibly effective(Level C)' · 안전성 양호"]),
    ("Diltiazem 30 mg", AMBER, [
        "Voon 2001 이중맹검 교차(n=13), 취침 시",
        "경련 횟수 5.8 → 0.16/2주 (P=0.04)",
        "강도는 불변 · 소규모",
        "AAN Level C · 저혈압 등 부작용 주의"]),
    ("Naftidrofuryl 300mg", AMBER, [
        "혈관확장제 · Young 1993 소규모(n=14)",
        "경련 감소 · AAN Level C",
        "국내 가용성 확인 필요"])]
xs = [Inches(0.8), Inches(4.85), Inches(8.9)]
for (t,c,lines),x in zip(cards_data, xs):
    card(s, x, Inches(1.55), Inches(3.75), Inches(5.0), WHITE, LINE)
    rect(s, x, Inches(1.55), Inches(3.75), Inches(0.62), c, round_=True)
    text(s, x, Inches(1.55), Inches(3.75), Inches(0.62), [[(t,13.5,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+Inches(0.28), Inches(2.4), Inches(3.25), Inches(4.0),
         [[("•  "+ln if not ln.startswith("  ") else ln, 12, INK)] for ln in lines],
         space_after=9, line_spacing=1.08)
footer(s, "Chan 1998(J Clin Pharmacol); Voon 2001(Age Ageing); Young 1993", 21)

# ============================================================ SLIDE 22 — Vit K2 / gabapentin·baclofen
s = slide()
header(s, "약물 ③ 최근·조건부 선택지", eyebrow="약제", tag="해석 주의", tag_color=AMBER)
card(s, Inches(0.8), Inches(1.55), Inches(5.85), Inches(4.95), WHITE, LINE)
rect(s, Inches(0.8), Inches(1.55), Inches(5.85), Inches(0.62), NAVY2, round_=True)
text(s, Inches(0.8), Inches(1.55), Inches(5.85), Inches(0.62), [[("Vitamin K2 (menaquinone-7)",13.5,WHITE,True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, Inches(1.1), Inches(2.45), Inches(5.3), Inches(4.0), [
    (0,"Tan 2024(JAMA Intern Med): 65세+ 199명, MK-7 180µg 8주.",INK),
    (0,"주간 경련 빈도 2.60 → 0.96로 유의 감소, 강도·지속 개선.",GREEN),
    (0,"⚠ 발표 후 '정정·교체 통지'(2025) — 결과 방향은 유지되나 데이터 정정.",RED,True),
    (-1,"확정적 근거로 과대해석 금지, 인용 시 정정 사실 명시.",TEALD,True),
], size=12.5, gap=11)
card(s, Inches(6.8), Inches(1.55), Inches(5.85), Inches(4.95), WHITE, LINE)
rect(s, Inches(6.8), Inches(1.55), Inches(5.85), Inches(0.62), TEALD, round_=True)
text(s, Inches(6.8), Inches(1.55), Inches(5.85), Inches(0.62), [[("Gabapentin · Baclofen (LSS 동반 시)",13.5,WHITE,True)]],
     align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
bullets(s, Inches(7.1), Inches(2.45), Inches(5.3), Inches(4.0), [
    (0,"NLC 특이 근거는 약함. gabapentin은 '고려 가능'(낮은 근거).",INK),
    (0,"Kim 2024 RCT: 요추관협착 동반 야간 종아리경련에서 baclofen ≈ gabapentin(유사 효능·안전).",INK),
    (0,"신경근 병변(요추질환) 연관 경련에서 제한적 역할.",INK),
    (0,"진정·어지럼 부작용, 고령 신중.",RED),
], size=12.5, gap=11)
footer(s, "Tan 2024(JAMA Intern Med; 정정통지 2025); Kim 2024(Am J Phys Med Rehabil)", 22)

# ============================================================ SLIDE 23 — RLS 약물 감별
s = slide()
header(s, "약물 ④ pramipexole·pregabalin은 'RLS 약'이다", eyebrow="약제 · 감별 핵심", tag="감별")
bullets(s, Inches(0.8), Inches(1.5), Inches(11.8), Inches(1.5), [
    (0,"환자가 복용 중인 pramipexole(미라펙스)+pregabalin(리리카)은 NLC 표준치료가 아니라 RLS 대표 치료제 → 임상상이 RLS(또는 중복)일 가능성. 감별이 먼저.",INK,True),
], size=13.5, gap=8)
rows = [("약물군","RLS에서의 위치(2024/2025 AASM 지침)"),
        ("α2δ 리간드 (gabapentin enacarbil·gabapentin·pregabalin)","1차 권고. pregabalin 강한 권고. augmentation 적음(Allen 2014 NEJM: 1.7% vs pramipexole 9.0%)"),
        ("도파민 작용제 (pramipexole·ropinirole·rotigotine)","augmentation(연 7–10%) 위험으로 1차 권고 안 함(against)"),
        ("철분 교정 (ferritin/TSAT)","기반 치료로 강조"),
        ("NLC(특발성)에서 pramipexole","직접 근거 없음 — 유효하다면 오히려 RLS를 시사")]
table(s, Inches(0.8), Inches(3.1), Inches(11.85), rows,
      [Inches(5.2), Inches(6.65)], size=12, row_h=Inches(0.72), align_first_left=True)
footer(s, "Winkelman 2025(AASM, J Clin Sleep Med); Allen 2014(NEJM NEJMoa1303646)", 23)

# ============================================================ SLIDE 24 — 급성 대증
s = slide()
header(s, "급성 발작 시 대증 요법", eyebrow="보조 · 급성", tag="보조")
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"즉시 신전: 발을 발등 쪽으로 굽혀(dorsiflexion) 종아리를 수동 신장하거나, 벽에 발바닥을 대고 체중을 싣는다.",INK,True),
    (0,"보조: 걷기, 발 흔들기, 근육 마사지, 온찜질.",INK),
    (0,"기전: 건·근 신전 → Ib(골지건) 구심성으로 경련을 반사적으로 억제(Khan & Burne 2007).",INK),
    (0,"흥미로운 기전 — 신맛 자극(pickle juice/식초): Miller 2010, 탈수 유발경련에서 지속시간 ~45% 단축. 구인두 TRP 채널(TRPA1/TRPV1) 자극 → 반사적 α-운동뉴런 억제 가설.",MUTE),
], size=14, gap=12)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), CARD)
text(s, Inches(8.4), Inches(1.9), Inches(4.0), Inches(0.4), [[("발작 시 순서",13,TEALD,True)]])
for i,st in enumerate(["족배굴곡으로 종아리 신장","벽 밀기 자세로 체중 신장","걷기·마사지","온열·수분","(연구단계) 신맛 자극"]):
    yy = Inches(2.5 + i*0.8)
    rect(s, Inches(8.4), yy, Inches(0.5), Inches(0.5), TEAL, round_=True)
    text(s, Inches(8.4), yy, Inches(0.5), Inches(0.5), [[(str(i+1),15,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(9.05), yy, Inches(3.4), Inches(0.5), [[(st,12.5,INK)]], anchor=MSO_ANCHOR.MIDDLE)
footer(s, "Khan & Burne 2007(J Neurophysiol); Miller 2010(Med Sci Sports Exerc)", 24)

# ============================================================ SLIDE 25 — 무효/비권고
s = slide()
header(s, "효과 없거나 권고되지 않는 것 (제외)", eyebrow="근거 부재 · 비권고", tag="비권고", tag_color=RED)
data = [
    ("마그네슘 (특발성 NLC)", "Garrison 2020 Cochrane(11 RCT, 735명): 고령 특발성 NLC에서 위약 대비 임상적으로 의미있는 이득 없음. 흔한 자가처방이나 예방 근거 없음(저마그네슘혈증 교정은 별개).", RED),
    ("혈관주위 스테로이드 주사", "야간경련 적응 인체 근거 0건(신규·비표준). 오히려 동맥내 오주입 → 색전·허혈, 조직·지방 위축, 건 약화 위험. RCT는 신경주위에서 스테로이드보다 D5W가 더 안전·효과적.", RED),
    ("LSB·경막외/SNRB (특발성)", "특발성 NLC 직접 근거 없음(Level V). LSB는 PAD/CLI·CRPS 확인 시에만, 경막외/SNRB는 방사통 동반 시 방사통 목적으로 — 경련 완화는 부수적 기대.", AMBER)]
for i,(t,d,c) in enumerate(data):
    y = Inches(1.55 + i*1.65)
    card(s, Inches(0.8), y, Inches(11.85), Inches(1.45), WHITE, LINE)
    rect(s, Inches(0.8), y, Inches(0.14), Inches(1.45), c)
    text(s, Inches(1.15), y+Inches(0.16), Inches(11.2), Inches(0.4), [[(t,14.5,c,True)]])
    text(s, Inches(1.15), y+Inches(0.62), Inches(11.2), Inches(0.75), [[(d,12.5,INK)]], line_spacing=1.08)
footer(s, "Garrison 2020(Cochrane CD009402); 문헌고찰 Part 7·1·2", 25)

# ============================================================ SLIDE 26 — FGA (기전상 타당)
s = slide()
header(s, "기전상 타당하나 연구 단계 ① FGA 부위 주사", eyebrow="연구 단계 · 신규 가설", tag="연구 단계", tag_color=NAVY2)
bullets(s, Inches(0.8), Inches(1.5), Inches(7.0), Inches(5.0), [
    (0,"직접 근거 없음 — 'FGA(유리 비복근 건막) 주사로 경련 치료'는 탐색적/신규 가설. 근거를 창작하지 않는다.",RED,True),
    (0,"해부(Pedret 2020): FGA = 내측 비복근 원위 근-건 이행부(MTJ)의 건성 영역, 'tennis leg' 호발 부위.",INK),
    (0,"타당성: 이 부위는 골지건기관·근방추 등 기계수용체가 밀집 → 경련 반사 회로의 표적으로 그럴듯함.",INK),
    (0,"경련은 단축 위치의 MTJ 부근에서 잘 유발되고 건 구심성으로 억제된다(Khan & Burne 2007).",INK),
    (-1,"필요: 초음파 유도 필수(소복재정맥·비복신경·족척근 회피), 파일럿·용량탐색 후 RCT.",TEALD,True),
], size=13.5, gap=10)
card(s, Inches(8.1), Inches(1.6), Inches(4.5), Inches(4.9), CARD)
text(s, Inches(8.35), Inches(1.85), Inches(4.0), Inches(0.4), [[("간접 토대(유추)",13,TEALD,True)]])
bullets(s, Inches(8.35), Inches(2.35), Inches(4.0), Inches(4.0), [
    (0,"비복근 유발점 주사가 야간경련 완화(Kim 2015).",INK),
    (0,"비복근 BTX가 야간경련 완화(Park 2017).",INK),
    (0,"FGA/MTJ는 이미 tennis leg·PRP·hydrodissection의 안전한 초음파 표적.",INK),
    (-1,"→ 세 갈래가 '가설'의 간접 토대(직접 외삽 불가).",MUTE),
], size=12.5, gap=10)
footer(s, "Pedret 2020(Scand J Med Sci Sports); Balius 2018; Kim 2015; Park 2017", 26)

# ============================================================ SLIDE 27 — 신경표적/조건부
s = slide()
header(s, "기전상 타당하나 연구 단계 ② 신경 표적·조건부", eyebrow="연구 단계 · 조건부", tag="연구 단계", tag_color=NAVY2)
rows = [("접근","위치·조건","핵심 주의"),
        ("경골/총비골 신경차단","불응성에 선택적(직접근거 제한)","족저굴곡 약화·족하수 → 고령 낙상"),
        ("경골신경 phenol/신경파괴","경직(spastic equinus) 영역 확립","야간경련은 근거 전이(미검증)"),
        ("PTNS/비골신경 자극","RLS·방광에 근거","야간경련 직접 근거 없음"),
        ("요추교감신경차단(LSB)","PAD/CLI·CRPS 확인 시만","특발성 경련엔 권고 안 함"),
        ("경막외/SNRB","방사통·신경인성 파행 동반 시","경련 완화는 부수적 기대")]
table(s, Inches(0.8), Inches(1.55), Inches(11.85), rows,
      [Inches(3.3), Inches(4.4), Inches(4.15)], size=11.5, row_h=Inches(0.6), head_size=12)
text(s, Inches(0.8), Inches(6.35), Inches(11.8), Inches(0.5),
     [[("공통 원칙: 이들은 '특발성 야간경련'의 표준치료가 아니다. 원인(PAD·협착·정맥부전)이 확인되면 그 원인 표적치료로서 의미가 있다.",12,TEALD,True)]])
footer(s, "문헌고찰 Part 1·2·4 (Imura 2015; Deltombe 2010; Charlesworth 2023)", 27)

# ============================================================ SLIDE 28 — 알고리즘
s = slide()
header(s, "종합 치료 알고리즘 / 사다리", eyebrow="종합", tag="정리")
steps = [
    ("1", "진단·감별 (workup)", "NLC vs RLS vs 신경·혈관성 · IRLSSG 기준 · 약물력. 단서 있을 때만 ABI·요추MRI·전해질·TSH.", NAVY),
    ("2", "이차 원인 교정", "PAD·요추관협착·신경병증·정맥부전·전해질 교정. 유발약물(이뇨제·statin·LABA) 조정. CVI→압박스타킹, LSS→재활·BTX.", NAVY2),
    ("3", "비약물 1차 (모든 환자)", "취침 전 종아리+햄스트링 스트레칭 ★핵심 · 자세·수분·온열 · 급성엔 dorsiflexion 신장.", TEAL),
    ("4", "표적 약물 (개별화)", "비교적 안전: Vit B(Level C). 고려: diltiazem·naftidrofuryl·gabapentin. 마그네슘 특발성 무효. quinine은 최후·선별.", TEALD),
    ("5", "불응성 국소치료 (선택)", "유발점 뚜렷 → 국소마취제/dry needling. 난치성 → 비복근 BTX(근력약화 설명). 보조 → ESWT.", GREEN)]
for i,(n,t,d,c) in enumerate(steps):
    y = Inches(1.5 + i*1.04)
    rect(s, Inches(0.8), y, Inches(0.75), Inches(0.9), c, round_=True)
    text(s, Inches(0.8), y, Inches(0.75), Inches(0.9), [[(n,26,WHITE,True)]],
         align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    card(s, Inches(1.7), y, Inches(10.95), Inches(0.9), CARD)
    text(s, Inches(2.0), y+Inches(0.12), Inches(3.4), Inches(0.7), [[(t,14,c,True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(5.2), y+Inches(0.1), Inches(7.2), Inches(0.72), [[(d,11.8,INK)]],
         anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.05)
footer(s, "문헌고찰 종합 결론 · 치료 사다리", 28)

# ============================================================ SLIDE 29 — 9개 항목 요약표
s = slide()
header(s, "9개 항목 근거 요약표", eyebrow="종합 · 근거표", tag="요약")
rows = [("치료","경련 직접근거","근거수준","권고"),
        ("요추교감신경차단(LSB)","없음","Level V","특발성 X · PAD/CRPS만"),
        ("경막외/SNRB","없음","II~IV(연관)/V","방사통 목적, 경련 부수"),
        ("체외충격파(ESWT)","후향 1편","경직 I~II/경련 III","보조 시도 가능"),
        ("경골/비골 신경주사","1편+BTX RCT","II(BTX)/III~IV","낙상 주의·선택적"),
        ("FGA 부위 주사","없음","Level V","연구단계 가설"),
        ("근육내/유발점 주사","BTX·유발점 소규모","II(BTX)/III","MTrP 뚜렷·불응성"),
        ("혈관주위 스테로이드","없음 + 위해","Level V","권고 안 함"),
        ("취침 전 약물(RLS약)","NLC 근거 없음","가이드라인(RLS)","NLC/RLS 감별 핵심"),
        ("기타(스트레칭·원인치료)","스트레칭 RCT","I~II(일부)","1차 · 최우선")]
table(s, Inches(0.8), Inches(1.45), Inches(11.85), rows,
      [Inches(3.6), Inches(3.0), Inches(2.35), Inches(2.9)], size=11, row_h=Inches(0.46), head_size=11.5)
footer(s, "근거수준: I(SR/MA)·II(RCT)·III(비무작위)·IV(관찰)·V(전문가/기전)", 29)

# ============================================================ SLIDE 30 — 핵심 메시지
s = slide()
rect(s, 0, 0, SW, SH, NAVY)
rect(s, 0, 0, Inches(0.22), SH, TEAL)
text(s, Inches(0.9), Inches(0.7), Inches(11.5), Inches(0.6), [[("핵심 메시지",13,RGBColor(0x9F,0xE0,0xD8),True)]])
text(s, Inches(0.9), Inches(1.2), Inches(11.5), Inches(0.8),
     [[("\"밤에 깨는 다리 증상\"의 성패는 시술이 아니라 감별에서 갈린다",23,WHITE,True)]])
msgs = [
    ("가장 확실한 것","정확한 감별 · 원인질환 교정 · 취침 전 스트레칭 · 유발약물 검토가 관리의 근간."),
    ("효과 있는 주사","BTX(비복근, RCT) / 국소마취제 유발점주사·dry needling(MTrP 동반) / 심비골신경 차단(Imura). 불응성에 선택적."),
    ("타당하나 제한적","ESWT는 경직 근거는 강하나 경련 직접근거는 약함 → 보조·근거형성 중."),
    ("근거 없음·비권고","마그네슘(특발성 무효), 혈관주위 스테로이드(위해), FGA·특발성 LSB는 표준치료 아님."),
    ("약물","근거 약함 → 개별화. quinine은 FDA 경고로 일상 회피. pramipexole/pregabalin은 RLS 약 → 감별.")]
for i,(t,d) in enumerate(msgs):
    y = Inches(2.35 + i*0.92)
    rect(s, Inches(0.9), y+Inches(0.04), Inches(0.16), Inches(0.66), TEAL)
    text(s, Inches(1.25), y, Inches(3.0), Inches(0.8), [[(t,14.5,RGBColor(0x9F,0xE0,0xD8),True)]], anchor=MSO_ANCHOR.MIDDLE)
    text(s, Inches(4.3), y, Inches(8.3), Inches(0.8), [[(d,13,WHITE)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.06)

# ============================================================ SLIDE 31 — 참고문헌 1
def ref_slide(idx, title, refs, page):
    s = slide()
    header(s, title, eyebrow="참고문헌", tag="References")
    half = (len(refs)+1)//2
    for col,chunk in enumerate([refs[:half], refs[half:]]):
        x = Inches(0.8 + col*6.0)
        text(s, x, Inches(1.5), Inches(5.75), Inches(5.3),
             [{'runs':[(r, 10.5, INK)], 'space_after':7, 'ls':1.06} for r in chunk])
    footer(s, "PubMed/PMC 대조 검증 완료 — 조작·확인불가 인용 없음", page)
    return s

refs1 = [
 "Hallegraeff JM, et al. Stretching before sleep reduces nocturnal leg cramps in older adults: RCT. J Physiother. 2012;58(1):17-22. PMID 22341378.",
 "Garrison SR, et al. Nocturnal leg cramps and prescription use: sequence symmetry analysis. Arch Intern Med. 2012;172(2):120-6. PMID 22157068.",
 "Park SJ, et al. Botulinum toxin for nocturnal calf cramps in LSS: RCT. Arch Phys Med Rehabil. 2017;98(5):957-63. PMID 28209505.",
 "Restivo DA, et al. Efficacy of Botulinum Toxin A for cramps in diabetic neuropathy. Ann Neurol. 2018;84(5):674-82. PMID 30225985.",
 "Kim DH, et al. Myofascial trigger point injections on nocturnal calf cramps. J Am Board Fam Med. 2015;28(1):21-7. PMID 25567819.",
 "Prateepavanich P, et al. MTrP of gastrocnemius and nocturnal calf cramps. J Med Assoc Thai. 1999;82(5):451-9. PMID 10443094.",
 "Temel MH, et al. Dry needling on nocturnal calf cramps: RCS. Turk J Osteoporos. 2023;29(3):170-6.",
 "Bagcier F, Yurdakul OV. Dry needling of MTrP in nocturnal calf cramp. J Am Board Fam Med. 2021;34(1):245-6. PMID 33452105.",
 "Imura T, et al. Nocturnal leg cramps treated by deep peroneal nerve medial branch block. Brain Behav. 2015;5(9):e00370. PMID 26445706.",
 "Minetto MA, et al. Mechanisms of cramp contractions: peripheral or central? J Physiol. 2011;589:5759-73. PMID 21969448.",
 "Miller TM, Layzer RB. Muscle cramps. Muscle Nerve. 2005;32(4):431-42. PMID 15902691.",
 "Khan SI, Burne JA. Reflex inhibition of cramp by tendon stimulation. J Neurophysiol. 2007;98(3):1102-7. PMID 17634341.",
]
ref_slide(1, "참고문헌 (1/2) — 비약물 · 주사 · 기전", refs1, 31)

# ============================================================ SLIDE 32 — 참고문헌 2
refs2 = [
 "Li BZ, et al. ESWT reduces leg cramps in lumbar degenerative disorders: retrospective. Biomed Res Int. 2021;2021:3554397. PMID 34734084.",
 "Otero-Luis I, et al. ESWT for spasticity: systematic review & meta-analysis. J Clin Med. 2024;13(5):1323. PMID 38592705.",
 "Mihai EE, et al. Long-term ESWT on lower-limb post-stroke spasticity: SR/MA. J Clin Med. 2020;10(1):86. PMID 33383655.",
 "Yang E, et al. Recent advances in spasticity: ESWT (mechanism review). J Clin Med. 2021;10(20):4723. PMID 34682846.",
 "El-Tawil S, et al. Quinine for muscle cramps. Cochrane Database Syst Rev. 2015;(4):CD005044. PMID 25842375.",
 "Katzberg HD, et al. Symptomatic treatment for muscle cramps (AAN evidence review). Neurology. 2010;74(8):691-6. PMID 20177124.",
 "Garrison SR, et al. Magnesium for skeletal muscle cramps. Cochrane Database Syst Rev. 2020;9:CD009402. PMID 32956536.",
 "Chan P, et al. Vitamin B complex for nocturnal leg cramps: RCT. J Clin Pharmacol. 1998;38(12):1151-4. PMID 11301568.",
 "Voon WC, Sheu SH. Diltiazem for nocturnal leg cramps. Age Ageing. 2001;30(1):91-2. PMID 11322688.",
 "Tan J, et al. Vitamin K2 in nocturnal leg cramps: RCT. JAMA Intern Med. 2024;184(12):1443-7. PMID 39466236 (정정·교체 2025).",
 "Allen RP, et al. Pregabalin vs pramipexole for RLS. N Engl J Med. 2014;370(7):621-31. PMID 24521108.",
 "Winkelman JW, et al. AASM clinical practice guideline: RLS/PLMD. J Clin Sleep Med. 2025;21(1):137-52. PMID 39324694.",
 "Pedret C, et al. Ultrasound classification of medial gastrocnemius injuries. Scand J Med Sci Sports. 2020;30(12):2456-65. PMID 32854168.",
 "Allen RE, Kirby KA. Nocturnal leg cramps. Am Fam Physician. 2012;86(4):350-5. PMID 22963024.",
]
ref_slide(2, "참고문헌 (2/2) — 충격파 · 약물 · 감별", refs2, 32)

prs.save("/home/user/ppt-work/야간_하지경련_치료_PPT.pptx")
print("saved:", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
print("OK")
