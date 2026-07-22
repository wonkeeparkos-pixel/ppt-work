# -*- coding: utf-8 -*-
"""PN(말초신경병증)·CVI(만성정맥부전) 웹 슬라이드 덱 빌드 — 기존 house 렌더러(deck_html) 재사용."""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
def PMC(x): return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x}/"

# ========================================================= 병태생리 그림 (SVG)
# PN — stocking-glove 분포 + 소/대섬유
FIG_STOCKING = '''
<div class="figpanel warn"><div class="pt">길이의존성 · 양말형</div>
<svg viewBox="0 0 220 250" role="img" aria-label="발끝부터 상행하는 양말형 감각이상">
 <path d="M96 20 h28 v150 q0 22 -14 22 q-16 0 -16 -24 Z" fill="#EDE3E0" stroke="#D9BDB6" stroke-width="1.5"/>
 <path d="M96 118 h28 v52 q0 22 -14 22 q-16 0 -16 -24 Z" fill="#D64A3A" opacity=".85"/>
 <path d="M92 190 q-6 22 22 22 q34 0 40 -6 q4 -18 -10 -22 Z" fill="#B23A2C"/>
 <text x="150" y="150" font-size="13" font-weight="800" fill="#A8352A">발끝→상행</text>
 <text class="a-spark" x="150" y="205" font-size="17" fill="#E8A33D">✳</text>
 <text x="110" y="240" text-anchor="middle" font-size="12.5" font-weight="700" fill="#55615B">저림·화끈거림</text>
</svg>
<div class="pl">가장 <b>긴 축삭</b>부터 침범 → <b>발끝→정강이</b> 상행(양말형)</div></div>
<div class="figpanel good"><div class="pt">소섬유 vs 대섬유</div>
<svg viewBox="0 0 220 250" role="img" aria-label="소섬유 대섬유 침범 양상">
 <rect x="20" y="30" width="180" height="88" rx="12" fill="#FCF4F2" stroke="#E7CFC9" stroke-width="1.5"/>
 <text x="110" y="52" text-anchor="middle" font-size="13.5" font-weight="800" fill="#A8352A">소섬유(Aδ·C)</text>
 <text x="110" y="76" text-anchor="middle" font-size="12" font-weight="700" fill="#55615B">통각·온도 — 화끈거림·이질통</text>
 <text x="110" y="99" text-anchor="middle" font-size="11.5" font-weight="700" fill="#8A6D2F">NCS 정상일 수 있음</text>
 <rect x="20" y="132" width="180" height="88" rx="12" fill="#EFF6F0" stroke="#CFE3D2" stroke-width="1.5"/>
 <text x="110" y="154" text-anchor="middle" font-size="13.5" font-weight="800" fill="#2E7D32">대섬유(Aβ)</text>
 <text x="110" y="178" text-anchor="middle" font-size="12" font-weight="700" fill="#55615B">진동·고유감각 — 저림·균형장애</text>
 <text x="110" y="201" text-anchor="middle" font-size="11.5" font-weight="700" fill="#55615B">반사 소실 · NCS 이상</text>
</svg>
<div class="pl"><b>소섬유 먼저</b>(화끈거림) → NCS 정상 ≠ 배제</div></div>
'''

# CVI — 판막부전→역류→정맥고혈압
FIG_VALVE = '''
<div class="figpanel good"><div class="pt">정상 판막</div>
<svg viewBox="0 0 200 250" role="img" aria-label="정상 정맥 판막 일방향">
 <rect x="78" y="16" width="44" height="218" rx="14" fill="#EAF1EE" stroke="#C4DDCA" stroke-width="1.5"/>
 <path d="M78 92 L100 112 L122 92" fill="none" stroke="#2E7D32" stroke-width="3"/>
 <path d="M78 150 L100 170 L122 150" fill="none" stroke="#2E7D32" stroke-width="3"/>
 <path class="a-flow" d="M100 224 L100 30" stroke="#2E7D32" stroke-width="3" fill="none"/>
 <path d="M94 40 L100 26 L106 40 Z" fill="#2E7D32"/>
 <text x="150" y="130" font-size="12.5" font-weight="800" fill="#2E7D32">위로만</text>
</svg>
<div class="pl">판막이 <b>일방향</b> 유지 → 심장쪽으로만 환류</div></div>
<div class="figpanel warn"><div class="pt">판막 부전 · 역류</div>
<svg viewBox="0 0 200 250" role="img" aria-label="판막 부전 역류 정맥고혈압">
 <rect x="70" y="16" width="60" height="218" rx="16" fill="#EFE3E0" stroke="#D9BDB6" stroke-width="2"/>
 <path d="M70 92 L100 104 L130 92" fill="none" stroke="#C6B0AB" stroke-width="3" stroke-dasharray="4 4"/>
 <path d="M70 150 L100 162 L130 150" fill="none" stroke="#C6B0AB" stroke-width="3" stroke-dasharray="4 4"/>
 <path class="a-flow" d="M100 30 L100 224" stroke="#D64A3A" stroke-width="3.5" fill="none"/>
 <path d="M94 214 L100 228 L106 214 Z" fill="#D64A3A"/>
 <g class="a-cramp"><ellipse cx="100" cy="210" rx="30" ry="16" fill="#D64A3A" opacity=".28"/></g>
 <text x="150" y="205" font-size="12.5" font-weight="800" fill="#A8352A">역류·울혈</text>
 <text class="a-spark" x="150" y="120" font-size="16" fill="#E8A33D">✳</text>
</svg>
<div class="pl"><b>판막 부전</b> → 아래로 역류 → <b>정맥고혈압</b>·부종</div></div>
'''

