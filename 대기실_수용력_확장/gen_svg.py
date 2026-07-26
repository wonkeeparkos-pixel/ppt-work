# -*- coding: utf-8 -*-
"""상록탑정형외과 — 동측 공용부 대기 수용력 확장 배치도
좌표계: 건물 북서 외벽 코너 기준(m). X=동, Y=남. 1 SVG unit = 100 mm.
범위: 동측(접수·원무·간호부·대기홀·로비)만. 서측 치료동은 제외.
좌석: 연결의자 피치 500 / 좌폭 450 / 깊이 580   (현행 벤치소파 1,800 × 700)
"""
OX, OY = 11.9, 5.1
P, SW, SD = 0.50, 0.45, 0.58
VB = "0 0 124 110"

def X(m): return round((m - OX) * 10, 2)
def Y(m): return round((m - OY) * 10, 2)
def W(m): return round(m * 10, 2)

def rect(x, y, w, h, cls, rx=0):
    return (f'<rect class="{cls}" x="{X(x)}" y="{Y(y)}" width="{W(w)}" '
            f'height="{W(h)}" rx="{rx}"/>')

def line(x1, y1, x2, y2, cls):
    return f'<line class="{cls}" x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}"/>'

def text(x, y, s, cls="lbl", anchor="start", extra=""):
    return (f'<text class="{cls}" x="{X(x)}" y="{Y(y)}" text-anchor="{anchor}"{extra}>'
            f'{s}</text>')

def rot(x, y, s, cls="mini", anchor="middle", deg=-90):
    return text(x, y, s, cls, anchor, f' transform="rotate({deg} {X(x)} {Y(y)})"')

def dot(cx, cy, filled=True, r=1.55):
    return (f'<circle class="{"occ" if filled else "lost"}" cx="{X(cx)}" '
            f'cy="{Y(cy)}" r="{r}"/>')

# ── 좌석 ────────────────────────────────────────────────────────────────────
def seat(cx, cy, facing):
    hw, hd = SW / 2, SD / 2
    if facing in ("n", "s"):
        x0, y0, w, h = cx - hw, cy - hd, SW, SD
    else:
        x0, y0, w, h = cx - hd, cy - hw, SD, SW
    bk = {'n': (x0, y0 + h, x0 + w, y0 + h), 's': (x0, y0, x0 + w, y0),
          'e': (x0, y0, x0, y0 + h), 'w': (x0 + w, y0, x0 + w, y0 + h)}[facing]
    return (f'<rect class="seat" x="{X(x0)}" y="{Y(y0)}" width="{W(w)}" '
            f'height="{W(h)}" rx="0.7"/>' + line(*bk, "seat-back"))

def bank(x0, y0, n, facing):
    """연결의자 1열 + 좌석 사이·양끝 팔걸이. facing 은 앉은 사람이 보는 방향.
    n·s → 동서로 늘어섬 / e·w → 남북으로 늘어섬."""
    horiz = facing in ("n", "s")
    out = [seat(x0 + P * i, y0, facing) if horiz else seat(x0, y0 + P * i, facing)
           for i in range(n)]
    for i in range(n + 1):
        if horiz:
            x = x0 - P/2 + P*i
            out.append(line(x, y0 - SD/2 + .05, x, y0 + SD/2 - .05, "arm"))
        else:
            y = y0 - P/2 + P*i
            out.append(line(x0 - SD/2 + .05, y, x0 + SD/2 - .05, y, "arm"))
    return "".join(out)

def wheel(x, y, w=0.9, h=1.2):
    return rect(x, y, w, h, "wc") + text(x + w/2, y + h/2 + .22, "휠", "wct", "middle")

