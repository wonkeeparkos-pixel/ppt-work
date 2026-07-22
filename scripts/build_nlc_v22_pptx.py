# -*- coding: utf-8 -*-
"""NLC v2.2 동영상 PPTX 빌더 (재생 안정화판).
- 각 웹 슬라이드를 16:9 PNG로 래스터화해 풀블리드 배치(폰트 폴백 없음)
- FGA 술기(15쪽)에 실제 초음파 동영상을 임베드
- 동영상: H.264+AAC(무음 트랙 포함) — 오디오 없는 MP4가 PPT에서 재생 안 되는
  문제를 회피. 슬라이드 진입 시 '자동 재생'되도록 timing 트리를 재작성."""
import os, glob
from pptx import Presentation
from pptx.util import Inches
from pptx.oxml.ns import qn
from lxml import etree

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/01_NLC"
SCRATCH = "/tmp/claude-0/-home-user-ppt-work/bb19d1cb-d1ba-542e-8235-38fcac774773/scratchpad"
PNG_DIR = os.path.join(SCRATCH, "png")
MOVIE   = os.path.join(SCRATCH, "fga_video_v2.mp4")
POSTER  = os.path.join(BASE, "assets/fga_us.jpg")
OUT     = os.path.join(BASE, "NLC_발표_v2.3_동영상.pptx")

FGA_PAGE = 15
VID = dict(left=0.859, top=2.250, width=5.219, height=3.625)
DUR_MS = 4000  # 동영상 길이(ms)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

pngs = sorted(glob.glob(os.path.join(PNG_DIR, "s*.png")))
assert len(pngs) == 21, f"expected 21 pngs, got {len(pngs)}"


def autoplay_timing_xml(spid, dur_ms):
    """슬라이드 진입 시 자동 재생되는 media timing 트리 (PowerPoint 표준 구조)."""
    P = "http://schemas.openxmlformats.org/presentationml/2006/main"
    return f'''<p:timing xmlns:p="{P}">
  <p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>
    <p:seq concurrent="1" nextAc="seek">
      <p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>
        <p:par><p:cTn id="3" fill="hold"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:childTnLst>
          <p:par><p:cTn id="4" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>
            <p:par><p:cTn id="5" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="afterEffect">
              <p:stCondLst><p:cond delay="0"/></p:stCondLst>
              <p:childTnLst>
                <p:cmd type="call" cmd="playFrom(0.0)">
                  <p:cBhvr><p:cTn id="6" dur="{dur_ms}" fill="hold"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr>
                </p:cmd>
              </p:childTnLst>
            </p:cTn></p:par>
          </p:childTnLst></p:cTn></p:par>
        </p:childTnLst></p:cTn></p:par>
      </p:childTnLst></p:cTn>
      <p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>
      <p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>
    </p:seq>
    <p:video><p:cMediaNode vol="80000">
      <p:cTn id="7" fill="hold" display="0"><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
        <p:endCondLst><p:cond evt="onStopped" delay="0"><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cond></p:endCondLst>
      </p:cTn>
      <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
    </p:cMediaNode></p:video>
  </p:childTnLst></p:cTn></p:par></p:tnLst>
</p:timing>'''


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
        spid = mv.shape_id
        # remove python-pptx's default (click-to-play) timing, insert autoplay timing
        sld = s._element
        old = sld.find(qn('p:timing'))
        if old is not None:
            sld.remove(old)
        new_timing = etree.fromstring(autoplay_timing_xml(spid, DUR_MS))
        sld.append(new_timing)
        print(f"  slide {i}: autoplay movie, spid={spid}, {VID['width']}x{VID['height']}in @ {VID['left']},{VID['top']}")

prs.save(OUT)
print("saved:", OUT, "|", round(os.path.getsize(OUT)/1e6, 2), "MB | slides", len(prs.slides._sldIdLst))
