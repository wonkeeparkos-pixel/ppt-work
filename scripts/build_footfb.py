# -*- coding: utf-8 -*-
"""발바닥 이물감(껌딱지 느낌)·지간신경종 문헌고찰 3종 md → docx 렌더.
기존 docx_lib.render_markdown 재사용(NLC/RLS/LSB와 동일 스타일)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import render_markdown

BASE = "/home/user/ppt-work/발바닥_이물감_껌딱지느낌"
NAMES = ["발바닥이물감_문헌고찰", "발바닥이물감_요약본", "발바닥이물감_참고문헌"]

made = []
for name in NAMES:
    md_path = os.path.join(BASE, name + ".md")
    docx_path = os.path.join(BASE, name + ".docx")
    with open(md_path, encoding="utf-8") as f:
        md = f.read()
    render_markdown(md, docx_path)
    made.append(docx_path)

for m in made:
    print(os.path.relpath(m, BASE), os.path.getsize(m))
print("TOTAL", len(made), "docx")