# ── 공통 골격 ───────────────────────────────────────────────────────────────
def shell(nurse_full=True):
    s = []
    # 북측 벽 / E-V 홀
    s.append(line(12.2, 6.0, 22.1, 6.0, "wall"))
    s.append(rect(16.0, 5.35, 3.0, 0.65, "core"))
    s.append(text(17.5, 5.82, "E/V 홀 · 출입", "mini", "middle"))
    s.append(f'<path class="arrow" d="M {X(17.5)} {Y(6.15)} V {Y(6.95)}"/>')
    # 동측 경계
    s.append(line(22.1, 6.0, 23.3, 6.0, "wall"))
    s.append(line(23.3, 6.0, 23.3, 9.5, "wall"))
    s.append(line(23.3, 9.5, 22.6, 9.5, "wall"))
    s.append(line(22.6, 9.5, 22.6, 15.35, "wall"))
    s.append(rot(23.62, 7.6, "X-RAY · CT · BMD · 직원휴게실", "mini"))
    # 남측 벽
    s.append(line(12.2, 15.35, 22.6, 15.35, "wall"))
    s.append(text(15.4, 15.28, "C-ARM실 · 의국 · 조영촬영실 · 진료실", "mini", "middle"))
    # 서측 범위 경계 (파단선)
    s.append(f'<path class="cut" d="M {X(12.3)} {Y(6.0)} V {Y(15.35)}"/>')
    s.append(rot(12.12, 10.7, "서측 치료동 — 금번 범위 외", "cutt"))
    # 정수기 / 커피
    s.append(rect(20.0, 6.0, 1.8, 0.45, "fix"))
    s.append(text(20.9, 6.9, "정수기 · 커피", "mini", "middle"))
    # 기둥
    s.append(rect(21.5, 6.95, 0.5, 0.5, "col"))
    # 접수 / 수납
    s.append(rect(13.6, 9.15, 5.4, 0.7, "counter"))
    s.append(text(16.3, 9.68, "접수 / 수납   L = 5,400", "lbl-w", "middle"))
    s.append(rect(13.6, 9.85, 5.4, 1.15, "back"))
    s.append(text(16.3, 10.62, "원무 백존", "mini", "middle"))
    # 간호부
    if nurse_full:
        s.append(rect(12.6, 11.0, 6.4, 3.0, "room"))
        s.append(rect(12.6, 11.0, 1.6, 3.0, "room2"))
        s.append(rot(13.4, 12.5, "간호실"))
        s.append(text(16.6, 12.4, "간 호 부", "lbl", "middle"))
        s.append(text(16.6, 13.15, "6,400 × 3,000 = 19.2 m²", "dim", "middle"))
    # 탈의실
    s.append(rect(22.6, 10.0, 1.2, 1.6, "room"))
    s.append(rect(22.6, 11.8, 1.2, 1.5, "room"))
    s.append(rot(23.2, 10.8, "탈의실(남)"))
    s.append(rot(23.2, 12.55, "탈의실(여)"))
    # X-RAY 동선
    s.append(f'<path class="flow" d="M {X(22.3)} {Y(14.9)} V {Y(9.0)}"/>')
    # 방위 · 축척
    s.append(f'<path class="north" d="M {X(12.85)} {Y(7.05)} V {Y(6.4)} '
             f'M {X(12.66)} {Y(6.66)} L {X(12.85)} {Y(6.36)} L {X(13.04)} {Y(6.66)} Z"/>')
    s.append(text(12.85, 7.5, "N", "mini", "middle"))
    for a, b, c, d in [(13.5, 6.8, 15.5, 6.8), (13.5, 6.65, 13.5, 6.95),
                       (14.5, 6.72, 14.5, 6.88), (15.5, 6.65, 15.5, 6.95)]:
        s.append(line(a, b, c, d, "scale"))
    s.append(text(14.5, 7.2, "0 ─ 2 m", "dim", "middle"))
    return "".join(s)

