# -*- coding: utf-8 -*-
"""LSB(요추교감신경차단) 웹 발표 덱 전용 빌더 — Pretendard 서브셋 임베드.
build_web_decks.py의 LSB 정의를 기반으로 하되, LSB 한 덱만 재생성한다(NLC/RLS 불변).

경로는 모두 저장소 기준(상대)이라 어느 컴퓨터에서도 그대로 돈다.
Pretendard 폰트는 아래 순서로 찾는다:
  1) 환경변수 PRETENDARD_DIR
  2) <저장소>/fonts
  3) /tmp/pretendard
없으면 받는 법을 안내하고 멈춘다:
  mkdir -p fonts && cd fonts && npm pack pretendard \
    && tar xzf pretendard-*.tgz --strip-components=4 package/dist/public/static
"""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from lsb_figures import AXIAL_SVG, CONTRAST_SVG, GF_SVG, SAGITTAL_SVG, CORONAL_SVG, AVOID_SVG
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
def PMC(x): return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x}/"
def CDSR(x): return f"https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.{x}/full"

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(REPO, "문헌고찰_NLC_RLS_LSB", "03_LSB", "assets")

def IMG(name, alt="", jpeg=False, q=90):
    """assets/의 래스터 그림을 data URI <img>로 임베드(덱 단일 파일 유지).

    사진성 그림(투시상·3D 렌더)은 jpeg=True로 재인코딩해 용량을 1/4로 줄인다.
    선화(해부 도판)는 글자 가장자리에 링잉이 생기므로 PNG 그대로 둔다.
    """
    path = os.path.join(ASSETS, name)
    if jpeg:
        from PIL import Image
        buf = io.BytesIO()
        Image.open(path).convert("RGB").save(
            buf, "JPEG", quality=q, optimize=True, progressive=True)
        data, mime = buf.getvalue(), "jpeg"
    else:
        data, mime = open(path, "rb").read(), "png"
    b64 = base64.b64encode(data).decode()
    return f'<img src="data:image/{mime};base64,{b64}" alt="{esc_attr(alt)}">'


def RAW(name, mime, alt=""):
    """이미 덱 크기에 맞춰 압축된 파일을 재인코딩 없이 그대로 임베드한다."""
    data = open(os.path.join(ASSETS, name), "rb").read()
    b64 = base64.b64encode(data).decode()
    return f'<img src="data:image/{mime};base64,{b64}" alt="{esc_attr(alt)}">'


def FIG(name, fallback, alt="", q=88):
    """assets/<name>.{webp,png,jpg} 가 있으면 그 그림을, 없으면 기존 SVG 도해를 쓴다.

    힉스필드로 생성한 그림이 들어오는 즉시 덱이 자동으로 교체된다.
    webp/jpg는 이미 덱 표시 크기(가로 1400px)에 맞춰 인코딩해 두었으므로
    재압축하지 않고 그대로 넣는다(이중 손실 방지). png만 JPEG로 줄인다.
    """
    for ext, mime in (("webp", "webp"), ("jpg", "jpeg")):
        if os.path.exists(os.path.join(ASSETS, f"{name}.{ext}")):
            return RAW(f"{name}.{ext}", mime, alt or name)
    if os.path.exists(os.path.join(ASSETS, name + ".png")):
        return IMG(name + ".png", alt or name, jpeg=True, q=q)
    return fallback


def esc_attr(s):
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))

