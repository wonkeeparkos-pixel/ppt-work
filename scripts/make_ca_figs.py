# -*- coding: utf-8 -*-
"""Complete Anatomy L3 축상면 렌더에 강의용 라벨을 얹어 덱 그림 2종을 만든다.

원칙
  · 원본 렌더는 픽셀 하나 건드리지 않는다. 생성형 모델로 다시 그리면 좌우·전후가
    틀어지므로, 정확도가 담보되는 방법은 "검증된 원본 + 내가 좌표를 통제하는 라벨"뿐이다.
  · 라벨은 얇은 지시선과 번호만. 굵은 화살표·색면을 쓰면 그림(일러스트)처럼 보인다.
  · 설명은 그림 위에 흩뿌리지 않고 오른쪽 한 칸에 번호순으로 모은다(발표 중 읽기 편하게).

원본 판독 (2026-07-27 실측, 세 갈래로 교차확인)
  1) 대동맥·IVC의 잘린 내강 입구가 우리를 향한다 → 위에서 내려다본 시점, 화면 아래가 후방.
  2) 적색 대동맥 내강이 청색 IVC 내강보다 화면 왼쪽 → 대동맥=환자 좌, IVC=환자 우
     → 화면 왼쪽 = 환자 좌측 (덱의 다른 축상면 도해와 같은 규약).
  3) 우측 신장이 통째로, 좌측 신장은 얇은 절단면으로 보인다 → 우신이 더 낮다는 사실과 일치.

출력
  assets/ca_target.webp   14쪽 — 표적이 어디인가
  assets/ca_avoid.webp    합병증 뒤 — 무엇을 피하나
"""

import base64
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(REPO, "문헌고찰_NLC_RLS_LSB", "03_LSB", "assets")
SRC = os.path.join(ASSETS, "ca_src_L3.png")

# ── 원본(1021×701)에서 잘라낼 범위와 배치 ──────────────────────────────
CROP = (52, 150, 992, 701)          # 위·좌우의 빈 여백을 덜어낸다
SCALE = 2                             # 글자를 또렷하게 하려고 2배로 얹는다
PAD = 30                              # 그림 둘레 여백
IW, IH = (CROP[2] - CROP[0]) * SCALE, (CROP[3] - CROP[1]) * SCALE   # 1960×1102
LEGEND_W = 860
W, H = PAD * 2 + IW + LEGEND_W, PAD * 2 + IH
BG = "#111519"                        # 원본 배경색(17,21,28)에 맞춘 값

def P(x, y):
    """원본 픽셀 좌표 → 캔버스 좌표."""
    return ((x - CROP[0]) * SCALE + PAD, (y - CROP[1]) * SCALE + PAD)

# 원본 좌표 (마커를 찍어 눈으로 확인한 값)
AORTA  = P(465, 387)
IVC    = P(552, 402)
BODY   = P(515, 500)
SYMP_L = P(439, 459)
SYMP_R = P(606, 457)
KID_L  = P(305, 490)
KID_R  = P(760, 445)
CANAL  = P(515, 592)

TARGET = "#4ade80"   # 표적
DANGER = "#ff5a5a"   # 위험
PLAIN  = "#dfe6ee"   # 지형지물

def _font_css():
    fdir = os.environ.get("PRETENDARD_DIR") or os.path.join(REPO, "fonts")
    if not os.path.isdir(fdir):
        fdir = "/tmp/pretendard"
    out = []
    for w, f in ((400, "Pretendard-Regular.otf"), (700, "Pretendard-Bold.otf")):
        p = os.path.join(fdir, f)
        if not os.path.exists(p):
            sys.exit(f"Pretendard 폰트가 없다: {p}\n  → scripts/README_로컬실행.md 참고")
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        out.append("@font-face{font-family:Pr;font-weight:%d;src:url(data:font/otf;base64,%s)}"
                   % (w, b64))
    return "".join(out)

def _img_href():
    return "data:image/png;base64," + base64.b64encode(open(SRC, "rb").read()).decode()

def marker(n, x, y, color):
    """번호 원판. 그림 위에 얹히므로 작고 담백하게."""
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="24" fill="#0a0d11" fill-opacity=".92" '
            f'stroke="{color}" stroke-width="3.5"/>'
            f'<text x="{x:.0f}" y="{y+9:.0f}" text-anchor="middle" class="num" '
            f'fill="{color}">{n}</text>')

def leader(x1, y1, x2, y2, color, dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
            f'stroke="{color}" stroke-width="2" stroke-opacity=".85"{d}/>')

