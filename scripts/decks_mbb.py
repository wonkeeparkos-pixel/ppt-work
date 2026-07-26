# -*- coding: utf-8 -*-
"""
하나의 내용 모듈에서 두 개의 발표를 조립한다.

  MBB — 요추 내측지 차단 (진단·예후 도구, 그리고 RFA로 이어지는 경로)
  FJ  — 요추 후관절 관절강내 주사 (치료 목적, 관절 자체를 겨누는 시술)

공유되는 슬라이드(연관통, 적응증 비교, 환자 선정, 한계, 참고문헌)는 양쪽에 들어간다.
섹션 번호와 표지·요약은 덱마다 다르게 붙인다.
"""
import figs_mbb as F
import content_mbb as C

K = C.BY_KEY


def sec(no, title, desc):
    return dict(t='sec', no=no, title=title, desc=desc)


DISCLAIM = ('교육·연구 참고용 문헌고찰<br>개별 환자의 진료 결정은 담당 의사의 판단에 따른다')


# ══════════════════════════════════════════════════════════════════
# 두 덱에만 쓰이는 슬라이드
# ══════════════════════════════════════════════════════════════════
TITLE_MBB = dict(
    t='title',
    eyebrow='LUMBAR MEDIAL BRANCH BLOCK · LITERATURE REVIEW',
    title='요추 내측지 차단',
    en='Lumbar Medial Branch Block (MBB)<br>'
       'Dual innervation · Level-by-level targets · Referred pain · Diagnostic validity<br>'
       'Fluoroscopic and ultrasound technique · Radiofrequency outcomes',
    sub='관절 하나에 신경 둘 — 어느 신경을, 어느 뼈 위에서,<br>'
        '얼마의 용량으로 막을 것인가',
    metaL=DISCLAIM,
    metaR='2026-07 · 1/2<br>PubMed · ASIPP · SIS',
)

TITLE_FJ = dict(
    t='title',
    eyebrow='LUMBAR FACET JOINT INJECTION · LITERATURE REVIEW',
    title='요추 후관절<br>관절강내 주사',
    en='Intra-articular Lumbar Facet (Zygapophysial) Joint Injection<br>'
       'Joint structure and orientation · Recess targeting · Arthrogram and capacity<br>'
       'Target specificity · Randomized evidence · Indications',
    sub='관절강은 1–1.5 mL밖에 담지 못한다.<br>'
        '그 한계가 이 시술의 적응증과 한계를 모두 결정한다',
    metaL=DISCLAIM,
    metaR='2026-07 · 2/2<br>PubMed · ASIPP · SIS',
)

FJ_STRUCTURE = dict(
    t='bigfig', eyebrow='ANATOMY · 관절 구조 (시상 단면)', ebc='j', kickc='j',
    title='후관절은 <b>피막과 두 개의 오목</b>으로 이루어진다',
    kick='어느 오목을 노리고 어느 오목을 피하는지가 이 시술의 전부다.',
    svg=F.facet_capsule(),
    caption='활막관절이며 유리연골 관절면을 <b>약 1 mm 두께의 섬유 피막</b>이 감싼다. '
            '피막하 지방패드와 섬유지방 반월판이 위·아래 극에서 관절면 사이로 들어간다',
    foot='Bogduk N, Clinical Anatomy of the Lumbar Spine and Sacrum · '
         'Engel R, Bogduk N. J Anat 1982 · Kapetanakis S, Gkantsinikoudis N. Folia Morphol 2021;80(4):799–805',
)

