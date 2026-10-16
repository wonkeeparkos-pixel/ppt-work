# -*- coding: utf-8 -*-
r"""
FBT 카페 수집기 v3
==================
하는 일
  - BOARDS 게시판의 글을 본문 + 사진 + 댓글까지 저장합니다.
      G:\내 드라이브\claude\FBT\data\게시판번호\글번호_제목\
          article.json  완결 데이터
          article.md    사람이 읽기 좋은 버전
          images\       본문 사진
  - 다시 돌리면 '아직 안 모은 글 + 새로 올라온 글'만 추가로 저장합니다.
  - 지난번에 내용이 빈 채로 저장된 글은 다시 받아봅니다.
  - 저장할 때 막 올라온 글이었다면, 그 뒤에 달린 댓글까지 받으려고 다시 저장합니다.
  - 전체공지(여러 게시판에 똑같이 걸린 글)는 빼고 모읍니다.

안전장치
  - 글마다 몇 초씩, 중간중간 길게 쉬면서 천천히 수집합니다.
  - 로그인이 풀렸거나 네이버 확인 화면(자동입력 방지 등)이 나오면 바로 멈춥니다.
  - 실행 중에는 컴퓨터가 절전으로 들어가지 않고, 검은 창을 클릭해도 멈추지 않습니다.

실행
  - 같은 폴더의 FBT_수집실행.bat 더블클릭
  - 자동 실행(작업 스케줄러)용: FBT_수집실행.bat --auto
"""
import os
import re
import sys
import json
import time
import random
import shutil
import datetime
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ============================ 설정 ============================
CAFE_ID = "31251118"                     # functionalbt 카페 고유번호
BOARDS = ["16", "17", "24", "25", "26", "28",
          "29", "30", "31", "32", "33", "34", "38"]   # 모을 게시판 (추가/삭제는 여기서)

FBT_DIR     = r"G:\내 드라이브\claude\FBT"         # 구글드라이브 FBT 폴더
OUT_ROOT    = os.path.join(FBT_DIR, "data")          # 수집 결과
TOOL_DIR    = os.path.join(FBT_DIR, "수집기")        # 이 프로그램 + 실행 기록
RECORD_FILE = os.path.join(TOOL_DIR, "수집기록.txt")  # 실행할 때마다 한 줄 요약
LOG_DIR_G   = os.path.join(TOOL_DIR, "로그")         # 실행별 상세 기록 (끝나면 복사)

LOCAL_DIR   = r"C:\FBT"                              # 로그인 정보 등은 C드라이브에만
PROFILE_DIR = os.path.join(LOCAL_DIR, ".browser")
INDEX_FILE  = os.path.join(LOCAL_DIR, "fbt_index.json")   # 저장 현황 색인 (속도용)
LOG_DIR     = os.path.join(LOCAL_DIR, "logs")

# 이미 확인된 전체공지 글번호 (여러 게시판에 걸린 글은 자동으로도 걸러짐)
NOTICE_IDS_SEED = {"16", "447", "904", "1493", "1770", "2307", "2681",
                   "2889", "2982", "3174", "3354", "3678", "3707", "3736"}

REFRESH_FRESH_DAYS  = 30    # 저장할 때 올라온 지 30일이 안 됐던 글은
REFRESH_AFTER_DAYS  = 7     # 저장하고 7일 넘게 지났으면 댓글 갱신을 위해 다시 저장
MAX_RETRY           = 2     # 내용이 비어서 실패한 글은 이 횟수까지만 다시 시도
MAX_PER_RUN         = 1000  # 한 번 실행에 저장할 최대 글 수 (나머지는 다음에 이어서)
MAX_PER_RUN_AUTO    = 400   # 자동 실행 때 최대 글 수
MIN_DELAY, MAX_DELAY = 4.0, 9.0   # 글 사이 쉬는 시간(초)
MAX_PAGES           = 300   # 게시판 목록 최대 페이지
EMPTY_STREAK_STOP   = 6     # 읽기 실패가 연속으로 이만큼 나오면 멈춤
UNAVAIL_STREAK_STOP = 15    # 볼 수 없는 글이 연속으로 이만큼 나오면 멈춤
# ==============================================================