LSB = [
 # ═══════════ 표지 ═══════════
 {'t':'title','eyebrow':'Lumbar Sympathetic Block · 문헌고찰','title':'요추교감신경차단',
  'sub':'방법 · 적응증 · 효과','order':'Technique · Indications · Efficacy','series':SERIES},
 # ═══════════ 질환 — 어떤 병에 쓰나 (적응증이 먼저) ═══════════
 {'t':'table','eyebrow':'질환 · 가장 먼저','tag':('적응증','ink'),
  'title':'LSB는 어떤 병에 쓰나 — 적응증 우선순위',
  'foot':'ABI = 발목-상완 혈압비(정상 0.9–1.3, 낮으면 동맥 협착) · 공통 관문은 SMP인가, 확정은 차단 반응 · 근거는 임상 비중과 역순(③만 위약대조 RCT 양성, PMID 3898891)',
  'headers':['질환 (임상 비중 순)','핵심 소견 — 감별점','LSB'],
  'rows':[
   ['<b>① SMP 우세형</b> (원인 불명)','작열통·이질통 + 좌우 <b>온도·색·발한</b> 차 · <b>신경 하나의 영역보다 넓게</b>','<b>○</b>'],
   ['<b>② 당뇨병성 신경병증</b>','양측 <b>‘양말’ 분포</b> 저림·화끈거림 · <b>야간 악화</b> · 모노필라멘트·진동감각 저하','<b>○</b>'],
   ['<b>③ 허혈성 안정통</b> (PAD·CLI)','파행 → 야간 안정통 · <b>다리를 내리면 완화</b> · 차고 창백한 발 · <b>ABI↓</b>','<b>○</b>'],
   ['<b>④ 하지 CRPS</b> (I/II)','손상 정도에 비해 <b>과도한</b> 작열통·이질통 · 부종 · 색/온도 좌우차','<b>○</b>'],
   ['⑤ 난치성 하지통 (암성·수술후)','원인 병소는 설명되나 통증이 남음 — <b>진단적 차단이 양성일 때</b>만','△'],
   ['⑥ 본태성 다한증','<b>통증이 없다</b> — 표적이 <b>발한</b>이지 진통이 아니다','○ 발한',],
  ]},
 # ---------- 걸러낼 것 (LSB 적응이 아닌 감별질환) ----------
 {'t':'table','eyebrow':'질환 · 먼저 걸러낸다','tag':('감별 제외','ink'),
  'title':'무엇을 걸러내나 — 증상은 비슷해도 LSB 적응이 아니다',
  'foot':'감별의 출발점은 ABI·도플러 — 동맥성 여부부터 가른다 · 앞 슬라이드의 적응 5개와 짝을 이룬다',
  'note':"이 셋은 <b>밤·하지 증상</b>이라는 겉모습만 겹친다. 기전이 교감신경이 아니므로 <b>차단해도 듣지 않는다.</b>",
  'headers':['질환','핵심 소견 — 감별점','LSB'],
  'rows':[
   ['특발성 야간경련 (NLC)','통증성 <b>근수축</b> · 만져지는 근경직 · <b>족배굴곡으로 완화</b>','✕'],
   ['RLS (하지불안)','<b>움직임 충동</b> · 움직이면 완화 · 근경직 없음','✕'],
   ['정맥부전·정맥류','부종·무거움 · <b>저녁</b> 악화 · 압박·거상으로 완화 — 교감차단은 <b>동맥 유입만 늘리고 정맥 유출은 못 고친다</b>(부종 위험)','✕'],
  ]},
 {'t':'bullets','eyebrow':'질환 · 공통 축','tag':('SMP 임상상','red'),
  'title':'교감신경 매개 통증(SMP) — 환자는 이렇게 호소한다',
  'foot':'Roberts, Pain 1986 (PMID 3515292) · Stanton-Hicks, Pain 1995 (PMID 8577483)',
  'items':[
   (0,'<b>통증:</b> 바탕에 <b>타는 듯한 작열통</b>이 깔리고, <b>스치기만 해도 아프다</b>(이질통).','red'),
   (1,'“양말이 닿아도 아파요” · “이불이 스치면 소스라쳐요”','muted'),
   (0,'<b>범위:</b> 신경 하나의 지배영역보다 <b>넓게</b> — “무릎 아래가 다 아파요”.',''),
   (0,'<b>눈에 보이는 변화:</b> 좌우 발의 <b>색·온도</b>가 다르다 · 땀이 유난히 많거나 없다 · 붓는다.','green'),
   (0,'<b>악화 조건:</b> <b>추울 때·긴장할 때</b> 심해지고, 밤에 더하다.',''),
   (0,'<b>오래되면:</b> 피부가 얇고 반들거리며 털·발톱이 변하고 관절이 굳는다.',''),
   (-1,'이 그림은 <b>의심 단서</b>일 뿐 — 차단으로 <b>통증이 줄면 SMP</b>, 안 줄면 <b>SIP</b>. 한 환자 안에 두 성분이 섞이고 만성화될수록 SIP로 기운다.','accent'),
  ]},
 {'t':'bullets','eyebrow':'적응증 · 증상 ②','tag':('당뇨병성 신경병증','green'),
  'title':'환자 증상·호소 ②-1 — 당뇨병성 신경병증: 통증의 성질과 분포',
  'foot':'Zhang 2020(PMID 32915421, n=60)은 두 군 모두 알코올 신경파괴 — 국소마취제 단독군이 없다 · 증례 PMID 22606406',
  'items':[
   (0,'<b>감각 양성증상:</b> <b>화끈거림</b> · <b>저림·찌릿한 전기 통증</b> · 쑤심 · <b>이질통</b> · 통각과민',''),
   (0,'<b>감각 음성증상:</b> 감각저하·먹먹함 — <b>“양말을 겹쳐 신은 느낌”</b> · 위치감각 저하로 <b>휘청임</b>',''),
   (0,'<b>분포:</b> 양측 대칭 <b>‘양말’ 형</b> — 발끝에서 시작해 위로 올라온다.',''),
   (0,'<b>시간 양상:</b> <b>밤에 악화</b> — <b>수면 방해</b>가 주 호소인 경우가 많다.','green'),
   (0,'<b>LSB 효과 — 정직하게:</b> 통제된 수치가 없다. 유일한 RCT는 양 군 모두 신경파괴였고, 차단만의 효과는 <b>증례 수준</b>.','red'),
   (-1,'호소 그대로: “발이 저리고 화끈거려요” · “밤에 더 심해서 잠을 못 자요” · “전기가 찌릿 와요”','accent'),
  ]},
 {'t':'bullets','eyebrow':'적응증 · 증상 ②','tag':('당뇨병성 신경병증','green'),
  'title':'환자 증상·호소 ②-2 — 당뇨병성 신경병증: 자율신경 소견과 진찰',
  'foot':'이질통은 음성 예측(PMID 22143169)·양성 예측(PMID 17173603)으로 문헌이 서로 반대 · StatPearls NBK442009',
  'items':[
   (0,'<b>자율신경 동반(= SMP 단서):</b> 발이 <b>차갑거나 화끈</b> · 좌우 <b>온도·색 차이</b> · 발한 증가/감소 · 피부 건조·부종','green'),
   (0,'<b>진찰:</b> 모노필라멘트·진동감각 저하 · 발목반사 소실 · 발톱 변화',''),
   (0,'<b>당뇨발이면:</b> <b>궤양</b>·관류저하 동반 — 통증뿐 아니라 <b>창상 치유</b>도 기대 효과.','green'),
   (-1,'1차는 혈당조절 + 약물(가바펜틴·프레가발린·듀록세틴). <b>난치성일 때 LSB를 얹어 보는 자리</b>이지 1차 치료가 아니다.','accent'),
  ]},
 {'t':'split','eyebrow':'적응증 · 증상 ② 심화','tag':('야간 신경병증통',''),
  'title':'밤에 저리고 화끈거리는 다리 — 당뇨병성 신경병증과 LSB','foot':'Zhang 2020(RCT) PMID 32915421; 증례 PMID 22606406; StatPearls NBK442009',
  'items':[
   (0,'<b>임상상:</b> 당뇨병성 말초신경병증 — 발·종아리 <b>저림·화끈거림·전기 찌름</b>, 양측 ‘양말’ 분포.',''),
   (0,'<b>야간통:</b> 이불 온기·야간 순환·주의분산 소실 → 밤에 증폭·수면 방해.',''),
   (0,'<b>감별:</b> RLS(움직이면 완화)·NLC(경련)·허혈성 안정통과 구분.',''),
   (-1,'1차: 혈당조절+약물(가바펜틴·듀록세틴) → 난치성이면 <b>LSB 고려</b>','accent'),
  ],
  'aside':{'title':'LSB — 치료 삽입','dark':True,'items':[
   (0,'<b>기전:</b> 교감차단 → <b>미세순환↑</b> + 교감매개통 차단.',''),
   (0,'<b>근거:</b> 국소마취제 차단만의 통제된 자료는 없다 — <b>증례 수준</b>.','muted'),
   (0,'<b>적용:</b> 진단차단이 양성일 때 <b>반복 차단</b>으로.',''),
  ]}},
 {'t':'bullets','eyebrow':'적응증 · 증상 ③','tag':('허혈 · 동맥성',''),
  'title':'환자 증상·호소 ③ — 허혈성 안정통 (PAD·CLI·버거병)',
  'foot':'ABI = 발목 수축기압 ÷ 상완 수축기압 · 정상 0.9–1.3 · ≤0.9 PAD · <0.4 중증허혈 · >1.3은 중막석회화로 위음성(당뇨·만성신부전에서 흔함) → 이때는 발가락-상완지수(TBI)나 도플러 파형으로 확인',
  'items':[
   (0,'<b>파행부터 갈라야 한다</b> — 걷다 아프고 쉬면 낫는 것은 <b>척추관협착(신경인성)</b>도 똑같다.','red'),
   (1,'<b>혈관성</b>: 아픈 <b>거리가 일정</b> · 서 있기만 하면 안 아픔 · <b>자세와 무관</b>하게 쉬면 완화 · 맥박↓·<b>ABI↓</b>',''),
   (1,'<b>신경인성</b>: 거리가 들쭉날쭉 · <b>서 있기만 해도</b> 유발 · <b>허리를 굽히면 완화</b> · 맥박·ABI 정상','muted'),
   (1,'<b>신경인성 파행에 LSB는 듣지 않는다</b> — 구조적 압박 문제라 교감신경 축이 아니다.','red'),
   (0,'<b>안정통(진행기):</b> 누우면 악화, <b>다리를 침대 밖으로 내리면 완화</b> — 야간에 심해 수면 방해.','green'),
   (0,'<b>진찰:</b> 차고 창백한 발 · 말초맥박 감소 · 재충혈 지연 · 발톱 비후·털 소실 · <b>ABI</b>',''),
   (-1,'호소 그대로: “걸으면 종아리가 터질 듯 아파요” · “밤에 발이 시려 잠을 못 자요” · “상처가 안 아물어요”','accent'),
  ]},
 {'t':'bullets','eyebrow':'적응증 · 증상 ④','tag':('하지 CRPS',''),
  'title':'환자 증상·호소 ④ — 하지 CRPS',
  'foot':'증상 자체는 5쪽 SMP와 같다 — 여기서는 CRPS만의 판단 포인트만 다룬다 · StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>SMP의 전형</b> — 증상 목록은 5쪽과 같다. CRPS에서 다른 점은 <b>유발 사건이 있고 통증이 그에 비해 과하다</b>는 것.',''),
   (0,'<b>흔한 방아쇠:</b> 골절·염좌·수술·석고 고정 — 손상은 나았는데 통증만 남아 커진다.',''),
   (0,'<b>진단은 임상(Budapest 기준):</b> 감각·혈관운동·발한/부종·운동/영양의 <b>네 축</b>에서 증상과 징후를 확인한다.',''),
   (-1,'<b>조기(≤12개월)에 하는 것이 유리하다</b> — 관절 강직·근위축이 굳기 전에.','accent'),
  ]},
 {'t':'bullets','eyebrow':'적응증 · 증상 ⑤','tag':('난치성 하지통',''),
  'title':'환자 증상·호소 ⑤ — 난치성 하지통 (암성·수술후·외상후)',
  'foot':'SMP 소견은 5쪽 참조 — 있으면 반응 가능성이 올라간다 · StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>암성 골반·하지통:</b> 골반강 종양·후복막 침범·골전이 — 깊은 쑤심에 작열·발작통이 겹치고 마약성 진통제로도 불충분.',''),
   (0,'<b>수술후·외상후:</b> 절단 후 <b>환상지통·단단통</b>, 신경손상 후 통증 — 발작적 찌름·작열, 추위에 악화.',''),
   (-1,'이 군은 병명이 아니라 <b>진단적 차단의 반응</b>으로 고른다 — 원인 병소가 설명돼도 통증이 남을 때 얹어 보는 자리.','accent'),
  ]},
 # ═══════════ 해부학 — 무엇을 겨냥하나 ═══════════
 {'t':'bullets','eyebrow':'개요','tag':('배경',''),'title':'개요 · 해부 · 원리','foot':'StatPearls NBK431107; Zhang 2022 (Ibrain)','items':[
   (0,'LSB는 70년 이상 다양한 하지 통증·허혈 질환에 사용되어 왔다.',''),
   (0,'표적: 신경절 밀도가 가장 높은 <b>L2–L3</b>(척추체 전외측). 일부 L2/L3/L4 다분절.',''),
   (0,'원리 ①: 교감신경 차단 → 혈관 확장·측부순환 증가 → 조직 산소화 개선.',''),
   (0,'원리 ②: 교감신경 매개 통증(sympathetically-maintained pain) 경로·자율신경 동반 구심로 차단.',''),
   (-1,'이 강의는 <b>국소마취제 차단</b>(진단적·치료적)만 다룬다 — 신경파괴는 우리 손에서 하는 시술이 아니다.','accent'),
 ]},
 {'t':'photo','eyebrow':'해부','title':'요추 교감신경간 — 어디를 겨냥하나',
  'caption':'교감신경간은 척추체 <b>전외측</b>을 좌우로 종주하며 <b>대동맥에 바짝 붙어</b> 지나간다 — LSB 표적은 <b>L2–L3</b>. '
            '복강(T12–L1)·상·하장간막 신경절은 대동맥 전면. 이 인접성 때문에 <b>혈관 손상·혈관내 주입</b>이 핵심 위험이고, '
            '조영제로 확산을 반드시 확인한다. · 좌: 오리지널 도해 / 우: 해부학 교과서 도판(교육용 인용)',
  'img':FIG('hf_anatomy', IMG('lsb_anatomy_merged.png','요추 교감신경간 해부 — 관상면 도해와 교과서 도판', jpeg=True, q=88),
            '요추 교감신경간 해부 — 관상면과 축상면')},
 {'t':'bigfig','eyebrow':'방법 · 그림으로','tag':('축상면 axial',''),'title':'L2·L3 조감도 — 표적과 위험 구조',
  'foot':'표적=척추체 전외측 교감신경절 · 방척추(정중선 ~7cm) 접근 · 대동맥·IVC·요관·신장·생식대퇴신경·추간공 회피',
  'svg':FIG('hf_axial', AXIAL_SVG, 'L2·L3 축상면 해부도')},
 # ═══════════ 감별 — 이 환자가 맞나 ═══════════
 # ═══════════ 술기 — 어떻게 하나 ═══════════
 {'t':'figsplit','eyebrow':'방법','tag':('기법',''),'title':'방법 (Technique)',
  'foot':'StatPearls NBK431107 · NBK560514 · 그림: 드라이브 원본 3D 애니메이션 스틸(교육용 인용)',
  'svg':IMG('lsb_tech_orig.png','바늘 접근과 약물 확산 — 원본 애니메이션 스틸', jpeg=True, q=86),
  'items':[
   (0,'<b>표준: 방척추 접근 + 투시</b> (CT·초음파도 가능)',''),
   (0,"바늘: 정중선 <b>~7 cm 외측</b> → 척추체 접촉 후 전내측 'walk'",''),
   (0,'<b>바늘·용량:</b> 22G 7인치 Quincke(<b>끝을 굽혀</b> 사용) · 레벨당 총 10–20 mL(예: 0.25% 부피바카인 10 mL)',''),
   (0,'조영제로 <b>두미측 종방향 확산</b> 확인',''),
   (0,'<b>성공 지표: 피부온도 ≥2°C↑</b>',''),
   (-1,'약제: 리도카인 1% · 부피바카인 0.25–0.5% · 로피바카인 — <b>국소마취제만</b>','accent'),
  ]},
 {'t':'bullets','eyebrow':'방법 · 실제 술기','tag':('투시 3-view','green'),
  'title':'실제 투시 술기 — 사위 → 측면 → 정면 순서',
  'foot':'술기 영상(TheProcedureGuide.com) 정리 · StatPearls NBK431107과 교차확인 · 교육용',
  'items':[
   (0,'<b>① 사위상(Scotty dog)</b>을 L2에서 얻고, 진입로가 열릴 때까지 <b>더 사위로</b> 회전.',''),
   (0,'<b>② 진입점: L2 하외측연</b> 바로 외측 — 긴 주사기를 <b>지시자(pointer)</b>로 체표에 표시.',''),
   (0,'<b>③ 척추체 접촉</b> 후 <b>외측으로 walk</b> — 척추체 전외측으로 미끄러뜨린다.','green'),
   (0,'<b>④ 측면상 전환</b> → <b>내측·전방</b>을 겨냥, 끝이 <b>척추체 바로 앞</b>에 오도록 진행.','green'),
   (0,'<b>⑤ 조영제 실시간 주입</b> — <b>두미측 확산</b> 확인, <b>혈관 조영 배제.</b>','red'),
   (0,'<b>⑥ L3 반복</b> → <b>흡인 음성</b> 확인 후 주입 · 정면상에서 최종 위치 확인.',''),
   (-1,'L2·L3 바늘을 모두 거치한 뒤 측면상으로 전환하면 빠르다 — 숙련 시 약 5분.','accent'),
  ]},
 {'t':'bigfig','eyebrow':'방법 · 영상으로','tag':('실제 투시상',''),
  'title':'투시 영상으로 본 술기 — 바늘은 이렇게 들어간다',
  'foot':'실제 시술 영상 스틸(TheProcedureGuide.com) · 사위 → 측면 → 정면 3-view · 교육용 인용',
  'svg':IMG('lsb_fluoro_steps.png','LSB 투시 술기 4단계', jpeg=True)},
 {'t':'bigfig','eyebrow':'방법 · 그림으로','tag':('3D 애니메이션',''),
  'title':'약물은 어디로 퍼지나 — 표적과 확산',
  'foot':'3D 의학 애니메이션 스틸 · 분홍=교감신경간(척추체 전외측), 파랑·보라=약물 확산 · 실제 확산 범위는 반드시 조영제로 확인 · 교육용 인용',
  'svg':IMG('lsb_anim_steps.png','LSB 3D 애니메이션 4단계', jpeg=True)},
 {'t':'bullets','eyebrow':'방법 · 안전','tag':('시술 주의',''),'title':'L2·L3 시술 — 전·중 주의할 점','foot':'StatPearls NBK431107 · NBK557637 · Feigl 1998(PMID 9425975)','items':[
   (0,'<b>영상 유도 필수:</b> 투시(또는 CT). <b>조영제</b>로 두미측 종방향 확산 확인 — 후방(추간공)·혈관 확산 시 즉시 재위치.',''),
   (0,'<b>바늘 끝은 척추체 전외측</b>에 — <b>psoas·추간공 진입 금지.</b>',''),
   (0,'<b>요추신경총차단과 혼동 금지</b> — 그쪽 표적은 <b>psoas 구획(체성신경)</b>, LSB에선 <b>피해야 할 구조.</b>','red'),
   (0,'<b>레벨은 L2 하1/3~L3 상1/3</b>, <b>L4로 내려가지 말 것</b>(생식대퇴신경통 급증).',''),
   (0,'<b>흡인 후 분할·점진 주입</b>(혈관내·경막외 조기 발견) · 소량 시험주입.',''),
   (0,'<b>항응고·항혈소판제 중단</b>(심부·후복막 차단 — 출혈 위험) · 무균술.',''),
   (-1,'성공지표 온도 ≥2°C↑ 확인 · 시술 후 혈압·하지 근력/감각 모니터.','accent'),
 ]},
 {'t':'bigfig','eyebrow':'안전 · 위험구조','tag':('혈관·신장 회피','red'),
  'title':'대동맥·IVC·신장을 피하는 법 — 뼈를 놓치지 않는다',
  'foot':'핵심 3가지 — ① 척추체 접촉을 유지한 채 뼈를 따라 미끄러뜨린다 ② 측면상에서 바늘 끝을 척추체 전연 앞으로 넘기지 않는다 ③ 너무 외측이면 신장, 너무 내측이면 추간공 · 오리지널 도해',
  'svg':FIG('hf_avoid', AVOID_SVG, '대혈관·신장 회피 축상면')},
 {'t':'bullets','eyebrow':'안전 · 위험구조','tag':('회피 수칙','red'),
  'title':'혈관·신장 천자 — 실제로 어떻게 피하나',
  'foot':'StatPearls NBK431107 · NBK557637 · 교육용 정리',
  'items':[
   (-1,'<b>뼈를 놓치지 말고, 전연을 넘기지 말고, 넣기 전에 조영제로 확인한다.</b>','accent'),
   (0,'<b>① 뼈를 기준으로:</b> 척추체 <b>접촉을 유지</b>한 채 외측으로 walk — 뼈를 놓치면 깊이 감각을 잃는다.','green'),
   (0,'<b>② 전연을 넘기지 않는다:</b> <b>측면상</b>에서 끝이 척추체 <b>전연 바로 앞</b>이면 정지 — 더 가면 <b>대동맥(좌)·IVC(우)</b>.','red'),
   (1,'우측 접근은 <b>IVC</b>가 먼저 — 벽이 얇아 흡인 음성이어도 관통될 수 있다.',''),
   (0,'<b>③ 신장:</b> <b>L1–L3</b> 높이 후외측 — <b>과도하게 외측</b>으로 들어가면 지난다. 정중선 ~7 cm를 지키고, 마른 환자·신장하수는 <b>하극을 먼저 확인</b>.',''),
   (0,'<b>④ 넣기 전 확인:</b> <b>흡인</b>(혈액·소변) → <b>조영제</b> → 혈관 음영이면 즉시 재위치.','red'),
  ]},
 {'t':'bigfig','eyebrow':'안전 · 핵심기술','tag':('조영제 읽기',''),'title':'조영제 확산 읽기 — 이 패턴이면 멈춰라',
  'foot':'실시간 조영제가 최고의 안전장치 — 종방향(위·아래) 확산만 진행 · 혈관·경막외·근육내 패턴이면 즉시 바늘 재위치·재확인',
  'svg':FIG('hf_contrast', CONTRAST_SVG, '조영제 종방향 확산')},
 # ═══════════ 합병증 — 무엇을 조심하나 ═══════════
 {'t':'table','eyebrow':'안전성','tag':('합병증·회피','red'),'title':'합병증 & 회피법','foot':'StatPearls NBK431107·NBK557637 · Feigl 1998(PMID 9425975)',
  'note':"핵심: 투시+조영제로 확산 확인 · 바늘 전외측 유지 · L2~L3 표적.",
  'headers':['합병증','원인·기전','피하는 법'],'rows':[
   ['생식대퇴신경통 (5–10%)','psoas 역류·자극 (<b>L2 0%·L4 40%</b>)','<b>L4 회피</b>·psoas 주입금지·최소용량'],
   ['혈관손상·혈관내주입','대동맥/IVC·요추혈관 인접','투시+<b>흡인+조영제</b>·항응고 중단'],
   ['요관·신장 천공','후복막 장기 인접','조영제로 깊이·궤적 확인'],
   ['체성신경·신경축 확산','바늘 후방→경막외 tracking','바늘 <b>전외측 유지</b>'],
   ['기립성 저혈압','교감차단 → 혈관확장','수액·서서히 기립·<b>양측 신중</b>'],
   ['생식기능 영향','양측 <b>L1–L2</b> 동시 차단','L1–L2 양측 동시 차단 회피'],
  ]},
 {'t':'bigfig','eyebrow':'합병증 · 심화','tag':('최다 우려',''),'title':'생식대퇴신경통 — 가장 흔한 걱정, 대부분 회피 가능',
  'foot':'회피: L2하~L3상 표적·L4 회피·psoas 주입금지·소량 / 발생 시: 대개 수 주 내 자연호전·신경병증통 약물로 대증 · Feigl 1998(PMID 9425975)','svg':GF_SVG},
 {'t':'bullets','eyebrow':'합병증 · 대응','tag':('인지·구조','red'),'title':'혈관·LAST·신경 손상 — 조기 인지와 대응','foot':'ASRA LAST 지침 · StatPearls NBK431107','items':[
   (0,'<b>LAST(국소마취제 전신독성):</b> 입 주변 저림·이명·금속맛·어지럼 → 경련·부정맥.','red'),
   (0,'대응 — 즉시 중단·산소/기도·경련조절·<b>20% 지질유탁액 정주</b>·소생술. 예방 — 흡인+조영제+분할주입+용량제한.',''),
   (0,'<b>신경·신경축:</b> 주입 중 방사통·하지 위약 → 즉시 중단·재위치. 시술 후 근력·감각 확인.',''),
   (0,'<b>출혈·감염:</b> 항응고 중단·무균술 · 심한 통증·발열·팽창 시 즉시 평가.',''),
   (-1,'준비된 상태(모니터·정맥로·지질유탁액)면 대부분 안전하게 관리된다.','accent'),
 ]},
 {'t':'bullets','eyebrow':'합병증 · 대비','tag':('환자 안심','ink'),'title':'합병증 대비 — 준비·조기인지·환자설명','foot':'교육용 정리','items':[
   (0,'<b>대부분 경미·자가회복</b> — 심각 합병증은 영상유도·정확한 술기로 드묾.',''),
   (0,'<b>준비:</b> 모니터·정맥로·응급장비·<b>20% 지질유탁액</b> 구비, 소생 프로토콜 숙지.',''),
   (0,'<b>조기 인지:</b> 조영제 패턴 + 환자 증상(통증·저림·어지럼)을 실시간 관찰.',''),
   (0,'<b>환자 설명(동의):</b> 흔한 것(일시적 저림·주사부위통·저혈압) vs 드문 것(신경통·출혈)을 사전 고지 → 신뢰·불안↓.',''),
   (-1,'용량은 최소로 — 확산이 넓을수록 위해가 는다.','accent'),
 ]},
 # ═══════════ 확인과 효과 — 되었는지, 듣는지 ═══════════
 {'t':'split','eyebrow':'효과','tag':('Lv III–IV','amber'),'title':'효과 ① 관류 개선 · 허혈성 통증','foot':'Dickey 2024 (Cureus); Medicina 2024; Barreto 2018',
  'items':[
   (0,'<b>관류 실측(Dickey 2024):</b> LSB 후 후경골동맥 직경 0.17→0.27 cm(+58.8%), 모세혈관 재충혈 3.92→1.30초, 족부온도 +2.8°C.',''),
   (0,'허혈성 통증(PAD): 하지 통증 최대 <b>75%↓</b>, Fontaine 분류·측부관류 개선(Medicina 2024).','green'),
   (0,'비재건성 CLI: 재건이 불가능한 환자에서 통증조절 수단이 된다(Barreto 2018).',''),
  ],
  'aside':{'title':'실측 수치 (Dickey 2024)','stat':[('+58.8%','후경골동맥 직경'),('+2.8°C','족부온도'),('3.92→1.30s','모세혈관 재충혈')]}},
 {'t':'bullets','eyebrow':'효과','tag':('Lv III–IV','amber'),'title':'효과 ② CRPS · 기전','foot':'Choi 2024 (Sci Rep); Pain Ther 2023','items':[
   (0,'CRPS는 교감신경 매개 통증의 전형 → LSB 후 유의한 통증완화. 최적 환자 선택·조기 시행이 성공률↑.',''),
   (0,'Choi 2024(Sci Rep): CRPS에서 교감신경 차단 효과의 지속기간을 전향 관찰로 제시.',''),
   (0,'반응 예측: <b>교감신경 피부반응(SSR)</b>이 LSB 반응 예측에 유용(Pain Ther 2023).',''),
   (0,'한계: 중추 감작이 진행되면 시간이 지날수록 효과 감소 가능.','muted'),
   (-1,'기전: 교감차단 → 측부순환 혈관확장 → 조직 산소화↑ → 통증↓, 그리고 교감매개통 경로 차단.','accent'),
 ]},
 {'t':'bullets','eyebrow':'결론','tag':('근거수준','ink'),
  'title':'근거수준 — 우리가 하는 국소마취제 차단은 어디쯤인가',
  'foot':'Cross &amp; Cotton 1985 (PMID 3898891) · Cochrane CD004598.pub4 (27467116) · Zhang 2020 (32915421)',
  'items':[
   (0,'<b>허혈성 안정통</b> — 유일하게 <b>위약대조 RCT 양성</b>(83.5% vs 23.5%). 가장 단단한 자리.','green'),
   (0,'<b>CRPS</b> — 시술 빈도 1위지만 <b>Cochrane은 음성</b>, 관찰연구는 양성으로 갈린다.',''),
   (0,'<b>당뇨병성 신경병증</b> — 차단만의 <b>통제된 자료가 없다</b>.','red'),
   (0,'<b>SMP 우세형·난치성 하지통</b> — RCT·지침 근거 없음.',''),
   (-1,'가장 확실한 값어치는 <b>진단</b>이다 — 이 통증이 교감신경 축인지 아닌지를 가려 준다.','accent'),
 ]},
 # ═══════════ 마무리 ═══════════
 {'t':'bullets','eyebrow':'나의 프로토콜 · 실제 적용','tag':('실전 순서','ink'),
  'title':'실제 진료 순서 — 교감신경 축을 겨냥한 단계적 접근','foot':'교육용 제안 · 개별 적용은 임상 판단','items':[
   (0,'<b>① 감별·검사:</b> ‘밤/하지 증상’이 <b>동맥성 허혈(ABI·도플러)</b>·CRPS·신경병증인지 확인. 특발 경련·RLS·정맥류 배제.',''),
   (0,'<b>② 방향 설정:</b> 교감매개통·허혈로 판단되면 <b>교감신경 축(L2–L3)</b>을 겨냥.',''),
   (0,'<b>③ 진단적 차단:</b> 투시 유도 국소마취제 LSB → <b>피부온도 ≥2°C 상승·통증 반응</b> 확인.','green'),
   (0,'<b>④ 반응 양호 시:</b> <b>치료적 반복 차단</b>으로 이어간다.','green'),
   (0,'<b>⑤ 대상별:</b> CRPS는 조기(≤12개월)가 유리 · 당뇨병성 신경병증은 난치성일 때 얹어 본다.',''),
   (-1,'⑥ 주의: 특발성 NLC·정맥질환은 적응 아님 · 합병증(생식대퇴신경통 5–10% 등) 사전 고지.','accent'),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · LSB','headline':'표준은 투시 유도 방척추 접근, 성공은 온도 ≥2°C','msgs':[
   ('방법','L2–L3 방척추 접근·투시, 정중선 7 cm 외측, 조영제 두미측 확산, 성공지표 온도 ≥2°C.'),
   ('약제','국소마취제(리도카인·부피바카인·로피바카인) — 이 강의는 신경파괴를 다루지 않는다.'),
   ('적응증','조기 CRPS·PAD/CLI 안정통·신경병증·다한증 등. 특발성 NLC·정맥질환(정맥류)은 적응 아님.'),
   ('효과','관류 실측 개선(Dickey), 허혈통 최대 75%↓, CRPS 통증완화(SSR로 예측).'),
   ('근거','통제된 근거가 얇다 — 허혈성 안정통 외에는 관찰·증례 수준.'),
 ]},
 {'t':'refs','title':'참고문헌 — LSB','refs':[
   ('<b>Dua & Varacallo.</b> Lumbar sympathetic block. StatPearls. 2026.','https://www.ncbi.nlm.nih.gov/books/NBK431107/'),
   ('Lumbar sympatholysis. StatPearls.','https://www.ncbi.nlm.nih.gov/books/NBK560514/'),
   ('<b>Zhang.</b> Lumbar sympathetic ganglion block in lower limb pain. Ibrain. 2022.',PM(37786587)),
   ('<b>Dickey & Sharma.</b> LSB increases arterial diameter and blood flow. Cureus. 2024.',PM(38975506)),
   ('<b>Barreto.</b> Neurolytic block of lumbar sympathetic chain in CLI. Braz J Anesthesiol. 2018.',PMC('PMC9391669')),
   ('<b>Choi.</b> Effect duration of lumbar sympathetic neurolysis in CRPS. Sci Rep. 2024.',PM(38830944)),
   ('<b>Gungor.</b> Sympathetic blocks for CRPS: case series. Medicine. 2018.',PM(29742728)),
   ('LSB on pain, Fontaine, perfusion in PAD. Medicina (Kaunas). 2024.','https://doi.org/10.3390/medicina60050682'),
   ('LSB efficacy in CRPS-1 by sympathetic skin response. Pain Ther. 2023.',PMC('PMC10199976')),
   ('<b>Straube (Cochrane).</b> Cervico-thoracic or lumbar sympathectomy for neuropathic pain and CRPS. 2013.',CDSR('CD002918.pub3')),
   ('<b>Continuous LSB + sympatholysis for refractory painful diabetic neuropathy — RCT.</b> 2020.',PM(32915421)),
   ('Sympathetic blocks: sustained relief in refractory painful diabetic neuropathy (case). 2012.',PM(22606406)),
   ('Lumbar sympathectomy for ischaemia·vasculitis·diabetic neuropathy·hyperhidrosis — series. 2018.',PM(29516399)),
 ]},
]

