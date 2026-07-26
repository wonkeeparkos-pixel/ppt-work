# -*- coding: utf-8 -*-
"""NLC 발표 웹덱 v1.1 (수정본). 사용자 지정 수정사항 반영."""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026 · v1.1"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

# ---- SVG: 반사 균형 / 단축 → 경련 (page 3 그림) ----
SVG_NORMAL = '''<div class="figpanel good"><div class="pt">정상 · 균형</div>
<svg viewBox="0 0 300 210" role="img">
 <!-- 근육 -->
 <rect x="60" y="40" width="150" height="60" rx="26" fill="#CFE3D2" stroke="#2E7D32" stroke-width="2.5"/>
 <text x="135" y="76" text-anchor="middle" font-size="13" font-weight="800" fill="#1c4a22">종아리 근육</text>
 <!-- 힘줄 -->
 <line x1="210" y1="70" x2="270" y2="70" stroke="#0B5F5E" stroke-width="6" stroke-linecap="round"/>
 <circle cx="255" cy="70" r="11" fill="#0E7C7B"/>
 <text x="255" y="98" text-anchor="middle" font-size="10.5" font-weight="700" fill="#0B5F5E">GTO</text>
 <text x="255" y="110" text-anchor="middle" font-size="9.5" fill="#55615B">건기관·브레이크</text>
 <!-- 근방추 -->
 <ellipse cx="110" cy="70" rx="16" ry="7" fill="#fff" stroke="#0E7C7B" stroke-width="2"/>
 <text x="110" y="122" text-anchor="middle" font-size="9.5" fill="#55615B">근방추·가속</text>
 <!-- 척수 -->
 <rect x="30" y="150" width="240" height="34" rx="8" fill="#EAF1EF" stroke="#0E7C7B" stroke-width="1.6"/>
 <text x="150" y="172" text-anchor="middle" font-size="11.5" font-weight="700" fill="#0B5F5E">척수 반사 (브레이크 정상 작동)</text>
 <line x1="255" y1="81" x2="230" y2="150" stroke="#2E7D32" stroke-width="2"/>
 <line x1="110" y1="77" x2="90" y2="150" stroke="#9AA6A2" stroke-width="1.6" stroke-dasharray="4 3"/>
</svg>
<div class="pl"><b>건기관(GTO)</b>이 "너무 세다·멈춰" 신호 → 근육 <b>이완</b></div></div>'''

SVG_CRAMP = '''<div class="figpanel warn"><div class="pt">단축된 위치 · 경련</div>
<svg viewBox="0 0 300 210" role="img">
 <!-- 짧아진 근육(수축) -->
 <rect class="a-cramp" x="78" y="42" width="110" height="56" rx="24" fill="#F2C9C1" stroke="#A8352A" stroke-width="2.5"/>
 <text x="133" y="76" text-anchor="middle" font-size="12.5" font-weight="800" fill="#7a221a">뭉친 근육</text>
 <!-- 느슨한 힘줄 -->
 <path d="M188 70 q20 14 40 0 q12 -10 30 0" fill="none" stroke="#0B5F5E" stroke-width="5" stroke-linecap="round"/>
 <circle cx="250" cy="70" r="11" fill="#B98"/>
 <text x="250" y="98" text-anchor="middle" font-size="10.5" font-weight="700" fill="#A8352A">GTO 느슨</text>
 <!-- 운동종판 스파크 -->
 <circle class="a-spark" cx="110" cy="70" r="9" fill="#A8352A"/>
 <text x="110" y="120" text-anchor="middle" font-size="9.5" fill="#7a221a">운동종판 폭주</text>
 <!-- 척수 -->
 <rect x="30" y="150" width="240" height="34" rx="8" fill="#FCEBE7" stroke="#A8352A" stroke-width="1.6"/>
 <text x="150" y="172" text-anchor="middle" font-size="11.5" font-weight="700" fill="#A8352A">척수가 신호를 되먹임해 증폭</text>
 <line class="a-flow" x1="250" y1="81" x2="225" y2="150" stroke="#A8352A" stroke-width="2"/>
 <line class="a-flow" x1="110" y1="79" x2="95" y2="150" stroke="#A8352A" stroke-width="2"/>
</svg>
<div class="pl">발끝이 펴져 근육이 <b>짧아짐</b> → 브레이크 헐거워지고 신경-근육 접점 <b>예민</b> → 폭주·경련</div></div>'''