FJ_NOCICEPTOR = dict(
    t='split', eyebrow='ANATOMY · 통증 수용', ebc='j', kickc='j',
    title='이 관절은 실제로 <b>아플 수 있는</b> 구조인가',
    kick='조직학적으로는 논쟁이 끝났다 — 침해수용 신경종말이 피막과 활막주름에 있다.',
    items=[
        (0, '인간 하부 요추 후관절의 <b>후내측 피막과 활막주름</b>에서 직경 <b>0.6–12 μm</b>의 '
            '가는 유수신경이 관찰된다. 신경당 1–5개 섬유이며 <b>혈관과 무관하게</b> 주행한다 — '
            '혈관운동성이 아니라 <b>침해수용성</b>이라는 형태학적 근거다.', 'hj'),
        (0, '<b>Substance P</b> 면역형광 신경이 하부 관절 오목의 피막과 활막주름에서 확인된다.'),
        (0, '피막 14개 검체에서 PGP 9.5 양성 12개, CGRP 양성 5개, substance P 자유신경종말 3개, '
            'VIP 5개, CPON 혈관주위신경 9개 — 그리고 <b>황색인대에는 없다</b>.', 'hj'),
        (0, '수술로 채취한 <b>퇴행성</b> 후관절 16개에서도 substance P 면역반응이 확인되었다.'),
        (0, '기계수용체는 경추 피막보다 <b>덜 일관되게</b> 관찰된다 — 흉·요추의 고유수용 기능이 '
            '덜 정교하다는 해석.'),
    ],
    aside=dict(title='전기생리 (토끼)', tone='joint', items=[
        (0, '후관절 부위 단일단위 <b>24개</b> 기록 — 피막 10, 피막–근/건 경계 12, 황색인대 2'),
        (0, '전도속도: group III(2.5–20 m/s) <b>15개</b> · group IV 2개 · 20 m/s 초과 7개'),
        (0, 'von Frey 역치 6.0 g 초과(고역치=침해성) <b>7개</b>', 'hj'),
        (-1, ''),
        (0, '<b>종 주의</b> — 토끼 자료다. 사람에 그대로 옮기지 않는다.', 'hr_'),
    ]),
    foot='Giles LGF, Taylor JR. Br J Rheumatol 1987 (PMID 2435355) / Acta Orthop Scand 1987 (PMID 2437759) · '
         'Giles LGF, Harvey AR. Br J Rheumatol 1987 (PMID 2444304) · Ashton IK et al. J Orthop Res 1992 '
         '(PMID 1530799) · Beaman DN et al. Spine 1993 · Yamashita T et al. JBJS Am 1990 (PMID 2365719) · '
         'McLain RF, Pickar JG. Spine 1998',
)

SUMMARY_MBB = dict(
    t='key', eyebrow='SUMMARY · MEDIAL BRANCH BLOCK',
    title='내측지 차단 — 여덟 문장',
    msgs=[
        ('이중 지배', '관절 하나에 신경 둘. <b>L4–5 = L3 + L4 내측지</b>. 표적 뼈는 신경 번호보다 한 칸 아래 — '
                      '신경으로 말하고 뼈로 가리켜라.'),
        ('표적', 'L1–L4는 <b>SAP–TP 접합부의 홈</b>(절흔 위, 유두돌기 외측). L5는 내측지가 아니라 '
                 '<b>후지 본간</b>을 천골익 × S1 SAP 접합부에서.'),
        ('연관통', '요부·둔부·대전자·외측/후방 대퇴·서혜부 <b>6구역</b>. 겹침이 커서 '
                   '<b>지도로 레벨을 특정할 수 없다</b> — 경추와 정반대다.'),
        ('선별 불가', '병력·진찰·영상 어느 것도 양성 차단을 예측하지 못한다(Revel 92% → Laslett &lt;17%). '
                      '단일 차단 위양성 <b>38%</b>, 위약 반응 24%.'),
        ('용량·확인', '<b>0.25 mL</b>는 표적에 머물고 <b>0.5 mL</b>는 인접 레벨·경막외강(16%)까지. '
                      '흡인 민감도 <b>34%</b> — 실시간 투시 조영이 최소 기준.'),
        ('스테로이드', '<b>진단 차단에는 넣지 않는다.</b> 마취제 지속시간이라는 판정 근거가 무너진다.'),
        ('RFA', '선정이 맞아도 병변이 신경을 <b>완전히 잡는 것은 42%</b>. 전극은 평행하게, 각도는 더 미측으로, '
                '표적은 복측으로.'),
        ('열린 질문', '차단 <b>몇 번</b>, 역치 <b>50%인가 80%인가</b> — SIS와 국제 합의가 다르고 '
                      'MINT 논쟁의 핵심도 이것이다.'),
    ],
    foot='각 문장의 출처는 해당 슬라이드에 표기',
)