# ---------- 신경병증 분류 (당뇨병성 외) ----------
LSB.append({'t':'table','eyebrow':'적응증 · 심화','tag':('신경병증 분류',''),
  'title':'신경병증은 당뇨병성만이 아니다 — 종류와 LSB 적용',
  'foot':'교감신경 매개 통증(SMP) 요소가 클수록 LSB 반응이 좋다 · StatPearls; 문헌고찰 종합',
  'note':"핵심: 병명보다 <b>교감신경 매개 통증(SMP)인가</b>가 관건 — 진단적 차단으로 확인 후 결정.",
  'headers':['분류','대표 질환','LSB 적용'],'rows':[
   ['대사성','<b>당뇨병성 말초신경병증(DPN)</b> · 알코올성 · 영양결핍(B12)','△ 난치성 <b>RCT</b>'],
   ['감염후','<b>대상포진후신경통(PHN)</b> 하지 분절 · HIV 신경병증','△ 선택적'],
   ['약제성','<b>항암제 유발 말초신경병증(CIPN)</b> — 옥살리플라틴·탁센','△ 보고 수준'],
   ['외상·수술후','<b>환상지통·단단통</b> · 신경손상 후 통증 · 수술후 신경병증','○ SMP 흔함'],
   ['교감매개 대표','<b>CRPS I / II</b> (반사교감이영양증·작열통)','◎ 대표 적응'],
   ['압박·유전성','요추신경근병증 · 포착신경병증 · 유전성(CMT)','✕ 원인치료 우선'],
  ]})