NLC = [
 {'t':'title','eyebrow':'Nocturnal Leg Cramps · 문헌고찰','title':'야간 하지경련',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사기법 · 경구약제 · 우리 프로토콜','series':SERIES},

 # ---- Page 2: 병태생리 (쉬운 말) ----
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'다리 근육을 움직이는 신경이 과흥분한다','foot':'Miller & Layzer 2005; Minetto 2011·2013','items':[
   (0,'야간 하지경련 = 근육이 스스로 <b>오작동</b>해 갑자기 강하게 뭉치는 것. 근육으로 가는 <b>운동신경이 과도하게 흥분</b>해 신호를 마구 쏘아서 생긴다.',''),
   (0,'신호가 정상보다 훨씬 빠르게 폭주 — 신경 끝에서 <b>초당 최대 150번(150 Hz)</b>까지 제멋대로 발화한다(Miller & Layzer 2005). 그래서 근육이 안 풀리고 뭉친다.',''),
   (0,'어디서 시작하나: 신경 끝(말초)만 막아도 경련은 생기지만 <b>더 세게 자극해야 하고 금방 멎는다</b>(Minetto 2011).',''),
   (-1,'→ 불씨는 <b>근육 끝(말초)</b>에서 붙고, <b>척수(중추)</b>가 되먹임으로 부채질해 키운다. <b>말초+중추 합작</b>.','accent'),
   (0,'노인에서 부추기는 요인: 요추관협착·신경눌림, 정맥순환 저하, 신경병증, 전해질 이상, 약물(천식흡입제·이뇨제·고지혈증약).',''),
 ]},

 # ---- Page 3: 그림 (GTO·운동종판) ----
 {'t':'figure','eyebrow':'병태생리','tag':('그림으로',''),'title':'가속과 브레이크 — 왜 짧아진 근육에서 경련이 나나',
  'foot':'Minetto 2013; Khan & Burne 2007',
  'svg':SVG_NORMAL+SVG_CRAMP,
  'caption':'<b>근방추(Ia)</b>=근육을 더 당기라는 <b>가속페달</b>, <b>골지건기관(GTO, Ib)</b>=너무 세니 멈추라는 <b>브레이크</b>. <b>운동종판</b>=신경이 근육에 명령을 넘겨주는 접점. 자는 동안 발끝이 펴져 종아리가 <b>짧아지면</b> 브레이크(GTO)가 헐거워지고 접점이 예민해져 작은 자극에도 폭주 → 경련. 그래서 <b>발끝을 몸쪽으로 당기면(스트레칭)</b> 힘줄이 당겨져 브레이크가 다시 걸리고 풀린다.'},

 # ---- Page 4: 주된 호소 (유지) ----
 {'t':'bullets','eyebrow':'임상 양상','tag':('호소',''),'title':'환자들의 주된 호소','foot':'Hallegraeff 2017; Grandner & Winkelman 2017','items':[
   (0,'수면 중 갑작스러운 종아리·발의 <b>강한 통증성 경련</b>으로 각성.',''),
   (0,'해당 근육이 단단하게 뭉침(<b>촉지되는 근경직</b>), 발끝을 몸쪽으로 당기면(족배굴곡) 완화.',''),
   (0,'지속 수초~최대 10분, 이후 <b>잔통</b>이 남고 수면 분절·주간 피로.',''),
   (0,'위치는 후종아리(비복근)·발이 대부분. 유병률 50세+ 경증 24~25%·중등도이상 ~6%, 요추관협착 시 최대 65%.',''),
   (-1,'감별: RLS(움직임 충동·움직이면 완화·근경직 없음)와 반드시 구분.','accent'),
 ]},

 # ---- Page 5: 치료 개관 (재정렬·비약물 제거) ----
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 근거 순','foot':'문헌고찰 종합',
  'headers':['치료','대표','야간경련 근거','위치'],'rows':[
   ['ESWT','종아리 표적 충격파','Li 2021(후향)+경직 RCT/MA','보조·근거형성 중'],
   ['주사','국소마취제 유발점','Kim 2015·Prateepavanich 1999','MTrP 동반 시'],
   ['주사','심비골신경 내측분지 차단','Imura 2015 <b>직접근거</b>','불응성 선택'],
   ['주사','보툴리눔(비복근)','Park 2017 RCT (Lv II)','불응성·고가'],
   ['경구약제','비타민 B·K2 → diltiazem','Chan·Tan·Voon (Lv C)','안전·우선'],
   ['경구약제','quinine','El-Tawil (효과O)','독성 → <b>최후</b>'],
  ],
  'note':'탐색적(Level V): 신경주위 dexamethasone · FGA(비복근 원위건막) 주사 — 뒤 슬라이드 참조.'},

 # ---- Page 6: ESWT 직접/경직 근거 (쉬운 말·MAS 정의) ----
 {'t':'split','eyebrow':'치료 · 체외충격파(ESWT)','tag':('근거형성중','amber'),'title':'종아리 충격파 — 경련 근거는 약, 경직 근거는 강','foot':'Li 2021; Otero-Luis 2024',
  'items':[
   (0,'<b>Li 2021</b>(후향 n=126): 종아리 충격파 → 경련·통증 크게 감소. 경련을 직접 본 <b>유일</b> 연구.',''),
   (0,"'경련' 무작위연구는 없어 <b>사촌격 '경직'(spasticity·근육이 늘 뻣뻣)</b> 근거를 빌린다 — 경직엔 RCT·메타분석이 탄탄해 충격파가 <b>근긴장도(MAS)를 0.40점↓</b>(Otero-Luis 2024).",''),
   (-1,'표적·목표가 같아 경련에도 기대하는 <b>간접근거</b> → 보조·실험 단계.','accent'),
  ],
  'aside':{'title':'Li 2021 결과 (ESWT군)','stat':[('5.7→1.3','경련 빈도 (회/시간)'),('57.6→10.6','지속 (초)'),('P<0.001','대조군 대비')]}},

 # ---- Page 7: ESWT 기전·프로토콜·한계 (가독성 재배치 split) ----
 {'t':'split','eyebrow':'치료 · ESWT','tag':('기전·프로토콜',''),'title':'어떻게 듣고, 어떻게 놓나','foot':'Yang 2021 (J Clin Med, 기전 리뷰)',
  'items':[
   (0,'<b>어떻게 듣나(기전, Yang 2021):</b> 충격파가 신경-근육 접합부를 리모델링(ACh수용체↓)하고 운동신경 흥분성을 낮춘다. 혈류·미세순환도 개선.',''),
   (0,'<b>NO 합성↑</b>·CMAP 6~8주 감소 등으로 과흥분이 가라앉는 것으로 설명된다.',''),
   (-1,'<b>왜 완치가 아닌가(한계):</b> 특발성 경련만 본 RCT가 없고, 효과가 대개 <b>12주 이내로 단기</b> → 보조·근거형성 단계.','accent'),
  ],
  'aside':{'title':'표준 프로토콜','items':[
   (0,'표적: 비복근 내·외측두·가자미근 <b>운동점</b>',''),
   (0,'강도: radial 1.5–2.5 bar / focused ~0.10 mJ/mm²',''),
   (0,'용량: <b>2,000–3,000</b> shots/근육',''),
   (0,'주기: <b>주 1–2회 × 3–4주</b>',''),
   (0,'상대금기: 항응고·DVT·감염·악성·임신',''),
   (-1,'초음파 유도 권장','accent'),
  ]}},

 # ---- Page 8: ① 유발점 주사 (상세) ----
 {'t':'split','eyebrow':'치료 · 주사기법','tag':('효과 있음','green'),'title':'① 국소마취제 유발점 주사','foot':'Kim 2015; Prateepavanich 1999',
  'items':[
   (0,'개념: 비복근 <b>근막통증유발점(MTrP)</b> — taut band 속 최대 압통점 — 에 소량 국소마취제 → 국소 근이완·유발점 비활성화.',''),
   (0,'결과(Kim 2015, n=12): NRS·경련 빈도·불면지수(ISI) 모두 유의 개선(P<0.01), 임상 불면 10명→4주째 1명.','green'),
   (0,'Prateepavanich 1999(RCT n=24): 리도카인 주사 vs quinine — <b>지속효과는 주사군 우월</b>.',''),
  ],
  'aside':{'title':'술기 상세 (Kim 2015)','items':[
   (0,'약제: <b>0.25% 리도카인 1–2 mL</b>',''),
   (0,'바늘: <b>25 G</b> · 피부 <b>30°</b> 자입',''),
   (0,'표적: taut band 최대 압통점(비복근 내측두)',''),
   (0,'<b>주입 전 흡인</b>(혈관내 회피) · 주 1회 · 초음파 유도',''),
  ]}},

 # ---- Page 9(구): dry needling 제거 ----

 # ---- ② 심비골신경 차단 (부위 명확화) ----
 {'t':'split','eyebrow':'치료 · 주사기법 · 직접근거','tag':('직접 근거',''),'title':'② 심비골신경 내측분지 차단','foot':'Imura 2015 (Brain Behav; PMID 26445706)',
  'items':[
   (0,'<b>Imura 2015:</b> 야간경련에 <b>말초 운동신경가지를 직접 표적</b>한 유일한 전향적 비교연구(요추수술 후 종아리·발 경련 66명).',''),
   (0,'<b>어디를 찌르나:</b> 발등 <b>제1–2 중족골 사이 원위 2/3</b>(심비골신경 <b>내측 종말가지</b>). 1.0% 리도카인 <b>5.0 mL</b>를 1.0–1.5 cm 깊이에.',''),
   (-1,'<b>왜 발등에 찌르는데 종아리가 주나:</b> 근육 마비(BTX)가 아니라 발의 <b>구심성 입력을 차단</b>해 경련 반사고리를 끊기 때문.','accent'),
  ],
  'aside':{'title':'결과 (2주 시점)','stat':[('61% vs 20%','빈도 1/4↓'),('80.5%','빈도 1/2↓ (P<0.01)'),('63.4%','12주+ 지속')]}},

 # ---- ③ 보툴리눔 (유지·번호 조정) ----
 {'t':'bullets','eyebrow':'치료 · 주사기법','tag':('효과 있음','green'),'title':'③ 보툴리눔 + 안전성','foot':'Park 2017·Restivo 2018','items':[
   (0,'<b>Park 2017 RCT(n=50):</b> 요추관협착 동반 야간 종아리경련. 비복근 BTX-A vs gabapentin → 전 시점 통증·빈도·강도 유의 감소(P<0.01).','green'),
   (0,'Restivo 2018 RCT: 당뇨병성 신경병증 경련에서 위약 대비 개선(1주부터 16주 지속).',''),
   (0,'주사 계열 중 근거 최고(Lv II)이나 고가·반복·근력약화 우려 → 선택적.',''),
   (-1,'안전(고령): 경골신경→족저굴곡 약화, 총비골신경→족하수→낙상. 초음파 유도·혈관내 주입 회피.','red'),
 ]},

 # ---- ④ 신경주위 dexamethasone (신규·Lv V) ----
 {'t':'bullets','eyebrow':'치료 · 주사기법 · 탐색적','tag':('Level V','amber'),'title':'④ 신경주위 덱사메타손 주사 — 가능성','foot':'기전 기반 유추 · 직접 임상근거 없음 (Level V)',
  'items':[
   (0,'<b>착상:</b> 경련을 유지하는 것은 운동신경 과흥분. 그렇다면 그 근육을 지배하는 <b>신경 줄기 주위</b>에 덱사메타손을 두면 이소성 과흥분·신경주위 염증을 눌러 경련 역치를 올릴 수 있다.',''),
   (0,'<b>표적 신경 = 경련 부위로 정한다:</b>',''),
   (1,'<b>후경골신경</b>(오금~족근관): 종아리 뒤칸(비복근·가자미근)·발바닥 지배 → <b>종아리 경련</b>.',''),
   (1,'<b>총비골신경</b>(비골두 뒤): 앞·가쪽칸(정강이·발등) 지배 → <b>정강이·발 경련</b>.',''),
   (-1,'근거: 덱사메타손은 말초신경차단의 <b>검증된 보조제</b>(진통 연장·항염). 단 경련 직접근거는 <b>없음</b> → 기전기반 <b>Level V</b>.','accent'),
   (0,'안전: 초음파 유도 필수, 신경내 주입 회피, 운동가지 차단 시 일시적 근력저하·족하수(총비골) 주의.','red'),
 ]},

 # ---- ⑤ FGA 주사 (신규·Lv V) ----
 {'t':'split','eyebrow':'치료 · 주사기법 · 탐색적','tag':('Level V','amber'),'title':'⑤ FGA 주사 — 신규 가설','foot':'Pedret 2020 (Scand J Med Sci Sports); Balius 2018',
  'items':[
   (0,'<b>FGA</b>(유리 비복근 건막) = 비복근 <b>내측두 근섬유가 끝나는 원위</b>의 자유 건막(원위 근-건 이행부 = <b>tennis leg</b> 부위)(Pedret 2020).',''),
   (0,'<b>왜 표적:</b> <b>GTO·근방추 밀집</b>·힘 전달 집중 부위 → 경련 호발, <b>건 자극으로 반사 억제</b>됨.',''),
   (0,'<b>간접 근거:</b> 비복근 국소주사(유발점·BTX)의 야간경련 감소 → FGA는 이를 <b>더 정밀화</b>한 표적.',''),
   (-1,'<b>직접 근거 없음 — 신규 가설(Lv V).</b> 표준치료 아님.','red'),
  ],
  'aside':{'title':'주사 범위·안전','items':[
   (0,'범위: <b>최원위 근섬유부 ~ AT 형성 직전</b> 건막 평면',''),
   (0,'<b>초음파 유도 필수</b> · 평면내(in-plane)',''),
   (0,'회피: <b>소복재정맥·비복신경·족척근</b> (GA–SA 확산 주의)',''),
   (0,'급성 통증·부종 시 <b>DVT 감별</b>',''),
  ]}},

 # ---- Page 12: 경구약제 (재정렬) ----
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'경구 약제 — 안전한 것부터','foot':'AAN(Katzberg 2010); Cochrane 종합',
  'headers':['약제','근거','평가'],'rows':[
   ['비타민 B 복합','Chan 1998 RCT','빈도·강도 감소·안전 <b>Lv C</b> → 우선 시도'],
   ['Vitamin K2','Tan 2024 (JAMA IM)','빈도 2.60→0.96 (⚠정정 통지·과대해석 금지)'],
   ['Diltiazem 30mg','Voon 2001 교차','빈도 5.8→0.16/2주, Lv C'],
   ['마그네슘(특발성)','Garrison 2020 Cochrane','임상 이득 없음 — <b>권고 안 함</b>'],
   ['Quinine','El-Tawil 2015 Cochrane','효과 O이나 혈소판감소/TTP·FDA 미승인 → <b>최후</b>'],
  ]},

 # ---- Page 13(구): 비약물 슬라이드 제거 ----

 # ---- our protocol (신규) ----
 {'t':'bullets','eyebrow':'우리 프로토콜 · 제안','tag':('종합','ink'),'title':'단계적 접근 — 덜 침습에서 더 침습으로','foot':'문헌고찰 종합 · 교육용 제안(개별 진료는 담당의 판단)',
  'items':[
   (0,'<b>0. 감별·원인교정:</b> RLS 감별 · 이차원인(요추협착·정맥부전·전해질·유발약물) 점검.',''),
   (0,'<b>1. 기본(모두에게):</b> 취침 전 종아리·햄스트링 스트레칭 · 급성 시 족배굴곡·마사지.',''),
   (0,'<b>2. 경구(안전 우선순):</b> 비타민 B 복합 ± K2 → 반응 없으면 diltiazem · quinine은 독성으로 <b>최후</b>.',''),
   (0,'<b>3. 불응 시 주사(근거순):</b> ① 비복근 유발점 국소마취제 → ② 심비골신경 차단(Imura) → ③ 보툴리눔(선택).','green'),
   (0,'<b>4. 탐색적(연구 틀·Lv V):</b> 신경주위 덱사메타손(경련 부위 맞춤) · FGA(비복근 원위건막) 초음파 유도.','accent'),
   (-1,'원칙: <b>덜 침습→더 침습</b> · 모두 <b>초음파 유도·안전 우선</b> · 효과·부작용 재평가하며 단계 이동.','accent'),
  ]},

 # ---- key (갱신) ----
 {'t':'key','eyebrow':'핵심 메시지 · NLC','headline':'감별이 먼저 · 기본 위에 근거순 단계적 주사','msgs':[
   ('감별','통증성 근수축·촉지 근경직·족배굴곡 완화 → RLS와 반드시 구분.'),
   ('토대','스트레칭·유발약물 검토·이차원인 교정이 모든 단계의 바탕.'),
   ('주사(근거)','유발점 국소마취제·심비골신경 차단(Imura)·보툴리눔(RCT)이 불응성 핵심.'),
   ('주사(탐색)','신경주위 덱사메타손·FGA(비복근 원위건막)는 기전기반 Level V — 연구 틀 안에서.'),
   ('경구·ESWT','비타민B·K2/diltiazem 안전·quinine 최후·마그네슘 무효; ESWT는 보조.'),
 ]},

 # ---- refs (갱신) ----
 {'t':'refs','title':'참고문헌 — NLC','refs':[
   ('<b>Miller & Layzer.</b> Muscle cramps. Muscle Nerve. 2005.',PM(15902691)),
   ('<b>Minetto.</b> Mechanisms of cramp contractions. J Physiol. 2011.',PM(21969448)),
   ('<b>Minetto.</b> Origin and development of muscle cramps. Exerc Sport Sci Rev. 2013.',PM(23038243)),
   ('<b>Khan & Burne.</b> Reflex inhibition of cramp by tendon stim. J Neurophysiol. 2007.',PM(17634341)),
   ('<b>Hallegraeff.</b> Stretching before sleep reduces NLC: RCT. J Physiother. 2012.',PM(22341378)),
   ('<b>Li.</b> ESWT reduces leg cramps in lumbar degenerative disorders. Biomed Res Int. 2021.',PM(34734084)),
   ('<b>Otero-Luis.</b> ESWT for spasticity: SR & MA. J Clin Med. 2024.',PM(38592705)),
   ('<b>Kim.</b> MTrP injections on nocturnal calf cramps. J Am Board Fam Med. 2015.',PM(25567819)),
   ('<b>Prateepavanich.</b> Lidocaine injection vs quinine for nocturnal cramps. 1999.',None),
   ('<b>Imura.</b> Deep peroneal nerve medial branch block for NLC. Brain Behav. 2015.',PM(26445706)),
   ('<b>Park.</b> Botulinum toxin for nocturnal calf cramps in LSS: RCT. Arch Phys Med Rehabil. 2017.',PM(28209505)),
   ('<b>Pedret.</b> Ultrasound classification of medial gastrocnemius injuries (FGA). Scand J Med Sci Sports. 2020.',PM(32854168)),
   ('<b>Balius.</b> Extracellular matrix in muscle injuries (GA–SA plane). Orthop J Sports Med. 2018.',PM(30246041)),
   ('<b>El-Tawil.</b> Quinine for muscle cramps. Cochrane. 2015.',PM(25842375)),
   ('<b>Garrison.</b> Magnesium for skeletal muscle cramps. Cochrane. 2020.',PM(32956536)),
   ('<b>Chan.</b> Vitamin B complex for NLC: RCT. J Clin Pharmacol. 1998.',PM(11301568)),
   ('<b>Voon & Sheu.</b> Diltiazem for nocturnal leg cramps. Age Ageing. 2001.',PM(11322688)),
   ('<b>Katzberg (AAN).</b> Symptomatic treatment for muscle cramps: evidence-based review. Neurology. 2010.',PM(20177124)),
 ]},
]

