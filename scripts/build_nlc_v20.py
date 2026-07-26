# -*- coding: utf-8 -*-
"""NLC 발표 웹덱 v1.1 (수정본). 사용자 지정 수정사항 반영."""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026 · v2.0"
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

# ---- SVG: FGA 근-건 구조 모식 (Pedret 레퍼런스 재현, page 13) ----
def _hatch(step=20, dx=170):
    return ''.join(f'<line x1="{c}" y1="360" x2="{c+dx}" y2="-30"/>' for c in range(-160,700,step))
SVG_FGA2 = f'''<svg viewBox="0 0 640 340" role="img" style="max-width:56cqw;max-height:37cqw;align-self:center">
 <defs>
  <clipPath id="gmc"><path d="M14 44 L392 168 L14 168 Z"/></clipPath>
  <clipPath id="solc"><path d="M14 214 L628 214 L628 322 L14 322 Z"/></clipPath>
 </defs>
 <!-- GM 비복근 내측두 -->
 <path d="M14 44 L392 168 L14 168 Z" fill="#B83B30" stroke="#7a241e" stroke-width="1.5"/>
 <g clip-path="url(#gmc)" stroke="#E7B7B0" stroke-width="2" opacity=".55">{_hatch()}</g>
 <text x="120" y="118" font-size="15" font-weight="800" fill="#fff">GM · 비복근</text>
 <!-- 건막(FGA) + 아킬레스건(AT) : 검은 선 -->
 <path d="M14 170 L556 156" fill="none" stroke="#1b1b1b" stroke-width="4.5"/>
 <path d="M556 156 L624 150" fill="none" stroke="#1b1b1b" stroke-width="7" stroke-linecap="round"/>
 <!-- 브래킷 -->
 <path d="M400 122 L400 134 L516 134 L516 122" fill="none" stroke="#33403B" stroke-width="1.8"/>
 <text x="458" y="114" text-anchor="middle" font-size="16" font-weight="900" fill="#A8352A">FGA</text>
 <path d="M524 122 L524 134 L620 134 L620 122" fill="none" stroke="#33403B" stroke-width="1.8"/>
 <text x="572" y="114" text-anchor="middle" font-size="16" font-weight="900" fill="#17232C">AT</text>
 <!-- 주사 표적 -->
 <circle cx="458" cy="162" r="8.5" fill="#A8352A"/>
 <line x1="458" y1="170" x2="458" y2="192" stroke="#A8352A" stroke-width="1.6"/>
 <text x="458" y="206" text-anchor="middle" font-size="12.5" font-weight="800" fill="#A8352A">주사 표적</text>
 <text x="320" y="196" text-anchor="middle" font-size="12" fill="#55615B">건막간 공간</text>
 <!-- soleus 가자미근 -->
 <path d="M14 214 L628 214 L628 322 L14 322 Z" fill="#B83B30" stroke="#7a241e" stroke-width="1.5"/>
 <g clip-path="url(#solc)" stroke="#E7B7B0" stroke-width="2" opacity=".55">{_hatch()}</g>
 <text x="90" y="276" font-size="15" font-weight="800" fill="#fff">soleus · 가자미근</text>
 <text x="320" y="338" text-anchor="middle" font-size="11.5" fill="#8a6d52">＊종아리 뒤 · 세로 단면 (Pedret 2020 모식)</text>
</svg>'''

