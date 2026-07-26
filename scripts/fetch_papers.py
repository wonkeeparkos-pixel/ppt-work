#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
원문 PDF 내려받기 — 네트워크 제약이 없는 환경에서 실행할 것.

이 저장소를 만든 컨테이너는 PubMed/PMC/출판사 호스트가 차단되어 있어(프록시 403)
원문을 받을 수 없었다. 로컬 PC나 병원 네트워크에서 아래처럼 실행하면
문헌고찰_Lumbar_MBB_Facet/ 의 주제별 폴더에 공개접근(OA) 원문이 채워진다.

    python3 scripts/fetch_papers.py                    # 전체
    python3 scripts/fetch_papers.py 02_연관통_Referred_Pain   # 특정 폴더만

동작 — 합법 공개본을 4단계로 훑는다
  1) 문헌카드(*.md)에서 PMID / PMCID / DOI 를 읽는다
  2) Europe PMC — OA 이면 PDF 내려받기
  3) Unpaywall — 구독 저널이라도 저자 원고본(accepted manuscript)이나 기관
     리포지토리 공개본이 있으면 그 위치를 알려준다. 실제로 여기서 가장 많이 건진다.
  4) OpenAlex — Unpaywall이 놓친 best_oa_location 보강
  5) 그래도 없으면 초록만 저장하고, 소속 기관 프록시 링크를 함께 남긴다

설정 (환경변수)
    export UNPAYWALL_EMAIL="본인@메일.주소"      # 필수는 아니지만 넣는 편이 안정적
    export EZPROXY="https://openurl.본인병원.ac.kr/login?url="   # 있으면 기관 링크 생성

    python3 scripts/fetch_papers.py                    # 전체
    python3 scripts/fetch_papers.py 02_연관통_Referred_Pain   # 특정 폴더만