AUTO = "--auto" in sys.argv
NOW = datetime.datetime.now()

BLOCK_WORDS = ["자동입력 방지", "자동 입력 방지", "보안문자", "보안 문자", "captcha", "CAPTCHA",
               "비정상적인 접근", "비정상적인 요청", "일시적으로 제한", "요청이 너무 많"]
UNAVAILABLE_WORDS = ["삭제되었거나", "존재하지 않는 게시글", "존재하지 않는 글", "삭제된 게시글",
                     "권한이 없", "등급이 되", "등급 이상", "멤버만 볼 수", "카페 멤버만", "멤버에게만"]

TITLE_SELS  = [".ArticleTitle .title_text", ".title_text", "h3.title_text",
               ".article_header h3", ".tit-box .tit"]
WRITER_SELS = [".WriterInfo .nickname", ".nick_box .nickname",
               ".profile_area .nickname", ".nickname"]
DATE_SELS   = [".WriterInfo .date", ".article_info .date", ".date"]
BODY_SELS   = [".se-main-container", ".article_viewer", ".ContentRenderer",
               ".content_box", ".NHN_Writeform_Main", ".se_component_wrap"]
COMMENT_ITEM_SELS = [".CommentItem", "li.comment_item", ".comment_list li",
                     ".u_cbox_comment", ".comment_area li"]
COMMENT_NICK_SELS = [".comment_nickname", ".nickname", ".u_cbox_nick"]
COMMENT_TEXT_SELS = [".text_comment", ".comment_text_view", ".comment_content", ".u_cbox_contents"]
COMMENT_DATE_SELS = [".comment_info_date", ".comment_created_at", "time", ".date",
                     '[class*="date"]', '[class*="Date"]']
PAGER_SELS = ['[class*="aginat"] a', '[class*="aginat"] button',
              '[class*="paging"] a', '[class*="paging"] button']

_log_fp = None


class Blocked(Exception):
    """네이버가 자동접속을 의심하는 화면"""


# ------------------------------------------------------------ 공통
def log(msg=""):
    print(msg, flush=True)
    if _log_fp:
        try:
            _log_fp.write(msg + "\n")
            _log_fp.flush()
        except Exception:
            pass


def win_console_tweaks():
    """검은 창을 클릭해도 멈추지 않게(빠른 편집 끄기) + 실행 중 절전 방지"""
    if os.name != "nt":
        return
    try:
        import ctypes
        k32 = ctypes.windll.kernel32
        handle = k32.GetStdHandle(-10)
        mode = ctypes.c_uint32()
        if k32.GetConsoleMode(handle, ctypes.byref(mode)):
            k32.SetConsoleMode(handle, (mode.value & ~0x0040) | 0x0080)
        k32.SetThreadExecutionState(0x80000000 | 0x00000001)
    except Exception:
        pass


def clean(t):
    return re.sub(r"\n{3,}", "\n\n", (t or "").strip())


def safe_name(title, fallback):
    s = re.sub(r'[\\/:*?"<>|\n\r\t]', "_", title or "")[:50].rstrip(" .")
    return s or fallback


DATE_RE = re.compile(r"(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.?(?:\s*(\d{1,2}):(\d{2}))?")


def parse_post_date(s):
    m = DATE_RE.search(s or "")
    if not m:
        return None
    try:
        return datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)),
                                 int(m.group(4) or 0), int(m.group(5) or 0))
    except ValueError:
        return None


def parse_iso(s):
    try:
        return datetime.datetime.fromisoformat(s)
    except Exception:
        return None


