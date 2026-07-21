# -*- coding: utf-8 -*-
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
def PMC(x): return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x}/"

# ==================================================== NLC
NLC = [
 {'t':'title','eyebrow':'Nocturnal Leg Cramps · 문헌고찰','title':'야간 하지경련',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사기법 · 경구약제','series':SERIES},
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'운동신경 과흥분에서 기원한다','foot':'Miller & Layzer 2005; Minetto 2011','items':[
   (0,'NLC는 <b>운동신경의 폭발적 과흥분</b>에 의한 불수의적·유통성 근수축이다.',''),
   (0,'진성 근경련은 원위 운동축삭 종말의 자발적·고빈도(최대 ~150 Hz) 방전에서 기원(Miller & Layzer 2005).',''),
   (0,'Minetto 2011: 후경골신경 차단 하에서도 경련은 유발되나 더 높은 자극빈도 필요·지속이 짧음.',''),
   (1,'→ 경련 유지에는 척수 회로(운동뉴런 과흥분의 양성 되먹임)가 필수. 중추+말초 복합.','accent'),
   (0,'이차 유발: 요추관협착·신경근병증, 정맥부전, 신경병증, 전해질, 약물(LABA·이뇨제·statin).',''),
 ]},
 {'t':'split','eyebrow':'병태생리','tag':('기전',''),'title':'반사 불균형과 근단축','foot':'Minetto 2013; Khan & Burne 2007',
  'items':[
   (0,'<b>근방추(Ia) 흥분</b> ↑ + <b>골지건기관(Ib) 억제</b> ↓ 불균형이 경련을 촉발·유지.',''),
   (0,"경련은 근육이 '단축'된 위치(수면 중 발 저측굴곡)에서 거의 배타적으로 발생, 신전으로 완화.",''),
   (0,'단축 시 GTO 억제가 약해지고 운동종판 흥분 역치가 낮아진다(Minetto 2013).',''),
  ],
  'aside':{'title':'왜 스트레칭이 듣는가','items':[
   (0,'Khan & Burne 2007: 아킬레스건 자극이 진행 중 경련을 <b>반사적으로 억제</b>.',''),
   (0,'신전·건 자극이 Ib 구심성으로 경련 회로를 직접 겨냥.',''),
   (-1,'→ 스트레칭·족배굴곡이 급성 완화·예방의 생리적 근거.','accent'),
  ]}},
 {'t':'bullets','eyebrow':'임상 양상','tag':('호소',''),'title':'환자들의 주된 호소','foot':'Hallegraeff 2017; Grandner & Winkelman 2017','items':[
   (0,'수면 중 갑작스러운 종아리·발의 <b>강한 통증성 경련</b>으로 각성.',''),
   (0,'해당 근육이 단단하게 뭉침(<b>촉지되는 근경직</b>), 발끝을 몸쪽으로 당기면(족배굴곡) 완화.',''),
   (0,'지속 수초~최대 10분, 이후 <b>잔통</b>이 남고 수면 분절·주간 피로.',''),
   (0,'위치는 후종아리(비복근)·발이 대부분. 유병률 50세+ 경증 24~25%·중등도이상 ~6%, 요추관협착 시 최대 65%.',''),
   (-1,'감별: RLS(움직임 충동·움직이면 완화·근경직 없음)와 반드시 구분.','accent'),
 ]},
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 3축 근거','foot':'문헌고찰 종합',
  'headers':['치료','대표','야간경련 근거','위치'],'rows':[
   ['ESWT','종아리 표적 충격파','Li 2021(후향)+경직 RCT/MA','보조·근거형성 중'],
   ['주사','보툴리눔(비복근)','Park 2017·Restivo 2018 RCT','불응성 선택(Lv II)'],
   ['주사','유발점/dry needling','Kim 2015·Temel 2023','MTrP 동반 시'],
   ['주사','심비골신경 차단','Imura 2015 <b>직접근거</b>','선택적'],
   ['경구약제','quinine / 비타민 B·diltiazem','El-Tawil / Chan·Voon','효과O·독성 / Lv C'],
   ['비약물','취침 전 스트레칭','Hallegraeff 2012 RCT','<b>1차·최우선</b>'],
  ]},
 {'t':'split','eyebrow':'치료 · 체외충격파(ESWT)','tag':('근거형성중','amber'),'title':'종아리 표적 충격파 — 경련 직접 근거','foot':'Li 2021 (Biomed Res Int)',
  'items':[
   (0,'<b>Li 2021</b>(후향 n=126): 요추퇴행성 동반 하지경련. 2,000 shocks/session, 2일 간격 4주.',''),
   (0,'경직 인접근거는 RCT·메타분석으로 비교적 견고(Otero-Luis 2024 MAS −0.40).',''),
   (0,'특발성 NLC만 표적한 ESWT RCT는 아직 없음(직접 근거 공백).','red'),
  ],
  'aside':{'title':'Li 2021 결과 (ESWT군)','stat':[('5.7→1.3','경련 빈도 (회/시간)'),('57.6→10.6','지속 (초)'),('P<0.001','대조군 대비')]}},
 {'t':'bullets','eyebrow':'치료 · ESWT','tag':('기전',''),'title':'기전 · 프로토콜 · 한계','foot':'Yang 2021 (J Clin Med, 기전 리뷰)','items':[
   (0,'기전(Yang 2021): NO 합성↑, 신경근접합부 ACh수용체 변성(CMAP↓ 6–8주), 운동신경원 흥분성↓, 미세순환 개선.',''),
   (0,'프로토콜: 비복근·가자미근 운동점, radial 1.5–2.5 bar / focused ~0.10 mJ/mm², 2,000–3,000 pulses/근육, 주 1–2회 3–4주.',''),
   (0,'안전: 대체로 안전(일시적 국소통증). 상대 금기 — 항응고제·심부정맥혈전·감염·악성종양·임신.',''),
   (-1,'한계: 특발성 직접 RCT 부재, 효과 대개 12주 이내 단기 → 보조·실험적.','accent'),
 ]},
 {'t':'split','eyebrow':'치료 · 주사기법','tag':('효과 있음','green'),'title':'① 국소마취제 유발점주사','foot':'Kim 2015; Prateepavanich 1999',
  'items':[
   (0,'개념: 비복근 근막통증유발점(MTrP)에 소량 국소마취제 → 국소 근이완·유발점 비활성화·되먹임 차단.',''),
   (0,'결과(Kim 2015, n=12): NRS·경련 빈도·불면지수(ISI) 모두 유의 개선(P<0.01), 임상적 불면 10명→4주째 1명.','green'),
   (0,'Prateepavanich 1999(무작위 n=24): xylocaine 주사 vs quinine — 지속효과 면에서 주사군 우월.',''),
  ],
  'aside':{'title':'기법 (Kim 2015)','items':[
   (0,'약제: <b>0.25% lidocaine 1–2 mL</b>',''),(0,'바늘: <b>25 G</b>, 피부 <b>30°</b> 접근',''),
   (0,'표적: 비복근 유발점(최대 압통점)',''),(0,'빈도: 주 1회',''),
  ]}},
 {'t':'bullets','eyebrow':'치료 · 주사기법','tag':('효과 있음','green'),'title':'② 건침(Dry Needling)','foot':'Temel 2023; Bagcier 2021','items':[
   (0,'기법: 비복근 유발점에 약물 없이 자침, 국소연축반응 유도·소실 → taut band 이완, 압력통증역치 상승. 주 1회 약 3회기.',''),
   (0,'<b>Temel 2023 RCT(n=42):</b> 스트레칭+DN 병용군이 3개월 경련 횟수(P=0.016)·강도·압력통증역치·수면질(PSQI) 우월.','green'),
   (0,'Bagcier 2021 증례: 주1회 3회기 후 경련 지속 60초→10초, VAS 8→1, 빈도 매일→주간.',''),
   (-1,'저침습·저비용·무약물. 근거는 소규모 RCT·증례(Lv III~). 초음파 유도 권장.','accent'),
 ]},
 {'t':'split','eyebrow':'치료 · 주사기법 · 직접근거','tag':('직접 근거',''),'title':'③ 심비골신경 내측분지 차단','foot':'Imura 2015 (Brain Behav; PMID 26445706)',
  'items':[
   (0,'<b>Imura 2015:</b> 야간경련에 말초 운동신경가지를 직접 표적한, 현재 유일한 전향적 비교연구.',''),
   (0,'대상: 요추수술 후 지속 경련 66명(차단군 41 vs 대조 25), 평균 60.9세.',''),
   (0,'<b>기법:</b> 제1–2 중족골 사이 간극 원위 2/3 지점, 1.0% lidocaine 5.0 mL(무에피네프린)를 1.0–1.5 cm 깊이에 서서히 주입.',''),
  ],
  'aside':{'title':'결과 (2주 시점)','stat':[('61% vs 20%','빈도 1/4↓'),('80.5%','빈도 1/2↓ (P<0.01)'),('63.4%','12주+ 지속')]}},
 {'t':'bullets','eyebrow':'치료 · 주사기법','tag':('효과 있음','green'),'title':'④ 보툴리눔 + 안전성','foot':'Park 2017·Restivo 2018','items':[
   (0,'<b>Park 2017 RCT(n=50):</b> 요추관협착 동반 야간 종아리경련. 비복근 BTX-A vs gabapentin → 전 시점 통증·빈도·강도 유의 감소(P<0.01).','green'),
   (0,'Restivo 2018 RCT: 당뇨병성 신경병증 경련에서 위약 대비 개선(1주부터 16주 지속).',''),
   (0,'주사 계열 중 근거 최고(Lv II)이나 고가·반복·근력약화 우려 → 선택적.',''),
   (-1,'안전(고령): 경골신경→족저굴곡 약화, 총비골신경→족하수→낙상. 초음파 유도·혈관내 주입 회피.','red'),
 ]},
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'효과 좋은 경구 약제','foot':'AAN(Katzberg 2010); Cochrane 종합',
  'headers':['약제','근거','평가'],'rows':[
   ['Quinine','El-Tawil 2015 Cochrane','효과 O이나 FDA 미승인·혈소판감소/TTP → 최후'],
   ['비타민 B 복합','Chan 1998 RCT','빈도·강도 감소, <b>Lv C·안전</b> → 우선 시도'],
   ['Diltiazem 30mg','Voon 2001 교차','빈도 5.8→0.16/2주, Lv C'],
   ['Vitamin K2','Tan 2024(JAMA IM)','빈도 2.60→0.96 (⚠정정·교체 통지)'],
   ['마그네슘(특발성)','Garrison 2020 Cochrane','임상적 이득 없음 — <b>권고 안 함</b>'],
  ]},
 {'t':'bullets','eyebrow':'비약물','tag':('1차','green'),'title':'1차 비약물 치료 (참고)','foot':'Hallegraeff 2012; Allen & Kirby 2012','items':[
   (0,'<b>취침 전 스트레칭(Hallegraeff 2012 RCT):</b> 종아리·햄스트링 6주 → 경련 빈도(−1.2회/야간)·강도(−1.3 cm VAS) 감소.','green'),
   (0,'위험 거의 없고 무비용 → 모든 고령 NLC 환자의 1차.',''),
   (0,'급성 발작: 족배굴곡 수동 신장·걷기·마사지. 자세·수분·온열 교정.',''),
   (0,'원인 교정: 유발약물(LABA·이뇨제·statin) 검토, 이차 원인(협착·정맥부전·전해질) 교정.',''),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · NLC','headline':'감별과 원인교정이 먼저, 스트레칭이 1차','msgs':[
   ('병태생리','운동신경 과흥분 + Ia/Ib 반사 불균형. 단축된 근육에서 유발, 신전으로 완화.'),
   ('주된 호소','수면 중 통증성 경련·촉지 근경직·족배굴곡 완화·잔통. RLS와 감별.'),
   ('ESWT','경직 근거는 강하나 경련 직접근거는 약함 → 보조·근거형성 중.'),
   ('주사','BTX(RCT)·유발점/dry needling(MTrP)·심비골신경 차단(Imura)이 불응성에 선택적.'),
   ('경구약제','quinine 효과O·독성으로 회피, 비타민B/diltiazem 비교적 안전, 마그네슘 특발성 무효.'),
 ]},
 {'t':'refs','title':'참고문헌 — NLC','refs':[
   ('<b>Miller & Layzer.</b> Muscle cramps. Muscle Nerve. 2005.',PM(15902691)),
   ('<b>Minetto.</b> Mechanisms of cramp contractions. J Physiol. 2011.',PM(21969448)),
   ('<b>Khan & Burne.</b> Reflex inhibition of cramp by tendon stim. J Neurophysiol. 2007.',PM(17634341)),
   ('<b>Hallegraeff.</b> Stretching before sleep reduces NLC: RCT. J Physiother. 2012.',PM(22341378)),
   ('<b>Li.</b> ESWT reduces leg cramps in lumbar degenerative disorders. Biomed Res Int. 2021.',PM(34734084)),
   ('<b>Otero-Luis.</b> ESWT for spasticity: SR & MA. J Clin Med. 2024.',PM(38592705)),
   ('<b>Kim.</b> MTrP injections on nocturnal calf cramps. J Am Board Fam Med. 2015.',PM(25567819)),
   ('<b>Temel.</b> Dry needling on nocturnal calf cramps: RCT. Turk J Osteoporos. 2023.','https://doi.org/10.4274/tod.galenos.2023.54254'),
   ('<b>Imura.</b> Deep peroneal nerve medial branch block for NLC. Brain Behav. 2015.',PM(26445706)),
   ('<b>Park.</b> Botulinum toxin for nocturnal calf cramps in LSS: RCT. Arch Phys Med Rehabil. 2017.',PM(28209505)),
   ('<b>El-Tawil.</b> Quinine for muscle cramps. Cochrane. 2015.',PM(25842375)),
   ('<b>Garrison.</b> Magnesium for skeletal muscle cramps. Cochrane. 2020.',PM(32956536)),
   ('<b>Chan.</b> Vitamin B complex for NLC: RCT. J Clin Pharmacol. 1998.',PM(11301568)),
   ('<b>Voon & Sheu.</b> Diltiazem for nocturnal leg cramps. Age Ageing. 2001.',PM(11322688)),
 ]},
]

