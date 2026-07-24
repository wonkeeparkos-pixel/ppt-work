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
  <text x="742" y="150" font-size="14.5" fill="#3E4A55" font-weight="700">방척추 접근</text>
  <text x="742" y="168" font-size="12.5" fill="#6B7680">척추체 접촉 후 전외측 walk</text>
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
