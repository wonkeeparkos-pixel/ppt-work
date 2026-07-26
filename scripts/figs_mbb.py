# -*- coding: utf-8 -*-
"""
MBB/FJB 덱 도해 (인라인 SVG).

색은 CSS 변수를 그대로 쓴다 → 라이트/다크 테마가 자동으로 따라온다.
  var(--nerve)/(--nerveB) 신경·내측지·MBB   var(--joint)/(--jointB) 관절·관절강내
  var(--panel) 뼈 채움    var(--line2) 뼈 윤곽    var(--crit) 오류·주의
"""

BONE = 'fill="var(--panel)" stroke="var(--line2)" stroke-width="1.6"'
BONE2 = 'fill="var(--stage)" stroke="var(--line2)" stroke-width="1.6"'
NERVE = 'fill="none" stroke="var(--nerve)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
NEEDLE = 'stroke="var(--ink)" stroke-width="2.8" stroke-linecap="round"'


def _t(x, y, s, size=11, anchor="middle", fill="var(--ink2)", w=600, cls="", extra=""):
    c = f' class="{cls}"' if cls else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
            f'fill="{fill}" font-weight="{w}"{c} {extra}>{s}</text>')


def _mono(x, y, s, size=11, anchor="middle", fill="var(--ink2)", w=600):
    return _t(x, y, s, size, anchor, fill, w, cls="m")


def _target(x, y, r=9, color="var(--nerve)", w=2.4):
    """표적점 마커 — 이중 링 + 십자선."""
    return (f'<g><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{color}" stroke-width="{w}"/>'
            f'<circle cx="{x}" cy="{y}" r="{r*0.32:.1f}" fill="{color}"/>'
            f'<path d="M{x-r-5} {y}H{x-r+2}M{x+r-2} {y}H{x+r+5}M{x} {y-r-5}V{y-r+2}M{x} {y+r-2}V{y+r+5}" '
            f'stroke="{color}" stroke-width="{w*0.75:.1f}" stroke-linecap="round"/></g>')


def _lead(x1, y1, x2, y2, color="var(--muted)"):
    return (f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="1.2" '
            f'stroke-dasharray="3 3" fill="none"/>')


def _needle(x1, y1, x2, y2, color="var(--ink)"):
    """바늘: 축 + 허브."""
    return (f'<g><path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{x1}" cy="{y1}" r="4.6" fill="{color}"/></g>')


def _svg(vb, inner, extra=""):
    return (f'<svg viewBox="{vb}" preserveAspectRatio="xMidYMid meet" role="img" {extra}>{inner}</svg>')


