# -*- coding: utf-8 -*-
"""도해 검수용 — 모든 SVG를 한 페이지에 렌더해 스크린샷으로 확인한다."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figs_mbb as F
import deck_mbb as D

FIGS = [
    ("posterior_spine", F.posterior_spine()),
    ("dual_bracket", F.dual_bracket()),
    ("scotty_dog", F.scotty_dog()),
    ("scotty_dog(wrong)", F.scotty_dog(target=False, wrong=True)),
    ("ap_target", F.ap_target()),
    ("l5_dorsal_ramus", F.l5_dorsal_ramus()),
    ("fukui_zones", F.fukui_zones("z")),
    ("facet_orientation", F.facet_orientation()),
    ("lateral_depth(ok)", F.lateral_depth(True)),
    ("lateral_depth(bad)", F.lateral_depth(False)),
    ("volume_spread(ok)", F.volume_spread("0.3-0.5 mL", True)),
    ("volume_spread(bad)", F.volume_spread("1.5 mL", False)),
    ("us_trident", F.us_trident()),
    ("algorithm", F.algorithm()),
]

cards = "".join(
    f'<div class="card"><div class="cn">{n}</div><div class="cs">{s}</div></div>' for n, s in FIGS
)

html = f"""<!doctype html><meta charset="utf-8"><title>figs</title>
<style>
{D.CSS}
body{{background:var(--room);padding:24px;font-family:Pretendard,sans-serif}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
.card{{background:var(--stage);border:1px solid var(--line);border-radius:8px;padding:14px}}
.cn{{font-family:PlexM,monospace;font-size:12px;font-weight:600;color:var(--nerve);margin-bottom:8px}}
.cs svg{{width:100%;height:auto;max-height:340px}}
</style>
<div class="grid">{cards}</div>
"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_figpreview.html")
open(out, "w", encoding="utf-8").write(html)
print(os.path.abspath(out))
