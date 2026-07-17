# -*- coding: utf-8 -*-
"""RLS 치료 문헌고찰 DOCX 생성 — 주사·충격파·약물의 치료효과."""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

KFONT = "맑은 고딕"
NAVY = RGBColor(0x1B, 0x35, 0x5E)
TEAL = RGBColor(0x1F, 0x6E, 0x70)
MUTE = RGBColor(0x55, 0x60, 0x6B)
RED  = RGBColor(0xA3, 0x30, 0x25)

doc = Document()

# base style
st = doc.styles['Normal']
st.font.name = 'Calibri'
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn('w:eastAsia'), KFONT)
for sec in doc.sections:
    sec.top_margin = Inches(0.9); sec.bottom_margin = Inches(0.9)
    sec.left_margin = Inches(1.0); sec.right_margin = Inches(1.0)

def kfont(run, size=None, color=None, bold=None, italic=None):
    run.font.name = 'Calibri'
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    rf.set(qn('w:eastAsia'), KFONT); rf.set(qn('w:ascii'), 'Calibri'); rf.set(qn('w:hAnsi'), 'Calibri')
    if size is not None: run.font.size = Pt(size)
    if color is not None: run.font.color.rgb = color
    if bold is not None: run.font.bold = bold
    if italic is not None: run.font.italic = italic

def para(text="", size=10.5, color=None, bold=False, italic=False, align=None,
         before=2, after=4, ls=1.12):
    p = doc.add_paragraph()
    if align: p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = ls
    if text:
        r = p.add_run(text); kfont(r, size, color, bold, italic)
    return p

def runs_para(segs, size=10.5, before=2, after=4, ls=1.12, align=None):
    """segs: list of (text, dict-of-opts)"""
    p = doc.add_paragraph()
    if align: p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(before); pf.space_after = Pt(after); pf.line_spacing = ls
    for txt, o in segs:
        r = p.add_run(txt)
        kfont(r, o.get('size', size), o.get('color'), o.get('bold', False), o.get('italic', False))
    return p

def h1(num, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    # bottom border
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement('w:pBdr'); bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'),'single'); bottom.set(qn('w:sz'),'12'); bottom.set(qn('w:space'),'4')
    bottom.set(qn('w:color'),'1F6E70'); pbdr.append(bottom); pPr.append(pbdr)
    if num:
        r0 = p.add_run(num + "  "); kfont(r0, 15, TEAL, True)
    r = p.add_run(text); kfont(r, 15, NAVY, True)
    return p

def h2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11); p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run("▍ "); kfont(r, 11.5, TEAL, True)
    r2 = p.add_run(text); kfont(r2, 12, NAVY, True)
    return p

def bullet(text, lvl=0, color=None, bold=False):
    p = doc.add_paragraph(style=None)
    p.paragraph_format.left_indent = Inches(0.28 + lvl*0.28)
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    mark = "•  " if lvl == 0 else "–  "
    rm = p.add_run(mark); kfont(rm, 10.5, TEAL if lvl==0 else MUTE, True)
    r = p.add_run(text); kfont(r, 10.5, color, bold)
    return p

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'),'clear'); sh.set(qn('w:fill'),hexcolor)
    tcPr.append(sh)

def set_cell(cell, text, size=9.5, color=None, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]; p.alignment = align
    p.paragraph_format.space_before = Pt(1); p.paragraph_format.space_after = Pt(1)
    r = p.add_run(text); kfont(r, size, color, bold)

def _cant_split(row, header=False):
    trPr = row._tr.get_or_add_trPr()
    cs = OxmlElement('w:cantSplit'); trPr.append(cs)
    if header:
        th = OxmlElement('w:tblHeader'); trPr.append(th)

