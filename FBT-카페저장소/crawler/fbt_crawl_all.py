# -*- coding: utf-8 -*-
"""
FBT 카페 여러 게시판 한 번에 크롤러 (G드라이브 저장)
- BOARDS에 적은 게시판들을 순서대로 전부 수집 (본문 + 사진 + 댓글)
- 전체공지(여러 게시판에 중복 등장하는 글)는 자동으로 제외
- 같은 글이 여러 게시판에 보여도 한 번만 저장, 이미 저장한 글은 건너뜀
- 주 1회 다시 돌리면 새 글만 추가됨
"""
import os, re, json, sys, time, random, glob
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ============== 설정 ==============
CAFE_ID = "31251118"
# 모을 게시판 번호들 (여기에 추가/삭제만 하면 됨)
BOARDS = ["29", "30", "31", "32", "33", "34", "38"]

OUT_ROOT    = r"G:\내 드라이브\claude\FBT\data"   # 결과물: 구글드라이브 (C+클라우드 동시)
PROFILE_DIR = r"C:\FBT\.browser"                  # 로그인 정보: C드라이브에만

# 이미 확인된 전체공지 글번호 (확실하게 제외)
NOTICE_IDS_SEED = {"16", "447", "904", "1493", "1770", "2307", "2681",
                   "2889", "2982", "3174", "3354", "3678", "3707", "3736"}

MIN_DELAY = 4.0
MAX_DELAY = 9.0
MAX_PAGES = 200
# =================================


def log(m):
    print(m, flush=True)


def clean(t):
    return re.sub(r"\n{3,}", "\n\n", (t or "").strip())


def collect_article_ids(page, menu_id):
    base = f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/menus/{menu_id}"
    ids, seen, prev = [], set(), None
    for pg in range(1, MAX_PAGES + 1):
        page.goto(f"{base}?page={pg}", wait_until="domcontentloaded")
        page.wait_for_timeout(2200)
        page_ids = []
        for a in page.query_selector_all('a[href*="/articles/"]'):
            href = a.get_attribute("href") or ""
            m = re.search(r"/articles/(\d+)", href)
            if m:
                page_ids.append(m.group(1))
        page_ids = list(dict.fromkeys(page_ids))
        if not page_ids:
            break
        if prev is not None and page_ids == prev:
            break
        for i in page_ids:
            if i not in seen:
                seen.add(i); ids.append(i)
        prev = page_ids
        page.wait_for_timeout(int(random.uniform(1.0, 2.2) * 1000))
    return ids


def already_saved_anywhere(article_id):
    # 어느 게시판 폴더든 이미 저장돼 있으면 True
    return bool(glob.glob(os.path.join(OUT_ROOT, "*", f"{article_id}_*")))


