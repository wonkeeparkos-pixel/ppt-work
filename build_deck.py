# -*- coding: utf-8 -*-
"""
친절이 통증을 바꾼다 — 근거 기반 환자 소통 가이드 (30장)
두 원문(과학적 근거 + 시술별 멘트)을 연결한 발표자료.
python-pptx 로 16:9 덱을 생성한다.
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ---------- 팔레트 ----------
INK   = RGBColor(0x1D, 0x3B, 0x36)   # 본문 짙은 청록회색
DEEP  = RGBColor(0x0E, 0x5C, 0x57)   # 딥 틸 (섹션/표지)
TEAL  = RGBColor(0x1F, 0x9E, 0x93)   # 포인트 틸
TEALL = RGBColor(0x8F, 0xCE, 0xC7)   # 옅은 틸
MINT  = RGBColor(0xE9, 0xF4, 0xF1)   # 민트 배경
MINT2 = RGBColor(0xD7, 0xEC, 0xE7)   # 민트 카드
CORAL = RGBColor(0xD3, 0x5D, 0x49)   # 회피/경고 웜
CORALB= RGBColor(0xFB, 0xEC, 0xE7)   # 옅은 코랄 배경
GOLD  = RGBColor(0xE3, 0x9A, 0x3B)   # 강조 숫자
GRAY  = RGBColor(0x7A, 0x8C, 0x88)   # 캡션/출처
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PAPER = RGBColor(0xFA, 0xFD, 0xFC)   # 살짝 따뜻한 흰 배경

FONT   = "Malgun Gothic"   # 한글 안전 폰트 (뷰어에서 자동 대체)
FONT_B = "Malgun Gothic"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
EMUW, EMUH = prs.slide_width, prs.slide_height


# ---------- 헬퍼 ----------
def _set_ea(run, name):
    """한글(East-Asian) 폰트 지정."""
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:ea", "a:cs", "a:latin"):
        el = rPr.find(qn(tag))
        if el is None:
            el = rPr.makeelement(qn(tag), {})
            rPr.append(el)
        el.set("typeface", name)

def bg(slide, color):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, shadow=False,
         shape=MSO_SHAPE.RECTANGLE, radius=None):
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius is not None:
        try:
            sp.adjustments[0] = radius
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = fill
    if line is None:
        sp.line.fill.background()
    else:
        sp.line.color.rgb = line; sp.line.width = Pt(line_w)
    sp.shadow.inherit = False
    if shadow:
        el = sp._element.spPr
        ef = el.makeelement(qn('a:effectLst'), {})
        sh = el.makeelement(qn('a:outerShdw'),
                            {'blurRad':'90000','dist':'40000','dir':'5400000','rotWithShape':'0'})
        clr = el.makeelement(qn('a:srgbClr'), {'val':'1D3B36'})
        al  = el.makeelement(qn('a:alpha'), {'val':'22000'})
        clr.append(al); sh.append(clr); ef.append(sh); el.append(ef)
    return sp

def line(slide, x, y, w, h, color, weight=2.0):
    sp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = color
    sp.line.fill.background(); sp.shadow.inherit = False
    return sp

def text(slide, x, y, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
         line_spacing=1.0, wrap=True):
    """
    runs: list of paragraphs; each paragraph = list of (string, size, color, bold, [font])
          또는 단일 (string, size, color, bold) 는 자동으로 문단 1개로.
    """
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    # 정규화: paragraphs = [ [run, run, ...], ... ]  (run = tuple)
    if isinstance(runs, tuple):
        paragraphs = [[runs]]
    else:
        paragraphs = []
        for para in runs:
            paragraphs.append([para] if isinstance(para, tuple) else list(para))
    for i, para in enumerate(paragraphs):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        for seg in para:
            s, size, color, bold = seg[0], seg[1], seg[2], seg[3]
            fname = seg[4] if len(seg) > 4 else FONT
            r = p.add_run(); r.text = s
            r.font.size = Pt(size); r.font.bold = bold
            r.font.color.rgb = color; r.font.name = fname
            _set_ea(r, fname)
    return tb

def chip(slide, x, y, label, fill=TEAL, fg=WHITE, size=12.5, padw=None):
    w = padw if padw else (0.16 + len(label) * (size/72.0) * 1.05)
    sp = rect(slide, x, y, w, 0.42, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tf = sp.text_frame; tf.word_wrap = False
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = label
    r.font.size=Pt(size); r.font.bold=True; r.font.color.rgb=fg; r.font.name=FONT
    _set_ea(r, FONT)
    return sp

def footer(slide, n):
    line(slide, 0.9, 6.72, 11.53, 0.014, MINT2)
    text(slide, 11.35, 6.82, 1.08, 0.35, (f"{n:02d}", 10, GRAY, True),
         align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def source(slide, s, x=0.9, y=6.82):
    text(slide, x, y, 9.8, 0.35, ("근거  " + s, 9.5, GRAY, False), anchor=MSO_ANCHOR.MIDDLE)

def kicker_head(slide, kick, head_runs, sub=None, kfill=TEAL):
    """상단 kicker chip + 헤드라인 (+옵션 서브)."""
    chip(slide, 0.9, 0.75, kick, fill=kfill)
    text(slide, 0.87, 1.35, 11.5, 1.5, head_runs, line_spacing=1.02)
    if sub:
        text(slide, 0.9, None or 0, 0, 0, "")  # placeholder (미사용)


PAGE = 0
def newslide(color=PAPER):
    global PAGE
    PAGE += 1
    s = prs.slides.add_slide(BLANK)
    bg(s, color)
    return s


# =====================================================================
# 1 — 표지
# =====================================================================
s = newslide(DEEP)
rect(s, 0, 0, 13.333, 0.28, fill=TEAL)
rect(s, 0, 7.22, 13.333, 0.28, fill=GOLD)
# 장식용 원
c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.7), Inches(-1.5), Inches(5.6), Inches(5.6))
c.fill.solid(); c.fill.fore_color.rgb = RGBColor(0x12,0x6B,0x65); c.line.fill.background(); c.shadow.inherit=False
c2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.2), Inches(3.4), Inches(4.4), Inches(4.4))
c2.fill.solid(); c2.fill.fore_color.rgb = RGBColor(0x10,0x64,0x5F); c2.line.fill.background(); c2.shadow.inherit=False
chip(s, 0.95, 1.35, "근거 기반 환자 소통 가이드", fill=TEAL)
text(s, 0.9, 2.15, 10.5, 2.4, [
    [("말과 친절이", 60, WHITE, True)],
    [("통증을 바꾼다", 60, TEALL, True)],
], line_spacing=1.05)
line(s, 0.98, 4.55, 2.1, 0.05, GOLD)
text(s, 0.95, 4.8, 10.5, 1.0, [
    [("노시보를 줄이고 안심을 더하는 진료실 커뮤니케이션", 20, WHITE, False)],
    [("척추 중재시술 · 사지 관절 주사 실무", 15, TEALL, False)],
], line_spacing=1.35)

# =====================================================================
# 2 — 핵심 선언
# =====================================================================
s = newslide(PAPER)
rect(s, 0, 0, 0.35, 7.5, fill=TEAL)
chip(s, 1.2, 1.15, "한 문장으로", fill=MINT2, fg=DEEP)
text(s, 1.15, 1.95, 11.2, 2.6, [
    [("통증은 자극만으로", 42, INK, True)],
    [("정해지지 않습니다.", 42, TEAL, True)],
], line_spacing=1.08)
text(s, 1.2, 4.55, 10.6, 1.6, [
    [("같은 주사도 ", 20, INK, False), ("어떤 말을 듣느냐에 따라", 20, DEEP, True),
     ("  더 아플 수도, 덜 아플 수도 있습니다.", 20, INK, False)],
    [("이것은 위안의 문제가 아니라 뇌·척수에서 일어나는 실제 현상입니다.", 16, GRAY, False)],
], line_spacing=1.4)
footer(s, PAGE)

# =====================================================================
# 3 — 아젠다 (3파트)
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "이 발표가 답하는 것", fill=TEAL)
text(s, 0.87, 1.35, 11, 0.9, [("세 걸음으로 이어집니다", 30, INK, True)])
cards = [
    ("왜", "왜 말과 친절이\n통증을 바꾸는가", "노시보·플라시보·불안의 근거", TEAL),
    ("어떻게", "어떻게 말할 것인가", "진료실 4가지 핵심 원칙", DEEP),
    ("무엇을", "무엇을 말할 것인가", "시술별로 바로 쓰는 문장", GOLD),
]
cx = 0.9
for i,(num,t,d,col) in enumerate(cards):
    x = 0.9 + i*4.05
    rect(s, x, 2.7, 3.7, 3.3, fill=WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, shadow=True)
    rect(s, x, 2.7, 3.7, 0.65, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
    rect(s, x, 3.05, 3.7, 0.3, fill=col)
    text(s, x, 2.7, 3.7, 0.65, (f"STEP {i+1}", 13, WHITE, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+0.35, 3.75, 3.0, 1.4, [[(seg, 21, INK, True)] for seg in t.split("\n")], line_spacing=1.1)
    text(s, x+0.35, 5.25, 3.0, 0.9, (d, 14, GRAY, False), line_spacing=1.25)
footer(s, PAGE)

# =====================================================================
# 4 — 섹션 01
# =====================================================================
def section(num, title, sub):
    s = newslide(DEEP)
    rect(s, 0, 0, 13.333, 0.24, fill=TEAL)
    rect(s, 0, 7.26, 13.333, 0.24, fill=GOLD)
    text(s, 0.95, 1.75, 6, 2.4, (num, 150, RGBColor(0x14,0x6B,0x65), True))
    line(s, 1.05, 4.1, 2.0, 0.06, GOLD)
    text(s, 1.0, 4.35, 11, 1.3, [[(t, 40, WHITE, True)] for t in title], line_spacing=1.05)
    text(s, 1.02, None, 0,0,"") if False else None
    text(s, 1.03, 4.3 + 0.75*len(title) + 0.35, 10.8, 0.8, (sub, 17, TEALL, False))
    return s
section("01", ["왜 말과 친절이 통증을 바꾸는가"], "노시보 · 플라시보 · 공감 · 불안의 과학")

# =====================================================================
# 5 — 통증은 뇌가 만든다
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "기본 원리", fill=TEAL)
text(s, 0.87, 1.35, 11.5, 1.4, [
    [("통증은 ", 34, INK, True), ("뇌가 만드는 경험", 34, TEAL, True), ("입니다", 34, INK, True)]])
text(s, 0.9, 2.55, 11.3, 1.0, [
    ("같은 자극이라도 다음 네 가지가 실제 통각을 바꿉니다.", 17, INK, False)])
items = [("기대", "무엇을 예상하는가"), ("불안", "얼마나 두려운가"),
         ("주의", "어디에 집중하는가"), ("태도", "어떻게 대하는가")]
for i,(t,d) in enumerate(items):
    x = 0.9 + i*3.0
    rect(s, x, 3.5, 2.75, 2.1, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    rect(s, x, 3.5, 0.14, 2.1, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    text(s, x+0.45, 3.85, 2.2, 0.8, (t, 25, DEEP, True))
    text(s, x+0.47, 4.75, 2.15, 0.8, (d, 14, GRAY, False), line_spacing=1.2)
source(s, "Blasini 2017; Colloca & Benedetti 2007 — 하행통증조절 회로의 신경생물학")
footer(s, PAGE)

# =====================================================================
# 6 — 노시보 데이터 (Varelmann)
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ① 노시보", fill=CORAL)
text(s, 0.87, 1.35, 7.6, 1.7, [
    [("부정적인 말이", 33, INK, True)],
    [("통증을 ", 33, INK, True), ("키웁니다", 33, CORAL, True)]], line_spacing=1.05)
text(s, 0.9, 3.35, 7.4, 2.6, [
    [("만삭 산모 ", 16, INK, False), ("140명", 16, DEEP, True), (" 무작위시험.", 16, INK, False)],
    [("주사 직전 ", 16, INK, False), ("말 한마디만 다르게", 16, DEEP, True), (" 했습니다.", 16, INK, False)],
    [(" ", 8, INK, False)],
    [("×  ", 15, CORAL, True), ("“벌에 쏘이듯 아플 거예요, 여기가 제일 아파요”", 15, INK, False)],
    [("○  ", 15, TEAL, True), ("“마취약을 넣어 편안하게 해드릴게요”", 15, INK, False)],
], line_spacing=1.5)
# 오른쪽 데이터 카드
rect(s, 8.7, 1.6, 3.75, 4.4, fill=DEEP, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, shadow=True)
text(s, 8.7, 2.05, 3.75, 0.6, ("통증 점수 (VAS 중앙값)", 14, TEALL, True), align=PP_ALIGN.CENTER)
text(s, 8.7, 2.65, 3.75, 1.5, [
    [("5", 66, CORAL, True), ("   vs   ", 26, TEALL, False), ("3", 66, WHITE, True)]],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 8.7, 4.15, 3.75, 0.6, [
    [("위협 예고", 13, CORAL, True), ("        안심 표현", 13, TEALL, True)]], align=PP_ALIGN.CENTER)
line(s, 9.3, 4.95, 2.55, 0.03, RGBColor(0x14,0x6B,0x65))
text(s, 8.7, 5.15, 3.75, 0.6, ("P < 0.001 · 말만 바꿔 통증이 갈렸다", 12.5, WHITE, False), align=PP_ALIGN.CENTER)
source(s, "Varelmann et al., Anesth Analg 2010 (n=140)")
footer(s, PAGE)

# =====================================================================
# 7 — 말이 아프게 할 수 있다 (Lang)
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ① 노시보", fill=CORAL)
text(s, 0.87, 1.35, 11.5, 1.4, [
    [("“아플 거예요”라는 경고가", 30, INK, True)],
    [("통증과 불안을 ", 30, INK, True), ("동시에 키웁니다", 30, CORAL, True)]], line_spacing=1.05)
text(s, 0.9, 3.35, 11.2, 1.6, [
    ("중재적 방사선 시술 159건을 분석했습니다.", 17, INK, False),
    ("시술이 끝난 뒤 “많이 아프셨죠”라는 부정적 공감조차 불안을 더 키웠습니다.", 17, INK, False),
], line_spacing=1.5)
for i,(v,lab,col) in enumerate([("P < 0.05","경고 → 통증 ↑",CORAL),("P < 0.001","경고 → 불안 ↑",CORAL)]):
    x = 0.9 + i*4.3
    rect(s, x, 5.05, 4.0, 1.15, fill=CORALB, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    text(s, x+0.4, 5.05, 3.4, 1.15, [
        [(lab, 15, INK, True)], [(v, 17, CORAL, True)]], anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)
source(s, "Lang et al., “Can words hurt?” Pain 2005 (159건)")
footer(s, PAGE)

# =====================================================================
# 8 — '따끔할 거예요'는 이득이 없다
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ① 노시보", fill=CORAL)
text(s, 0.87, 1.35, 11.5, 1.4, [
    [("“따끔할 거예요”는", 32, INK, True)],
    [("통증을 ", 32, INK, True), ("줄여주지 않습니다", 32, CORAL, True)]], line_spacing=1.05)
text(s, 0.9, 3.4, 11.3, 2.2, [
    [("‘따끔’ 경고와 중립 신호(“준비되셨어요?”)의 통증 점수는 ", 17, INK, False),
     ("사실상 같았습니다.", 17, DEEP, True)],
    [(" ", 8, INK, False)],
    [("통증 단어는 이득 없이 ", 17, INK, False), ("부정 암시의 위험만", 17, CORAL, True),
     (" 남깁니다.", 17, INK, False)],
    [("경고를 들은 환자는 소리 내어 아파하는 반응이 유의하게 늘었습니다.", 15, GRAY, False)],
], line_spacing=1.5)
source(s, "Vijayan et al., Pain Pract 2015 · Dutt-Gupta et al., Br J Anaesth 2007")
footer(s, PAGE)

# =====================================================================
# 9 — 안심의 힘 (플라시보)
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ② 플라시보", fill=TEAL)
text(s, 0.87, 1.35, 7.7, 1.7, [
    [("안심시키는 말은", 33, INK, True)],
    [("통증을 ", 33, INK, True), ("낮춥니다", 33, TEAL, True)]], line_spacing=1.05)
text(s, 0.9, 3.4, 7.5, 2.5, [
    [("효과는 ", 16, INK, False), ("‘작지만 분명’", 16, DEEP, True), ("합니다.", 16, INK, False)],
    [("정보 · 주의분산 · 통제감과 ", 16, INK, False), ("함께 쓸 때 커집니다.", 16, DEEP, True)],
    [(" ", 8, INK, False)],
    [("단, 어떤 말도 진통제를 대체하지는 못합니다.", 15, GRAY, False)],
], line_spacing=1.5)
rect(s, 8.7, 1.75, 3.75, 4.1, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06, shadow=True)
text(s, 8.7, 2.3, 3.75, 1.5, [
    [("51", 60, TEAL, True), ("개 RCT", 20, DEEP, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 8.7, 3.75, 3.75, 1.0, [
    [("5,079", 40, DEEP, True), ("명", 18, INK, True)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 8.85, 4.85, 3.45, 0.9, ("소통은 급성 통증에 유의한(작은) 효과", 13.5, INK, False),
     align=PP_ALIGN.CENTER, line_spacing=1.2)
source(s, "Mistiaen et al., Eur J Pain 2016 (체계적 문헌고찰)")
footer(s, PAGE)

# =====================================================================
# 10 — 태도가 스위치다
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ③ 공감·태도", fill=TEAL)
text(s, 0.87, 1.35, 11.5, 1.4, [
    [("태도가 ", 33, INK, True), ("스위치", 33, GOLD, True), ("입니다", 33, INK, True)]])
text(s, 0.9, 2.5, 11.2, 0.9, ("따뜻한 어조와 유능함이 함께일 때 비로소 불안이 유의하게 줄었습니다.", 17, INK, False))
# 공식 카드
combos = [("따뜻함", TEAL, "만으로는 부족"), ("유능함", DEEP, "만으로도 부족"), ("둘 다", GOLD, "효과가 켜진다")]
for i,(t,col,d) in enumerate(combos):
    x = 0.9 + i*3.95
    rect(s, x, 3.5, 3.05, 2.35, fill=WHITE, line=col, line_w=2.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07, shadow=True)
    text(s, x, 3.9, 3.05, 0.9, (t, 27, col, True), align=PP_ALIGN.CENTER)
    text(s, x, 4.95, 3.05, 0.6, (d, 15, GRAY, False), align=PP_ALIGN.CENTER)
    if i < 2:
        text(s, x+3.15, 3.5, 0.7, 2.35, ("+", 34, TEALL, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Verheul et al. 2010 · Howe, Goyer & Crum 2017")
footer(s, PAGE)

# =====================================================================
# 11 — 불안이 증폭기
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "근거 ④ 불안", fill=CORAL)
text(s, 0.87, 1.35, 11.5, 1.4, [
    [("불안이 통증의 ", 33, INK, True), ("증폭기", 33, CORAL, True), ("입니다", 33, INK, True)]])
text(s, 0.9, 2.65, 11.2, 1.6, [
    ("시술 전 불안이 높을수록 통증을 더 크게 느끼고, 진통제도 더 필요했습니다.", 17, INK, False),
    ("그래서 통증을 다루기 전에 불안을 먼저 다뤄야 합니다.", 17, DEEP, False),
], line_spacing=1.5)
# 불안→통증 고리를 끊는 5가지
five = ["정보 제공", "주의 분산", "통제감", "예측 가능성", "호흡 유도"]
for i,t in enumerate(five):
    x = 0.9 + i*2.37
    rect(s, x, 4.6, 2.15, 1.3, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
    text(s, x, 4.6, 2.15, 1.3, (t, 15.5, DEEP, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.9, 4.05, 8, 0.5, ("불안–통증 고리를 끊는 5가지", 14, GRAY, True))
source(s, "Sorrentino et al. 2020 (자궁경 104명) · 이하 원칙의 근거")
footer(s, PAGE)

# =====================================================================
# 12 — 뇌 속 두 갈래 길
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "왜 그럴까", fill=TEAL)
text(s, 0.87, 1.35, 11.5, 1.1, [("뇌 속에는 두 갈래 길이 있습니다", 30, INK, True)])
# 노시보 경로
rect(s, 0.9, 2.8, 11.5, 1.55, fill=CORALB, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
text(s, 1.25, 2.8, 2.2, 1.55, ("노시보", 21, CORAL, True), anchor=MSO_ANCHOR.MIDDLE)
text(s, 3.4, 2.8, 9.0, 1.55, [
    [("부정적 기대 · 불안", 16, INK, True), ("   →   CCK 활성   →   ", 15, GRAY, False),
     ("통증 ↑", 18, CORAL, True)]], anchor=MSO_ANCHOR.MIDDLE)
# 플라시보 경로
rect(s, 0.9, 4.6, 11.5, 1.55, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
text(s, 1.25, 4.6, 2.2, 1.55, ("플라시보", 21, TEAL, True), anchor=MSO_ANCHOR.MIDDLE)
text(s, 3.4, 4.6, 9.0, 1.55, [
    [("안심 · 긍정 기대", 16, INK, True), ("   →   오피오이드·도파민   →   ", 15, GRAY, False),
     ("통증 ↓", 18, TEAL, True)]], anchor=MSO_ANCHOR.MIDDLE)
source(s, "하행통증조절 회로(ACC–PAG–척수)가 통증 신호를 실제로 키우거나 줄인다 — Benedetti 2006")
footer(s, PAGE)

# =====================================================================
# 13 — 섹션 02
# =====================================================================
section("02", ["어떻게 말할 것인가"], "진료실에서 지키는 4가지 핵심 원칙")

# =====================================================================
# 14 — 4원칙 개요
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "한눈에", fill=TEAL)
text(s, 0.87, 1.35, 11.5, 1.0, [("네 가지만 기억하세요", 30, INK, True)])
prin = [
    ("①", "정직하되 안심", "거짓 안심 대신 실제 감각을 미리"),
    ("②", "중립 감각어", "위협어를 ‘누르는 느낌’으로"),
    ("③", "통제감·예측", "멈출 권한과 예고를 준다"),
    ("④", "격려·주의분산", "반복 위로보다 주의를 돌리기"),
]
for i,(n,t,d) in enumerate(prin):
    x = 0.9 + (i%2)*5.85
    y = 2.55 + (i//2)*1.95
    rect(s, x, y, 5.5, 1.65, fill=WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07, shadow=True)
    rect(s, x, y, 1.15, 1.65, fill=DEEP if i%2==0 else TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.07)
    rect(s, x+0.85, y, 0.3, 1.65, fill=DEEP if i%2==0 else TEAL)
    text(s, x, y, 1.15, 1.65, (n, 34, WHITE, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, x+1.45, y+0.28, 3.9, 0.7, (t, 21, INK, True))
    text(s, x+1.47, y+0.98, 3.9, 0.6, (d, 14, GRAY, False))
footer(s, PAGE)

# 원칙 상세 공통 함수
def principle(num, title_col, title, body_lines, quote_good=None, quote_bad=None, src=None, kfill=TEAL):
    s = newslide(PAPER)
    rect(s, 0, 0, 0.35, 7.5, fill=title_col)
    chip(s, 1.2, 0.85, f"원칙 {num}", fill=kfill)
    text(s, 1.15, 1.5, 11, 1.2, title, line_spacing=1.03)
    text(s, 1.2, 2.95, 10.9, 1.5, body_lines, line_spacing=1.5)
    yq = 4.55
    if quote_good:
        rect(s, 1.2, yq, 10.9, 0.95, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
        text(s, 1.55, yq, 0.6, 0.95, ("○", 22, TEAL, True), anchor=MSO_ANCHOR.MIDDLE)
        text(s, 2.2, yq, 9.6, 0.95, (quote_good, 16, INK, False), anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)
        yq += 1.1
    if quote_bad:
        rect(s, 1.2, yq, 10.9, 0.95, fill=CORALB, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
        text(s, 1.55, yq, 0.6, 0.95, ("×", 22, CORAL, True), anchor=MSO_ANCHOR.MIDDLE)
        text(s, 2.2, yq, 9.6, 0.95, (quote_bad, 16, INK, False), anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)
    if src:
        source(s, src)
    footer(s, PAGE)
    return s

# 15 — 원칙 1
principle("①", DEEP,
    [[("정직하되 ", 32, INK, True), ("안심시킨다", 32, TEAL, True)]],
    [[("“하나도 안 아파요” 같은 ", 16, INK, False), ("거짓 안심은 역효과", 16, CORAL, True), ("입니다.", 16, INK, False)],
     [("무엇이·언제·어떤 느낌인지 ", 16, INK, False), ("절차와 감각을 함께", 16, DEEP, True), (" 미리 알려주세요.", 16, INK, False)]],
    quote_good="“잠깐 뻐근한 느낌이 몇 초 지나가고, 그다음엔 훨씬 편해지실 거예요.”",
    src="Suls & Wan 1989 (감각+절차 정보 결합이 통증·불안을 가장 잘 낮춤)")

# 16 — 원칙 2 (버리기/쓰기)
s = newslide(PAPER)
rect(s, 0, 0, 0.35, 7.5, fill=TEAL)
chip(s, 1.2, 0.85, "원칙 ②", fill=TEAL)
text(s, 1.15, 1.5, 11, 1.2, [[("위협어를 ", 32, INK, True), ("중립 감각어로", 32, TEAL, True)]])
text(s, 1.2, 2.75, 10.8, 0.7, ("같은 상황, 단어만 바꿔도 통증이 달라집니다.", 16, INK, False))
# 버리기
rect(s, 1.2, 3.6, 5.3, 2.5, fill=CORALB, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
text(s, 1.55, 3.8, 4.6, 0.6, ("×  버리기", 18, CORAL, True))
for i,w in enumerate(["따끔 · 벌침","제일 아픈 부분","찢어지듯","많이 아플 거예요"]):
    text(s, 1.6, 4.45+i*0.4, 4.7, 0.4, (w, 15, INK, False))
# 쓰기
rect(s, 6.9, 3.6, 5.2, 2.5, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.06)
text(s, 7.25, 3.8, 4.6, 0.6, ("○  쓰기", 18, TEAL, True))
for i,w in enumerate(["누르는 느낌 · 압박감","지그시 눌림","뻐근함","곧 편해지실 거예요"]):
    text(s, 7.3, 4.45+i*0.4, 4.7, 0.4, (w, 15, INK, False))
# 화살표
text(s, 6.45, 3.6, 0.6, 2.5, ("→", 30, TEALL, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
source(s, "Varelmann 2010 · Taddio CMAJ 2015 (백신 통증 지침, 중립 감각어 권고)")
footer(s, PAGE)

# 17 — 원칙 3
principle("③", DEEP,
    [[("통제감과 ", 32, INK, True), ("예측 가능성", 32, TEAL, True), ("을 준다", 32, INK, True)]],
    [[("멈출 권한과 예고를 주면 ", 16, INK, False), ("뇌가 자극을 계속 경계할 필요가 줄어", 16, DEEP, True),
      ("듭니다.", 16, INK, False)]],
    quote_good="“불편하면 언제든 손 들어 주세요. 바로 멈추겠습니다.”",
    quote_bad="“움직이지 말고 가만히 계세요.”",
    src="Habermann & Büchel, Nat Commun 2025 (통제·예측이 기대 정밀도를 높여 통증 조절)")

# 18 — 원칙 4
s = newslide(PAPER)
rect(s, 0, 0, 0.35, 7.5, fill=TEAL)
chip(s, 1.2, 0.85, "원칙 ④", fill=TEAL)
text(s, 1.15, 1.5, 11, 1.2, [[("격려하고 ", 32, INK, True), ("주의를 분산", 32, TEAL, True), ("한다", 32, INK, True)]])
text(s, 1.2, 2.75, 10.9, 1.3, [
    [("진행 안내 · 호흡 유도 · 대화 · 음악 · VR.", 16, INK, False)],
    [("단, ", 16, INK, False), ("반복적 “괜찮아요”와 사과는 오히려 고통을 키웁니다.", 16, CORAL, True)],
], line_spacing=1.45)
# 데이터 두 개
data = [("음악 시술", "통증 NRS", "2 vs 6", "음악군 vs 대조군"),
        ("VR 몰입", "추가 마취 필요", "21% vs 68%", "VR군 vs 대조군")]
for i,(t,lab,val,d) in enumerate(data):
    x = 1.2 + i*5.6
    rect(s, x, 4.35, 5.2, 1.75, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, shadow=True)
    text(s, x+0.4, 4.6, 4.5, 0.5, (t, 14, DEEP, True))
    text(s, x+0.4, 5.05, 4.5, 0.9, [
        [(val, 30, TEAL, True)]], anchor=MSO_ANCHOR.TOP)
    text(s, x+3.0, 4.6, 2.0, 1.4, [[(lab,12.5,GRAY,True)],[(d,11.5,GRAY,False)]],
         align=PP_ALIGN.RIGHT, line_spacing=1.2)
source(s, "Fleckenstein 2025 (음악, CT 시술 209명) · Joo 2021 (VR, 요추 교감신경차단)")
footer(s, PAGE)

# =====================================================================
# 19 — 섹션 03
# =====================================================================
section("03", ["진료실에서, 이렇게 말하세요"], "시술 전·중·후 3단계 & 말 바꾸기 카드")

# 20~22 — 3단계
def stage(kick, kfill, title, quotes, note=None, src=None):
    s = newslide(PAPER)
    rect(s, 0.9, 1.5, 3.4, 4.7, fill=kfill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
    text(s, 1.2, 2.1, 2.8, 0.5, (kick, 15, WHITE, True))
    text(s, 1.2, 2.55, 3.05, 2.2, title, line_spacing=1.12)
    chip(s, 0.9, 0.75, "3단계 멘트", fill=TEAL)
    yy = 1.7
    for q in quotes:
        rect(s, 4.7, yy, 7.7, 1.15, fill=WHITE, line=TEALL, line_w=1.3, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.09, shadow=True)
        text(s, 5.0, yy, 0.55, 1.15, ("“", 34, TEAL, True), anchor=MSO_ANCHOR.MIDDLE)
        text(s, 5.5, yy, 6.7, 1.15, (q, 15.5, INK, False), anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.25)
        yy += 1.32
    if note:
        text(s, 4.7, yy+0.05, 7.7, 0.7, [[("● ", 14, TEAL, True), (note, 13.5, GRAY, False)]], line_spacing=1.2)
    if src:
        source(s, src)
    footer(s, PAGE)
    return s

# 20
stage("시술 전", DEEP, [[("순서를", 24, WHITE, True)],[("먼저 그려드립니다", 24, WHITE, True)]],
    ["먼저 소독하고 마취로 저리게 한 다음, 화면을 보며 정확한 지점까지 진행해요. 대부분 눌리는 느낌 정도예요.",
     "전체는 준비까지 30분 안팎, 실제 주사는 몇 분이면 끝납니다."],
    note="예측 가능성을 주면 예기 불안이 줄어듭니다.",
    src="Suls & Wan 1989 · Taddio 2015")

# 21
stage("시술 중", TEAL, [[("정상 감각을 짚고,", 24, WHITE, True)],[("곁을 지킵니다", 24, WHITE, True)]],
    ["누르는 느낌은 정상이에요. 날카롭게 찌릿하면 바로 말씀해 주세요.",
     "아주 잘하고 계세요. 절반쯤 지났어요. 숨을 천천히 내쉬어 볼까요?"],
    note="통제감·격려·주의분산을 함께 씁니다.",
    src="Lang 2005 · Boerner 2015")

# 22
stage("시술 후", GOLD, [[("잘 끝났음을", 24, WHITE, True)],[("함께 확인합니다", 24, WHITE, True)]],
    ["다 끝났습니다. 정말 잘 참으셨어요. 어지럽거나 불편한 곳은 없으세요?",
     "잠시 앉아서 쉬었다가 천천히 일어날게요."],
    note="주사 후 실신의 80%가 15분 이내 — 앉히거나 눕혀 15분 관찰.",
    src="U.S. CDC, Vaccine Administration Best Practices")

# 23~25 — Do / Don't
def dodont(kick, title, good, bad, src=None):
    s = newslide(PAPER)
    chip(s, 0.9, 0.8, kick, fill=TEAL)
    text(s, 0.87, 1.35, 11.5, 1.0, title)
    # good
    rect(s, 0.9, 2.75, 5.6, 3.15, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
    rect(s, 0.9, 2.75, 5.6, 0.75, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    rect(s, 0.9, 3.15, 5.6, 0.35, fill=TEAL)
    text(s, 0.9, 2.75, 5.6, 0.75, ("○  이렇게 말하세요", 17, WHITE, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    yy = 3.75
    for g in good:
        text(s, 1.3, yy, 4.9, 1.0, [[("“", 18, TEAL, True), (g, 15, INK, False), ("”", 18, TEAL, True)]], line_spacing=1.28)
        yy += 1.05
    # bad
    rect(s, 6.9, 2.75, 5.5, 3.15, fill=CORALB, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
    rect(s, 6.9, 2.75, 5.5, 0.75, fill=CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05)
    rect(s, 6.9, 3.15, 5.5, 0.35, fill=CORAL)
    text(s, 6.9, 2.75, 5.5, 0.75, ("×  이런 말은 피하세요", 17, WHITE, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    yy = 3.75
    for b in bad:
        text(s, 7.3, yy, 4.8, 1.0, [[("“", 18, CORAL, True), (b, 15, INK, False), ("”", 18, CORAL, True)]], line_spacing=1.28)
        yy += 1.05
    if src:
        source(s, src)
    footer(s, PAGE)
    return s

# 23
dodont("말 바꾸기 · 시작과 마취",
    [[("시작과 마취 직전", 30, INK, True)]],
    ["잠깐 시원하거나 뻐근하고 몇 초면 지나가요. 그다음엔 훨씬 편해지실 거예요.",
     "제가 셋을 세고 시작할게요. 준비되면 말씀해 주세요."],
    ["벌에 쏘인 것처럼 아플 거예요. 이게 제일 아픈 부분이에요.",
     "하나도 안 아파요. / 금방 끝나요."],
    src="Varelmann 2010")

# 24
dodont("말 바꾸기 · 압박감과 걱정",
    [[("압박감 · 신경 · 방사선 걱정", 28, INK, True)]],
    ["누르는 느낌은 정상이에요. 찌릿하면 바로 말씀해 주세요.",
     "표적은 신경이 아니라 뼈 위 정해진 지점이라, 뼈에 닿으면 멈춰요."],
    ["많이 아플 수 있어요, 참으세요.",
     "신경 근처라 잘못되면 마비될 수도 있어요."],
    src="Lang 2005 · 시술 안내 실무가이드")

# 25
dodont("말 바꾸기 · 격려와 마무리",
    [[("진행 중 격려와 마무리", 29, INK, True)]],
    ["아주 잘하고 계세요. 거의 다 됐어요.",
     "다 끝났어요. 생각보다 금방 끝났죠? 오늘 정말 잘 해내셨어요."],
    ["괜찮아요, 하나도 안 아파요, 전혀 안 아파요.",
     "그것 봐요, 많이 아팠죠? 다음엔 더 아플 수도 있어요."],
    src="McMurtry 2006/2010 (반복 안심·부정적 공감의 역효과)")

# =====================================================================
# 26 — 섹션 04
# =====================================================================
section("04", ["시술별로 바로 쓰는 문장"], "척추 중재시술 · 관절 주사 · 안전 관리")

# =====================================================================
# 27 — 척추 중재시술
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "척추 중재시술", fill=DEEP)
text(s, 0.87, 1.35, 11.5, 1.0, [[("“표적은 뼈, 확인은 안전”", 30, INK, True)]])
# 공통 안심
rect(s, 0.9, 2.6, 5.55, 3.35, fill=MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
text(s, 1.25, 2.9, 5.0, 0.6, ("공통 안심 메시지", 16, DEEP, True))
text(s, 1.25, 3.55, 5.0, 2.3, [
    [("투시 유도 내측지신경차단 ", 14, INK, False), ("7,500회·43,000개", 14, DEEP, True)],
    [("신경차단에서 ", 14, INK, False), ("중대 합병증 0건.", 14, TEAL, True)],
    [(" ", 7, INK, False)],
    [("“여러 번 촬영하는 건 위험 신호가", 14, INK, False)],
    [(" 아니라 그만큼 신중하게 하는 거예요.”", 14, INK, False)],
], line_spacing=1.4)
# 신경근차단 방사감
rect(s, 6.75, 2.6, 5.65, 3.35, fill=DEEP, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
text(s, 7.1, 2.9, 5.1, 0.6, ("신경근차단 — 가장 중요한 한마디", 15, TEALL, True))
text(s, 7.1, 3.6, 5.1, 2.3, [
    [("“다리로 찌릿·전기 오는 느낌은", 15.5, WHITE, False)],
    [(" 바늘이 제 위치에 왔다는 신호예요.", 15.5, WHITE, False)],
    [(" 움직이지 마시고 ", 15.5, WHITE, False), ("‘찌릿해요’", 15.5, GOLD, True)],
    [(" 라고 말로만 알려주세요.”", 15.5, WHITE, False)],
], line_spacing=1.4)
text(s, 7.1, 5.5, 5.1, 0.5, ("이 한마디가 신경 손상을 막는 안전장치입니다.", 12.5, TEALL, False))
source(s, "Manchikanti 2012 · Sato 2013 (방사감 = 위치 확인·손상 회피 신호)")
footer(s, PAGE)

# =====================================================================
# 28 — 관절 주사
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "사지 관절 주사", fill=DEEP)
text(s, 0.87, 1.35, 11.5, 1.0, [[("기대치를 함께 관리합니다", 30, INK, True)]])
joints = [
    ("무릎", "몇 주 통증을 줄여주는 ‘다리’. 운동·체중관리를 함께.", "6주 넘는 이득은 불확실 (Cochrane)"),
    ("어깨", "바늘 안 보이게 뒤에서. 첫 시술·공복은 실신 위험.", "어깨 힘 빼고, 어지러우면 바로 눕히기"),
    ("팔꿈치", "단기 효과·장기 재발. 주사 반복보다 운동 병행.", "장기적으로는 오히려 예후가 나쁠 수 있음"),
]
for i,(t,d,note) in enumerate(joints):
    y = 2.55 + i*1.2
    rect(s, 0.9, y, 11.5, 1.05, fill=WHITE if i%2==0 else MINT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08, shadow=(i%2==0))
    rect(s, 0.9, y, 1.7, 1.05, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
    rect(s, 1.9, y, 0.7, 1.05, fill=TEAL)
    text(s, 0.9, y, 1.7, 1.05, (t, 21, WHITE, True), align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    text(s, 2.9, y+0.14, 6.4, 0.8, (d, 15, INK, False), anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.15)
    text(s, 9.35, y, 3.0, 1.05, (note, 12, GRAY, False), anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.2)
text(s, 0.9, 6.25, 11.5, 0.5, [[("공통  ", 13, DEEP, True),
    ("“다음 날 잠깐 더 아플 수 있어요(흔한 반응, 2~3일). 주사액을 체온으로 데우면 덜 아파요.”", 13, GRAY, False)]])
footer(s, PAGE)

# =====================================================================
# 29 — 안전
# =====================================================================
s = newslide(PAPER)
chip(s, 0.9, 0.8, "안전 관리", fill=CORAL)
text(s, 0.87, 1.35, 11.5, 1.0, [[("쓰러짐과 바늘 공포에 대비합니다", 29, INK, True)]])
# 실신
rect(s, 0.9, 2.6, 5.6, 3.35, fill=WHITE, line=CORAL, line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
text(s, 1.25, 2.9, 5.0, 0.6, ("미주신경성 실신", 17, CORAL, True))
text(s, 1.25, 3.6, 5.05, 2.3, [
    [("· 평생 유병률 약 ", 14, INK, False), ("16%", 14, CORAL, True), (" — 흔합니다", 14, INK, False)],
    [("· 실신 과거력은 ", 14, INK, False), ("반드시 사전 선별", 14, DEEP, True)],
    [("· 전조(어지럼·식은땀·메스꺼움) 교육", 14, INK, False)],
    [("· 발생 시 눕히고 ", 14, INK, False), ("다리 거상 → 15분 관찰", 14, DEEP, True)],
], line_spacing=1.55)
# 바늘 공포
rect(s, 6.75, 2.6, 5.65, 3.35, fill=WHITE, line=TEAL, line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05, shadow=True)
text(s, 7.1, 2.9, 5.1, 0.6, ("바늘 공포", 17, TEAL, True))
text(s, 7.1, 3.6, 5.1, 2.3, [
    [("· 아주 흔한 일 — ", 14, INK, False), ("정상화·공감", 14, DEEP, True), ("으로", 14, INK, False)],
    [("  “무서워하는 건 흔한 일이에요.”", 14, INK, False)],
    [("· 주사 팔은 힘 빼고, 반대쪽만 긴장", 14, INK, False)],
    [("· ", 14, INK, False), ("적용된 긴장(applied tension)", 14, TEAL, True), ("으로", 14, INK, False)],
    [("  실신 예방 — 근거가 확립된 기법", 14, INK, False)],
], line_spacing=1.5)
source(s, "Salari 2024 · Williams 2022 · McLenon & Rogers 2019")
footer(s, PAGE)

# =====================================================================
# 30 — 마무리
# =====================================================================
s = newslide(DEEP)
rect(s, 0, 0, 13.333, 0.28, fill=TEAL)
rect(s, 0, 7.22, 13.333, 0.28, fill=GOLD)
chip(s, 0.95, 1.05, "한 줄 요약", fill=TEAL)
text(s, 0.9, 1.75, 11.5, 1.9, [
    [("통증 단어를 빼고,", 44, WHITE, True)],
    [("안심을 더하세요.", 44, TEALL, True)],
], line_spacing=1.08)
line(s, 0.98, 4.05, 2.1, 0.05, GOLD)
steps = ["정상 감각을 미리 알리고", "통제권과 예고를 주고", "반복 안심 대신 격려·주의분산", "끝나면 15분 관찰"]
for i,t in enumerate(steps):
    x = 0.95 + (i%2)*5.9
    y = 4.4 + (i//2)*0.95
    text(s, x, y, 5.7, 0.8, [[("○  ", 18, GOLD, True), (t, 17, WHITE, False)]], anchor=MSO_ANCHOR.MIDDLE)
text(s, 0.95, 6.5, 11, 0.6, ("오늘 진료실에서, 한 문장부터 바꿔 보세요.", 16, TEALL, False))

prs.save("/home/user/ppt-work/친절_통증소통_가이드_30.pptx")
print("OK — slides:", len(prs.slides._sldIdLst), "PAGE counter:", PAGE)
