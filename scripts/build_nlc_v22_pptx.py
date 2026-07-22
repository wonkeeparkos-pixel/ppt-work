# -*- coding: utf-8 -*-
"""NLC v2.2 동영상 PPTX 빌더.
각 웹 슬라이드를 16:9 PNG로 래스터화해 풀블리드 배치(폰트 폴백 없음, 픽셀 동일),
FGA 술기 슬라이드(15쪽)에 실제 초음파 동영상을 재생 가능하도록 오버레이."""
import os, glob
from pptx import Presentation
from pptx.util import Inches

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/01_NLC"
SCRATCH = "/tmp/claude-0/-home-user-ppt-work/bb19d1cb-d1ba-542e-8235-38fcac774773/scratchpad"
PNG_DIR = os.path.join(SCRATCH, "png")
MOVIE   = os.path.join(SCRATCH, "fga_video_clean.mp4")
POSTER  = os.path.join(BASE, "assets/fga_us.jpg")
OUT     = os.path.join(BASE, "NLC_발표_v2.2_동영상.pptx")

# FGA 술기 슬라이드 = 15쪽 (1-indexed). 초음파 이미지 사각형(래스터에서 검출한 위치, inch)
FGA_PAGE = 15
VID = dict(left=0.859, top=2.250, width=5.219, height=3.625)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

pngs = sorted(glob.glob(os.path.join(PNG_DIR, "s*.png")))
assert len(pngs) == 20, f"expected 20 pngs, got {len(pngs)}"

for i, png in enumerate(pngs, 1):
    s = prs.slides.add_slide(BLANK)
    s.shapes.add_picture(png, 0, 0, width=prs.slide_width, height=prs.slide_height)
    if i == FGA_PAGE:
        mv = s.shapes.add_movie(
            MOVIE,
            Inches(VID["left"]), Inches(VID["top"]),
            Inches(VID["width"]), Inches(VID["height"]),
            poster_frame_image=POSTER,
            mime_type="video/mp4",
        )
        print(f"  slide {i}: movie overlaid ({VID['width']}x{VID['height']} in @ {VID['left']},{VID['top']})")

prs.save(OUT)
print("saved:", OUT, "|", round(os.path.getsize(OUT)/1e6, 2), "MB", "| slides", len(prs.slides._sldIdLst))
