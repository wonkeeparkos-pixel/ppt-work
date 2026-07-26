# -*- coding: utf-8 -*-
"""정형외과 통증 · 보툴리눔 톡신 문헌고찰 — 웹 덱(HTML) 빌드.

deck_html.render_deck() + Pretendard 서브셋 임베드(외부 리소스 0).
"""
import os
import sys
import re
import io
import base64

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_html import render_deck                      # noqa: E402
from content_botox import BOTOX                        # noqa: E402
from fontTools.subset import Subsetter, Options        # noqa: E402
from fontTools.ttLib import TTFont                      # noqa: E402

TITLE = "정형외과 통증과 보툴리눔 톡신 · 문헌고찰 · v1.0"
REPO = "/home/user/ppt-work"
OUT_DIR = os.path.join(REPO, "문헌고찰_보툴리눔_정형외과통증")
FONT_DIR = os.environ.get(
    "PRETENDARD_DIR",
    "/tmp/claude-0/-home-user-ppt-work/4a16da38-a82b-5d5e-a9c9-97ae114e4ff2/scratchpad/fonts",
)
FONTS = {
    "__F900__": "Pretendard-Black.otf",
    "__F800__": "Pretendard-ExtraBold.otf",
    "__F700__": "Pretendard-Bold.otf",
    "__F300__": "Pretendard-Light.otf",
}

os.makedirs(OUT_DIR, exist_ok=True)
html = render_deck(TITLE, BOTOX)
html = html.replace(
    f'<div class="deckttl">{TITLE}</div>',
    '<div class="deckttl">정형외과 통증과 보툴리눔 톡신 · 문헌고찰 · <b>v1.0</b></div>',
)
# 이 덱은 항목 수가 많다 → 덱 전체에 compact 타입 스케일 적용(일관성 유지)
for k in ("content", "split", "key", "refs"):
    html = html.replace(f'class="snap {k}"', f'class="snap {k} cp"')

# ── 폰트 서브셋: 실제로 쓰인 글자만 ─────────────────────
vis = re.sub(r"<style.*?</style>", "", html, flags=re.S)
vis = re.sub(r"<script.*?</script>", "", vis, flags=re.S)
vis = re.sub(r"<[^>]+>", " ", vis)
chars = set(vis)
chars |= set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    ".,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@✓✗①②③④⑤⑥"
)
text = "".join(sorted(chars))
print("glyphs:", len(chars))

for ph, fname in FONTS.items():
    path = os.path.join(FONT_DIR, fname)
    opt = Options()
    opt.flavor = "woff2"
    opt.desubroutinize = True
    opt.name_IDs = []
    opt.name_legacy = False
    opt.name_languages = []
    font = TTFont(path)
    sub = Subsetter(options=opt)
    sub.populate(text=text)
    sub.subset(font)
    buf = io.BytesIO()
    font.save(buf)
    uri = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
    html = html.replace(ph, uri)
    print(f"  {ph} {len(buf.getvalue())/1024:.0f} KB")

out = os.path.join(OUT_DIR, "보툴리눔_정형외과통증_발표_웹.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print(f"slides: {len(BOTOX)} | out: {out} | {len(html.encode())/1024:.0f} KB")