SUMMARY_FJ = dict(
    t='key', eyebrow='SUMMARY · FACET JOINT INJECTION',
    title='관절강내 주사 — 여덟 문장',
    msgs=[
        ('구조', '유리연골 관절면 + <b>≈1 mm 섬유 피막</b> + 상·하 두 개의 오목. '
                 '반월판과 지방패드가 관절면 사이로 들어간다.', 'j'),
        ('방향', '관절면은 미측으로 갈수록 <b>관상면</b>에 가까워지고, 축상면에서 <b>C자로 굽어</b> 있다. '
                 '투시로 열리는 것은 뒤쪽 부분뿐이다.', 'j'),
        ('표적', '관절선이 아니라 <b>하부 오목</b>. 상부 오목은 경막외강에 인접해 피한다.', 'j'),
        ('증거', '<b>관절조영상이 유일한 증거</b>다. 조영제 0.1–0.3 mL에서 위아래 오목이 부풀어야 한다. '
                 '피막을 뚫는 느낌은 퇴행 관절에서 없을 수 있다.', 'j'),
        ('용적', '<b>1–1.5 mL</b>. 넘기면 피막이 터지고 경막외강·척추간공·근육으로 샌다.', 'j'),
        ('특이도', '실측에서 환자의 <b>64.6%</b>, 시술의 <b>49.5%</b>에서 경막외 확산. '
                   '그래서 <b>진단 도구가 아니다</b>.', 'j'),
        ('근거', '고전 무작위 시험은 대체로 음성이나 <b>선정이 모두 부적절</b>했다. FACTS에서 '
                 '관절강내 51% vs 내측지 56% — 둘은 구별되지 않았다.', 'j'),
        ('자리', '진단은 내측지 차단이 맡는다. 관절강내 주사는 <b>치료</b>와 '
                 '<b>낭종·삼출·배양</b>이라는 특수 적응에서 제 몫을 한다.', 'j'),
    ],
    foot='각 문장의 출처는 해당 슬라이드에 표기',
)


def _refs(prefix):
    """참고문헌 슬라이드의 eyebrow만 덱에 맞게 갈아끼운다."""
    out = []
    keys = ['ref1', 'ref2', 'ref3', 'ref4', 'ref5']
    for i, k in enumerate(keys, 1):
        s = dict(K[k])
        s['eyebrow'] = f'REFERENCES · {i}/{len(keys)}'
        s['foot'] = (s['foot'] + f' · 두 발표({prefix})가 같은 문헌 목록을 공유한다')
        out.append(s)
    return out


