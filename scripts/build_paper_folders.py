# -*- coding: utf-8 -*-
"""질환·부위별 논문 폴더와 확인용 체크리스트를 만든다.

PDF 자체는 `fetch_papers.py`가 각자 컴퓨터에서 받아 같은 폴더에 채운다.
(이 저장소를 만든 세션은 PubMed·PMC·출판사 도메인이 차단돼 있어 PDF를 받을 수 없다.)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from papers import FOLDERS, PAPERS, link  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "문헌고찰_보툴리눔_정형외과통증", "논문")


def main():
    os.makedirs(ROOT, exist_ok=True)
    by_folder = {}
    for p in PAPERS:
        by_folder.setdefault(p["folder"], []).append(p)

    index = ["# 논문 폴더 — 질환·부위별\n",
             "발표에 인용한 논문을 슬라이드 순서(목 → 발 → 수술후)대로 폴더에 나눴다.",
             "폴더마다 `README.md`에 **체크리스트**가 있으니 하나씩 원문과 대조하면서 `[ ]`를 `[x]`로 바꾸면 된다.\n",
             "## PDF는 아직 비어 있다\n",
             "이 저장소를 만든 환경은 PubMed·PMC·출판사 도메인이 차단돼 PDF를 받을 수 없었다.",
             "각자 컴퓨터(또는 병원 네트워크)에서 아래를 실행하면 오픈액세스 논문이 자동으로 각 폴더의 `PDF/`에 들어간다.\n",
             "```bash\npython3 scripts/fetch_papers.py\n```\n",
             "받지 못한 논문은 `_못받은목록.md`에 링크와 함께 남는다 — 도서관 프록시로 직접 받으면 된다.\n",
             "## 폴더\n",
             "| 폴더 | 부위 · 질환 | 논문 수 | 슬라이드 |",
             "|---|---|---|---|"]

    for folder, label in FOLDERS:
        ps = by_folder.get(folder, [])
        pdf_dir = os.path.join(ROOT, folder, "PDF")
        os.makedirs(pdf_dir, exist_ok=True)
        with open(os.path.join(pdf_dir, ".gitkeep"), "w") as f:
            f.write("")

        slides = sorted({s.strip() for p in ps for s in p["slides"].split(",")})
        index.append(f"| [`{folder}`](./{folder}/) | {label} | {len(ps)} | {', '.join(slides)} |")

        lines = [f"# {label}\n",
                 f"발표 슬라이드 **{', '.join(slides)}**번의 근거.\n",
                 "원문을 확인하면 `[ ]`를 `[x]`로 바꾼다. "
                 "**핵심 수치**는 발표에 실제로 쓴 값이므로 이것부터 대조한다.\n"]
        for p in ps:
            lines += [
                f"## [ ] {p['authors']} ({p['year']})\n",
                f"**{p['title']}**  ",
                f"*{p['journal']}*\n",
                f"- 슬라이드 **{p['slides']}**",
                f"- 핵심 수치 — {p['finding']}",
                f"- 원문 — {link(p)}",
                f"- PDF — `PDF/{p['key']}.pdf`\n",
            ]
        lines += ["---\n", "PDF가 없으면 저장소 최상위에서 `python3 scripts/fetch_papers.py` 실행.\n"]
        with open(os.path.join(ROOT, folder, "README.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    index += ["\n## 대조할 때 우선순위\n",
              "1. **06쪽 근거지도**의 등급(A/B/C)이 원문 결론과 맞는지",
              "2. **32쪽 용량표**의 U 값이 각 원문의 실제 투여량인지",
              "3. 승모근 09쪽의 **WMD −10.22**와 요통 20쪽의 **73.3% vs 25%** — 발표에서 가장 세게 말하는 두 숫자\n"]
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))

    print(f"folders: {len(FOLDERS)} | papers: {len(PAPERS)} | -> {ROOT}")


if __name__ == "__main__":
    main()