# ==================================================== RLS
RLS = [
 {'t':'title','eyebrow':'Restless Legs Syndrome · 문헌고찰','title':'하지불안증후군',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사 · 경구약제','series':SERIES},
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'뇌 철분 결핍이 핵심','foot':'IRLSSG; AASM 2025 지침 방향','items':[
   (0,'<b>뇌 철분 결핍:</b> 혈청 철분이 정상이어도 흑질·기저핵 등 뇌 국소 철분이 부족 → 도파민 신호 이상.',''),
   (0,'도파민 이상: 야간 도파민 기능 저하 가설. 도파민제 단기 효과, 장기 사용 시 <b>augmentation</b> 유발.',''),
   (0,'아데노신 저하 가설(최근): 뇌 철분 결핍이 아데노신 신호를 낮춰 과흥분 → dipyridamole의 근거.',''),
   (0,'유전(가족력 흔함)·이차 요인(철결핍·임신·말기신부전·특정 약물).',''),
   (-1,'→ 치료 기반은 철분 교정, 약물 축은 도파민에서 α2δ 리간드로 이동.','accent'),
 ]},
 {'t':'bullets','eyebrow':'임상 양상 · 진단','tag':('진단',''),'title':'주된 호소 — IRLSSG 2014 필수 5기준','foot':'Allen 2014 (Sleep Med, IRLSSG)','items':[
   (0,'① 다리를 <b>움직이고 싶은 충동</b>(대개 불쾌한 다리 감각 동반).',''),
   (0,'② 안정·비활동 시 시작·악화. ③ 움직임(걷기·스트레칭)으로 부분적·일시적 완화.',''),
   (0,'④ 저녁·밤에 악화되는 뚜렷한 일주기(circadian). ⑤ 다른 질환(다리경련 등)으로 더 잘 설명되지 않음.',''),
   (0,'통증보다 이상감각이 주, <b>촉지되는 근경직 없음</b>. PLMS 동반. 유병률 5~10%.',''),
   (-1,'감별: NLC(통증성 근수축·근경직·족배굴곡 완화)와 구분.','accent'),
 ]},
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 3축 근거','foot':'AASM 2025 지침 종합',
  'headers':['치료','대표','RLS 근거','위치'],'rows':[
   ['ESWT','체외충격파','RLS 표적 연구 없음','<b>권고 불가</b>(비골신경자극 대안)'],
   ['주사','IV 철분(FCM)','Earley 2024 RCT·메타분석','철결핍 시 강한 권고'],
   ['주사','보툴리눔 / 정맥경화','Mittal 2018 / Pyne 2023','연구단계 / 정맥질환 동반'],
   ['경구약제','α2δ 리간드','Allen 2014 등 RCT','<b>1차(강한 권고)</b>'],
   ['경구약제','도파민 작용제','Winkelman 2006','augmentation로 후순위'],
   ['경구약제','dipyridamole','Garcia-Borreguero 2021','조건부(신규)'],
  ]},
 {'t':'split','eyebrow':'치료 · 체외충격파(ESWT)','tag':('근거 없음','red'),'title':'ESWT — RLS 직접 근거 없음','foot':'Charlesworth 2023; AASM 2025',
  'items':[
   (0,'RLS를 결과변수로 ESWT를 평가한 RCT·전향연구·증례는 검색되지 않음(<b>직접 근거 없음</b>).','red'),
   (0,'ESWT의 확립된 근거는 근골격계 통증·경직 영역으로 RLS(뇌 철분·도파민·아데노신)와 병태가 다르다.',''),
   (0,'근거를 창작하지 않는다 → RLS에 ESWT는 권고할 수 없다.',''),
  ],
  'aside':{'title':'근거 있는 대안','dark':True,'items':[
   (0,'<b>비골신경 자극(TOMAC)</b> — 근거 있는 비약물 대안.',''),
   (0,'Charlesworth 2023: sham 대조 증상 개선·수면 무방해.',''),
   (0,'AASM 2025 조건부 권고.',''),
  ]}},
 {'t':'split','eyebrow':'치료 · 주사','tag':('효과 있음','green'),'title':'① 정맥 철분 — 근거 최강','foot':'Earley 2024 (Sleep); IRLSSG iron 2018',
  'items':[
   (0,'뇌 철분 결핍을 직접 교정하는, RLS 주사 치료 중 근거 최강.',''),
   (0,'<b>Earley 2024(Sleep) 다기관 RCT(n=209):</b> FCM 750 mg(0·5일) vs 위약 → 42일 IRLS·CGI 유의 개선.','green'),
   (0,'메타분석 2024(537명)도 효과·안전성 확인. AASM 2025 강한 권고.',''),
  ],
  'aside':{'title':'용량 · 적응','items':[
   (0,'<b>FCM 1000 mg 단회</b>(또는 750 mg×2)',''),(0,'1시간 이내 점적',''),
   (0,'적응: ferritin ≤100 또는 경구 부적절',''),(0,'경구는 ferritin ≥75에서 흡수 미미',''),
  ]}},
 {'t':'bullets','eyebrow':'치료 · 주사','tag':('제한적','amber'),'title':'② 보툴리눔 · 정맥 경화요법','foot':'Mittal 2018; Pyne 2023; Sundaresan 2019','items':[
   (0,'<b>보툴리눔(Mittal 2018 이중맹검 교차 n=24):</b> incoA 100U를 전경골근·비복근·대퇴이두근에 주사 → 4·6주 IRLS·통증(VAS) 유의 개선.',''),
   (1,'SR/MA(Healthcare 2021): RCT 2편 27명 IRLS SMD −0.819. 표본 매우 작아 확정 불가 → 표준치료 아님.','muted'),
   (0,'정맥 경화요법(정맥류/CVI 동반): Pyne 2023·Sundaresan 2019 → 하지정맥 치료 후 IRLS 19.83→7.89(약 63%↓).',''),
   (-1,'두 방법 모두 특정 표현형·연구단계. 특발성 RLS 전반의 표준치료는 아님.','accent'),
 ]},
 {'t':'split','eyebrow':'치료 · 경구약제','tag':('1차','green'),'title':'③ α2δ 리간드 — 1차','foot':'Allen 2014 (NEJM); AASM 2025',
  'items':[
   (0,'gabapentin enacarbil·gabapentin·pregabalin. AASM 2025 <b>1차 강한 권고</b>.',''),
   (0,'<b>Allen 2014(NEJM) 52주 RCT:</b> pregabalin 300 mg 효과적, augmentation 1.7% vs pramipexole 9.0%.','green'),
   (0,'Gabapentin enacarbil은 PSG상 각성·PLM 감소(Winkelman 2011). 부작용: 어지럼·졸림·부종.',''),
  ],
  'aside':{'title':'왜 1차인가','items':[
   (0,'도파민제보다 <b>augmentation이 유의하게 적음</b>.',''),
   (0,'수면·감각증상 함께 개선.',''),(0,'철분 교정과 병행이 기반.',''),
  ]}},
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'④ 도파민제 · 신규 · 요약','foot':'AASM 2025 (J Clin Sleep Med)',
  'headers':['약물군','위치 · 근거'],'rows':[
   ['도파민 작용제 (pramipexole 등)','단기 효능O(Winkelman 2006) — <b>augmentation(연 7~10%)</b>로 장기 권고 안 함(AASM against)'],
   ['Dipyridamole','Garcia-Borreguero 2021 교차 RCT: IRLS 24.1→11.1(위약 18.7). 아데노신 가설, 조건부'],
   ['오피오이드 (서방형 oxycodone·부프레노르핀)','난치성·augmentation에 조건부. 진정·호흡 위험 신중'],
   ['철분(경구)','ferritin ≤75에서 기반 치료. 흡수 부족 시 정맥 전환'],
  ]},
 {'t':'key','eyebrow':'핵심 메시지 · RLS','headline':'철분 교정이 기반, α2δ 리간드가 1차','msgs':[
   ('병태생리','뇌 국소 철분 결핍 → 도파민·아데노신 신호 이상.'),
   ('주된 호소','움직임 충동·안정 시 악화·움직이면 완화·저녁 악화(IRLSSG 5기준). NLC와 감별.'),
   ('주사','IV 철분(FCM)이 근거 최강. 보툴리눔은 연구단계, 정맥경화는 정맥질환 동반 시.'),
   ('ESWT','RLS 직접근거 없음 → 비약물은 비골신경 자극(근거 있음).'),
   ('경구약제','α2δ 리간드 1차. 도파민제는 augmentation로 후순위. dipyridamole 조건부.'),
 ]},
 {'t':'refs','title':'참고문헌 — RLS','refs':[
   ('<b>Allen.</b> IRLSSG diagnostic criteria (updated). Sleep Med. 2014.',PM(25023924)),
   ('<b>Winkelman.</b> RLS/PLMD treatment: AASM guideline. J Clin Sleep Med. 2025.',PM(39324694)),
   ('<b>Allen.</b> IRLSSG task force: iron treatment of RLS. Sleep Med. 2018.',PM(29425576)),
   ('<b>Earley.</b> IV ferric carboxymaltose for RLS: multicenter RCT. Sleep. 2024.',PM(38625730)),
   ('<b>Mittal.</b> Botulinum toxin in RLS: crossover RCT. Toxins. 2018.',PMC('PMC6215171')),
   ('Botulinum toxin A in RLS: SR & MA. Healthcare. 2021.',PMC('PMC8623507')),
   ('<b>Pyne.</b> Varicose veins with RLS & NLC. J Vasc Interv Radiol. 2023.',PM(36526075)),
   ('<b>Charlesworth.</b> Peroneal nerve stimulation for RLS. J Clin Sleep Med. 2023.',PM(36856064)),
   ('<b>Allen.</b> Pregabalin vs pramipexole for RLS. N Engl J Med. 2014.',PM(24521108)),
   ('<b>Winkelman.</b> Pramipexole in RLS. Neurology. 2006.',PM(16931507)),
   ('<b>Winkelman.</b> Gabapentin enacarbil PSG study in RLS. Mov Disord. 2011.',PM(21611981)),
   ('<b>Garcia-Borreguero.</b> Dipyridamole for RLS: crossover RCT. Mov Disord. 2021.',PM(34137476)),
 ]},
]