TITLE = "야간 하지경련 · 문헌고찰 발표 · v1.1 (수정본)"
BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/01_NLC"
htmlc = render_deck(TITLE, NLC)
# 화면 하단 버전 라벨 강조
htmlc = htmlc.replace(f'<div class="deckttl">{TITLE}</div>',
                      '<div class="deckttl">야간 하지경련 · 문헌고찰 발표 · <b>v1.1 (수정본)</b></div>')

# ---- 폰트 서브셋 ----
vis = re.sub(r'<style.*?</style>','',htmlc,flags=re.S)
vis = re.sub(r'<script.*?</script>','',vis,flags=re.S)
vis = re.sub(r'<[^>]+>',' ',vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@")
text=''.join(sorted(chars)); print("glyphs:",len(chars))

UP=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","fonts")+"/"
FONTS={"__F900__":UP+"PretendardBlack.otf","__F800__":UP+"PretendardExtraBold.otf",
       "__F700__":UP+"PretendardBold.otf","__F300__":UP+"PretendardLight.otf"}
for ph,path in FONTS.items():
    o=Options(); o.flavor='woff2'; o.desubroutinize=True; o.name_IDs=[]; o.name_legacy=False; o.name_languages=[]
    f=TTFont(path); s=Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf=io.BytesIO(); f.save(buf); uri="data:font/woff2;base64,"+base64.b64encode(buf.getvalue()).decode()
    htmlc=htmlc.replace(ph,uri); print(ph,f"{len(buf.getvalue())/1024:.0f}KB")

out=os.path.join(BASE,"NLC_발표_웹_v1.1.html")
open(out,'w',encoding='utf-8').write(htmlc)
print("slides:",len(NLC),"| out:",out,f"{len(htmlc.encode())/1024:.0f}KB")