def add_table(headers, rows, widths, header_fill="1B355E"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.style = 'Table Grid'
    _cant_split(t.rows[0], header=True)
    for i, htext in enumerate(headers):
        c = t.rows[0].cells[i]; shade(c, header_fill)
        set_cell(c, htext, 9.5, RGBColor(0xFF,0xFF,0xFF), True, WD_ALIGN_PARAGRAPH.CENTER)
    for r_i, row in enumerate(rows):
        trow = t.add_row(); _cant_split(trow)
        cells = trow.cells
        for i, val in enumerate(row):
            if r_i % 2 == 1: shade(cells[i], "EEF2F6")
            al = WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_cell(cells[i], val, 9.3, None, False, al)
    for i, w in enumerate(widths):
        for row in t.rows:
            row.cells[i].width = Inches(w)
    return t

# ============================================================ TITLE
p = para("하지불안증후군(RLS) 치료 문헌고찰", 21, NAVY, True, align=WD_ALIGN_PARAGRAPH.CENTER, before=10, after=2)
para("주사 · 체외충격파 · 약물의 치료효과 정리", 14, TEAL, True, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("Restless Legs Syndrome (Willis–Ekbom Disease) — Efficacy of Injection, ESWT, and Pharmacotherapy",
     10.5, MUTE, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=8)
para("작성일 2026-07  ·  구성: 서론/감별 → 주사 → 충격파 → 약물 → 종합 결론 → 참고문헌",
     9.5, MUTE, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
para("※ 임상·교육·연구 참고용 문헌고찰입니다. 개별 환자의 진단·처방 결정은 담당 의사(신경과/수면의학 등)의 판단에 따릅니다.",
     9, MUTE, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, after=6)

# ============================================================ 서론
h1("", "서론 — RLS의 이해와 치료 원칙")
h2("정의·진단 (IRLSSG 2014 필수 5기준)")
para("하지불안증후군(RLS)은 다음 5가지를 모두 충족할 때 진단한다. RLS는 야간 하지경련(NLC)과 흔히 혼동되나, 치료가 근본적으로 다르므로 감별이 선행되어야 한다.")
for b in [
    "다리를 움직이고 싶은 충동(대개 불쾌한 다리 감각을 동반)",
    "안정·비활동 시 증상이 시작·악화",
    "움직임(걷기·스트레칭)으로 부분적·일시적 완화",
    "저녁·밤에 악화되는 뚜렷한 일주기(circadian) 패턴",
    "다른 질환(다리경련·자세성 불편·근육통·정맥울혈 등)으로 더 잘 설명되지 않음(mimic 배제)",
]:
    bullet(b)
runs_para([("NLC와의 감별: ", {'bold':True,'color':RED}),
           ("RLS는 ‘움직이고 싶은 충동’이 핵심이며 움직이면 완화되고 만져지는 근경직이 없다. 반면 NLC는 통증성 근수축·촉지되는 근경직이 특징이고 족배굴곡(스트레칭)으로 완화된다.", {})])

h2("유병률·병태생리")
for b in [
    "유병률: 성인 약 5~10%. 여성·고령·철결핍·임신·말기신부전에서 증가.",
    "뇌 철분 결핍: 혈청 철분이 정상이어도 흑질·기저핵 등 뇌 국소 철분이 부족 → 도파민 신호 이상. 치료의 생물학적 근거.",
    "도파민 이상: 야간 도파민 기능 저하 가설. 도파민제가 단기 효과를 내나 장기 사용 시 augmentation을 유발.",
    "아데노신 저하 가설(최근): 뇌 철분 결핍이 아데노신 신호를 낮춰 과흥분 유발 → dipyridamole 등 새 표적의 근거.",
]:
    bullet(b)

h2("치료 원칙 (2024/2025 AASM 지침 방향)")
for b in [
    "① 철분 상태(ferritin/TSAT) 평가·교정을 모든 환자의 기반 치료로 한다.",
    "② 약물은 alpha-2-delta 리간드(gabapentin enacarbil·gabapentin·pregabalin)를 1차로 권고(강한 권고).",
    "③ 도파민 작용제(pramipexole·ropinirole·rotigotine)·levodopa는 augmentation 위험으로 장기 표준 사용을 권고하지 않는다.",
    "④ 유발·악화 요인(항히스타민·항우울제·도파민 차단제·철결핍·수면부족)을 교정한다.",
]:
    bullet(b)

# ============================================================ 요약표
h1("", "핵심 요약 — 3개 치료 축의 근거")
add_table(
    ["치료 축","대표 치료","RLS 치료효과 근거","근거수준","요지"],
    [["주사","IV 철분 (ferric carboxymaltose)","다기관 RCT·메타분석","Level I","철결핍 동반 시 효과적 — AASM 강한 권고"],
     ["주사","보툴리눔 독소(BoNT-A)","소규모 RCT 2편·SR/MA","Level II(소표본)","근거 약함·혼재. 대규모 RCT 필요"],
     ["주사","정맥 경화요법/소작","후향·관찰","Level III~IV","정맥류·CVI 동반 RLS에서 증상 개선"],
     ["충격파","체외충격파(ESWT)","RLS 표적 연구 없음","근거 없음","권고 불가 — 비골신경자극이 근거 있는 대안"],
     ["약물","α2δ 리간드","다수 RCT","Level I","1차 치료(강한 권고)"],
     ["약물","도파민 작용제","다수 RCT / augmentation","Level I(효능)","단기 효과O, 장기 권고 안 함"],
     ["약물","dipyridamole·오피오이드","RCT·전문가","Level II~","조건부·난치성 선택지"]],
    [0.75, 2.05, 1.7, 1.0, 2.4])
para("근거수준: Level I(메타분석/다수 RCT) · II(개별/소규모 RCT) · III(비무작위·코호트) · IV(관찰·증례).",
     8.7, MUTE, italic=True, before=3)

# ============================================================ PART 1 주사
h1("Part 1.", "주사(Injection) 치료의 효과")

h2("1-1. 정맥 철분 주사 (IV Ferric Carboxymaltose) — 가장 근거가 확실한 ‘주사’ 치료")
para("RLS의 주사 치료 중 근거가 가장 강한 것은 정맥 철분이다. 뇌 철분 결핍이라는 핵심 병태를 직접 교정한다.")
runs_para([("Earley 등(2024, Sleep) 다기관 RCT: ", {'bold':True}),
           ("IRLS ≥15인 성인 209명을 FCM 750 mg(0일·5일 2회) vs 위약으로 무작위 배정. 42일째 IRLS 총점과 CGI(much/very much improved) 비율이 위약 대비 유의하게 개선.", {})])
runs_para([("메타분석(2024, Sleep Med, 537명): ", {'bold':True}),
           ("IV FCM이 RLS 중증도를 임상적으로 유의하게 개선하고 안전성이 양호함을 확인.", {})])
runs_para([("IRLSSG 철분 치료 지침(Allen 등, 2018): ", {'bold':True}),
           ("모든 RLS 환자에서 철분 치료를 고려. 경구 철분은 ferritin ≤75 μg/L에서, 정맥 철분은 경구가 부적절하거나 ferritin ≤100 μg/L일 때 고려. 중등도~중증에서 FCM 1000 mg 단회(ferritin <300 & TSAT <45%)는 Level A 근거.", {})])
for b in [
    "AASM 2025: 철결핍 동반 RLS에서 IV FCM을 강한 권고. ferritin <100 μg/L 또는 TSAT <45%가 대표 기준.",
    "제형: ferric carboxymaltose(FCM) 1000 mg(또는 750 mg×2)이 대표. 경구 철분은 ferritin ≥75에서 흡수가 미미해 정맥 투여가 유리.",
    "안전: FCM은 내약성이 양호하나 일과성 저인산혈증이 알려져 있어 반복 투여 시 모니터링.",
]:
    bullet(b)
runs_para([("요점: ", {'bold':True,'color':TEAL}),
           ("‘주사’ 치료를 논할 때 RLS에서 근거가 가장 확실한 것은 정맥 철분이며, 철결핍(ferritin 저하)이 확인된 환자에서 우선 고려된다.", {})])

h2("1-2. 보툴리눔 독소 주사 (BoNT-A) — 근거 약함·혼재")
runs_para([("Mittal 등(2018, Toxins) 이중맹검 위약대조 교차연구: ", {'bold':True}),
           ("중등도~중증(IRLS >11) 24명에게 incobotulinumtoxinA 100단위를 전경골근·비복근·대퇴이두근에 주사. 4주·6주에 중증(IRLS >21)→경증/중등도(≤20) 전환이 위약 대비 유의, 6주에 통증(VAS)도 유의 개선. Patient Global Impression 개선도 우위.", {})])
runs_para([("체계적 문헌고찰·메타분석(Healthcare, 2021): ", {'bold':True}),
           ("RCT 2편(총 27명)에서 IRLS의 표준화 평균차 −0.819(95% CI −1.377~−0.262)로 위약 대비 개선. 그러나 표본이 매우 작아 확정적 결론은 불가하며, 최적 용량·안전성·장기효과 규명을 위한 대규모 RCT가 필요.", {})])
for b in [
    "Ghorayeb의 공개표지 연구: abobotulinumtoxinA 진피내 주사 26명에서 IRLS 개선 보고(대조군 없음).",
    "이상반응은 대개 일시적·자기한정적. 다만 표준치료로 볼 근거는 아직 부족.",
]:
    bullet(b)
runs_para([("평가: ", {'bold':True,'color':RED}),
           ("보툴리눔 독소는 소규모 연구에서 긍정 신호가 있으나 근거가 약하고 혼재한다. RLS의 표준 주사 치료가 아니며 연구적 맥락에서만 고려한다.", {})])

h2("1-3. 정맥 경화요법·소작 (정맥류/만성정맥부전 동반 RLS)")
runs_para([("Pyne 등(2023, JVIR): ", {'bold':True}),
           ("야간 다리 증상 환자에서 외측 진피하 정맥총(LSVP)의 역류가 높은 빈도로 확인되었고, 초음파 유도 폼경화요법 후 상당수가 호전(추적 유지).", {})])
runs_para([("Sundaresan 등(2019, Cureus): ", {'bold':True}),
           ("하지정맥 치료(고주파소작 + 폼경화요법) 후 RLS 척도(IRLS)가 평균 19.83 → 7.89로 약 63% 호전.", {})])
for b in [
    "기전: 정맥판막 부전 → 하지 정맥울혈·근피로가 RLS 증상에 기여. 원인 정맥을 치료하면 증상이 감소할 수 있음.",
    "적용: 정맥류·만성정맥부전이 동반된 RLS 표현형에서 표적 치료로 의미. 특발성 RLS 전반에 대한 표준치료는 아님.",
]:
    bullet(b)

# ============================================================ PART 2 충격파
h1("Part 2.", "체외충격파(ESWT) 치료의 효과")
h2("2-1. 직접 근거 — 없음 (정직한 평가)")
para("RLS를 결과변수로 ESWT의 효과를 평가한 무작위대조시험·전향적 연구·증례는 검색되지 않았다(2026-07 기준). 즉 ESWT의 RLS 치료효과에 대한 직접 근거는 존재하지 않으며, 효과를 창작하지 않는다.")
for b in [
    "ESWT의 확립된 근거는 근골격계 통증(족저근막염 등)·경직·근경련 영역이며, 이는 RLS와 병태가 다르다.",
    "이론적 타당성(가설): ESWT의 미세순환 개선·산화질소(NO)·운동신경원 흥분성 조절이 거론될 수 있으나, RLS의 핵심 병태(뇌 철분 결핍·도파민·아데노신)와 직접 연결하는 근거는 없다.",
]:
    bullet(b)

h2("2-2. 근거가 있는 비약물·기기 대안 — 말초 비골신경 자극")
para("‘약물이 아닌 물리·기기 치료’를 원한다면, RLS에서 실제 근거가 있는 것은 충격파가 아니라 말초 비골신경 자극이다.")
runs_para([("Charlesworth 등(2023, J Clin Sleep Med): ", {'bold':True}),
           ("양측 고빈도 비침습적 비골신경자극(NPNS/TOMAC)을 중등도~중증 RLS에서 sham 대조로 평가. 다리 근육의 긴장성 활성을 유발하며 수면을 방해하지 않고 증상을 개선.", {})])
for b in [
    "AASM 2025: 양측 고빈도 비골신경 자극을 조건부 권고(비약물 옵션).",
    "비침습·비약물로 augmentation·약물 부작용을 피하려는 환자에 대안이 될 수 있음.",
]:
    bullet(b)
runs_para([("결론(충격파): ", {'bold':True,'color':RED}),
           ("ESWT는 RLS에 대한 근거가 없어 권고할 수 없다. 비약물 치료가 필요하면 근거가 있는 비골신경 자극을 우선 고려한다.", {})])

# ============================================================ PART 3 약물
h1("Part 3.", "약물(Pharmacotherapy) 치료의 효과 — 근거의 중심")
para("RLS 치료효과의 근거가 가장 두텁게 축적된 축은 약물이다. 2024/2025 AASM 지침이 1차 약물을 도파민제에서 α2δ 리간드로 전환한 점이 핵심 변화다.")

h2("3-1. 철분(경구) — 기반 치료")
bullet("경구 철분(예: ferrous sulfate + 비타민 C)은 ferritin ≤75 μg/L에서 고려. 흡수가 낮거나 불충분하면 정맥 철분(Part 1-1)으로 전환.")

h2("3-2. α2δ 리간드 (gabapentin enacarbil·gabapentin·pregabalin) — 1차")
runs_para([("Allen 등(2014, NEJM) 52주 RCT: ", {'bold':True}),
           ("pregabalin 300 mg이 RLS에 효과적이며, augmentation 발생률이 pregabalin 1.7% vs pramipexole 0.5 mg 9.0%로 유의하게 낮음.", {})])
for b in [
    "Gabapentin enacarbil: 수면다원검사 RCT(Winkelman 2011)에서 각성시간·PLM 감소, 장기 유지 RCT(Bogan 2010)에서 재발 억제.",
    "AASM 2025: gabapentin enacarbil·gabapentin·pregabalin을 1차 강한 권고(gabapentin·pregabalin은 off-label).",
    "부작용: 어지럼·졸림·부종·체중증가. 고령·신기능 저하 시 감량.",
]:
    bullet(b)

h2("3-3. 도파민 작용제 (pramipexole·ropinirole·rotigotine) — 후순위")
runs_para([("Winkelman 등(2006, Neurology): ", {'bold':True}),
           ("pramipexole 12주 RCT에서 IRLS·CGI 유의 개선 — 단기 효능은 확립.", {})])
for b in [
    "핵심 제약 — Augmentation: 수개월~수년 사용 후 증상이 오히려 악화되고 발현이 이른 시각으로 당겨지며 부위가 전이. 도파민제 사용자에서 연 약 7~10% 발생.",
    "AASM 2025: 도파민 작용제·levodopa를 augmentation 위험으로 장기 표준 사용에 대해 ‘권고하지 않음(against)’.",
    "이미 복용 중이면 augmentation 징후를 정기 점검하고, 발견 시 철분 재평가 후 감량/전환(α2δ 리간드)을 고려. 급격한 중단은 반동 유발 → 단계적 조정.",
]:
    bullet(b)

h2("3-4. 오피오이드 — 난치성/augmentation 관리")
bullet("저용량 오피오이드(예: 서방형 oxycodone)는 난치성·augmentation 상황에서 조건부 사용. 부프레노르핀은 중추성 수면무호흡·호흡억제 위험이 상대적으로 낮음. 진정·의존·호흡 위험으로 신중.")

h2("3-5. Dipyridamole — 신규 표적(아데노신)")
runs_para([("Garcia-Borreguero 등(2021, Mov Disord) 교차 RCT: ", {'bold':True}),
           ("dipyridamole(ENT1/ENT2 억제로 뇌 아데노신 증가)이 IRLS를 24.1 → 11.1로 개선(위약 23.7 → 18.7). 감각·운동 증상과 수면 모두 호전. 아데노신 가설을 지지하는 조건부 선택지.", {})])

h2("3-6. AASM 2025 지침 요약")
add_table(
    ["구분","약물","권고"],
    [["1차","gabapentin enacarbil·gabapentin·pregabalin","강한 권고"],
     ["기반","철분(경구/IV FCM)","철결핍 교정 강조"],
     ["후순위","pramipexole·ropinirole·rotigotine·levodopa","장기 사용 권고 안 함(augmentation)"],
     ["조건부","dipyridamole, 서방형 oxycodone/μ-오피오이드, 양측 비골신경 자극","조건부 권고"]],
    [1.1, 4.2, 2.6])

# ============================================================ 종합 결론
h1("", "종합 결론 및 임상 접근")
h2("무엇이 확실하고 무엇이 불확실한가")
for b in [
    "가장 확실: 진단 확정(IRLSSG 5기준) + 철분 상태 교정 + α2δ 리간드 1차 약물.",
    "확실한 주사 치료: 정맥 철분(FCM)이 철결핍 동반 RLS에서 효과적(RCT·메타분석·강한 권고).",
    "약하거나 혼재: 보툴리눔 독소(소규모 RCT), 정맥 경화요법(정맥질환 동반 표현형).",
    "근거 없음: 체외충격파(ESWT)는 RLS 표적 연구가 없어 권고 불가. 비약물이 필요하면 비골신경 자극이 근거 있는 대안.",
    "주의: 도파민 작용제는 단기 효과에도 불구하고 augmentation 때문에 장기 1차에서 밀려났다.",
]:
    bullet(b)

h2("단계적 접근(제안)")
for i, b in enumerate([
    "진단 확정 및 유발요인 검토(약물·수면·철결핍) + ferritin/TSAT 측정.",
    "철분 교정 — 경구(ferritin ≤75) 또는 정맥 FCM(ferritin ≤100 또는 경구 부적절).",
    "1차 약물 — α2δ 리간드(pregabalin/gabapentin/gabapentin enacarbil).",
    "불응성 — dipyridamole, 저용량 오피오이드, 양측 비골신경 자극 고려.",
    "주사: 철결핍이면 정맥 철분 우선. 보툴리눔은 연구단계, 충격파는 근거 없음.",
], 1):
    bullet(f"{i}단계 — {b}")

runs_para([("최종 메시지: ", {'bold':True,'color':NAVY}),
           ("RLS 치료효과의 근거는 ‘약물(α2δ 리간드) + 철분(경구·정맥)’에 집중되어 있다. 주사 중에서는 정맥 철분이 근거가 확실하고, 보툴리눔은 연구단계이며, 체외충격파는 RLS에 대한 근거가 없다.", {})],
          before=6)

# ============================================================ 참고문헌
h1("", "참고문헌 (References)")
refs = [
 "Allen RP, Picchietti DL, Garcia-Borreguero D, et al. Restless legs syndrome/Willis-Ekbom disease diagnostic criteria: updated IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-873. PMID 25023924.",
 "Winkelman JW, Berkowski JA, DelRosso LM, et al. Treatment of restless legs syndrome and periodic limb movement disorder: an American Academy of Sleep Medicine clinical practice guideline. J Clin Sleep Med. 2025;21(1):137-152. PMID 39324694.",
 "Allen RP, Picchietti DL, Auerbach M, et al. Evidence-based and consensus clinical practice guidelines for the iron treatment of restless legs syndrome/Willis-Ekbom disease in adults and children: an IRLSSG task force report. Sleep Med. 2018;41:27-44. PMID 29425576.",
 "Earley CJ, García-Borreguero D, Falone M, Winkelman JW. Clinical efficacy and safety of intravenous ferric carboxymaltose for treatment of restless legs syndrome: a multicenter, randomized, placebo-controlled clinical trial. Sleep. 2024;47(7):zsae095. PMID 38625730.",
 "Clinical efficacy and safety of IV ferric carboxymaltose in restless legs syndrome: a meta-analysis of 537 patients. Sleep Med. 2024. PMID 39326219.",
 "Mittal SO, Machado D, Richardson D, Dubey D, Jabbari B. Botulinum toxin in restless legs syndrome—a randomized double-blind placebo-controlled crossover study. Toxins (Basel). 2018;10(10):401. PMCID PMC6215171.",
 "Effectiveness and Safety of Botulinum Toxin Type A in Treatment of Restless Legs Syndrome: A Systematic Review and Meta-Analysis. Healthcare (Basel). 2021;9(11):1538. PMCID PMC8623507.",
 "Pyne R, Shah S, Stevens L, Bress J. Lateral subdermic venous plexus insufficiency: the association of varicose veins with restless legs syndrome and nocturnal leg cramps. J Vasc Interv Radiol. 2023;34(4):534-542. PMID 36526075.",
 "Sundaresan S, Migden MR, Silapunt S. Treatment of leg veins for restless leg syndrome: a retrospective review. Cureus. 2019;11(4):e4368. PMID 31192073.",
 "Charlesworth JD, Adlou B, Singh H, Buchfuhrer MJ. Bilateral high-frequency noninvasive peroneal nerve stimulation evokes tonic leg muscle activation for sleep-compatible reduction of restless legs syndrome symptoms. J Clin Sleep Med. 2023;19(7):1199-1209. PMID 36856064.",
 "Allen RP, Chen C, Garcia-Borreguero D, et al. Comparison of pregabalin with pramipexole for restless legs syndrome. N Engl J Med. 2014;370(7):621-631. PMID 24521108.",
 "Winkelman JW, Sethi KD, Kushida CA, et al. Efficacy and safety of pramipexole in restless legs syndrome. Neurology. 2006;67(6):1034-1039. PMID 16931507.",
 "Winkelman JW, Bogan RK, Schmidt MH, et al. Randomized polysomnography study of gabapentin enacarbil in subjects with restless legs syndrome. Mov Disord. 2011;26(11):2065-2072. PMID 21611981.",
 "Bogan RK, Bornemann MAC, Kushida CA, et al. Long-term maintenance treatment of restless legs syndrome with gabapentin enacarbil: a randomized controlled study. Mayo Clin Proc. 2010;85(6):512-521. PMID 20511481.",
 "Garcia-Borreguero D, Guitart X, Garcia Malo C, et al. A randomized, placebo-controlled crossover study with dipyridamole for restless legs syndrome. Mov Disord. 2021;36(10):2387-2392. PMID 34137476.",
]
for i, r in enumerate(refs, 1):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3); p.paragraph_format.first_line_indent = Inches(-0.3)
    p.paragraph_format.space_after = Pt(3); p.paragraph_format.line_spacing = 1.08
    rn = p.add_run(f"{i}. "); kfont(rn, 9.3, TEAL, True)
    rr = p.add_run(r); kfont(rr, 9.3)

para("인용·검증 메모: 상기 서지정보는 PubMed·학술지 페이지 목록을 웹 검색으로 대조해 정리하였다. RLS를 표적으로 한 체외충격파(ESWT)의 임상연구는 확인되지 않아 ‘직접 근거 없음’으로 명시하였으며, 근거를 창작하지 않았다. 개별 인용의 권·페이지 일부는 원문 재확인을 권장한다.",
     8.7, MUTE, italic=True, before=8)

doc.save("/home/user/ppt-work/RLS_치료_문헌고찰.docx")
print("saved docx, paragraphs:", len(doc.paragraphs))
