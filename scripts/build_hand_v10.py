# -*- coding: utf-8 -*-
"""손 경련(Hand Cramps) 문헌고찰 웹덱 v1.0 — NLC 덱과 동일한 Clinical Ledger 포맷.

주소: "밥 먹을 때(젓가락질)·글씨 쓸 때 손에 쥐가 난다" → 과제특이성을 축으로 구성.
치료는 충격파(ESWT) · 주사 · 경구약제 3축.

폰트: Pretendard 파일이 이 세션에 없어 NanumGothic(4 weight)을 서브셋 임베드하되,
@font-face src 에 local("Pretendard …")를 먼저 두어 Pretendard가 설치된 PC에서는
그대로 Pretendard가 쓰이게 했다. (본문 분량은 더 넓은 NanumGothic 기준으로 맞춤)
"""
import os, sys, re

sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck

SERIES = "상지증상 문헌고찰 시리즈 · 2026 · v1.0"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

EMBED_FONTS = True
NG = "/usr/local/lib/python3.11/dist-packages/koreanize_matplotlib/fonts/"
FONTS = {  # placeholder → (폰트 파일, local() 후보)
    "__F900__": (NG + "NanumGothicExtraBold.ttf", ['Pretendard Black', 'Pretendard ExtraBold']),
    "__F800__": (NG + "NanumGothicExtraBold.ttf", ['Pretendard ExtraBold', 'Pretendard Bold']),
    "__F700__": (NG + "NanumGothicBold.ttf",      ['Pretendard Bold']),
    "__F300__": (NG + "NanumGothicLight.ttf",     ['Pretendard Light', 'Pretendard Regular']),
}
FONT_STACK = ('"Pretendard Variable","Apple SD Gothic Neo",'
              '"Malgun Gothic","맑은 고딕",AppleGothic,"Noto Sans KR",system-ui,sans-serif')

# ---------------------------------------------------------------- SVG 1·2
SVG_TRUE = '''<div class="figpanel warn"><div class="pt">① 진성 근경련 (true cramp) · 말초</div>
<svg viewBox="0 0 320 236" role="img">
 <text x="160" y="22" text-anchor="middle" font-size="13.5" font-weight="800" fill="#7a221a">신경 끝이 폭주한다</text>
 <path class="a-cramp" d="M44 66 Q60 44 118 44 L176 44 Q200 44 205 66 Q200 90 176 90 L118 90 Q60 90 44 66 Z"
       fill="#F2C9C1" stroke="#A8352A" stroke-width="3"/>
 <text x="122" y="72" text-anchor="middle" font-size="13" font-weight="800" fill="#7a221a">전완 굴근 · 손 근육</text>
 <path d="M262 40 Q240 52 214 62" fill="none" stroke="#33403B" stroke-width="3" stroke-linecap="round"/>
 <text x="286" y="36" text-anchor="middle" font-size="12" font-weight="700" fill="#33403B">운동신경</text>
 <circle class="a-spark" cx="208" cy="64" r="10" fill="#A8352A"/>
 <text x="252" y="86" text-anchor="middle" font-size="11.5" font-weight="700" fill="#A8352A">최대 150 Hz 방전</text>
 <rect x="34" y="158" width="252" height="44" rx="10" fill="#FCEBE7" stroke="#A8352A" stroke-width="2"/>
 <text x="160" y="185" text-anchor="middle" font-size="13" font-weight="800" fill="#A8352A">척수가 되먹임 → 증폭·유지</text>
 <line class="a-flow" x1="150" y1="92" x2="140" y2="158" stroke="#A8352A" stroke-width="2.5"/>
 <line class="a-flow" x1="208" y1="76" x2="196" y2="158" stroke="#A8352A" stroke-width="2.5"/>
 <text x="160" y="224" text-anchor="middle" font-size="11.5" fill="#8a6d52">＊야간 하지경련(NLC)과 같은 축</text>
</svg>
<div class="pl">불씨는 <b>말초 운동신경 종말</b> · 척수가 키운다 → <b>신전으로 완화</b></div></div>'''

SVG_DYST = '''<div class="figpanel"><div class="pt" style="color:#0B5F5E">② 과제특이 이긴장증 (FTSD) · 중추</div>
<svg viewBox="0 0 320 236" role="img">
 <text x="160" y="22" text-anchor="middle" font-size="13.5" font-weight="800" fill="#0B5F5E">브레이크(억제)가 빠진다</text>
 <path d="M40 40 Q160 14 280 40 L280 84 L40 84 Z" fill="#EAF1EF" stroke="#0E7C7B" stroke-width="2.5"/>
 <text x="160" y="60" text-anchor="middle" font-size="12.5" font-weight="800" fill="#0B5F5E">감각·운동 피질</text>
 <circle cx="128" cy="76" r="17" fill="#0E7C7B" opacity=".33"/>
 <circle cx="152" cy="76" r="17" fill="#0E7C7B" opacity=".33"/>
 <circle cx="176" cy="76" r="17" fill="#0E7C7B" opacity=".33"/>
 <text x="146" y="112" text-anchor="middle" font-size="11.5" font-weight="700" fill="#0B5F5E">손가락 표상이 겹침</text>
 <line class="a-brk" x1="252" y1="86" x2="252" y2="140" stroke="#A8352A" stroke-width="3" stroke-dasharray="6 6"/>
 <text x="288" y="118" text-anchor="middle" font-size="11.5" font-weight="800" fill="#A8352A">주변억제</text>
 <text x="288" y="132" text-anchor="middle" font-size="11.5" font-weight="800" fill="#A8352A">소실</text>
 <rect class="a-spark" x="56" y="150" width="86" height="34" rx="8" fill="#CFE3D2" stroke="#2E7D32" stroke-width="2.5"/>
 <text x="99" y="172" text-anchor="middle" font-size="12" font-weight="800" fill="#1c4a22">목표 근육</text>
 <rect class="a-spark" x="158" y="150" width="96" height="34" rx="8" fill="#F2C9C1" stroke="#A8352A" stroke-width="2.5"/>
 <text x="206" y="172" text-anchor="middle" font-size="12" font-weight="800" fill="#7a221a">옆·길항 근육</text>
 <text x="160" y="206" text-anchor="middle" font-size="12" font-weight="800" fill="#A8352A">같이 켜짐 = 과다동시수축</text>
 <text x="160" y="226" text-anchor="middle" font-size="11.5" fill="#8a6d52">＊쓰기·젓가락질에서만 나타남</text>
</svg>
<div class="pl">근육이 아니라 <b>회로의 조절 실패</b> → <b>그 과제에서만</b> 굳는다</div></div>'''