# ═══ 현황 ══════════════════════════════════════════════════════════════════
def before():
    s = ['<g>', shell(True)]
    s.append(rect(19.1, 8.6, 3.5, 6.75, "zone-now"))
    s.append(rot(19.3, 12.3, "메인 대기홀 ≈ 24 m²", "zt"))
    for cy in [10.15, 11.55, 12.95, 14.35]:
        s.append(rect(19.75, cy - 0.35, 1.8, 0.7, "bench"))
        s.append(line(19.75, cy + 0.35, 21.55, cy + 0.35, "bench-back"))
        for j in range(4):
            s.append(dot(19.975 + 0.45 * j, cy, j < 3))
    s.append(text(20.8, 15.15, "벤치소파 1,800×700 × 4대 → 실착석 12", "dim", "middle"))
    s.append(rect(20.3, 8.85, 1.35, 0.62, "bench"))
    s.append(line(20.3, 8.85, 21.65, 8.85, "bench-back"))
    for j in range(3):
        s.append(dot(20.53 + 0.45 * j, 9.16, j < 2))
    s.append(f'<circle class="benchc" cx="{X(22.9)}" cy="{Y(7.7)}" r="3.1"/>')
    s.append(dot(22.9, 7.7))
    for x, y, w, h, t, v in [
            (16.1, 6.6, 6.4, 1.9, "로비 · 전실   약 19 m² 미사용", False),
            (12.7, 14.1, 6.2, 1.0, "간호부 남측 데드코리도  7.7 m²", False),
            (21.62, 10.0, 0.95, 4.5, "순수 통로", True)]:
        s.append(rect(x, y, w, h, "void"))
        cx, cy = x + w/2, y + h/2
        s.append(rot(cx, cy, t, "voidt") if v else text(cx, cy + .12, t, "voidt", "middle"))
    return "".join(s) + '</g>'

# ═══ 개선 (B안) ════════════════════════════════════════════════════════════
def after():
    s = ['<g>', shell(False)]
    s.append(rect(12.6, 11.0, 2.6, 3.0, "room"))
    s.append(rot(13.75, 12.5, "간호 스테이션"))
    s.append(rot(14.4, 12.5, "7.8 m²", "dim"))
    for a, b, c, d in [(15.2, 11.0, 19.0, 11.0), (19.0, 11.0, 19.0, 14.0),
                       (15.2, 14.0, 19.0, 14.0)]:
        s.append(line(a, b, c, d, "demo"))
    s.append(text(17.1, 14.62, "철거 (B안)   L ≈ 11.6 m", "demot", "middle"))

    # ZONE 1 — 진료 대기
    s.append(rect(19.1, 8.6, 3.5, 6.75, "zone1"))
    s.append(bank(19.65, 10.44, 4, 'n') + bank(19.65, 11.02, 4, 's'))
    s.append(bank(19.65, 12.75, 4, 'n') + bank(19.65, 13.33, 4, 's'))
    s.append(bank(19.65, 15.06, 4, 'n'))
    s.append(wheel(19.45, 8.75))
    s.append(text(20.62, 9.05, "ZONE 1  진료 대기", "zt1"))
    s.append(text(20.62, 9.75, "20석", "cnt"))

    # ZONE 2 — 로비 · 전실 대기
    s.append(rect(16.0, 6.05, 7.25, 2.55, "zone2"))
    s.append(bank(19.65, 7.55, 4, 'n') + bank(19.65, 8.13, 4, 's'))
    s.append(bank(22.96, 7.30, 3, 'w'))
    s.append(wheel(18.3, 7.15))
    s.append(text(16.25, 7.75, "ZONE 2  로비 대기", "zt2"))
    s.append(text(16.25, 8.45, "11석", "cnt"))

    # ZONE 3 — 간호부 동측 편입
    s.append(rect(15.2, 11.0, 3.8, 3.0, "zone3"))
    s.append(bank(16.00, 12.21, 5, 'n') + bank(16.00, 12.79, 5, 's'))
    s.append(text(15.35, 11.62, "ZONE 3  간호부 편입", "zt3"))
    s.append(text(15.35, 13.78, "10석", "cnt"))
    s.append(text(18.9, 13.75, "3,800 × 3,000", "dim", "end"))

    for dx, dy, lab in [(18.72, 9.52, "1"), (19.3, 6.45, "2"), (22.3, 11.4, "3")]:
        s.append(f'<circle class="disp" cx="{X(dx)}" cy="{Y(dy)}" r="2.3"/>')
        s.append(text(dx, dy + 0.22, lab, "dispt", "middle"))
    return "".join(s) + '</g>'