# ==================================================== LSB
LSB = [
 {'t':'title','eyebrow':'Lumbar Sympathetic Block · 문헌고찰','title':'요추교감신경차단',
  'sub':'방법 · 적응증 · 효과','order':'Technique · Indications · Efficacy','series':SERIES},
 {'t':'bullets','eyebrow':'개요','tag':('배경',''),'title':'개요 · 해부 · 원리','foot':'StatPearls NBK431107; Zhang 2022 (Ibrain)','items':[
   (0,'LSB와 교감신경 신경파괴(sympatholysis)는 70년 이상 다양한 하지 통증·허혈 질환에 사용.',''),
   (0,'표적: 신경절 밀도가 가장 높은 <b>L2–L3</b>(척추체 전외측). 일부 L2/L3/L4 다분절.',''),
   (0,'원리 ①: 교감신경 차단 → 혈관 확장·측부순환 증가 → 조직 산소화 개선.',''),
   (0,'원리 ②: 교감신경 매개 통증(sympathetically-maintained pain) 경로·자율신경 동반 구심로 차단.',''),
   (-1,'국소마취제 차단(진단적/치료적)과 화학적/열적 신경파괴로 나뉜다.','accent'),
 ]},
 {'t':'split','eyebrow':'방법','tag':('기법',''),'title':'방법 (Technique)','foot':'StatPearls NBK431107 · NBK560514',
  'items':[
   (0,'<b>표준: 방척추(paravertebral) 접근 + 투시(fluoroscopy).</b> CT·초음파도 가능.',''),
   (0,"바늘 진입: 정중선에서 약 7 cm 외측. 척추체 접촉 후 전내측으로 'walk'하여 척추체 전외측으로 진입.",''),
   (0,'흡인 후 조영제 주입 → 두미측(craniocaudal) 종방향 확산 확인.',''),
   (0,'<b>성공 지표: 동측 하지 피부온도 ≥2°C 상승.</b>',''),
  ],
  'aside':{'title':'약제','items':[
   (0,'진단/치료: lidocaine 1%,',''),(0,'bupivacaine 0.25–0.5%, ropivacaine',''),
   (0,'신경파괴: 무수알코올/phenol, RFA',''),(-1,'신경파괴는 진단적 차단 양성 시에만','accent'),
  ]}},
 {'t':'table','eyebrow':'적응증','tag':('적응',''),'title':'적응증 (Indications)','foot':'StatPearls; 문헌고찰 종합',
  'note':"특발성 야간 하지경련(NLC)은 적응증 아님 — '밤 다리증상'이 허혈성 안정통(PAD/CLI)이면 적응. 원인 감별(ABI·도플러) 선행.",
  'headers':['범주','대표 적응증'],'rows':[
   ['통증증후군','하지 복합부위통증증후군(CRPS I/II) — <b>조기(≤12개월) 시행 유리</b>'],
   ['허혈질환','PAD·중증 하지허혈(CLI) 안정통·비재건성, 버거병, 색전, 동상, 혈관연축'],
   ['신경병증','당뇨병성 신경병증/당뇨발, 대상포진후신경통, 환상지통·단단통'],
   ['기타','족부 다한증, 레이노 증후군(하지)·홍색사지통증, 암성 골반/하지통'],
  ]},
 {'t':'split','eyebrow':'효과','tag':('효과','green'),'title':'효과 ① 관류 개선 · 허혈성 통증','foot':'Dickey 2024 (Cureus); Medicina 2024; Barreto 2018',
  'items':[
   (0,'<b>관류 실측(Dickey 2024):</b> LSB 후 후경골동맥 직경 0.17→0.27 cm(+58.8%), 모세혈관 재충혈 3.92→1.30초, 족부온도 +2.8°C.',''),
   (0,'허혈성 통증(PAD): 하지 통증 최대 <b>75%↓</b>, Fontaine 분류·측부관류 개선(Medicina 2024).','green'),
   (0,'비재건성 CLI: 교감신경 신경파괴가 절단 외 대안이 없는 환자의 통증조절에 효과적·안전(Barreto 2018).',''),
  ],
  'aside':{'title':'실측 수치 (Dickey 2024)','stat':[('+58.8%','후경골동맥 직경'),('+2.8°C','족부온도'),('3.92→1.30s','모세혈관 재충혈')]}},
 {'t':'bullets','eyebrow':'효과','tag':('효과','green'),'title':'효과 ② CRPS · 기전','foot':'Choi 2024 (Sci Rep); Pain Ther 2023','items':[
   (0,'CRPS는 교감신경 매개 통증의 전형 → LSB 후 유의한 통증완화. 최적 환자 선택·조기 시행이 성공률↑.',''),
   (0,'Choi 2024(Sci Rep): 교감신경 신경파괴의 효과 지속기간을 전향 관찰로 제시.',''),
   (0,'반응 예측: <b>교감신경 피부반응(SSR)</b>이 LSB 반응 예측에 유용(Pain Ther 2023).',''),
   (0,'한계: 중추 감작이 진행되면 시간이 지날수록 효과 감소 가능.','muted'),
   (-1,'기전: 교감차단 → 측부순환 혈관확장 → 조직 산소화↑ → 통증↓ + 교감매개통 차단 + 신경파괴 직접효과.','accent'),
 ]},
 {'t':'bullets','eyebrow':'안전성 · 결론','tag':('안전성','red'),'title':'합병증 · 근거수준 · 결론','foot':'StatPearls; 문헌고찰 종합','items':[
   (0,'합병증: <b>생식대퇴신경통(신경파괴 시 5–10%)</b>, 외측대퇴피신경 손상, 기립성 저혈압.','red'),
   (0,'혈관·요관·신장 등 내장 구조 천공, 출혈, 신경축 확산, 신경파괴 후 통증성 신경염(dysesthesia).',''),
   (0,'근거수준: 대부분 관찰·증례군·소규모 전향연구, 대규모 RCT는 부족(허혈질환·CRPS Lv III~IV).',''),
   (-1,'그럼에도 조기 CRPS·재건 불가능한 중증 하지허혈(안정통)에서 임상적으로 유용.','accent'),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · LSB','headline':'표준은 투시 유도 방척추 접근, 성공은 온도 ≥2°C','msgs':[
   ('방법','L2–L3 방척추 접근·투시, 정중선 7 cm 외측, 조영제 두미측 확산, 성공지표 온도 ≥2°C.'),
   ('약제','진단/치료는 국소마취제, 신경파괴는 무수알코올/phenol·RFA — 진단차단 양성 시에만.'),
   ('적응증','조기 CRPS·PAD/CLI 안정통·신경병증·다한증 등. 특발성 NLC는 적응 아님.'),
   ('효과','관류 실측 개선(Dickey), 허혈통 최대 75%↓, CRPS 통증완화(SSR로 예측).'),
   ('근거','대규모 RCT 부족(관찰·증례 중심). 조기 CRPS·비재건성 CLI에서 유용.'),
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
 ]},
]