# ========================================================= 04 PN
PN = [
 {'t':'title','eyebrow':'Peripheral Neuropathy · 문헌고찰','title':'말초신경병증',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료 (당뇨병성 DPN 중심)','order':'ESWT · 주사·중재 · 경구약제','series':SERIES},
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'왜 신경이 상하나 — 고혈당의 4갈래 손상','foot':'Feldman 2019; Cameron 2001','items':[
   (0,'고혈당은 <b>4개 경로(폴리올·AGE·PKC·hexosamine)</b>로 갈라져 결국 <b>활성산소(ROS)·미토콘드리아 손상</b>으로 수렴한다.',''),
   (0,'여기에 <b>vasa nervorum(신경 미세혈관) 허혈</b>이 겹쳐 신경내막 저산소증 — 순수 대사병이 아니라 대사-혈관 복합.',''),
   (0,'<b>DCCT(RCT n=1,441):</b> 강화혈당조절이 임상 신경병증을 <b>60% 감소</b>(95% CI 38~74) → 혈당이 인과적 상류.',''),
   (-1,'→ 원인(당뇨·항암제·알코올·B12·요독·갑상선)은 달라도 하류 기전이 겹친다.','accent'),
 ]},
 {'t':'figure','eyebrow':'병태생리 · 쉽게 보기','tag':('그림 설명','ink'),'title':'왜 발끝부터 저리고, NCS가 정상일 수 있나','foot':'Tesfaye 2010; Feldman 2019','svg':FIG_STOCKING,
  'caption':"가장 <b>긴 신경(발끝)</b>부터 상해 <b>양말형</b>으로 번져요. <b>소섬유</b>(화끈거림·이질통)가 먼저 상하는데, 이때 <b>신경전도검사(NCS)는 정상</b>일 수 있어 '정상=신경병증 아님'이 아닙니다."},
 {'t':'split','eyebrow':'병태생리 · 통증','tag':('기전',''),'title':'저림·화끈거림은 어떻게 통증이 되나','foot':'Baron 2010; Woolf 2011',
  'items':[
   (0,'<b>말초감작:</b> 손상 신경의 Na⁺채널(Naᵥ1.7/1.8) 과발현 → <b>이소성 자발발화</b> → 자발통·전기충격 통증.',''),
   (0,'<b>중추감작:</b> 척수후각 NMDA·Ca²⁺ 과흥분 → 무해한 촉각(Aβ)이 통증회로로 재배선 → <b>이질통</b>("이불도 아파").',''),
   (0,'야간 악화는 다인성 가설(주의분산↓·피부온·일주기) — 단일 확립 기전 없음.','muted'),
  ],
  'aside':{'title':'양성 vs 음성 증상','items':[
   (0,'<b>양성:</b> 화끈거림·이질통·자발통',''),(0,'<b>음성:</b> 저림·무감각·감각저하',''),
   (0,'둘이 공존 = 신경병증 특징',''),(-1,'양성 우세 = 통증성 DPN','accent'),
  ]}},
 {'t':'bullets','eyebrow':'임상 양상','tag':('호소',''),'title':'환자들의 주된 호소 · 선별','foot':'ADA/Pop-Busui 2022; Bouhassira 2005','items':[
   (0,'좌우대칭 <b>양말형 저림·화끈거림·감각이상·이질통</b>, 밤·안정 시 악화, 움직여도 안 풀림.',''),
   (0,'진행 시 <b>무감각발</b> → 통증 소실이 호전이 아니라 악화 신호. 당뇨발궤양 평생 위험 약 <b>19~34%</b>.','red'),
   (0,'선별: <b>10g 모노필라멘트(LOPS)</b> + 128Hz 진동각·발목반사·핀찌름 병용(단독 아님), <b>DN4 ≥4/10</b>(민감도 83%).',''),
   (-1,'선별 시점: T2DM 진단 시점부터, T1DM 진단 5년 후 매년.','accent'),
 ]},
 {'t':'split','eyebrow':'임상 양상 · 감별','tag':('감별','ink'),'title':'밤 다리 증상 — 4가지 감별','foot':'감별 콜아웃 · 시리즈 공통',
  'items':[
   (0,'<b>vs NLC:</b> NLC는 촉지되는 통증성 근수축·족배굴곡 완화. PN은 근경직 없이 감각소실.',''),
   (0,'<b>vs RLS:</b> RLS는 움직임 충동·보행 완화. PN은 움직여도 안 풀리고 접촉으로 악화.',''),
   (0,'<b>vs CVI:</b> CVI는 부종·무거움·거상 완화. PN은 거상 무관·감각소실.',''),
   (0,'<b>vs PAD:</b> 허혈 안정통·ABI<0.9. 당뇨는 동맥석회화로 ABI 위양성↑ → <b>TBI 병용</b>.','red'),
  ],
  'aside':{'title':'층화 감별','dark':True,'items':[
   (0,'① 신경 — 모노필라멘트·진동각',''),(0,'② 동맥 — ABI/TBI·맥박',''),
   (0,'③ 정맥 — 정맥진찰·거상반응',''),(0,'④ 완화동작 — 스트레칭/움직임/거상',''),
  ]}},
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 3축 근거','foot':'문헌고찰 종합',
  'headers':['치료','대표','DPN 근거','위치'],'rows':[
   ['ESWT','당뇨발궤양(DFU)','Hitchman 2019 SR/MA·dermaPACE','창상치유 보조 <b>(증상 직접근거 없음)</b>'],
   ['주사·중재','척수자극(10 kHz)','SENZA-PDN·de Vos·Slangen RCT','<b>불응성 선택지(근거 최강)</b>'],
   ['주사·중재','보툴리눔 피내','Yuan 2009·Ghasemi 2014','연구단계'],
   ['경구약제','gabapentinoid·SNRI·TCA','AAN 2022·NeuPSIG·OPTION-DM','<b>통증치료 근거 중심(1차)</b>'],
   ['경구(국소)','capsaicin 8%·lidocaine','STEP 2017','전신 불내성 2차'],
   ['원인·비약물','혈당·B12·발관리','DCCT·ASCO 2020·IWGDF','<b>1차·최우선</b>'],
  ]},
 {'t':'split','eyebrow':'치료 · 체외충격파(ESWT)','tag':('근거 비대칭','amber'),'title':'ESWT — 두 갈래를 분리하라','foot':'Cooper/Hitchman 2019; 신경전도 MA 2024',
  'items':[
   (0,'<b>당뇨발궤양(DFU) 창상 치유:</b> 반복 RCT·메타분석 존재 — Hitchman 2019 완전치유 <b>OR 2.66</b>(단 비뚤림 높음), dermaPACE FDA 허가.','green'),
   (0,'<b>DPN 증상·신경전도 개선:</b> 양질의 사람 RCT <b>사실상 부재</b> — 근거를 창작하지 않는다.','red'),
   (0,'ESWT-신경전도 MA는 수근관 등 포착성 대상이라 DPN 외삽 불가. 오인 인용되는 진동감각 RCT는 전신진동(WBV).','muted'),
  ],
  'aside':{'title':'DFU 창상 치유 (Hitchman 2019)','stat':[('OR 2.66','완전 치유(vs 표준)'),('64.5→81일','치유 시간 단축'),('FDA','dermaPACE 허가')]}},
 {'t':'split','eyebrow':'치료 · 주사·중재 · 직접근거','tag':('근거 최강','green'),'title':'① 척수자극(SCS) — 10 kHz SENZA-PDN','foot':'Petersen 2021 (JAMA Neurol); de Vos 2014; Slangen 2014',
  'items':[
   (0,'<b>SENZA-PDN(Petersen 2021, RCT n=216):</b> 10 kHz SCS+CMM vs CMM → 6개월 치료반응 <b>약 79% vs 5%(P<0.001)</b>, paresthesia-free, 24개월 지속.','green'),
   (0,'저주파 SCS도 2개 RCT(de Vos 2014 VAS 73→31; Slangen 2014 치료성공 59% vs 7%).',''),
   (0,'2021·2023 FDA 승인. <b>단 open-label 대조</b> → "불응성 중증 통증성 DPN의 선택지"까지가 정확.','muted'),
   (-1,'주의: AAN 2022 지침은 경구·국소 약물에 한정 — SCS를 권고·언급하지 않음(별도 합의문).','red'),
  ],
  'aside':{'title':'SENZA-PDN','stat':[('79% vs 5%','6개월 치료반응'),('P<0.001','vs 약물단독'),('24개월','효과 지속')]}},
 {'t':'bullets','eyebrow':'치료 · 주사·중재','tag':('연구단계','amber'),'title':'② 보툴리눔 피내 · 신경주위','foot':'Yuan 2009; Ghasemi 2014; Lakhan 2015','items':[
   (0,'<b>Yuan 2009(교차 RCT n=18):</b> 발등 피내 격자주사 → 12주 VAS <b>−2.53</b>(P<0.05), 반응 44%·위약 0.',''),
   (0,'Ghasemi 2014(n=40)·Salehi 2019(n≈40)도 통증·수면 개선. 메타분석(Lakhan 2015)은 <b>단 2개 RCT</b> 통합.','muted'),
   (0,'효과는 단기(수 주~개월)·재주사 필요 → "치료 옵션"이 아니라 <b>연구단계</b>.','amber'),
   (-1,'미만성 DPN에 대한 신경주위 주사·신경수분박리(hydrodissection)는 직접 근거 없음.','red'),
 ]},
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('1차·근거중심','green'),'title':'③ 경구약제 — 계열별 NNT','foot':'Finnerup 2015 (NeuPSIG); AAN 2022 (Price)',
  'note':"AAN 2022: 4계열(TCA·SNRI·gabapentinoid·Na채널차단제) 효과 <b>서로 유사</b> → 동반질환으로 개별화. FDA 승인은 pregabalin·duloxetine·tapentadol ER·capsaicin 8%뿐(gabapentin·amitriptyline은 오프라벨).",
  'headers':['계열','대표약','통합 NNT','권고'],'rows':[
   ['TCA','amitriptyline','<b>3.6</b>','1차(고령 제약)'],
   ['SNRI','duloxetine','6.4','1차'],
   ['Gabapentin','gabapentin','6.3','1차'],
   ['Pregabalin','pregabalin','7.7','1차'],
   ['국소','capsaicin 8% 패치','10.6','2차'],
  ]},
 {'t':'split','eyebrow':'치료 · 경구약제','tag':('head-to-head','green'),'title':'단독 동등, 실패 시 병합 — OPTION-DM','foot':'Tesfaye 2022 (Lancet); COMBO-DN 2013',
  'items':[
   (0,'<b>OPTION-DM(교차 RCT n=140):</b> A-P·P-A·D-P 3경로 각 16주 → NRS <b>6.6→약 3.3</b>, <b>경로 간 차이 없음</b>(D-P vs A-P −0.1).','green'),
   (0,'즉 <b>어느 1차 단독으로 시작하든 효과 동등</b> → 동반질환으로 선택.',''),
   (0,'단독 불충분 시 <b>두 계열 병합이 우수</b>(추가 −1.0점; COMBO-DN도 병용 이점).',''),
   (-1,'α-리포산(ALA): SYDNEY 2 단기 양성이나 NATHAN 1 1차종결점 음성 → 통증 1차 대체 아님.','muted'),
  ],
  'aside':{'title':'동반질환 맞춤','items':[
   (0,'신부전 → gabapentinoid 감량',''),(0,'심질환·고령 → gabapentinoid/duloxetine',''),
   (0,'우울·불면 → TCA/duloxetine',''),(-1,'오피오이드 지양(AAN·ADA)','red'),
  ]}},
 {'t':'bullets','eyebrow':'원인 교정 · 비약물','tag':('1차','green'),'title':'원인 교정이 진짜 1차','foot':'Callaghan 2012 Cochrane; ASCO 2020; IWGDF 2023','items':[
   (0,'<b>혈당(1형 강함/2형 약함):</b> DCCT/EDIC 1형 확립 vs 2형은 임상 신경병증 감소 미도달·저혈당↑(ACCORD) → 2형은 다요인 교정.',''),
   (0,'<b>가역 원인 배제:</b> B12(특히 metformin 장기복용 — ADA 주기 측정)·금주+티아민·갑상선. CIPN은 예방약 없음 → 용량조절(ASCO 2020).',''),
   (0,'<b>발 관리(IWGDF 2023):</b> 위험 계층화·자가검진·맞춤 신발·offloading — 궤양은 압력점(중족골두·족저). 절단 예방 표준.','green'),
   (0,'운동(Kluding 2012): 통증·MNSI 개선 + 표피내신경섬유 분지 증가(신경 재생 시사, 예비연구). 감각 소실 발은 하중 주의.',''),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · PN','headline':'원인 교정이 1차, 통증은 경구 4계열 맞춤 → 병합','msgs':[
   ('병태생리','고혈당 4경로+미세혈관 허혈 → 양말형 축삭 퇴행, 말초·중추 감작으로 자발통·이질통.'),
   ('주된 호소','좌우대칭 양말형 저림·화끈거림·감각소실, 밤 악화, 무감각발→궤양. NLC·RLS·CVI·PAD와 감별.'),
   ('경구약제','AAN 2022 4계열 효과 동등 → 동반질환 맞춤 단독, 실패 시 병합(OPTION-DM). 오피오이드 지양.'),
   ('주사·중재','척수자극(10 kHz SENZA-PDN)이 근거 최강(불응성 선택). 보툴리눔은 연구단계.'),
   ('ESWT · 비약물','ESWT는 DFU 창상엔 근거·DPN 증상엔 직접근거 없음. 발 관리(IWGDF)가 절단 예방 표준.'),
 ]},
 {'t':'refs','title':'참고문헌 — PN','refs':[
   ('<b>Feldman.</b> Diabetic neuropathy. Nat Rev Dis Primers. 2019.',PM(31197153)),
   ('<b>DCCT Research Group.</b> Intensive treatment and complications in T1DM. N Engl J Med. 1993.',PM(8366922)),
   ('<b>Tesfaye.</b> Diabetic neuropathies: Toronto consensus. Diabetes Care. 2010.',PM(20876709)),
   ('<b>Bouhassira.</b> DN4 neuropathic pain questionnaire. Pain. 2005.',PM(15733628)),
   ('<b>Pop-Busui.</b> Diabetic neuropathy: ADA position statement. Diabetes Care. 2017.',PM(27999003)),
   ('<b>Hitchman.</b> ESWT for diabetic foot ulcers: SR & MA. Ann Vasc Surg. 2019.',PM(30496896)),
   ('<b>Petersen.</b> 10-kHz SCS in painful diabetic neuropathy (SENZA-PDN): RCT. JAMA Neurol. 2021.',PM(33818600)),
   ('<b>Slangen.</b> SCS in painful DPN: RCT. Diabetes Care. 2014.',PM(25216508)),
   ('<b>Yuan.</b> Botulinum toxin for diabetic neuropathic pain: crossover RCT. Neurology. 2009.',PM(19246421)),
   ('<b>Price.</b> Oral & topical treatment of painful DPN: AAN guideline. Neurology. 2022.',PM(34965987)),
   ('<b>Finnerup.</b> Pharmacotherapy for neuropathic pain: NeuPSIG SR & MA. Lancet Neurol. 2015.',PM(25575710)),
   ('<b>Tesfaye.</b> OPTION-DM: amitriptyline/pregabalin/duloxetine crossover. Lancet. 2022.',PM(36007526)),
   ('<b>Simpson.</b> Capsaicin 8% patch in painful DPN (STEP): RCT. J Pain. 2017.',PM(27746370)),
   ('<b>Ziegler.</b> α-lipoic acid over 4 years (NATHAN 1): RCT. Diabetes Care. 2011.',PM(21775755)),
   ('<b>Loprinzi.</b> Prevention & management of CIPN: ASCO guideline. J Clin Oncol. 2020.',PM(32663120)),
   ('<b>Kluding.</b> Exercise on neuropathic symptoms & cutaneous innervation. J Diabetes Complications. 2012.',PM(22717465)),
 ]},
]

