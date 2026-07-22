# -*- coding: utf-8 -*-
"""NLC 발표 웹덱 v1.1 (수정본). 사용자 지정 수정사항 반영."""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026 · v1.6"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

# ---- SVG: 반사 균형 / 단축 → 경련 (page 3 그림, 개선) ----
SVG_NORMAL = '''<div class="figpanel good"><div class="pt">평소 (근육 정상 길이)</div>
<svg viewBox="0 0 320 230" role="img">
 <text x="160" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="#1c4a22">브레이크 작동 → 편안</text>
 <!-- 근육 belly -->
 <path d="M40 70 Q55 48 120 48 L180 48 Q200 48 205 70 Q200 92 180 92 L120 92 Q55 92 40 70 Z" fill="#CFE3D2" stroke="#2E7D32" stroke-width="3"/>
 <text x="120" y="75" text-anchor="middle" font-size="14" font-weight="800" fill="#1c4a22">종아리 근육</text>
 <!-- 힘줄 -->
 <line x1="205" y1="70" x2="285" y2="70" stroke="#0B5F5E" stroke-width="8" stroke-linecap="round"/>
 <!-- GTO -->
 <circle cx="250" cy="70" r="15" fill="#0E7C7B"/><text x="250" y="75" text-anchor="middle" font-size="12" font-weight="800" fill="#fff">GTO</text>
 <text x="250" y="102" text-anchor="middle" font-size="12.5" font-weight="700" fill="#0B5F5E">힘줄 센서 = 브레이크</text>
 <!-- 척수 -->
 <rect x="34" y="160" width="252" height="42" rx="10" fill="#EAF1EF" stroke="#0E7C7B" stroke-width="2"/>
 <text x="160" y="186" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0B5F5E">척수 · 브레이크 정상</text>
 <line x1="250" y1="86" x2="220" y2="160" stroke="#2E7D32" stroke-width="2.5"/>
 <text x="292" y="150" text-anchor="middle" font-size="20" font-weight="900" fill="#2E7D32">✓</text>
</svg>
<div class="pl"><b>GTO</b>가 "충분해, 멈춰" 신호를 보내 근육이 <b>이완</b></div></div>'''

SVG_CRAMP = '''<div class="figpanel warn"><div class="pt">자면서 발끝이 펴짐 (근육 짧아짐)</div>
<svg viewBox="0 0 320 230" role="img">
 <text x="160" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="#7a221a">브레이크 풀림 → 폭주</text>
 <!-- 짧아진 근육 -->
 <path class="a-cramp" d="M70 70 Q82 48 130 48 L175 48 Q198 48 202 70 Q198 92 175 92 L130 92 Q82 92 70 70 Z" fill="#F2C9C1" stroke="#A8352A" stroke-width="3"/>
 <text x="135" y="75" text-anchor="middle" font-size="14" font-weight="800" fill="#7a221a">뭉친 근육</text>
 <!-- 느슨한 힘줄 -->
 <path d="M202 70 q22 16 44 0 q14 -12 39 0" fill="none" stroke="#B08" stroke-width="7" stroke-linecap="round" opacity=".55"/>
 <circle cx="252" cy="70" r="15" fill="#C99"/><text x="252" y="75" text-anchor="middle" font-size="12" font-weight="800" fill="#7a221a">GTO</text>
 <text x="252" y="102" text-anchor="middle" font-size="12.5" font-weight="700" fill="#A8352A">느슨 = 브레이크 풀림</text>
 <!-- 운동종판 스파크 -->
 <circle class="a-spark" cx="108" cy="70" r="11" fill="#A8352A"/>
 <text x="108" y="126" text-anchor="middle" font-size="12" font-weight="700" fill="#7a221a">신경-근육 접점 폭주</text>
 <!-- 척수 -->
 <rect x="34" y="160" width="252" height="42" rx="10" fill="#FCEBE7" stroke="#A8352A" stroke-width="2"/>
 <text x="160" y="186" text-anchor="middle" font-size="13.5" font-weight="800" fill="#A8352A">척수가 신호 되먹임 → 증폭</text>
 <line class="a-flow" x1="108" y1="82" x2="120" y2="160" stroke="#A8352A" stroke-width="2.5"/>
 <line class="a-flow" x1="252" y1="86" x2="230" y2="160" stroke="#A8352A" stroke-width="2.5"/>
</svg>
<div class="pl">브레이크(GTO) 헐거워지고 접점 <b>예민</b> → 작은 자극에도 <b>경련</b>. 발끝 당기면 다시 걸림</div></div>'''

