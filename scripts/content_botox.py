# -*- coding: utf-8 -*-
"""정형외과 통증에서의 보툴리눔 톡신 — 문헌고찰 발표 슬라이드 콘텐츠.

deck_html.render_deck() 스키마를 따른다.
모든 SVG 일러스트는 인라인(외부 리소스 0) — 아티팩트 CSP 대응.
"""

SERIES = "정형외과 통증 · 보툴리눔 톡신 문헌고찰 · 2026 · v1.0"


def PM(pmid):
    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"


# ════════════════════════════════════════════════════════════
#  공통 SVG 부품
# ════════════════════════════════════════════════════════════
SKIN, SKINL = "#C9A98C", "#F3E7DC"
MUS, MUSL = "#A8352A", "#EFCDC5"
BONE, BONEL = "#B08D6A", "#EADFCF"
NRV, NRVD = "#5548B0", "#332876"
INK, MUTED = "#181A2E", "#6E6E88"


def needle(x1, y1, x2, y2, w=3):
    """바늘 + 주사기 몸통. (x1,y1)=바늘 끝(표적), (x2,y2)=손잡이 쪽."""
    import math
    ang = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (f'<g><line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#33355A" stroke-width="{w}"/>'
            f'<rect x="{x2}" y="{y2-11}" width="62" height="22" rx="4" '
            f'transform="rotate({ang:.1f} {x2} {y2})" fill="#DAD6EA" stroke="#585976" stroke-width="2"/></g>')


def target(cx, cy, r=9, halo=18):
    return (f'<circle cx="{cx}" cy="{cy}" r="{halo}" fill="none" stroke="{MUS}" '
            f'stroke-width="2" stroke-dasharray="4 4"/>'
            f'<circle class="a-spark" cx="{cx}" cy="{cy}" r="{r}" fill="{MUS}"/>')


# ── 기전 ──────────────────────────────────────────────────
# ── 기전 (Higgsfield 생성 일러스트 + 한글 라벨 오버레이) ──────
#   그림은 글자 없이 생성하고, 라벨은 % 좌표로 얹는다.
MECH_A_IMG = """<div class="figpanel" style="flex:1"><div class="pt">신경근접합부 · 단면</div>
<div class="figimg"><img src="__FIG_NMJ__" alt="신경근접합부 — 시냅스 소포와 절단된 SNAP-25"/>
 <span class="lb ind" style="left:20%;top:9%">운동신경 축삭</span>
 <span class="lb" style="left:47%;top:37%">ACh 소포</span>
 <span class="lb red" style="left:50%;top:60%">SNAP-25 절단 → 방출 차단</span>
 <span class="lb" style="left:71%;top:79%">근육섬유 · 접합주름</span>
</div>
<div class="pl">소포는 그대로 있는데 <b>막과 융합하지 못한다</b> — 신경은 살아 있고 전달만 끊긴다</div></div>"""

MECH_A_TXT = """<div class="figpanel txt" style="flex:1.32"><div class="pt">일어나는 일 · 순서대로</div>
<ul class="m">
<li><b>① 결합:</b> 무거운사슬이 종말막의 <b>SV2 수용체</b>에 붙는다 — <b>활동 중인 종말</b>일수록 잘 들어간다.</li>
<li><b>② 절단:</b> 가벼운사슬이 세포질로 나와 <b>SNAP-25</b>를 자른다 → SNARE 복합체가 못 만들어진다.</li>
<li class="red"><b>③ 차단:</b> 소포가 막과 융합하지 못해 ACh 방출이 멈춘다 = <b>화학적 탈신경</b>.</li>
<li class="green"><b>④ 고리 절단:</b> 과수축 → 허혈 → 통증 → 다시 과수축. 이 <b>악순환</b>이 끊긴다.</li>
<li class="none"><b>회복:</b> 축삭이 새 가지를 내며 <b>12–16주</b>에 되돌아온다 — 신경은 파괴되지 않는다.</li>
</ul></div>"""

MECH_B_IMG = """<div class="figpanel" style="flex:1"><div class="pt">통각신경 종말 · 단면</div>
<div class="figimg"><img src="__FIG_NOCI__" alt="통각신경 종말 — 신경펩타이드 방출 차단과 역행성 수송"/>
 <span class="lb" style="left:30%;top:10%">통각 종말 (C섬유)</span>
 <span class="lb red" style="left:40%;top:60%">SP · CGRP 방출 차단</span>
 <span class="lb ind" style="left:60%;top:27%">역행성 축삭수송</span>
 <span class="lb ind" style="left:80%;top:82%">후근신경절</span>
</div>
<div class="pl">같은 SNARE 기전이 <b>통각 종말에서도</b> 작동한다 — 근육과 무관한 진통</div></div>"""

MECH_B_TXT = """<div class="figpanel txt" style="flex:1.32"><div class="pt">근이완으로 설명되지 않는 것들</div>
<ul class="m">
<li><b>① 신경펩타이드 차단:</b> 통각 종말에서 <b>substance P · CGRP</b> 방출이 막힌다.</li>
<li><b>② 수용체 감소:</b> <b>TRPV1</b>이 막으로 못 나가 역치가 오른다 → <b>말초 감작 ↓</b>.</li>
<li class="green"><b>③ 중추까지:</b> <b>역행성 축삭수송</b>으로 후근신경절·척수후각에 도달 → <b>중추 감작 ↓</b>.</li>
<li class="none accent"><b>증거 둘:</b> 근력약화 없이 진통이 나고, <b>진통이 근력 회복보다 오래</b> 간다.</li>
<li class="red"><b>그래서:</b> 관절강·근막·신경 주위처럼 <b>근육이 아닌 곳</b>에 놓아도 듣는다.</li>
</ul></div>"""

# ── 승모근 5점 + 안전 단면 ──────────────────────────────
SVG_TRAP_A = f'''<div class="figpanel"><div class="pt">상부 승모근 · 5점 분할 (뒤에서 본 모습)</div>
<svg viewBox="0 0 300 230" role="img">
 <path d="M18 128 Q86 80 150 76 Q214 80 282 128 L282 90 Q214 42 150 38 Q86 42 18 90 Z"
       fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <circle cx="150" cy="26" r="5" fill="{BONE}"/>
 <text x="162" y="30" font-size="11.5" font-weight="700" fill="#8a6d52">C7 극돌기</text>
 <circle cx="20" cy="109" r="6" fill="{BONE}"/>
 <text x="12" y="136" font-size="11.5" font-weight="700" fill="#8a6d52">견봉</text>
 <circle cx="280" cy="109" r="6" fill="{BONE}"/>
 <text x="288" y="136" text-anchor="end" font-size="11.5" font-weight="700" fill="#8a6d52">견봉</text>
 {target(74,70,7,13)}{target(112,61,7,13)}{target(150,57,7,13)}{target(188,61,7,13)}{target(226,70,7,13)}
 <text x="150" y="168" text-anchor="middle" font-size="12.5" font-weight="800" fill="{MUS}">가장 두꺼운 지점 1점 + 주위 4점</text>
 <text x="150" y="190" text-anchor="middle" font-size="12.5" font-weight="700" fill="{NRVD}">각 10–20 U · 한쪽 총 50–100 U</text>
 <line x1="40" y1="204" x2="260" y2="204" stroke="#E0DEEC" stroke-width="1.5"/>
 <text x="150" y="222" text-anchor="middle" font-size="11.5" font-weight="700" fill="{MUTED}">＊두께는 초음파로 확인 — 촉진은 깊이를 알려주지 않는다</text>
</svg>
<div class="pl">Jiang 2021 초음파 유도 <b>5점법</b> · 한쪽 <b>100 U 초과 금지</b></div></div>'''

SVG_TRAP_B = f'''<div class="figpanel warn"><div class="pt">기흉을 피하는 진입 — 단면</div>
<svg viewBox="0 0 300 230" role="img">
 <text x="150" y="16" text-anchor="middle" font-size="12" font-weight="800" fill="#2E6B3E">✓ 접선(tangential) 진입 · 13 mm 바늘</text>
 <path d="M62 96 q44 -46 88 -46 q44 0 88 46 q-44 22 -88 22 q-44 0 -88 -22 Z"
       fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <path d="M58 94 q-13 -13 -3 -26" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
 <path d="M242 94 q13 -13 3 -26" fill="none" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>
 {needle(110, 84, 246, 46)}
 <text x="150" y="128" text-anchor="middle" font-size="12" font-weight="800" fill="#7a221a">근육을 집게로 들어올린다</text>
 <ellipse cx="58" cy="156" rx="30" ry="10" fill="{BONEL}" stroke="{BONE}" stroke-width="2"/>
 <ellipse cx="150" cy="156" rx="30" ry="10" fill="{BONEL}" stroke="{BONE}" stroke-width="2"/>
 <ellipse cx="242" cy="156" rx="30" ry="10" fill="{BONEL}" stroke="{BONE}" stroke-width="2"/>
 <text x="150" y="160" text-anchor="middle" font-size="11" font-weight="700" fill="#8a6d52">늑골</text>
 <rect x="16" y="178" width="268" height="18" rx="6" fill="#DCE6EA" stroke="#8FA5B0" stroke-width="2"/>
 <text x="150" y="192" text-anchor="middle" font-size="11.5" font-weight="800" fill="#41616f">흉막 · 폐</text>
 <line x1="272" y1="104" x2="280" y2="176" stroke="{MUS}" stroke-width="3" stroke-dasharray="5 4"/>
 <text x="290" y="100" text-anchor="end" font-size="15" font-weight="900" fill="{MUS}">✗</text>
 <text x="150" y="218" text-anchor="middle" font-size="12" font-weight="800" fill="{MUS}">✗ 수직 진입 · 50–60 mm 바늘 금지</text>
</svg>
<div class="pl">늑골·흉막을 <b>초음파로 먼저 확인</b> — 마른 체형일수록 여유가 없다</div></div>'''