# ═══ 의자 비교 ═════════════════════════════════════════════════════════════
def chairs():
    U = 0.05
    def u(mm): return round(mm * U, 2)
    def d2(cx, cy, f=True):
        return f'<circle class="{"occ2" if f else "lost2"}" cx="{cx}" cy="{cy}" r="4.4"/>'
    s = []
    for y in (20, 76):
        s.append(f'<line class="base" x1="10" y1="{y}" x2="{10+u(3600)}" y2="{y}"/>')
    for k in range(2):
        x = 10 + u(1800) * k
        s.append(f'<rect class="bench2" x="{x}" y="20" width="{u(1800)}" '
                 f'height="{u(700)}" rx="1.5"/>')
        s.append(f'<line class="bench-back2" x1="{x}" y1="20" x2="{x+u(1800)}" y2="20"/>')
        for j in range(4):
            s.append(d2(x + u(225) + u(450) * j, 20 + u(380), j < 3))
    s.append('<text class="ct" x="10" y="13">현재 · 무팔걸이 벤치소파 1,800 × 700</text>')
    s.append(f'<text class="cd" x="{10+u(3600)}" y="13" text-anchor="end">'
             f'공칭 8석 → 실착석 5.2</text>')
    s.append(f'<text class="cd" x="{10+u(3600)+6}" y="{20+u(420)}">깊이 700</text>')
    n = 7
    s.append(f'<rect class="gang" x="10" y="76" width="{u(500*n)}" '
             f'height="{u(580)}" rx="1.5"/>')
    s.append(f'<line class="seat-back2" x1="10" y1="76" x2="{10+u(500*n)}" y2="76"/>')
    for j in range(n + 1):
        x = 10 + u(500) * j
        s.append(f'<line class="arm2" x1="{x}" y1="78" x2="{x}" y2="{76+u(580)-2}"/>')
    for j in range(n):
        s.append(d2(10 + u(250) + u(500) * j, 76 + u(330)))
    s.append('<text class="ct" x="10" y="69">제안 · 팔걸이 분리형 연결의자 500 × 580</text>')
    s.append(f'<text class="cd" x="{10+u(3600)}" y="69" text-anchor="end">'
             f'공칭 7석 → 실착석 6.7</text>')
    s.append(f'<text class="cd" x="{10+u(500*n)+6}" y="{76+u(340)}">깊이 580</text>')
    s.append(f'<line class="dimline" x1="10" y1="114" x2="{10+u(3600)}" y2="114"/>')
    s.append('<line class="dimtick" x1="10" y1="109" x2="10" y2="119"/>')
    s.append(f'<line class="dimtick" x1="{10+u(3600)}" y1="109" x2="{10+u(3600)}" y2="119"/>')
    s.append(f'<text class="cd" x="{10+u(1800)}" y="127" text-anchor="middle">'
             f'동일 벽면 3,600 기준</text>')
    return "".join(s)