# ---- SVG: 심비골신경 주사 위치 (발등, page 11 신규) ----
SVG_DPN = '''<svg viewBox="0 0 640 300" role="img" style="max-width:100%;max-height:34cqw">
 <!-- 발등 윤곽 (위에서 본 오른발) -->
 <path d="M250 40 Q330 30 360 70 Q380 110 372 175 Q365 240 320 262 Q270 275 235 250 Q205 225 210 170 Q214 100 250 40 Z" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2.5"/>
 <!-- 발가락 -->
 <ellipse cx="248" cy="34" rx="15" ry="20" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <ellipse cx="285" cy="28" rx="12" ry="17" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <ellipse cx="315" cy="30" rx="11" ry="15" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <ellipse cx="340" cy="36" rx="10" ry="13" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <ellipse cx="360" cy="46" rx="9" ry="11" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <text x="248" y="16" text-anchor="middle" font-size="13" font-weight="700" fill="#8a6d52">엄지(제1)</text>
 <!-- 제1·2 중족골 -->
 <line x1="255" y1="90" x2="252" y2="55" stroke="#B8946f" stroke-width="7" stroke-linecap="round" opacity=".5"/>
 <line x1="288" y1="92" x2="286" y2="50" stroke="#B8946f" stroke-width="6" stroke-linecap="round" opacity=".5"/>
 <text x="250" y="120" font-size="12.5" fill="#8a6d52">제1 중족골</text>
 <text x="298" y="120" font-size="12.5" fill="#8a6d52">제2 중족골</text>
 <!-- 심비골신경 내측 종말가지 -->
 <path d="M300 250 Q285 180 272 108 Q270 90 269 78" fill="none" stroke="#0E7C7B" stroke-width="3.5" stroke-dasharray="2 5" stroke-linecap="round"/>
 <text x="330" y="215" font-size="13" font-weight="700" fill="#0B5F5E">심비골신경</text>
 <text x="330" y="232" font-size="13" font-weight="700" fill="#0B5F5E">내측 종말가지</text>
 <!-- 주사 표적: 제1-2 중족골 사이 원위 2/3 -->
 <circle class="a-spark" cx="270" cy="95" r="10" fill="#A8352A"/>
 <circle cx="270" cy="95" r="19" fill="none" stroke="#A8352A" stroke-width="2" stroke-dasharray="4 4"/>
 <!-- 주사기 -->
 <g class="a-sway">
 <line x1="270" y1="95" x2="420" y2="180" stroke="#33403B" stroke-width="3"/>
 <rect x="418" y="168" width="70" height="26" rx="4" transform="rotate(29.5 418 168)" fill="#DDE6E4" stroke="#55615B" stroke-width="2"/>
 </g>
 <!-- 라벨 박스 -->
 <rect x="470" y="40" width="158" height="120" rx="10" fill="#F0F4F3" stroke="#DDE6E4" stroke-width="1.5"/>
 <text x="482" y="66" font-size="13.5" font-weight="800" fill="#0B5F5E">주사 위치</text>
 <text x="482" y="90" font-size="12.5" fill="#33403B">· 제1–2 중족골 사이</text>
 <text x="482" y="110" font-size="12.5" fill="#33403B">· 원위 2/3 지점</text>
 <text x="482" y="130" font-size="12.5" fill="#33403B">· 리도카인 5.0 mL</text>
 <text x="482" y="150" font-size="12.5" fill="#33403B">· 깊이 1.0–1.5 cm</text>
 <text x="230" y="290" text-anchor="middle" font-size="12.5" fill="#8a6d52">＊오른발 발등을 위에서 본 모습</text>
</svg>'''