# ══════════════════════════════════════════════════════════════════
# 1. 후방 시야 요추 — 내측지 주행과 표적점
# ══════════════════════════════════════════════════════════════════
def posterior_spine():
    """후방(posterior) 시야: L1–S1, 내측지가 상관절돌기-횡돌기 접합부를 넘는 모습."""
    W, H = 440, 470
    cx = 208
    lv = [("L1", 62), ("L2", 138), ("L3", 214), ("L4", 290), ("L5", 366)]
    g = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="none"/>']

    # ── 뼈: 후궁·극돌기·횡돌기·관절돌기
    for name, cy in lv:
        # 극돌기
        g.append(f'<rect x="{cx-9}" y="{cy-20}" width="18" height="50" rx="5" {BONE}/>')
        for sgn in (-1, 1):
            # 후궁 (lamina)
            g.append(f'<path d="M{cx+sgn*8} {cy-14}Q{cx+sgn*40} {cy-20} {cx+sgn*58} {cy-4}'
                     f'L{cx+sgn*58} {cy+16}Q{cx+sgn*34} {cy+22} {cx+sgn*8} {cy+22}Z" {BONE}/>')
            # 횡돌기 (transverse process)
            g.append(f'<path d="M{cx+sgn*56} {cy-9}L{cx+sgn*116} {cy-13}'
                     f'Q{cx+sgn*128} {cy-2} {cx+sgn*114} {cy+7}L{cx+sgn*56} {cy+9}Z" {BONE}/>')
            # 상관절돌기 (SAP) — 위로
            g.append(f'<path d="M{cx+sgn*50} {cy-12}L{cx+sgn*50} {cy-36}'
                     f'Q{cx+sgn*62} {cy-44} {cx+sgn*72} {cy-34}L{cx+sgn*72} {cy-8}Z" {BONE2}/>')
            # 하관절돌기 (IAP) — 아래
            g.append(f'<path d="M{cx+sgn*54} {cy+14}L{cx+sgn*54} {cy+40}'
                     f'Q{cx+sgn*66} {cy+48} {cx+sgn*76} {cy+38}L{cx+sgn*76} {cy+12}Z" {BONE}/>')
        g.append(_mono(cx, cy + 12, name, 12, fill="var(--muted)"))

    # 천골 (sacrum) + 천골익
    sy = 430
    g.append(f'<path d="M{cx-92} {sy-28}Q{cx} {sy-40} {cx+92} {sy-28}L{cx+72} {sy+34}'
             f'Q{cx} {sy+46} {cx-72} {sy+34}Z" {BONE}/>')
    g.append(_mono(cx, sy + 8, "SACRUM", 11, fill="var(--muted)"))
    # S1 상관절돌기
    for sgn in (-1, 1):
        g.append(f'<path d="M{cx+sgn*50} {sy-26}L{cx+sgn*50} {sy-48}Q{cx+sgn*62} {sy-56} {cx+sgn*72} {sy-46}'
                 f'L{cx+sgn*72} {sy-24}Z" {BONE2}/>')

    # ── 후관절 (facet joint) 표시: 좌측만 파란 관절선
    for i in range(len(lv) - 1):
        cy = lv[i][1]
        jy = cy + 26
        g.append(f'<path d="M{cx-74} {jy-6}L{cx-52} {jy+6}" stroke="var(--joint)" stroke-width="3.4" '
                 f'stroke-linecap="round" opacity=".9"/>')
    g.append(f'<path d="M{cx-74} {lv[4][1]+26-6}L{cx-52} {lv[4][1]+26+6}" stroke="var(--joint)" '
             f'stroke-width="3.4" stroke-linecap="round" opacity=".9"/>')

    # ── 내측지 (우측): 상위 레벨에서 나와 한 레벨 아래 SAP-TP 접합부를 넘는다
    #    Ln 내측지 → Ln+1 횡돌기·상관절돌기 접합부가 표적
    def nerve_path(d, label, tx, ty):
        return [f'<path d="{d}" fill="none" stroke="var(--stage)" stroke-width="7" stroke-linecap="round"/>',
                f'<path d="{d}" {NERVE}/>', _target(tx, ty, 8.5),
                _lead(tx + 11, ty, W - 62, ty),
                _mono(W - 8, ty + 4, label, 11.5, anchor="end", fill="var(--nerve)")]

    for i in range(4):
        oy = lv[i][1]
        ty = lv[i + 1][1]
        tx = cx + 54
        tgt_y = ty - 14
        d = (f"M{cx+122} {oy+14}Q{cx+112} {oy+42} {tx+16} {tgt_y-16}"
             f"Q{tx-2} {tgt_y+8} {cx+24} {ty+24}")
        g += nerve_path(d, f"{lv[i][0]} MB", tx, tgt_y)

    # L5 후지 — 천골익 / S1 상관절돌기 접합부
    oy = lv[4][1]
    d = (f"M{cx+122} {oy+16}Q{cx+112} {oy+46} {cx+68} {sy-52}"
         f"Q{cx+40} {sy-26} {cx+22} {sy-4}")
    g += nerve_path(d, "L5 후지", cx + 56, sy - 44)

    # 범례
    g.append(f'<g transform="translate(12,{H-38})">'
             f'<path d="M0 0h20" {NERVE}/>{_t(26, 4, "내측지", 11, "start")}'
             f'<path d="M0 18h20" stroke="var(--joint)" stroke-width="3.4" stroke-linecap="round"/>'
             f'{_t(26, 22, "후관절", 11, "start")}</g>')
    g.append(f'<g transform="translate({W-104},{H-38})">{_target(9, 0, 8)}'
             f'{_t(24, 4, "표적점", 11, "start", fill="var(--nerve)", w=700)}</g>')

    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 2. 이중 지배 브래킷 — 관절 1개 = 내측지 2개
# ══════════════════════════════════════════════════════════════════
def dual_bracket():
    W, H = 400, 470
    g = []
    joints = [("L1-2", "T12 · L1"), ("L2-3", "L1 · L2"), ("L3-4", "L2 · L3"),
              ("L4-5", "L3 · L4"), ("L5-S1", "L4 · L5 후지")]
    y0, step = 58, 78
    g.append(_mono(28, 30, "관절", 12, "start", "var(--joint)", 700))
    g.append(_mono(W - 28, 30, "차단해야 할 신경 2개", 12, "end", "var(--nerve)", 700))
    for i, (j, nn) in enumerate(joints):
        y = y0 + i * step
        hl = (j in ("L4-5", "L5-S1"))
        bg = "var(--nerveW)" if hl else "none"
        g.append(f'<rect x="16" y="{y-24}" width="{W-32}" height="56" rx="7" fill="{bg}" '
                 f'stroke="{"var(--nerve)" if hl else "var(--line)"}" stroke-width="{1.8 if hl else 1.3}"/>')
        g.append(f'<rect x="30" y="{y-13}" width="66" height="30" rx="5" fill="var(--joint)"/>')
        g.append(_mono(63, y + 7, j, 14, fill="var(--stage)", w=600))
        # 브래킷
        g.append(f'<path d="M112 {y+2}h22" stroke="var(--line2)" stroke-width="1.5"/>')
        g.append(f'<path d="M134 {y-14}v32M134 {y-14}h10M134 {y+18}h10" stroke="var(--nerve)" '
                 f'stroke-width="1.8" fill="none" stroke-linecap="round"/>')
        a, b = nn.split(" · ")
        for k, lab in enumerate((a, b)):
            yy = y - 14 if k == 0 else y + 18
            g.append(f'<rect x="150" y="{yy-12}" width="{92 if "후지" in lab else 62}" height="24" rx="4" '
                     f'fill="none" stroke="var(--nerve)" stroke-width="1.6"/>')
            g.append(_mono(150 + (46 if "후지" in lab else 31), yy + 5,
                           lab if "후지" in lab else f"{lab} MB", 12, fill="var(--nerve)"))
        g.append(_t(W - 26, y + 6, "내측지 2개 = 주사 2회", 10.5, "end", "var(--muted)", 500))
    g.append(_t(W / 2, H - 14,
                "한 관절은 같은 번호·바로 위 번호 내측지의 이중 지배를 받는다", 11.5,
                fill="var(--nerve)", w=700))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 3. 사위상 "스코티독" — 표적은 눈(귀-코 접합부)