# ---------------------------------------------------------------- SVG 3 (표적 지도)
SVG_TARGET = '''<svg viewBox="0 0 620 330" role="img" style="max-width:58cqw;max-height:37cqw;align-self:center">
 <text x="300" y="20" text-anchor="middle" font-size="14" font-weight="800" fill="#17232C">오른 전완·손 · 손바닥 쪽에서 본 모습</text>
 <path d="M20 96 Q22 74 60 70 L300 74 Q322 92 322 148 Q322 204 300 222 L60 226 Q22 222 20 200 Z"
       fill="#F3E7DC" stroke="#C9A98C" stroke-width="2.5"/>
 <text x="26" y="62" font-size="12" fill="#8a6d52">팔꿈치</text>
 <path d="M60 108 Q170 100 268 110" fill="none" stroke="#B07F63" stroke-width="7" opacity=".45" stroke-linecap="round"/>
 <path d="M60 148 Q170 142 268 150" fill="none" stroke="#B07F63" stroke-width="7" opacity=".45" stroke-linecap="round"/>
 <path d="M60 188 Q170 184 268 188" fill="none" stroke="#B07F63" stroke-width="7" opacity=".45" stroke-linecap="round"/>
 <text x="44" y="256" font-size="12.5" font-weight="700" fill="#8a6d52">전완 굴근군</text>
 <text x="44" y="274" font-size="12" fill="#8a6d52">FCR · FCU · FDS · FDP</text>
 <rect x="322" y="86" width="26" height="150" rx="8" fill="#E6D2C4" stroke="#C9A98C" stroke-width="2"/>
 <path d="M348 92 Q408 84 442 104 Q470 122 470 160 Q470 200 442 218 Q408 238 348 230 Z"
       fill="#F3E7DC" stroke="#C9A98C" stroke-width="2.5"/>
 <rect x="466" y="104" width="86" height="17" rx="8" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <rect x="466" y="132" width="98" height="17" rx="8" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <rect x="466" y="160" width="92" height="17" rx="8" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <rect x="466" y="188" width="78" height="17" rx="8" fill="#F3E7DC" stroke="#C9A98C" stroke-width="2"/>
 <path d="M366 232 Q392 262 428 268 Q446 270 452 256 Q456 242 438 234 Q404 224 384 210 Z"
       fill="#F3E7DC" stroke="#C9A98C" stroke-width="2.5"/>
 <text x="558" y="118" font-size="12" fill="#8a6d52">검지</text>
 <path d="M200 140 Q290 138 336 146 Q382 154 430 150" fill="none" stroke="#0E7C7B" stroke-width="3.2" stroke-dasharray="2 5" stroke-linecap="round"/>
 <path d="M200 196 Q290 196 336 198 Q380 200 420 206" fill="none" stroke="#7A4AA8" stroke-width="3.2" stroke-dasharray="2 5" stroke-linecap="round"/>
 <circle class="a-spark" cx="150" cy="148" r="11" fill="#A8352A"/>
 <text x="150" y="128" text-anchor="middle" font-size="13" font-weight="900" fill="#A8352A">①</text>
 <circle cx="336" cy="146" r="10" fill="#0E7C7B"/>
 <text x="336" y="70" text-anchor="middle" font-size="13" font-weight="900" fill="#0B5F5E">②</text>
 <line x1="336" y1="78" x2="336" y2="136" stroke="#0B5F5E" stroke-width="1.6"/>
 <circle cx="336" cy="198" r="10" fill="#7A4AA8"/>
 <text x="268" y="296" text-anchor="middle" font-size="13" font-weight="900" fill="#5A2E8A">③</text>
 <line x1="276" y1="290" x2="330" y2="208" stroke="#5A2E8A" stroke-width="1.6"/>
 <circle class="a-spark" cx="404" cy="240" r="10" fill="#A8352A"/>
 <text x="404" y="296" text-anchor="middle" font-size="13" font-weight="900" fill="#A8352A">④</text>
 <line x1="404" y1="288" x2="404" y2="250" stroke="#A8352A" stroke-width="1.6"/>
 <circle class="a-spark" cx="452" cy="120" r="10" fill="#A8352A"/>
 <text x="452" y="66" text-anchor="middle" font-size="13" font-weight="900" fill="#A8352A">⑤</text>
 <line x1="452" y1="74" x2="452" y2="110" stroke="#A8352A" stroke-width="1.6"/>
 <text x="300" y="322" text-anchor="middle" font-size="11.5" fill="#8a6d52">— · — 초록 = 정중신경 · 보라 = 척골신경</text>
</svg>
<div style="flex:1;max-width:32cqw;display:flex;flex-direction:column;justify-content:center;gap:1.15cqw;text-align:left">
 <div style="font-weight:800;font-size:2.05cqw;color:#17232C">표적 5곳</div>
 <div style="font-weight:300;font-size:1.72cqw;line-height:1.28;color:#33403B"><b style="color:#A8352A">①</b> <b>전완 굴근군</b> — ESWT·보툴리눔·유발점</div>
 <div style="font-weight:300;font-size:1.72cqw;line-height:1.28;color:#33403B"><b style="color:#0B5F5E">②</b> <b>수근관 정중신경</b> — D5W 수압박리</div>
 <div style="font-weight:300;font-size:1.72cqw;line-height:1.28;color:#33403B"><b style="color:#5A2E8A">③</b> <b>기용관 척골신경</b> — 신경주위 주사</div>
 <div style="font-weight:300;font-size:1.72cqw;line-height:1.28;color:#33403B"><b style="color:#A8352A">④</b> <b>무지구·무지내전근</b> — 보툴리눔·유발점</div>
 <div style="font-weight:300;font-size:1.72cqw;line-height:1.28;color:#33403B"><b style="color:#A8352A">⑤</b> <b>제1배측골간근</b> — 보툴리눔</div>
 <div style="font-weight:700;font-size:1.5cqw;line-height:1.3;color:#9A6800;border-top:1.5px solid #E4E9E8;padding-top:1cqw">손은 구조가 밀집 → <b>용량을 줄이고 초음파를 쓴다</b></div>
</div>'''