# ---- SVG: 신경 초음파 단면 (perineural vs intraneural, page 14 신규) ----
def _nerve(cx,cy,r,color):
    dots=''
    import math
    for a in range(0,360,45):
        x=cx+r*0.5*math.cos(math.radians(a)); y=cy+r*0.5*math.sin(math.radians(a))
        dots+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.16:.0f}" fill="#3a4750"/>'
    dots+=f'<circle cx="{cx}" cy="{cy}" r="{r*0.16:.0f}" fill="#3a4750"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#8f9aa0" stroke="{color}" stroke-width="3"/>'+dots

SVG_US_OK = '''<div class="figpanel good"><div class="pt">신경 바깥(perineural) · 올바름 ✓</div>
<svg viewBox="0 0 300 210" role="img">
 <rect x="0" y="0" width="300" height="210" rx="8" fill="#1a2228"/>
 <text x="150" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="#9FB0AD">초음파 단면</text>
 '''+_nerve(150,120,42,'#EAF3F1')+'''
 <text x="150" y="176" text-anchor="middle" font-size="12" font-weight="700" fill="#cfd8d6">신경 (벌집 모양 다발)</text>
 <!-- 주입액 halo -->
 <circle cx="150" cy="120" r="60" fill="none" stroke="#5FD6CC" stroke-width="2.5" stroke-dasharray="5 4"/>
 <text x="232" y="70" font-size="12" font-weight="700" fill="#5FD6CC">약물이</text>
 <text x="232" y="86" font-size="12" font-weight="700" fill="#5FD6CC">감쌈</text>
 <!-- 바늘: 신경 바깥에서 멈춤 -->
 <line x1="10" y1="60" x2="112" y2="104" stroke="#F4F7F5" stroke-width="3"/>
 <text x="20" y="52" font-size="12" font-weight="700" fill="#F4F7F5">바늘</text>
</svg>
<div class="pl">바늘 끝을 <b>신경 바로 바깥</b>에 두고 약물이 신경을 <b>도넛처럼 감싸게</b></div></div>'''

SVG_US_BAD = '''<div class="figpanel warn"><div class="pt">신경 속(intraneural) · 금기 ✗</div>
<svg viewBox="0 0 300 210" role="img">
 <rect x="0" y="0" width="300" height="210" rx="8" fill="#1a2228"/>
 <text x="150" y="22" text-anchor="middle" font-size="12.5" font-weight="700" fill="#9FB0AD">초음파 단면</text>
 '''+_nerve(150,120,48,'#E7877A')+'''
 <text x="150" y="182" text-anchor="middle" font-size="12" font-weight="700" fill="#E7877A">신경이 부풀어 오름</text>
 <!-- 바늘: 신경 안으로 들어감 -->
 <line x1="10" y1="70" x2="150" y2="118" stroke="#F4B4A8" stroke-width="3"/>
 <circle class="a-spark" cx="150" cy="120" r="9" fill="#A8352A"/>
 <text x="20" y="62" font-size="12" font-weight="700" fill="#F4B4A8">바늘이 신경 속</text>
</svg>
<div class="pl">신경 <b>안으로</b> 찌르면 신경 부종·손상 → <b>절대 금기</b></div></div>'''