# ---------- 전체 흐름 안내(로드맵) ----------
LSB.append({'t':'bullets','eyebrow':'확인과 효과','tag':('진단적 차단','red'),
  'title':'확인과 효과 — 진단적 차단으로 SMP를 확정한다',
  'foot':'온도 상승은 차단이 걸렸다는 지표, 통증 감소가 SMP의 근거 — 둘은 다른 것을 말한다 · 함정은 다음 슬라이드 · StatPearls NBK431107',
  'note':"순서를 뒤집지 않는다 — <b>먼저 차단이 되었는지</b>(온도), <b>그다음 통증이 줄었는지</b>(SMP 여부). "
         "차단이 안 된 상태의 무반응을 SIP로 읽으면 안 된다.",
  'items':[
   (0,'<b>① 차단이 되었나 — 피부온도 ≥2°C 상승.</b> 되지 않았으면 판정 자체가 불가하다. 재위치·재시도.','green'),
   (0,'<b>② 통증이 줄었나 — 줄면 SMP</b>(교감신경 매개 통증, sympathetically maintained pain).','red'),
   (1,'반복 차단으로 효과가 누적되는지 확인한다 — 지속되지 않으면 다른 축을 본다.',''),
   (0,'<b>줄지 않으면 SIP</b>(교감신경 <b>비</b>의존성 통증, sympathetically <b>independent</b> pain) — 교감신경이 원인이 아니다.',''),
   (1,'교감신경 축을 더 밀지 않고 <b>방향을 바꾼다</b> — 약물·체성신경 차단·재활·정신사회적 요인.','accent'),
  ]})