ARROW_DEFS = """<defs>
 <marker id="ah_t" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
   orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="%s"/></marker>
 <marker id="ah_d" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6"
   orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="%s"/></marker>
</defs>""" % (TARGET, DANGER)

def arrow(p1, p2, color, dash="", width=5):
    """짧은 방향 화살표. 길게 그으면 없는 경로를 지어낸 것처럼 보인다."""
    mk = "ah_t" if color == TARGET else "ah_d"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<line x1="{p1[0]:.0f}" y1="{p1[1]:.0f}" x2="{p2[0]:.0f}" y2="{p2[1]:.0f}" '
            f'stroke="{color}" stroke-width="{width}" stroke-linecap="round"'
            f'{d} marker-end="url(#{mk})"/>')

def spot(pt, color, r=11):
    """정확한 지점을 가리키는 작은 고리 — 구조물을 가리지 않는다."""
    return (f'<circle cx="{pt[0]:.0f}" cy="{pt[1]:.0f}" r="{r}" fill="none" '
            f'stroke="{color}" stroke-width="3"/>')

def tag(n, pt, at, color):
    """구조물은 고리로 짚고, 번호는 빈 곳으로 옮겨 지시선으로 잇는다."""
    return (spot(pt, color) + leader(pt[0], pt[1], at[0], at[1], color)
            + marker(n, at[0], at[1], color))

def _b(t):
    """SVG text는 <b>를 모르므로 tspan으로 바꾼다."""
    return t.replace("<b>", '<tspan font-weight="700">').replace("</b>", "</tspan>")

def legend(rows, note):
    """오른쪽 설명 칸. 번호 - 굵은 제목 - 한 줄 설명."""
    x = PAD + IW + 44
    out = []
    yy = PAD + 40
    for line in note:
        out.append(f'<text x="{x}" y="{yy}" class="lgh">{line}</text>')
        yy += 42
    y = yy + 66
    for n, color, head, body in rows:
        out.append(f'<circle cx="{x+18}" cy="{y-14}" r="22" fill="none" '
                   f'stroke="{color}" stroke-width="3.5"/>')
        out.append(f'<text x="{x+18}" y="{y-4}" text-anchor="middle" class="num" '
                   f'fill="{color}">{n}</text>')
        out.append(f'<text x="{x+56}" y="{y-1}" class="lgt" fill="{color}">{head}</text>')
        yy = y + 47
        for line in body:
            out.append(f'<text x="{x+56}" y="{yy}" class="lgb">{_b(line)}</text>')
            yy += 43
        y = yy + 38
    return "".join(out)

def build(overlay, rows, note, out_name):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"
 viewBox="0 0 {W} {H}">