# ══════════════════════════════════════════════════════════════════
def scotty_dog(target=True, wrong=False):
    """사위상. 개는 왼쪽을 본다: 코=TP, 눈=척추경, 귀=SAP, 목=협부, 앞다리=IAP."""
    W, H = 440, 340
    g = []
    # 하나의 연속 윤곽으로 그려야 '개'로 읽힌다
    dog = ("M56 152 Q74 128 104 122 L146 116 L150 68 Q160 44 180 44 Q200 46 204 70 L206 118"
           " Q244 114 268 106 Q296 96 318 98 Q330 62 352 54 Q372 50 372 70 Q368 92 354 106"
           " Q372 132 372 158 Q370 186 358 202 L356 262 Q356 280 340 282 Q324 282 324 262"
           " L322 212 Q300 220 274 220 L272 262 Q272 282 256 283 Q240 283 240 262 L238 216"
           " Q212 208 200 192 Q184 176 152 180 L106 184 Q76 180 56 152 Z")
    g.append(f'<path d="{dog}" {BONE}/>')
    # 눈 = 척추경
    g.append(f'<ellipse cx="140" cy="150" rx="25" ry="21" fill="var(--stage)" stroke="var(--line2)" stroke-width="1.9"/>')
    # 협부(목) 음영
    g.append(f'<path d="M206 122 Q230 150 208 188" fill="none" stroke="var(--line2)" '
             f'stroke-width="1.3" stroke-dasharray="4 3" opacity=".8"/>')

    labs = [("코 = 횡돌기 TP", 48, 206, "start"),
            ("눈 = 척추경", 140, 155, "middle"),
            ("귀 = 상관절돌기 SAP", 178, 30, "middle"),
            ("목 = 협부 Pars", 250, 178, "middle"),
            ("앞다리 = 하관절돌기 IAP", 256, 308, "middle"),
            ("꼬리 = 반대측 SAP", 428, 42, "end")]
    for s, x, y, an in labs:
        g.append(_t(x, y, s, 11, an, "var(--muted)", 600))

    # 표적 = SAP 기저부와 횡돌기 상연이 만나는 곳 (귀 뿌리 ~ 눈 상방)
    tx, ty = 152, 118
    if target:
        g.append(_lead(tx - 6, ty - 4, 96, 64))
        g.append(_target(tx, ty, 11))
        g.append(_mono(10, 52, "TARGET", 12, "start", "var(--nerve)"))
        g.append(_t(10, 68, "SAP 기저부 × TP 상연", 11, "start", "var(--nerve)", 700))
        g.append(_t(10, 83, "= '귀 뿌리 ~ 눈' 위치", 10.5, "start", "var(--muted)", 600))
        g.append(_needle(30, 250, tx - 8, ty + 8))
    if wrong:
        g.append(f'<circle cx="212" cy="150" r="12" fill="none" stroke="var(--crit)" stroke-width="2.6"/>')
        g.append(f'<path d="M204 142l16 16M220 142l-16 16" stroke="var(--crit)" stroke-width="2.4" stroke-linecap="round"/>')
        g.append(_t(232, 132, "너무 내측 = 협부·관절강", 11, "start", "var(--crit)", 700))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 4. 정면(AP) 시야 표적 — 횡돌기 상연 + SAP 외측연