# ── 사각근 / 흉곽출구 ───────────────────────────────────
SVG_SCALENE = f'''<svg viewBox="0 0 760 300" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <rect x="20" y="18" width="500" height="264" rx="14" fill="#181A2E"/>
 <text x="270" y="44" text-anchor="middle" font-size="14" font-weight="800" fill="#9C9CBC">목 횡단면 · 초음파 시야 (쇄골 상부)</text>
 <ellipse cx="150" cy="150" rx="70" ry="46" fill="#7d8b91" stroke="#CFCEE4" stroke-width="2"/>
 <text x="150" y="128" text-anchor="middle" font-size="13" font-weight="800" fill="#181A2E">전사각근</text>
 <ellipse cx="330" cy="162" rx="74" ry="48" fill="#6f7d83" stroke="#CFCEE4" stroke-width="2"/>
 <text x="330" y="168" text-anchor="middle" font-size="13" font-weight="800" fill="#181A2E">중사각근</text>
 <circle cx="238" cy="140" r="12" fill="#2A2C52" stroke="#9B8CF0" stroke-width="2.5"/>
 <circle cx="244" cy="166" r="11" fill="#2A2C52" stroke="#9B8CF0" stroke-width="2.5"/>
 <circle cx="232" cy="190" r="10" fill="#2A2C52" stroke="#9B8CF0" stroke-width="2.5"/>
 <text x="252" y="222" font-size="12.5" font-weight="800" fill="#9B8CF0">상완신경총 (C5–T1)</text>
 <circle cx="112" cy="208" r="15" fill="#7a2a2a" stroke="#e8a79f" stroke-width="2.5"/>
 <text x="60" y="242" font-size="12" font-weight="800" fill="#e8a79f">쇄골하동맥</text>
 <path d="M46 244 Q240 268 494 250" fill="none" stroke="#8FA5B0" stroke-width="5"/>
 <text x="400" y="272" font-size="12.5" font-weight="800" fill="#8FA5B0">흉막 돔 · 폐첨</text>
 <line x1="34" y1="70" x2="140" y2="164" stroke="#F6F5FB" stroke-width="3.5"/>
 <text x="40" y="62" font-size="12.5" font-weight="800" fill="#F6F5FB">평면내(in-plane) 진입</text>
 <circle class="a-spark" cx="148" cy="170" r="10" fill="#A8352A"/>
 <rect x="546" y="30" width="196" height="240" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="562" y="58" font-size="14" font-weight="800" fill="{NRVD}">사각근 주사 원칙</text>
 <text x="562" y="86" font-size="12.5" fill="#33355A">· 전사각근 <tspan font-weight="800">25–50 U</tspan></text>
 <text x="562" y="108" font-size="12.5" fill="#33355A">· 중사각근 병행 시 총 <tspan font-weight="800">≤75 U</tspan></text>
 <text x="562" y="130" font-size="12.5" fill="#33355A">· <tspan font-weight="800">초음파 필수</tspan> (맹목 금지)</text>
 <text x="562" y="152" font-size="12.5" fill="#33355A">· 근복 <tspan font-weight="800">중앙</tspan>, 신경총에서 이격</text>
 <text x="562" y="174" font-size="12.5" fill="#33355A">· 흡인 후 서서히 주입</text>
 <text x="562" y="200" font-size="12.5" font-weight="800" fill="{MUS}">피해야 할 것</text>
 <text x="562" y="222" font-size="12.5" fill="{MUS}">· 흉막 돔(폐첨) 아래로 진행</text>
 <text x="562" y="244" font-size="12.5" fill="{MUS}">· 고용량·고용적 → 연하곤란</text>
 <text x="562" y="262" font-size="11.5" fill="{MUTED}">· 양측 동시 주사</text>
</svg>'''

# ── 외측상과염 ──────────────────────────────────────────
SVG_ELBOW = f'''<svg viewBox="0 0 720 280" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <path d="M40 84 q34 -20 66 -6 l0 96 q-32 14 -66 -6 Z" fill="{SKINL}" stroke="{SKIN}" stroke-width="2.5"/>
 <text x="72" y="70" text-anchor="middle" font-size="12.5" font-weight="700" fill="#8a6d52">상완</text>
 <path d="M106 80 Q250 68 380 94 Q422 102 440 120 L440 166 Q418 184 380 192 Q250 216 106 172 Z"
       fill="{SKINL}" stroke="{SKIN}" stroke-width="2.5"/>
 <text x="272" y="240" text-anchor="middle" font-size="12.5" font-weight="700" fill="#8a6d52">전완 (손등이 위로 · 회내위)</text>
 <circle cx="126" cy="128" r="17" fill="{BONEL}" stroke="{BONE}" stroke-width="2.5"/>
 <text x="126" y="196" text-anchor="middle" font-size="12.5" font-weight="800" fill="#8a6d52">외상과</text>
 <path d="M144 112 Q236 108 302 124 Q364 138 420 148" fill="none" stroke="{MUS}" stroke-width="16" opacity=".28" stroke-linecap="round"/>
 <text x="330" y="98" text-anchor="middle" font-size="12.5" font-weight="800" fill="#7a221a">ECRB · EDC 근복</text>
 {target(236, 118, 10, 21)}
 <line x1="126" y1="128" x2="236" y2="118" stroke="{NRVD}" stroke-width="2" stroke-dasharray="6 5"/>
 <text x="182" y="158" text-anchor="middle" font-size="12" font-weight="800" fill="{NRVD}">외상과에서 원위 4–5 cm</text>
 {needle(236, 118, 344, 44)}
 <rect x="470" y="26" width="230" height="118" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="486" y="52" font-size="13.5" font-weight="800" fill="{NRVD}">용량 · 근거</text>
 <text x="486" y="76" font-size="12.5" fill="#33355A">· Botox <tspan font-weight="800">50–60 U</tspan> 1–2점</text>
 <text x="486" y="98" font-size="12.5" fill="#33355A">· 메타분석: 위약 &gt; <tspan font-weight="800">최대 16주</tspan></text>
 <text x="486" y="120" font-size="12.5" fill="#33355A">· 스테로이드와 12주 후 대등</text>
 <rect x="470" y="158" width="230" height="104" rx="12" fill="#FBF1EF" stroke="#EBD2CC" stroke-width="1.5"/>
 <text x="486" y="184" font-size="13.5" font-weight="800" fill="{MUS}">대가 — 반드시 설명</text>
 <text x="486" y="208" font-size="12.5" fill="{MUS}">· 3–4번째 손가락 신전 약화</text>
 <text x="486" y="230" font-size="12.5" fill="{MUS}">· 악력 저하 2–4주(고용량 8–12주)</text>
 <text x="486" y="252" font-size="12" fill="{MUTED}">· 손 쓰는 직업군은 신중히</text>
</svg>'''

# ── 종아리 ──────────────────────────────────────────────
SVG_CALF = f'''<svg viewBox="0 0 720 300" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <path d="M336 18 q56 0 64 42 q16 80 4 132 q-8 36 -12 66 l-56 0 q-4 -30 -12 -66
          q-12 -52 4 -132 q8 -42 64 -42 Z" fill="{SKINL}" stroke="{SKIN}" stroke-width="2.5" transform="translate(-24 0)"/>
 <path d="M338 196 q-6 42 -2 78" fill="none" stroke="{NRVD}" stroke-width="3" stroke-dasharray="5 5"/>
 <circle cx="337" cy="240" r="8" fill="{NRVD}"/>
 <path d="M276 52 q32 -18 58 0 q22 62 4 108 q-32 16 -64 0 q-18 -46 2 -108 Z" fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <path d="M334 52 q32 -18 56 0 q20 58 2 100 q-30 14 -60 0 q-16 -44 2 -100 Z" fill="#E5C0B8" stroke="{MUS}" stroke-width="2.5"/>
 <text x="300" y="38" text-anchor="middle" font-size="12.5" font-weight="800" fill="#7a221a">내측두</text>
 <text x="376" y="38" text-anchor="middle" font-size="12.5" font-weight="800" fill="#7a221a">외측두</text>
 <text x="334" y="186" text-anchor="middle" font-size="13" font-weight="800" fill="#7a221a">비복근</text>
 {target(303, 100, 9, 18)}{target(371, 96, 9, 18)}
 {target(295, 144, 8, 16)}{target(379, 138, 8, 16)}
 {needle(303, 100, 196, 40)}
 <line x1="328" y1="240" x2="256" y2="240" stroke="{NRVD}" stroke-width="1.5" stroke-dasharray="3 3"/>
 <text x="248" y="236" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">경골신경 — 깊이</text>
 <text x="248" y="258" text-anchor="end" font-size="12" font-weight="700" fill="{MUTED}">총비골신경 — 외측(족하수)</text>
 <rect x="446" y="30" width="256" height="112" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="462" y="56" font-size="13.5" font-weight="800" fill="{NRVD}">종아리 경련 · 근거 기반 용량</text>
 <text x="462" y="80" font-size="12.5" fill="#33355A">· 비복근 <tspan font-weight="800">한쪽 100 U</tspan> 분할 (Restivo)</text>
 <text x="462" y="102" font-size="12.5" fill="#33355A">· 발 소근육 <tspan font-weight="800">한쪽 30 U</tspan></text>
 <text x="462" y="124" font-size="12.5" fill="#33355A">· 내·외측두 각 2–3점, 근복 중앙</text>
 <rect x="446" y="156" width="256" height="112" rx="12" fill="#FBF1EF" stroke="#EBD2CC" stroke-width="1.5"/>
 <text x="462" y="182" font-size="13.5" font-weight="800" fill="{MUS}">고령에서 특히 조심</text>
 <text x="462" y="206" font-size="12.5" fill="{MUS}">· 족저굴곡 약화 → 계단·경사 불안</text>
 <text x="462" y="228" font-size="12.5" fill="{MUS}">· 총비골신경 확산 → 족하수·낙상</text>
 <text x="462" y="250" font-size="12" fill="{MUTED}">· 보행 불안정·근감소증이면 감량</text>
</svg>'''

# ── 족저근막 ────────────────────────────────────────────
SVG_PLANTAR = f'''<svg viewBox="0 0 720 290" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <path d="M56 168 q8 -52 60 -60 q64 -10 144 -26 q80 -16 144 -12 q50 4 52 28 q2 24 -50 32
          q-88 14 -156 28 q-68 16 -128 24 q-56 8 -66 -14 Z" fill="{SKINL}" stroke="{SKIN}" stroke-width="2.5"/>
 <ellipse cx="82" cy="146" rx="32" ry="28" fill="{BONEL}" stroke="{BONE}" stroke-width="2.5"/>
 <text x="82" y="110" text-anchor="middle" font-size="12.5" font-weight="800" fill="#8a6d52">종골</text>
 <path d="M100 176 Q214 198 344 188 Q400 184 428 176" fill="none" stroke="#D8B08C" stroke-width="13" opacity=".7" stroke-linecap="round"/>
 <text x="336" y="146" text-anchor="middle" font-size="12.5" font-weight="800" fill="#8a6d52">족저근막 (내측 다발)</text>
 {target(122, 180, 10, 21)}
 <text x="122" y="238" text-anchor="middle" font-size="12.5" font-weight="800" fill="{MUS}">① 종골 내측 기시부</text>
 <text x="122" y="262" text-anchor="middle" font-size="14" font-weight="900" fill="{NRVD}">40 U</text>
 {target(272, 192, 10, 21)}
 <text x="286" y="238" text-anchor="middle" font-size="12.5" font-weight="800" fill="{MUS}">② 족궁 최대 압통점</text>
 <text x="286" y="262" text-anchor="middle" font-size="14" font-weight="900" fill="{NRVD}">30 U</text>
 {needle(122, 180, 214, 66)}
 <rect x="470" y="26" width="234" height="108" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="486" y="52" font-size="13.5" font-weight="800" fill="{NRVD}">Babcock 2005 · 2점법</text>
 <text x="486" y="76" font-size="12.5" fill="#33355A">· 한 발 총 <tspan font-weight="800">70 U</tspan> (40 + 30)</text>
 <text x="486" y="98" font-size="12.5" fill="#33355A">· 근막 <tspan font-weight="800">내부</tspan>로 · 지방패드 아님</text>
 <text x="486" y="120" font-size="12.5" fill="#33355A">· 3주·8주 통증·기능 유의 개선</text>
 <rect x="470" y="150" width="234" height="118" rx="12" fill="#EEF4EF" stroke="#CFE0D3" stroke-width="1.5"/>
 <text x="486" y="176" font-size="13.5" font-weight="800" fill="#2E6B3E">대안 표적</text>
 <text x="486" y="200" font-size="12.5" fill="#33355A">비복근 <tspan font-weight="800">내측두 70 U</tspan></text>
 <text x="486" y="222" font-size="12.5" fill="#33355A">— 종아리 단축이 근막을 당기는</text>
 <text x="486" y="242" font-size="12.5" fill="#33355A">　 기전을 겨냥 (족부 근력 보존)</text>
 <text x="486" y="262" font-size="11.5" fill="{MUTED}">＊200 U 고용량은 오히려 효과 소실</text>
</svg>'''