LSB.append({'t':'bullets','eyebrow':'확인 · 함정','tag':('위양성 주의','red'),
  'title':'확인의 함정 — 양성 차단을 그대로 믿지 않는다',
  'foot':'Price, Clin J Pain 1998;14:216-226 (맹검 위약 비교) · Anesthesiology 2019;131:883 (PMID 31365367, n=318) · '
         'SSR 진폭 &lt;510 µV·이환 &lt;12개월이 독립 예측인자였으나 단일기관 미재현 (Pain Ther 2023, PMC10199976)',
  'items':[
   (0,'<b>단일 개방형 양성 차단은 진단이 아니라 가설이다.</b>','red'),
   (1,'교감신경절에 국소마취제 vs 생리식염수를 맹검 비교하면 <b>최대 진통 효과는 차이가 없고 지속시간만 다르다</b>(Price 1998).',''),
   (0,'확산에 의한 <b>체성신경 차단</b>도 위양성을 만든다 — 온도와 <b>감각 분포</b>를 함께 기록해 해석한다.',''),
   (0,'온도 상승 <b>폭</b>이 진통 정도를 예측하지는 않는다(n=318, PMID 31365367).',''),
   (-1,'차단 반응으로 <b>척수자극기 성공을 예측하지 말 것.</b>','accent'),
  ]})

