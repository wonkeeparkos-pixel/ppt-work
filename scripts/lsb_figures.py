# -*- coding: utf-8 -*-
"""LSB 발표용 오리지널 도해(SVG). 저작권 안전(직접 제작), 한글 라벨.
AXIAL_SVG: L2·L3 축상면(axial) 조감도 — 표적(교감신경절)·방척추 바늘 접근·주변 위험구조."""

# 축상면(위에서 본 단면), 엎드린 자세: 후방(등)=위, 전방(배)=아래
AXIAL_SVG = r'''<svg viewBox="0 0 960 600" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg" font-family="Pretendard,sans-serif">
  <defs>
    <marker id="lead" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5"><circle cx="3.5" cy="3.5" r="2.2" fill="#8A96A0"/></marker>
  </defs>
  <!-- 방향 -->
  <text x="480" y="26" text-anchor="middle" font-size="17" font-weight="800" fill="#6B7680">후방 (등) · 바늘 진입</text>
  <text x="480" y="592" text-anchor="middle" font-size="17" font-weight="800" fill="#6B7680">전방 (배)</text>
  <!-- 등 피부선 -->
  <path d="M70,70 Q480,34 890,70" fill="none" stroke="#C7CDD2" stroke-width="3"/>
  <!-- 정중선 기준 -->
  <line x1="480" y1="150" x2="480" y2="560" stroke="#B7C0C7" stroke-width="1.6" stroke-dasharray="7 7"/>
  <text x="486" y="168" font-size="14" fill="#8A96A0">정중선</text>

  <!-- 척추체 -->
  <ellipse cx="480" cy="350" rx="150" ry="100" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2.4"/>
  <text x="480" y="360" text-anchor="middle" font-size="18" font-weight="800" fill="#8C8368">척추체</text>
  <text x="480" y="382" text-anchor="middle" font-size="13.5" fill="#A79C82">(L2–L3)</text>

  <!-- 횡돌기 -->
  <polygon points="335,305 205,278 210,306 340,326" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2"/>
  <polygon points="625,305 755,278 750,306 620,326" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2"/>
  <text x="248" y="268" font-size="14.5" fill="#8C8368">횡돌기</text>

  <!-- 극돌기 + 척수강 -->
  <polygon points="464,258 496,258 490,150 470,150" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2"/>
  <circle cx="480" cy="268" r="40" fill="#F7F8F6" stroke="#C7BFAE" stroke-width="2.2"/>
  <g fill="#9AA6AD"><circle cx="470" cy="260" r="4"/><circle cx="491" cy="262" r="4"/><circle cx="466" cy="277" r="4"/><circle cx="486" cy="280" r="4"/><circle cx="479" cy="269" r="4"/></g>
  <text x="480" y="120" text-anchor="middle" font-size="14.5" fill="#8A96A0">척수강 · 경막낭</text>

  <!-- 추간공 (경막외 확산 주의) -->
  <ellipse cx="612" cy="318" rx="16" ry="12" fill="#FBEFEC" stroke="#A8352A" stroke-width="2" stroke-dasharray="4 3"/>
  <line x1="628" y1="315" x2="742" y2="300" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#lead)"/>
  <text x="748" y="298" font-size="14.5" fill="#A8352A" font-weight="700">추간공</text>
  <text x="748" y="316" font-size="12.5" fill="#A8352A">경막외 확산 주의</text>

  <!-- 대요근(psoas) -->
  <ellipse cx="352" cy="438" rx="80" ry="62" fill="#E6C7C1" stroke="#CC9E96" stroke-width="2"/>
  <ellipse cx="608" cy="438" rx="80" ry="62" fill="#E6C7C1" stroke="#CC9E96" stroke-width="2"/>
  <text x="352" y="470" text-anchor="middle" font-size="15" fill="#B07C73" font-weight="700">대요근</text>
  <text x="352" y="489" text-anchor="middle" font-size="12.5" fill="#B07C73">(psoas)</text>

  <!-- 교감신경절: 좌(연함) / 우(표적) -->
  <circle cx="360" cy="410" r="8" fill="#0E7C7B" opacity="0.45"/>
  <circle cx="604" cy="408" r="17" fill="none" stroke="#0E7C7B" stroke-width="3"/>
  <circle cx="604" cy="408" r="8" fill="#0E7C7B"/>
  <line x1="620" y1="404" x2="726" y2="392" stroke="#0E7C7B" stroke-width="1.4" marker-end="url(#lead)"/>
  <text x="732" y="390" font-size="15.5" fill="#0B5F5E" font-weight="800">교감신경절 (표적)</text>
  <text x="732" y="409" font-size="12.5" fill="#0B5F5E">척추체 전외측 · L2하–L3상</text>

  <!-- 바늘: 방척추 접근 -->
  <polyline points="852,64 726,214 660,318 604,408" fill="none" stroke="#3E4A55" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>
  <rect x="838" y="44" width="40" height="20" rx="3" transform="rotate(50 858 54)" fill="#5A6B7B" stroke="#3E4A55" stroke-width="1.5"/>
  <circle cx="604" cy="408" r="4.5" fill="#A8352A"/>
  <text x="742" y="150" font-size="14.5" fill="#3E4A55" font-weight="700">C-arm 사위 30–35° · 동축 진입</text>
  <text x="742" y="168" font-size="12.5" fill="#6B7680">척추체 외측면 접촉 → 전내측 walk</text>
  <!-- 7cm 브래킷 -->
  <line x1="480" y1="96" x2="852" y2="96" stroke="#8A96A0" stroke-width="1.3"/>
  <line x1="480" y1="90" x2="480" y2="102" stroke="#8A96A0" stroke-width="1.3"/>
  <line x1="852" y1="90" x2="852" y2="102" stroke="#8A96A0" stroke-width="1.3"/>
  <text x="666" y="88" text-anchor="middle" font-size="13.5" fill="#6B7680">정중선에서 약 7 cm 외측</text>

  <!-- 대동맥 / IVC (전방) -->
  <circle cx="405" cy="516" r="35" fill="#C0504D" stroke="#9B3F3C" stroke-width="2"/>
  <text x="405" y="521" text-anchor="middle" font-size="14" fill="#fff" font-weight="800">대동맥</text>
  <text x="405" y="566" text-anchor="middle" font-size="12.5" fill="#9B3F3C">(좌)</text>
  <ellipse cx="537" cy="520" rx="35" ry="29" fill="#5A7C9C" stroke="#47617B" stroke-width="2"/>
  <text x="537" y="518" text-anchor="middle" font-size="13" fill="#fff" font-weight="800">IVC</text>
  <text x="537" y="536" text-anchor="middle" font-size="11.5" fill="#fff">하대정맥</text>
  <text x="537" y="566" text-anchor="middle" font-size="12.5" fill="#47617B">(우)</text>

  <!-- 신장 / 요관 -->
  <path d="M165,300 Q120,350 165,400 Q205,388 200,350 Q205,312 165,300 Z" fill="#C98B6B" stroke="#A9744F" stroke-width="2"/>
  <text x="150" y="430" text-anchor="middle" font-size="14.5" fill="#8F6142" font-weight="700">신장</text>
  <circle cx="300" cy="500" r="10" fill="#DCC079" stroke="#B79A4E" stroke-width="1.8"/>
  <line x1="290" y1="500" x2="232" y2="516" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#lead)"/>
  <text x="150" y="520" font-size="14.5" fill="#9A7B2E" font-weight="700">요관</text>

  <!-- 생식대퇴신경 (핵심 위험) -->
  <circle cx="616" cy="474" r="8.5" fill="#E0A800" stroke="#9A6800" stroke-width="2"/>
  <line x1="624" y1="480" x2="726" y2="500" stroke="#8A96A0" stroke-width="1.3" marker-end="url(#lead)"/>
  <text x="732" y="498" font-size="15" fill="#9A6800" font-weight="800">생식대퇴신경</text>
  <text x="732" y="517" font-size="12.5" fill="#9A6800">psoas 전면 — 신경파괴 시 회피</text>
</svg>'''