CSS = """
.wall{stroke:var(--pl-wall);stroke-width:1.6;fill:none}
.cut{stroke:var(--pl-ink3);stroke-width:1;stroke-dasharray:5 2 1 2;fill:none}
.core{fill:var(--pl-solid)}
.fix{fill:var(--pl-solid)}
.col{fill:var(--pl-wall)}
.arrow{stroke:var(--pl-accent);stroke-width:1;fill:none;marker-end:url(#ah)}
.room{fill:var(--pl-room);stroke:var(--pl-wall);stroke-width:.8}
.room2{fill:var(--pl-room2);stroke:var(--pl-wall);stroke-width:.5}
.counter{fill:var(--pl-counter)}
.back{fill:var(--pl-room2);stroke:var(--pl-wall);stroke-width:.5;stroke-dasharray:1.6 1.2}
.bench,.benchc{fill:var(--pl-bench);stroke:var(--pl-benchs);stroke-width:.6}
.bench-back{stroke:var(--pl-benchs);stroke-width:1.4}
.occ{fill:var(--pl-occ)}
.lost{fill:none;stroke:var(--pl-lost);stroke-width:.7;stroke-dasharray:1.1 .9}
.seat{fill:var(--pl-seat);stroke:var(--pl-seats);stroke-width:.5}
.seat-back{stroke:var(--pl-seats);stroke-width:1.5;stroke-linecap:round}
.arm{stroke:var(--pl-arm);stroke-width:.85;stroke-linecap:round}
.wc{fill:var(--pl-wc);stroke:var(--pl-accent);stroke-width:.6;stroke-dasharray:1.4 1}
.disp{fill:var(--pl-accent)}
.zone-now{fill:var(--pl-znow);stroke:var(--pl-lost);stroke-width:.6;stroke-dasharray:2 1.4}
.zone1{fill:var(--pl-z1);stroke:var(--pl-z1s);stroke-width:.6}
.zone2{fill:var(--pl-z2);stroke:var(--pl-z2s);stroke-width:.6}
.zone3{fill:var(--pl-z3);stroke:var(--pl-z3s);stroke-width:.6}
.void{fill:var(--pl-void);stroke:var(--pl-voids);stroke-width:.5;stroke-dasharray:1.4 1.4}
.demo{stroke:var(--pl-demo);stroke-width:2;stroke-dasharray:2.4 1.6;stroke-linecap:round}
.flow{stroke:var(--pl-flow);stroke-width:1.4;stroke-dasharray:3 2;fill:none}
.north{stroke:var(--pl-ink2);stroke-width:.8;fill:var(--pl-ink2)}
.scale{stroke:var(--pl-ink2);stroke-width:.7}
text{font-family:var(--fs);fill:var(--pl-ink)}
.lbl{font-size:3px;font-weight:700;letter-spacing:.04em}
.lbl-w{font-size:2.6px;font-weight:700;fill:var(--pl-oncounter)}
.mini{font-size:2.5px;font-weight:600;fill:var(--pl-ink2)}
.dim{font-family:var(--fm);font-size:2.3px;fill:var(--pl-ink3)}
.zt{font-size:2.8px;font-weight:700;fill:var(--pl-lost)}
.zt1{font-size:2.8px;font-weight:700;fill:var(--pl-z1s)}
.zt2{font-size:2.8px;font-weight:700;fill:var(--pl-z2s)}
.zt3{font-size:2.8px;font-weight:700;fill:var(--pl-z3s)}
.cnt{font-family:var(--fm);font-size:4.4px;font-weight:700;fill:var(--pl-accent)}
.voidt{font-size:2.5px;font-weight:600;fill:var(--pl-voids)}
.cutt{font-family:var(--fm);font-size:2.2px;fill:var(--pl-ink3)}
.demot{font-family:var(--fm);font-size:2.3px;fill:var(--pl-demo)}
.dispt{font-size:2.4px;font-weight:700;fill:var(--pl-ondisp)}
.wct{font-size:2.1px;font-weight:700;fill:var(--pl-accent)}
"""

CSS_CHAIR = """
text{font-family:var(--fs);fill:var(--pl-ink)}
.base{stroke:var(--pl-wall);stroke-width:2}
.bench2{fill:var(--pl-bench);stroke:var(--pl-benchs);stroke-width:.9}
.bench-back2{stroke:var(--pl-benchs);stroke-width:3}
.gang{fill:var(--pl-seat);stroke:var(--pl-seats);stroke-width:.9}
.seat-back2{stroke:var(--pl-seats);stroke-width:3}
.arm2{stroke:var(--pl-arm);stroke-width:1.8;stroke-linecap:round}
.occ2{fill:var(--pl-occ)}
.lost2{fill:none;stroke:var(--pl-lost);stroke-width:1.2;stroke-dasharray:2 1.6}
.dimline,.dimtick{stroke:var(--pl-ink3);stroke-width:.8}
.ct{font-size:6px;font-weight:700}
.cd{font-family:var(--fm);font-size:5.2px;fill:var(--pl-ink3)}
"""

DEFS = ('<defs><marker id="ah" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="4" '
        'markerHeight="4" orient="auto"><path d="M0 0 L6 3 L0 6 z" '
        'fill="var(--pl-accent)"/></marker></defs>')

def svg(body, label, vb=VB, css=CSS, defs=DEFS):
    return (f'<svg viewBox="{vb}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg"><style>{css}</style>{defs}{body}</svg>')

if __name__ == "__main__":
    import os
    d = os.path.dirname(os.path.abspath(__file__))
    for fn, body, lab in [
            ("plan_before.svg", before(), "동측 공용부 현황 — 대기 실효 15석"),
            ("plan_after.svg", after(), "동측 공용부 개선 B안 — 대기 41석")]:
        open(os.path.join(d, fn), "w").write(svg(body, lab))
    open(os.path.join(d, "chairs.svg"), "w").write(
        svg(chairs(), "의자 비교 — 동일 벽면 3,600 실착석", "0 0 226 138", CSS_CHAIR, ""))
    print("written 3 svg")