<style>{_font_css()}
 text{{font-family:Pr,sans-serif;fill:{PLAIN}}}
 .num{{font-size:27px;font-weight:700}}
 .cap{{font-size:26px;font-weight:700}}
 .lgh{{font-size:31px;font-weight:700;fill:#9fb2c6}}
 .lgt{{font-size:43px;font-weight:700}}
 .lgb{{font-size:35px;fill:#c9d5e3}}
</style>
<rect width="{W}" height="{H}" fill="{BG}"/>\n{ARROW_DEFS}
<svg x="{PAD}" y="{PAD}" width="{IW}" height="{IH}"
     viewBox="{CROP[0]} {CROP[1]} {CROP[2]-CROP[0]} {CROP[3]-CROP[1]}">
  <image href="{_img_href()}" x="0" y="0" width="1021" height="701"/>
</svg>
{overlay}
{legend(rows, note)}
</svg>'''
    tmp = os.path.join(ASSETS, "_ca_tmp.svg")
    open(tmp, "w", encoding="utf-8").write(svg)
    png = os.path.join(ASSETS, "_ca_tmp.png")
    _raster(tmp, png)
    from PIL import Image
    im = Image.open(png).convert("RGB")
    im.thumbnail((1900, 1900), Image.LANCZOS)
    dst = os.path.join(ASSETS, out_name + ".webp")
    im.save(dst, "WEBP", quality=86, method=6)
    os.remove(tmp); os.remove(png)
    print(f"  {out_name}.webp  {im.size[0]}×{im.size[1]}  {os.path.getsize(dst)//1024} KB")

def _raster(svg_path, png_path):
    from playwright.sync_api import sync_playwright
    html = (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>html,body{{margin:0;background:{BG}}}</style></head>'
            f'<body>{open(svg_path, encoding="utf-8").read()}</body></html>')
    hp = svg_path + ".html"
    open(hp, "w", encoding="utf-8").write(html)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg.goto("file://" + hp)
        pg.wait_for_timeout(700)
        pg.screenshot(path=png_path, clip={"x": 0, "y": 0, "width": W, "height": H})
        b.close()
    os.remove(hp)

# ══════════════ ① 표적 그림 (14쪽) ══════════════
def fig_target():
    ov = [
        # 표적은 작은 결절이라 번호로 덮으면 안 된다 — 고리로 짚고 번호는 옆으로 뺀다.
        # 척추체 절단면은 결이 균일해 번호를 얹어도 가리는 것이 없다.
        tag("1", SYMP_L, P(462, 522), TARGET),
        tag("1", SYMP_R, P(578, 522), TARGET),
        marker("2", *AORTA, PLAIN),
        marker("3", *IVC, PLAIN),
        marker("4", *KID_L, PLAIN),
        marker("4", *KID_R, PLAIN),
        marker("5", *P(520, 522), PLAIN),
        marker("6", *CANAL, PLAIN),
    ]
    rows = [
        ("1", TARGET, "교감신경절 — 표적",
         ["척추체 <b>전외측 모서리</b>의 홈에 좌우로 하나씩.",
          "L2–L3에서 신경절 밀도가 가장 높다."]),
        ("2", PLAIN, "복부대동맥", ["척추체 바로 앞, <b>환자 좌측</b>."]),
        ("3", PLAIN, "하대정맥(IVC)", ["척추체 바로 앞, <b>환자 우측</b>. 벽이 얇다."]),
        ("4", PLAIN, "신장", ["지방에 싸여 <b>후외측</b>. 우신이 더 낮다."]),
        ("5", PLAIN, "L3 척추체", ["바늘이 끝까지 붙어 가는 기준면."]),
        ("6", PLAIN, "척수강 · 마미", ["표적에서 <b>내측</b>으로 벗어나면 만나는 곳."]),
    ]
    build("".join(ov), rows,
          ["L3 척추체 높이 · 위에서 내려다본 축상면",
           "화면 왼쪽 = 환자 좌측 · 화면 아래 = 등(후방)"],
          "ca_target")

# ══════════════ ② 회피 그림 (합병증 뒤) ══════════════
def fig_avoid():
    # 환자 우측(화면 오른쪽) 하나만 그린다. 좌우를 다 그리면 화살표가 엉켜 못 읽는다.
    ov = [
        # 들어오는 방향 — 뼈에 붙여 후외측에서. 짧게, 프레임 안에서만.
        arrow(P(706, 572), P(628, 476), TARGET, "", 6),
        tag("1", SYMP_R, P(578, 522), TARGET),
        spot(SYMP_L, TARGET),

        # 표적에서 어느 쪽으로 벗어나면 무엇을 만나는가 — 짧게, 방향만.
        arrow(P(634, 450), P(704, 442), DANGER, "10 7", 5),   # 외측 → 신장
        arrow(P(596, 436), P(564, 410), DANGER, "10 7", 5),   # 전방 → IVC
        arrow(P(618, 481), P(632, 558), DANGER, "10 7", 5),   # 후방 → 추간공·신경근

        marker("2", *KID_R, DANGER),
        marker("2", *KID_L, DANGER),
        marker("3", *IVC, DANGER),
        marker("3", *AORTA, DANGER),
        marker("4", *CANAL, DANGER),
    ]
    rows = [
        ("1", TARGET, "여기서 멈춘다",
         ["척추체 <b>전외측 모서리</b>. 뼈에 붙인 채 외측으로",
          "walk 해서 여기까지만 — 화살표가 들어오는 방향."]),
        ("2", DANGER, "외측으로 벗어나면 → 신장",
         ["정중선 ~7 cm보다 더 벌리면 지난다.",
          "마른 환자·신장하수에서 더 가깝다."]),
        ("3", DANGER, "전방으로 넘기면 → 대혈관",
         ["측면상에서 <b>척추체 전연</b>을 넘기는 순간",
          "대동맥(좌)·IVC(우). 우측 접근은 IVC가 먼저."]),
        ("4", DANGER, "뒤로 물러나면 → 추간공",
         ["척추체 뒤로 물러나면 신경근·경막외.",
          "조영제로 반드시 배제한다."]),
    ]
    build("".join(ov), rows,
          ["같은 L3 단면 — 무엇을 피하나 (환자 우측 기준)",
           "화면 왼쪽 = 환자 좌측 · 화면 아래 = 등(후방)"],
          "ca_avoid")

if __name__ == "__main__":
    if not os.path.exists(SRC):
        sys.exit(f"원본이 없다: {SRC}")
    fig_target()
    fig_avoid()