# ============================================================
# 조영제 확산 읽기 (AP 투시 도식): 안전 1 + 위험 3 패널
# ============================================================
def _spine(cx, top):
    """AP 척추 3분절(둥근 사각) + 극돌기 수직선 + 페디클 눈."""
    s = ''
    for i in range(3):
        y = top + i * 62
        s += f'<rect x="{cx-46}" y="{y}" width="92" height="52" rx="10" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2"/>'
        s += f'<circle cx="{cx-24}" cy="{y+26}" r="7.5" fill="none" stroke="#C7BFAE" stroke-width="2"/>'
        s += f'<circle cx="{cx+24}" cy="{y+26}" r="7.5" fill="none" stroke="#C7BFAE" stroke-width="2"/>'
    s += f'<line x1="{cx}" y1="{top-6}" x2="{cx}" y2="{top+3*62+2}" stroke="#C7BFAE" stroke-width="2.4"/>'
    return s

def _panel(x, ok, title, sub, body):
    fr = '#CFE3D2' if ok else '#E7CFC9'
    bg = '#F1F7F1' if ok else '#FCF4F2'
    badge = '#2E7D32' if ok else '#A8352A'
    mark = '✓' if ok else '✕'
    return f'''<g>
  <rect x="{x}" y="20" width="222" height="424" rx="16" fill="{bg}" stroke="{fr}" stroke-width="2"/>
  <circle cx="{x+30}" cy="52" r="15" fill="{badge}"/>
  <text x="{x+30}" y="58" text-anchor="middle" font-size="18" font-weight="900" fill="#fff">{mark}</text>
  <text x="{x+52}" y="50" font-size="17" font-weight="800" fill="{badge}">{title}</text>
  <text x="{x+52}" y="70" font-size="12.5" fill="#5A6B7B">{sub}</text>
  {body}
</g>'''