DECKS = [("NLC_발표_웹","야간 하지경련 · 문헌고찰 발표",NLC),
         ("RLS_발표_웹","하지불안증후군 · 문헌고찰 발표",RLS),
         ("LSB_발표_웹","요추교감신경차단 · 문헌고찰 발표",LSB)]

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"
raw = {}
for fname,title,slides in DECKS:
    raw[fname] = (title, render_deck(title, slides))

# ---- collect all glyphs, subset 4 weights once ----
allhtml = "".join(h for _,h in raw.values())
vis = re.sub(r'<style.*?</style>','',allhtml,flags=re.S)
vis = re.sub(r'<script.*?</script>','',vis,flags=re.S)
vis = re.sub(r'<[^>]+>',' ',vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@")
text=''.join(sorted(chars)); print("glyphs:",len(chars))

UP="/root/.claude/uploads/bb19d1cb-d1ba-542e-8235-38fcac774773/"
FONTS={"__F900__":UP+"c71b728f-PretendardBlack.otf","__F800__":UP+"3a19e05c-PretendardExtraBold.otf",
       "__F700__":UP+"1121d3ff-PretendardBold.otf","__F300__":UP+"82c21b19-PretendardLight.otf"}
uris={}
for ph,path in FONTS.items():
    o=Options(); o.flavor='woff2'; o.desubroutinize=True; o.name_IDs=[]; o.name_legacy=False; o.name_languages=[]
    f=TTFont(path); s=Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf=io.BytesIO(); f.save(buf); uris[ph]="data:font/woff2;base64,"+base64.b64encode(buf.getvalue()).decode()
    print(ph,f"{len(buf.getvalue())/1024:.0f}KB")

for fname,(title,htmlc) in raw.items():
    for ph,uri in uris.items(): htmlc=htmlc.replace(ph,uri)
    out=os.path.join(BASE,fname+".html"); open(out,'w',encoding='utf-8').write(htmlc)
    print(fname, f"{len(htmlc.encode())/1024:.0f}KB")
print("done")
