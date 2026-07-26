# -*- coding: utf-8 -*-
"""
문헌 아카이브 생성기.

이 컨테이너의 네트워크 정책이 PubMed/PMC/출판사 호스트로의 아웃바운드를 차단하므로
(프록시가 CONNECT에 403), PDF 원문을 내려받을 수 없다. 대신 문헌고찰 워크플로가
수집한 근거를 출처(문헌) 단위로 재조립해 주제별 폴더에 '문헌 카드'로 저장한다.

각 카드에 담기는 것
  · 서지정보 (저자·저널·연도·PMID/PMC/DOI)
  · 원문 링크 (PubMed / PMC / DOI)
  · 그 문헌에서 인용된 모든 근거 항목 (수치 포함, 신뢰도 등급 표기)
  · 확인 실패 항목은 그대로 '미확인'으로 남긴다

원문 PDF가 필요하면 scripts/fetch_papers.py 를 네트워크 제약이 없는 환경에서 실행한다.
"""
import json
import os
import re
import sys
from collections import OrderedDict

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(BASE, "문헌고찰_Lumbar_MBB_Facet")

# 워크플로 토픽 순서 → 폴더
FOLDERS = [
    "01_해부_Anatomy",
    "02_연관통_Referred_Pain",
    "03_진단차단_근거_Validity",
    "04_술기_MBB_Technique",
    "05_술기_관절강내_IA_Injection",
    "06_적응증_가이드라인_Guidelines",
    "07_효과_논쟁_Outcomes",
    "08_합병증_안전성_Complications",
]

PMID_RE = re.compile(r"PMID[:\s]*(\d{5,9})", re.I)
PMC_RE = re.compile(r"(PMC\d{5,9})", re.I)
DOI_RE = re.compile(r"\b(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+?)(?=[\s,;)]|$)")
YEAR_RE = re.compile(r"\b(19[5-9]\d|20[0-2]\d)\b")


def slug(s, n=70):
    s = re.sub(r"[^\w가-힣\s.-]", "", s)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:n].strip("._-") or "untitled"


def split_sources(src):
    """'A. J. 1999. PMID 1; B. J. 2000' → 개별 문헌 문자열로 분리."""
    if not src:
        return []
    parts = re.split(r";\s+(?=[A-Z강-힣])|\.\s+(?=[A-Z][a-z]+\s+[A-Z]{1,3}[,.]\s)", src)
    return [p.strip(" ;.") for p in parts if len(p.strip(" ;.")) > 12]


def keyize(s):
    """같은 문헌을 하나로 묶기 위한 키 — PMID > PMC > DOI > 저자+연도."""
    m = PMID_RE.search(s)
    if m:
        return "pmid:" + m.group(1)
    m = PMC_RE.search(s)
    if m:
        return "pmc:" + m.group(1).upper()
    m = DOI_RE.search(s)
    if m:
        return "doi:" + m.group(1).lower().rstrip(".")
    au = re.match(r"([A-Z][A-Za-z'\-]+)", s)
    yr = YEAR_RE.search(s)
    return f"cite:{(au.group(1) if au else '?').lower()}:{yr.group(1) if yr else '?'}"


def links_for(s):
    out = []
    m = PMID_RE.search(s)
    if m:
        out.append(("PubMed", f"https://pubmed.ncbi.nlm.nih.gov/{m.group(1)}/"))
    m = PMC_RE.search(s)
    if m:
        out.append(("PMC 전문", f"https://www.ncbi.nlm.nih.gov/pmc/articles/{m.group(1).upper()}/"))
    m = DOI_RE.search(s)
    if m:
        out.append(("DOI", f"https://doi.org/{m.group(1).rstrip('.')}"))
    if not out:
        q = re.sub(r"\s+", "+", s[:120])
        out.append(("PubMed 검색", f"https://pubmed.ncbi.nlm.nih.gov/?term={q}"))
    return out