NLC = [
 {'t':'title','eyebrow':'Nocturnal Leg Cramps · 문헌고찰','title':'야간 하지경련',
  'sub':'병태생리 · 주된 호소 · 근거 기반 치료','order':'ESWT · 주사기법 · 경구약제 · 우리 프로토콜','series':SERIES},

 # ---- 감별 진단 (표지 다음, 맨 앞) ----
 {'t':'table','eyebrow':'가장 먼저','tag':('감별','ink'),'title':'감별이 필요한 것들 — 밤 다리증상','foot':'감별이 치료의 출발점',
  'headers':['질환','핵심 소견'],'hlrows':[0],'rows':[
   ['<b>NLC</b> (진성 경련·표적)','<b>통증성 근수축·촉지 근경직·족배굴곡 완화·수면 중</b>'],
   ['<b>RLS</b> (하지불안)','움직임 <b>충동</b>·움직이면 <b>완화</b>·근경직 없음·저녁 악화'],
   ['<b>PAD</b>·파행','걸으면 아프고 쉬면 완화(경련과 <b>반대</b>)·ABI↓'],
   ['신경병증','저림·화끈거림·감각이상 (당뇨 등)'],
   ['정맥부전·정맥류','부종·무거움·저녁 악화'],
   ['국소 이긴장증','지속적 자세이상·특정 동작 유발 (진성 경련 아님)'],
  ],
  'note':'＊빨간 칸이 <b>NLC(우리 표적)</b> — 나머지와 반드시 구분. 원인 감별(ABI·전해질·요추영상) 선행이 치료의 출발점.'},

 # ---- Page 2: 병태생리 (쉬운 말, 명확화) ----
 {'t':'bullets','eyebrow':'병태생리','tag':('기전',''),'title':'다리 근육을 움직이는 신경이 과흥분한다','foot':'Miller & Layzer 2005; Minetto 2011·2013','items':[
   (0,'야간 하지경련 = 근육이 스스로 <b>오작동</b>해 갑자기 강하게 뭉치는 것. 근육으로 가는 <b>운동신경이 과도하게 흥분</b>해 신호를 마구 쏘아서 생긴다.',''),
   (0,'<b>발화 속도가 폭주:</b> 정상 근수축은 초당 <b>5~30번(5~30 Hz)</b>인데, 경련 땐 신경 끝에서 <b>최대 150번(150 Hz)</b>까지 마구 발화(Miller & Layzer 2005).',''),
   (0,'<b>불씨(시작)는 \'말초\':</b> 경련의 첫 발화는 <b>근육 끝의 말초 신경</b>에서 붙는다(Minetto 2011).',''),
   (-1,'이어서 <b>척수(중추)</b>가 되먹임으로 <b>부채질해 키우고 유지</b> → 말초 시작, 중추 증폭.','accent'),
   (0,'<b>(＊중추 병 아님)</b> 경련을 <b>부추기는 딴 요인</b>(전신·말초): 요추관협착·신경눌림, 정맥순환 저하, 신경병증, 전해질, 약물(흡입제·이뇨제·statin).',''),
 ]},

 # ---- Page 3: 그림 (힉스필드 이미지 + 한글 legend) ----
 {'t':'figure','eyebrow':'병태생리 · 그림으로','tag':('가속과 브레이크',''),'title':'왜 짧아진 근육에서 경련이 나나',
  'foot':'Minetto 2013 · Khan & Burne 2007',
  'svg':('<img src="__PAGE3IMG__" alt="정상 vs 경련" '
         'style="max-height:100%;max-width:62cqw;width:auto;object-fit:contain;align-self:center;border-radius:1.4cqw;border:1.5px solid #E4E9E8"/>'
         '<div style="flex:1;max-width:30cqw;display:flex;flex-direction:column;justify-content:center;gap:1.8cqw;text-align:left">'
         '<div style="font-weight:800;font-size:2.2cqw;color:#17232C">요약</div>'
         '<div style="font-weight:300;font-size:1.95cqw;line-height:1.36;color:#33403B">정상은 <b>GTO(브레이크)</b>가 켜져 척수 신호가 안정. 근육이 <b>짧아지면 브레이크가 헐거워져</b> 작은 자극에 신호가 <b>스스로 커져</b> 경련.</div>'
         '<div style="font-weight:700;font-size:1.6cqw;line-height:1.32;color:#6B7680;border-top:1.5px solid #E4E9E8;padding-top:1.3cqw">＊그림의 "꺼짐"은 정확히는 "헐거워짐"(GTO=장력 센서). 유력 모델·중추/말초 기원 논쟁 중.</div>'
         '<div style="font-weight:700;font-size:1.55cqw;color:#0B5F5E">Ref · Minetto 2013 · Khan &amp; Burne 2007</div>'
         '</div>'),
  'caption':''},

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
 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 개관','foot':'문헌고찰 종합',
  'headers':['치료','대표','야간경련 근거','근거수준'],'rows':[
   ['ESWT','종아리 표적 충격파','Li 2021 (후향)','<b>III</b>'],
   ['주사','국소마취제 유발점','Kim 2015·Prateepavanich 1999','<b>II</b>'],
   ['주사','심비골신경 내측분지 차단','Imura 2015 <b>직접근거</b>','<b>II</b>'],
   ['주사','보툴리눔(비복근)','Park 2017 RCT','<b>II</b>'],
   ['경구약제','비타민 B·K2 → diltiazem','Chan·Tan·Voon RCT','<b>II</b>'],
  ],
  'note':'＊탐색적(Lv V) 주사(신경주위 덱사메타손·FGA)는 뒤 슬라이드 참조. 근거수준은 연구 설계 기준(I~V).'},

 # ---- Page 6: Li 2021 — 충격파를 어떻게 놓았나 ----
 {'t':'split','eyebrow':'치료 · ESWT · 직접근거','tag':('Lv III','amber'),'title':'Li 2021 — 충격파를 어떻게 놓았나','foot':'Li 2021 (Biomed Res Int; PMID 34734084) · 후향적 연구',
  'items':[
   (0,'<b>대상:</b> 요추 퇴행성질환에 동반된 하지경련 환자 <b>126명</b>(후향적 분석).',''),
   (0,'<b>방법:</b> <b>종아리(비복근) 표적</b>으로 1회 <b>2,000타(shocks)</b>, <b>2일 간격</b>, <b>4주간</b> 반복.',''),
   (-1,'경련을 <b>직접</b> 평가한 유일한 임상연구 — 단 후향적이라 근거등급은 제한적. (결과는 오른쪽 카드)','accent'),
  ],
  'aside':{'title':'Li 2021 결과 (ESWT군)','stat':[('5.7→1.3','경련 빈도 (회/시간)'),('57.6→10.6','지속 (초)'),('P<0.001','대조군 대비')]}},

 # ---- (Otero-Luis 슬라이드 삭제 — 본주제와 안 맞음) ----
 # ---- ESWT 기전·한계 (표준 프로토콜 제거, bullets) ----
 {'t':'bullets','eyebrow':'치료 · ESWT','tag':('기전',''),'title':'충격파는 어떻게 듣나 · 한계','foot':'Yang 2021 (J Clin Med, 기전 리뷰)','items':[
   (0,'<b>기전 (Yang 2021) — 충격파가 과흥분을 4가지로 가라앉힌다:</b>',''),
   (1,'① 신경-근육 접합부 <b>리모델링</b> (ACh 수용체↓ → CMAP 6~8주 감소)',''),
   (1,'② <b>운동신경 흥분성 낮춤</b>',''),
   (1,'③ <b>산화질소(NO) 합성 증가</b>',''),
   (1,'④ <b>혈류·미세순환 개선</b>',''),
   (-1,'<b>한계:</b> 특발성 경련만 본 RCT 없음 · 효과 대개 <b>12주 이내 단기</b> → 보조·근거형성 단계.','accent'),
 ]},

 # ---- Page 8: ① 유발점 주사 (상세) ----
 {'t':'split','eyebrow':'치료 · 주사기법','tag':('Lv II','green'),'title':'① 국소마취제 유발점 주사','foot':'Kim 2015 (J Am Board Fam Med)',
  'items':[
   (0,'개념: 비복근 <b>유발점(MTrP)</b>의 최대 압통점에 소량 국소마취제 → 국소 근이완·유발점 비활성화.',''),
   (0,'<b>대상:</b> 야간 종아리경련 <b>12명</b>(전향·대조군 없음).',''),
   (0,'<b>약제·바늘:</b> 0.25% 리도카인 <b>1–2 mL</b> · <b>25 G</b>·30° → taut band 최대 압통점(비복근 내측두).',''),
   (0,'<b>확인·반복:</b> twitch·주입 전 흡인 · <b>주 1회</b> · 초음파 유도.',''),
  ],
  'aside':{'title':'결과 (Kim 2015, n=12)','items':[
   (0,'<b>NRS·경련 빈도·불면(ISI)</b> 모두 유의 감소',''),
   (0,'1·2·4주 <b>전 시점 P&lt;0.01</b>',''),
   (-1,'임상 불면 환자: <b>10 → 3(2주) → 1명(4주)</b>','green'),
   (0,'(P=0.012 · 0.001)',''),
  ]}},

 # ---- Page 9(구): dry needling 제거 ----

 # ---- ② 심비골신경 차단 (부위 명확화) ----
 {'t':'split','eyebrow':'치료 · 주사기법 · 직접근거','tag':('Lv II','green'),'title':'② 심비골신경 내측분지 차단','foot':'Imura 2015 (Brain Behav; PMID 26445706)',
  'items':[
   (0,'<b>Imura 2015:</b> 야간경련에 <b>말초 운동신경가지를 직접 표적</b>한 유일한 전향적 비교연구(n=66).',''),
   (0,'<b>어디를:</b> 발등 <b>제1–2 중족골 사이 원위 2/3</b>. 1.0% 리도카인 <b>5.0 mL</b>, 깊이 1.0–1.5 cm.',''),
   (-1,'<b>왜 발등 찌르는데 종아리가 풀리나:</b> 경련은 <b>빙빙 도는 신호 고리</b>로 유지 → 발 감각이 그 고리의 한 축. <b>신경을 끊으면 고리가 멈춰</b> 종아리도 풀림(근육 마비 아님).','accent'),
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
   (0,'<b>치료 근거:</b> 경련을 유지하는 건 운동신경 과흥분 → 그 근육을 지배하는 <b>신경 줄기 주위</b>에 덱사메타손을 두면 이소성 과흥분·신경주위 염증을 눌러 경련 역치를 올릴 수 있다.',''),
   (0,'<b>표적 신경 = 경련 부위로 정한다:</b>',''),
   (1,'<b>후경골신경</b> → <b>종아리 후측 경련</b> (오금~족근관 접근)',''),
   (1,'<b>총비골신경</b> → <b>정강이 외측·발 경련</b> (비골두 뒤 접근)',''),
   (-1,'덱사메타손은 말초신경차단의 <b>검증된 보조제</b>(진통 연장·항염). 단 경련 직접근거 <b>없음</b> → 기전기반 <b>Lv V</b>.','accent'),
   (0,'안전: 초음파로 <b>신경 바깥(perineural)에만</b> — 신경 속(intraneural) 금기 · <b>국소마취제와 혼합 금지</b> · 총비골 차단 시 족하수 주의.','red'),
 ]},

 # ---- (신경 초음파 단면 그림 삭제) ----

 # ---- ⑤ FGA 주사 — 개념·근거 (1/2) ----
 {'t':'bullets','eyebrow':'치료 · 주사기법 · 탐색적','tag':('Lv V','amber'),'title':'⑤ FGA 주사 — 어디를·왜 (1/2)','foot':'Pedret 2020 (Scand J Med Sci Sports); Balius 2018','items':[
   (0,'<b>표적(FGA):</b> 비복근 <b>근섬유가 끝나고 힘줄로 바뀌는 바로 그 지점</b> = 원위 근-건 이행부(임상적으로 <b>tennis leg</b>가 생기는 자리).',''),
   (0,'<b>왜 하필 여기?</b> 이 자리에 <b>브레이크 센서(GTO)·근방추가 가장 몰려</b> 있다 — 경련을 껐다 켜는 <b>스위치가 밀집</b>한 곳.',''),
   (0,'<b>발상(직관):</b> 비복근에 <b>대충 국소주사(유발점·보툴리눔)만 해도 야간경련이 줄었으니</b> → 스위치가 몰린 <b>이 지점을 콕 집으면</b> 더 정밀하게 들을 것이라는 생각.',''),
   (-1,'<b>단, 직접 근거는 아직 없음 → 신규 가설(Lv V).</b> 표준치료 아님, 연구 틀 안에서.','red'),
 ]},

 # ---- FGA 초음파 술기 (2/2, 실제 초음파) ----
 {'t':'figure','eyebrow':'치료 · 주사기법 · 술기','tag':('초음파 술기',''),'title':'⑤ FGA 주사 — 초음파 술기 (2/2)','foot':'김형기(그림)·김우선(영상) 원장 · 실제 초음파 (PPT 전환 시 동영상 삽입)',
  'svg':('<img src="__FGAUS__" alt="FGA 실제 초음파" '
         'style="max-height:100%;max-width:44cqw;width:auto;object-fit:contain;align-self:center;border-radius:1.2cqw;border:1.5px solid #33403B"/>'
         '<div style="flex:1;max-width:47cqw;display:flex;flex-direction:column;justify-content:center;gap:1.5cqw;text-align:left">'
         '<div style="font-weight:800;font-size:2.15cqw;color:#17232C">초음파 술기 (실제 스캔)</div>'
         '<div style="font-weight:300;font-size:1.9cqw;line-height:1.3;color:#33403B"><b>위치:</b> 종아리 뒤 <b>원위 1/3 · 내측(medial)</b></div>'
         '<div style="font-weight:300;font-size:1.9cqw;line-height:1.3;color:#33403B"><b>초음파 소견:</b> 비복근(GC) 건 바로 아래·가자미근 바로 위에 <b>1~2mm 저에코(hypoechoic) 띠</b>가 길게 = FGA</div>'
         '<div style="font-weight:300;font-size:1.9cqw;line-height:1.3;color:#33403B"><b>프로브:</b> linear·평면내(in-plane) · <b>횡단면(transverse)</b>으로 보고 진입(장축 평행 X)</div>'
         '<div style="font-weight:300;font-size:1.9cqw;line-height:1.3;color:#33403B"><b>바늘:</b> 내측을 치료하되 <b>삽입은 외측(lateral)에서</b></div>'
         '<div style="font-weight:700;font-size:1.72cqw;line-height:1.3;color:#9A6800;border-top:1.5px solid #E4E9E8;padding-top:1.2cqw"><b>시술 후:</b> 뻐근함·중압감 <b>3~4일(길면 7일)</b> — 시술 전 미리 설명</div>'
         '</div>'),
  'caption':''},

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
 {'t':'key','eyebrow':'요약 · NLC','headline':'감별이 먼저 · 기본 위에 근거순 단계적 주사','msgs':[
   ('감별','통증성 근수축·촉지 근경직·족배굴곡 완화 → RLS·PAD·신경병증과 구분.'),
   ('기본(모두)','취침 전 스트레칭 · 유발약물 검토 · 이차원인 교정이 모든 단계의 바탕.'),
   ('경구','비타민 B·K2·diltiazem(Lv II) 우선 · quinine 최후 · 마그네슘 무효.'),
   ('주사(근거순)','유발점 → 심비골신경 차단(Imura) → 보툴리눔 (모두 Lv II)이 불응성 핵심.'),
   ('탐색적(Lv V)','신경주위 덱사메타손·FGA — 기전기반, 연구 틀 안에서만.'),
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

TITLE = "야간 하지경련 · 문헌고찰 발표 · v2.0 (수정본)"
BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/01_NLC"
htmlc = render_deck(TITLE, NLC)
# 화면 하단 버전 라벨 강조
htmlc = htmlc.replace(f'<div class="deckttl">{TITLE}</div>',
                      '<div class="deckttl">야간 하지경련 · 문헌고찰 발표 · <b>v2.0 (수정본)</b></div>')
# 페이지3 힉스필드 이미지 임베드
import base64 as _b64
_p3=_b64.b64encode(open(os.path.join(BASE,"assets/page3_reflex.jpg"),'rb').read()).decode()
htmlc = htmlc.replace("__PAGE3IMG__","data:image/jpeg;base64,"+_p3)
_fu=_b64.b64encode(open(os.path.join(BASE,"assets/fga_us.jpg"),'rb').read()).decode()
htmlc = htmlc.replace("__FGAUS__","data:image/jpeg;base64,"+_fu)

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

out=os.path.join(BASE,"NLC_발표_웹_v2.0.html")
open(out,'w',encoding='utf-8').write(htmlc)
print("slides:",len(NLC),"| out:",out,f"{len(htmlc.encode())/1024:.0f}KB")