# ── 요추 방척추근 ───────────────────────────────────────
SVG_LUMBAR = f'''<svg viewBox="0 0 720 300" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <rect x="322" y="30" width="34" height="230" rx="8" fill="{BONEL}" stroke="{BONE}" stroke-width="2"/>
 <text x="339" y="282" text-anchor="middle" font-size="12" font-weight="700" fill="#8a6d52">극돌기</text>
 <path d="M230 34 q66 -8 84 6 l0 214 q-20 14 -84 6 Z" fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <path d="M448 34 q-66 -8 -84 6 l0 214 q20 14 84 6 Z" fill="{MUSL}" stroke="{MUS}" stroke-width="2.5" opacity=".45"/>
 <text x="272" y="150" text-anchor="middle" font-size="13" font-weight="800" fill="#7a221a">척추기립근</text>
 <text x="272" y="172" text-anchor="middle" font-size="13" font-weight="800" fill="#7a221a">· 다열근</text>
 <text x="406" y="160" text-anchor="middle" font-size="12.5" font-weight="700" fill="{MUTED}">반대측</text>
 {target(276, 62, 8, 16)}{target(276, 106, 8, 16)}{target(276, 150, 8, 16)}
 {target(276, 194, 8, 16)}{target(276, 238, 8, 16)}
 <text x="196" y="66" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">L1</text>
 <text x="196" y="110" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">L2</text>
 <text x="196" y="154" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">L3</text>
 <text x="196" y="198" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">L4</text>
 <text x="196" y="242" text-anchor="end" font-size="12.5" font-weight="800" fill="{NRVD}">L5</text>
 <text x="140" y="154" text-anchor="end" font-size="12.5" font-weight="800" fill="{MUS}">40 U</text>
 <text x="140" y="174" text-anchor="end" font-size="12.5" font-weight="800" fill="{MUS}">× 5레벨</text>
 {needle(276, 106, 396, 44)}
 <rect x="480" y="34" width="222" height="106" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="496" y="60" font-size="13.5" font-weight="800" fill="{NRVD}">Foster 2001 프로토콜</text>
 <text x="496" y="84" font-size="12.5" fill="#33355A">· Botox <tspan font-weight="800">총 200 U</tspan></text>
 <text x="496" y="106" font-size="12.5" fill="#33355A">· 통증 <tspan font-weight="800">심한 쪽</tspan> 방척추 5레벨</text>
 <text x="496" y="128" font-size="12.5" fill="#33355A">· 극돌기에서 외측 2–3 cm</text>
 <rect x="480" y="156" width="222" height="112" rx="12" fill="#FBF1EF" stroke="#EBD2CC" stroke-width="1.5"/>
 <text x="496" y="182" font-size="13.5" font-weight="800" fill="{MUS}">안전</text>
 <text x="496" y="206" font-size="12.5" fill="{MUS}">· 정중선 가까이 깊게 = 위험</text>
 <text x="496" y="228" font-size="12.5" fill="{MUS}">· 흉추로 올라가면 기흉 위험</text>
 <text x="496" y="250" font-size="12" fill="{MUTED}">· 체간 신전근 약화 → 자세 악화</text>
</svg>'''

# ── 이상근 ──────────────────────────────────────────────
SVG_PIRI = f'''<svg viewBox="0 0 720 290" preserveAspectRatio="xMidYMid meet" style="width:100%;height:100%" role="img">
 <path d="M70 60 L250 44 L266 210 L86 240 Z" fill="{BONEL}" stroke="{BONE}" stroke-width="2.5"/>
 <text x="150" y="94" font-size="12.5" font-weight="800" fill="#8a6d52">천골 · 장골</text>
 <circle cx="392" cy="150" r="42" fill="{BONEL}" stroke="{BONE}" stroke-width="2.5"/>
 <text x="392" y="156" text-anchor="middle" font-size="12" font-weight="800" fill="#8a6d52">대전자</text>
 <path d="M186 118 Q286 108 366 132 L370 168 Q286 148 190 158 Z" fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <text x="272" y="106" text-anchor="middle" font-size="13" font-weight="800" fill="#7a221a">이상근</text>
 <path d="M214 176 Q286 190 330 236 Q352 258 362 278" fill="none" stroke="{NRVD}" stroke-width="9" stroke-linecap="round"/>
 <text x="252" y="228" font-size="13" font-weight="800" fill="{NRVD}">좌골신경</text>
 <path d="M84 62 Q220 34 330 66" fill="none" stroke="{MUTED}" stroke-width="18" opacity=".22" stroke-linecap="round"/>
 <text x="104" y="34" font-size="11.5" font-weight="700" fill="{MUTED}">대둔근(표층) — 이 아래가 이상근</text>
 {target(268, 138, 10, 21)}
 {needle(268, 138, 160, 232)}
 <rect x="452" y="26" width="252" height="110" rx="12" fill="#EBE9F4" stroke="#DAD6EA" stroke-width="1.5"/>
 <text x="468" y="52" font-size="13.5" font-weight="800" fill="{NRVD}">용량 · 근거</text>
 <text x="468" y="76" font-size="12.5" fill="#33355A">· <tspan font-weight="800">100–200 U</tspan> (문헌 100–300)</text>
 <text x="468" y="98" font-size="12.5" fill="#33355A">· Fishman: ≥50% 개선 <tspan font-weight="800">65% vs 32%</tspan></text>
 <text x="468" y="120" font-size="12.5" fill="#33355A">· SR 7편 152명 · 근거 fair · Level B</text>
 <rect x="452" y="152" width="252" height="118" rx="12" fill="#FBF1EF" stroke="#EBD2CC" stroke-width="1.5"/>
 <text x="468" y="178" font-size="13.5" font-weight="800" fill="{MUS}">유도가 곧 안전</text>
 <text x="468" y="202" font-size="12.5" fill="{MUS}">· 초음파/투시·EMG 없이는 하지 말 것</text>
 <text x="468" y="224" font-size="12.5" fill="{MUS}">· 좌골신경 먼저 찾고 → 멀리서 진입</text>
 <text x="468" y="246" font-size="12.5" fill="{MUS}">· 이상감각 오면 즉시 중단·후퇴</text>
 <text x="468" y="266" font-size="12" fill="{MUTED}">· 대둔근에만 들어가면 효과 없음</text>
</svg>'''

# ── 안전 3원칙 ──────────────────────────────────────────
SVG_SAFE_A = f'''<div class="figpanel good"><div class="pt">① 고농도 · 소용적</div>
<svg viewBox="0 0 300 200" role="img">
 <text x="76" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="#2E6B3E">100 U / 1–2 mL</text>
 <circle cx="76" cy="100" r="42" fill="none" stroke="#2E6B3E" stroke-width="2" stroke-dasharray="5 4"/>
 <circle cx="76" cy="100" r="30" fill="#CFE0D3" stroke="#2E6B3E" stroke-width="3"/>
 <text x="76" y="105" text-anchor="middle" font-size="12" font-weight="800" fill="#20502F">표적근</text>
 <text x="76" y="180" text-anchor="middle" font-size="12.5" font-weight="800" fill="#2E6B3E">확산 좁음</text>
 <text x="224" y="26" text-anchor="middle" font-size="12" font-weight="800" fill="{MUS}">100 U / 4–8 mL</text>
 <circle class="a-brk" cx="224" cy="100" r="60" fill="none" stroke="{MUS}" stroke-width="2" stroke-dasharray="5 4"/>
 <circle cx="224" cy="100" r="30" fill="#F2C9C1" stroke="{MUS}" stroke-width="3"/>
 <text x="224" y="105" text-anchor="middle" font-size="12" font-weight="800" fill="#7a221a">표적근</text>
 <text x="224" y="180" text-anchor="middle" font-size="12.5" font-weight="800" fill="{MUS}">인접근까지 마비</text>
</svg>
<div class="pl">같은 용량이라도 <b>희석을 늘리면</b> 옆 근육이 약해진다</div></div>'''

SVG_SAFE_B = f'''<div class="figpanel good"><div class="pt">② 신경은 &quot;찾고 나서&quot; 피한다</div>
<svg viewBox="0 0 300 200" role="img">
 <rect x="10" y="10" width="280" height="180" rx="10" fill="#181A2E"/>
 <circle cx="196" cy="112" r="30" fill="#8f9aa0" stroke="#9B8CF0" stroke-width="3"/>
 <circle cx="186" cy="102" r="6" fill="#3a4750"/><circle cx="206" cy="104" r="6" fill="#3a4750"/>
 <circle cx="190" cy="122" r="6" fill="#3a4750"/><circle cx="208" cy="122" r="6" fill="#3a4750"/>
 <text x="196" y="164" text-anchor="middle" font-size="12" font-weight="700" fill="#CFCEE4">신경 (벌집 모양)</text>
 <ellipse cx="96" cy="104" rx="52" ry="40" fill="#6f7d83" stroke="#CFCEE4" stroke-width="2"/>
 <text x="96" y="110" text-anchor="middle" font-size="12.5" font-weight="800" fill="#181A2E">표적근</text>
 <line x1="20" y1="46" x2="88" y2="92" stroke="#F6F5FB" stroke-width="3"/>
 <circle class="a-spark" cx="92" cy="96" r="8" fill="#A8352A"/>
 <path d="M150 60 q26 20 30 44" fill="none" stroke="#9B8CF0" stroke-width="2.5" stroke-dasharray="4 4"/>
 <text x="150" y="52" font-size="12" font-weight="800" fill="#9B8CF0">이 거리를 확보</text>
</svg>
<div class="pl">이상근·사각근·전완 — <b>신경을 먼저 화면에 띄운 뒤</b> 반대편에서 진입</div></div>'''

