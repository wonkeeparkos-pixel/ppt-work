# -*- coding: utf-8 -*-
"""
FBT 카페 게시판 목록 뽑기
- 이 카페에 있는 모든 게시판의 이름과 번호(menuid)를 출력합니다.
- 크롤링은 하지 않고, 목록만 보여주고 끝납니다.
"""
import os, re, sys
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

CAFE_ID = "31251118"
PROFILE_DIR = r"C:\FBT\.browser"   # 로그인 정보 (기존 것 그대로 사용)


def main():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        print(">> 카페를 여는 중...")
        page.goto(f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}", wait_until="domcontentloaded")
        page.wait_for_timeout(4000)
        print("")
        print(">> 크롬 창에서 로그인 확인 후, 이 검은 창에서  Esc → Enter  하세요.")
        input()

        # 사이드바가 다 뜨도록 조금 스크롤
        for _ in range(4):
            try:
                page.mouse.wheel(0, 2000)
            except Exception:
                pass
            page.wait_for_timeout(400)

        # 게시판 링크(menus/번호) 모으기
        boards = {}
        for a in page.query_selector_all('a[href*="/menus/"]'):
            href = a.get_attribute("href") or ""
            m = re.search(r"/menus/(\d+)", href)
            if not m:
                continue
            mid = m.group(1)
            name = (a.inner_text() or "").strip().split("\n")[0].strip()
            name = re.sub(r"\s+", " ", name)
            if name and mid not in boards:
                boards[mid] = name

        print("\n=============== 게시판 목록 ===============")
        # 번호 순으로 정렬해서 보기 좋게
        for mid in sorted(boards, key=lambda x: int(x)):
            print(f"menuid {mid} : {boards[mid]}")
        print("==========================================")
        print(f"총 {len(boards)}개 게시판 발견")
        print(">> 위 목록을 통째로 복사해서 알려주세요.")
        input(">> 확인 후 Enter로 종료...")
        ctx.close()


if __name__ == "__main__":
    main()
