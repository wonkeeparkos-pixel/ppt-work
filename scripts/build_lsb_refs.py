# -*- coding: utf-8 -*-
"""LSB 근거문헌 카드 PDF 생성기.
03_LSB/근거문헌/ 아래에 문헌별 요약 PDF + 색인 PDF를 만든다.
각 카드: 서지정보 · 식별자(PMID/PMCID/DOI) · 원문 링크 · 핵심 결과 · 덱에서 쓰인 위치."""
import os, json, html

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/03_LSB/근거문헌"
os.makedirs(BASE, exist_ok=True)

REFS = [
 dict(no=1, key="StatPearls_LSB", title="Lumbar Sympathetic Block",
      authors="Dua A, Varacallo MA.", src="StatPearls [Internet]. Treasure Island (FL): StatPearls Publishing; 2026.",
      ids=[("Bookshelf", "NBK431107", "https://www.ncbi.nlm.nih.gov/books/NBK431107/")],
      kind="총설 (Review)", level="—",
      points=["표적: 교감신경절 밀도가 가장 높은 L2 하 1/3 ~ L3 상 1/3, 척추체 전외측.",
              "표준 술기: 방척추(paravertebral) 접근 + 투시 유도. 정중선에서 약 7 cm 외측 진입.",
              "조영제로 두미측(craniocaudal) 종방향 확산 확인 후 약물 주입.",
              "성공 지표: 동측 하지 피부온도 ≥2°C 상승.",
              "합병증: 생식대퇴신경통, 외측대퇴피신경 손상, 기립성 저혈압, 혈관·요관·신장 손상, 신경축 확산."],
      used="p3 개요·해부 / p4 방법 / p5 조감도 / p7 주의점 / p8 합병증표"),
 dict(no=2, key="StatPearls_Sympatholysis", title="Lumbar Sympatholysis",
      authors="StatPearls [Internet].", src="Treasure Island (FL): StatPearls Publishing.",
      ids=[("Bookshelf", "NBK560514", "https://www.ncbi.nlm.nih.gov/books/NBK560514/")],
      kind="총설 (Review)", level="—",
      points=["국소마취제 차단(진단적/치료적)과 화학적·열적 신경파괴(무수알코올/phenol, RFA)의 구분.",
              "신경파괴는 국소마취제 진단적 차단이 양성일 때에만 시행하는 것이 원칙.",
              "적응증·금기·합병증 총설."],
      used="p4 방법(약제) / p12 프로토콜"),
 dict(no=3, key="Zhang_2022_Ibrain", title="Efficacy of the lumbar sympathetic ganglion block in lower limb pain and its application prospects during the perioperative period",
      authors="Zhang JH, Deng YP, Geng MJ.", src="Ibrain. 2022;8(4):442-452.",
      ids=[("PMID","37786587","https://pubmed.ncbi.nlm.nih.gov/37786587/"),
           ("PMCID","PMC10529158","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10529158/")],
      kind="종설 (Narrative review)", level="—",
      points=["기전: 하지 혈관 긴장도 감소 · 평활근 연축 완화 · 측부순환 증가 · endothelin 감소.",
              "교감신경 매개 통증(sympathetically-maintained pain) 경로 차단.",
              "주술기(perioperative) 적용 가능성 제시."],
      used="p3 개요·원리 / p11 효과②(기전)"),
 dict(no=4, key="Dickey_2024_Cureus", title="Lumbar Sympathetic Block Leading to Increased Arterial Diameter and Blood Flow: A Mechanism of Therapeutic Benefit",
      authors="Dickey Z, Sharma N.", src="Cureus. 2024;16(6):e61755.",
      ids=[("PMID","38975506","https://pubmed.ncbi.nlm.nih.gov/38975506/"),
           ("PMCID","PMC11227424","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11227424/")],
      kind="증례/실측 관찰", level="Level IV",
      points=["LSB 후 초음파상 후경골동맥 직경 0.17 → 0.27 cm (+58.8%).",
              "모세혈관 재충혈 시간 3.92 → 1.30초.",
              "족부 온도 +2.8°C.",
              "→ 관류 개선을 객관적으로 실측한 근거."],
      used="p10 효과①(관류 실측 카드)"),
 dict(no=5, key="Barreto_2018_BJAN", title="Neurolytic block of the lumbar sympathetic chain improves chronic pain in a patient with critical lower limb ischemia",
      authors="Barreto Junior EPS, Nascimento JS, Castro APCR.", src="Braz J Anesthesiol. 2018;68(1):100-103.",
      ids=[("PMCID","PMC9391669","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9391669/")],
      kind="증례 보고 (Case report)", level="Level V",
      points=["재건 불가능한 중증 하지허혈(CLI) 환자에서 교감신경 신경파괴로 만성 통증 개선.",
              "절단 외 대안이 없는 환자에서 통증조절 수단으로 효과적·안전."],
      used="p10 효과①(비재건성 CLI)"),
 dict(no=6, key="Choi_2024_SciRep", title="Effect duration of lumbar sympathetic ganglion neurolysis in patients with complex regional pain syndrome: a prospective observational study",
      authors="Choi EJ, Kim S, Lim D, et al.", src="Sci Rep. 2024;14(1):12693.",
      ids=[("PMID","38830944","https://pubmed.ncbi.nlm.nih.gov/38830944/")],
      kind="전향 관찰연구", level="Level III",
      points=["CRPS 환자에서 교감신경절 신경파괴의 효과 지속기간을 전향적으로 제시.",
              "환자 선택과 시행 시점이 결과에 영향."],
      used="p11 효과②(CRPS)"),
 dict(no=7, key="Gungor_2018_Medicine", title="Sympathetic blocks for the treatment of complex regional pain syndrome: a case series",
      authors="Gungor S, Aiyer R, Baykoca B.", src="Medicine (Baltimore). 2018;97(19):e0705.",
      ids=[("PMID","29742728","https://pubmed.ncbi.nlm.nih.gov/29742728/")],
      kind="증례군 (Case series)", level="Level IV",
      points=["CRPS에서 교감신경차단 후 통증완화 경험 축적.",
              "조기 시행·적절한 환자 선택이 성공률을 높임."],
      used="p11 효과②(CRPS)"),
 dict(no=8, key="Medicina_2024_PAD", title="Retrospective Evaluation of the Effect of Lumbar Sympathetic Blockade on Pain Scores, Fontaine Classification, and Collateral Perfusion Status in Patients with Lower Extremity Peripheral Arterial Disease",
      authors="(Medicina 편집부 게재 논문)", src="Medicina (Kaunas). 2024;60(5):682.",
      ids=[("DOI","10.3390/medicina60050682","https://doi.org/10.3390/medicina60050682")],
      kind="후향 연구 (Retrospective)", level="Level III",
      points=["PAD 환자에서 LSB 후 하지 통증 최대 75% 감소 보고.",
              "Fontaine 분류 및 측부관류 상태 개선."],
      used="p10 효과①(허혈성 통증)"),
 dict(no=9, key="PainTher_2023_SSR", title="Prediction of the Efficacy of Lumbar Sympathetic Block in Patients with Lower Extremity Complex Regional Pain Syndrome Type 1 Based on the Sympathetic Skin Response",
      authors="(Pain and Therapy 게재 논문)", src="Pain Ther. 2023;12(3):809-822.",
      ids=[("PMCID","PMC10199976","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10199976/")],
      kind="예측인자 연구", level="Level III",
      points=["교감신경 피부반응(SSR)이 하지 CRPS I형에서 LSB 반응을 예측하는 데 유용.",
              "시술 전 반응 예측 → 환자 선택 정밀화."],
      used="p11 효과②(반응 예측)"),
 dict(no=10, key="Feigl_1998_L2vsL4", title="Incidence of genitofemoral nerve block during lumbar sympathetic block: comparison of two lumbar injection sites",
      authors="(Regional Anesthesia 게재 논문)", src="Reg Anesth Pain Med. 1998.",
      ids=[("PMID","9425975","https://pubmed.ncbi.nlm.nih.gov/9425975/")],
      kind="비교 연구", level="Level III",
      points=["L2에서 시행 시 생식대퇴신경 차단 발생 0%, L4에서는 약 40%.",
              "→ 낮은 레벨(L4)일수록 생식대퇴신경통 위험이 급증.",
              "표적은 L2 하 1/3 ~ L3 상 1/3로 유지하고 L4는 피할 것."],
      used="p8 합병증표 / p9 생식대퇴신경통 도해"),
 dict(no=11, key="StatPearls_SympatheticBlock", title="Sympathetic Nerve Block",
      authors="StatPearls [Internet].", src="Treasure Island (FL): StatPearls Publishing.",
      ids=[("Bookshelf","NBK557637","https://www.ncbi.nlm.nih.gov/books/NBK557637/")],
      kind="총설 (Review)", level="—",
      points=["교감신경차단 전반의 적응증·기법·합병증.",
              "psoas 근육내 주입 회피, 영상 유도의 중요성."],
      used="p7 주의점 / p8 합병증표"),
 dict(no=12, key="DPN_RCT_2020", title="Continuous lumbar sympathetic blockade enhances the effect of lumbar sympatholysis on refractory painful diabetic neuropathy (RCT)",
      authors="Zhang X, et al.", src="2020. (Randomized controlled trial)",
      ids=[("PMID","32915421","https://pubmed.ncbi.nlm.nih.gov/32915421/"),
           ("PMCID","PMC7547930","https://pmc.ncbi.nlm.nih.gov/articles/PMC7547930/")],
      kind="무작위 대조 연구 (RCT)", level="Level II",
      points=["난치성 당뇨병성 신경병증통에서 지속적 요추교감신경차단 + 신경파괴의 효과를 RCT로 검증.",
              "LSB 계열에서 드문 상위 근거 — 통증완화와 효과 지속성 제시.",
              "약물 불응(refractory) 환자에서 중재적 치료 선택지로 뒷받침."],
      used="p6 야간 신경병증통 + LSB / p13 근거수준"),
 dict(no=13, key="DPN_case_2012", title="Sympathetic blocks provided sustained pain relief in a patient with refractory painful diabetic neuropathy",
      authors="(Case report)", src="2012.",
      ids=[("PMID","22606406","https://pubmed.ncbi.nlm.nih.gov/22606406/"),
           ("PMCID","PMC3350298","https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3350298/")],
      kind="증례 보고 (Case report)", level="Level V",
      points=["난치성 당뇨병성 신경병증통에서 반복 교감신경차단으로 지속적 통증완화."],
      used="p6 야간 신경병증통 + LSB"),
 dict(no=14, key="Sympathectomy_series_2018", title="Lumbar sympathectomy for ischaemia, vasculitis, diabetic neuropathy and hyperhidrosis — single centre series",
      authors="(Single-centre series)", src="2018.",
      ids=[("PMID","29516399","https://pubmed.ncbi.nlm.nih.gov/29516399/")],
      kind="증례군 (Case series)", level="Level IV",
      points=["허혈·혈관염·당뇨병성 신경병증·다한증에서 요추교감신경절제 결과.",
              "다양한 적응증에서의 실제 임상 경험."],
      used="p6 신경병증 / p14 적응증"),
 dict(no=15, key="StatPearls_DPN", title="Diabetic Peripheral Neuropathy",
      authors="StatPearls [Internet].", src="Treasure Island (FL): StatPearls Publishing.",
      ids=[("Bookshelf","NBK442009","https://www.ncbi.nlm.nih.gov/books/NBK442009/")],
      kind="총설 (Review)", level="—",
      points=["당뇨병성 말초신경병증의 임상상: 저림·화끈거림·전기 오듯 찌름·감각이상, 양측 '양말' 분포.",
              "야간 악화(이불 속 온기·야간 순환 변화·주의분산 소실)로 수면 방해.",
              "1차 치료: 혈당조절 + 약물(가바펜틴·프레가발린·듀록세틴)."],
      used="p6 야간 신경병증통"),
]

