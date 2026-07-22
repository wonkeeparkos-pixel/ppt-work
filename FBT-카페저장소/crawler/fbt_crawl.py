# -*- coding: utf-8 -*-
"""
FBT 카페 게시판 크롤러 (게시판 전체)
- 지정한 게시판(MENU_ID)의 모든 글을 본문 + 사진 + 댓글까지 폴더 하나씩 저장
- 이미 저장한 글은 자동으로 건너뜀 (주 1회 다시 돌리면 새 글만 추가됨)
- 안전을 위해 글마다 몇 초씩 쉬면서 천천히 수집
"""
import os, re, json, sys, time, random, glob
from playwright.sync_api import sync_playwright

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ============== 설정 (여기 숫자만 바꾸면 됨) ==============
CAFE_ID  = "31251118"        # functionalbt 카페 고유번호 (고정)
MENU_ID  = "29"              # 긁을 게시판 번호  ← 게시판 바꿀 때 이 숫자만 변경

# 결과물 저장 위치 = 구글드라이브 폴더 (C드라이브 + 클라우드 양쪽에 자동 저장)
OUT_ROOT = r"G:\내 드라이브\claude\FBT\data"

# 브라우저 로그인 정보 = C드라이브에만 (클라우드에 올리면 동기화가 엉킴)
PROFILE_DIR = r"C:\FBT\.browser"

MIN_DELAY = 4.0    # 글 사이 최소 대기(초)
MAX_DELAY = 9.0    # 글 사이 최대 대기(초)
MAX_PAGES = 200    # 목록 페이지 안전 상한
MAX_ARTICLES_PER_RUN = 100000
# =====================================================


def log(m):
    print(m, flush=True)


def clean(t):
    return re.sub(r"\n{3,}", "\n\n", (t or "").strip())


def collect_article_ids(page):
    """게시판 목록을 페이지별로 넘기며 모든 글 번호를 수집"""
    base = f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/menus/{MENU_ID}"
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
            log(f"   (더 넘길 페이지가 없어 {pg - 1}페이지에서 멈춤)")
            break
        added = 0
        for i in page_ids:
            if i not in seen:
                seen.add(i); ids.append(i); added += 1
        log(f"   목록 {pg}페이지: {len(page_ids)}개 (신규 {added}, 누적 {len(ids)})")
        prev = page_ids
        page.wait_for_timeout(int(random.uniform(1.0, 2.5) * 1000))
    return ids


def already_saved(article_id):
    return bool(glob.glob(os.path.join(OUT_ROOT, MENU_ID, f"{article_id}_*")))


def crawl_article(page, ctx, article_id):
    url = (f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/articles/{article_id}"
           f"?menuid={MENU_ID}&referrerAllArticles=false")
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

    # 이미지 URL 모으기
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

    # 댓글 (날짜 선택자 보강)
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

    # 저장 폴더
    safe = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", title)[:50] or article_id
    folder = os.path.join(OUT_ROOT, MENU_ID, f"{article_id}_{safe}")
    img_dir = os.path.join(folder, "images")
    os.makedirs(img_dir, exist_ok=True)

    # 이미지 다운로드
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

    # article.json
    data = {"cafe_id": CAFE_ID, "menu_id": MENU_ID, "article_id": article_id,
            "url": url, "title": title, "writer": writer, "date": date,
            "body_text": body_text, "images": saved_imgs, "comments": comments}
    with open(os.path.join(folder, "article.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # article.md
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
        log(">> 크롬 창에서 로그인 되어 있는지 확인하세요. (안 되어 있으면 지금 로그인)")
        input(">> 준비되면 이 검은 창을 클릭하고 Enter... ")

        log(f"\n>> 게시판 {MENU_ID}번의 글 목록을 수집합니다...")
        ids = collect_article_ids(page)
        log(f"\n>> 게시판 {MENU_ID}번에서 총 {len(ids)}개 글 발견.")

        todo = [i for i in ids if not already_saved(i)]
        skip = len(ids) - len(todo)
        log(f">> 이미 저장됨: {skip}개  /  새로 저장할 글: {len(todo)}개")
        if not todo:
            log(">> 새로 저장할 글이 없습니다. 종료합니다.")
            input(">> Enter로 종료...")
            ctx.close()
            return

        log("\n>> 위 '발견 개수'가 실제 게시판 글 수와 비슷한지 확인하세요.")
        log(">> 맞으면 Enter를 눌러 저장을 시작합니다. (그만하려면 이 창을 닫으세요)")
        input()

        done = 0
        for idx, aid in enumerate(todo[:MAX_ARTICLES_PER_RUN], 1):
            try:
                r = crawl_article(page, ctx, aid)
                done += 1
                log(f"[{idx}/{len(todo)}] {aid}  본문{r['body']}자 사진{r['imgs']} 댓글{r['cmts']}  {r['title'][:30]}")
            except Exception as e:
                log(f"[{idx}/{len(todo)}] {aid}  실패: {e}")
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            if idx % 40 == 0:
                log("   ...잠시 쉬는 중 (30초)")
                time.sleep(30)

        log("\n================= 완료 =================")
        log(f"저장 완료: {done}개")
        log(f"저장 위치: {os.path.join(OUT_ROOT, MENU_ID)}")
        log("=======================================")
        input(">> Enter로 종료...")
        ctx.close()


if __name__ == "__main__":
    main()