# ---------------------------------------------------------------- 슬라이드
HAND = [
 {'t':'title','eyebrow':'Hand Cramps · 문헌고찰','title':'손에 쥐가 난다',
  'sub':'밥 먹을 때·글씨 쓸 때만 — 원인 감별과 근거 기반 치료',
  'order':'감별 · 병태생리 → 충격파(ESWT) · 주사기법 · 경구약제','series':SERIES},

 # ---- 원인 5갈래 ----
 {'t':'split','eyebrow':'가장 먼저 · 원인','tag':('원인 5갈래','ink'),
  'title':'"손 쥐" 한 단어에 서로 다른 병이 섞여 있다','foot':'Stahl & Frucht 2017; Miller & Layzer 2005; Ahmed & Simmons 2017 종합',
  'items':[
   (0,'<b>과제 특이성</b>(그 동작에서만)이 있으면 <b>과제특이 국소 손 이긴장증(FTSD)</b>을 먼저 놓는다.','accent'),
   (0,'저림·야간 증상 → <b>포착신경병증</b>. 압통·과사용 → <b>근막통증</b>.',''),
   (0,'양측·입주위 저림 → <b>테타니</b>. 잔떨림·위약 → <b>신경과 정밀검사</b>.',''),
   (0,'실제로는 <b>FTSD + 포착·과사용이 겹친</b> 경우가 흔하다.',''),
   (-1,'⚠ 손 경련은 <b>원인별 % 통계가 없다</b> — 오른쪽은 분포가 아닌 <b>감별 순서</b>.','red'),
  ],
  'aside':{'title':'보는 순서','items':[
   (0,'<b>① 과제특이 이긴장증</b> — 쓰기·젓가락질'),
   (0,'<b>② 포착</b> — 정중·척골·C8–T1'),
   (0,'<b>③ 과사용·근막통증</b> — 전완 굴근'),
   (0,'<b>④ 전신·대사·약물</b> — Ca·Mg·갑상선'),
   (-1,'<b>⑤ 적색기</b> — 잔떨림·위약·위축','red'),
  ]}},

 # ---- 감별표 ----
 {'t':'table','eyebrow':'가장 먼저','tag':('감별','ink'),'title':'감별 — 손이 굳는 증상',
  'foot':'＊"그 손으로 하는 다른 동작은 정상인가?" — 이 질문이 FTSD와 나머지를 가른다 · 빨간 칸이 표적',
  'headers':['질환','핵심 소견'],'hlrows':[0],'rows':[
   ['<b>과제특이 손 이긴장증</b>','<b>그 동작에서만 · 감각 트릭 · 안정 시 정상</b>'],
   ['진성 근경련','촉지 근경직 · 신전으로 완화'],
   ['손목터널증후군','야간 저림 · 1~3수지 · Phalen/Tinel'],
   ['척골신경병증','4·5수지 · Froment · 골간근 위축'],
   ['경추 신경근증 C8–T1','팔 방사통 · 감각저하 · Spurling'],
   ['테타니(저칼슘)','양측 손·입주위 저림 · Trousseau'],
   ['경련-잔떨림 증후군','잔떨림 · 전신 확산 · 진행성 위약'],
  ]},

 # ---- 병태생리 ----
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'기전이 둘이다 — 말초의 폭주 vs 중추의 억제 실패','foot':'Miller & Layzer 2005; Minetto 2013; Stahl & Frucht 2017','items':[
   (0,'<b>진성 근경련:</b> 원위 <b>운동축삭 종말</b>의 고빈도(최대 <b>150 Hz</b>) 방전 → 척수가 증폭. <b>짧아진 자세</b>에서 나고 <b>신전으로 완화</b>.',''),
   (0,'<b>과제특이 이긴장증(FTSD):</b> 근육의 병이 아니라 <b>운동 회로의 조절 실패</b>다.',''),
   (1,'① <b>억제 결핍</b> — 목표 근육을 쓸 때 <b>옆 근육까지 같이 켜짐</b>(과다동시수축)',''),
   (1,'② <b>감각-운동 통합 이상</b> — 감각피질의 <b>손가락 표상이 겹침</b>',''),
   (1,'③ <b>비정상 가소성</b> — 반복 훈련이 잘못된 회로를 오히려 굳힌다',''),
   (-1,'원인은 중추인데 <b>말초를 눌러도 좋아진다</b> → 그래서 <b>보툴리눔 + 재훈련</b>을 함께 쓴다.','accent'),
 ]},

 # ---- 그림 ----
 {'t':'figure','eyebrow':'병태생리 · 그림으로','tag':('두 기전',''),'title':'같은 "쥐"인데 왜 치료가 다른가',
  'foot':'Minetto 2013 · Stahl & Frucht 2017',
  'svg':SVG_TRUE+SVG_DYST,
  'caption':'<b>왼쪽</b>은 신전·유발점·신경 접근이, <b>오른쪽</b>은 보툴리눔·재훈련·도구 개조가 듣는다.'},

 # ---- 임상 양상 ----
 {'t':'split','eyebrow':'임상 양상','tag':('호소',''),'title':'왜 하필 "밥 먹을 때·쓸 때"만 나는가','foot':'Stahl & Frucht 2017; Torres-Russotto & Perlmutter 2008',
  'items':[
   (0,'젓가락질과 필기는 둘 다 <b>정밀 파지(precision grip)</b> — 같은 회로·같은 근육을 쓴다.',''),
   (0,'<b>통증보다 자세 이상·경직감</b>이 앞서고, 펜·젓가락을 <b>과하게 움켜쥐거나 검지가 벌어진다</b>.',''),
   (0,'<b>감각 트릭</b>(반대 손으로 손목을 잡으면 완화)이 있으면 진단적 가치가 크다.',''),
   (-1,'반대로 <b>안정 시에도</b>, <b>다른 동작에서도</b>, <b>양손·발까지</b> 번지면 FTSD가 아니다.','red'),
  ],
  'aside':{'title':'FTSD 역학','stat':[('2.7/백만','연간 발생률'),('7~69/백만','유병률 추정'),('5~20%','가족력')]}},

 # ---- 진단 접근 ----
 {'t':'bullets','eyebrow':'진단','tag':('접근 순서','ink'),'title':'진단 — 병력 · 재현 관찰 · 검사','foot':'교육용 진단 순서 · 개별 적용은 임상 판단','items':[
   (0,'<b>① 병력:</b> 어떤 동작에서? <b>다른 동작은 정상인가?</b> 감각 트릭·야간 저림·복용약.',''),
   (0,'<b>② 재현 관찰:</b> <b>직접 쓰게 하고 젓가락을 쥐게 한다</b> — <b>동영상</b>이 전후 비교의 유일한 객관 자료.','accent'),
   (0,'<b>③ 진찰:</b> Phalen·Tinel / Froment / Spurling / Trousseau / 근위축.',''),
   (0,'<b>④ NCS/EMG:</b> 포착·신경근병증·경련잔떨림증후군 감별의 중심축.',''),
   (0,'<b>⑤ 혈액:</b> 이온화 Ca · Mg · TSH · HbA1c · CK.',''),
   (-1,'<b>⑥ 초음파:</b> 정중·척골신경 단면적, 전완 굴근 유발점 → 그대로 <b>주사 유도</b>.','accent'),
 ]},

 # ---- 치료 개관 ----
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관 — 근거가 있는 것과 외삽인 것','foot':'문헌고찰 종합 · 근거수준은 연구 설계 기준(I~V)',
  'headers':['축','치료','손 경련 근거','수준'],'rows':[
   ['주사','보툴리눔 (전완 굴근·손 내재근)','Kruisdijk 2007 RCT','<b>II</b>'],
   ['주사','정중신경 D5W 수압박리','Wu 2017 RCT (손목터널)','<b>II</b>'],
   ['주사','척골신경 주위 · 유발점','외삽 — 직접 근거 없음','<b>IV~V</b>'],
   ['ESWT','상지 이긴장증','Trompetto 2009 (예비)','<b>IV</b>'],
   ['ESWT','손목터널 · 상지 경직(인접)','Chen 2022 · Cabanas-Valdés 2020','<b>I(제한)</b>'],
   ['경구','mexiletine · carbamazepine','Weiss 2016 RCT · CFS 후향','<b>II(간접)</b>'],
  ],
  'note':'＊근거의 무게 = <b>보툴리눔 &gt; 신경 수압박리 &gt; ESWT &gt; 경구약제</b>.'},

 # ---- ESWT 직접근거 ----
 {'t':'split','eyebrow':'치료 · ESWT · 직접근거','tag':('Lv IV','amber'),'title':'Trompetto 2009 — 이긴장증에 충격파를 놓아 봤다','foot':'Trompetto 2009 (Eur J Neurol; PMID 19187259) · 예비연구·소규모',
  'items':[
   (0,'상지 이긴장증 환자에게 <b>이환된 근육을 표적</b>으로 ESWT를 시행한 <b>예비연구</b>.',''),
   (0,'<b>이차성 이긴장증 3명</b>은 마지막 세션 후 <b>최소 1개월 지속되는 현저한 호전</b>.','green'),
   (0,'그러나 <b>writer\'s cramp에서는 일관되지 않아 2명에서만 유효</b>했다.','red'),
   (-1,'정직하게: 특발 FTSD에 대한 ESWT 근거는 <b>예비 단계</b>. 무해·저렴하므로 <b>병용·근거형성</b>으로 위치시킨다.','accent'),
  ],
  'aside':{'title':'무엇을 말할 수 있나','items':[
   (0,'<b>이차성</b> 이긴장증 → 반응 좋음','green'),
   (0,'<b>특발 writer\'s cramp</b> → 일관되지 않음','red'),
   (0,'부작용 없음 · 비침습'),
   (-1,'→ 단독이 아니라 <b>병용</b>으로','accent'),
  ]}},

 # ---- ESWT 인접근거 ----
 {'t':'split','eyebrow':'치료 · ESWT · 인접근거','tag':('Lv I','green'),'title':'충격파의 무게는 "경직"과 "손목터널"에서 온다','foot':'Cabanas-Valdés 2020 (Clin Rehabil, 16 RCT·764명); Chen 2022 (Medicina, 7 RCT·376명)',
  'items':[
   (0,'<b>상지 경직 SR/MA:</b> 가짜자극 대비 <b>MAS −0.28</b>(95% CI −0.54~−0.03), 물리치료 병용 시 <b>−1.78</b>. 상지 Fugl-Meyer 단기 <b>+0.94</b>.','green'),
   (0,'<b>손목터널 SR/MA:</b> 부목 단독 대비 효과는 <b>대체로 일시적</b>이나 <b>4주 시점 기능·증상은 유의 호전</b>. 국소 스테로이드 주사와 <b>차이 뚜렷하지 않음</b>.',''),
   (-1,'경직 ≠ 경련 ≠ 이긴장증이지만 <b>표적(전완 굴근군)</b>과 <b>목표(과흥분 낮추기)</b>가 맞닿는다.','accent'),
  ],
  'aside':{'title':'인접 근거 숫자','stat':[('−0.28','상지 경직 MAS'),('−1.78','물리치료 병용 시'),('4주','손목터널 유의 시점')]}},

 # ---- ESWT 기전·프로토콜 ----
 {'t':'bullets','eyebrow':'치료 · ESWT','tag':('기전·술기',''),'title':'충격파는 어떻게 듣나 · 손에서의 프로토콜','foot':'Yang 2021 (J Clin Med, 기전 리뷰) · 프로토콜은 문헌 기반 제안','items':[
   (0,'<b>기전 — 과흥분을 네 갈래로 가라앉힌다:</b>',''),
   (1,'① 신경-근접합부 <b>리모델링</b>(ACh 수용체↓) ② <b>운동신경 흥분성↓</b>',''),
   (1,'③ <b>산화질소(NO) 합성↑</b> ④ <b>혈류·미세순환 개선</b>',''),
   (0,'<b>표적(제안):</b> 전완 굴근군(FCR·FCU·FDS) 근복·운동점 + 무지구.',''),
   (0,'<b>용량(제안):</b> radial <b>1.5~2.5 bar</b> 또는 focused <b>~0.10 mJ/mm²</b>, 부위당 <b>1,500~2,000 타</b>, <b>주 1~2회 · 3~4주</b>.',''),
   (-1,'<b>안전:</b> 초음파로 신경 주행 확인, <b>신경 위 고에너지 직접 조사는 피한다</b>.','red'),
 ]},

 # ---- 주사 ① 보툴리눔 ----
 {'t':'split','eyebrow':'치료 · 주사 · 최고 근거','tag':('Lv II','green'),'title':'① 보툴리눔 — 유일한 위약대조 RCT','foot':'Kruisdijk 2007 (J Neurol Neurosurg Psychiatry, n=40, 2회 주사·12주 + 1년 추적)',
  'items':[
   (0,'<b>Kruisdijk 2007:</b> writer\'s cramp 40명을 BoNT-A vs 위약으로 무작위 배정.',''),
   (0,'<b>BoNT-A군 14/20(70%)</b>이 이득을 보고하고 <b>치료 지속을 선택</b> — 위약군 6/19(31.6%), <b>P=0.03</b>.','green'),
   (0,'<b>체계적 고찰:</b> 6개 대조연구·139명 통합 <b>약 73% 호전</b> → 상지 이긴장증에서 <b>"probably effective"</b>.',''),
   (-1,'원인은 중추 회로지만 <b>말초의 과다동시수축을 약하게 만들면</b> 출력이 정상 범위로 돌아온다 — <b>증상 조절</b>이지 근치가 아니다.','accent'),
  ],
  'aside':{'title':'Kruisdijk 2007','stat':[('70%','BoNT-A군 (14/20)'),('31.6%','위약군 (6/19)'),('P=0.03','군간 차이')]}},

 # ---- 주사 ① 술기 ----
 {'t':'bullets','eyebrow':'치료 · 주사 · 술기','tag':('보툴리눔',''),'title':'① 보툴리눔 — 어디에 · 얼마나 · 무엇을 조심하나','foot':'Kruisdijk 2007; Toxins 2021 리뷰; 유도법 비교 2024 (PMID 38336523)','items':[
   (0,'<b>표적은 근육 목록이 아니라 "이상 자세 패턴"으로 정한다:</b>',''),
   (1,'손목 굴곡·편위 → <b>FCR·FCU</b> · 손가락 굴곡 → <b>FDS·FDP</b>',''),
   (1,'엄지 굴곡·내전 → <b>FPL·무지내전근</b> · 검지 벌림 → <b>제1배측골간근</b>',''),
   (0,'<b>용량:</b> 세션당 평균 <b>133.2 U</b>(40~240 U, 1~4개 근육) — <b>저용량부터 적정</b>.',''),
   (0,'<b>유도:</b> EMG·전기자극·초음파 — <b>초음파로 바꾼 뒤 더 낮은 용량</b>을 쓰게 됐다(2024).',''),
   (-1,'<b>부작용:</b> 일시적 손가락·손목 <b>위약</b>. 정밀 작업자에겐 <b>위약이 곧 기능 상실</b> → 사전 설명 필수.','red'),
 ]},

 # ---- 표적 지도 ----
 {'t':'figure','eyebrow':'치료 · 주사 · 위치','tag':('표적 지도',''),'title':'어디에 놓는가 — 전완·손 표적 5곳',
  'foot':'주사·충격파 표적 종합 · 모든 술기는 초음파 유도 권장',
  'svg':SVG_TARGET,'caption':''},

 # ---- 주사 ② 수압박리 ----
 {'t':'split','eyebrow':'치료 · 주사 · 포착 동반','tag':('Lv II','green'),'title':'② 정중신경 수압박리 — 5% 포도당(D5W)','foot':'Wu 2017 (Mayo Clin Proc; 무작위 이중맹검 n=49) · 경도~중등도 손목터널',
  'items':[
   (0,'<b>Wu 2017:</b> 초음파 유도 신경주위 <b>5% 포도당 5 mL 1회</b> vs 생리식염수 → <b>6개월까지</b> 통증·기능 유의 감소, <b>신경전도 호전</b>, <b>정중신경 단면적 감소</b>.','green'),
   (0,'<b>의미:</b> 스테로이드 없이 포착을 푼다 → 저림 동반 손 경련에서 <b>위험이 낮은 우선 선택지</b>.',''),
   (0,'<b>기법:</b> in-plane · <b>척측 접근</b> · 바늘 끝을 신경 <b>바깥(perineural)</b>에 두고 신경을 <b>감싸도록</b> 확산.',''),
   (-1,'<b>신경 속(intraneural) 주입은 절대 금기</b> — 신경이 부풀면 즉시 중단.','red'),
  ],
  'aside':{'title':'Wu 2017','stat':[('6개월','효과 지속 확인'),('n=49','무작위 이중맹검'),('CSA ↓','신경 단면적 감소')]}},

 # ---- 주사 ③④⑤ ----
 {'t':'bullets','eyebrow':'치료 · 주사 · 보조와 탐색','tag':('Lv IV~V','amber'),'title':'③ 척골신경 · ④ 유발점 · ⑤ 신경주위 덱사메타손','foot':'③④⑤ 모두 손 경련 직접 근거 없음 — 외삽·기전 기반','items':[
   (0,'<b>③ 척골신경(주관·기용관):</b> 4·5수지 경련·Froment 양성이면 표적. 원칙은 ②와 동일.',''),
   (0,'<b>④ 유발점 주사:</b> 전완 굴근군·무지내전근·제1배측골간근 압통점에 <b>0.25~0.5% 리도카인 0.5~1 mL</b>, 25~27 G.',''),
   (1,'근거는 <b>하지 야간경련의 유발점 주사(Kim 2015)</b>를 손으로 외삽한 것(Lv V).',''),
   (0,'<b>⑤ 신경주위 덱사메타손(탐색적):</b> 신경 주위 항염이 방전 역치를 올릴 수 있다 — 단 <b>직접 근거는 없다</b>.',''),
   (-1,'<b>공통 안전:</b> 손은 신경·건·혈관이 밀집 → 무균술·초음파 유도·흡인 확인·혈종 주의.','red'),
 ]},

 # ---- 경구약제 ----
 {'t':'table','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'경구 약제 — 안전한 것부터, 대부분은 외삽','foot':'AAN(Katzberg 2010); Cochrane 종합; ALS 경련 RCT',
  'headers':['약제','근거','수준','평가'],'rows':[
   ['비타민 B 복합','Chan 1998 RCT(하지경련)','<b>II(간접)</b>','안전 → 우선 시도'],
   ['Mexiletine','Weiss 2016 RCT: 빈도 위약의 <b>31%</b>','<b>II(간접)</b>','진성 경련형 · 심전도'],
   ['Carbamazepine·Gabapentin','CFS 후향 — 반응 <b>70%·77%</b>','<b>IV</b>','잔떨림 동반 경련에'],
   ['Trihexyphenidyl','고용량 항콜린(전신형)','<b>IV</b>','국소형 반응 <b>10~20%</b>'],
   ['마그네슘','Garrison 2020 Cochrane','<b>I</b>','무효 — <b>권고 안 함</b>'],
   ['Quinine','El-Tawil 2015 Cochrane','<b>I</b>','효과O·TTP → <b>최후</b>'],
  ],
  'note':'＊<b>손 경련 경구약제 RCT는 사실상 없다.</b> 약보다 먼저 <b>Ca·Mg·갑상선·유발 약물</b>을 교정한다.'},

 # ---- 비약물 ----
 {'t':'bullets','eyebrow':'치료 · 비약물','tag':('FTSD의 절반','ink'),'title':'주사만으로 끝나지 않는다 — 도구 개조와 재훈련','foot':'Zeuner 2008 (Mov Disord, 무작위); 재활 체계적 고찰 2021 (PMID 33619945)','items':[
   (0,'<b>도구·자세 개조:</b> 굵고 마찰 있는 필기구 · <b>손잡이 굵은 수저·포크</b> · <b>파지압 낮추기</b> · 작업 중 휴식. 위험이 없고 <b>오늘 바로 적용</b>된다.',''),
   (0,'<b>감각 트릭 활용:</b> 환자가 이미 찾아낸 완화 동작을 치료에 편입.',''),
   (0,'<b>Zeuner 2008(무작위):</b> <b>8주 재훈련이 이긴장증을 개선</b>했고, 훈련이 <b>반드시 과제특이적일 필요는 없었다</b>(퍼티 훈련도 동등).','green'),
   (-1,'주사는 <b>재훈련이 가능해지는 창(window)</b>을 열어주는 역할 — 병용이 단독보다 낫다는 예비연구.','accent'),
 ]},

 # ---- 진료 순서 제안 ----
 {'t':'bullets','eyebrow':'실제 적용 · 제안','tag':('초안','ink'),'title':'진료 순서 제안 — 확정 전 검토','foot':'＊NLC 덱의 "나의 실제 진료 순서"에 대응하는 자리 · 실제 프로토콜로 교체 필요','items':[
   (0,'<b>① 재현 관찰 + 적색기 배제</b> — 동작 촬영, 위약·위축·잔떨림이면 신경과.',''),
   (0,'<b>② 기본 검사</b> — 혈액(Ca·Mg·TSH·HbA1c) + <b>NCS/EMG</b> + 초음파.',''),
   (0,'<b>③ 포착 소견 있으면</b> — <b>정중신경 D5W 수압박리</b>(±ESWT).','green'),
   (0,'<b>④ 과제특이 이긴장증이면</b> — <b>저용량 보툴리눔</b> + <b>도구 개조·재훈련</b>.','green'),
   (0,'<b>⑤ 과사용·근막 우세면</b> — <b>ESWT(전완 굴근군)</b> + 유발점 주사.','green'),
   (-1,'<b>⑥ 약물</b> — 비타민 B 먼저 · 잔떨림 동반이면 carbamazepine·gabapentin · 진성 경련형이면 mexiletine · <b>마그네슘은 결핍 시에만</b>.','accent'),
 ]},

 # ---- key ----
 {'t':'key','eyebrow':'요약 · 손 경련','headline':'"언제 나는가"가 진단이다','msgs':[
   ('감별','쓰기·젓가락질에서만 → 이긴장증. 야간 저림 → 포착. 잔떨림·위약 → 신경과.'),
   ('먼저','가역적 원인(Ca·Mg·갑상선·약물·포착)부터 교정한다.'),
   ('주사','보툴리눔이 유일한 위약대조 RCT. 포착 동반이면 D5W 수압박리.'),
   ('ESWT','직접 RCT 없음 — 인접 근거 + 무해성 → 보조·병용.'),
   ('빠뜨리지 말 것','FTSD면 도구 개조와 재훈련을 반드시 함께.'),
 ]},

 # ---- refs 1 ----
 {'t':'refs','title':'참고문헌 (1/2) — 이긴장증 · 주사 · 충격파','refs':[
   ('<b>Stahl & Frucht.</b> Focal task specific dystonia: a review and update. J Neurol. 2017.',PM(28039522)),
   ('<b>Torres-Russotto & Perlmutter.</b> Focal dystonias of the hand and upper extremity. 2008.',PM(18984354)),
   ('<b>Karp.</b> A practical approach to management of focal hand dystonia. 2015.',PM(26019409)),
   ('<b>Kruisdijk.</b> Botulinum toxin for writer\'s cramp: randomised, placebo-controlled trial. JNNP. 2007.','https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2117645/'),
   ('<b>Botulinum toxin therapy in writer\'s cramp and musician\'s dystonia.</b> Toxins. 2021.','https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8708945/'),
   ('<b>Guidance method and BoNT doses in writer\'s cramp.</b> Rev Neurol (Paris). 2024.',PM(38336523)),
   ('<b>Trompetto.</b> External shock waves therapy in dystonia. Eur J Neurol. 2009.',PM(19187259)),
   ('<b>Cabanas-Valdés.</b> ESWT for upper limb spasticity after stroke: SR & MA. Clin Rehabil. 2020.','https://doi.org/10.1177/0269215520932196'),
   ('<b>Chen.</b> ESWT provides limited effects on carpal tunnel syndrome: SR & MA. Medicina. 2022.','https://doi.org/10.3390/medicina58050677'),
   ('<b>Radial ESWT vs local corticosteroid injection in CTS: RCT.</b> 2022.',PM(35706121)),
   ('<b>Wu.</b> Six-month efficacy of perineural dextrose for CTS: RCT. Mayo Clin Proc. 2017.','https://doi.org/10.1016/j.mayocp.2017.05.025'),
   ('<b>Kim.</b> Trigger point injections on nocturnal calf cramps. J Am Board Fam Med. 2015.',PM(25567819)),
 ]},

 # ---- refs 2 ----
 {'t':'refs','title':'참고문헌 (2/2) — 경련 기전 · 약제 · 재훈련','refs':[
   ('<b>Miller & Layzer.</b> Muscle cramps. Muscle Nerve. 2005.',PM(15902691)),
   ('<b>Minetto.</b> Origin and development of muscle cramps. Exerc Sport Sci Rev. 2013.',PM(23038243)),
   ('<b>Ahmed & Simmons.</b> Peripheral nerve hyperexcitability syndromes. Muscle Nerve. 2017.',PM(28968370)),
   ('<b>Harrison.</b> Repetitive nerve stimulation for cramp-fasciculation syndrome. 2007.',PM(17405138)),
   ('<b>Peripheral nerve hyperexcitability in muscle cramping: retrospective review.</b> 2016.',PM(27258601)),
   ('<b>Weiss.</b> Randomized trial of mexiletine in ALS: muscle cramps. Neurology. 2016.',PM(26911633)),
   ('<b>Oskarsson.</b> Mexiletine for muscle cramps in ALS: crossover RCT. Muscle Nerve. 2018.',PM(29510461)),
   ('<b>El-Tawil.</b> Quinine for muscle cramps. Cochrane. 2015.',PM(25842375)),
   ('<b>Garrison.</b> Magnesium for skeletal muscle cramps. Cochrane. 2020.',PM(32956536)),
   ('<b>Chan.</b> Vitamin B complex for nocturnal leg cramps: RCT. 1998.',PM(11301568)),
   ('<b>Katzberg (AAN).</b> Symptomatic treatment for muscle cramps: evidence-based review. 2010.',PM(20177124)),
   ('<b>Zeuner.</b> Motor re-training does not need to be task specific to improve writer\'s cramp. Mov Disord. 2008.','https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4149415/'),
   ('<b>Evidence of rehabilitation therapy in task-specific focal dystonia: SR.</b> 2021.',PM(33619945)),
 ]},
]