# ========================================================= 05 CVI
CVI = [
 {'t':'title','eyebrow':'Chronic Venous Insufficiency · 문헌고찰','title':'만성 정맥부전·정맥류',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사·중재 · 경구약제','series':SERIES},
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'정맥고혈압이 모든 것의 상류','foot':'Bergan 2006 (NEJM); Eberhardt & Raffetto 2014','items':[
   (0,'<b>판막 부전 → 역류 → 지속적 정맥고혈압(ambulatory venous hypertension)</b>이 자기증폭 악순환의 출발점.',''),
   (0,'<b>근육펌프 부전</b>이 이를 고착(발목 강직·부동·비만·고령) → 정맥압이 보행으로도 안 떨어짐.',''),
   (0,'<b>백혈구 포획·염증</b>이 정맥고혈압을 조직 손상으로 번역(MMP·사이토카인) → 벽 리모델링·정맥류.',''),
   (-1,'→ 부종 → 색소침착 → 지방피부경화 → 궤양(C3→C6)으로 진행.','accent'),
 ]},
 {'t':'figure','eyebrow':'병태생리 · 쉽게 보기','tag':('그림 설명','ink'),'title':'왜 저녁에 붓고 무거운가 — 판막과 역류','foot':'Bergan 2006; Mansilha & Sousa 2018','svg':FIG_VALVE,
  'caption':"정맥 판막이 <b>일방향 문</b> 역할을 해 피를 심장으로만 보내요. 판막이 <b>고장나면(부전)</b> 피가 아래로 <b>역류</b>해 정맥압이 올라가고(정맥고혈압), 하루 종일 서 있으면 <b>저녁에 붓고 무거워</b>집니다. 다리를 올리면 완화돼요."},
 {'t':'bullets','eyebrow':'임상 양상','tag':('호소',''),'title':'환자들의 주된 호소','foot':'ESVS 2022; Bradbury 2000','items':[
   (0,'다리 <b>무거움·둔통·부종</b>, <b>오래 서면/저녁에 악화</b>, <b>다리 올림·보행·압박으로 완화</b>.',''),
   (0,'부종은 의존성·오목부종, 저녁 악화·아침 호전(diurnal). 울혈성 피부염 부위에 저림·가려움.',''),
   (0,'가시 소견: 거미정맥·정맥류·헤모시데린 색소침착·지방피부경화·내과부(gaiter) 궤양. <b>감각은 정상.</b>',''),
   (-1,'주의: 증상-역류 상관은 증상특이·성별의존(Bradbury 2000) — "다리 증상=정맥질환" 단정 금지.','accent'),
 ]},
 {'t':'split','eyebrow':'임상 양상 · 진단','tag':('진단',''),'title':'진단 — duplex 초음파가 표준','foot':'Coleridge-Smith 2006 (UIP); Lurie 2020 (CEAP)',
  'items':[
   (0,'<b>정맥 duplex:</b> 역류 지속 <b>표재 >0.5초, 심부 >1.0초</b>가 병적. GSV/SSV/관통/심부·폐색을 지도화.',''),
   (0,'<b>ABI 필수:</b> 압박·소작 전 PAD 배제 — ABI<0.8 주의, <0.5 압박 금기(혼합성 궤양).','red'),
   (0,'중증도 <b>VCSS</b>(CEAP는 분류이지 중증도 아님), QoL <b>CIVIQ-20</b>(신뢰도 >0.80).',''),
   (0,'감별: 림프부종(비오목·Stemmer+)·전신부종(심부전·신장)·DPN·후혈전증후군(PTS)·May-Thurner.',''),
  ],
  'aside':{'title':'CEAP (임상 C등급)','items':[
   (0,'C1 거미·세정맥 / C2 정맥류',''),(0,'C3 부종 / C4 피부변화',''),
   (0,'C5 치유된 궤양 / C6 활동성 궤양',''),(-1,'S 유증상 · A 무증상 · r 재발','accent'),
  ]}},
 {'t':'split','eyebrow':'임상 양상 · 감별','tag':('감별','ink'),'title':'밤 다리 증상 — 4가지 감별','foot':'감별 콜아웃 · 시리즈 공통',
  'items':[
   (0,'<b>vs NLC:</b> NLC는 촉지 통증성 근수축·스트레칭 완화. CVI는 지속적 무거움·거상 완화(경련 아님).',''),
   (0,'<b>vs RLS:</b> RLS는 움직임 충동·보행 완화. CVI는 거상·안정으로 완화, 충동 없음.',''),
   (0,'<b>vs PAD:</b> 허혈은 거상 시 악화·하수 시 완화(정반대). 궤양은 발가락·건조, 맥박 소실.','red'),
   (0,'<b>vs PN:</b> 양말형 감각소실·거상 무관. CVI는 감각 정상·정맥 소견·거상반응이 결정타.',''),
  ],
  'aside':{'title':'정맥소각과 RLS/경련','dark':True,'items':[
   (0,'정맥류 환자에 야간경련·RLS 동반 보고',''),(0,'경화 후 호전(Kanter 1995)',''),
   (0,'그러나 후향·비대조·저근거',''),(-1,'인과 단정 금지 — 감별 우선','accent'),
  ]}},
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 3축 근거','foot':'ESVS 2022 종합',
  'headers':['치료','대표','CVI 근거','위치'],'rows':[
   ['ESWT','정맥성 궤양(C6)','Cooper 2018(RCT 0건)·Dolibog 2024(열등)','궤양 압박 add-on <b>(증상 직접근거 없음)</b>'],
   ['주사·중재','열소작 EVLA/RFA','CLASS(Brittenden 2014·5년)','<b>적합 복재정맥 역류 1차</b>'],
   ['주사·중재','CAC(VenaSeal)/MOCA/폼','VeClose·MARADONA·CLASS','대안 / 보조'],
   ['주사·중재','궤양 조기 소작','EVRA(Gohel 2018)','<b>정맥성 궤양 표준</b>'],
   ['경구약제','MPFF·pentoxifylline·sulodexide','Cochrane·Jull 2012','증상·부종·궤양 <b>보조</b>'],
   ['비약물','압박치료','Amsler 2008·O\'Meara 2012','<b>1차·근간(ABI 후)</b>'],
  ]},
 {'t':'split','eyebrow':'치료 · 체외충격파(ESWT)','tag':('근거 약함','red'),'title':'ESWT — "RCT가 하나도 없다"에서 출발','foot':'Cooper 2018 (Cochrane); Dolibog 2024 (JCM)',
  'items':[
   (0,'<b>Cochrane 2018(Cooper):</b> 정맥성 궤양 치유에 대한 ESWT 평가 — 포함 가능한 <b>RCT 0건</b>(근거 공백 공식 확인).','red'),
   (0,'이후 소규모 RCT: Taheri 2021(n=50) add-on 통증·QoL 신호. 그러나…',''),
   (0,'<b>Dolibog 2024(n=69):</b> ESWT가 표준 압박/IPC보다 <b>오히려 열등</b>(창상 감소 IPC 52.9% > R-ESWT 31.6% > F-ESWT 18%).','red'),
  ],
  'aside':{'title':'정직한 위치','items':[
   (0,'CVI 증상(C3/C4) 직접근거 <b>없음</b>',''),(0,'난치성 궤양 압박 <b>add-on</b>만',''),
   (0,'우월성 미입증',''),(-1,'근본(정맥고혈압) 교정 못 함','accent'),
  ]}},
 {'t':'split','eyebrow':'치료 · 주사·중재 · 근거중심','tag':('1차','green'),'title':'① 열소작(EVLA/RFA) — 근본 교정 1차','foot':'Brittenden 2014·2019 (CLASS, NEJM)',
  'items':[
   (0,'초음파 유도 카테터 + <b>종양팽창마취(tumescent)</b>로 정맥벽 열손상·섬유화 폐쇄(EVLA 810~1470 nm / RFA ~120℃).',''),
   (0,'<b>CLASS(RCT n=798):</b> 폼 vs 레이저 vs 수술 → 본줄기 폐쇄율 <b>폼이 유의하게 낮음</b>, 합병증 레이저 최소.','green'),
   (0,'<b>5년(CLASS 2019):</b> 질병특이 QoL 레이저·수술 > 폼, 비용효과도 레이저 선호 → EVLA를 적합 환자 1차로.','green'),
   (-1,'NICE CG168 등 다수 지침이 복재정맥 역류의 1차로 열소작 권고.','accent'),
  ],
  'aside':{'title':'CLASS 5년','stat':[('n=798','3군 RCT'),('레이저>폼','QoL 우월'),('EVLA','비용효과 1차')]}},
 {'t':'bullets','eyebrow':'치료 · 주사·중재','tag':('대안·보조',''),'title':'② 비열소작(CAC·MOCA) · 폼 경화요법','foot':'VeClose(Morrison 2015); MARADONA 2019; Rabe 2014','items':[
   (0,'<b>시아노아크릴레이트(VenaSeal):</b> 접착제로 즉시 폐쇄, tumescent 불필요. VeClose(RCT n=222) 36개월 폐쇄 <b>CAC 94.4% ≈ RFA 91.9%</b>.','green'),
   (0,'<b>MOCA(ClariVein):</b> 기계+경화제. 시술 통증은 낮으나 2년 폐쇄율 RFA보다 낮은 경향(비열등성 미입증).','muted'),
   (0,'<b>폼 경화요법(Rabe 2014):</b> POL/STS, Tessari 1:4~1:5, 세션당 ≤10 mL. 저비용이나 재개통·재치료 많음.',''),
   (-1,'선택: 적합 복재정맥은 열소작 1차, CAC/MOCA는 대안, 폼은 보조.','accent'),
 ]},
 {'t':'split','eyebrow':'치료 · 주사·중재 · 궤양','tag':('근거 정점','green'),'title':'③ 정맥성 궤양은 조기 소작 — EVRA','foot':'Gohel 2018 (NEJM); Gohel 2020 (JAMA Surg)',
  'items':[
   (0,'<b>EVRA(RCT n=450):</b> 활동성 정맥궤양+표재역류 → (조기 소작+압박) vs (지연 소작).',''),
   (0,'궤양 치유 <b>HR 1.38(95% CI 1.13~1.68, P=0.001)</b>, 치유 중앙 <b>56 vs 82일</b>, 24주 치유 85.6% vs 76.3%.','green'),
   (0,'장기(Gohel 2020): 재발↓(IRR 0.66)·비용효과 우월.',''),
   (-1,'→ 정맥성 궤양은 압박만 하지 말고 <b>역류를 조기에 소작</b>(Level 1).','accent'),
  ],
  'aside':{'title':'EVRA','stat':[('HR 1.38','궤양 치유(P=0.001)'),('56 vs 82일','치유 중앙시간'),('IRR 0.66','재발')]}},
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('보조',''),'title':'④ 정맥활성약물(venoactive drugs)','foot':'Martinez-Zapata 2020 (Cochrane); Jull 2012',
  'note':"Cochrane 총괄: 계열 전체로 부종 경미↓·QoL 무차이·궤양 무효(저확실성)·이상반응↑(rutoside). <b>약물 특이적 근거</b>로 선택 — 압박·중재의 보조이며 단독 대체 아님.",
  'headers':['약물','근거','평가'],'rows':[
   ['MPFF(Daflon)','Kakkos 2018·Coleridge-Smith 2005','<b>근거 최다</b> — 증상·부종·궤양 보조치유'],
   ['말밤나무(HCSE)','Pittler 2012 Cochrane','하지용적 −32.1 mL, 압박스타킹과 대등'],
   ['Pentoxifylline','Jull 2012 Cochrane','궤양 완전치유 <b>RR 1.70</b>(압박 없이도 유효)'],
   ['Sulodexide','Wu 2016 Cochrane','궤양 치유 29.8→49.4%(근거 질 낮음)'],
  ]},
 {'t':'split','eyebrow':'비약물 · 1차','tag':('1차·근간','green'),'title':'⑤ 압박치료 — CVI의 근간','foot':"Amsler & Blättler 2008; O'Meara 2012; ESCHAR",
  'items':[
   (0,'모든 병기(C1~C6)의 <b>1차·근간</b>. 발목 최고 점층압으로 정맥 단면적↓·펌프 효율↑·부종 억제.',''),
   (0,'증상·부종: <b>10–20 mmHg만으로도 위약 대비 유의 개선</b>(Amsler 2008) — 매일 신는 최저 유효압이 관건.','green'),
   (0,"궤양 치유: 압박>무압박(Shi 2021), <b>다성분·탄력·4층붕대 우월</b>(O'Meara 2012). 시행 전 <b>ABI 필수</b>.",''),
   (-1,'재발: 압박이 재발↓, 표재역류 교정 병용 시 4년 재발 56%→31%(ESCHAR P<0.001).','accent'),
  ],
  'aside':{'title':'등급 (발목 mmHg)','items':[
   (0,'15–20: 예방·경증(C0s~C1)',''),(0,'<b>Class I 20–30: 표준(C2~C3)</b>',''),
   (0,'Class II 30–40: C4·궤양 후 유지',''),(-1,'종아리펌프 운동(Padberg 2004) 병용','accent'),
  ]}},
 {'t':'key','eyebrow':'핵심 메시지 · CVI','headline':'압박이 근간(ABI 후), 근본 교정은 표재역류 소작','msgs':[
   ('병태생리','판막부전→역류→정맥고혈압, 근육펌프 부전이 고착, 백혈구 포획·염증→부종·피부변화·궤양.'),
   ('주된 호소','무거움·둔통·부종, 오래 서면/저녁 악화·거상으로 완화, 정맥류·색소·내과부 궤양(감각 정상).'),
   ('압박치료','1차·근간(ABI 확인 후) — 부종·증상·궤양 치유·재발예방 최다 근거. 매일 신는 최저 유효압.'),
   ('주사·중재','적합 복재정맥은 열소작(EVLA/RFA) 1차, 정맥성 궤양은 조기 소작(EVRA). CAC/폼은 대안·보조.'),
   ('경구·ESWT','정맥활성약물(MPFF·pentoxifylline)은 보조. ESWT는 CVI 증상 직접근거 없음 — 과대평가 금지.'),
 ]},
 {'t':'refs','title':'참고문헌 — CVI','refs':[
   ('<b>Bergan.</b> Chronic venous disease. N Engl J Med. 2006.',PM(16885552)),
   ('<b>Eberhardt & Raffetto.</b> Chronic venous insufficiency. Circulation. 2014.',PM(25047584)),
   ('<b>Lurie.</b> The 2020 update of the CEAP classification. J Vasc Surg Venous Lymphat Disord. 2020.',PM(32113854)),
   ('<b>Bradbury.</b> Lower limb symptoms and venous reflux: Edinburgh Vein Study. J Vasc Surg. 2000.',PM(11054224)),
   ('<b>Cooper & Bachoo.</b> ESWT for venous leg ulcers. Cochrane. 2018.',PM(29889978)),
   ('<b>Brittenden.</b> Randomized trial comparing treatments for varicose veins (CLASS). N Engl J Med. 2014.',PM(25251616)),
   ('<b>Brittenden.</b> Five-year outcomes of CLASS. N Engl J Med. 2019.',PM(31483963)),
   ('<b>Gohel.</b> Early endovenous ablation in venous ulceration (EVRA). N Engl J Med. 2018.',PM(29688123)),
   ('<b>Gohel.</b> Long-term outcomes of EVRA. JAMA Surg. 2020.',PM(32965493)),
   ('<b>Morrison.</b> Cyanoacrylate vs RFA for GSV (VeClose): RCT. J Vasc Surg. 2015.',PM(25650040)),
   ('<b>Rabe.</b> European guidelines for sclerotherapy in CVD. Phlebology. 2014.',PM(23559590)),
   ('<b>Martinez-Zapata.</b> Phlebotonics for venous insufficiency. Cochrane. 2020.',PM(33141449)),
   ('<b>Pittler & Ernst.</b> Horse chestnut seed extract for CVI. Cochrane. 2012.',PM(23152216)),
   ('<b>Jull.</b> Pentoxifylline for venous leg ulcers. Cochrane. 2012.',PM(23235582)),
   ("<b>O'Meara.</b> Compression for venous leg ulcers. Cochrane. 2012.",PM(23152202)),
   ('<b>Gohel (ESCHAR).</b> Compression alone vs plus surgery: long-term RCT. BMJ. 2007.',PM(17545185)),
   ('<b>Amsler & Blättler.</b> Compression for leg symptoms & CVD: meta-analysis. Eur J Vasc Endovasc Surg. 2008.',PM(18063393)),
   ('<b>Padberg.</b> Structured exercise improves calf muscle pump in CVI: RCT. J Vasc Surg. 2004.',PM(14718821)),
 ]},
]