def read_json(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ------------------------------------------------ 저장 현황(색인)
ID_DIR_RE = re.compile(r"^(\d+)_")


def scan_saved_folders():
    """data/게시판/글번호_제목 폴더를 한 번에 훑어서 {글번호: 폴더경로}"""
    cands = {}
    if not os.path.isdir(OUT_ROOT):
        return {}
    for board in os.scandir(OUT_ROOT):
        if not board.is_dir():
            continue
        for e in os.scandir(board.path):
            m = ID_DIR_RE.match(e.name)
            if m and e.is_dir():
                cands.setdefault(m.group(1), []).append(e.path)
    found = {}
    for aid, paths in cands.items():
        named = [p for p in paths if os.path.basename(p) != f"{aid}_{aid}"]
        found[aid] = sorted(named or paths)[0]
    return found


def is_empty_article(data):
    return not (data.get("title") or data.get("body_text") or data.get("images"))


def entry_from_folder(folder):
    jpath = os.path.join(folder, "article.json")
    data = read_json(jpath)
    if not isinstance(data, dict):
        return {"folder": folder, "broken": True, "fail_count": 0}
    crawled = data.get("crawled_at") or ""
    if not crawled:
        try:
            crawled = datetime.datetime.fromtimestamp(
                os.path.getmtime(jpath)).isoformat(timespec="seconds")
        except Exception:
            crawled = ""
    return {"folder": folder,
            "date": data.get("date") or "",
            "crawled_at": crawled,
            "empty": is_empty_article(data),
            "fail_count": int(data.get("fail_count") or 0),
            "comments": len(data.get("comments") or [])}


def load_index():
    data = read_json(INDEX_FILE)
    return data if isinstance(data, dict) else {}


def save_index(index):
    try:
        tmp = INDEX_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(index, f, ensure_ascii=False)
        os.replace(tmp, INDEX_FILE)
    except Exception as e:
        log(f"   (색인 저장 실패: {e})")


def sync_index(index, folders):
    """드라이브에 실제로 있는 폴더와 색인을 맞춘다. 처음 한 번은 기존 글을 읽느라 오래 걸릴 수 있음."""
    todo = [aid for aid, path in folders.items()
            if (index.get(aid) or {}).get("folder") != path]
    if todo:
        log(f">> 저장돼 있는 글 {len(todo)}개 상태 확인 중... (처음 한 번만 오래 걸려요)")
    for n, aid in enumerate(todo, 1):
        index[aid] = entry_from_folder(folders[aid])
        if n % 200 == 0:
            log(f"   {n}/{len(todo)}")
            save_index(index)
    for aid in list(index):
        if (index[aid] or {}).get("folder") and aid not in folders:
            del index[aid]          # 드라이브에서 지운 글은 색인에서도 뺌
    save_index(index)
    return index


def decide(entry, now=None):
    """이번에 받을 글인지: 'new' / 'retry' / 'refresh' / None(건너뜀)"""
    now = now or NOW
    if not entry:
        return "new"
    if not entry.get("folder") or entry.get("broken") or entry.get("empty"):
        return "retry" if int(entry.get("fail_count") or 0) < MAX_RETRY else None
    post_dt = parse_post_date(entry.get("date"))
    saved_dt = parse_iso(entry.get("crawled_at"))
    if post_dt and saved_dt:
        if ((saved_dt - post_dt).days < REFRESH_FRESH_DAYS
                and (now - saved_dt).days >= REFRESH_AFTER_DAYS):
            return "refresh"
    return None


def build_plan(board_ids, index, now=None):
    """게시판별 글 목록 → 받을 목록. 여러 게시판에 걸린 글(전체공지)은 제외."""
    cnt = {}
    for ids in board_ids.values():
        for i in set(ids):
            cnt[i] = cnt.get(i, 0) + 1
    notices = {i for i, c in cnt.items() if c >= 2} | NOTICE_IDS_SEED
    plan, seen = [], set()
    for mid in BOARDS:
        for aid in board_ids.get(mid, []):
            if aid in notices or aid in seen:
                continue
            seen.add(aid)
            why = decide(index.get(aid), now)
            if why:
                plan.append((why, mid, aid))
    rank = {"new": 0, "retry": 1, "refresh": 2}
    plan.sort(key=lambda x: (rank[x[0]], -int(x[2])))
    return plan, len([i for i in notices if i in cnt])


def mark_failed(entry, aid, status):
    """읽기 실패 기록. 기존에 잘 저장된 내용은 건드리지 않음."""
    e = dict(entry or {})
    e["fail_count"] = int(e.get("fail_count") or 0) + 1
    e["empty"] = True
    e["status"] = status
    e.setdefault("folder", None)
    folder = e.get("folder")
    if folder and os.path.isdir(folder):
        jpath = os.path.join(folder, "article.json")
        data = read_json(jpath)
        if not isinstance(data, dict):
            data = {"article_id": aid}
        if is_empty_article(data):
            data["fail_count"] = e["fail_count"]
            data["status"] = status
            try:
                write_json(jpath, data)
            except Exception:
                pass
    return e


def render_md(d):
    lines = [f"# {d.get('title', '')}", "",
             f"- 게시판: {d.get('menu_id', '')}",
             f"- 작성자: {d.get('writer', '')}",
             f"- 날짜: {d.get('date', '')}",
             f"- 원문: {d.get('url', '')}",
             "", "---", "", d.get("body_text", ""), ""]
    imgs = d.get("images") or []
    if imgs:
        lines.append("## 첨부 이미지")
        lines += [f"![{fn}](images/{fn})" for fn in imgs]
        lines.append("")
    cmts = d.get("comments") or []
    if cmts:
        lines.append(f"## 댓글 ({len(cmts)}개)")
        for c in cmts:
            when = f" ({c['date']})" if c.get("date") else ""
            head = "  - ↳ " if c.get("reply") else "- "
            text = (c.get("text") or "").replace("\n", "\n    ")
            lines.append(f"{head}**{c.get('nick', '')}**{when}: {text}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------- 브라우저
def logged_in(ctx):
    try:
        return any(c.get("name") == "NID_AUT" for c in ctx.cookies(["https://cafe.naver.com/"]))
    except Exception:
        return False


def ensure_login(page, ctx):
    if logged_in(ctx):
        return True
    if AUTO:
        return False
    log("")
    log(">> 네이버 로그인이 필요해요. 열린 크롬 창에서 로그인해주세요.")
    log("   ('로그인 상태 유지'를 체크하면 다음부터는 안 물어봐요. 로그인되면 자동으로 시작합니다.)")
    try:
        page.goto("https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fcafe.naver.com%2Ffunctionalbt",
                  wait_until="domcontentloaded")
    except Exception:
        pass
    for _ in range(300):            # 최대 15분 기다림
        time.sleep(3)
        if logged_in(ctx):
            log(">> 로그인 확인!")
            return True
    return False


def body_text_of(page):
    try:
        return page.inner_text("body")[:5000]
    except Exception:
        return ""


def page_article_ids(page, url):
    """목록 한 쪽을 열어 글 번호들을 돌려준다. 끝내 안 열리면 None."""
    for attempt in range(2):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            break
        except Exception:
            if attempt:
                return None
            page.wait_for_timeout(5000)
    page.wait_for_timeout(2200)
    ids = []
    for a in page.query_selector_all('a[href*="/articles/"]'):
        m = re.search(r"/articles/(\d+)", a.get_attribute("href") or "")
        if m:
            ids.append(m.group(1))
    return list(dict.fromkeys(ids))


def list_board(page, menu_id, index=None, early_stop=False):
    """게시판 목록을 쪽마다 넘기며 글 번호를 모은다."""
    root = f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/menus/{menu_id}"
    base = root + "?viewType=L&page="
    ids, seen, prev, idle = [], set(), None, 0
    for pg in range(1, MAX_PAGES + 1):
        page_ids = page_article_ids(page, base + str(pg))
        if page_ids is None:
            log(f"   (게시판 {menu_id} {pg}쪽이 안 열려서 여기까지만 확인)")
            break
        if not page_ids and pg == 1:
            text = body_text_of(page)
            if any(w in text for w in BLOCK_WORDS):
                raise Blocked(text[:120].replace("\n", " "))
            base = root + "?page="      # 목록형 주소로 안 나오면 기본 주소로 다시
            page_ids = page_article_ids(page, base + "1") or []
        if not page_ids or page_ids == prev:
            break
        fresh = [i for i in page_ids if i not in seen]
        for i in fresh:
            seen.add(i)
            ids.append(i)
        prev = page_ids
        if pg % 10 == 0:
            log(f"      (게시판 {menu_id}: {pg}쪽까지 {len(ids)}개 확인)")
        if early_stop and index is not None and pg > 1:
            if any(decide(index.get(i)) for i in fresh):
                idle = 0
            else:
                idle += 1
                if idle >= 3:       # 받을 게 없는 쪽이 3번 이어지면 그 게시판은 끝
                    break
        page.wait_for_timeout(int(random.uniform(1.0, 2.2) * 1000))
    return ids


def text_of(scope, sels):
    for s in sels:
        try:
            el = scope.query_selector(s)
            if el:
                t = el.inner_text().strip()
                if t:
                    return t
        except Exception:
            pass
    return ""


def extract_comments(frame):
    items = []
    for s in COMMENT_ITEM_SELS:
        try:
            items = frame.query_selector_all(s)
        except Exception:
            items = []
        if items:
            break
    out = []
    for c in items:
        text = text_of(c, COMMENT_TEXT_SELS)
        if not text:
            continue
        try:
            cls = (c.get_attribute("class") or "").lower()
        except Exception:
            cls = ""
        out.append({"nick": text_of(c, COMMENT_NICK_SELS),
                    "date": text_of(c, COMMENT_DATE_SELS),
                    "text": text,
                    "reply": "reply" in cls})
    return out


def more_comment_pages(page, frame, article_id, comments):
    """댓글이 여러 쪽으로 나뉜 글이면 다음 쪽들도 읽는다 (댓글창 안의 쪽 번호만 누름)."""
    try:
        box = (frame.query_selector('[class*="CommentBox"]')
               or frame.query_selector('[class*="comment_box"]'))
    except Exception:
        box = None
    if not box:
        return comments
    keys = {(c["nick"], c["text"], c["date"]) for c in comments}
    clicked = {"1"}
    for _ in range(30):
        target = None
        for sel in PAGER_SELS:
            try:
                for b in box.query_selector_all(sel):
                    t = (b.inner_text() or "").strip()
                    if t.isdigit() and t not in clicked:
                        target = (t, b)
                        break
            except Exception:
                pass
            if target:
                break
        if not target:
            break
        clicked.add(target[0])
        try:
            target[1].click()
            page.wait_for_timeout(1800)
        except Exception:
            break
        if f"/articles/{article_id}" not in page.url:
            break
        for c in extract_comments(frame):
            k = (c["nick"], c["text"], c["date"])
            if k not in keys:
                keys.add(k)
                comments.append(c)
    return comments


def crawl_article(page, ctx, menu_id, aid, existing_folder=None):
    url = (f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}/articles/{aid}"
           f"?menuid={menu_id}&referrerAllArticles=false")
    page.goto(url, wait_until="domcontentloaded")
    try:
        page.wait_for_load_state("networkidle", timeout=12000)
    except Exception:
        pass
    page.wait_for_timeout(2500)
    for _ in range(8):              # 사진·댓글이 스크롤해야 나오는 경우가 있어 끝까지 내림
        try:
            page.mouse.wheel(0, 4000)
        except Exception:
            pass
        page.wait_for_timeout(400)
    page.wait_for_timeout(1000)

    frame = page
    try:
        if page.query_selector("iframe#cafe_main"):
            frame = page.frame(name="cafe_main") or page
    except Exception:
        pass

    title = text_of(frame, TITLE_SELS)
    writer = text_of(frame, WRITER_SELS)
    date = text_of(frame, DATE_SELS)
    body_el = None
    for s in BODY_SELS:
        try:
            body_el = frame.query_selector(s)
        except Exception:
            body_el = None
        if body_el:
            break
    try:
        body_text = clean(body_el.inner_text()) if body_el else ""
    except Exception:
        body_text = ""

    img_urls = []
    if body_el:
        try:
            for img in body_el.query_selector_all("img"):
                src = img.get_attribute("src") or img.get_attribute("data-src") or ""
                if src.startswith("http") and "static.nid" not in src and "cafe_meta" not in src:
                    img_urls.append(src)
        except Exception:
            pass
    img_urls = list(dict.fromkeys(img_urls))

    if not (title or body_text or img_urls):
        text = body_text_of(frame)
        if any(w in text for w in BLOCK_WORDS):
            raise Blocked(text[:120].replace("\n", " "))
        return {"status": "unavailable" if any(w in text for w in UNAVAILABLE_WORDS) else "empty"}

    comments = extract_comments(frame)
    if len(comments) >= 50:
        comments = more_comment_pages(page, frame, aid, comments)

    # 저장 폴더: 이미 있는 글이면 그 폴더를 그대로 씀 (제목 못 읽었던 폴더는 제목으로 바꿈)
    sname = safe_name(title, aid)
    folder = existing_folder if existing_folder and os.path.isdir(existing_folder) else None
    if folder and os.path.basename(folder) == f"{aid}_{aid}" and sname != aid:
        target = os.path.join(os.path.dirname(folder), f"{aid}_{sname}")
        if not os.path.exists(target):
            try:
                os.rename(folder, target)
                folder = target
            except Exception:
                pass
    if not folder:
        folder = os.path.join(OUT_ROOT, menu_id, f"{aid}_{sname}")
    img_dir = os.path.join(folder, "images")
    os.makedirs(img_dir, exist_ok=True)

    saved_imgs = []
    for i, u in enumerate(img_urls, 1):
        m = re.search(r"\.(jpg|jpeg|png|gif|webp)", u.lower())
        fn = f"img_{i:02d}" + ("." + m.group(1) if m else ".jpg")
        fp = os.path.join(img_dir, fn)
        try:
            if os.path.exists(fp) and os.path.getsize(fp) > 0:
                saved_imgs.append(fn)      # 이미 받은 사진은 다시 받지 않음
                continue
            r = ctx.request.get(u, headers={"Referer": "https://cafe.naver.com/"})
            if r.ok:
                with open(fp, "wb") as f:
                    f.write(r.body())
                saved_imgs.append(fn)
        except Exception:
            pass

    crawled_at = datetime.datetime.now().isoformat(timespec="seconds")
    data = {"cafe_id": CAFE_ID, "menu_id": menu_id, "article_id": aid, "url": url,
            "title": title, "writer": writer, "date": date, "body_text": body_text,
            "images": saved_imgs, "comments": comments, "crawled_at": crawled_at}
    write_json(os.path.join(folder, "article.json"), data)
    with open(os.path.join(folder, "article.md"), "w", encoding="utf-8") as f:
        f.write(render_md(data))
    return {"status": "ok", "folder": folder, "title": title, "date": date,
            "crawled_at": crawled_at, "body": len(body_text),
            "imgs": len(saved_imgs), "cmts": len(comments)}


# ------------------------------------------------------- 실행 흐름
def crawl_all(ctx, index, stats):
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto(f"https://cafe.naver.com/f-e/cafes/{CAFE_ID}", wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    if not ensure_login(page, ctx):
        log("!! 네이버 로그인이 안 되어 있어 멈춥니다. FBT_수집실행.bat 을 직접 실행해서 로그인해주세요.")
        return "로그인 필요"
    log(">> 네이버 로그인 확인됨")

    log("\n>> [1단계] 게시판별 글 목록 확인 중... (10~20분 걸려요)")
    board_ids = {}
    try:
        for mid in BOARDS:
            board_ids[mid] = list_board(page, mid, index, early_stop=AUTO)
            log(f"   게시판 {mid}: {len(board_ids[mid])}개")
            page.wait_for_timeout(int(random.uniform(3, 7) * 1000))
    except Blocked as b:
        log(f"!! 네이버 확인 화면이 나와서 멈춥니다: {b}")
        log("   하루쯤 쉬었다가 다시 실행해주세요. 저장된 건 그대로예요.")
        return "네이버 확인 화면(자동접속 의심)"

    plan, n_notice = build_plan(board_ids, index)
    counts = {k: sum(1 for x in plan if x[0] == k) for k in ("new", "retry", "refresh")}
    log("")
    log(f">> 새로 저장할 글 : {counts['new']}개  (아직 안 모은 글 + 새로 올라온 글)")
    log(f">> 다시 받을 글   : {counts['retry']}개  (지난번에 내용이 비어 저장된 글)")
    log(f">> 댓글 갱신할 글 : {counts['refresh']}개  (저장할 때 막 올라왔던 글 → 그 뒤 댓글까지)")
    log(f">> 전체공지 제외  : {n_notice}개")
    limit = MAX_PER_RUN_AUTO if AUTO else MAX_PER_RUN
    if len(plan) > limit:
        log(f">> 이번에는 {limit}개까지만 하고, 나머지는 다음 실행 때 이어서 합니다.")
        plan = plan[:limit]
    if not plan:
        log(">> 받을 글이 없어요. 모두 최신 상태입니다!")
        return ""
    log(f">> 예상 시간: 약 {max(1, len(plan) * 22 // 60)}분")
    if not AUTO:
        log("")
        log(">> 시작하려면 이 검은 창을 클릭하고 Enter  (그만두려면 창을 닫으세요)")
        input()

    log("\n>> [2단계] 저장 시작")
    tag = {"new": "새 글", "retry": "재시도", "refresh": "댓글갱신"}
    empty_streak = unavail_streak = 0
    for idx, (why, mid, aid) in enumerate(plan, 1):
        entry = index.get(aid) or {}
        head = f"[{idx}/{len(plan)}] {tag[why]} (게시판{mid}) {aid}"
        try:
            r = crawl_article(page, ctx, mid, aid, entry.get("folder"))
        except Blocked as b:
            log(f"{head}  !! 네이버 확인 화면이 나와서 멈춥니다: {b}")
            log("   하루쯤 쉬었다가 다시 실행해주세요. 저장된 건 그대로예요.")
            return "네이버 확인 화면(자동접속 의심)"
        except Exception as e:
            msg = str(e)
            if "closed" in msg.lower():
                log(f"{head}  !! 크롬 창이 닫혀서 멈춥니다.")
                return "크롬 창 닫힘"
            stats["fail"] += 1
            empty_streak += 1
            log(f"{head}  실패: {msg[:150]}")
            r = None

        if r and r["status"] == "ok":
            empty_streak = unavail_streak = 0
            stats[why] += 1
            index[aid] = {"folder": r["folder"], "date": r["date"], "crawled_at": r["crawled_at"],
                          "empty": False, "fail_count": 0, "comments": r["cmts"]}
            log(f"{head}  본문{r['body']}자 사진{r['imgs']} 댓글{r['cmts']}  {r['title'][:26]}")
        elif r:
            if not logged_in(ctx):
                log(f"{head}  !! 로그인이 풀렸어요. 멈춥니다.")
                return "로그인 풀림"
            unavailable = r["status"] == "unavailable"
            if unavailable:
                unavail_streak += 1
            else:
                empty_streak += 1
            if why == "refresh":
                stats["kept"] += 1      # 기존에 잘 저장된 내용은 그대로 둠
                log(f"{head}  (이번엔 못 읽음 — 기존 저장본 유지)")
            else:
                index[aid] = mark_failed(entry, aid, r["status"])
                if unavailable:
                    stats["unavailable"] += 1
                    log(f"{head}  볼 수 없는 글 (삭제됐거나 볼 권한 없음)")
                else:
                    stats["fail"] += 1
                    log(f"{head}  내용이 비어 있음 (다음 실행 때 다시 시도)")

        if empty_streak >= EMPTY_STREAK_STOP:
            return f"읽기 실패 {empty_streak}번 연속 (로그인/접속 상태 확인 필요)"
        if unavail_streak >= UNAVAIL_STREAK_STOP:
            return f"볼 수 없는 글 {unavail_streak}개 연속 (등급/로그인 확인 필요)"
        if idx % 10 == 0:
            save_index(index)
        if idx < len(plan):
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))
            if idx % 150 == 0:
                rest = random.randint(120, 240)
                log(f"   ...좀 길게 쉬는 중 ({rest}초)")
                time.sleep(rest)
            elif idx % 40 == 0:
                log("   ...잠깐 쉬는 중 (30초)")
                time.sleep(30)
    return ""