TITLE = "손 경련(손에 쥐가 남) · 문헌고찰 발표 · v1.0"
BASE = "/home/user/ppt-work/문헌고찰_손경련"

# 이 덱은 표·항목이 NLC보다 촘촘해 본문 밀도를 약 5% 낮춘다(폰트 폴백까지 감안한 여백 확보).
CSS_TUNE = """
.tableS .pad{padding:4.3cqw 5.6cqw}
.tableS h2.ct{font-size:3.5cqw}
table.t{margin-top:0.5cqw}
table.t th{font-size:1.9cqw;padding:1.0cqw 1.3cqw}
table.t td{font-size:1.8cqw;padding:0.8cqw 1.3cqw;line-height:1.2}
.note{font-size:1.78cqw;margin-top:1.2cqw}
ul.b{gap:1.06cqw}
ul.b li{font-size:2.32cqw;line-height:1.24}
ul.b li.sub2{font-size:2.16cqw}
.aside ul.b li{font-size:2.04cqw}
.key .msg{padding:1.1cqw 0}
.key .msg .ml{font-size:2.34cqw}
.key .msg .md{font-size:2.08cqw}
.key h2.kh{font-size:4.5cqw;margin:1.3cqw 0 2.1cqw}
"""

htmlc = render_deck(TITLE, HAND)
htmlc = htmlc.replace('</style>', CSS_TUNE + '</style>')
htmlc = htmlc.replace(f'<div class="deckttl">{TITLE}</div>',
                      '<div class="deckttl">손 경련 · 문헌고찰 발표 · <b>v1.0</b></div>')