구독 원문을 우회해 받지는 않는다. 못 받은 항목은 _다운로드결과.md 에 기관 접근용
링크와 함께 남으므로, 병원 도서관·RISS·상호대차로 이어서 처리하면 된다.
"""
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "문헌고찰_Lumbar_MBB_Facet")
EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest"
UNPAYWALL = "https://api.unpaywall.org/v2"
OPENALEX = "https://api.openalex.org/works"
EMAIL = os.environ.get("UNPAYWALL_EMAIL", "").strip()
EZPROXY = os.environ.get("EZPROXY", "").strip()
UA = {"User-Agent": f"lumbar-mbb-litreview/1.1 (academic use; mailto:{EMAIL or 'user@example.com'})"}
PAUSE = 0.7   # API 예의상 간격


def get(url, binary=False, timeout=60):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read() if binary else r.read().decode("utf-8", "replace")


def epmc_lookup(pmid=None, pmcid=None, doi=None):
    if pmid:
        q = f"EXT_ID:{pmid} AND SRC:MED"
    elif pmcid:
        q = f"PMCID:{pmcid}"
    elif doi:
        q = f'DOI:"{doi}"'
    else:
        return None
    url = f"{EPMC}/search?query={urllib.parse.quote(q)}&format=json&resultType=core&pageSize=1"
    try:
        res = json.loads(get(url)).get("resultList", {}).get("result", [])
    except Exception as e:
        print("   조회 실패:", e)
        return None
    return res[0] if res else None


def unpaywall_pdf(doi):
    """구독 저널이라도 합법 공개본(저자 원고본·리포지토리)이 있으면 그 URL을 준다."""
    if not doi:
        return []
    email = EMAIL or "user@example.com"
    try:
        d = json.loads(get(f"{UNPAYWALL}/{urllib.parse.quote(doi)}?email={urllib.parse.quote(email)}"))
    except Exception:
        return []
    out = []
    for loc in ([d.get("best_oa_location")] + (d.get("oa_locations") or [])):
        if not loc:
            continue
        for k in ("url_for_pdf", "url"):
            if loc.get(k):
                out.append(loc[k])
    return out


def openalex_pdf(doi):
    """Unpaywall이 놓친 공개본 보강."""
    if not doi:
        return []
    try:
        d = json.loads(get(f"{OPENALEX}/doi:{urllib.parse.quote(doi)}"))
    except Exception:
        return []
    out = []
    for loc in ([d.get("best_oa_location")] + (d.get("locations") or [])):
        if isinstance(loc, dict) and loc.get("is_oa"):
            for k in ("pdf_url", "landing_page_url"):
                if loc.get(k):
                    out.append(loc[k])
    return out


def try_pdf(url, dest):
    try:
        blob = get(url, binary=True)
    except Exception:
        return False
    if blob[:4] == b"%PDF" and len(blob) > 20000:
        with open(dest, "wb") as fh:
            fh.write(blob)
        return True
    return False


def download_pdf(rec, dest, doi=None):
    """Europe PMC → Unpaywall → OpenAlex 순으로 합법 공개본을 찾는다."""
    pmcid = rec.get("pmcid") if rec else None
    doi = doi or (rec.get("doi") if rec else None)
    cands = []
    if rec and rec.get("isOpenAccess") == "Y" and pmcid:
        cands.append(f"{EPMC}/{pmcid}/fullTextPDF")
    if rec:
        for u in rec.get("fullTextUrlList", {}).get("fullTextUrl", []):
            if u.get("documentStyle") == "pdf" and u.get("availabilityCode") in ("OA", "F"):
                cands.append(u["url"])
    seen = set()
    for u in cands:
        if u in seen:
            continue
        seen.add(u)
        if try_pdf(u, dest):
            return u, "EuropePMC"
    for u in unpaywall_pdf(doi):
        if u in seen:
            continue
        seen.add(u)
        if try_pdf(u, dest):
            return u, "Unpaywall"
    for u in openalex_pdf(doi):
        if u in seen:
            continue
        seen.add(u)
        if try_pdf(u, dest):
            return u, "OpenAlex"
    return None, None


def institutional_link(doi, pmid):
    """소속 기관 프록시 링크 — EZPROXY 환경변수가 있을 때만."""
    if not EZPROXY:
        return ""
    target = (f"https://doi.org/{doi}" if doi
              else f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "")
    return (EZPROXY + urllib.parse.quote(target, safe="")) if target else ""


def ids_from_card(path):
    txt = open(path, encoding="utf-8").read()
    head = txt.split("\n")[0]
    pmid = re.search(r"pubmed\.ncbi\.nlm\.nih\.gov/(\d+)", txt)
    pmc = re.search(r"(PMC\d{5,9})", txt)
    doi = re.search(r"doi\.org/(10\.[^\s)]+)", txt)
    return (head.lstrip("# ").strip(),
            pmid.group(1) if pmid else None,
            pmc.group(1) if pmc else None,
            doi.group(1) if doi else None)


def run(only=None):
    folders = sorted(d for d in os.listdir(ARCHIVE)
                     if os.path.isdir(os.path.join(ARCHIVE, d)) and (only is None or d == only))
    log = ["# 원문 다운로드 결과", ""]
    if not EMAIL:
        log.append("> `UNPAYWALL_EMAIL` 미설정 — Unpaywall 조회가 제한될 수 있다.\n")
    if not EZPROXY:
        log.append("> `EZPROXY` 미설정 — 기관 접근 링크는 생성되지 않았다.\n")
    log += ["| 폴더 | 문헌 | 결과 | 경로 / 기관 링크 |", "|---|---|---|---|"]
    got = miss = 0
    for folder in folders:
        fdir = os.path.join(ARCHIVE, folder)
        for fn in sorted(os.listdir(fdir)):
            if not fn.endswith(".md") or fn.startswith("_") or fn.endswith("_abstract.md"):
                continue
            card = os.path.join(fdir, fn)
            title, pmid, pmc, doi = ids_from_card(card)
            pdf = os.path.join(fdir, fn[:-3] + ".pdf")
            if os.path.exists(pdf):
                continue
            print(f"[{folder}] {title[:70]}")
            rec = epmc_lookup(pmid=pmid, pmcid=pmc, doi=doi)
            time.sleep(PAUSE)
            doi = doi or (rec.get("doi") if rec else None)

            src, via = download_pdf(rec, pdf, doi=doi)
            if src:
                print(f"   PDF 저장 ({via}):", os.path.basename(pdf))
                log.append(f"| {folder} | {title[:80]} | PDF | {via} |")
                got += 1
                time.sleep(PAUSE)
                continue

            ab = rec.get("abstractText") if rec else None
            if ab:
                with open(os.path.join(fdir, fn[:-3] + "_abstract.md"), "w", encoding="utf-8") as fh:
                    fh.write(f"# {rec.get('title','')}\n\n"
                             f"{rec.get('authorString','')}. {rec.get('journalTitle','')} "
                             f"{rec.get('pubYear','')}.\n\n"
                             f"PMID {rec.get('pmid','-')} · {rec.get('doi','-')}\n\n"
                             f"## Abstract\n\n{ab}\n")
                status = "초록만 (구독 필요)"
            else:
                status = "색인 없음" if not rec else "실패"
            inst = institutional_link(doi, pmid)
            link = f"[기관 접근]({inst})" if inst else (f"[DOI](https://doi.org/{doi})" if doi else "—")
            log.append(f"| {folder} | {title[:80]} | {status} | {link} |")
            miss += 1
            time.sleep(PAUSE)

    log += ["", f"**PDF {got}건 · 미확보 {miss}건**", "",
            "미확보 문헌은 아래 순서로 이어서 처리한다.", "",
            "1. 소속 병원 도서관 전자저널 (위 기관 접근 링크)",
            "2. RISS 상호대차 / 원문복사 서비스 (`riss.kr`)",
            "3. 저자에게 직접 요청 — ResearchGate 또는 교신저자 이메일",
            "4. 대한통증학회·대한마취통증의학회 회원 접근 권한"]
    with open(os.path.join(ARCHIVE, "_다운로드결과.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log))
    print(f"\n완료 — PDF {got}건, 미확보 {miss}건 → _다운로드결과.md")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else None)