# ══════════════════════════════════════════════════════════════════
def ap_target():
    W, H = 420, 330
    g = []
    cx = 210
    for i, cy in enumerate((92, 194, 296)):
        # 척추체
        g.append(f'<rect x="{cx-66}" y="{cy-34}" width="132" height="68" rx="9" {BONE}/>')
        # 척추경 (eyes)
        for sgn in (-1, 1):
            g.append(f'<ellipse cx="{cx+sgn*40}" cy="{cy-8}" rx="15" ry="12" {BONE2}/>')
            # 횡돌기
            g.append(f'<path d="M{cx+sgn*62} {cy-14}L{cx+sgn*126} {cy-18}Q{cx+sgn*138} {cy-6} '
                     f'{cx+sgn*124} {cy+3}L{cx+sgn*62} {cy+2}Z" {BONE}/>')
            # 상관절돌기
            g.append(f'<path d="M{cx+sgn*52} {cy-22}L{cx+sgn*52} {cy-46}Q{cx+sgn*64} {cy-54} '
                     f'{cx+sgn*74} {cy-44}L{cx+sgn*74} {cy-16}Z" {BONE2}/>')
        g.append(f'<rect x="{cx-8}" y="{cy-12}" width="16" height="40" rx="4" {BONE}/>')
        g.append(_mono(cx, cy + 24, ["L3", "L4", "L5"][i], 12, fill="var(--muted)"))

    # 표적 = 횡돌기 상연과 SAP 외측연이 만나는 지점
    for cy in (194, 296):
        g.append(_target(cx + 60, cy - 18, 10))
    g.append(_lead(cx + 60, 194 - 18, 388, 118))
    g.append(_mono(392, 112, "TARGET", 12, "end", "var(--nerve)"))
    g.append(_t(392, 128, "횡돌기 상연 × SAP 외측연", 11, "end", "var(--nerve)", 700))
    g.append(_t(392, 143, "바늘끝은 SAP 외측연에 걸치거나", 10.5, "end", "var(--muted)", 600))
    g.append(_t(392, 157, "약간 내측에 위치한다", 10.5, "end", "var(--muted)", 600))
    # 종판 정렬 표시
    g.append(f'<path d="M{cx-96} {58}h192" stroke="var(--joint)" stroke-width="1.8" stroke-dasharray="6 4"/>')
    g.append(_t(cx - 100, 62, "종판 일치", 10.5, "end", "var(--joint)", 700))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 5. L5 후지 — 천골익 / S1 상관절돌기 접합부
# ══════════════════════════════════════════════════════════════════
def l5_dorsal_ramus():
    W, H = 420, 330
    g = []
    cx = 200
    # L5 척추
    g.append(f'<rect x="{cx-66}" y="60" width="132" height="66" rx="9" {BONE}/>')
    for sgn in (-1, 1):
        g.append(f'<ellipse cx="{cx+sgn*40}" cy="88" rx="15" ry="12" {BONE2}/>')
        g.append(f'<path d="M{cx+sgn*62} 78L{cx+sgn*118} 74Q{cx+sgn*130} 86 {cx+sgn*116} 95L{cx+sgn*62} 94Z" {BONE}/>')
    g.append(_mono(cx, 116, "L5", 13, fill="var(--muted)"))
    # 천골 + 천골익
    g.append(f'<path d="M{cx-150} 150Q{cx} 132 {cx+150} 150L{cx+104} 288Q{cx} 306 {cx-104} 288Z" {BONE}/>')
    g.append(_mono(cx, 250, "SACRUM", 12, fill="var(--muted)"))
    g.append(_t(cx - 118, 176, "천골익", 11, "middle", "var(--muted)", 600))
    g.append(_t(cx + 118, 176, "ala", 11, "middle", "var(--muted)", 600))
    # S1 상관절돌기
    for sgn in (-1, 1):
        g.append(f'<path d="M{cx+sgn*46} 156L{cx+sgn*46} 132Q{cx+sgn*60} 124 {cx+sgn*72} 134'
                 f'L{cx+sgn*72} 158Z" {BONE2}/>')
    g.append(_t(cx + 96, 132, "S1 SAP", 11, "start", "var(--muted)", 600))
    # 표적: 천골익과 S1 SAP 이 만나는 오목한 지점
    tx, ty = cx + 40, 156
    g.append(_target(tx, ty, 10))
    g.append(f'<path d="M{cx+118} 100Q{cx+80} 130 {tx+10} {ty-2}Q{cx+18} 178 {cx+6} 206" {NERVE}/>')
    g.append(_mono(cx + 126, 96, "L5 dorsal ramus", 11.5, "start", "var(--nerve)"))
    g.append(_lead(tx, ty, 372, 232))
    g.append(_mono(376, 226, "TARGET", 12, "end", "var(--nerve)"))
    g.append(_t(376, 242, "천골익 × S1 SAP 접합부", 11, "end", "var(--nerve)", 700))
    # 장골능 장애물
    g.append(f'<path d="M18 214Q60 176 96 190" stroke="var(--crit)" stroke-width="2.6" fill="none" '
             f'stroke-dasharray="7 5" stroke-linecap="round"/>')
    g.append(_t(24, 234, "장골능이 가리면", 10.5, "start", "var(--crit)", 700))
    g.append(_t(24, 248, "사위를 5–10° AP로 되돌리거나", 10, "start", "var(--crit)", 600))
    g.append(_t(24, 261, "C-arm을 두측(cephalad)으로 기울인다", 10, "start", "var(--crit)", 600))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 6. 연관통 지도 — 후면 인체 실루엣