CONTRAST_SVG = ('<svg viewBox="0 0 960 470" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" '
  'xmlns="http://www.w3.org/2000/svg" font-family="Pretendard,sans-serif">'
  # P1 안전: 두미측 종방향
  + _panel(16, True, '종방향 확산', '안전 — 진행',
      _spine(96, 130)
      + '<path d="M132,120 Q150,220 132,320 Q120,220 132,120 Z" fill="#0E7C7B" opacity="0.5"/>'
      + '<line x1="205" y1="120" x2="150" y2="180" stroke="#3E4A55" stroke-width="4" stroke-linecap="round"/>'
      + '<text x="127" y="405" text-anchor="middle" font-size="13" fill="#2E7D32" font-weight="700">위·아래로 길게</text>'
      + '<text x="127" y="424" text-anchor="middle" font-size="12" fill="#5A6B7B">척추체 전외측 층 확산</text>')
  # P2 위험: 혈관내
  + _panel(254, False, '혈관 음영', '위험 — 씻겨나감',
      _spine(334, 130)
      + '<path d="M372,120 C400,150 360,190 392,230 C360,270 400,300 372,330" fill="none" stroke="#B03A2E" stroke-width="3.5" stroke-dasharray="2 5" opacity="0.85"/>'
      + '<path d="M372,175 L410,168 M388,235 L424,244 M372,300 L408,312" stroke="#B03A2E" stroke-width="2.4" opacity="0.7"/>'
      + '<line x1="443" y1="120" x2="388" y2="180" stroke="#3E4A55" stroke-width="4" stroke-linecap="round"/>'
      + '<text x="365" y="405" text-anchor="middle" font-size="13" fill="#A8352A" font-weight="700">가늘게 흐르며 사라짐</text>'
      + '<text x="365" y="424" text-anchor="middle" font-size="12" fill="#5A6B7B">→ 흡인·재위치, 재확인</text>')
  # P3 위험: 경막외/추간공
  + _panel(492, False, '경막외·수평', '위험 — 후방/중심',
      _spine(572, 130)
      + '<ellipse cx="572" cy="222" rx="58" ry="26" fill="#9A6800" opacity="0.4"/>'
      + '<path d="M540,222 L512,222 M604,222 L632,222" stroke="#9A6800" stroke-width="3" opacity="0.7"/>'
      + '<line x1="681" y1="120" x2="612" y2="200" stroke="#3E4A55" stroke-width="4" stroke-linecap="round"/>'
      + '<text x="565" y="405" text-anchor="middle" font-size="13" fill="#9A6800" font-weight="700">중심·양옆 수평 확산</text>'
      + '<text x="565" y="424" text-anchor="middle" font-size="12" fill="#5A6B7B">바늘 너무 후방 → 재위치</text>')
  # P4 위험: 근육내(psoas)
  + _panel(730, False, '근육내(psoas)', '위험 — 깃털형',
      _spine(810, 130)
      + '<g fill="#B85C4A" opacity="0.5">'
      + '<path d="M864,150 q22,10 6,26 q22,6 4,24 q22,8 4,24 q20,6 2,22"/>'
      + '<ellipse cx="880" cy="200" rx="26" ry="46"/></g>'
      + '<line x1="919" y1="120" x2="866" y2="182" stroke="#3E4A55" stroke-width="4" stroke-linecap="round"/>'
      + '<text x="820" y="405" text-anchor="middle" font-size="13" fill="#A8352A" font-weight="700">줄무늬·깃털 확산</text>'
      + '<text x="820" y="424" text-anchor="middle" font-size="12" fill="#5A6B7B">근육내 → 전외측으로 재위치</text>')
  + '</svg>')