if EMBED_FONTS and FONTS:
    import base64, io
    from fontTools.subset import Subsetter, Options
    from fontTools.ttLib import TTFont
    vis = re.sub(r'<style.*?</style>', '', htmlc, flags=re.S)
    vis = re.sub(r'<script.*?</script>', '', vis, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    chars = set(vis)
    chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
                 ".,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@")
    text = ''.join(sorted(chars))
    print("glyphs:", len(chars))
    for ph, (path, locals_) in FONTS.items():
        o = Options(); o.flavor = 'woff2'; o.desubroutinize = True
        o.name_IDs = []; o.name_legacy = False; o.name_languages = []
        f = TTFont(path); s = Subsetter(options=o); s.populate(text=text); s.subset(f)
        buf = io.BytesIO(); f.save(buf)
        uri = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
        pre = ''.join(f'local("{n}"),' for n in locals_)
        htmlc = htmlc.replace(f'url({ph})', pre + f'url({uri})')
    # Pretendard가 없는 PC에서도 폴백이 한글 폰트가 되도록 스택 보강
    htmlc = htmlc.replace('font-family:Pretendard,system-ui,sans-serif',
                          'font-family:Pretendard,' + FONT_STACK)
else:
    htmlc = re.sub(r'@font-face\{font-family:Pretendard;[^}]*\}', '', htmlc)
    htmlc = htmlc.replace('font-family:Pretendard,system-ui,sans-serif', 'font-family:Pretendard,' + FONT_STACK)

os.makedirs(BASE, exist_ok=True)
out = os.path.join(BASE, "손경련_발표_웹_v1.0.html")
open(out, 'w', encoding='utf-8').write(htmlc)
print("slides:", len(HAND), "| out:", out, f"{len(htmlc.encode())/1024:.0f}KB")
