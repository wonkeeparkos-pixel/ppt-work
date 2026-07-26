# -*- coding: utf-8 -*-
"""Drive 03_LSB 미디어에서 덱용 그림 생성 (bigfig 슬롯 비율 ≈ 3:1 에 맞춘 1×4 가로 배열).
 - lsb_fluoro_steps.png : 실제 투시 술기 4단계 (TheProcedureGuide 영상)
 - lsb_anim_steps.png   : 3D 애니메이션 4단계 (표적·확산)
"""
import cv2
import textwrap
from PIL import Image, ImageDraw, ImageFont

BOLD = "/tmp/pretendard/Pretendard-Bold.otf"
LIGHT = "/tmp/pretendard/Pretendard-Light.otf"
BG = (14, 17, 24)
TILE, PAD, LABEL_H = 720, 24, 242


def montage(src, panels, out, crop_w=None, wrap=22):
    cap = cv2.VideoCapture(src)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    for t, _, _ in panels:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ok, fr = cap.read()
        assert ok, f"{src} @ {t}s"
        if crop_w:
            fr = fr[:, :crop_w]
        frames.append(cv2.resize(fr, (TILE, TILE), interpolation=cv2.INTER_CUBIC))
    cap.release()

    n = len(panels)
    W = n * TILE + (n + 1) * PAD
    H = TILE + LABEL_H + 2 * PAD
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    f_num = ImageFont.truetype(BOLD, 52)
    f_lab = ImageFont.truetype(LIGHT, 40)

    for i, (frame, (_, num, text)) in enumerate(zip(frames, panels)):
        x = PAD + i * (TILE + PAD)
        y = PAD
        canvas.paste(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)), (x, y))
        d.rectangle([x, y, x + TILE - 1, y + TILE - 1], outline=(70, 78, 92), width=3)
        ty = y + TILE + 26
        d.text((x, ty), num, font=f_num, fill=(232, 168, 116))
        for line in textwrap.wrap(text, wrap):
            d.text((x + 66, ty + 6), line, font=f_lab, fill=(226, 230, 238))
            ty += 52
    canvas.save(out)
    print("wrote", out, canvas.size, f"ratio={W/H:.2f}")


# 실제 투시 술기 — 프레임 좌측 356px가 투시화면(우측은 영문 캡션이라 잘라냄)
montage("v4_5min.mp4", [
    (84,  "①", "사위상(Scotty dog) — L2 하외측연에 바늘 접촉"),
    (90,  "②", "척추체 따라 외측으로 walk — 전외측으로"),
    (106, "③", "측면상 — L2·L3 바늘이 척추체 전방까지"),
    (118, "④", "정면상 — 최종 위치에서 바늘 끝이 더 내측"),
], "fig_fluoro_steps.png", crop_w=356)

# 3D 애니메이션 — 전체 프레임 사용
montage("v2_animation.mp4", [
    (9,  "①", "표적: 척추체 전외측 교감신경간(분홍)"),
    (17, "②", "피부·연부조직 국소마취"),
    (30, "③", "바늘 끝을 교감신경간 옆으로"),
    (36, "④", "약물 확산 — 신경간을 따라 종방향"),
], "fig_anim_steps.png")