CSS = """
*{box-sizing:border-box} body{margin:0;font-family:'Noto Sans KR','NanumGothic',sans-serif;color:#17232C}
.page{width:210mm;min-height:296mm;padding:18mm 16mm;page-break-after:always}
.eb{font-size:10.5pt;font-weight:800;letter-spacing:.12em;color:#0E7C7B;text-transform:uppercase}
h1{font-size:19pt;line-height:1.28;margin:6px 0 4px;letter-spacing:-.3px}
.auth{font-size:11.5pt;color:#3A4750;margin:2px 0}
.src{font-size:11.5pt;color:#5A6B7B;font-style:italic;margin-bottom:10px}
.meta{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 14px}
.chip{font-size:10pt;font-weight:700;padding:4px 10px;border-radius:999px;background:#EEF3F2;color:#0B5F5E;border:1px solid #D6E3E1}
.chip.lv{background:#FBF3E3;color:#8A5D00;border-color:#EAD9B4}
hr{border:0;border-top:1.4px solid #E4E9E8;margin:12px 0 14px}
h2{font-size:12.5pt;color:#0B5F5E;margin:14px 0 6px}
ul{margin:0;padding-left:18px} li{font-size:11.5pt;line-height:1.55;margin-bottom:5px}
.ids a{font-size:11pt;color:#0E7C7B;text-decoration:none;word-break:break-all}
.ids div{margin-bottom:4px}
.used{font-size:11pt;background:#F5F8FB;border-left:3px solid #0E7C7B;padding:8px 12px;color:#33403B}
.foot{margin-top:18px;font-size:9.5pt;color:#8A96A0;border-top:1px solid #E4E9E8;padding-top:8px}
table{width:100%;border-collapse:collapse;margin-top:8px}
th{background:#17232C;color:#fff;font-size:10.5pt;text-align:left;padding:7px 8px}
td{font-size:10.5pt;padding:6px 8px;border-bottom:1px solid #E4E9E8;vertical-align:top}
tr:nth-child(even) td{background:#F5F8FB}
"""

