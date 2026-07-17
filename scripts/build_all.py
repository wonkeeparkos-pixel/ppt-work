# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from docx_lib import render_markdown
from content_nlc import NLC
from content_rls import RLS
from content_lsb import LSB

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"
TOPICS = [("01_NLC", NLC), ("02_RLS", RLS), ("03_LSB", LSB)]

made = []
for sub, docs in TOPICS:
    d = os.path.join(BASE, sub)
    os.makedirs(d, exist_ok=True)
    for name, md in docs.items():
        docx_path = os.path.join(d, name + ".docx")
        md_path = os.path.join(d, name + ".md")
        open(md_path, "w").write(md)
        render_markdown(md, docx_path)
        made.append(docx_path)

for m in made:
    print(os.path.relpath(m, BASE), os.path.getsize(m))
print("TOTAL", len(made), "docx")