# ============================================================
# 생식대퇴신경통: 왜 L2가 L4보다 안전한가 (축상 2패널)
# ============================================================
def _mini_axial(cx, cy, gf_exposed, needle_ok):
    """소형 축상: 척추체 + 좌우 psoas + 교감표적 + 생식대퇴신경(노출 여부)."""
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="72" ry="50" fill="#ECE7DB" stroke="#C7BFAE" stroke-width="2"/>'
    s += f'<ellipse cx="{cx-92}" cy="{cy+44}" rx="46" ry="36" fill="#E6C7C1" stroke="#CC9E96" stroke-width="1.8"/>'
    s += f'<ellipse cx="{cx+92}" cy="{cy+44}" rx="46" ry="36" fill="#E6C7C1" stroke="#CC9E96" stroke-width="1.8"/>'
    # 교감 표적 (우 전외측)
    s += f'<circle cx="{cx+70}" cy="{cy+30}" r="12" fill="none" stroke="#0E7C7B" stroke-width="2.6"/><circle cx="{cx+70}" cy="{cy+30}" r="6" fill="#0E7C7B"/>'
    # 바늘
    tipy = cy + 30
    s += f'<line x1="{cx+190}" y1="{cy-70}" x2="{cx+70}" y2="{tipy}" stroke="#3E4A55" stroke-width="4.5" stroke-linecap="round"/>'
    # 약물 blob
    if gf_exposed:
        s += f'<ellipse cx="{cx+82}" cy="{cy+46}" rx="34" ry="24" fill="#B03A2E" opacity="0.32"/>'
        s += f'<path d="M{cx+96},{cy+40} q18,10 6,26" fill="none" stroke="#B03A2E" stroke-width="2.4" marker-end="url(#lead)"/>'
        # GF nerve on psoas anterior — 노출
        s += f'<circle cx="{cx+104}" cy="{cy+64}" r="9" fill="#E0A800" stroke="#9A6800" stroke-width="2.4"/>'
        s += f'<text x="{cx+120}" y="{cy+70}" font-size="13" fill="#9A6800" font-weight="800">생식대퇴신경 노출</text>'
    else:
        s += f'<ellipse cx="{cx+72}" cy="{cy+30}" rx="20" ry="15" fill="#0E7C7B" opacity="0.3"/>'
        s += f'<circle cx="{cx+96}" cy="{cy+70}" r="8" fill="#E0A800" stroke="#9A6800" stroke-width="2" opacity="0.5"/>'
        s += f'<text x="{cx+112}" y="{cy+76}" font-size="12.5" fill="#9A6800">신경 미노출</text>'
    return s

GF_SVG = ('<svg viewBox="0 0 900 470" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" '
  'xmlns="http://www.w3.org/2000/svg" font-family="Pretendard,sans-serif">'
  '<defs><marker id="lead" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5"><circle cx="3.5" cy="3.5" r="2.2" fill="#B03A2E"/></marker></defs>'
  # 패널 A: L2 안전
  '<rect x="16" y="22" width="420" height="426" rx="18" fill="#F1F7F1" stroke="#CFE3D2" stroke-width="2"/>'
  '<text x="42" y="62" font-size="21" font-weight="900" fill="#2E7D32">L2 시행</text>'
  '<text x="150" y="62" font-size="19" font-weight="900" fill="#2E7D32">생식대퇴신경차단 0%</text>'
  + _mini_axial(190, 150, False, True)
  + '<text x="226" y="410" text-anchor="middle" font-size="14" fill="#33403B">신경이 아직 psoas 속 → 약물에 잘 노출 안 됨</text>'
  # 패널 B: L4 위험
  + '<rect x="464" y="22" width="420" height="426" rx="18" fill="#FCF4F2" stroke="#E7CFC9" stroke-width="2"/>'
  + '<text x="490" y="62" font-size="21" font-weight="900" fill="#A8352A">L4 시행</text>'
  + '<text x="600" y="62" font-size="19" font-weight="900" fill="#A8352A">약 40%</text>'
  + _mini_axial(636, 150, True, False)
  + '<text x="674" y="410" text-anchor="middle" font-size="14" fill="#33403B">신경이 psoas 전면으로 나옴 + 약물 역류 → 자극</text>'
  + '</svg>')


