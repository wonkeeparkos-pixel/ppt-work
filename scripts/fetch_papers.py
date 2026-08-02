# -*- coding: utf-8 -*-
"""각 논문 PDF를 질환·부위별 폴더에 내려받는다. **각자 컴퓨터에서 실행할 것.**

이 저장소를 만든 원격 환경은 PubMed·PMC·출판사 도메인이 차단돼 있어 여기서는 실패한다.
로컬(또는 병원 네트워크)에서 돌리면 오픈액세스 논문이 자동으로 채워지고,
받지 못한 것은 `논문/_못받은목록.md`에 링크와 함께 남는다.

    python3 scripts/fetch_papers.py            # 전부
    python3 scripts/fetch_papers.py 06_허리    # 폴더 하나만
"""
import os
import sys
import time
import urllib.request
import urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from papers import PAPERS, link  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "문헌고찰_보툴리눔_정형외과통증", "논문")
UA = "Mozilla/5.0 (compatible; ppt-work paper fetcher; academic use)"
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/pdf,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read(), r.headers.get("Content-Type", "")


def candidates(p):
    """오픈액세스 PDF 후보 URL을 시도 순서대로."""
    out = []
    if p.get("pmcid"):
        pmc = p["pmcid"]
        out.append(f"{EPMC}/PMC/{pmc}/fullTextPDF")
        out.append(f"https://pmc.ncbi.nlm.nih.gov/articles/{pmc}/pdf/")
    if p.get("pmid"):
        out.append(f"{EPMC}/MED/{p['pmid']}/fullTextPDF")
    if p.get("url", "").lower().endswith(".pdf"):
        out.append(p["url"])
    return out


def fetch_one(p, only=None):
    if only and p["folder"] != only:
        return None
    dest_dir = os.path.join(ROOT, p["folder"], "PDF")
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, f"{p['key']}.pdf")
    if os.path.exists(dest) and os.path.getsize(dest) > 20_000:
        print(f"  = {p['key']} (이미 있음)")
        return True
    for url in candidates(p):
        try:
            data, ctype = get(url)
        except Exception as e:                       # noqa: BLE001
            print(f"    · 실패 {type(e).__name__} {url[:70]}")
            continue
        if data[:4] != b"%PDF":
            print(f"    · PDF 아님({ctype[:24]}) {url[:70]}")
            continue
        with open(dest, "wb") as f:
            f.write(data)
        print(f"  + {p['key']}  {len(data)/1e6:.1f} MB")
        return True
    print(f"  ! {p['key']} — 오픈액세스 아님")
    return False


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    todo = [p for p in PAPERS if not only or p["folder"] == only]
    print(f"대상 {len(todo)}편" + (f" (폴더 {only})" if only else ""))
    missing = []
    for p in todo:
        print(f"[{p['folder']}] {p['key']}")
        if not fetch_one(p, only):
            missing.append(p)
        time.sleep(0.6)                              # 서버 예의

    os.makedirs(ROOT, exist_ok=True)
    path = os.path.join(ROOT, "_못받은목록.md")
    if missing:
        lines = ["# 자동으로 받지 못한 논문\n",
                 "오픈액세스가 아니라서 자동 수집이 안 된다. 아래 링크를 열어",
                 "도서관 프록시·기관 구독으로 받은 뒤 각 폴더의 `PDF/`에 `<key>.pdf`로 저장한다.\n",
                 "| 폴더 | 파일명 | 논문 | 링크 |", "|---|---|---|---|"]
        for p in missing:
            lines.append(f"| `{p['folder']}` | `{p['key']}.pdf` | {p['authors']} ({p['year']}) "
                         f"— {p['title'][:70]} | {link(p)} |")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print(f"\n받지 못한 {len(missing)}편 → {path}")
    else:
        if os.path.exists(path):
            os.remove(path)
        print("\n전부 받았다.")


if __name__ == "__main__":
    main()