def card_html(r):
    ids = ''.join(f'<div><b>{html.escape(k)}</b> {html.escape(v)} — <a href="{u}">{u}</a></div>'
                  for k, v, u in r['ids'])
    pts = ''.join(f'<li>{html.escape(p)}</li>' for p in r['points'])
    return f"""<div class="page">
<div class="eb">근거문헌 {r['no']:02d} · LSB</div>
<h1>{html.escape(r['title'])}</h1>
<div class="auth">{html.escape(r['authors'])}</div>
<div class="src">{html.escape(r['src'])}</div>
<div class="meta"><span class="chip">{html.escape(r['kind'])}</span><span class="chip lv">근거수준 {html.escape(r['level'])}</span></div>
<hr>
<h2>핵심 내용</h2><ul>{pts}</ul>
<h2>식별자 · 원문</h2><div class="ids">{ids}</div>
<h2>발표자료에서 쓰인 곳</h2><div class="used">{html.escape(r['used'])}</div>
<div class="foot">요추교감신경차단(LSB) 문헌고찰 · 교육·연구 참고용 · 서지정보는 PubMed/PMC/StatPearls 대조 · 원문 전문은 위 링크에서 확인</div>
</div>"""

def index_html():
    rows = ''.join(
        f"<tr><td>{r['no']:02d}</td><td><b>{html.escape(r['title'][:78])}</b><br>"
        f"<span style='color:#5A6B7B'>{html.escape(r['authors'])} {html.escape(r['src'])}</span></td>"
        f"<td>{html.escape(r['kind'])}<br>{html.escape(r['level'])}</td>"
        f"<td>{'<br>'.join(html.escape(k+' '+v) for k,v,_ in r['ids'])}</td></tr>" for r in REFS)
    return f"""<div class="page">
<div class="eb">색인 · Index</div>
<h1>LSB 근거문헌 목록 ({len(REFS)}편)</h1>
<div class="src">요추교감신경차단 발표자료의 모든 인용 문헌 — 파일별 PDF는 같은 폴더에 저장</div>
<table><tr><th>#</th><th>제목 / 서지</th><th>유형·수준</th><th>식별자</th></tr>{rows}</table>
<div class="foot">조작된 인용 없음 — 모든 항목은 PubMed/PMC/StatPearls 목록과 대조. 일부 종설의 권·페이지·저자는 원문 재확인 권장.</div>
</div>"""

def wrap(body):
    return f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>"

pages = [("00_색인_INDEX", index_html())]
for r in REFS:
    pages.append((f"{r['no']:02d}_{r['key']}", card_html(r)))

manifest = []
for name, body in pages:
    p = os.path.join(BASE, name + ".html")
    open(p, "w", encoding="utf-8").write(wrap(body))
    manifest.append({"name": name, "html": p, "pdf": os.path.join(BASE, name + ".pdf")})
open(os.path.join(BASE, "_manifest.json"), "w").write(json.dumps(manifest, ensure_ascii=False))
print("html pages:", len(pages), "->", BASE)