SVG_SAFE_C = f'''<div class="figpanel good"><div class="pt">③ 흉벽 위에서는 접선으로</div>
<svg viewBox="0 0 300 200" role="img">
 <text x="150" y="22" text-anchor="middle" font-size="11.5" font-weight="700" fill="{MUTED}">승모근 · 능형근 · 견갑하근 · 사각근</text>
 <path d="M44 100 q40 -42 80 -42 q40 0 80 42 q-40 20 -80 20 q-40 0 -80 -20 Z"
       fill="{MUSL}" stroke="{MUS}" stroke-width="2.5"/>
 <line x1="62" y1="98" x2="174" y2="64" stroke="#2E6B3E" stroke-width="3.5"/>
 <text x="188" y="60" font-size="15" font-weight="900" fill="#2E6B3E">✓</text>
 <text x="124" y="136" text-anchor="middle" font-size="12" font-weight="800" fill="#7a221a">근육을 들어올림</text>
 <line x1="244" y1="52" x2="252" y2="150" stroke="{MUS}" stroke-width="3" stroke-dasharray="5 4"/>
 <text x="262" y="50" font-size="15" font-weight="900" fill="{MUS}">✗</text>
 <rect x="16" y="154" width="268" height="16" rx="6" fill="#DCE6EA" stroke="#8FA5B0" stroke-width="2"/>
 <text x="150" y="166" text-anchor="middle" font-size="11.5" font-weight="800" fill="#41616f">흉막 · 폐</text>
</svg>
<div class="pl">집게로 들고 <b>접선 진입</b> · <b>13 mm</b> 바늘 · 늑골·흉막 확인</div></div>'''


# ════════════════════════════════════════════════════════════
#  슬라이드
# ════════════════════════════════════════════════════════════
BOTOX = [


# 01 ─────────────────────────────────────────────────────
{'t': 'title', 'eyebrow': 'Botulinum Toxin in Orthopedic Pain · 문헌고찰',
 'title': '정형외과 통증과<br>보툴리눔 톡신',
 'sub': '어디에 듣는가 · 어떻게 놓는가 · 얼마나 · 무엇을 조심하는가',
 'order': '목어깨 · 팔 · 허리 · 엉덩이 · 무릎 · 종아리 · 발 · 수술후',
 'series': SERIES},

# 02 ─────────────────────────────────────────────────────
{'t': 'bullets', 'eyebrow': '들어가며', 'tag': '이 발표의 틀',
 'title': '“보톡스가 통증에 듣는다”를 부위별로 검증한다',
 'items': [
   (0, '보툴리눔 톡신은 <b>근이완제이면서 동시에 진통제</b>다 — 근력약화 없이도 통증이 주는 현상이 반복 관찰됐다.', ''),
   (0, '그러나 <b>부위마다 근거의 질이 완전히 다르다.</b> 같은 약, 같은 용량이라도 족저근막염은 Level B, 목·어깨 근막통은 임상적 유의성 미달이다.', ''),
   (0, '이 발표는 <b>목에서 발까지</b> 내려가며, 부위마다 <b>① 근거 → ② 주사기법 → ③ 용량 → ④ 부작용 → ⑤ 회피법</b> 순으로 정리한다.', 'accent'),
   (-1, '＊정형외과 통증 대부분에서 보툴리눔은 <b>허가초과(off-label)</b> 사용이다. 국내 급여는 뇌졸중 후 상지경직·경부근긴장이상 등에 한정된다.', 'red'),
 ],
 'stat': [('18', '평가된 통증 증후군 (Jabbari 2018)'), ('3', 'Level A 적응증'), ('6', 'Level B 적응증'), ('12–16주', '1회 효과 지속')],
 'foot': 'Safarpour & Jabbari, Toxicon 2018 · 부위별 최신 메타분석 종합'},

# 03 ─────────────────────────────────────────────────────
{'t': 'figure', 'eyebrow': '기전 ① · 근이완', 'tag': '두 갈래 중 첫째',
 'title': '① 근육을 풀어 통증 고리를 끊는다',
 'svg': MECH_A_IMG + MECH_A_TXT,
 'caption': '표적은 <b>신경이 아니라 신경-근육 사이의 전달</b>이다 — 자르는 것은 신경이 아니라 <b>SNAP-25라는 단백질</b>',
 'foot': 'Matak & Lacković 2014 (Prog Neurobiol) · 제품 첨부문서'},

# 04 ─────────────────────────────────────────────────────
{'t': 'figure', 'eyebrow': '기전 ② · 직접 진통', 'tag': ('두 갈래 중 둘째', 'green'),
 'title': '② 통증 신호 자체를 줄인다',
 'svg': MECH_B_IMG + MECH_B_TXT,
 'caption': '보툴리눔의 진통은 <b>근이완의 부산물이 아니다</b> — 이 두 번째 갈래가 있어야 관절강·근막 주사가 설명된다',
 'foot': 'Mechanisms of BoNT-A action on pain (PMC6723487) · Matak & Lacković 2014'},

# 05 ─────────────────────────────────────────────────────
{'t': 'bullets', 'eyebrow': '기전 · 임상적 함의', 'tag': '시간표',
 'title': '언제 나타나고 언제 사라지나 — 진료 설계의 기준',
 'items': [
   (0, '<b>발현 3–7일 · 최대 2–4주 · 지속 12–16주.</b> 스테로이드처럼 “맞고 바로”가 아니다 → 환자에게 반드시 미리 설명.', ''),
   (0, '<b>진통이 근력약화보다 오래 간다.</b> 근력은 6–8주에 돌아오는데 통증 완화는 12주 이상 가는 경우가 흔하다.', 'accent'),
   (0, '<b>1회로 끝내지 않는다.</b> 자세·작업·근력 같은 근본 부하를 함께 고치지 않으면 3–4개월 뒤 되돌아온다.', ''),
   (0, '<b>재주사는 최소 12주 간격.</b> 3개월 미만 간격·3주 내 보충주사는 중화항체를 만든다.', 'red'),
   (0, '<b>끊을 수 있는 경우도 있다:</b> 약효가 끝나도 재발하지 않는 환자군이 존재한다 — TMD 근막통은 단일 주사 후 <b>2년</b>까지 통증 감소 유지, 족저근막염은 <b>12개월</b> 기능 개선 유지. 반대로 경직·이긴장증처럼 <b>원인이 계속 남는 병은 평생 반복</b>이 원칙.', 'green'),
   (-1, '＊효과 판정은 <b>4주 시점</b>에 한다. 2주에 “효과 없다”고 판단하면 너무 이르다.', 'accent'),
 ],
 'foot': '제품 첨부문서 · 면역원성 리뷰 · Sitnikova 2024(TMD 2년 추적) · PLOS One 2024(족저근막 12개월)'},

# 06 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '총괄', 'tag': ('근거 지도', 'ink'), 'dense': True,
 'title': '부위별 근거 수준 — 어디까지 믿을 수 있나',
 'headers': ['부위 · 질환', '근거 수준', '핵심 근거'],
 'rows': [
   ['목 · 어깨 — <b>승모근 근막통증</b>', '<b>C</b> (제한적)', 'MA 7편: 통계적 유의, <b>임상적 유의성 미달</b>'],
   ['팔꿈치 — <b>외측상과염</b>', '<b>C</b> (상충)', '위약엔 우월, 스테로이드와 대등 · 손가락 약화'],
   ['허리 — <b>만성 요통</b> (방척추근)', '<b>B</b>', 'Foster 2001 · SR/MA (Eur J Pain 2025)'],
   ['엉덩이 — <b>이상근증후군</b>', '<b>B</b>', 'SR 7편 152명 · Fishman 2002'],
   ['무릎 — 관절강내 (OA · 인공관절 후)', '<b>B</b>', 'Singh 2010 · IA 메타 6편 348명'],
   ['종아리 — <b>근경련</b> (당뇨병성 신경병증 · 협착)', '<b>B</b>', 'Restivo 2018 RCT · Park 2017 RCT'],
   ['발 — <b>족저근막염</b>', '<b>B</b>', 'RCT 7편 305명 메타 (PLOS One 2024)'],
   ['<b>수술후 절개부 신경통</b> (부위 무관)', '<b>A</b>', '외상후신경통 — AAN 기준 effective (Jabbari 2018)'],
 ],
 'note': 'A=효과 있음 · B=아마 효과 있음 · C=효과 가능성(AAN 분류) · <b>목에서 발까지</b> 정렬하고, 부위를 가리지 않는 <b>수술후 신경통</b>을 맨 아래 두었다.',
 'foot': 'Safarpour & Jabbari, Toxicon 2018 + 2024–2025 최신 메타분석 갱신'},

# 07 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '약제', 'tag': '제제·희석', 'dense': True,
 'title': '단위(U)는 제품마다 다른 화폐다',
 'headers': ['제제', '대표 제품', '환산', '메모'],
 'rows': [
   ['onabotulinumtoxinA', 'Botox', '<b>1</b> (기준)', '대부분 통증 문헌의 기준 단위'],
   ['abobotulinumtoxinA', 'Dysport', '<b>2.5–3</b> : 1', '문헌마다 비율 상이 — 기계적 환산 금지'],
   ['incobotulinumtoxinA', 'Xeomin', '<b>≈1</b> : 1', '복합단백 없음 → 항체 위험 낮음'],
   ['국내 제제', 'Botulax · Nabota · Coretox 등', '<b>≈1</b> : 1 (표기상)', '단위당 신경독소량은 제품별로 다름'],
 ],
 'note': '<b>희석:</b> 100 U + 생리식염수 <b>2 mL = 5 U/0.1 mL</b>가 표준 · 정밀 표적은 <b>1 mL(고농도·소용적)</b> · <b>희석을 늘릴수록 옆 근육이 약해진다.</b>',
 'foot': '제품 간 단위는 상호 교환 불가 — 문헌의 용량은 그 문헌의 제제 기준으로만 읽는다'},

# 08 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '승모근 · 근막통증 ①', 'tag': ('긍정 근거', 'green'),
 'title': 'Göbel 2006 — 가장 강한 긍정 RCT',
 'items': [
   (0, '<b>대상:</b> 상부 등·어깨 <b>근막통증증후군</b>(활성 유발점 보유) 환자를 위약과 비교한 다기관 이중맹검 RCT.', ''),
   (0, '<b>방법:</b> Dysport <b>총 400 U</b>를 <b>최대 10개 유발점</b>에 분할(한 점당 약 40 U) 1회 주사.', ''),
   (0, '<b>결과:</b> 위약 대비 <b>5주 시점 통증 없음/경미 비율이 유의하게 높았고</b> 효과는 8주까지 유지.', 'green'),
   (-1, '핵심 조건 — <b>“활성 유발점을 정확히 찌른 경우”</b>. 같은 해 별도 논평에서 주사 정확도가 결과를 갈랐다는 지적이 나왔다.', 'accent'),
 ],
 'aside': {'title': '왜 이 연구가 중요한가', 'items': [
   (0, '근막통에서 <b>충분한 용량</b>을 쓴 몇 안 되는 RCT', ''),
   (0, '음성 연구들은 대개 <b>5 U/유발점</b> 수준의 소량', ''),
   (-1, '→ 용량과 표적 정확도가 <b>결과를 뒤집는다</b>', 'green'),
 ]},
 'foot': 'Göbel H et al. Pain 2006;125:82-88 (Dysport Myofascial Pain Study Group)'},

