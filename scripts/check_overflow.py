# -*- coding: utf-8 -*-
"""각 슬라이드의 내용이 16:9 스테이지를 넘치는지 검사."""
import os
import sys
import glob
import asyncio
from playwright.async_api import async_playwright

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    REPO, "문헌고찰_보툴리눔_정형외과통증", "보툴리눔_정형외과통증_발표_웹.html")


async def main():
    async with async_playwright() as p:
        pre = glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
        b = await p.chromium.launch(
            executable_path=pre[0] if pre else None, args=["--no-sandbox"]
        )
        page = await b.new_page(viewport={"width": 1280, "height": 720})
        await page.goto("file://" + HTML)
        await page.wait_for_timeout(2200)
        await page.add_style_tag(content="""
          .deck{height:auto!important;overflow:visible!important;scroll-snap-type:none!important}
          .snap{height:auto!important;padding:0!important;display:block!important}
          .stage{width:1280px!important;max-width:none!important}
        """)
        await page.wait_for_timeout(400)
        # flex 컬럼이 넘치면 .foot(margin-top:auto)와 본문이 겹친다 → 둘 다 잡는다
        res = await page.evaluate("""() => {
          const SEL = '.pad,.row,.col,.aside,.cols,.cols .c,.figbox,.bigimg,ul.b';
          return [...document.querySelectorAll('.stage')].map((st,i)=>{
            const pad = st.querySelector('.pad');
            let over = 0, where='';
            pad.parentElement.querySelectorAll(SEL).forEach(el=>{
              const d = el.scrollHeight - el.clientHeight;
              if (d > over) { over = d; where = el.className || el.tagName; }
            });
            const kids = [...pad.children];
            for (let k=1;k<kids.length;k++){
              const a = kids[k-1].getBoundingClientRect();
              const b = kids[k].getBoundingClientRect();
              const d = Math.round(a.bottom - b.top);
              if (a.height && b.height && d > over) { over = d; where = 'sibling-overlap'; }
            }
            return {n:i+1, over: Math.round(over), where};
          });
        }""")
        bad = [r for r in res if r["over"] > 0]
        for r in bad:
            print(f"  OVERFLOW slide {r['n']:02d}: +{r['over']}px  ({r['where']})")
        print(f"{len(bad)} / {len(res)} slides overflow")
        await b.close()


asyncio.run(main())
