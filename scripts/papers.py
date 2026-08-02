# -*- coding: utf-8 -*-
"""발표에 인용한 논문 목록 — 폴더 생성기와 PDF 수집기가 함께 쓰는 단일 원본.

필드
  folder  : 저장 폴더 (질환·부위별)
  slides  : 이 논문이 근거로 쓰인 발표 슬라이드 번호
  finding : 발표에 실제로 인용한 수치·결론 (대조 확인용)
  pmid/pmcid/doi/url : 식별자. PDF 수집기가 이 순서로 시도한다.
"""

FOLDERS = [
    ("00_기전_총론", "기전 · 근거등급 총론"),
    ("01_목어깨_승모근", "목·어깨 — 승모근 근막통증"),
    ("02_어깨", "어깨 — 편마비성 어깨통증"),
    ("03_팔_근경련_경직", "팔 — 진성 근경련 · 경직"),
    ("04_팔_TOS_이긴장증", "팔 — 흉곽출구증후군 · 국소 이긴장증"),
    ("05_팔꿈치_외측상과염", "팔꿈치 — 외측상과염"),
    ("06_허리", "허리 — 만성 요통"),
    ("07_엉덩이_이상근", "엉덩이 — 이상근증후군"),
    ("08_무릎", "무릎 — 관절강내"),
    ("09_종아리_경련_구획", "종아리 — 야간 경련 · 운동유발 구획증후군"),
    ("10_발_족저근막염", "발 — 족저근막염"),
    ("11_수술후_신경통", "수술후 절개부 · 절단 후 신경통"),
    ("12_안전_용량_면역원성", "안전 — 확산 · 면역원성 · 박스경고"),
]