# ============================================================
# 측면도(lateral/sagittal 모식도): L2–L4 · 교감신경사슬 · 바늘 접근 · 척수신경 분지
# ============================================================
_BONE, _BONE_S = '#ECE7DB', '#C7BFAE'
_DISC, _DISC_S = '#C3D7E8', '#9DB6CD'
_NRV,  _NRV_S  = '#F0DB90', '#B9973F'

def _sag_level(yb, label):
    s = ''
    s += f'<rect x="300" y="{yb}" width="152" height="90" rx="10" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2.2"/>'
    s += f'<ellipse cx="232" cy="{yb+42}" rx="45" ry="35" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2"/>'
    s += f'<rect x="258" y="{yb+26}" width="50" height="32" rx="9" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2"/>'
    s += f'<polygon points="197,{yb+24} 148,{yb+36} 148,{yb+62} 197,{yb+60}" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2"/>'
    s += f'<text x="376" y="{yb+80}" text-anchor="middle" font-size="21" font-weight="800" fill="#8C8368">{label}</text>'
    return s

def _sag_nerves(yb):
    """후근신경절 + 후/전 일차분지 + 내측분지 + 교통가지."""
    g = yb + 98                      # 신경 출구(추간공) 높이
    s = ''
    # 전방일차분지 → 교감사슬 방향
    s += f'<path d="M272,{g} C330,{g+6} 400,{g+16} 458,{g+10}" fill="none" stroke="{_NRV}" stroke-width="9" stroke-linecap="round"/>'
    s += f'<path d="M272,{g} C330,{g+6} 400,{g+16} 458,{g+10}" fill="none" stroke="{_NRV_S}" stroke-width="1.2" opacity=".55"/>'
    # 교통가지 (사슬로 연결)
    s += f'<path d="M430,{g+14} C450,{g+12} 462,{g+4} 470,{g-8}" fill="none" stroke="{_NRV}" stroke-width="6" stroke-linecap="round"/>'
    # 후방일차분지
    s += f'<path d="M258,{g-4} C232,{g+6} 214,{g+16} 196,{g+14}" fill="none" stroke="{_NRV}" stroke-width="8" stroke-linecap="round"/>'
    # 내측분지 (후지에서 갈라져 관절 쪽)
    s += f'<path d="M224,{g+10} C216,{g-6} 220,{g-22} 234,{g-30}" fill="none" stroke="{_NRV}" stroke-width="5.5" stroke-linecap="round"/>'
    # 후근신경절
    s += f'<ellipse cx="268" cy="{g-4}" rx="17" ry="12" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
    return s

_chain = ''.join(
    f'<ellipse cx="478" cy="{y}" rx="13" ry="21" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
    for y in (145, 267, 389, 511))