# 09 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '승모근 · 근막통증 ②', 'tag': ('반대 근거', 'red'),
 'title': '그런데 메타분석은 “권고할 수 없다”고 말한다',
 'items': [
   (0, '<b>2025 메타분석(RCT 7편 261명):</b> 위약 대비 통합 평균차 <b>−10.22</b> (0–100 척도).', ''),
   (0, '<b>통계적으로 유의하나 임상적으로는 미달.</b> 저자 결론 — “권고할 수 없다”(근거 질 moderate).', 'red'),
   (0, '<b>Ojala 2006:</b> 유발점당 <b>5 U</b> 소량 → 개선 없음. <b>Cochrane(2014):</b> 근거 불충분.', ''),
   (0, '<b>Leonardi 2024 SR(10편 651명):</b> 결과 혼재 — <b>중등도–중증 + 활성 유발점</b>에는 신중히 고려 가능.', 'accent'),
   (-1, '<b>정리:</b> 1차 치료 아님. 운동·자세교정·유발점주사·건식침이 <b>실패한 뒤</b>의 선택지다.', 'accent'),
 ],
 'aside': {'title': '용량이 갈림길', 'stat': [
   ('20–400 U', '문헌들의 용량 범위'),
   ('5 U/점', '음성 연구의 전형'),
   ('40 U/점', 'Göbel 양성 연구'),
   ('−10 / 100', '메타분석 효과크기'),
 ]},
 'foot': 'Int J Rehabil Res 2025 (PMID 40237694) · Leonardi, Eur J Pain 2024 · Soares, Cochrane 2014'},

# 10 ─────────────────────────────────────────────────────
{'t': 'figure', 'eyebrow': '승모근 ③ · 주사기법', 'tag': '술기',
 'title': '승모근에 놓는 법 — 5점법과 흉막',
 'svg': SVG_TRAP_A + SVG_TRAP_B,
 'caption': '승모근은 <b>얇고 그 아래가 바로 흉곽</b>이다 — 정확도(효과)와 깊이(안전)를 동시에 잡는 유일한 방법이 초음파다',
 'foot': 'Jiang 2021 (J Orthop Surg Res, 초음파 5점법) · 유발점 주사 기흉 증례 종합'},

# 11 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '승모근 ④ · 용량과 안전', 'tag': ('용량·부작용', 'amber'),
 'title': '얼마나 놓고, 무엇이 생기고, 어떻게 피하나',
 'items': [
   (0, '<b>용량:</b> 한쪽 <b>50–100 U</b>(onabot 기준)를 3–5점 분할. <b>한쪽 어깨 100 U를 넘기지 않는다.</b>', ''),
   (0, '<b>가장 흔한 부작용:</b> 승모근 경도 근력약화 — 계통적 리뷰에서 <b>약 10.7%</b>, 대개 1–3개월 내 회복.', ''),
   (0, '<b>드물지만 중요한 것:</b> 심부 확산 시 <b>목 신전근 약화(두부하수)</b>·<b>연하곤란</b>, 반복 주사 시 <b>승모근 위축</b>과 어깨 윤곽 변화.', 'red'),
   (0, '<b>회피:</b> 표재성·정해진 5점·고농도 소용적·짧은 바늘·집게로 근육 들기·경부 심층(견갑거근/사각근) 동시 고용량 회피.', 'accent'),
 ],
 'aside': {'title': '설명해야 할 것', 'items': [
   (0, '“어깨가 가벼워지지만 <b>무거운 것을 들 때 힘이 덜 들어갈 수 있다</b>”', ''),
   (0, '미용 목적 <b>승모근 축소</b>와 통증 치료는 용량·목표가 다르다', ''),
   (-1, '삼킴·숨쉬기 이상은 <b>즉시 연락</b>', 'red'),
 ]},
 'foot': 'Kapoor 2025 (승모근 계통적 리뷰) · 제품 안전성 정보 종합'},

# 12 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '어깨', 'tag': ('혼재', 'amber'),
 'title': '어깨 — 표적을 어디로 잡느냐가 결과를 갈랐다',
 'items': [
   (0, '<b>견갑하근 표적(Stroke 2021, n=36):</b> 초음파 유도 견갑하근 주사가 편마비성 어깨통증을 <b>유의하게 감소</b>시켰다.', 'green'),
   (0, '<b>대흉근+견갑하근(Dysport 200 U):</b> 통증은 줄었으나 <b>통계적 유의성에는 이르지 못했다</b>.', 'red'),
   (0, '<b>메타분석(만성 어깨통증):</b> 관절강내·근육내 주사 모두에서 통증 개선 보고 — 다만 이질성이 크다.', ''),
   (0, '<b>임상 해석:</b> 어깨는 <b>내회전 구축을 만드는 견갑하근</b>이 핵심 표적이다. “아픈 곳”이 아니라 “당기는 근육”을 겨냥한다.', 'accent'),
   (-1, '유착성 관절낭염(오십견) 자체에 대한 근거는 아직 약하다 — 관절낭 문제이지 근육 문제가 아니기 때문.', 'red'),
 ],
 'aside': {'title': '어깨 주사 시 주의', 'items': [
   (0, '견갑하근은 <b>흉벽에 접해</b> 있다 → 초음파 필수', 'red'),
   (0, '삼각근 확산 시 <b>거상 근력 저하</b>', ''),
   (-1, '재활(스트레칭·자세)과 반드시 병행', 'accent'),
 ]},
 'foot': 'Stroke 2021 (견갑하근 RCT) · Toxins 2023 (대흉근+견갑하근 RCT) · 만성 어깨통증 메타분석 2020'},

# 13 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '팔 · 손', 'tag': ('감별이 먼저', 'ink'), 'dense': True,
 'title': '“팔에 쥐가 난다” — 원인마다 표적이 다르다',
 'headers': ['임상 유형', '무엇이 문제인가', '보툴리눔 표적', '근거'],
 'rows': [
   ['<b>진성 근경련</b> (cramp)', '말초 운동신경 과흥분·자발발화', '경련 나는 근육 자체', '<b>B</b> (RCT)'],
   ['<b>경직</b> (뇌졸중·척수손상 후)', '상위운동신경 손상', '주동 굴곡근군', '<b>A</b> · 허가'],
   ['<b>국소 이긴장증</b> (서경 등)', '작업 특이적 이상 동시수축', '해당 전완근 (EMG 유도)', '<b>표준치료</b>'],
   ['<b>흉곽출구증후군</b>', '사각근·소흉근에 의한 압박', '전·중사각근, 소흉근', '<b>U</b> (RCT 음성)'],
   ['<b>근막통증</b> (전완 신전근)', '유발점·건부착부 과부하', 'ECRB/EDC 근복', '<b>C</b>'],
   ['<b>대사·전해질·약물</b>', '탈수·이뇨제·statin·투석', '해당 없음 — 원인 교정', '—'],
 ],
 'hlrows': [5],
 'note': '＊<b>빨간 칸을 먼저 배제</b>하지 않으면 다른 모든 치료가 헛돈다. 경추 신경근증·다발신경병증도 동일하게 선행 감별.',
 'foot': '“쥐가 난다”는 호소는 최소 6가지 서로 다른 병태를 포함한다'},

# 14 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '팔 ① · 진성 근경련', 'tag': ('Level B · RCT', 'green'),
 'title': 'Restivo 2018 — 경련에 대한 가장 좋은 직접 근거',
 'items': [
   (0, '<b>대상:</b> 약물 불응성 종아리·발 경련을 가진 <b>당뇨병성 말초신경병증 50명</b>, 무작위 이중맹검 위약대조.', ''),
   (0, '<b>방법:</b> 각 측 <b>비복근 100 U</b> 또는 <b>발 소근육 30 U</b> 주사 (onabot 기준), 위약은 생리식염수.', ''),
   (0, '<b>결과:</b> 통증 강도(1차 결과)·경련 빈도 모두 위약 대비 유의 개선. <b>1주부터 나타나 14주까지 지속</b>, 20주 추적.', 'green'),
   (0, '<b>팔에도 적용되는 논리:</b> 경련의 발화점은 <b>근육 끝의 말초 운동신경 종말</b> — 부위와 무관하게 같은 표적이다.', 'accent'),
   (-1, '＊단, 상지 경련에 대한 <b>전용 RCT는 없다</b>. 하지 근거의 외삽이며 저용량부터 시작한다.', 'red'),
 ],
 'aside': {'title': '경련 계열 근거', 'stat': [
   ('n=50', 'Restivo 2018 RCT'),
   ('1–14주', '효과 발현–지속'),
   ('100 U', '비복근 · 한쪽'),
   ('30 U', '발 소근육 · 한쪽'),
 ]},
 'foot': 'Restivo DA et al. Ann Neurol 2018 (PMID 30225985) · Bertolasi 1997 (경련-근속연축 증후군)'},

# 15 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '팔 ② · 경직', 'tag': ('Level A · 허가', 'green'),
 'title': '뇌졸중 후 상지 경직 — 유일하게 급여되는 영역',
 'items': [
   (0, '<b>표적:</b> 팔꿈치 굴곡(상완이두근·상완근·상완요골근), 손목·손가락 굴곡(FCR·FCU·FDS·FDP), 엄지 내전근.', ''),
   (0, '<b>용량:</b> 성인 상지 <b>총 300–400 U</b>(onabot)까지 RCT로 검증 — 400 U군이 240 U군보다 팔꿈치 굴곡근 긴장 감소가 컸다.', ''),
   (0, '<b>국내 급여:</b> 뇌졸중 발병 3년 내 상지 경직(어깨 제외), MAS 2–3등급. <b>1회 최대 300 U</b>, 최소 <b>3개월</b> 간격, 3년 내 최대 6회.', 'accent'),
   (0, '<b>주의:</b> 소아 경직 치료에서 <b>확산에 의한 전신 증상 보고가 가장 많다</b>(FDA 박스경고). 체중당 용량 준수.', 'red'),
 ],
 'aside': {'title': '유도 방법의 가치', 'items': [
   (0, '전완근은 <b>작고 겹쳐 있다</b> — 촉진만으로는 부정확', ''),
   (0, '<b>초음파 · 전기자극 · EMG</b> 중 하나는 필수', ''),
   (-1, '비표적 근육 약화가 이 영역 실패의 1위 원인', 'red'),
 ]},
 'foot': 'onabotA 400 U 상지경직 RCT · 국내 급여기준(뇌졸중 후 상지경직) 고시'},

# 16 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '팔 ③ · 흉곽출구증후군', 'tag': ('U · RCT 음성', 'amber'),
 'title': '사각근 주사 — 해부는 명확한데 근거는 그렇지 않다',
 'svg': SVG_SCALENE,
 'foot': '증례군: 64%에서 50%↑ 증상 감소·평균 88일 · Finlayson 2011 RCT(n=38): 6주 VAS 위약 대비 차이 없음(P=.36)'},