# ══════════════════════════════════════════════════════════════════
# 덱 1 — 내측지 차단
# ══════════════════════════════════════════════════════════════════
MBB = [
    TITLE_MBB,
    sec('01', '해부가 술기를 결정한다',
        '내측지 차단이 재현 가능한 시술인 이유는 단 하나 — 신경이 아주 짧은 구간 동안 '
        '뼈에 고정되어 있기 때문이다. 그 구간이 곧 표적이다.'),
    K['anat_posterior'], K['anat_mapping'], K['anat_naming'], K['anat_mal'], K['anat_l5'],

    sec('02', '연관통은 어디까지 가는가',
        '그리고 더 중요한 질문 — 그 지도로 책임 레벨을 고를 수 있는가. '
        '세 개의 독립된 유발 연구가 같은 답을 내놓았다.'),
    K['ref_zones'], K['ref_table'], K['ref_controversy'], K['ref_mechanism'],
    K['ref_cervical'], K['ref_predictors'],

    sec('03', '차단은 무엇을 증명하는가',
        '병력도 진찰도 예측하지 못한다면 남는 것은 차단뿐이다. '
        '그런데 그 차단 자체가 절반 가까이 틀린다.'),
    K['dx_prevalence'], K['dx_falsepos'], K['dx_threshold'], K['dx_algorithm'], K['dx_facts'],

    sec('04', '정확한 주사',
        '표적은 뼈의 한 지점이다. 영상 각도, 바늘 끝의 위치, 그리고 주입량 — '
        '이 셋이 어긋나면 검사 자체가 무효가 된다.'),
    K['tech_target'], K['tech_carm'], K['tech_proc1'], K['tech_proc2'],
    K['tech_depth'], K['tech_volume'], K['tech_vascular'], K['tech_us'], K['tech_us_fig'],

    sec('05', '효과는 어디까지 증명됐나',
        '진단이 맞아도 시술이 실패할 수 있다. 그리고 그 실패의 상당 부분은 '
        '환자 선정이 아니라 바늘이 신경을 못 잡아서 생긴다.'),
    K['out_rfa_fail'], K['out_mint'], K['out_prognosis'],

    sec('06', '안전성 — 무엇이 실제로 측정되었나',
        '이 시술의 위해는 대부분 “합병증”이 아니라 주입액이 가면 안 될 곳에 가는 것으로 '
        '나타난다. 그것은 실측되어 있다.'),
    K['safe_table'], K['safe_multifidus'],

    sec('07', '그래서 누구에게 쓰는가',
        '관절강내 주사와는 목적이 다르다. 하나는 질문을 던지는 도구이고, '
        '다른 하나는 답이 나온 뒤의 처치다.'),
    K['ind_selection'], K['ind_compare'],

    SUMMARY_MBB, K['limitations'],
] + _refs('내측지 차단 · 관절강내 주사')


# ══════════════════════════════════════════════════════════════════
# 덱 2 — 후관절 관절강내 주사
# ══════════════════════════════════════════════════════════════════
FJ = [
    TITLE_FJ,
    sec('01', '관절이라는 표적',
        '내측지 차단이 신경을 겨눈다면, 이 시술은 관절강 자체를 겨눈다. '
        '피막·오목·용적이라는 세 가지 사실이 나머지를 전부 결정한다.'),
    FJ_STRUCTURE, FJ_NOCICEPTOR, K['ia_orientation'],

    sec('02', '이 관절은 어디로 아픔을 보내는가',
        '관절을 조영제로 팽창시켜 유발한 통증의 분포 — 그리고 그 지도로 '
        '책임 레벨을 고를 수 없는 이유.'),
    K['ref_zones'], K['ref_table'], K['ref_mechanism'], K['ref_predictors'],

    sec('03', '정확한 주사',
        '관절선이 아니라 오목을 노린다. 그리고 관절조영상이 나오기 전까지는 '
        '관절 안에 있다고 말할 수 없다.'),
    K['ia_technique'], K['ia_specificity'],

    sec('04', '무엇이 증명되었나',
        '고전 무작위 시험은 대체로 음성이다. 다만 그 시험들의 환자 선정이 '
        '오늘 기준으로는 모두 부적절했다는 점을 함께 읽어야 한다.'),
    K['ia_evidence'], K['dx_facts'], K['dx_prevalence'],

    sec('05', '그래서 언제 쓰는가',
        '진단은 내측지 차단이 맡는다. 그렇다면 관절강내 주사의 자리는 어디인가.'),
    K['ind_compare'], K['ind_selection'],

    SUMMARY_FJ, K['limitations'],
] + _refs('관절강내 주사 · 내측지 차단')


DECKS = {
    'mbb': ('요추 내측지 차단 문헌고찰', MBB),
    'fj': ('요추 후관절 관절강내 주사 문헌고찰', FJ),
}
