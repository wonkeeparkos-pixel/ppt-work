# -*- coding: utf-8 -*-
"""웹덱 슬라이드 넘침 검사 — .pad 의 scrollHeight 가 clientHeight 를 넘으면 보고."""
import sys
from playwright.sync_api import sync_playwright

HTML = sys.argv[1] if len(sys.argv) > 1 else \
    "/home/user/ppt-work/문헌고찰_손경련/손경련_발표_웹_v1.0.html"

with sync_playwright() as p:
    br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
    pg = br.new_page(viewport={"width": 1600, "height": 900})
    pg.goto("file://" + HTML)
    pg.wait_for_timeout(2000)
    res = pg.evaluate("""() => [...document.querySelectorAll('.pad')].map((el,i)=>{
        const t = el.querySelector('h2.ct, h1.t, h2.kh');
        return {n:i+1, over: el.scrollHeight - el.clientHeight,
                title: t ? t.textContent.slice(0,34) : ''};
    })""")
    br.close()

bad = [r for r in res if r["over"] > 2]
for r in res:
    flag = "  ⚠ OVER" if r["over"] > 2 else ""
    print(f'{r["n"]:>3}  넘침 {r["over"]:>4}px  {r["title"]}{flag}')
print(f"\n넘치는 슬라이드: {len(bad)} / {len(res)}")