# ---- SVG: FGA 위치 (비복근 원위 건막, page 16 신규) ----
SVG_FGA = '''<svg viewBox="0 0 560 320" role="img" style="max-width:100%;max-height:36cqw">
 <text x="280" y="24" text-anchor="middle" font-size="14" font-weight="800" fill="#17232C">종아리 뒤 · 세로 단면 (안쪽에서 본 모습)</text>
 <!-- 무릎/위 -->
 <text x="60" y="60" font-size="12.5" fill="#55615B">무릎쪽 ↑</text>
 <text x="60" y="300" font-size="12.5" fill="#55615B">발꿈치 ↓</text>
 <!-- 비복근 내측두 belly -->
 <path d="M150 60 Q245 55 250 130 Q252 175 210 205 L150 220 Z" fill="#D8B9A8" stroke="#B07F63" stroke-width="2.5"/>
 <text x="188" y="135" text-anchor="middle" font-size="13.5" font-weight="800" fill="#7a4a34">비복근 내측두</text>
 <text x="188" y="153" text-anchor="middle" font-size="11.5" fill="#8a6d52">(근육 배)</text>
 <!-- 가자미근 -->
 <path d="M150 225 Q235 210 250 145 Q262 210 235 265 L150 285 Z" fill="#E6D2C4" stroke="#C9A98C" stroke-width="2" opacity=".85"/>
 <text x="205" y="250" text-anchor="middle" font-size="12.5" font-weight="700" fill="#8a6d52">가자미근</text>
 <!-- 건막/아킬레스건 -->
 <path d="M150 220 L215 208 Q245 250 235 300 L150 300 Z" fill="#EAF1EF" stroke="#0B5F5E" stroke-width="2"/>
 <text x="120" y="270" text-anchor="end" font-size="12.5" font-weight="700" fill="#0B5F5E">아킬레스건</text>
 <!-- FGA 지점: 근섬유가 끝나는 원위 -->
 <circle class="a-spark" cx="207" cy="203" r="11" fill="#A8352A"/>
 <circle cx="207" cy="203" r="21" fill="none" stroke="#A8352A" stroke-width="2" stroke-dasharray="4 4"/>
 <line x1="207" y1="203" x2="360" y2="150" stroke="#A8352A" stroke-width="2.5"/>
 <!-- 라벨 -->
 <rect x="356" y="80" width="196" height="150" rx="10" fill="#FCEEEB" stroke="#E7CFC9" stroke-width="1.5"/>
 <text x="368" y="106" font-size="13.5" font-weight="800" fill="#A8352A">FGA = 주사 표적</text>
 <text x="368" y="130" font-size="12.5" fill="#33403B">비복근 내측두 근섬유가</text>
 <text x="368" y="148" font-size="12.5" fill="#33403B"><tspan font-weight="800">끝나는 바로 원위</tspan></text>
 <text x="368" y="168" font-size="12.5" fill="#33403B">= 원위 근-건 이행부</text>
 <text x="368" y="188" font-size="12.5" fill="#33403B">= "tennis leg" 부위</text>
 <text x="368" y="212" font-size="12" fill="#8a6d52">아킬레스건 형성 직전</text>
 <!-- US probe -->
 <rect x="120" y="188" width="34" height="14" rx="3" fill="#33403B"/>
 <text x="98" y="199" text-anchor="end" font-size="11.5" font-weight="700" fill="#33403B">초음파</text>
</svg>'''