# ══════════════════════════════════════════════════════════════════
_HALF = ("M150 24 L120 30 Q98 38 95 62 L89 122 Q85 150 93 174 L87 214 Q83 252 97 270"
         " L101 346 Q105 354 107 362 L111 422 Q113 452 109 470 L105 488 Q103 498 117 498"
         " L141 496 Q149 494 147 480 L145 462 Q149 422 149 382 L143 300 L143 276"
         " Q146 271 150 270 Z")


def _body(sfx):
    """후면 전신 실루엣 + 구역 클리핑용 clipPath. viewBox 0 0 300 520 기준."""
    body = (f'<path d="{_HALF}" />'
            f'<path d="{_HALF}" transform="translate(300,0) scale(-1,1)"/>')
    return (f'<defs><clipPath id="bc{sfx}">{body}</clipPath></defs>'
            f'<g fill="var(--stage)" stroke="var(--line2)" stroke-width="2">'
            f'<path d="{_HALF}"/><path d="{_HALF}" transform="translate(300,0) scale(-1,1)"/></g>')


_ZONES = [
    ("1", "요부", "M104 128 H196 V196 H104 Z", .92),
    ("2", "둔부", "M86 200 H214 V258 H86 Z", .78),
    ("3", "대전자부", "M78 204 H104 V250 H78 Z|M196 204 H222 V250 H196 Z", .60),
    ("4", "외측대퇴", "M92 262 H116 V352 H92 Z|M184 262 H208 V352 H184 Z", .48),
    ("5", "후방대퇴", "M118 262 H146 V352 H118 Z|M154 262 H182 V352 H154 Z", .38),
]