DECKS = [("PN_발표_웹","말초신경병증 · 문헌고찰 발표", PN, "04_PN"),
         ("CVI_발표_웹","만성 정맥부전·정맥류 · 문헌고찰 발표", CVI, "05_CVI")]

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"
raw = {}
for fname,title,slides,sub in DECKS:
    raw[fname] = (title, render_deck(title, slides), sub)

# ---- collect glyphs, subset 4 weights ----
allhtml = "".join(h for _,h,_ in raw.values())
vis = re.sub(r'<style.*?</style>','',allhtml,flags=re.S)
vis = re.sub(r'<script.*?</script>','',vis,flags=re.S)
vis = re.sub(r'<[^>]+>',' ',vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@▲▼✕✳")
text=''.join(sorted(chars)); print("glyphs:",len(chars))

PF = os.path.join(os.path.dirname(__file__), "..", "..")  # not used
FONTDIR = "/tmp/claude-0/-home-user-ppt-work/9c48d634-79b7-528e-a229-7723bd2f5c4f/scratchpad/pfont/package/dist/web/static/woff2"
FONTS={"__F900__":FONTDIR+"/Pretendard-Black.woff2","__F800__":FONTDIR+"/Pretendard-ExtraBold.woff2",
       "__F700__":FONTDIR+"/Pretendard-Bold.woff2","__F300__":FONTDIR+"/Pretendard-Light.woff2"}
uris={}
for ph,path in FONTS.items():
    o=Options(); o.flavor='woff2'; o.desubroutinize=True; o.name_IDs=[]; o.name_legacy=False; o.name_languages=[]
    f=TTFont(path); s=Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf=io.BytesIO(); f.save(buf); uris[ph]="data:font/woff2;base64,"+base64.b64encode(buf.getvalue()).decode()
    print(ph,f"{len(buf.getvalue())/1024:.0f}KB")

for fname,(title,htmlc,sub) in raw.items():
    for ph,uri in uris.items(): htmlc=htmlc.replace(ph,uri)
    out=os.path.join(BASE,sub,fname+".html"); open(out,'w',encoding='utf-8').write(htmlc)
    print(out, f"{len(htmlc.encode())/1024:.0f}KB")
print("done")