def crawl_article(page, ctx, menu_id, article_id):
    url = (f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/articles/{article_id}"
           f"?menuid={menu_id}&referrerAllArticles=false")
    page.goto(url, wait_until="domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except Exception:
        pass
    page.wait_for_timeout(2500)
    for _ in range(8):
        try:
            page.mouse.wheel(0, 4000)
        except Exception:
            pass
        page.wait_for_timeout(400)
    page.wait_for_timeout(1000)

    frame = page
    if page.query_selector("iframe#cafe_main"):
        frame = page.frame(name="cafe_main") or page

    def q_text(sels):
        for s in sels:
            try:
                el = frame.query_selector(s)
                if el:
                    t = el.inner_text().strip()
                    if t:
                        return t
            except Exception:
                pass
        return ""

    title  = q_text([".ArticleTitle .title_text", ".title_text", "h3.title_text",
                     ".article_header h3", ".tit-box .tit"])
    writer = q_text([".WriterInfo .nickname", ".nick_box .nickname",
                     ".profile_area .nickname", ".nickname"])
    date   = q_text([".WriterInfo .date", ".article_info .date", ".date"])

    body_el = None
    for s in [".se-main-container", ".article_viewer", ".ContentRenderer",
              ".content_box", ".NHN_Writeform_Main", ".se_component_wrap"]:
        try:
            body_el = frame.query_selector(s)
        except Exception:
            body_el = None
        if body_el:
            break
    body_text = clean(body_el.inner_text()) if body_el else ""

    img_urls = []
    scope = body_el if body_el else frame
    try:
        for img in scope.query_selector_all("img"):
            src = img.get_attribute("src") or img.get_attribute("data-src") or ""
            if src.startswith("http") and "static.nid" not in src and "cafe_meta" not in src:
                img_urls.append(src)
    except Exception:
        pass
    img_urls = list(dict.fromkeys(img_urls))

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
        ct = cin([".text_comment", ".comment_text_view", ".comment_content", ".u_cbox_contents"])
        cd = cin([".comment_info_date", ".comment_created_at", "time", ".date",
                  '[class*="date"]', '[class*="Date"]'])
        if ct:
            comments.append({"nick": cn, "date": cd, "text": ct})

    safe = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", title)[:50] or article_id
    folder = os.path.join(OUT_ROOT, menu_id, f"{article_id}_{safe}")
    img_dir = os.path.join(folder, "images")
    os.makedirs(img_dir, exist_ok=True)

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
        except Exception:
            pass

    data = {"cafe_id": CAFE_ID, "menu_id": menu_id, "article_id": article_id,
            "url": url, "title": title, "writer": writer, "date": date,
            "body_text": body_text, "images": saved_imgs, "comments": comments}
    with open(os.path.join(folder, "article.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    md = [f"# {title}", "", f"- 작성자: {writer}", f"- 날짜: {date}", f"- 원문: {url}",
          "", "---", "", body_text, ""]
    if saved_imgs:
        md.append("## 첨부 이미지")
        for fn in saved_imgs:
            md.append(f"![{fn}](images/{fn})")
        md.append("")
    if comments:
        md.append(f"## 댓글 ({len(comments)}개)")
        for c in comments:
            d = f" ({c['date']})" if c['date'] else ""
            md.append(f"- **{c['nick']}**{d}: {c['text']}")
    with open(os.path.join(folder, "article.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    return {"title": title, "body": len(body_text), "imgs": len(saved_imgs),
            "cmts": len(comments)}


def main():
    os.makedirs(PROFILE_DIR, exist_ok=True)
    os.makedirs(OUT_ROOT, exist_ok=True)
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"])
        page = ctx.pages[0] if ctx.pages else ctx.new_page()

        log(">> 카페를 여는 중...")
        page.goto(f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}", wait_until="domcontentloaded")
        page.wait_for_timeout(2500)
        log("")
        log(">> 크롬 창에서 로그인 확인 후, 이 검은 창에서  Esc → Enter")
        input()

        # ---- 1단계: 게시판별 글 목록 수집 ----
        log("\n>> [1단계] 게시판별 글 목록을 수집합니다...")
        board_ids = {}
        for mid in BOARDS:
            lst = collect_article_ids(page, mid)
            board_ids[mid] = lst
            log(f"   게시판 {mid}: {len(lst)}개")

        # ---- 전체공지 자동 감지 (2개 이상 게시판에 중복 등장) ----
        cnt = {}
        for mid, lst in board_ids.items():
            for i in set(lst):
                cnt[i] = cnt.get(i, 0) + 1
        notices = {i for i, c in cnt.items() if c >= 2} | NOTICE_IDS_SEED
        log(f"\n>> 전체공지로 판단되어 제외할 글: {len(notices)}개")

        # ---- 크롤 대상 정리 ----
        seen = set()
        todo_per_board = {}
        total_todo = 0
        for mid in BOARDS:
            todo = []
            for i in board_ids[mid]:
                if i in notices:
                    continue
                if i in seen:
                    continue
                if already_saved_anywhere(i):
                    seen.add(i)
                    continue
                seen.add(i)
                todo.append(i)
            todo_per_board[mid] = todo
            total_todo += len(todo)
            log(f"   게시판 {mid}: 새로 저장할 글 {len(todo)}개")

        log(f"\n>> 새로 저장할 글 합계: {total_todo}개")
        if total_todo == 0:
            log(">> 새로 저장할 글이 없습니다. 종료합니다.")
            input(">> Enter로 종료...")
            ctx.close()
            return

        log(">> 시작하려면  Esc → Enter  (그만하려면 창을 닫으세요)")
        input()

        # ---- 2단계: 크롤링 ----
        idx = 0
        done = 0
        for mid in BOARDS:
            for aid in todo_per_board[mid]:
                idx += 1
                try:
                    r = crawl_article(page, ctx, mid, aid)
                    done += 1
                    log(f"[{idx}/{total_todo}] (게시판{mid}) {aid}  "
                        f"본문{r['body']}자 사진{r['imgs']} 댓글{r['cmts']}  {r['title'][:26]}")
                except Exception as e:
                    log(f"[{idx}/{total_todo}] (게시판{mid}) {aid}  실패: {e}")
                time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
                if idx % 40 == 0:
                    log("   ...잠시 쉬는 중 (30초)")
                    time.sleep(30)

        log("\n================= 완료 =================")
        log(f"저장 완료: {done}개")
        log(f"저장 위치: {OUT_ROOT}")
        log("=======================================")
        input(">> Enter로 종료...")
        ctx.close()


if __name__ == "__main__":
    main()
