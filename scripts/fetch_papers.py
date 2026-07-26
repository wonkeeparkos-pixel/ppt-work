#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
원문 PDF 내려받기 — 네트워크 제약이 없는 환경에서 실행할 것.

이 저장소를 만든 컨테이너는 PubMed/PMC/출판사 호스트가 차단되어 있어(프록시 403)
원문을 받을 수 없었다. 로컬 PC나 병원 네트워크에서 아래처럼 실행하면
문헌고찰_Lumbar_MBB_Facet/ 의 주제별 폴더에 공개접근(OA) 원문이 채워진다.

    python3 scripts/fetch_papers.py                    # 전체
    python3 scripts/fetch_papers.py 02_연관통_Referred_Pain   # 특정 폴더만

동작
  1) 문헌카드(*.md)에서 PMID / PMCID / DOI 를 읽는다
  2) Europe PMC 로 OA 여부를 조회하고, OA면 PDF 를 내려받는다
  3) OA 가 아니면 초록만 <파일명>_abstract.md 로 저장하고 링크를 남긴다
  4) 결과를 _다운로드결과.md 에 기록한다

구독 저널 원문은 내려받지 않는다. 소속 기관 권한으로 직접 접근할 것.
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
UA = {"User-Agent": "lumbar-mbb-litreview/1.0 (academic use; mailto:user@example.com)"}
PAUSE = 0.7   # Europe PMC 예의상 간격


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


def download_pdf(rec, dest):
    """OA PDF 후보 URL을 순서대로 시도."""
    pmcid = rec.get("pmcid")
    cands = []
    if rec.get("isOpenAccess") == "Y" and pmcid:
        cands.append(f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextPDF")
        cands.append(f"https://europepmc.org/api/fulltextRepo?pprId={pmcid}&type=FILE&fileName=EMS.pdf")
    for u in rec.get("fullTextUrlList", {}).get("fullTextUrl", []):
        if u.get("documentStyle") == "pdf" and u.get("availabilityCode") in ("OA", "F"):
            cands.append(u["url"])
    for u in cands:
        try:
            blob = get(u, binary=True)
            if blob[:4] == b"%PDF" and len(blob) > 20000:
                with open(dest, "wb") as fh:
                    fh.write(blob)
                return u
        except Exception:
            continue
    return None


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
    log = ["# 원문 다운로드 결과", "", "| 폴더 | 문헌 | 결과 |", "|---|---|---|"]
    got = miss = 0
    for folder in folders:
        fdir = os.path.join(ARCHIVE, folder)
        for fn in sorted(os.listdir(fdir)):
            if not fn.endswith(".md") or fn.startswith("_"):
                continue
            card = os.path.join(fdir, fn)
            title, pmid, pmc, doi = ids_from_card(card)
            pdf = os.path.join(fdir, fn[:-3] + ".pdf")
            if os.path.exists(pdf):
                continue
            print(f"[{folder}] {title[:70]}")
            rec = epmc_lookup(pmid=pmid, pmcid=pmc, doi=doi)
            time.sleep(PAUSE)
            if not rec:
                log.append(f"| {folder} | {title[:80]} | 색인 없음 |")
                miss += 1
                continue
            src = download_pdf(rec, pdf)
            if src:
                print("   PDF 저장:", os.path.basename(pdf))
                log.append(f"| {folder} | {title[:80]} | PDF |")
                got += 1
            else:
                ab = rec.get("abstractText")
                if ab:
                    with open(os.path.join(fdir, fn[:-3] + "_abstract.md"), "w", encoding="utf-8") as fh:
                        fh.write(f"# {rec.get('title','')}\n\n"
                                 f"{rec.get('authorString','')}. {rec.get('journalTitle','')} "
                                 f"{rec.get('pubYear','')}.\n\n"
                                 f"PMID {rec.get('pmid','-')} · {rec.get('doi','-')}\n\n"
                                 f"## Abstract\n\n{ab}\n")
                    log.append(f"| {folder} | {title[:80]} | 초록만 (구독 필요) |")
                else:
                    log.append(f"| {folder} | {title[:80]} | 실패 |")
                miss += 1
            time.sleep(PAUSE)
    log += ["", f"PDF {got}건 · 미확보 {miss}건"]
    with open(os.path.join(ARCHIVE, "_다운로드결과.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(log))
    print(f"\n완료 — PDF {got}건, 미확보 {miss}건")


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else None)
