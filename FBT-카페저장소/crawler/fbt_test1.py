# -*- coding: utf-8 -*-
"""
FBT 카페 크롤러 - 1개 글 테스트 버전
글 하나(제목 + 본문 + 사진 + 댓글)를 폴더 하나로 저장해서
제대로 긁히는지 확인하는 용도입니다.
"""
import os, re, json, sys
from playwright.sync_api import sync_playwright

# 콘솔에 한글이 깨지지 않게
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ================= 설정 =================
CAFE_ID    = "31251118"     # functionalbt 카페 고유번호
MENU_ID    = "29"           # 게시판 번호
ARTICLE_ID = "3088"         # 테스트로 저장할 글 번호
BASE_DIR   = r"C:\FBT"
PROFILE_DIR = os.path.join(BASE_DIR, ".browser")   # 로그인 정보 저장 폴더
OUT_ROOT    = os.path.join(BASE_DIR, "data")        # 크롤링 결과 저장 폴더
# =======================================

ART_URL = (f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/articles/{ARTICLE_ID}"
           f"?menuid={MENU_ID}&referrerAllArticles=false")


def log(m):
    print(m, flush=True)


def main():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    captured = {}

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE_DIR,
            headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],
        )
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        # 네이버 내부 API 응답도 몰래 받아서 백업(디버그용)
        def on_response(resp):
            u = resp.url
            try:
                if "cafe-articleapi" in u and "/articles/" in u and "/comments" not in u:
                    captured["article_api"] = resp.json()
                elif "cafe-articleapi" in u and "comments" in u:
                    captured["comments_api"] = resp.json()
            except Exception:
                pass
        page.on("response", on_response)

        # --- 1) 로그인 확인 ---
        log(">> 카페를 여는 중입니다...")
        page.goto(f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        log("")
        log(">> 지금 열린 크롬 창에서 카페가 보이고 '로그인' 되어 있는지 확인하세요.")
        log(">> (로그인이 안 되어 있으면 그 창에서 지금 네이버 로그인 하세요.)")
        input(">> 준비되면 이 검은 창을 클릭하고 Enter 키를 누르세요... ")

        # --- 2) 글 열기 ---
        log(f">> 글 {ARTICLE_ID}번을 여는 중...")
        page.goto(ART_URL, wait_until="domcontentloaded")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        page.wait_for_timeout(3000)

        # 사진/댓글이 스크롤해야 나오는 경우가 있어 끝까지 내려줌
        for _ in range(8):
            try:
                page.mouse.wheel(0, 4000)
            except Exception:
                pass
            page.wait_for_timeout(500)
        page.wait_for_timeout(1500)

        # 신형은 메인 프레임, 구형은 iframe(cafe_main) 안에 본문이 있음
        frame = page
        if page.query_selector("iframe#cafe_main"):
            frame = page.frame(name="cafe_main") or page

        def q_text(selectors):
            for s in selectors:
                try:
                    el = frame.query_selector(s)
                    if el:
                        t = el.inner_text().strip()
                        if t:
                            return t
                except Exception:
                    pass
            return ""

        # --- 3) 제목 / 작성자 / 날짜 ---
        title  = q_text([".ArticleTitle .title_text", ".title_text",
                         "h3.title_text", ".article_header h3", ".tit-box .tit"])
        writer = q_text([".WriterInfo .nickname", ".nick_box .nickname",
                         ".profile_area .nickname", ".nickname"])
        date   = q_text([".WriterInfo .date", ".article_info .date", ".date"])

        # --- 4) 본문 ---
        body_el = None
        for s in [".se-main-container", ".article_viewer", ".ContentRenderer",
                  ".content_box", ".NHN_Writeform_Main", ".se_component_wrap"]:
            try:
                body_el = frame.query_selector(s)
            except Exception:
                body_el = None
            if body_el:
                break
        body_text = body_el.inner_text().strip() if body_el else ""

        # --- 5) 이미지 URL 모으기 ---
        img_urls = []
        search_scope = body_el if body_el else frame
        try:
            for img in search_scope.query_selector_all("img"):
                src = img.get_attribute("src") or img.get_attribute("data-src") or ""
                if src.startswith("http") and "static.nid" not in src \
                   and "cafe_meta" not in src:
                    img_urls.append(src)
        except Exception:
            pass
        img_urls = list(dict.fromkeys(img_urls))  # 중복 제거

        # --- 6) 댓글 ---
        comments = []
        c_items = []
        for s in [".CommentItem", "li.comment_item", ".comment_list li",
                  ".u_cbox_comment", ".comment_area li"]:
            try:
                c_items = frame.query_selector_all(s)
            except Exception:
                c_items = []
            if c_items:
                break
        for c in c_items:
            def cin(sels):
                for s in sels:
                    try:
                        e = c.query_selector(s)
                        if e:
                            t = e.inner_text().strip()
                            if t:
                                return t
                    except Exception:
                        pass
                return ""
            cn = cin([".comment_nickname", ".nickname", ".u_cbox_nick"])
            ct = cin([".text_comment", ".comment_text_view",
                      ".comment_content", ".u_cbox_contents"])
            cd = cin([".comment_info .date", ".date", ".u_cbox_date"])
            if ct:
                comments.append({"nick": cn, "date": cd, "text": ct})

        # --- 7) 저장 폴더 만들기 ---
        safe_title = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", title)[:50] or ARTICLE_ID
        folder = os.path.join(OUT_ROOT, MENU_ID, f"{ARTICLE_ID}_{safe_title}")
        img_dir = os.path.join(folder, "images")
        os.makedirs(img_dir, exist_ok=True)

        # --- 8) 이미지 다운로드(로그인된 상태 + Referer로) ---
        saved_imgs = []
        for i, u in enumerate(img_urls, 1):
            try:
                r = ctx.request.get(u, headers={"Referer": "https://cafe.naver.com/"})
                if r.ok:
                    m = re.search(r"\.(jpg|jpeg|png|gif|webp)", u.lower())
                    ext = "." + m.group(1) if m else ".jpg"
                    fn = f"img_{i:02d}{ext}"
                    with open(os.path.join(img_dir, fn), "wb") as f:
                        f.write(r.body())
                    saved_imgs.append(fn)
            except Exception as e:
                log(f"   - 이미지 {i} 실패: {e}")

        # --- 9) article.json (완결 데이터) ---
        data = {
            "cafe_id": CAFE_ID, "menu_id": MENU_ID, "article_id": ARTICLE_ID,
            "url": ART_URL, "title": title, "writer": writer, "date": date,
            "body_text": body_text, "images": saved_imgs, "comments": comments,
        }
        with open(os.path.join(folder, "article.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # --- 10) article.md (사람이 읽기 좋은 버전) ---
        md = [f"# {title}", "",
              f"- 작성자: {writer}", f"- 날짜: {date}", f"- 원문: {ART_URL}",
              "", "---", "", body_text, ""]
        if saved_imgs:
            md.append("## 첨부 이미지")
            for fn in saved_imgs:
                md.append(f"![{fn}](images/{fn})")
            md.append("")
        if comments:
            md.append(f"## 댓글 ({len(comments)}개)")
            for c in comments:
                md.append(f"- **{c['nick']}** ({c['date']}): {c['text']}")
        with open(os.path.join(folder, "article.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(md))

        # --- 11) 디버그 자료 저장(문제 있을 때 확인용) ---
        dbg = os.path.join(folder, "_debug")
        os.makedirs(dbg, exist_ok=True)
        try:
            with open(os.path.join(dbg, "page.html"), "w", encoding="utf-8") as f:
                f.write(page.content())
        except Exception:
            pass
        for key, name in [("article_api", "article_api.json"),
                          ("comments_api", "comments_api.json")]:
            if captured.get(key):
                with open(os.path.join(dbg, name), "w", encoding="utf-8") as f:
                    json.dump(captured[key], f, ensure_ascii=False, indent=2)
        try:
            page.screenshot(path=os.path.join(dbg, "screenshot.png"), full_page=True)
        except Exception:
            pass

        # --- 12) 결과 요약 출력 ---
        log("\n================= 결과 =================")
        log(f"제목    : {title}")
        log(f"작성자  : {writer}")
        log(f"날짜    : {date}")
        log(f"본문    : {len(body_text)}자  (앞부분: {body_text[:60]}...)")
        log(f"이미지  : {len(saved_imgs)}개 저장")
        log(f"댓글    : {len(comments)}개")
        log(f"저장위치: {folder}")
        log("=======================================")
        log(">> 위 내용을 복사해서 알려주세요. 확인 후 Enter 누르면 종료합니다.")
        input()
        ctx.close()


if __name__ == "__main__":
    main()