NLC = [
 {'t':'title','eyebrow':'Nocturnal Leg Cramps · 문헌고찰','title':'야간 하지경련',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사기법 · 경구약제 · 우리 프로토콜','series':SERIES},

 # ---- Page 2: 병태생리 (쉬운 말, 명확화) ----
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'다리 근육을 움직이는 신경이 과흥분한다','foot':'Miller & Layzer 2005; Minetto 2011·2013','items':[
   (0,'야간 하지경련 = 근육이 스스로 <b>오작동</b>해 갑자기 강하게 뭉치는 것. 근육으로 가는 <b>운동신경이 과도하게 흥분</b>해 신호를 마구 쏘아서 생긴다.',''),
   (0,'<b>발화 속도가 폭주:</b> 정상 근수축은 초당 <b>5~30번(5~30 Hz)</b>인데, 경련 땐 신경 끝에서 <b>최대 150번(150 Hz)</b>까지 마구 발화(Miller & Layzer 2005).',''),
   (0,'<b>불씨는 어디서?</b> 다리 <b>말초 신경을 마취로 차단(척수와 연결 끊음)</b>해도 경련은 생김 — 단 더 세게 자극해야 하고 금방 멎음(Minetto 2011) → 불씨는 <b>말초</b>.',''),
   (-1,'이어서 <b>척수(중추)</b>가 되먹임으로 <b>부채질해 키우고 유지</b> → 말초 시작, 중추 증폭.','accent'),
   (0,'<b>(＊중추 병 아님)</b> 경련을 <b>부추기는 딴 요인</b>(전신·말초): 요추관협착·신경눌림, 정맥순환 저하, 신경병증, 전해질, 약물(흡입제·이뇨제·statin).',''),
 ]},

 # ---- Page 3: 그림 (힉스필드 이미지 + 한글 legend) ----
 {'t':'bigfig','eyebrow':'병태생리 · 그림으로','tag':('가속과 브레이크',''),'title':'왜 짧아진 근육에서 경련이 나나',
  'foot':'＊"꺼짐"은 정확히는 "헐거워짐"(GTO=장력 센서) · 유력 모델 · Minetto 2013',
  'svg':'<img src="__PAGE3IMG__" alt="정상 vs 경련 — 브레이크와 신호"/>'},

 # ---- Page 4: 주된 호소 (유지) ----
 {'t':'bullets','eyebrow':'임상 양상','tag':('호소',''),'title':'환자들의 주된 호소','foot':'Hallegraeff 2017; Grandner & Winkelman 2017','items':[
   (0,'수면 중 갑작스러운 종아리·발의 <b>강한 통증성 경련</b>으로 각성.',''),
   (0,'해당 근육이 단단하게 뭉침(<b>촉지되는 근경직</b>), 발끝을 몸쪽으로 당기면(족배굴곡) 완화.',''),
   (0,'지속 수초~최대 10분, 이후 <b>잔통</b>이 남고 수면 분절·주간 피로.',''),
   (0,'<b>위치:</b> 후종아리(비복근)·발이 대부분.',''),
   (0,'<b>유병률(50세+):</b> 경증 24~25% · 중등도 이상 ~6% · 요추관협착 동반 시 최대 65%.',''),
   (-1,'감별: RLS(움직임 충동·움직이면 완화·근경직 없음)와 반드시 구분.','accent'),
 ]},

 # ---- Page 5: 치료 개관 (재정렬·비약물 제거) ----
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 근거 순','foot':'문헌고찰 종합','hlrows':[0,1,2,4],
  'headers':['치료','대표','야간경련 근거','위치'],'rows':[
   ['ESWT','종아리 표적 충격파','Li 2021(후향)+경직 RCT/MA','보조·근거형성 중'],
   ['주사','국소마취제 유발점','Kim 2015·Prateepavanich 1999','MTrP 동반 시'],
   ['주사','심비골신경 내측분지 차단','Imura 2015 <b>직접근거</b>','불응성 선택'],
   ['주사','보툴리눔(비복근)','Park 2017 RCT (Lv II)','불응성·고가'],
   ['경구약제','비타민 B·K2 → diltiazem','Chan·Tan·Voon (Lv C)','안전·우선'],
  ],
  'note':'＊빨간 박스 = 우리 프로토콜 우선순위 · 탐색적(Lv V) 주사(덱사메타손·FGA)는 뒤 슬라이드.'},

 # ---- Page 6: Li 2021 — 충격파를 어떻게 놓았나 ----
 {'t':'split','eyebrow':'치료 · ESWT · 직접근거','tag':('Lv III','amber'),'title':'Li 2021 — 충격파를 어떻게 놓았나','foot':'Li 2021 (Biomed Res Int; PMID 34734084) · 후향적 연구',
  'items':[
   (0,'<b>대상:</b> 요추 퇴행성질환에 동반된 하지경련 환자 <b>126명</b>(후향적 분석).',''),
   (0,'<b>방법:</b> <b>종아리(비복근) 표적</b>으로 1회 <b>2,000타(shocks)</b>, <b>2일 간격</b>, <b>4주간</b> 반복.',''),
   (0,'<b>결과:</b> 경련 빈도·지속·통증 모두 유의하게 감소(P<0.001).','green'),
   (-1,'경련을 <b>직접</b> 평가한 유일한 임상연구 — 단 후향적이라 근거등급은 제한적.','accent'),
  ],
  'aside':{'title':'Li 2021 결과 (ESWT군)','stat':[('5.7→1.3','경련 빈도 (회/시간)'),('57.6→10.6','지속 (초)'),('P<0.001','대조군 대비')]}},

 # ---- (Otero-Luis 슬라이드 삭제 — 본주제와 안 맞음) ----
 # ---- ESWT 기전·한계 (표준 프로토콜 제거, bullets) ----
 {'t':'bullets','eyebrow':'치료 · ESWT','tag':('기전',''),'title':'충격파는 어떻게 듣나 · 한계','foot':'Yang 2021 (J Clin Med, 기전 리뷰)','items':[
   (0,'<b>어떻게 듣나(기전, Yang 2021):</b> 충격파가 신경-근육 접합부를 리모델링(ACh수용체↓)하고 운동신경 흥분성을 낮춘다. 혈류·미세순환도 개선.',''),
   (0,'<b>NO 합성↑</b>·CMAP 6~8주 감소 등으로 과흥분이 가라앉는 것으로 설명된다.',''),
   (-1,'<b>왜 완치가 아닌가(한계):</b> 특발성 경련만 본 RCT가 없고, 효과가 대개 <b>12주 이내로 단기</b> → 보조·근거형성 단계.','accent'),
 ]},

 # ---- Page 8: ① 유발점 주사 (상세) ----
 {'t':'split','eyebrow':'치료 · 주사기법','tag':('Lv II','green'),'title':'① 국소마취제 유발점 주사','foot':'Kim 2015; Prateepavanich 1999',
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
 {'t':'split','eyebrow':'치료 · 주사기법 · 직접근거','tag':('Lv II','green'),'title':'② 심비골신경 내측분지 차단','foot':'Imura 2015 (Brain Behav; PMID 26445706)',
  'items':[
   (0,'<b>Imura 2015:</b> 야간경련에 <b>말초 운동신경가지를 직접 표적</b>한 유일한 전향적 비교연구(요추수술 후 종아리·발 경련 66명).',''),
   (0,'<b>어디를 찌르나:</b> 발등 <b>제1–2 중족골 사이 원위 2/3</b>(심비골신경 <b>내측 종말가지</b>). 1.0% 리도카인 <b>5.0 mL</b>를 1.0–1.5 cm 깊이에.',''),
   (-1,'<b>왜 발등에 찌르는데 종아리가 주나:</b> 근육 마비(BTX)가 아니라 발의 <b>구심성 입력을 차단</b>해 경련 반사고리를 끊기 때문.','accent'),
  ],
  'aside':{'title':'결과 (2주 시점)','stat':[('61% vs 20%','빈도 1/4↓'),('80.5%','빈도 1/2↓ (P<0.01)'),('63.4%','12주+ 지속')]}},

 # ---- ② 심비골 주사 위치 그림 (신규) ----
 {'t':'figure','eyebrow':'치료 · 주사기법 · 위치','tag':('주사 위치',''),'title':'② 심비골신경 차단 — 정확한 주사 위치','foot':'Imura 2015 기법 · 발등 접근',
  'svg':SVG_DPN,
  'caption':'<b>오른발 발등</b>에서 <b>제1·2 중족골 사이 원위 2/3</b> 지점(심비골신경 내측 종말가지)에 <b>1.0% 리도카인 5.0 mL</b>를 깊이 <b>1.0–1.5 cm</b>로 서서히. 근육을 마비시키는 게 아니라 <b>말초 구심성 입력을 차단</b>해 종아리 경련 반사고리를 끊는다.'},

 # ---- ③ 보툴리눔 (유지·번호 조정) ----
 {'t':'bullets','eyebrow':'치료 · 주사기법','tag':('Lv II','green'),'title':'③ 보툴리눔 + 안전성','foot':'Park 2017·Restivo 2018','items':[
   (0,'<b>Park 2017 RCT(n=50):</b> 요추관협착 동반 야간 종아리경련. 비복근 BTX-A vs gabapentin → 전 시점 통증·빈도·강도 유의 감소(P<0.01).','green'),
   (0,'Restivo 2018 RCT: 당뇨병성 신경병증 경련에서 위약 대비 개선(1주부터 16주 지속).',''),
   (0,'주사 계열 중 근거 최고(Lv II)이나 고가·반복·근력약화 우려 → 선택적.',''),
   (-1,'안전(고령): 경골신경→족저굴곡 약화, 총비골신경→족하수→낙상. 초음파 유도·혈관내 주입 회피.','red'),
 ]},

 # ---- ④ 신경주위 dexamethasone (신규·Lv V) ----
 {'t':'bullets','eyebrow':'치료 · 주사기법 · 탐색적','tag':('Lv V','amber'),'title':'④ 신경주위 덱사메타손 주사 — 가능성','foot':'기전 기반 유추 · 직접 임상근거 없음 (Level V)',
  'items':[
   (0,'<b>착상:</b> 경련을 유지하는 것은 운동신경 과흥분. 그렇다면 그 근육을 지배하는 <b>신경 줄기 주위</b>에 덱사메타손을 두면 이소성 과흥분·신경주위 염증을 눌러 경련 역치를 올릴 수 있다.',''),
   (0,'<b>표적 신경 = 경련 부위로 정한다:</b>',''),
   (1,'<b>후경골신경</b>(오금~족근관): 종아리 뒤칸(비복근·가자미근)·발바닥 지배 → <b>종아리 경련</b>.',''),
   (1,'<b>총비골신경</b>(비골두 뒤): 앞·가쪽칸(정강이·발등) 지배 → <b>정강이·발 경련</b>.',''),
   (-1,'근거: 덱사메타손은 말초신경차단의 <b>검증된 보조제</b>(진통 연장·항염). 단 경련 직접근거는 <b>없음</b> → 기전기반 <b>Level V</b>.','accent'),
   (0,'안전: 초음파로 <b>신경 바깥(perineural)에만</b> 주입 — <b>신경 속(intraneural)은 신경손상 위험이라 금기</b>. 총비골 차단 시 족하수 주의.','red'),
 ]},

 # ---- 신경 초음파 단면 그림 (신규) ----
 {'t':'figure','eyebrow':'치료 · 주사기법 · 안전','tag':('초음파',''),'title':'초음파 단면 — 신경 바깥에만, 신경 속은 금기','foot':'신경주위(perineural) 주사 안전 원칙',
  'svg':SVG_US_OK+SVG_US_BAD,
  'caption':'신경은 초음파에서 <b>벌집 모양 다발</b>로 보인다. 바늘 끝을 <b>신경 바로 바깥</b>에 두고 약물이 신경을 <b>도넛처럼 감싸게</b> 하는 것이 정답(왼쪽). <b>신경 속으로</b> 찌르면 신경이 부풀고 손상되므로 <b>절대 금기</b>(오른쪽).'},

 # ---- ⑤ FGA 주사 (신규·Lv V) ----
 {'t':'split','eyebrow':'치료 · 주사기법 · 탐색적','tag':('Lv V','amber'),'title':'⑤ FGA 주사 — 신규 가설','foot':'Pedret 2020 (Scand J Med Sci Sports); Balius 2018',
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

 # ---- FGA 위치 그림 (신규) ----
 {'t':'figure','eyebrow':'치료 · 주사기법 · 위치','tag':('FGA 위치',''),'title':'⑤ FGA — 정확히 어디인가','foot':'Pedret 2020 · 비복근 원위 근-건 이행부',
  'svg':SVG_FGA,
  'caption':'<b>FGA</b>는 <b>비복근 내측두의 근섬유가 끝나는 바로 원위</b> = 원위 근-건 이행부(아킬레스건이 만들어지기 직전, 임상적으로 <b>"tennis leg"</b>가 생기는 자리). 근육 배(belly)가 아니라 <b>건막</b>을 겨냥하며, <b>초음파 유도</b>로 소복재정맥·비복신경을 피해 접근한다.'},

 # ---- Page 12: 경구약제 (재정렬) ----
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'경구 약제 — 안전한 것부터','foot':'AAN(Katzberg 2010); Cochrane 종합',
  'headers':['약제','근거','근거수준','평가'],'rows':[
   ['비타민 B 복합','Chan 1998 RCT','<b>Lv II</b>','빈도·강도 감소·안전 → 우선 시도'],
   ['Vitamin K2','Tan 2024 RCT','<b>Lv II</b>','빈도 2.60→0.96 (⚠정정 통지)'],
   ['Diltiazem 30mg','Voon 2001 교차RCT','<b>Lv II</b>','빈도 5.8→0.16/2주'],
   ['마그네슘(특발성)','Garrison 2020 Cochrane','<b>Lv I</b>','임상 이득 없음 — <b>권고 안 함</b>'],
   ['Quinine','El-Tawil 2015 Cochrane','<b>Lv I</b>','효과O·혈소판감소/TTP → <b>최후</b>'],
  ],
  'note':'＊근거수준(Lv I~V)은 연구 설계 기준 — Lv I이라도 마그네슘은 무효, quinine은 독성이라 권고 안 함(근거수준 ≠ 권고).'},

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

TITLE = "야간 하지경련 · 문헌고찰 발표 · v1.6 (수정본)"
BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/01_NLC"
htmlc = render_deck(TITLE, NLC)
# 화면 하단 버전 라벨 강조
htmlc = htmlc.replace(f'<div class="deckttl">{TITLE}</div>',
                      '<div class="deckttl">야간 하지경련 · 문헌고찰 발표 · <b>v1.6 (수정본)</b></div>')
# 페이지3 힉스필드 이미지 임베드
import base64 as _b64
_p3=_b64.b64encode(open(os.path.join(BASE,"assets/page3_reflex.jpg"),'rb').read()).decode()
htmlc = htmlc.replace("__PAGE3IMG__","data:image/jpeg;base64,"+_p3)

# ---- 폰트 서브셋 ----
vis = re.sub(r'<style.*?</style>','',htmlc,flags=re.S)
vis = re.sub(r'<script.*?</script>','',vis,flags=re.S)
vis = re.sub(r'<[^>]+>',' ',vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@")
text=''.join(sorted(chars)); print("glyphs:",len(chars))

UP="/root/.claude/uploads/bb19d1cb-d1ba-542e-8235-38fcac774773/"
FONTS={"__F900__":UP+"c71b728f-PretendardBlack.otf","__F800__":UP+"3a19e05c-PretendardExtraBold.otf",
       "__F700__":UP+"1121d3ff-PretendardBold.otf","__F300__":UP+"82c21b19-PretendardLight.otf"}
for ph,path in FONTS.items():
    o=Options(); o.flavor='woff2'; o.desubroutinize=True; o.name_IDs=[]; o.name_legacy=False; o.name_languages=[]
    f=TTFont(path); s=Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf=io.BytesIO(); f.save(buf); uri="data:font/woff2;base64,"+base64.b64encode(buf.getvalue()).decode()
    htmlc=htmlc.replace(ph,uri); print(ph,f"{len(buf.getvalue())/1024:.0f}KB")

out=os.path.join(BASE,"NLC_발표_웹_v1.6.html")
open(out,'w',encoding='utf-8').write(htmlc)
print("slides:",len(NLC),"| out:",out,f"{len(htmlc.encode())/1024:.0f}KB")