# 17 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '팔 ④ · 국소 이긴장증', 'tag': ('표준치료', 'green'),
 'title': '서경(writer’s cramp) — “쥐”라 부르지만 이긴장증이다',
 'items': [
   (0, '<b>양상:</b> 글씨·악기 등 <b>특정 동작에서만</b> 손·전완이 굳는다. 진성 경련과 달리 <b>쉬면 풀리고 통증은 부수적</b>.', ''),
   (0, '<b>효과:</b> 대조연구 통합 139명에서 <b>약 73%가 호전</b> — 이 영역의 1차 치료다.', 'green'),
   (0, '<b>한계:</b> 효과를 제한하는 것은 언제나 <b>비표적 근육의 약화</b>. 전완근은 작고 층층이 겹친다.', 'red'),
   (0, '<b>기법:</b> 표적근을 <b>EMG(수의수축 중 신호) 또는 전기자극</b>으로 확정한 뒤 소량 주사. 표면 해부학만으로는 부정확.', 'accent'),
   (-1, '저용량에서 시작해 <b>4주 뒤 반응을 보고 증량</b>하는 것이 원칙 — 처음부터 충분히 넣지 않는다.', 'accent'),
 ],
 'aside': {'title': '유도법 비교', 'items': [
   (0, '<b>촉진만:</b> 전완 심층근 부정확', ''),
   (0, '<b>전기자극:</b> 표적 확인 직관적', ''),
   (0, '<b>EMG:</b> 이상 동시수축 근육 특정', ''),
   (-1, '<b>초음파 병용</b>이 가장 안전', 'accent'),
 ]},
 'foot': 'Focal hand dystonia 계통적 리뷰 · 유도법 비교 연구 종합'},

# 18 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '팔 ⑤ · 외측상과염', 'tag': ('Level C · 상충', 'amber'),
 'title': '테니스엘보 — 듣기는 하는데, 손가락 힘을 대가로 준다',
 'items': [
   (0, '<b>Wong 2005(n=60):</b> Botox <b>60 U</b> 단일 주사 → 4주·12주 통증 유의 감소. 단 <b>손가락 신전 약화</b> 발생.', ''),
   (0, '<b>Placzek 2007·Espandar 2010:</b> 위약 대비 개선 확인 — 해부학적 계측 주사로 16주까지 감소.', ''),
   (0, '<b>메타분석:</b> 위약보다 우월(최대 16주) · <b>스테로이드는 2–4주 우월, 12주 후 대등</b> · 용량 20–60 U.', 'accent'),
   (0, '<b>대가:</b> 2–4주 악력 저하(고용량 8–12주). <b>손 쓰는 직업이면 사실상 금기에 가깝다.</b>', 'red'),
 ],
 'aside': {'title': '언제 고려하나', 'items': [
   (0, '6개월 이상 지속 · 스테로이드 실패', ''),
   (0, '수술을 미루고 싶은 환자', ''),
   (0, '악력 저하를 <b>감수할 수 있는</b> 생활', ''),
   (-1, '연주자·조리사·미용사 → 신중', 'red'),
 ]},
 'foot': 'Wong 2005 (PMID 16330790) · Placzek 2007 (PMID 17272437) · Espandar 2010 (PMID 20421357) · 메타분석 2021–2024'},

# 19 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '팔 ⑥ · 주사기법', 'tag': '술기',
 'title': '외측상과염 — 건이 아니라 근복에 놓는다',
 'svg': SVG_ELBOW,
 'foot': '건 부착부(enthesis)가 아닌 ECRB/EDC 근복이 표적 — 건 내 주입은 이론적 이득이 없고 손상 위험만 있다'},

# 20 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '허리 ① · 만성 요통', 'tag': ('Level B', 'green'),
 'title': 'Foster 2001 — 방척추근 주사가 요통을 줄였다',
 'items': [
   (0, '<b>방법:</b> 만성 요통 <b>31명</b> 이중맹검 — Botox <b>200 U</b>를 통증 심한 쪽 <b>방척추 5레벨에 40 U씩</b>.', ''),
   (0, '<b>결과:</b> 3주 <b>≥50% 완화 73.3% vs 25%</b>, 8주 Oswestry 기능장애도 유의 개선.', 'green'),
   (0, '<b>2025 SR/MA:</b> 대조 대비 통증·기능 유의 개선, <b>중대 부작용 없음</b> — Level B 재확인.', 'green'),
   (0, '<b>표적이 관건:</b> 방척추근 외에 <b>요방형근·이상근</b>이 진짜 발생원일 수 있다 — 먼저 확인.', 'accent'),
   (-1, '＊<b>구조적 원인(추간판·협착)은 해결되지 않는다.</b> 근육성 요통이 표적이다.', 'red'),
 ],
 'aside': {'title': 'Foster 2001', 'stat': [
   ('73.3%', 'BTX군 · 3주 ≥50% 완화'),
   ('25%', '위약군'),
   ('200 U', '총 용량'),
   ('40 U × 5', '레벨당 용량'),
 ]},
 'foot': 'Foster L et al. Neurology 2001;56:1290-3 (PMID 11376175) · Wagrees, Eur J Pain 2025'},

# 21 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '허리 ② · 주사기법', 'tag': '술기',
 'title': '요추 방척추 주사 — 5레벨 · 한쪽 · 40 U',
 'svg': SVG_LUMBAR,
 'foot': 'Foster 2001 프로토콜 · 흉추로 올라갈수록 기흉 위험이 커진다 — 흉추 레벨은 초음파 없이는 피한다'},

# 22 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '엉덩이 · 이상근증후군', 'tag': ('Level B', 'green'),
 'title': '이상근증후군 — 스테로이드보다 나은 몇 안 되는 근거',
 'items': [
   (0, '<b>Fishman 2002:</b> BTX-A 100 U군에서 <b>50% 이상 통증 개선 65%</b>, 트리암시놀론+리도카인군 <b>32%</b>.', 'green'),
   (0, '<b>계통적 리뷰(7편 152명):</b> RCT 3편 포함, 용량 <b>100–300 U</b>, 근거 질 fair, <b>안전성 양호</b>.', ''),
   (0, '<b>왜 듣나:</b> 이상근의 지속 수축이 좌골신경을 누르고, 그 통증이 다시 수축을 부른다 — 그 고리를 끊는다.', 'accent'),
   (0, '<b>필수 조건:</b> 이상근은 깊고 <b>좌골신경이 바로 아래(또는 관통)</b>를 지난다. <b>영상 유도 없는 맹목 주사는 하지 않는다.</b>', 'red'),
 ],
 'aside': {'title': 'Fishman 2002', 'stat': [
   ('65%', 'BTX군 ≥50% 개선'),
   ('32%', '스테로이드+리도카인군'),
   ('100 U', '사용 용량'),
   ('100–300 U', '문헌 전체 범위'),
 ]},
 'foot': 'Fishman LM et al. 2002 (PMID 12362115) · SR: J Clin Orthop Trauma 2022 (PMC9294329)'},

# 23 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '엉덩이 · 주사기법', 'tag': '술기',
 'title': '이상근 — 신경을 먼저 찾고, 그 다음에 근육을 찌른다',
 'svg': SVG_PIRI,
 'foot': '초음파·투시·EMG 중 하나는 필수 · 대둔근에만 들어가면 무효, 신경 내로 들어가면 손상'},

# 24 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '무릎', 'tag': ('Level B', 'green'),
 'title': '무릎 — 근육이 아니라 관절강에 놓는다',
 'items': [
   (0, '<b>관절강내(무릎 OA):</b> 메타분석 <b>6편 348명</b> — 히알루론산보다 우수, <b>스테로이드와 대등·안전성 우위</b>.', 'green'),
   (0, '<b>용량:</b> 관절강내 <b>100 U</b> 단회 — 소규모 RCT 3편에서 단기 개선.', ''),
   (0, '<b>TKA 후 난치성 통증(Singh 2010):</b> 관절강내 주사로 유의 개선 — <b>수술로 더 할 게 없는 환자</b>의 선택지.', 'accent'),
   (0, '<b>전방 슬관절통(Singer):</b> <b>원위 외측광근</b> 주사 + 운동 → 개선(“비수술적 외측 유리술”).', ''),
   (-1, '＊작용 기전은 근이완이 아니라 <b>관절 내 통각 종말 억제</b>다.', 'accent'),
 ],
 'aside': {'title': '무릎 요약', 'stat': [
   ('100 U', '관절강내 표준 용량'),
   ('6편 348명', 'IA 메타분석 규모'),
   ('> HA', '히알루론산 대비'),
   ('≈ 스테로이드', '효과는 대등·안전성 우위'),
 ]},
 'foot': 'IA BoNT-A 메타분석 (Toxicon 2023·2024) · Singh JA, J Rheumatol 2010 · Singer BJ, Br J Sports Med 2011'},

# 25 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '종아리 ① · 야간 경련', 'tag': ('Level B · RCT', 'green'),
 'title': 'Park 2017 — 요추관협착 동반 야간 종아리경련',
 'items': [
   (0, '<b>대상:</b> 요추관협착증에 동반된 야간 종아리 경련 환자 <b>50명</b>, 무작위 배정.', ''),
   (0, '<b>비교:</b> 비복근 <b>BTX-A 주사</b> vs <b>gabapentin 경구</b>.', ''),
   (0, '<b>결과:</b> 전 추적 시점에서 <b>통증·경련 빈도·강도 모두 유의 감소</b>(P&lt;0.01) — 주사 계열 중 근거 수준이 가장 높다.', 'green'),
   (0, '<b>임상적 의미:</b> 경구약 부작용(졸림·어지럼)을 피하고 싶은 <b>고령 환자</b>에서 특히 매력적인 대안.', 'accent'),
   (-1, '단점 — 고가, 3–4개월마다 반복, 그리고 <b>족저굴곡 근력약화</b>. 낙상 위험군에서는 감량하거나 피한다.', 'red'),
 ],
 'aside': {'title': '종아리 경련 근거 정리', 'items': [
   (0, '<b>Park 2017:</b> 협착 동반 야간경련 RCT', 'green'),
   (0, '<b>Restivo 2018:</b> 당뇨 신경병증 경련 RCT', 'green'),
   (0, '<b>Bertolasi 1997:</b> 경련-근속연축 증후군', ''),
   (-1, '→ 원인이 달라도 <b>비복근 표적</b>은 공통', 'accent'),
 ]},
 'foot': 'Park 2017, Arch Phys Med Rehabil (PMID 28209505)'},

# 26 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '종아리 ② · 운동유발 통증', 'tag': ('탐색적', 'amber'),
 'title': '만성 운동유발 구획증후군 — 수술 대신 화학적 감압',
 'items': [
   (0, '<b>발상:</b> 근막을 절개(근막절개술)하는 대신 <b>근육 부피를 줄여</b> 구획내압을 낮춘다.', ''),
   (0, '<b>Isner-Horobeti 2013:</b> 전방·전외측 구획증후군 환자에서 주사 후 <b>구획내압이 유의하게 감소하고 통증이 소실</b>.', 'green'),
   (0, '<b>용량 예:</b> 한 다리 <b>총 150 U</b>를 내측 비복근·외측 비복근·외측 구획에 <b>50 U씩</b> 분할(100 U/mL 고농도).', ''),
   (0, '<b>한계:</b> 후속 16례 보고에서는 <b>초기 호전 후 재발</b>이 흔했다 — 특히 부분 반응군. 근거는 증례 수준.', 'red'),
   (-1, '운동선수에게는 <b>근력 저하가 곧 경기력 저하</b>다. 시즌 중 사용은 신중히.', 'accent'),
 ],
 'aside': {'title': '이 영역의 위치', 'items': [
   (0, '수술을 피하고 싶은 환자의 <b>가교 치료</b>', ''),
   (0, '진단적 가치도 있음(압력↓ = 기전 확인)', ''),
   (-1, 'RCT 없음 → <b>연구·개별 동의 틀 안에서</b>', 'red'),
 ]},
 'foot': 'Isner-Horobeti M-E et al. Am J Sports Med 2013 · 상·하지 16례 후향 연구 2021'},