SAGITTAL_SVG = (
 '<svg viewBox="0 0 790 640" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" '
 'xmlns="http://www.w3.org/2000/svg" font-family="Pretendard,sans-serif">'
 '<defs><marker id="ld2" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5">'
 '<circle cx="3.5" cy="3.5" r="2.2" fill="#8A96A0"/></marker></defs>'
 # 방향 표시
 '<text x="150" y="26" font-size="14" font-weight="800" fill="#6B7680">후방 (등)</text>'
 '<text x="560" y="26" font-size="14" font-weight="800" fill="#6B7680">전방 (배)</text>'
 # 위/아래 잘린 분절
 f'<rect x="300" y="44" width="152" height="56" rx="10" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2.2"/>'
 f'<rect x="300" y="466" width="152" height="60" rx="10" fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2.2"/>'
 # 디스크
 + ''.join(f'<rect x="300" y="{y}" width="152" height="32" rx="7" fill="{_DISC}" stroke="{_DISC_S}" stroke-width="2"/>'
           for y in (100, 190, 312, 434))
 # 척추 3분절
 + _sag_level(122, 'L2') + _sag_level(222, 'L3') + _sag_level(344, 'L4')
 # 교감신경사슬 (전외측 세로 주행)
 + f'<path d="M478,52 C470,140 486,200 478,268 C470,330 486,400 478,468 C474,500 478,530 478,560" '
   f'fill="none" stroke="{_NRV}" stroke-width="10" stroke-linecap="round"/>'
 + _chain
 # 신경 분지
 + _sag_nerves(122) + _sag_nerves(222) + _sag_nerves(344)
 # 표적 강조 (L3 신경절)
 + '<circle cx="478" cy="267" r="30" fill="none" stroke="#0E7C7B" stroke-width="3.4"/>'
 # 바늘 (후외측 → 전외측), 흰 halo로 '척추체 외측면 통과' 표현
 + '<line x1="24" y1="243" x2="470" y2="267" stroke="#F7F8F6" stroke-width="13" stroke-linecap="round"/>'
 + '<line x1="24" y1="243" x2="470" y2="267" stroke="#3E4A55" stroke-width="5.5" stroke-linecap="round"/>'
 + '<rect x="10" y="230" width="52" height="24" rx="5" fill="#5A6B7B" stroke="#3E4A55" stroke-width="1.6"/>'
 + '<circle cx="470" cy="267" r="5.5" fill="#A8352A"/>'
 # ---- 라벨 (좌: 후방 구조 / 우: 교감·바늘) ----
 + '<text x="12" y="284" font-size="15" font-weight="800" fill="#3E4A55">바늘</text>'
 + '<line x1="118" y1="120" x2="228" y2="196" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld2)"/>'
 + '<text x="12" y="112" font-size="14.5" font-weight="800" fill="#9A6800">후근신경절</text>'
 + '<text x="12" y="130" font-size="12" fill="#8A96A0">(DRG)</text>'
 + '<line x1="118" y1="168" x2="222" y2="212" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld2)"/>'
 + '<text x="12" y="172" font-size="14" font-weight="700" fill="#9A6800">내측분지</text>'
 + '<line x1="120" y1="452" x2="200" y2="452" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld2)"/>'
 + '<text x="12" y="440" font-size="14" font-weight="700" fill="#9A6800">후방일차분지</text>'
 + '<line x1="150" y1="536" x2="300" y2="472" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld2)"/>'
 + '<text x="12" y="548" font-size="14" font-weight="700" fill="#9A6800">전방일차분지</text>'
 + '<line x1="514" y1="252" x2="560" y2="238" stroke="#0E7C7B" stroke-width="1.4" marker-end="url(#ld2)"/>'
 + '<text x="566" y="232" font-size="15.5" font-weight="800" fill="#0B5F5E">교감신경사슬</text>'
 + '<text x="566" y="251" font-size="12.5" fill="#0B5F5E">L2–L3가 표적</text>'
 + '<line x1="500" y1="372" x2="556" y2="384" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld2)"/>'
 + '<text x="562" y="390" font-size="14" font-weight="700" fill="#9A6800">교통가지</text>'
 + '<text x="562" y="408" font-size="12" fill="#8A96A0">(rami comm.)</text>'
 + '<text x="300" y="600" font-size="12.5" fill="#8A96A0">*측면 모식도 — 바늘은 척추체 <tspan font-weight="800">외측면</tspan>을 따라 전외측으로 진행</text>'
 + '</svg>')


# ============================================================
# 관상면(전면) 해부 모식도: 복부 교감신경간 · 대동맥/IVC · 신경절 + 요추 레벨(T12–L5)
# ============================================================
_LEVELS = [('T12', 50), ('L1', 134), ('L2', 218), ('L3', 302), ('L4', 386), ('L5', 470)]
_BODY_H = 72
_BX, _BW = 350, 220          # 척추체 x, 폭