PAPERS = [
    # ── 00 기전 · 총론 ────────────────────────────────────
    dict(folder="00_기전_총론", key="Safarpour2018", year=2018,
         authors="Safarpour Y, Jabbari B",
         title="Botulinum toxin treatment of pain syndromes — an evidence based review",
         journal="Toxicon", pmid="29409817", slides="06, 30",
         finding="18개 통증 증후군 AAN 등급화. 외상후·삼차·대상포진후 신경통 = Level A"),
    dict(folder="00_기전_총론", key="Matak2014", year=2014,
         authors="Matak I, Lacković Z", title="Botulinum toxin A, brain and pain",
         journal="Prog Neurobiol", pmid="24915026", slides="03, 04",
         finding="역행성 축삭수송 · 중추 작용 기전 리뷰"),
    dict(folder="00_기전_총론", key="Mechanisms2019", year=2019,
         authors="—", title="Mechanisms of botulinum toxin type A action on pain",
         journal="Toxins", pmcid="PMC6723487", slides="03, 04",
         finding="SNAP-25 절단 → SP·CGRP·글루타메이트 방출 차단, TRPV1 막이동 감소"),

    # ── 01 목·어깨 승모근 ────────────────────────────────
    dict(folder="01_목어깨_승모근", key="Gobel2006", year=2006,
         authors="Göbel H, et al.",
         title="Efficacy and safety of a single botulinum type A toxin complex treatment (Dysport) for the relief of upper back myofascial pain syndrome",
         journal="Pain 2006;125:82-88", pmid="16750294", slides="08",
         finding="Dysport 400 U를 최대 10개 유발점에 분할 → 5주 시점 위약 대비 유의, 8주까지 유지"),
    dict(folder="01_목어깨_승모근", key="Ojala2006", year=2006,
         authors="Ojala T, et al.",
         title="A randomized, double-blind, placebo-controlled, crossover trial of botulinum toxin A in neck-shoulder myofascial pain",
         journal="Clin J Pain", pmid="16691083", slides="09",
         finding="유발점당 5 U 소량 → 개선 없음 (음성 연구의 전형)"),
    dict(folder="01_목어깨_승모근", key="Soares2014", year=2014,
         authors="Soares A, et al.",
         title="Botulinum toxin for myofascial pain syndromes in adults",
         journal="Cochrane Database Syst Rev", pmid="25062018", slides="09",
         finding="근거 불충분"),
    dict(folder="01_목어깨_승모근", key="Leonardi2024", year=2024,
         authors="Leonardi L, et al.",
         title="Botulinum toxin for upper back myofascial pain syndrome: systematic review of RCTs",
         journal="Eur J Pain", doi="10.1002/ejp.2198", slides="09",
         finding="10편 651명, 결과 혼재 — 중등도–중증 + 활성 유발점에는 신중히 고려"),
    dict(folder="01_목어깨_승모근", key="IJRR2025", year=2025,
         authors="—",
         title="Efficacy of botulinum toxin in myofascial pain in neck and shoulder — systematic review and meta-analysis",
         journal="Int J Rehabil Res", pmid="40237694", slides="09",
         finding="7편 261명, WMD −10.22 (95% CI −12.77~−7.68, 0–100). 통계적 유의·임상적 유의성 미달 → 권고 불가"),
    dict(folder="01_목어깨_승모근", key="Jiang2021", year=2021,
         authors="Jiang Y, et al.",
         title="Ultrasound-guided five-point injection of botulinum toxin for trapezius",
         journal="J Orthop Surg Res", pmid="34686203", slides="10",
         finding="가장 두꺼운 지점 + 주위 4점, 한쪽 50 U"),
    dict(folder="01_목어깨_승모근", key="Kapoor2025", year=2025,
         authors="Kapoor KM, et al.",
         title="Efficacy and safety of botulinum toxin type A injection for trapezius muscle contouring: a systematic review",
         journal="Aesthet Surg J Open Forum", doi="10.1177/30499240251320906", slides="11",
         finding="경도 승모근 근력약화 약 10.7%, 1–3개월 내 회복"),

    # ── 02 어깨 ──────────────────────────────────────────
    dict(folder="02_어깨", key="Stroke2021", year=2021,
         authors="—",
         title="Ultrasound-guided botulinum toxin A injection into subscapularis for hemiplegic shoulder pain: RCT",
         journal="Stroke", doi="10.1161/STROKEAHA.121.034049", slides="12",
         finding="n=36, 견갑하근 표적 → 통증 유의 감소. 대흉근 병행군은 유의성 미달"),

    # ── 03 팔 근경련 · 경직 ──────────────────────────────
    dict(folder="03_팔_근경련_경직", key="Restivo2018", year=2018,
         authors="Restivo DA, et al.",
         title="Efficacy of botulinum toxin A for treating cramps in diabetic neuropathy",
         journal="Ann Neurol", pmid="30225985", slides="14",
         finding="n=50 RCT. 비복근 100 U / 발 소근육 30 U → 1주부터 유의, 14주까지 지속"),
    dict(folder="03_팔_근경련_경직", key="Bertolasi1997", year=1997,
         authors="Bertolasi L, et al.",
         title="Botulinum toxin treatment of muscle cramps: a clinical and neurophysiological study",
         journal="Ann Neurol", pmid="9029067", slides="14",
         finding="경련-근속연축 증후군에서 임상·전기생리 개선"),

    # ── 04 팔 TOS · 이긴장증 ─────────────────────────────
    dict(folder="04_팔_TOS_이긴장증", key="Finlayson2011", year=2011,
         authors="Finlayson HC, et al.",
         title="Botulinum toxin injection for management of thoracic outlet syndrome: a double-blind, randomized, controlled trial",
         journal="Pain", pmid="21628084", slides="16",
         finding="n=38. 6주 VAS 위약 대비 차이 없음 (P=.36) — 음성"),
    dict(folder="04_팔_TOS_이긴장증", key="Torriani2010", year=2010,
         authors="Torriani M, et al.",
         title="Botulinum toxin injection in neurogenic thoracic outlet syndrome: results and experience using a ultrasound-guided approach",
         journal="Skeletal Radiol", pmid="20186413", slides="16",
         finding="41명 92회 주사, 기술적 성공 100%, 합병증 없음"),
    dict(folder="04_팔_TOS_이긴장증", key="HandDystonia2021", year=2021,
         authors="—",
         title="Botulinum toxin therapy in writer's cramp and musician's dystonia",
         journal="Toxins", pmcid="PMC8708945", slides="17",
         finding="대조연구 통합 139명 중 약 73% 호전. 비표적 근육 약화가 한계"),

    # ── 05 팔꿈치 외측상과염 ─────────────────────────────
    dict(folder="05_팔꿈치_외측상과염", key="Wong2005", year=2005,
         authors="Wong SM, et al.",
         title="Treatment of lateral epicondylitis with botulinum toxin: a randomized, double-blind, placebo-controlled trial",
         journal="Ann Intern Med", pmid="16330790", slides="18, 19",
         finding="n=60. Botox 60 U 단일 주사 → 4·12주 통증 유의 감소. 손가락 신전 약화 발생"),
    dict(folder="05_팔꿈치_외측상과염", key="Placzek2007", year=2007,
         authors="Placzek R, et al.",
         title="Treatment of chronic radial epicondylitis with botulinum toxin A: a double-blind, placebo-controlled, randomized multicenter study",
         journal="J Bone Joint Surg Am", pmid="17272437", slides="18",
         finding="위약 대비 개선 확인"),
    dict(folder="05_팔꿈치_외측상과염", key="Espandar2010", year=2010,
         authors="Espandar R, et al.",
         title="Use of anatomic measurement to guide injection of botulinum toxin for the management of chronic lateral epicondylitis: RCT",
         journal="CMAJ", pmid="20421357", slides="18",
         finding="해부학적 계측 주사로 16주까지 통증 감소"),

    # ── 06 허리 ──────────────────────────────────────────
    dict(folder="06_허리", key="Foster2001", year=2001,
         authors="Foster L, Clapp L, Erickson M, Jabbari B",
         title="Botulinum toxin A and chronic low back pain: a randomized, double-blind study",
         journal="Neurology 2001;56:1290-3", pmid="11376175", slides="20, 21",
         finding="n=31. Botox 200 U(방척추 5레벨 × 40 U) → 3주 ≥50% 완화 73.3% vs 25%, 8주 Oswestry 개선"),
    dict(folder="06_허리", key="Wagrees2025", year=2025,
         authors="Wagrees W, et al.",
         title="Botulinum toxin A in chronic low back pain: systematic review, meta-analysis and trial sequential analysis",
         journal="Eur J Pain", doi="10.1002/ejp.4796", slides="20",
         finding="대조 대비 통증·기능 유의 개선, 중대 부작용 없음"),

    # ── 07 엉덩이 이상근 ─────────────────────────────────
    dict(folder="07_엉덩이_이상근", key="Fishman2002", year=2002,
         authors="Fishman LM, et al.",
         title="BOTOX and physical therapy in the treatment of piriformis syndrome",
         journal="Am J Phys Med Rehabil", pmid="12362115", slides="22, 23",
         finding="BTX-A 100 U → ≥50% 개선 65% vs 트리암시놀론+리도카인 32%"),
    dict(folder="07_엉덩이_이상근", key="PiriformisSR2022", year=2022,
         authors="—",
         title="Use of botulinum neurotoxin in the treatment of piriformis syndrome: a systematic review",
         journal="J Clin Orthop Trauma", pmcid="PMC9294329", slides="22",
         finding="7편 152명(RCT 3편), 용량 100–300 U, 근거 fair, 안전성 양호"),

    # ── 08 무릎 ──────────────────────────────────────────
    dict(folder="08_무릎", key="IAKneeMeta2023", year=2023,
         authors="—",
         title="Intra-articular botulinum toxin A for knee osteoarthritis: meta-analysis of randomized controlled trials",
         journal="Toxicon", pmid="36640812", slides="24",
         finding="6편 348명. 히알루론산보다 우수, 스테로이드와 대등하면서 안전성 양호"),
    dict(folder="08_무릎", key="Singh2010", year=2010,
         authors="Singh JA, et al.",
         title="Intraarticular botulinum toxin A for refractory painful total knee arthroplasty: a randomized controlled trial",
         journal="J Rheumatol 2010;37:2377", url="https://www.jrheum.org/content/37/11/2377",
         slides="24", finding="난치성 인공관절 통증에서 유의한 개선"),

    # ── 09 종아리 ────────────────────────────────────────
    dict(folder="09_종아리_경련_구획", key="Park2017", year=2017,
         authors="Park J, et al.",
         title="Botulinum toxin injection for nocturnal calf cramps in patients with lumbar spinal stenosis: RCT",
         journal="Arch Phys Med Rehabil", pmid="28209505", slides="25",
         finding="n=50. 비복근 BTX-A vs gabapentin → 전 시점 통증·빈도·강도 유의 감소 (P<0.01)"),
    dict(folder="09_종아리_경련_구획", key="IsnerHorobeti2013", year=2013,
         authors="Isner-Horobeti ME, Dufour SP, Blaes C, Lecocq J",
         title="Intramuscular pressure before and after botulinum toxin in chronic exertional compartment syndrome of the leg: a preliminary study",
         journal="Am J Sports Med", doi="10.1177/0363546513499183", slides="26",
         finding="구획내압 유의 감소·통증 소실. 한 다리 총 150 U(50 U씩 3부위)"),

    # ── 10 발 족저근막염 ─────────────────────────────────
    dict(folder="10_발_족저근막염", key="Babcock2005", year=2005,
         authors="Babcock MS, et al.",
         title="Treatment of pain attributed to plantar fasciitis with botulinum toxin A: a short-term, randomized, placebo-controlled, double-blind study",
         journal="Am J Phys Med Rehabil", pmid="16034223", slides="28, 29",
         finding="2점법 — 종골 내측 40 U + 족궁 30 U(총 70 U). 3·8주 유의 개선"),
    dict(folder="10_발_족저근막염", key="Elizondo2013", year=2013,
         authors="Elizondo-Rodríguez J, et al.",
         title="Botulinum toxin A vs corticosteroid vs anesthetic for plantar fasciitis",
         journal="Foot Ankle Int", doi="10.1177/1071100720961093", slides="28",
         finding="6개월 시점 보툴리눔 우수. 근막 파열·지방패드 위축 위험 없음"),
    dict(folder="10_발_족저근막염", key="APMR2021", year=2021,
         authors="—",
         title="Clinical efficacy of botulinum toxin in the treatment of plantar fasciitis: systematic review and meta-analysis of RCTs",
         journal="Arch Phys Med Rehabil", pmid="34688605", slides="28",
         finding="0–6개월 통증 강도 유의 감소"),
    dict(folder="10_발_족저근막염", key="PLOSOne2024", year=2024,
         authors="—",
         title="Therapeutic efficacy and safety of botulinum toxin A injection in plantar fasciitis: a systematic review and meta-analysis",
         journal="PLOS One", pmcid="PMC11651609", slides="05, 28",
         finding="RCT 7편 305명. 1개월 통증 감소, 12개월 기능 개선 유지. 200 U 고용량은 효과 소실"),

    # ── 11 수술후 · 절단 후 신경통 ───────────────────────
    dict(folder="11_수술후_신경통", key="AmputationSR", year=2023,
         authors="—",
         title="Botulinum toxin for residual limb and phantom limb pain after amputation — systematic review",
         journal="—", url="https://pubmed.ncbi.nlm.nih.gov/?term=botulinum+residual+limb+phantom+limb+pain+systematic+review",
         slides="30",
         finding="잔단통(RLP) 6개월 개선, 환상통(PLP)은 변화 없음 — 표적이 말초임을 시사"),
    dict(folder="11_수술후_신경통", key="Neuroma2025", year=2025,
         authors="—",
         title="Perineuromal botulinum toxin injection for post-amputation pain (multicenter)",
         journal="Arch Phys Med Rehabil",
         url="https://pubmed.ncbi.nlm.nih.gov/?term=perineuromal+botulinum+toxin+amputation+pain",
         slides="30", finding="1개월 시점 환상통 감소 보고, 3개월엔 종합치료군이 우수"),

    # ── 12 안전 · 용량 · 면역원성 ────────────────────────
    dict(folder="12_안전_용량_면역원성", key="Hsu2004", year=2004,
         authors="Hsu AT, et al.",
         title="Effect of volume and concentration on the diffusion of botulinum exotoxin A",
         journal="Arch Dermatol", pmid="15545544", slides="34, 35",
         finding="저농도·고용적 = 확산 증가 → 인접근 마비. 정밀 표적은 고농도·소용적"),
    dict(folder="12_안전_용량_면역원성", key="Immunogenicity2022", year=2022,
         authors="—", title="Immunogenicity of botulinum toxin — review",
         journal="Toxins", pmcid="PMC8795657", slides="05, 36",
         finding="이차 무반응 위험인자: 3개월 미만 간격, 고누적용량, 3주 내 보충주사"),
    dict(folder="12_안전_용량_면역원성", key="FDABoxedWarning", year=2009,
         authors="FDA / Allergan", title="BOTOX Product Monograph — Boxed Warning: Distant Spread of Toxin Effect",
         journal="제품 첨부문서",
         url="https://www.botoxone.com/content/dam/botoxone/pdf/BOTOX%20Product%20Monograph%20-%20All%20Indications.pdf",
         slides="33, 36",
         finding="전신쇠약·복시·안검하수·연하곤란·호흡곤란. 주사 수시간~수주 후. 경직 치료(특히 소아) 최고위험"),
]


def link(p):
    """대표 링크 하나."""
    if p.get("pmid"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{p['pmid']}/"
    if p.get("pmcid"):
        return f"https://pmc.ncbi.nlm.nih.gov/articles/{p['pmcid']}/"
    if p.get("doi"):
        return f"https://doi.org/{p['doi']}"
    return p.get("url", "")