LSB.append({'t':'key','eyebrow':'전체 흐름 · Roadmap',
  'headline':'어떤 병에 → 어디를 → 이 환자가 맞나 → 어떻게 → 되었는지','msgs':[
   ('① 질환','LSB가 듣는 병 — <b>특발성 SMP</b>가 최우선, 이어 당뇨병성 신경병증·허혈성 안정통·하지 CRPS'),
   ('② 해부','교감신경간은 척추체 <b>전외측 L2–L3</b> — 표적과 주변 위험 구조'),
   ('③ 감별','밤·하지 증상 중 LSB 적응이 <b>아닌 것</b>을 걸러낸다 — ABI·도플러가 출발점'),
   ('④ 술기·안전','투시+조영제로 정확히 — 합병증은 대부분 <b>회피·관리 가능</b>'),
   ('⑤ 확인·효과','진단적 차단 반응으로 SMP 확정 → 관류 실측·통증 감소 <b>(근거수준과 함께)</b>'),
 ]})

# ---------- 강의 흐름에 맞춘 슬라이드 순서 재배열 ----------
# 흐름: 질환(어떤 병에 쓰나) → 해부 → 감별 → 술기 → 합병증 → 확인·효과 → 마무리.
# 적응증 우선순위는 전 슬라이드 공통: ① 특발성 SMP ② 당뇨병성 신경병증
# ③ 허혈성 안정통 ④ 하지 CRPS ⑤ 난치성 하지통. RLS·정맥부전은 적응 아님(옅게 표시).
_ORDER = ['요추교감신경차단', '전체 흐름',
          # ── 질환: 어떤 병에 쓰나 ──
          'LSB는 어떤 병에 쓰나', '무엇을 걸러내나',
          '교감신경 매개 통증(SMP)',
          '증상·호소 ②-1', '증상·호소 ②-2', '밤에 저리고 화끈거리는 다리', '신경병증은 당뇨병성만이',
          '증상·호소 ③ — 허혈성', '증상·호소 ④ — 하지 CRPS', '증상·호소 ⑤ — 난치성 하지통',
          # ── 해부: 어디를 겨냥하나 ──
          '개요 · 해부 · 원리', '요추 교감신경간 — 어디를', 'L2·L3 조감도',
          # ── 술기: 어떻게 하나 ──
          '방법 (Technique)', '실제 투시 술기', '투시 영상으로 본', '약물은 어디로 퍼지나',
          'L2·L3 시술', '대동맥·IVC·신장을 피하는', '혈관·신장 천자', '조영제 확산 읽기',
          # ── 합병증 ──
          '합병증 & 회피법', '생식대퇴신경통', '혈관·LAST·신경 손상', '합병증 대비',
          # ── 확인과 효과 ──
          '확인과 효과 — 진단적', '효과 ① 관류', '효과 ② CRPS', '근거수준 · 결론',
          # ── 마무리 ──
          '실제 진료 순서', '표준은 투시 유도', '참고문헌']