# 27 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '종아리 ③ · 주사기법', 'tag': '술기',
 'title': '비복근 — 어디에, 얼마나, 무엇을 피하며',
 'svg': SVG_CALF,
 'foot': '근복 중앙·다점 분할이 원칙 · 깊게 들어가면 경골신경, 외측으로 치우치면 총비골신경(족하수)'},

# 28 ─────────────────────────────────────────────────────
{'t': 'split', 'eyebrow': '발 · 족저근막염', 'tag': ('Level B', 'green'),
 'title': '족저근막염 — 정형외과 통증 중 근거가 가장 단단한 축',
 'items': [
   (0, '<b>메타분석(RCT 7편 305명, 2024):</b> 1개월 시점 통증 유의 감소, <b>12개월까지 기능 개선 유지</b>, 부작용은 대조군과 차이 없음.', 'green'),
   (0, '<b>2021 Arch Phys Med Rehabil 메타:</b> 0–6개월 통증 강도 유의 감소.', ''),
   (0, '<b>스테로이드 비교:</b> 초기엔 비슷하나 <b>6개월 시점에서는 보툴리눔이 우수</b> — 근막 파열 위험도 없다.', 'accent'),
   (0, '<b>용량-반응이 단조롭지 않다:</b> 200 U 고용량 연구는 효과가 거의 없었다 — <b>70 U 전후</b>가 재현 구간.', 'red'),
 ],
 'aside': {'title': '왜 스테로이드보다 나은가', 'items': [
   (0, '스테로이드: <b>근막 파열·지방패드 위축</b> 위험', 'red'),
   (0, '보툴리눔: 구조 손상 보고 없음', 'green'),
   (0, '효과 지속 <b>더 김</b> (6개월 비교 우위)', 'green'),
   (-1, '단점 — 비용·발현 지연(1–2주)', ''),
 ]},
 'foot': 'PLOS One 2024 메타분석 · Arch Phys Med Rehabil 2021 (PMID 34688605) · Elizondo-Rodriguez, Foot Ankle Int'},

# 29 ─────────────────────────────────────────────────────
{'t': 'bigfig', 'eyebrow': '발 · 주사기법', 'tag': '술기',
 'title': '족저근막 2점법 — 그리고 종아리라는 대안',
 'svg': SVG_PLANTAR,
 'foot': 'Babcock 2005 (Am J Phys Med Rehabil) 2점법 · 비복근 내측두 접근은 “근막을 당기는 원인”을 겨냥한 변형'},

# 30 ─────────────────────────────────────────────────────
{'t': 'bullets', 'eyebrow': '수술후 · 절개부', 'tag': ('Level A', 'green'),
 'title': '수술후 절개부 신경통 — 우리가 만든 통증',
 'items': [
   (0, '<b>왜 맨 마지막인가:</b> 이것만 <b>부위가 아니라 원인</b>으로 묶인다 — 절개·견인·금속물 주변에서 생기는 외상후 신경통.', 'accent'),
   (0, '<b>근거는 이 발표에서 가장 높다:</b> 외상후신경통은 AAN 기준 <b>Level A</b>(효과 있음). 수술 절개부 신경통이 그 하위 범주다.', 'green'),
   (0, '<b>주사법이 완전히 다르다:</b> 근육이 아니라 <b>통증 부위 피내·피하에 격자로 소량 분할</b> — 2.5–5 U씩 1–2 cm 간격, 총 50–100 U.', ''),
   (0, '<b>절단 후 통증:</b> 잔단통은 6개월 개선, <b>환상통은 변화 없음</b> — 표적이 말초임을 보여준다. 신경종 주위 주사는 1개월 시점 개선 보고.', ''),
   (0, '<b>안 되는 것:</b> 복합부위통증증후군(CRPS)·수근관증후군은 근거 불충분 — 특히 수근관은 부정적 결과가 많다.', 'red'),
 ],
 'foot': 'Safarpour & Jabbari, Toxicon 2018 · 절단 후 통증 SR · Arch Phys Med Rehabil 2025 (신경종 주위 주사)'},

# 31 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '그 밖의 부위', 'tag': '확장 적응', 'dense': True,
 'title': '문의가 많은 나머지 부위들 — 한 장 정리',
 'headers': ['부위 · 질환', '표적 · 용량', '근거', '한 줄 평'],
 'rows': [
   ['턱관절 · 저작근 근막통', '교근 25–50 U, 측두근 10–25 U', '<b>B–C</b>', '효과 명확, 반복 시 교근 위축·저작곤란'],
   ['경추성 두통 · 후두신경통', '후경부 근육 ~100 U', '<b>C</b>', '소규모 RCT 혼재 · 만성편두통과 구분'],
   ['레이노 · 수지 허혈', '한 손 50–100 U (원위 수장부)', '<b>C</b>', '통증·궤양 치유엔 유망 · 총 50 U 이하면 약화 거의 없음'],
   ['천장관절 · 후관절 통증', '관절내 25–100 U', '<b>U</b>', '증례군 수준 — 표준치료 아님'],
   ['대전자 통증증후군', '중둔근 주변', '<b>없음</b>', '직접 근거 부재 — 권고 불가'],
   ['수근관증후군', '수근관 주변', '<b>부정적</b>', '하지 않는 편이 낫다'],
 ],
 'hlrows': [5],
 'note': '＊<b>근거가 없다</b>와 <b>효과가 없다</b>는 다르지만, 설명·동의·비용의 기준은 “근거가 없다” 쪽에 맞춘다.',
 'foot': '각 항목의 상세는 참고문헌 슬라이드 참조'},

# 32 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '용량 · 총정리', 'tag': ('onabotA 기준', 'ink'), 'dense': True,
 'title': '한 장으로 보는 부위별 용량표',
 'headers': ['부위', '총 용량 (한쪽)', '분할', '희석 · 바늘'],
 'rows': [
   ['<b>상부 승모근</b>', '50–100 U', '3–5점 (10–20 U/점)', '2 mL · 27G 13 mm'],
   ['전·중 사각근', '25–75 U', '1–2점', '1 mL · 25–27G · <b>초음파 필수</b>'],
   ['견갑하근', '~100 U', '2–3점', '2 mL · 장침 + <b>초음파</b>'],
   ['<b>ECRB/EDC (테니스엘보)</b>', '20–60 U', '1–2점', '1 mL · 27G'],
   ['<b>요추 방척추근</b>', '200 U', '5레벨 × 40 U', '2–4 mL · 25G'],
   ['<b>이상근</b>', '100–200 U', '1–2점', '2 mL · 장침 + <b>영상 유도</b>'],
   ['<b>비복근 (경련)</b>', '100 U', '4–6점 (내·외측두)', '1–2 mL · 27G'],
   ['<b>족저근막</b>', '70 U', '40 U 종골내측 + 30 U 족궁', '1 mL · 25–27G'],
   ['무릎 관절강내', '100 U', '단회', '2 mL · 21–23G'],
 ],
 'note': '<b>세션 총량 ≤400 U / 12주</b>(성인 통상) · 소아·저체중·근감소증 고령자는 체중당 환산 · <b>한 점에 50 U를 넘기지 않는다.</b>',
 'foot': '각 부위 근거 문헌의 용량을 onabotulinumtoxinA 단위로 정리 — Dysport는 2.5–3배'},

# 33 ─────────────────────────────────────────────────────
{'t': 'table', 'eyebrow': '부작용 · 총정리', 'tag': ('안전', 'red'), 'dense': True,
 'title': '무엇이, 얼마나 자주, 어디서 생기나',
 'headers': ['범주', '증상', '빈도 · 경과', '고위험 부위'],
 'rows': [
   ['국소 반응', '주사부 통증·멍·부종·혈종', '흔함 · 수일', '모든 부위'],
   ['전신 경미', '감기유사 증상·피로·두통', '수 % · 1–2주', '고용량 세션'],
   ['<b>표적근 약화</b>', '해당 근육 힘 빠짐', '용량 의존 · 4–8주', '승모근 <b>약 10.7%</b>'],
   ['<b>인접근 확산</b>', '연하곤란 · 목 신전근 약화 · 발성장애', '드묾 · 2–8주', '경부(사각근·SCM)'],
   ['<b>기능적 위해</b>', '손가락 신전 약화 / 족저굴곡 약화', '용량 의존', '전완 · 종아리'],
   ['<b>술기 합병증</b>', '기흉 · 신경 손상 · 혈관 내 주입', '매우 드묾', '흉벽 위 · 이상근'],
   ['<b>전신 확산(박스경고)</b>', '전신쇠약 · 복시 · 호흡곤란', '매우 드묾 · 수시간~수주', '경직 치료(특히 소아)'],
   ['면역원성', '이차 무반응(효과 소실)', '누적 위험', '잦은 재주사 · 고용량'],
 ],
 'hlrows': [6],
 'note': '＊<b>빨간 칸이 FDA 박스경고 영역</b> — 삼킴·호흡 곤란은 생명을 위협할 수 있다. “이런 증상이면 즉시 연락”을 문서로 남긴다.',
 'foot': 'FDA Boxed Warning (Distant Spread of Toxin Effect) · 부위별 계통적 리뷰 종합'},

# 34 ─────────────────────────────────────────────────────
{'t': 'figure', 'eyebrow': '부작용 회피 · 술기', 'tag': ('3원칙', 'green'),
 'title': '주사 자체로 막을 수 있는 것 — 세 가지',
 'svg': SVG_SAFE_A + SVG_SAFE_B + SVG_SAFE_C,
 'caption': '부작용의 대부분은 <b>약이 아니라 바늘 끝의 문제</b>다 — 농도, 거리, 각도',
 'foot': '희석-확산 연구 (PMID 15545544) · 초음파 유도 안전성 연구 종합'},

# 35 ─────────────────────────────────────────────────────
{'t': 'bullets', 'eyebrow': '부작용 회피 ① · 놓기 전에', 'tag': ('체크리스트', 'green'),
 'title': '주사 전에 결정되는 안전 — 6가지',
 'items': [
   (0, '<b>① 최소 유효 용량에서 시작한다.</b> 과다는 되돌릴 수 없다 — 세션 ≤400 U, 한 점 ≤50 U.', 'green'),
   (0, '<b>② 고농도·소용적으로 만든다.</b> 표적이 작을수록 희석을 줄인다 — 1 mL/100 U.', 'green'),
   (0, '<b>③ 유도 장비를 쓴다.</b> 전완·사각근·이상근·견갑하근·심부 경부는 <b>초음파(또는 EMG·전기자극) 없이는 하지 않는다</b>. 촉진은 근육 두께를 알려주지 않는다.', 'green'),
   (0, '<b>④ 흉벽 위에서는 집게로 들고 접선으로, 13 mm 바늘로.</b> 50–60 mm 바늘은 실시간 유도 없이는 금지 — 기흉의 대부분이 여기서 나온다.', 'green'),
   (0, '<b>⑤ 신경을 먼저 화면에 띄운다.</b> 좌골신경·상완신경총·척골신경을 확인한 뒤 반대편에서 진입. 주입 전 흡인, 이상감각 시 즉시 중단.', 'green'),
   (0, '<b>⑥ 기저 근력을 숫자로 기록한다.</b> 악력 · 족저굴곡력 · 경부 신전력.', 'accent'),
 ],
 'foot': '이 여섯 가지가 술기 관련 합병증의 대부분을 차단한다'},