def _coronal_spine():
    s = ''
    for name, y in _LEVELS:
        s += (f'<rect x="{_BX}" y="{y}" width="{_BW}" height="{_BODY_H}" rx="10" '
              f'fill="{_BONE}" stroke="{_BONE_S}" stroke-width="2.2"/>')
        s += (f'<rect x="{_BX}" y="{y+_BODY_H}" width="{_BW}" height="12" '
              f'fill="{_DISC}" stroke="{_DISC_S}" stroke-width="1.6"/>')
    return s

def _level_tags():
    s = ''
    for name, y in _LEVELS:
        cy = y + _BODY_H / 2
        hot = name in ('L2', 'L3')
        fill = '#0E7C7B' if hot else '#FFFFFF'
        txt = '#FFFFFF' if hot else '#5A6B7B'
        bd = '#0E7C7B' if hot else '#C7CDD2'
        s += (f'<rect x="248" y="{cy-19}" width="70" height="38" rx="10" fill="{fill}" '
              f'stroke="{bd}" stroke-width="2.2"/>')
        s += (f'<text x="283" y="{cy+7}" text-anchor="middle" font-size="20" font-weight="900" '
              f'fill="{txt}">{name}</text>')
        s += f'<line x1="318" y1="{cy}" x2="{_BX}" y2="{cy}" stroke="{bd}" stroke-width="2.2"/>'
    return s

def _trunk(x, flip=1):
    """교감신경간(사슬) + 신경절."""
    s = (f'<path d="M{x},44 C{x-8*flip},150 {x+8*flip},240 {x},330 '
         f'C{x-8*flip},420 {x+6*flip},500 {x},572" fill="none" '
         f'stroke="{_NRV}" stroke-width="9" stroke-linecap="round"/>')
    for _, y in _LEVELS:
        s += (f'<ellipse cx="{x}" cy="{y+_BODY_H/2}" rx="12" ry="19" fill="{_NRV}" '
              f'stroke="{_NRV_S}" stroke-width="2"/>')
    # 교통가지 (사슬 → 대동맥신경총 방향)
    for _, y in _LEVELS[1:5]:
        yy = y + _BODY_H / 2
        s += (f'<path d="M{x+18*flip},{yy} C{x+60*flip},{yy-6} {x+96*flip},{yy+4} {x+128*flip},{yy}" '
              f'fill="none" stroke="{_NRV}" stroke-width="4.5" stroke-linecap="round" opacity=".95"/>')
    return s