def _skey(s):
    return s.get('title') or s.get('headline') or s.get('eyebrow') or ''

def _rank(s):
    t = _skey(s) + ' ' + (s.get('eyebrow') or '')
    for i, frag in enumerate(_ORDER):
        if frag in t:
            return i
    return 999

LSB = sorted(LSB, key=_rank)

# ---------- 내용이 많아 각주(출처)가 잘리는 슬라이드는 dense로 한 단계 축소 ----------
_DENSE = ['전체 흐름', 'LSB는 어떤 병에 쓰나', '교감신경 매개 통증(SMP)', '개요 · 해부 · 원리',
          '증상·호소',
          '신경병증은 당뇨병성만이', '밤에 저리고 화끈거리는 다리', '효과 ② CRPS',
          '방법 (Technique)', '실제 투시 술기', '혈관·신장 천자', 'L2·L3 시술', '합병증 & 회피법',
          '근거수준 · 결론', '실제 진료 순서', '표준은 투시 유도',
          '무엇을 걸러내나', '확인의 함정', '확인과 효과']
for _s in LSB:
    _t = _skey(_s) + ' ' + (_s.get('eyebrow') or '')
    if any(f in _t for f in _DENSE):
        _s['dense'] = True

BASE = os.path.join(REPO, "문헌고찰_NLC_RLS_LSB")
TITLE = "요추교감신경차단 · 문헌고찰 발표"
FNAME = "LSB_발표_웹"