def fukui_zones(sfx="a"):
    """
    Fukui 1997이 사용한 6개 구역을 인체에 그대로 표시한다.
    후면 5개 + 전면(서혜부) 1개. 이 논문에는 '옆구리·장골능·무릎 아래' 구역이 없다.
    """
    col = "var(--nerve)"
    g = [_body(sfx)]
    g.append(f'<g clip-path="url(#bc{sfx})">')
    for no, name, d, op in _ZONES:
        for seg in d.split("|"):
            g.append(f'<path d="{seg}" fill="{col}" opacity="{op}"/>')
    g.append('</g>')
    g.append(f'<g fill="none" stroke="var(--line2)" stroke-width="2">'
             f'<path d="{_HALF}"/><path d="{_HALF}" transform="translate(300,0) scale(-1,1)"/></g>')

    # 번호 배지 + 지시선 (오른쪽 범례)
    ann = [("1", "요부", "lumbar", 172), ("2", "둔부", "gluteal", 214),
           ("3", "대전자부", "trochanteric", 256), ("4", "외측 대퇴", "lateral thigh", 298),
           ("5", "후방 대퇴", "posterior thigh", 340)]
    anchor = {"1": (196, 162), "2": (214, 230), "3": (222, 227), "4": (208, 300), "5": (182, 330)}
    for no, ko, en, ly in ann:
        ax, ay = anchor[no]
        g.append(f'<path d="M{ax} {ay} L{326} {ly-5}" stroke="var(--line2)" stroke-width="1" stroke-dasharray="3 3"/>')
        g.append(f'<circle cx="340" cy="{ly-5}" r="11" fill="{col}"/>')
        g.append(_mono(340, ly - 1, no, 12, fill="var(--stage)"))
        g.append(_t(358, ly - 9, ko, 14, "start", "var(--ink)", 700))
        g.append(_mono(358, ly + 8, en, 11.5, "start", "var(--muted)", 500))

    # 전면 소도해 — 서혜부
    g.append(f'<g transform="translate(348,372) scale(0.26)">'
             f'<path d="{_HALF}" fill="var(--stage)" stroke="var(--line2)" stroke-width="6"/>'
             f'<path d="{_HALF}" transform="translate(300,0) scale(-1,1)" fill="var(--stage)" '
             f'stroke="var(--line2)" stroke-width="6"/>'
             f'<path d="M100 206 H150 V264 H100 Z" fill="{col}" opacity=".6"/>'
             f'<path d="M150 206 H200 V264 H150 Z" fill="{col}" opacity=".6"/></g>')
    g.append(_t(387, 500, "앞면", 11, "middle", "var(--muted)", 600))
    g.append(f'<circle cx="440" cy="404" r="11" fill="{col}"/>')
    g.append(_mono(440, 408, "6", 12, fill="var(--stage)"))
    g.append(_t(458, 400, "서혜부", 14, "start", "var(--ink)", 700))
    g.append(_mono(458, 417, "groin — 전면", 11.5, "start", "var(--muted)", 500))
    g.append(_t(458, 440, "모든 레벨에서", 11.5, "start", "var(--muted)", 600))
    g.append(_t(458, 456, "가장 드문 구역", 11.5, "start", "var(--muted)", 600))

    g.append(_t(150, 126, "Fukui 1997 — 6 zones", 13, "middle", "var(--nerve)", 700))
    return _svg("0 112 600 400", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 7. 후관절 방향 변화 (축상면) — 상위 시상 → 하위 관상
# ══════════════════════════════════════════════════════════════════
def facet_orientation():
    """축상면(axial): 관절면이 시상면 → 관상면으로 돌아가는 변화."""
    import math
    W, H = 480, 262
    g = []
    specs = [("L1-2", 25, "시상면에 가까움"), ("L3-4", 45, "중간"), ("L5-S1", 60, "관상면에 가까움")]
    # 각도 값은 도해용 근사치다. 계측 시리즈마다 기준면·영상법·측정 슬라이스가 달라
    # 같은 관절도 15–20° 차이가 나므로 슬라이드에 숫자를 단정해 올리지 않는다.
    for i, (lab, ang, desc) in enumerate(specs):
        cx, cy = 84 + i * 156, 108
        # 척추체 (전방 = 위)
        g.append(f'<ellipse cx="{cx}" cy="{cy-30}" rx="43" ry="25" {BONE}/>')
        # 척추경
        for sgn in (-1, 1):
            g.append(f'<path d="M{cx+sgn*32} {cy-14}L{cx+sgn*44} {cy+2}" stroke="var(--line2)" '
                     f'stroke-width="9" stroke-linecap="round"/>')
        # 후궁 + 극돌기
        g.append(f'<path d="M{cx-42} {cy+8}Q{cx} {cy+56} {cx+42} {cy+8}" fill="none" '
                 f'stroke="var(--line2)" stroke-width="9" stroke-linecap="round"/>')
        g.append(f'<rect x="{cx-4}" y="{cy+40}" width="8" height="20" rx="3" fill="var(--line2)"/>')
        # 관절면
        rad = math.radians(ang)
        for sgn in (-1, 1):
            jx, jy = cx + sgn * 44, cy + 6
            ux, uy = sgn * math.sin(rad) * 19, -math.cos(rad) * 19
            nx, ny = sgn * math.cos(rad) * 7.5, math.sin(rad) * 7.5
            for k in (-1, 1):   # 관절면을 이루는 두 뼈
                g.append(f'<path d="M{jx-ux+k*nx:.1f} {jy-uy+k*ny:.1f}L{jx+ux+k*nx:.1f} {jy+uy+k*ny:.1f}" '
                         f'stroke="var(--line2)" stroke-width="6" stroke-linecap="round"/>')
            g.append(f'<path d="M{jx-ux:.1f} {jy-uy:.1f}L{jx+ux:.1f} {jy+uy:.1f}" '
                     f'stroke="var(--joint)" stroke-width="3.2" stroke-linecap="round"/>')
        # 시상면 기준선 + 각도
        g.append(f'<path d="M{cx+44} {cy-24}V{cy+36}" stroke="var(--muted)" stroke-width="1.1" stroke-dasharray="4 3"/>')
        g.append(f'<path d="M{cx+44} {cy-16}A16 16 0 0 1 {cx+44+16*math.sin(rad):.1f} {cy-16+16*(1-math.cos(rad)):.1f}" '
                 f'fill="none" stroke="var(--joint)" stroke-width="1.4"/>')
        g.append(_mono(cx, 36, lab, 14, fill="var(--ink)"))
        g.append(_t(cx, 204, desc, 12.5, "middle", "var(--joint)", 700))
    g.append(_t(20, 30, "전방", 10.5, "start", "var(--muted)", 600))
    g.append(_t(20, 172, "후방", 10.5, "start", "var(--muted)", 600))
    g.append(f'<path d="M56 236 H424" stroke="var(--joint)" stroke-width="1.6"/>'
             f'<path d="M418 231 L426 236 L418 241 Z" fill="var(--joint)"/>')
    g.append(_t(W / 2, H - 6, "미측으로 갈수록 관상면에 가까워진다 → 관절을 여는 사위각이 레벨마다 다르다",
                11.5, "middle", "var(--ink2)", 700))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 8. 측면상 바늘 깊이 — 올바름 vs 너무 복측
# ══════════════════════════════════════════════════════════════════
def lateral_depth(correct=True):
    W, H = 340, 250
    g = []
    # 척추체 (측면)
    g.append(f'<rect x="42" y="70" width="118" height="98" rx="10" {BONE}/>')
    g.append(f'<rect x="42" y="182" width="118" height="14" rx="5" fill="var(--line2)" opacity=".35"/>')
    g.append(_t(101, 214, "추간판", 10, "middle", "var(--muted)", 600))
    # 척추경·관절돌기 (후방)
    g.append(f'<path d="M160 96 Q206 88 232 106 L236 152 Q206 172 160 160Z" {BONE}/>')
    g.append(f'<path d="M232 92 Q258 78 276 96 L276 130 Q252 140 234 128Z" {BONE2}/>')
    g.append(_t(101, 124, "척추체", 11, "middle", "var(--muted)", 600))
    g.append(_t(214, 62, "횡돌기 기저부", 10.5, "middle", "var(--muted)", 600))
    # 척추관
    g.append(f'<ellipse cx="184" cy="128" rx="15" ry="24" fill="var(--critW)" stroke="var(--crit)" '
             f'stroke-width="1.4" stroke-dasharray="4 3"/>')
    g.append(_t(184, 168, "척추관", 10, "middle", "var(--crit)", 600))
    if correct:
        g.append(_needle(316, 60, 226, 108))
        g.append(_target(222, 110, 9, "var(--good)"))
        g.append(_t(300, 168, "골 접촉에서 정지", 11, "end", "var(--good)", 700))
        g.append(_t(300, 184, "복측 진행 없음", 10.5, "end", "var(--muted)", 600))
    else:
        g.append(_needle(316, 60, 186, 128, "var(--crit)"))
        g.append(f'<path d="M180 122l12 12M192 122l-12 12" stroke="var(--crit)" stroke-width="2.6" stroke-linecap="round"/>')
        g.append(_t(300, 168, "복측으로 미끄러짐", 11, "end", "var(--crit)", 700))
        g.append(_t(300, 184, "→ 척추간공·신경뿌리", 10.5, "end", "var(--crit)", 600))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 9. 주입량과 확산 — 표적 특이도
# ══════════════════════════════════════════════════════════════════
def volume_spread(vol="0.3–0.5 mL", ok=True):
    W, H = 340, 250
    g = []
    cx, cy = 168, 118
    # 뼈 배경
    g.append(f'<path d="M40 152 Q100 128 168 132 Q236 136 300 158 L300 210 L40 210 Z" {BONE}/>')
    g.append(f'<path d="M140 62 Q168 44 196 62 L200 132 L136 132 Z" {BONE2}/>')
    g.append(_t(168, 196, "SAP-TP 접합부", 10.5, "middle", "var(--muted)", 600))
    r = 26 if ok else 62
    col = "var(--good)" if ok else "var(--crit)"
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" opacity=".2"/>')
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="2.2" stroke-dasharray="5 4"/>')
    g.append(_target(cx, cy, 8, col))
    g.append(_mono(cx, 34, vol, 15, fill=col))
    if ok:
        g.append(_t(cx, 232, "표적 신경에만 국한 → 진단 특이도 유지", 10.5, "middle", "var(--good)", 700))
    else:
        g.append(_t(cx, 232, "인접 구조로 확산 → 위양성", 10.5, "middle", "var(--crit)", 700))
        g.append(_t(292, 90, "후지 본간", 10, "end", "var(--crit)", 600))
        g.append(_t(56, 90, "척추간공", 10, "start", "var(--crit)", 600))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 10. 초음파 횡단면 — 삼지창(trident) 소견
# ══════════════════════════════════════════════════════════════════
def us_trident():
    W, H = 340, 250
    g = []
    g.append(f'<rect x="16" y="16" width="{W-32}" height="{H-56}" rx="6" fill="#0F1519" stroke="var(--line2)" stroke-width="1.4"/>')
    # 횡돌기 3개 — 고에코 선 + 음향 음영
    for i, x in enumerate((78, 168, 258)):
        g.append(f'<path d="M{x-28} 118 Q{x} 108 {x+28} 118" stroke="#EDEDED" stroke-width="4.5" fill="none" stroke-linecap="round"/>')
        g.append(f'<rect x="{x-26}" y="122" width="52" height="72" fill="#05080A" opacity=".92"/>')
        g.append(_mono(x, 210, ["TP", "TP", "TP"][i], 11, fill="#8A97A1"))
    # 근육층
    g.append(f'<path d="M20 74 Q170 60 320 74" stroke="#6E7A84" stroke-width="2" fill="none" opacity=".7"/>')
    g.append(_t(170, 52, "다열근 · 최장근", 10.5, "middle", "#9AA7B1", 600))
    # 표적 = 횡돌기 사이 오목 (SAP-TP 접합)
    g.append(_target(123, 116, 9, "var(--nerveB)"))
    g.append(_target(213, 116, 9, "var(--nerveB)"))
    g.append(f'<path d="M312 40 L131 108" stroke="var(--nerveB)" stroke-width="2.6" stroke-linecap="round"/>')
    g.append(_mono(170, 232, "TRIDENT SIGN — 횡돌기 3개의 고에코 + 음향음영", 10.5, fill="var(--muted)"))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 11. 진단 알고리즘 흐름
# ══════════════════════════════════════════════════════════════════
def algorithm():
    W, H = 900, 300
    g = []
    boxes = [
        (20, "축성 요통 3개월↑\n보존치료 실패", "var(--panel)", "var(--line2)", "var(--ink)"),
        (200, "1차 진단적 MBB\n관절당 신경 2개", "var(--nerveW)", "var(--nerve)", "var(--nerve)"),
        (380, "2차 확인 차단\n다른 약제·이중차단", "var(--nerveW)", "var(--nerve)", "var(--nerve)"),
        (560, "두 번 모두 양성\n≥80% 통증감소", "var(--goodW)", "var(--good)", "var(--good)"),
        (740, "고주파 신경차단술\nRFA", "var(--ink)", "var(--ink)", "var(--stage)"),
    ]
    for x, label, bg, bd, fg in boxes:
        g.append(f'<rect x="{x}" y="66" width="140" height="86" rx="8" fill="{bg}" stroke="{bd}" stroke-width="1.8"/>')
        for i, line in enumerate(label.split("\n")):
            g.append(_t(x + 70, 100 + i * 20, line, 12.5, "middle", fg, 700 if i == 0 else 500))
        if x < 740:
            g.append(f'<path d="M{x+146} 109 L{x+174} 109" stroke="var(--line2)" stroke-width="2"/>')
            g.append(f'<path d="M{x+168} 104 L{x+176} 109 L{x+168} 114 Z" fill="var(--line2)"/>')
    # 음성 경로
    g.append(f'<path d="M270 158 L270 208 L660 208 L660 176" stroke="var(--crit)" stroke-width="1.8" '
             f'fill="none" stroke-dasharray="6 4"/>')
    g.append(f'<path d="M655 182 L660 172 L665 182 Z" fill="var(--crit)"/>')
    g.append(_t(465, 228, "위양성 25–41%를 걸러내는 단계 — 단일 차단만으로 RFA로 가지 않는다",
                12, "middle", "var(--crit)", 700))
    return _svg(f"0 0 {W} {H}", ''.join(g))


# ══════════════════════════════════════════════════════════════════
# 12. 후관절 구조 — 피막·상하 오목·반월판
# ══════════════════════════════════════════════════════════════════
def facet_capsule():
    """시상 단면: 관절강, 상부·하부 오목, 섬유지방 반월판, 피막 두께."""
    W, H = 780, 340
    g = []
    # ── 왼쪽: 관절 단면
    g.append(f'<path d="M104 44 Q160 38 200 60 L206 206 Q164 228 110 220 Z" {BONE}/>')
    g.append(f'<path d="M216 122 Q272 114 306 138 L312 296 Q266 314 218 302 Z" {BONE}/>')
    g.append(_t(150, 132, "하관절돌기", 13, "middle", "var(--muted)", 600))
    g.append(_t(150, 149, "IAP · 위 척추", 11.5, "middle", "var(--muted)", 500))
    g.append(_t(266, 224, "상관절돌기", 13, "middle", "var(--muted)", 600))
    g.append(_t(266, 241, "SAP · 아래 척추", 11.5, "middle", "var(--muted)", 500))

    # 관절강
    g.append(f'<path d="M202 64 L212 70 L220 296 L208 292 Z" fill="var(--joint)" opacity=".28"/>')
    # 피막
    cap = ('M198 56 Q226 48 242 64 L250 114 Q260 120 260 134'
           ' L266 302 Q240 318 212 310 Q200 296 202 282 L194 132 Q186 124 188 110 Z')
    g.append(f'<path d="{cap}" fill="none" stroke="var(--joint)" stroke-width="3.2" '
             f'stroke-linejoin="round" opacity=".95"/>')
    # 오목
    g.append(f'<ellipse cx="222" cy="74" rx="26" ry="17" fill="var(--joint)" opacity=".45"/>')
    g.append(f'<ellipse cx="240" cy="296" rx="28" ry="18" fill="var(--joint)" opacity=".58"/>')
    g.append(_target(240, 296, 9, "var(--good)"))
    g.append(_needle(140, 314, 230, 300, "var(--good)"))
    # 반월판
    for cx_, cy_ in ((202, 98), (208, 264)):
        g.append(f'<path d="M{cx_-2} {cy_}q11 7 2 17" stroke="var(--nerve)" stroke-width="3.6" '
                 f'fill="none" stroke-linecap="round"/>')

    # ── 오른쪽: 주석 열
    def row(y, color, kicker, l1, l2, ax, ay):
        g.append(_lead(ax, ay, 388, y - 6, color))
        g.append(f'<rect x="392" y="{y-26}" width="4" height="46" rx="2" fill="{color}"/>')
        g.append(_mono(410, y - 10, kicker, 12.5, "start", color))
        g.append(_t(410, y + 8, l1, 13.5, "start", "var(--ink)", 700))
        g.append(_t(410, y + 25, l2, 12, "start", "var(--muted)", 600))

    row(62, "var(--crit)", "SUPERIOR RECESS", "상부 오목 — 피한다",
        "황색인대·경막외강에 인접. 터지면 여기로 샌다", 246, 70)
    row(140, "var(--nerve)", "MENISCOID", "섬유지방 반월판",
        "관절면 사이로 들어간다 · 통증 유발 후보", 210, 104)
    row(218, "var(--joint)", "CAPSULE", "섬유 피막 ≈1 mm",
        "관절연에서 약 2 mm 바깥에 부착", 192, 180)
    row(296, "var(--good)", "INFERIOR RECESS", "하부 오목 — 진입 표적",
        "더 크고 잘 늘어난다 · 퇴행 관절의 대안", 266, 296)

    return _svg(f"0 24 {W} {H-40}", ''.join(g))