CORONAL_SVG = (
 '<svg viewBox="0 0 1200 640" width="100%" height="100%" preserveAspectRatio="xMidYMid meet" '
 'xmlns="http://www.w3.org/2000/svg" font-family="Pretendard,sans-serif">'
 '<defs><marker id="ld3" markerWidth="7" markerHeight="7" refX="3.5" refY="3.5">'
 '<circle cx="3.5" cy="3.5" r="2.2" fill="#8A96A0"/></marker></defs>'
 + _coronal_spine()
 # LSB 표적 밴드 (L2–L3)
 + f'<rect x="{_BX-6}" y="218" width="{_BW+12}" height="156" rx="10" fill="#0E7C7B" opacity="0.13"/>'
 + f'<rect x="{_BX-6}" y="218" width="{_BW+12}" height="156" rx="10" fill="none" stroke="#0E7C7B" '
   'stroke-width="2.6" stroke-dasharray="8 6"/>'
 # 하대정맥 (우) / 대동맥 (좌) — 전면 관찰이므로 화면 좌=환자 우
 + '<path d="M516,40 L556,40 L556,452 L516,452 Z" fill="#5A7C9C" opacity=".92"/>'
 + '<path d="M462,40 L508,40 L508,452 L462,452 Z" fill="#C0504D"/>'
 # 총장골동맥 분지 (L4 높이)
 + '<path d="M462,440 L508,440 L560,600 L520,600 Z" fill="#C0504D"/>'
 + '<path d="M462,440 L508,440 L452,600 L412,600 Z" fill="#C0504D"/>'
 # 신동맥 (L1–L2)
 + '<rect x="330" y="196" width="132" height="13" rx="6" fill="#C0504D"/>'
 + '<rect x="508" y="196" width="120" height="13" rx="6" fill="#C0504D"/>'
 # 교감신경간 좌·우
 + _trunk(332, 1) + _trunk(588, -1)
 # 내장신경 (상부 → 복강신경절)
 + f'<path d="M336,60 C380,96 410,116 432,136" fill="none" stroke="{_NRV}" stroke-width="6.5" stroke-linecap="round"/>'
 + f'<path d="M584,60 C542,96 514,116 494,136" fill="none" stroke="{_NRV}" stroke-width="6.5" stroke-linecap="round"/>'
 # 복강신경절 (좌우)
 + f'<ellipse cx="436" cy="146" rx="24" ry="17" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
 + f'<ellipse cx="500" cy="146" rx="22" ry="16" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
 # 대동맥신장신경절 · 상장간막신경절 · 하장간막신경절
 + f'<ellipse cx="440" cy="206" rx="19" ry="14" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
 + f'<ellipse cx="486" cy="236" rx="17" ry="13" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
 + f'<ellipse cx="470" cy="404" rx="18" ry="13" fill="{_NRV}" stroke="{_NRV_S}" stroke-width="2"/>'
 # 대동맥신경총 (얇은 그물)
 + ''.join(f'<path d="M446,{y} C470,{y+16} 500,{y-12} 520,{y+8}" fill="none" stroke="{_NRV}" '
           f'stroke-width="2.6" opacity=".85"/>' for y in (270, 310, 350, 384))
 + _level_tags()
 # ---- 라벨 ----
 + '<text x="248" y="34" font-size="14.5" font-weight="800" fill="#0B5F5E">요추 레벨</text>'
 + '<line x1="612" y1="264" x2="874" y2="248" stroke="#8A96A0" stroke-width="1.3" marker-end="url(#ld3)"/>'
 + '<text x="880" y="242" font-size="16.5" font-weight="800" fill="#0B5F5E">교감신경간(사슬)</text>'
 + '<text x="880" y="263" font-size="13.5" fill="#0B5F5E">척추체 전외측 · 좌우 한 쌍</text>'
 + '<line x1="520" y1="140" x2="874" y2="120" stroke="#8A96A0" stroke-width="1.3" marker-end="url(#ld3)"/>'
 + '<text x="880" y="116" font-size="15.5" font-weight="700" fill="#9A6800">복강신경절</text>'
 + '<text x="880" y="136" font-size="13" fill="#8A96A0">(celiac, T12–L1)</text>'
 + '<line x1="503" y1="236" x2="874" y2="186" stroke="#8A96A0" stroke-width="1.3" marker-end="url(#ld3)"/>'
 + '<text x="880" y="182" font-size="14.5" font-weight="700" fill="#9A6800">상장간막신경절</text>'
 + '<line x1="488" y1="404" x2="874" y2="404" stroke="#8A96A0" stroke-width="1.3" marker-end="url(#ld3)"/>'
 + '<text x="880" y="400" font-size="14.5" font-weight="700" fill="#9A6800">하장간막신경절</text>'
 + '<text x="880" y="420" font-size="13" fill="#8A96A0">(L3 부근)</text>'
 + '<line x1="150" y1="190" x2="336" y2="200" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld3)"/>'
 + '<text x="86" y="186" font-size="13.5" font-weight="700" fill="#9B3F3C">신동맥</text>'
 + '<line x1="150" y1="96" x2="340" y2="74" stroke="#8A96A0" stroke-width="1.2" marker-end="url(#ld3)"/>'
 + '<text x="86" y="92" font-size="13.5" font-weight="700" fill="#9A6800">내장신경</text>'
 + '<text transform="rotate(-90 486 95)" x="486" y="95" text-anchor="middle" font-size="15" '
   'font-weight="800" fill="#fff">대동맥</text>'
 + '<text transform="rotate(-90 536 95)" x="536" y="95" text-anchor="middle" font-size="13.5" '
   'font-weight="800" fill="#fff">하대정맥</text>'
 # 표적 배지
 + '<rect x="876" y="292" width="150" height="38" rx="19" fill="#0E7C7B"/>'
 + '<text x="951" y="318" text-anchor="middle" font-size="16.5" font-weight="900" fill="#fff">LSB 표적 L2–L3</text>'
 + '<text x="286" y="622" font-size="12.5" fill="#8A96A0">*후면(등 쪽에서 본) 모식도 — 엎드린 자세 기준 · 화면 좌측 = 환자 좌측</text>'
 + '</svg>')