# ---- Pretendard 위치 탐색 (환경변수 → 저장소/fonts → /tmp) ----
def _font_dir():
    cands = [os.environ.get("PRETENDARD_DIR"),
             os.path.join(REPO, "fonts"),
             "/tmp/pretendard"]
    for d in cands:
        if d and os.path.exists(os.path.join(d, "Pretendard-Bold.otf")):
            return d
    sys.exit(
        "Pretendard 폰트를 찾지 못했습니다. 아래로 받으세요:\n"
        "  mkdir -p fonts && cd fonts && npm pack pretendard \\\n"
        "    && tar xzf pretendard-*.tgz --strip-components=4 package/dist/public/static\n"
        "또는 PRETENDARD_DIR 환경변수로 경로를 지정하세요.")

FDIR = _font_dir()
FONTS = {
  "__F900__": os.path.join(FDIR, "Pretendard-Black.otf"),
  "__F800__": os.path.join(FDIR, "Pretendard-ExtraBold.otf"),
  "__F700__": os.path.join(FDIR, "Pretendard-Bold.otf"),
  "__F300__": os.path.join(FDIR, "Pretendard-Light.otf"),
}

htmlc = render_deck(TITLE, LSB)

# collect glyphs actually used
vis = re.sub(r'<style.*?</style>', '', htmlc, flags=re.S)
vis = re.sub(r'<script.*?</script>', '', vis, flags=re.S)
vis = re.sub(r'<[^>]+>', ' ', vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@▲▼✕✳“”")
text = ''.join(sorted(chars))
print("glyphs:", len(chars))

uris = {}
for ph, path in FONTS.items():
    o = Options(); o.flavor = 'woff2'; o.desubroutinize = True
    o.name_IDs = []; o.name_legacy = False; o.name_languages = []
    f = TTFont(path); s = Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf = io.BytesIO(); f.save(buf)
    uris[ph] = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
    print(ph, f"{len(buf.getvalue())/1024:.0f}KB  <- {os.path.basename(path)}")

for ph, uri in uris.items():
    htmlc = htmlc.replace(ph, uri)
out = os.path.join(BASE, FNAME + ".html")
open(out, 'w', encoding='utf-8').write(htmlc)
print("slides:", len(LSB), "->", out, f"({len(htmlc.encode())/1024:.0f}KB)")
