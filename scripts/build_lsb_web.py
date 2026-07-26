# -*- coding: utf-8 -*-
"""LSB(요추교감신경차단) 웹 발표 덱 전용 빌더 — Pretendard 서브셋 임베드.
build_web_decks.py의 LSB 정의를 기반으로 하되, LSB 한 덱만 재생성한다(NLC/RLS 불변).
폰트는 /tmp/pretendard 우선, 없으면 기존 업로드 경로 폴백."""
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

ASSETS = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/03_LSB/assets"

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


def esc_attr(s):
    return (str(s).replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))

LSB = [
 {'t':'title','eyebrow':'Lumbar Sympathetic Block · 문헌고찰','title':'요추교감신경차단',
  'sub':'방법 · 적응증 · 효과','order':'Technique · Indications · Efficacy','series':SERIES},
 # ---------- 감별 오프너 (NLC 스타일: 감별이 먼저) ----------
 {'t':'table','eyebrow':'가장 먼저','tag':('감별','ink'),'title':'밤·하지 증상 감별 — LSB는 어디에 쓰나','foot':'감별이 치료의 출발점 · ABI·도플러 선행',
  'note':"핵심: <b>ABI·도플러</b>로 동맥성 여부 감별이 출발점 — 정맥류·특발경련·RLS는 LSB 적응 아님.",
  'headers':['질환','핵심 소견','LSB 적응'],'rows':[
   ['허혈성 안정통 (PAD·CLI)','파행 → 야간 안정통 · 차고 창백한 발 · <b>ABI↓</b> (동맥성)','<b>○</b>'],
   ['하지 CRPS','작열통·이질통·부종·피부색/온도 좌우차 (교감매개통)','<b>○</b>'],
   ['당뇨병성 신경병증','저림·화끈거림·감각이상·<b>야간 악화</b>','△ 난치성'],
   ['특발성 NLC (야간경련)','통증성 근수축·촉지 근경직·족배굴곡 완화','✕'],
   ['RLS (하지불안)','움직임 충동·움직이면 완화·근경직 없음','✕'],
   ['정맥부전·정맥류','부종·무거움·저녁 악화 (정맥 역류)','✕'],
  ]},
 # ---------- 교감신경 매개 통증(SMP) — 이 환자를 골라내는 것이 핵심 ----------
 {'t':'split','eyebrow':'가장 중요','tag':('SMP 감별','red'),
  'title':'교감신경 매개 통증(SMP) — 진단명과 별개의 축',
  'foot':'SMP/SIP의 구분은 진단명이 아니라 진단적 차단의 반응으로 정해진다 · Pain Ther 2023(SSR)',
  'items':[
   (0,'<b>SMP는 병명이 아니라 독립된 축이다</b> — 어떤 진단 위에도 얹히고, <b>선행 질환 없이 단독으로도</b> 나타난다.','red'),
   (1,'<b>동반형</b> — 당뇨병성 신경병증·PHN·CRPS·허혈에 겹침 (같은 병명이라도 <b>있는 환자만</b> 반응)',''),
   (1,'<b>단독·특발형</b> — <b>원발성 레이노·홍색사지통증·본태성 다한증</b>, 유발 사건이 없는 CRPS','green'),
   (0,'<b>통증의 질:</b> <b>작열통</b>+<b>이질통</b>·통각과민, 신경 지배영역을 <b>넘어</b> 퍼진다.',''),
   (0,'<b>자율신경 징후:</b> 좌우 <b>온도차</b>·색 변화·<b>발한 이상</b>·부종.',''),
  ],
  'aside':{'title':'확인과 효과','dark':True,'items':[
   (0,'<b>확인</b> 진단적 LSB 후 통증 감소 = SMP. 무반응이면 <b>SIP</b> — 방향을 바꾼다.',''),
   (0,'<b>성공 판정</b> 피부온도 <b>≥2°C↑</b>.',''),
   (0,'<b>효과</b> 양성이면 반복 차단 → <b>신경파괴·RFA</b>.',''),
  ]}},
 {'t':'bullets','eyebrow':'개요','tag':('배경',''),'title':'개요 · 해부 · 원리','foot':'StatPearls NBK431107; Zhang 2022 (Ibrain)','items':[
   (0,'LSB와 교감신경 신경파괴(sympatholysis)는 70년 이상 다양한 하지 통증·허혈 질환에 사용.',''),
   (0,'표적: 신경절 밀도가 가장 높은 <b>L2–L3</b>(척추체 전외측). 일부 L2/L3/L4 다분절.',''),
   (0,'원리 ①: 교감신경 차단 → 혈관 확장·측부순환 증가 → 조직 산소화 개선.',''),
   (0,'원리 ②: 교감신경 매개 통증(sympathetically-maintained pain) 경로·자율신경 동반 구심로 차단.',''),
   (-1,'국소마취제 차단(진단적/치료적)과 화학적/열적 신경파괴로 나뉜다.','accent'),
 ]},
 {'t':'figsplit','eyebrow':'방법','tag':('기법',''),'title':'방법 (Technique)',
  'foot':'StatPearls NBK431107 · NBK560514 · 그림: 드라이브 원본 3D 애니메이션 스틸(교육용 인용)',
  'svg':IMG('lsb_tech_orig.png','바늘 접근과 약물 확산 — 원본 애니메이션 스틸', jpeg=True, q=86),
  'items':[
   (0,'<b>표준: 방척추 접근 + 투시</b> (CT·초음파도 가능)',''),
   (0,"바늘: 정중선 <b>~7 cm 외측</b> → 척추체 접촉 후 전내측 'walk'",''),
   (0,'<b>바늘·용량:</b> 22G 7인치 Quincke(<b>끝을 굽혀</b> 사용) · 레벨당 총 10–20 mL(예: 0.25% 부피바카인 10 mL)',''),
   (0,'조영제로 <b>두미측 종방향 확산</b> 확인',''),
   (0,'<b>성공 지표: 피부온도 ≥2°C↑</b>',''),
   (-1,'약제: 국소마취제 / 신경파괴(무수알코올·phenol·RFA)는 진단차단 양성 시에만','accent'),
  ]},
 # ---------- 실제 투시 술기 3-view 순서 (술기 영상 기반) ----------
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
 # ---------- 투시 영상 스틸 ----------
 {'t':'bigfig','eyebrow':'방법 · 영상으로','tag':('실제 투시상',''),
  'title':'투시 영상으로 본 술기 — 바늘은 이렇게 들어간다',
  'foot':'실제 시술 영상 스틸(TheProcedureGuide.com) · 사위 → 측면 → 정면 3-view · 교육용 인용',
  'svg':IMG('lsb_fluoro_steps.png','LSB 투시 술기 4단계', jpeg=True)},
 # ---------- 3D 애니메이션 스틸 ----------
 {'t':'bigfig','eyebrow':'방법 · 그림으로','tag':('3D 애니메이션',''),
  'title':'약물은 어디로 퍼지나 — 표적과 확산',
  'foot':'3D 의학 애니메이션 스틸 · 분홍=교감신경간(척추체 전외측), 파랑·보라=약물 확산 · 실제 확산 범위는 반드시 조영제로 확인 · 교육용 인용',
  'svg':IMG('lsb_anim_steps.png','LSB 3D 애니메이션 4단계', jpeg=True)},
 # ---------- L2·L3 조감도 (오리지널 도해) ----------
 {'t':'bigfig','eyebrow':'방법 · 그림으로','tag':('축상면 axial',''),'title':'L2·L3 조감도 — 표적과 위험 구조',
  'foot':'표적=척추체 전외측 교감신경절 · 방척추(정중선 ~7cm) 접근 · 대동맥·IVC·요관·신장·생식대퇴신경·추간공 회피 · 오리지널 도해','svg':AXIAL_SVG},
 # ---------- 해부 (도해 + 실제 도판 병합, 그림 최대 크기) ----------
 {'t':'photo','eyebrow':'해부','title':'요추 교감신경간 — 어디를 겨냥하나',
  'caption':'교감신경간은 척추체 <b>전외측</b>을 좌우로 종주하며 <b>대동맥에 바짝 붙어</b> 지나간다 — LSB 표적은 <b>L2–L3</b>. '
            '복강(T12–L1)·상·하장간막 신경절은 대동맥 전면. 이 인접성 때문에 <b>혈관 손상·혈관내 주입</b>이 핵심 위험이고, '
            '조영제로 확산을 반드시 확인한다. · 좌: 오리지널 도해 / 우: 해부학 교과서 도판(교육용 인용)',
  'img':IMG('lsb_anatomy_merged.png','요추 교감신경간 해부 — 관상면 도해와 교과서 도판', jpeg=True, q=88)},
 # ---------- L2·L3 시술 주의점 ----------
 {'t':'bullets','eyebrow':'방법 · 안전','tag':('시술 주의',''),'title':'L2·L3 시술 — 전·중 주의할 점','foot':'StatPearls NBK431107 · NBK557637 · Feigl 1998(PMID 9425975)','items':[
   (0,'<b>영상 유도 필수:</b> 투시(또는 CT). <b>조영제</b>로 두미측 종방향 확산 확인 — 후방(추간공)·혈관 확산 시 즉시 재위치.',''),
   (0,'<b>바늘 끝은 척추체 전외측</b>에 — <b>psoas·추간공 진입 금지.</b>',''),
   (0,'<b>요추신경총차단과 혼동 금지</b> — 그쪽 표적은 <b>psoas 구획(체성신경)</b>, LSB에선 <b>피해야 할 구조.</b>','red'),
   (0,'<b>레벨은 L2 하1/3~L3 상1/3</b>, <b>L4로 내려가지 말 것</b>(생식대퇴신경통 급증).',''),
   (0,'<b>흡인 후 분할·점진 주입</b>(혈관내·경막외 조기 발견) · 소량 시험주입.',''),
   (0,'<b>항응고·항혈소판제 중단</b>(심부·후복막 차단 — 출혈 위험) · 무균술.',''),
   (-1,'성공지표 온도 ≥2°C↑ 확인 · 시술 후 혈압·하지 근력/감각 모니터.','accent'),
 ]},
 # ---------- 대혈관·신장 천자 회피 (도해) ----------
 {'t':'bigfig','eyebrow':'안전 · 위험구조','tag':('혈관·신장 회피','red'),
  'title':'대동맥·IVC·신장을 피하는 법 — 뼈를 놓치지 않는다',
  'foot':'핵심 3가지 — ① 척추체 접촉을 유지한 채 뼈를 따라 미끄러뜨린다 ② 측면상에서 바늘 끝을 척추체 전연 앞으로 넘기지 않는다 ③ 너무 외측이면 신장, 너무 내측이면 추간공 · 오리지널 도해',
  'svg':AVOID_SVG},
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
 # ---------- 조영제 확산 읽기 (도해) ----------
 {'t':'bigfig','eyebrow':'안전 · 핵심기술','tag':('조영제 읽기',''),'title':'조영제 확산 읽기 — 이 패턴이면 멈춰라',
  'foot':'실시간 조영제가 최고의 안전장치 — 종방향(위·아래) 확산만 진행 · 혈관·경막외·근육내 패턴이면 즉시 바늘 재위치·재확인','svg':CONTRAST_SVG},
 # ---------- 합병증 & 회피법 (표) ----------
 {'t':'table','eyebrow':'안전성','tag':('합병증·회피','red'),'title':'합병증 & 회피법','foot':'StatPearls NBK431107·NBK557637 · Feigl 1998(PMID 9425975)',
  'note':"핵심: 투시+조영제로 확산 확인 · 바늘 전외측 유지 · L2~L3 표적 · 신경파괴는 진단차단 양성 시.",
  'headers':['합병증','원인·기전','피하는 법'],'rows':[
   ['생식대퇴신경통 (5–10%)','psoas 역류·자극 (<b>L2 0%·L4 40%</b>)','<b>L4 회피</b>·psoas 주입금지·최소용량'],
   ['혈관손상·혈관내주입','대동맥/IVC·요추혈관 인접','투시+<b>흡인+조영제</b>·항응고 중단'],
   ['요관·신장 천공','후복막 장기 인접','조영제로 깊이·궤적 확인'],
   ['체성신경·신경축 확산','바늘 후방→경막외 tracking','바늘 <b>전외측 유지</b>'],
   ['기립성 저혈압','교감차단 → 혈관확장','수액·서서히 기립·<b>양측 신중</b>'],
   ['신경염·사정장애','알코올/phenol·양측 <b>L1–L2</b>','진단차단 양성 시만·L1–L2 회피'],
  ]},
 # ---------- 생식대퇴신경통 심화 (도해) ----------
 {'t':'bigfig','eyebrow':'합병증 · 심화','tag':('최다 우려',''),'title':'생식대퇴신경통 — 가장 흔한 걱정, 대부분 회피 가능',
  'foot':'회피: L2하~L3상 표적·L4 회피·psoas 주입금지·소량 / 발생 시: 대개 수 주 내 자연호전·신경병증통 약물로 대증 · Feigl 1998(PMID 9425975)','svg':GF_SVG},
 # ---------- 혈관·LAST·신경 손상 대응 ----------
 {'t':'bullets','eyebrow':'합병증 · 대응','tag':('인지·구조','red'),'title':'혈관·LAST·신경 손상 — 조기 인지와 대응','foot':'ASRA LAST 지침 · StatPearls NBK431107','items':[
   (0,'<b>LAST(국소마취제 전신독성):</b> 입 주변 저림·이명·금속맛·어지럼 → 경련·부정맥.','red'),
   (0,'대응 — 즉시 중단·산소/기도·경련조절·<b>20% 지질유탁액 정주</b>·소생술. 예방 — 흡인+조영제+분할주입+용량제한.',''),
   (0,'<b>신경·신경축:</b> 주입 중 방사통·하지 위약 → 즉시 중단·재위치. 시술 후 근력·감각 확인.',''),
   (0,'<b>출혈·감염:</b> 항응고 중단·무균술 · 심한 통증·발열·팽창 시 즉시 평가.',''),
   (-1,'준비된 상태(모니터·정맥로·지질유탁액)면 대부분 안전하게 관리된다.','accent'),
 ]},
 # ---------- 합병증 대비 · 환자설명 ----------
 {'t':'bullets','eyebrow':'합병증 · 대비','tag':('환자 안심','ink'),'title':'합병증 대비 — 준비·조기인지·환자설명','foot':'교육용 정리','items':[
   (0,'<b>대부분 경미·자가회복</b> — 심각 합병증은 영상유도·정확한 술기로 드묾.',''),
   (0,'<b>준비:</b> 모니터·정맥로·응급장비·<b>20% 지질유탁액</b> 구비, 소생 프로토콜 숙지.',''),
   (0,'<b>조기 인지:</b> 조영제 패턴 + 환자 증상(통증·저림·어지럼)을 실시간 관찰.',''),
   (0,'<b>환자 설명(동의):</b> 흔한 것(일시적 저림·주사부위통·저혈압) vs 드문 것(신경통·출혈)을 사전 고지 → 신뢰·불안↓.',''),
   (-1,'신경파괴는 진단차단 양성 시에만·소량 — 위해를 최소화.','accent'),
 ]},
 {'t':'table','eyebrow':'적응증','tag':('적응',''),'title':'적응증 (Indications) — 우리 진료 비중 순','foot':'StatPearls; 문헌고찰 종합 · 순서는 본 강의의 임상 비중 기준',
  'note':"공통 관문은 <b>SMP인가</b> — <b>선행 질환이 없어도(특발·원발형) 적응이 된다.</b> 특발성 NLC·정맥질환은 적응 아님.",
  'headers':['순위','범주','대표 적응증'],'rows':[
   ['<b>①</b>','<b>신경병증</b>','<b>당뇨병성 말초신경병증/당뇨발</b> · 대상포진후신경통 · CIPN · 환상지통·단단통'],
   ['<b>②</b>','<b>하지통</b>','<b>암성 골반·하지통</b> · 수술후/외상후 난치통 · <b>원인 미상 만성 하지통</b> (SMP 소견 시)'],
   ['<b>③</b>','허혈질환','PAD·중증 하지허혈(CLI) 안정통·비재건성, 버거병, 색전, 동상, 혈관연축'],
   ['<b>④</b>','CRPS','하지 복합부위통증증후군(I/II) — <b>조기(≤12개월) 시행 유리</b>'],
   ['<b>⑤</b>','<b>특발·원발형</b>','<b>본태성 다한증</b>·<b>원발성 레이노</b>·<b>원발성 홍색사지통증</b> — 선행 질환 없이 교감 항진 자체가 문제'],
  ]},
 # ---------- 증상·호소 ① 신경병증 (최우선 · 가장 상세) ----------
 {'t':'bullets','eyebrow':'적응증 · 증상 ①','tag':('신경병증 · 최우선','green'),
  'title':'환자 증상·호소 ①-1 — 신경병증: 통증의 성질과 분포','foot':'StatPearls NBK442009; 문헌고찰 종합',
  'items':[
   (0,'<b>감각 양성증상:</b> <b>화끈거림(작열)</b> · <b>저림·찌릿한 전기 통증</b> · 쑤심 · <b>이질통</b>(양말·이불 스침에도 통증) · 통각과민',''),
   (0,'<b>감각 음성증상:</b> 감각저하·먹먹함 — <b>“양말을 겹쳐 신은 느낌”</b> · 위치감각 저하로 <b>휘청임</b>',''),
   (0,'<b>분포:</b> 양측 대칭 <b>‘양말’ 형</b>(당뇨병성) / 편측 분절형(대상포진후) / 수술·절단 부위(외상후)',''),
   (0,'<b>시간 양상:</b> <b>밤에 악화</b> — 이불 온기·야간 순환 변화·주의분산 소실 → <b>수면 방해</b>가 주 호소인 경우가 많다.','green'),
   (-1,'호소 그대로: “발이 저리고 화끈거려요” · “밤에 더 심해서 잠을 못 자요” · “전기가 찌릿 와요” · “남의 발 같아요”','accent'),
  ]},
 # ---------- 증상·호소 ①-2 신경병증: 자율신경 동반·진찰 ----------
 {'t':'bullets','eyebrow':'적응증 · 증상 ①','tag':('신경병증 · 최우선','green'),
  'title':'환자 증상·호소 ①-2 — 신경병증: 자율신경 소견과 진찰','foot':'StatPearls NBK442009; 문헌고찰 종합',
  'note':"신경병증 안에서도 <b>SMP 소견(작열통·이질통·온도·색·발한 이상)</b>이 겹칠수록 LSB 반응이 좋다.",
  'items':[
   (0,'<b>자율신경 동반(= SMP 단서):</b> 발이 <b>차갑거나 반대로 화끈</b> · 좌우 <b>온도·색 차이</b> · 발한 증가/감소 · 피부 건조·균열 · 부종','green'),
   (0,'<b>진찰:</b> 10 g 모노필라멘트·진동감각 저하 · 발목반사 소실 · 발톱·발가락 사이 변화',''),
   (0,'<b>당뇨발이면:</b> 잘 낫지 않는 <b>궤양</b>·관류저하 동반 — 통증뿐 아니라 <b>창상 치유</b>도 LSB의 기대 효과.','red'),
   (0,'<b>감별:</b> RLS(움직이면 완화)·야간경련(만져지는 근경직)·허혈성 안정통(ABI↓, 다리 내리면 완화)과 구분.',''),
   (-1,'1차: 혈당조절 + 약물(가바펜틴·프레가발린·듀록세틴) → <b>난치성이면 LSB 고려.</b>','accent'),
  ]},
 # ---------- 증상·호소 ② 하지통 ----------
 {'t':'bullets','eyebrow':'적응증 · 증상 ②','tag':('하지통',''),
  'title':'환자 증상·호소 ② — 난치성 하지통 (암성·수술후·외상후)','foot':'StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>암성 골반·하지통:</b> 골반강 종양·후복막 침범·골전이 — 깊은 <b>쑤심</b>에 <b>작열·발작통</b>이 겹치고 마약성 진통제로도 불충분',''),
   (1,'교감·내장 구심로를 함께 타는 통증이라 <b>교감차단이 보조 수단</b>이 된다.',''),
   (0,'<b>수술후·외상후 난치성 하지통:</b> 절단 후 <b>환상지통·단단통</b>, 신경손상 후 통증 — 발작적 <b>찌름·작열</b>, 날씨·추위에 악화',''),
   (0,'<b>공통 단서(SMP):</b> 통증 부위의 <b>색·온도 좌우차</b>, 발한 이상, 부종, <b>추위·스트레스에 악화</b> — 있으면 LSB 반응 가능성↑','green'),
   (-1,'호소 그대로: “진통제를 먹어도 밤새 쑤셔요” · “없는 발이 아파요” · “추운 날 유독 심해요”','accent'),
  ]},
 # ---------- 증상·호소 ③ 허혈 ----------
 {'t':'bullets','eyebrow':'적응증 · 증상 ③','tag':('허혈 · 동맥성',''),
  'title':'환자 증상·호소 ③ — 허혈성 통증 (PAD·CLI·버거병)','foot':'StatPearls; 문헌고찰 종합',
  'note':"‘허혈’은 <b>동맥성</b> 부족 — 하지정맥류 등 <b>정맥질환은 LSB 적응증 아님</b>(압박·정맥폐색술이 표준).",
  'items':[
   (0,'<b>간헐적 파행:</b> 일정 거리를 걸으면 종아리·둔부가 조이듯 아프고 <b>쉬면 수 분 내 완화</b> — 재현성이 특징.',''),
   (0,'<b>안정통(진행기):</b> 누우면 악화, <b>다리를 침대 밖으로 내리면 완화</b> — 야간에 심해 수면 방해.','green'),
   (0,'<b>진찰:</b> 차고 창백한 발, 말초맥박 감소·소실, 모세혈관 재충혈 지연, 발톱 비후·털 소실, <b>ABI 저하</b>',''),
   (0,'<b>조직 손상:</b> 잘 낫지 않는 궤양·괴저 — 재건 불가능한 CLI에서는 신경파괴가 <b>절단의 대안</b>이 된다.','red'),
   (-1,'호소 그대로: “걸으면 종아리가 터질 듯 아파요” · “밤에 발이 시려 잠을 못 자요” · “상처가 안 아물어요”','accent'),
  ]},
 # ---------- 증상·호소 ④ CRPS·기타 ----------
 {'t':'bullets','eyebrow':'적응증 · 증상 ④','tag':('CRPS · 기타',''),
  'title':'환자 증상·호소 ④ — CRPS · 기타','foot':'StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>하지 CRPS I/II</b> — 교감신경 매개 통증의 <b>전형</b>. 손상 정도에 비해 통증이 과하고 오래간다.',''),
   (1,'<b>작열통·이질통</b>(옷·바람 스침에도 통증)·통각과민 · 부종 · 피부색(발적↔창백↔청색) · <b>좌우 온도차</b> · 발한 이상',''),
   (1,'경과 시 <b>영양 변화</b>·관절 강직·근위축 → 조기(≤12개월) 시행이 유리한 이유.',''),
   (0,'<b>기타 — 족부 다한증·레이노(하지)·홍색사지통증</b>',''),
   (1,'다한증(과한 발땀·축축·악취) · 레이노(추위·스트레스에 <b>창백→청색→발적</b> 삼색변화) · 홍색사지통증(발작적 <b>발적·작열</b>, 열에 악화)',''),
   (-1,'호소 그대로: “이불만 스쳐도 아파요” · “붓고 색이 자꾸 변해요” · “추우면 발이 하얘졌다 파래져요”','accent'),
  ]},
 # ---------- NEW: 야간 신경병증통 서사 + LSB 치료 삽입 (NLC 스타일) ----------
 {'t':'split','eyebrow':'적응증 · 심화','tag':('야간 신경병증통',''),
  'title':'밤에 저리고 화끈거리는 다리 — 당뇨병성 신경병증과 LSB','foot':'Zhang 2020(RCT) PMID 32915421; 증례 PMID 22606406; StatPearls NBK442009',
  'items':[
   (0,'<b>임상상:</b> 당뇨병성 말초신경병증 — 발·종아리 <b>저림·화끈거림·전기 찌름</b>, 양측 ‘양말’ 분포.',''),
   (0,'<b>야간통:</b> 이불 온기·야간 순환·주의분산 소실 → 밤에 증폭·수면 방해.',''),
   (0,'<b>감별:</b> RLS(움직이면 완화)·NLC(경련)·허혈성 안정통과 구분.',''),
   (-1,'1차: 혈당조절+약물(가바펜틴·듀록세틴) → 난치성이면 <b>LSB 고려</b>','accent'),
  ],
  'aside':{'title':'LSB — 치료 삽입','dark':True,'items':[
   (0,'<b>기전:</b> 교감차단 → <b>미세순환↑</b> + 교감매개통 차단.',''),
   (0,'<b>근거:</b> 난치성 DPN에 LSB+신경파괴 <b>RCT</b>·증례.',''),
   (0,'<b>적용:</b> 진단차단 양성 시 선택적 시행.',''),
  ]}},
 {'t':'split','eyebrow':'효과','tag':('Lv III–IV','amber'),'title':'효과 ① 관류 개선 · 허혈성 통증','foot':'Dickey 2024 (Cureus); Medicina 2024; Barreto 2018',
  'items':[
   (0,'<b>관류 실측(Dickey 2024):</b> LSB 후 후경골동맥 직경 0.17→0.27 cm(+58.8%), 모세혈관 재충혈 3.92→1.30초, 족부온도 +2.8°C.',''),
   (0,'허혈성 통증(PAD): 하지 통증 최대 <b>75%↓</b>, Fontaine 분류·측부관류 개선(Medicina 2024).','green'),
   (0,'비재건성 CLI: 교감신경 신경파괴가 절단 외 대안이 없는 환자의 통증조절에 효과적·안전(Barreto 2018).',''),
  ],
  'aside':{'title':'실측 수치 (Dickey 2024)','stat':[('+58.8%','후경골동맥 직경'),('+2.8°C','족부온도'),('3.92→1.30s','모세혈관 재충혈')]}},
 {'t':'bullets','eyebrow':'효과','tag':('Lv III–IV','amber'),'title':'효과 ② CRPS · 기전','foot':'Choi 2024 (Sci Rep); Pain Ther 2023','items':[
   (0,'CRPS는 교감신경 매개 통증의 전형 → LSB 후 유의한 통증완화. 최적 환자 선택·조기 시행이 성공률↑.',''),
   (0,'Choi 2024(Sci Rep): 교감신경 신경파괴의 효과 지속기간을 전향 관찰로 제시.',''),
   (0,'반응 예측: <b>교감신경 피부반응(SSR)</b>이 LSB 반응 예측에 유용(Pain Ther 2023).',''),
   (0,'한계: 중추 감작이 진행되면 시간이 지날수록 효과 감소 가능.','muted'),
   (-1,'기전: 교감차단 → 측부순환 혈관확장 → 조직 산소화↑ → 통증↓ + 교감매개통 차단 + 신경파괴 직접효과.','accent'),
 ]},
 {'t':'bullets','eyebrow':'안전성 · 결론','tag':('결론','red'),'title':'근거수준 · 결론','foot':'Cochrane 2013 (CD002918); Manjunath 2008 (PMID 18227328); StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>Cochrane 2013(CD002918):</b> 신경병증통·CRPS 교감신경<b>절제</b> 무작위연구는 <b>단 1편(n=20)</b>, <b>위약 대조 0편.</b>','red'),
   (1,'Manjunath 2008: 하지 CRPS-1에서 <b>고주파 vs 7% phenol</b> — 통증 8–9/10 → 3–5/10(4개월). <b>두 군 차이 없음.</b>',''),
   (1,'결론: “근거가 매우 빈약 — <b>신중히, 선별된 환자에서, 대개 다른 치료 실패 후</b> 사용”.','muted'),
   (1,'단, 이 평가의 대상은 <b>신경파괴·절제</b> — 진단적·치료적 국소마취제 차단은 여기에 포함되지 않는다.','muted'),
   (0,'그 외 허혈·CRPS는 관찰·증례군 중심(Lv III~IV) · 난치성 당뇨병성 신경병증엔 별도 RCT 존재.',''),
   (-1,'근거는 약하지만 조기 CRPS·비재건성 중증 하지허혈·난치성 신경병증에서 <b>대안이 없을 때</b> 유용.','accent'),
 ]},
 # ---------- 나의 프로토콜 · 실제 적용 (NLC 스타일 단계적 접근) ----------
 {'t':'bullets','eyebrow':'나의 프로토콜 · 실제 적용','tag':('실전 순서','ink'),
  'title':'실제 진료 순서 — 교감신경 축을 겨냥한 단계적 접근','foot':'교육용 제안 · 개별 적용은 임상 판단 · 신경파괴는 진단차단 양성 시에만','items':[
   (0,'<b>① 감별·검사:</b> ‘밤/하지 증상’이 <b>동맥성 허혈(ABI·도플러)</b>·CRPS·신경병증인지 확인. 특발 경련·RLS·정맥류 배제.',''),
   (0,'<b>② 방향 설정:</b> 교감매개통·허혈로 판단되면 <b>교감신경 축(L2–L3)</b>을 겨냥.',''),
   (0,'<b>③ 진단적 차단:</b> 투시 유도 국소마취제 LSB → <b>피부온도 ≥2°C 상승·통증 반응</b> 확인.','green'),
   (0,'<b>④ 반응 양호 시:</b> 치료적 반복 차단, 또는 <b>신경파괴(무수알코올/phenol)·RFA</b>로 장기 완화.','green'),
   (0,'<b>⑤ 대상별:</b> CRPS는 조기(≤12개월) 유리 · 난치성 당뇨병성 신경병증은 지속 LSB+신경파괴(RCT).',''),
   (-1,'⑥ 주의: 특발성 NLC·정맥질환은 적응 아님 · 합병증(생식대퇴신경통 5–10% 등) 사전 고지.','accent'),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · LSB','headline':'표준은 투시 유도 방척추 접근, 성공은 온도 ≥2°C','msgs':[
   ('방법','L2–L3 방척추 접근·투시, 정중선 7 cm 외측, 조영제 두미측 확산, 성공지표 온도 ≥2°C.'),
   ('약제','진단/치료는 국소마취제, 신경파괴는 무수알코올/phenol·RFA — 진단차단 양성 시에만.'),
   ('적응증','조기 CRPS·PAD/CLI 안정통·신경병증·다한증 등. 특발성 NLC·정맥질환(정맥류)은 적응 아님.'),
   ('효과','관류 실측 개선(Dickey), 허혈통 최대 75%↓, CRPS 통증완화(SSR로 예측).'),
   ('근거','신경파괴 RCT는 <b>Cochrane상 1편(n=20)</b>뿐 — 다른 치료 실패 후 신중히.'),
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
   ('<b>Manjunath.</b> RF thermal lumbar sympathectomy vs phenol neurolysis, lower-limb CRPS-1 (RCT n=20). Anesth Analg. 2008.',PM(18227328)),
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
LSB.append({'t':'key','eyebrow':'전체 흐름 · Roadmap',
  'headline':'누구에게 → 어디를 → 왜 → 어떻게 → 안전하게','msgs':[
   ('① 감별','밤·하지 증상 중 <b>LSB가 듣는 것</b>과 아닌 것을 먼저 가른다'),
   ('② 해부','교감신경간은 척추체 <b>전외측 L2–L3</b> — 표적과 주변 위험 구조'),
   ('③ 적응증·증상','CRPS·허혈·신경병증에서 환자가 실제로 하는 말'),
   ('④ 효과','관류 실측·통증 감소·CRPS 완화 <b>(근거수준과 함께)</b>'),
   ('⑤ 술기·안전','투시+조영제로 정확히 — 합병증은 대부분 <b>회피·관리 가능</b>'),
 ]})

# ---------- 강의 흐름에 맞춘 슬라이드 순서 재배열 ----------
_ORDER = ['요추교감신경차단', '전체 흐름', '밤·하지 증상 감별', '교감신경 매개 통증(SMP)',
          '개요 · 해부 · 원리', '요추 교감신경간 — 어디를',
          '적응증 (Indications)',
          '증상·호소 ①-1', '증상·호소 ①-2', '신경병증은 당뇨병성만이',
          '증상·호소 ② — 난치성 하지통', '증상·호소 ③ — 허혈성', '증상·호소 ④ — CRPS',
          '밤에 저리고 화끈거리는 다리', '효과 ① 관류', '효과 ② CRPS',
          '방법 (Technique)', '약물은 어디로 퍼지나', '실제 투시 술기', '투시 영상으로 본',
          'L2·L3 조감도', '대동맥·IVC·신장을 피하는', '혈관·신장 천자', '조영제 확산 읽기', 'L2·L3 시술',
          '합병증 & 회피법', '생식대퇴신경통', '혈관·LAST·신경 손상', '합병증 대비',
          '근거수준 · 결론', '실제 진료 순서', '표준은 투시 유도', '참고문헌']

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
_DENSE = ['전체 흐름', '밤·하지 증상 감별', '교감신경 매개 통증(SMP)', '개요 · 해부 · 원리',
          '적응증 (Indications)', '증상·호소 ①', '증상·호소 ②', '증상·호소 ③', '증상·호소 ④',
          '신경병증은 당뇨병성만이', '밤에 저리고 화끈거리는 다리', '효과 ② CRPS',
          '방법 (Technique)', '실제 투시 술기', '혈관·신장 천자', 'L2·L3 시술', '합병증 & 회피법',
          '근거수준 · 결론', '실제 진료 순서', '표준은 투시 유도']
for _s in LSB:
    _t = _skey(_s) + ' ' + (_s.get('eyebrow') or '')
    if any(f in _t for f in _DENSE):
        _s['dense'] = True

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"
TITLE = "요추교감신경차단 · 문헌고찰 발표"
FNAME = "LSB_발표_웹"

# ---- font sources: /tmp/pretendard 우선, 없으면 업로드 경로 폴백 ----
TMP = "/tmp/pretendard"
UP = "/root/.claude/uploads/bb19d1cb-d1ba-542e-8235-38fcac774773/"
def pick(tmp_name, up_name):
    p = os.path.join(TMP, tmp_name)
    return p if os.path.exists(p) else (UP + up_name)
FONTS = {
  "__F900__": pick("Pretendard-Black.otf",     "c71b728f-PretendardBlack.otf"),
  "__F800__": pick("Pretendard-ExtraBold.otf", "3a19e05c-PretendardExtraBold.otf"),
  "__F700__": pick("Pretendard-Bold.otf",      "1121d3ff-PretendardBold.otf"),
  "__F300__": pick("Pretendard-Light.otf",     "82c21b19-PretendardLight.otf"),
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