def run(stats):
    if not os.path.isdir(FBT_DIR):
        log("!! 구글 드라이브 폴더를 찾을 수 없어요: " + FBT_DIR)
        log("   'Google Drive' 프로그램이 켜져 있는지(G: 드라이브가 보이는지) 확인해주세요.")
        return "구글 드라이브(G:) 없음"
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        log("!! 크롤링 도구(playwright)가 이 파이썬에 없어요: " + sys.executable)
        log("   이 창에 아래 두 줄을 차례로 붙여넣고 Enter 한 뒤 다시 실행해주세요.")
        log(f'   "{sys.executable}" -m pip install playwright')
        log(f'   "{sys.executable}" -m playwright install chromium')
        return "playwright 없음"
    os.makedirs(OUT_ROOT, exist_ok=True)

    folders = scan_saved_folders()
    log(f">> 지금까지 저장된 글: {len(folders)}개")
    index = sync_index(load_index(), folders)

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            PROFILE_DIR, headless=False,
            viewport={"width": 1280, "height": 900},
            args=["--disable-blink-features=AutomationControlled"])
        try:
            return crawl_all(ctx, index, stats)
        finally:
            save_index(index)
            try:
                ctx.close()
            except Exception:
                pass


def write_record(line):
    try:
        os.makedirs(TOOL_DIR, exist_ok=True)
        with open(RECORD_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception as e:
        log(f"   (수집기록 저장 실패: {e})")


def main():
    global _log_fp
    win_console_tweaks()
    for d in (LOCAL_DIR, PROFILE_DIR, LOG_DIR):
        os.makedirs(d, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"수집_{NOW:%Y%m%d_%H%M}.txt")
    _log_fp = open(log_path, "a", encoding="utf-8")
    log(f"FBT 카페 수집기 v3  |  {NOW:%Y-%m-%d %H:%M}  |  {'자동' if AUTO else '수동'} 실행")

    stats = {"new": 0, "retry": 0, "refresh": 0, "fail": 0, "unavailable": 0, "kept": 0}
    t0 = time.time()
    try:
        stop = run(stats)
    except KeyboardInterrupt:
        stop = "사용자가 멈춤"
        log("\n>> 멈췄습니다. (지금까지 저장한 건 그대로 남아 있어요)")
    except Exception as e:
        stop = f"오류: {str(e)[:100]}"
        log("\n!! 오류가 났어요:")
        log(traceback.format_exc())

    mins = int((time.time() - t0) / 60)
    log("")
    log("================ 결과 ================")
    log(f"  새로 저장  : {stats['new']}개")
    log(f"  다시 받음  : {stats['retry']}개")
    log(f"  댓글 갱신  : {stats['refresh']}개")
    if stats["fail"] or stats["unavailable"]:
        log(f"  실패 / 볼 수 없음 : {stats['fail']} / {stats['unavailable']}개")
    if stop:
        log(f"  멈춘 이유  : {stop}")
    log(f"  걸린 시간  : {mins}분")
    log(f"  저장 위치  : {OUT_ROOT}")
    log("=====================================")

    record = (f"{NOW:%Y-%m-%d %H:%M} | {'자동' if AUTO else '수동'} | 새 글 {stats['new']} | "
              f"재시도 {stats['retry']} | 댓글갱신 {stats['refresh']} | 실패 {stats['fail']} | "
              f"볼 수 없음 {stats['unavailable']} | {mins}분")
    if stop:
        record += f" | 멈춤: {stop}"
    if os.path.isdir(FBT_DIR):
        write_record(record)
    _log_fp.close()
    _log_fp = None
    try:
        os.makedirs(LOG_DIR_G, exist_ok=True)
        shutil.copy2(log_path, os.path.join(LOG_DIR_G, os.path.basename(log_path)))
    except Exception:
        pass


if __name__ == "__main__":
    main()
