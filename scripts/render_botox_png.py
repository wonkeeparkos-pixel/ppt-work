# -*- coding: utf-8 -*-
"""웹 덱의 각 슬라이드(.stage)를 16:9 PNG로 래스터화. PPTX/PDF 재료."""
import os
import sys
import asyncio
from playwright.async_api import async_playwright

HTML = sys.argv[1] if len(sys.argv) > 1 else (
    "/home/user/ppt-work/문헌고찰_보툴리눔_정형외과통증/보툴리눔_정형외과통증_발표_웹.html"
)
PNG_DIR = sys.argv[2] if len(sys.argv) > 2 else (
    "/tmp/claude-0/-home-user-ppt-work/4a16da38-a82b-5d5e-a9c9-97ae114e4ff2/scratchpad/png_botox"
)
W, H, SCALE = 1280, 720, 2


async def main():
    os.makedirs(PNG_DIR, exist_ok=True)
    for f in os.listdir(PNG_DIR):
        os.remove(os.path.join(PNG_DIR, f))
    async with async_playwright() as p:
        exe = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
        browser = await p.chromium.launch(
            executable_path=exe if os.path.exists(exe) else None,
            args=["--force-color-profile=srgb", "--no-sandbox"],
        )
        page = await browser.new_page(
            viewport={"width": W, "height": H}, device_scale_factor=SCALE
        )
        await page.goto("file://" + HTML)
        await page.wait_for_timeout(2500)
        # 스냅/애니메이션 정지 + 스테이지를 뷰포트에 꽉 채움
        await page.add_style_tag(content="""
          *{animation:none!important;transition:none!important}
          .deck{height:auto!important;overflow:visible!important;scroll-snap-type:none!important}
          .snap{height:auto!important;padding:0!important;display:block!important}
          .stage{width:%dpx!important;max-width:none!important;border-radius:0!important;box-shadow:none!important}
          .bar,.count,.hint,.deckttl{display:none!important}
        """ % W)
        await page.wait_for_timeout(600)
        stages = await page.query_selector_all(".stage")
        print("stages:", len(stages))
        for i, st in enumerate(stages, 1):
            await st.scroll_into_view_if_needed()
            await page.wait_for_timeout(90)
            await st.screenshot(path=os.path.join(PNG_DIR, f"s{i:02d}.png"))
        await browser.close()
    print("saved:", len(os.listdir(PNG_DIR)), "png ->", PNG_DIR)


asyncio.run(main())
