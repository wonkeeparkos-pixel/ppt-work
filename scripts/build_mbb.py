# -*- coding: utf-8 -*-
"""HTML 덱 빌드 — 사용 글리프만 서브셋해 Pretendard/IBM Plex Mono를 data URI로 임베드한다."""
import base64
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fontTools.subset import Options, Subsetter
from fontTools.ttLib import TTFont

import deck_mbb as D
import content_mbb as C

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FDIR = os.path.join(BASE, "assets", "fonts")

FONTS = {
    "__P900__": "Pretendard-Black.woff2",
    "__P800__": "Pretendard-ExtraBold.woff2",
    "__P600__": "Pretendard-SemiBold.woff2",
    "__P400__": "Pretendard-Regular.woff2",
    "__P300__": "Pretendard-Light.woff2",
    "__M500__": "ibm-plex-mono-latin-500-normal.woff2",
    "__M600__": "ibm-plex-mono-latin-600-normal.woff2",
}
LATIN = ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
         " .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@①②③④⑤⑥⑦⑧⑨✓✗")


def visible_text(html):
    v = re.sub(r"<style.*?</style>", "", html, flags=re.S)
    v = re.sub(r"<script.*?</script>", "", v, flags=re.S)
    v = re.sub(r"<[^>]+>", " ", v)
    return v


def subset(path, text, mono=False):
    o = Options()
    o.flavor = "woff2"
    o.desubroutinize = True
    o.name_IDs = []
    o.name_legacy = False
    o.name_languages = []
    o.layout_features = ["*"]
    f = TTFont(path)
    s = Subsetter(options=o)
    s.populate(text=LATIN if mono else text)
    s.subset(f)
    buf = io.BytesIO()
    f.save(buf)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()


def build(out_path, title):
    html = D.render_deck(title, C.SLIDES)
    chars = set(visible_text(html)) | set(LATIN)
    text = "".join(sorted(chars))
    print(f"슬라이드 {len(C.SLIDES)}장 · 글리프 {len(chars)}자")
    for ph, fn in FONTS.items():
        path = os.path.join(FDIR, fn)
        uri = subset(path, text, mono=ph.startswith("__M"))
        print(f"  {ph} {len(uri)/1024:6.0f}KB  {fn}")
        html = html.replace(ph, uri)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"→ {out_path}  ({len(html.encode())/1024:.0f}KB)")
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "요추_MBB_후관절차단_발표.html")
    build(out, "요추 내측지차단 · 후관절차단 문헌고찰")