def load_results(journal_path):
    res = []
    with open(journal_path, encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            r = d.get("result")
            if isinstance(r, dict) and r.get("findings"):
                res.append(r)
    return res


def build(journal_path):
    results = load_results(journal_path)
    if not results:
        print("결과 없음:", journal_path)
        return
    os.makedirs(ARCHIVE, exist_ok=True)
    master = OrderedDict()
    total_cards = 0

    for i, r in enumerate(results):
        folder = os.path.join(ARCHIVE, FOLDERS[i] if i < len(FOLDERS) else f"{i+1:02d}_기타")
        os.makedirs(folder, exist_ok=True)

        papers = OrderedDict()
        for f in r.get("findings", []):
            for one in split_sources(f.get("source", "")):
                k = keyize(one)
                p = papers.setdefault(k, {"cites": set(), "findings": []})
                p["cites"].add(one)
                p["findings"].append(f)

        index = [f"# {FOLDERS[i] if i < len(FOLDERS) else '기타'}",
                 "", f"**주제**: {r.get('topic','')}", "",
                 f"문헌 {len(papers)}편 · 근거항목 {len(r.get('findings', []))}개", "",
                 "| # | 문헌 | 근거항목 | 파일 |", "|---|---|---|---|"]

        for n, (k, p) in enumerate(papers.items(), 1):
            cite = sorted(p["cites"], key=len)[-1]
            fname = f"{n:02d}_{slug(cite.split('.')[0])}.md"
            lines = [f"# {cite}", ""]
            lines.append("> 이 파일은 원문 PDF가 아니다. 컨테이너 네트워크 정책이 PubMed/PMC/출판사")
            lines.append("> 접속을 차단해(프록시 403) 원문을 내려받을 수 없었다. 아래 내용은 문헌검색으로")
            lines.append("> 수집한 근거를 문헌 단위로 재조립한 것이며, 초록 원문 전재가 아니다.")
            lines.append("> 원문은 아래 링크에서 직접 확인할 것.")
            lines.append("")
            lines.append("## 원문 링크")
            for label, url in links_for(cite):
                lines.append(f"- [{label}]({url})")
            lines.append("")
            lines.append(f"## 이 문헌에서 인용된 근거 ({len(p['findings'])}건)")
            lines.append("")
            for f in p["findings"]:
                conf = {"high": "확실", "medium": "보통", "low": "미확인"}.get(f.get("confidence"), "?")
                lines.append(f"### [{conf}] {f.get('claim','')}")
                lines.append("")
                lines.append(f.get("detail", ""))
                lines.append("")
                lines.append(f"*원 출처 표기*: `{f.get('source','')}`")
                lines.append("")
            if len(p["cites"]) > 1:
                lines.append("## 함께 표기된 다른 서지 문자열")
                for c in sorted(p["cites"]):
                    lines.append(f"- {c}")
                lines.append("")
            with open(os.path.join(folder, fname), "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines))
            total_cards += 1
            index.append(f"| {n} | {cite[:110]} | {len(p['findings'])} | [{fname}]({fname}) |")
            master.setdefault(k, {"cite": cite, "topics": []})["topics"].append(
                FOLDERS[i] if i < len(FOLDERS) else "기타")

        if r.get("gaps"):
            index += ["", "## 확인하지 못한 항목 (gaps)", ""]
            index += [f"- {g}" for g in r["gaps"]]
        with open(os.path.join(folder, "_INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("\n".join(index))

    # 마스터 서지
    m = ["# 전체 참고문헌", "",
         f"주제 {len(results)}개 · 문헌 {len(master)}편 · 문헌카드 {total_cards}개", "",
         "| # | 문헌 | 주제 폴더 | 링크 |", "|---|---|---|---|"]
    for n, (k, v) in enumerate(sorted(master.items(), key=lambda x: x[1]["cite"]), 1):
        ln = " · ".join(f"[{a}]({b})" for a, b in links_for(v["cite"]))
        m.append(f"| {n} | {v['cite'][:130]} | {', '.join(sorted(set(v['topics'])))} | {ln} |")
    with open(os.path.join(ARCHIVE, "00_전체참고문헌.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(m))

    print(f"주제 {len(results)} · 고유문헌 {len(master)} · 카드 {total_cards} → {ARCHIVE}")


if __name__ == "__main__":
    build(sys.argv[1])