# 36 ─────────────────────────────────────────────────────
{'t': 'bullets', 'eyebrow': '부작용 회피 ② · 환자와 약제', 'tag': ('체크리스트', 'green'),
 'title': '누구에게 놓지 않을 것인가 — 그리고 그 다음',
 'items': [
   (0, '<b>절대 피한다:</b> 중증근무력증·Lambert-Eaton·ALS 등 <b>신경근접합부 질환</b>, 주사 부위 <b>활동성 감염</b>, 과민반응.', 'red'),
   (0, '<b>신중히:</b> 임신·수유(안전성 미확립), <b>아미노글리코사이드·근이완제 병용</b>(효과 증강), 항응고 치료(혈종), 심한 근감소증·낙상 고위험 고령.', 'red'),
   (0, '<b>부위별 “하지 말 것”:</b> 양측 흉쇄유돌근 동시 고용량(연하곤란), 손 쓰는 직업의 전완 고용량, 보행 불안정 환자의 비복근 고용량(낙상).', 'red'),
   (0, '<b>항체를 막는 법:</b> 재주사 간격 <b>≥12주</b>, 3주 내 보충주사 금지, 누적용량 최소화, 필요 시 <b>복합단백 없는 제제</b> 고려.', 'accent'),
   (0, '<b>주사 후:</b> 주사부 문지르지 않기, 당일 격한 운동 회피, <b>4주 재평가 예약</b>, 삼킴·호흡·복시 시 즉시 연락.', 'accent'),
   (-1, '＊한 번의 “조금 더 넣어달라”가 <b>몇 년치 반응성</b>을 잃게 만들 수 있다.', 'red'),
 ],
 'foot': '제품 첨부문서 금기·경고 · 면역원성 리뷰 · 신경근접합부 질환 증례 보고'},

# 37 ─────────────────────────────────────────────────────
{'t': 'key', 'eyebrow': 'Clinical Algorithm',
 'headline': '진료에서는 이 순서로 결정한다',
 'msgs': [
   ('1 · 감별', '“쥐가 난다·아프다”를 <b>경련 / 경직 / 이긴장증 / 신경포착 / 근막통 / 대사</b>로 먼저 나눈다. 여기서 틀리면 나머지가 다 헛돈다.'),
   ('2 · 순서', '보툴리눔은 <b>2차 이상</b>이다. 운동·자세·부하 교정, 물리치료, 유발점주사·건식침, (필요 시) 스테로이드가 먼저다.'),
   ('3 · 부위별 기대치', '<b>요통·이상근·무릎·경련·족저근막염</b>은 근거를 갖고 권한다. <b>승모근 근막통·테니스엘보</b>는 “선택지 중 하나”로 설명한다.'),
   ('4 · 용량', '문헌 용량의 <b>하한에서 시작</b>하고 4주에 평가해 올린다. 한 점 ≤50 U, 세션 ≤400 U.'),
   ('5 · 안전', '흉벽 위·신경 옆은 <b>초음파</b>. 고농도·소용적. 기저 근력 기록. 재주사 <b>≥12주</b>.'),
 ]},

# 38 ─────────────────────────────────────────────────────
{'t': 'key', 'eyebrow': 'Key Messages',
 'headline': '오늘 남길 다섯 문장',
 'msgs': [
   ('기전', '보툴리눔의 진통은 근이완의 <b>부산물이 아니다</b> — 통각 종말의 신경펩타이드 방출을 직접 막는다.'),
   ('가장 강한 곳', '근거가 가장 단단한 곳은 <b>수술후 절개부 신경통(A)</b>, 그다음 <b>요통·이상근·무릎·경련·족저근막염(B)</b>.'),
   ('가장 약한 곳', '가장 흔히 요청받는 <b>승모근 근막통</b>은 메타분석에서 <b>임상적 유의성에 미달</b>했다 — 기대치를 정직하게 낮춰 설명한다.'),
   ('용량', '음성 연구는 대개 <b>용량이 모자랐고</b>, 부작용 연구는 대개 <b>용량이 과했다</b>. 정답은 문헌 용량의 하한에서 시작하는 것.'),
   ('부작용', '합병증의 대부분은 약제가 아니라 <b>농도·거리·각도</b>에서 온다.'),
 ]},

# 39 ─────────────────────────────────────────────────────
{'t': 'refs', 'title': '참고문헌 ① — 기전 · 근막통증 · 승모근',
 'refs': [
   ('<b>Safarpour Y, Jabbari B.</b> Botulinum toxin treatment of pain syndromes — an evidence based review. Toxicon. 2018.', PM(29409817)),
   ('<b>Matak I, Lacković Z.</b> Botulinum toxin A, brain and pain. Prog Neurobiol. 2014.', PM(24915026)),
   ('<b>Mechanisms of botulinum toxin type A action on pain.</b> Toxins. 2019.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC6723487/'),
   ('<b>Göbel H, et al.</b> Dysport for upper back myofascial pain syndrome: multicentre RCT. Pain. 2006;125:82-8.', PM(16750294)),
   ('<b>Ojala T, et al.</b> Small doses of BoNT-A in neck-shoulder myofascial pain: crossover RCT. Clin J Pain. 2006.', PM(16691083)),
   ('<b>Soares A, et al.</b> Botulinum toxin for myofascial pain syndromes in adults. Cochrane. 2014.', PM(25062018)),
   ('<b>Leonardi L, et al.</b> BoNT for upper back myofascial pain syndrome: SR of RCTs. Eur J Pain. 2024.', 'https://onlinelibrary.wiley.com/doi/10.1002/ejp.2198'),
   ('<b>Efficacy of BoNT in myofascial pain in neck and shoulder</b> — SR & meta-analysis. Int J Rehabil Res. 2025.', PM(40237694)),
   ('<b>Jiang Y, et al.</b> Ultrasound-guided five-point injection of BoNT for trapezius. J Orthop Surg Res. 2021.', PM(34686203)),
   ('<b>Kapoor KM, et al.</b> BoNT-A for trapezius contouring: systematic review (안전성). 2025.', 'https://journals.sagepub.com/doi/10.1177/30499240251320906'),
 ]},

# 40 ─────────────────────────────────────────────────────
{'t': 'refs', 'title': '참고문헌 ② — 상지 · 근경련 · 하지',
 'refs': [
   ('<b>Wong SM, et al.</b> Lateral epicondylitis treated with botulinum toxin: RCT. Ann Intern Med. 2005.', PM(16330790)),
   ('<b>Placzek R, et al.</b> Chronic radial epicondylitis with BoNT-A: multicentre RCT. J Bone Joint Surg Am. 2007.', PM(17272437)),
   ('<b>Espandar R, et al.</b> Anatomic measurement–guided BoNT for lateral epicondylitis: RCT. CMAJ. 2010.', PM(20421357)),
   ('<b>Finlayson HC, et al.</b> BoNT injection for thoracic outlet syndrome: double-blind RCT. Pain. 2011.', PM(21628084)),
   ('<b>Torriani M, et al.</b> BoNT in neurogenic TOS: ultrasound-guided approach. 2010.', PM(20186413)),
   ('<b>Botulinum toxin therapy in writer’s cramp and musician’s dystonia.</b> 2021.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8708945/'),
   ('<b>Restivo DA, et al.</b> BoNT-A for treating cramps in diabetic neuropathy. Ann Neurol. 2018.', PM(30225985)),
   ('<b>Bertolasi L, et al.</b> Botulinum toxin treatment of muscle cramps. 1997.', PM(9029067)),
   ('<b>Park J, et al.</b> BoNT for nocturnal calf cramps in lumbar spinal stenosis: RCT. Arch Phys Med Rehabil. 2017.', PM(28209505)),
   ('<b>Isner-Horobeti M-E, et al.</b> Intramuscular pressure and BoNT in chronic exertional compartment syndrome. 2013.', 'https://journals.sagepub.com/doi/10.1177/0363546513499183'),
   ('<b>Babcock MS, et al.</b> Plantar fasciitis pain treated with BoNT-A: RCT. Am J Phys Med Rehabil. 2005.', PM(16034223)),
   ('<b>Elizondo-Rodríguez J, et al.</b> BoNT-A vs corticosteroid vs anesthetic for plantar fasciitis. Foot Ankle Int.', 'https://journals.sagepub.com/doi/abs/10.1177/1071100720961093'),
 ]},

# 41 ─────────────────────────────────────────────────────
{'t': 'refs', 'title': '참고문헌 ③ — 체간 · 관절 · 안전',
 'refs': [
   ('<b>Clinical efficacy of BoNT in plantar fasciitis</b> — SR & meta-analysis of RCTs. Arch Phys Med Rehabil. 2021.', PM(34688605)),
   ('<b>Efficacy and safety of BoNT-A in plantar fasciitis</b> — SR & meta-analysis. PLOS One. 2024.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11651609/'),
   ('<b>Foster L, et al.</b> Botulinum toxin A and chronic low back pain: RCT. Neurology. 2001.', PM(11376175)),
   ('<b>Wagrees W, et al.</b> BoNT-A in chronic low back pain: SR, meta-analysis, TSA. Eur J Pain. 2025.', 'https://onlinelibrary.wiley.com/doi/10.1002/ejp.4796'),
   ('<b>Fishman LM, et al.</b> BoNT type A in piriformis muscle syndrome: pilot study. 2002.', PM(12362115)),
   ('<b>Use of botulinum neurotoxin in piriformis syndrome</b> — systematic review. 2022.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9294329/'),
   ('<b>Intra-articular BoNT-A for knee osteoarthritis</b> — meta-analysis of RCTs. Toxicon. 2023.', PM(36640812)),
   ('<b>Singh JA, et al.</b> Intraarticular BoNT-A for refractory painful TKA: RCT. J Rheumatol. 2010.', 'https://www.jrheum.org/content/37/11/2377'),
   ('<b>Ultrasound-guided BoNT-A into subscapularis for hemiplegic shoulder pain</b>: RCT. Stroke. 2021.', 'https://www.ahajournals.org/doi/full/10.1161/STROKEAHA.121.034049'),
   ('<b>Hsu AT, et al.</b> Effect of volume and concentration on diffusion of botulinum exotoxin A. 2004.', PM(15545544)),
   ('<b>Immunogenicity of botulinum toxin</b> — review (이차 무반응 · 주사 간격). 2022.', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8795657/'),
   ('<b>FDA Boxed Warning</b> — Distant Spread of Toxin Effect (BOTOX Product Monograph).', 'https://www.botoxone.com/content/dam/botoxone/pdf/BOTOX%20Product%20Monograph%20-%20All%20Indications.pdf'),
 ]},

]
