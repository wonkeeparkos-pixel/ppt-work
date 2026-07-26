# -*- coding: utf-8 -*-
"""
요추 내측지차단(MBB) · 후관절차단(FJB) 문헌고찰 발표 — 슬라이드 내용.

원칙
  · 모든 수치에는 출처를 붙인다. 확인하지 못한 수치는 슬라이드에 올리지 않는다.
  · 문헌이 서로 어긋나면 한쪽을 고르지 않고 양쪽을 함께 적는다.
  · 신경(MBB) = 금색, 관절(관절강내) = 청색. 색이 곧 정보다.
"""
import figs_mbb as F

SERIES = "요추 후관절 중재술 문헌고찰"

SLIDES = []


def add(**kw):
    SLIDES.append(kw)


# ══════════════════════════════════════════════ 표지
add(
    t='title',
    eyebrow='LUMBAR FACET INTERVENTIONS · LITERATURE REVIEW',
    title='내측지 차단과 후관절 차단',
    en='Lumbar Medial Branch Block vs. Intra-articular Facet Joint Block<br>'
       'Level-by-level effect · Referred pain coverage · Indications · Accurate needle placement',
    sub='레벨별 효과와 연관통 커버 범위, 각 주사의 적응증,<br>그리고 정확한 주사를 위한 표적 위치',
    metaL='교육·연구 참고용 문헌고찰<br>개별 환자의 진료 결정은 담당 의사의 판단에 따른다',
    metaR='2026-07<br>PubMed · ASIPP · SIS',
)

# ══════════════════════════════════════════════ 01 해부와 표적
add(
    t='sec', no='01', title='해부가 술기를 결정한다',
    desc='내측지 차단이 재현 가능한 시술인 이유는 단 하나 — 신경이 아주 짧은 구간 동안 '
         '뼈에 고정되어 있기 때문이다. 그 구간이 곧 표적이다.',
)

add(
    t='figure', eyebrow='ANATOMY · 후방 시야',
    title='내측지는 <b>한 레벨 아래</b> 척추의 SAP–TP 접합부를 넘는다',
    kick='Ln 내측지의 표적은 Ln 척추가 아니라 Ln+1 척추의 횡돌기·상관절돌기 접합부다.',
    panels=[
        dict(pt='후방 시야 (posterior)', svg=F.posterior_spine(), tone='',
             pl='내측지는 척추간공을 나와 <b>상관절돌기 외측 경부</b>를 돌아 '
                '<b>횡돌기 기저부 상연</b>의 홈으로 들어간다'),
        dict(pt='관절 1개 = 신경 2개', svg=F.dual_bracket(), tone='n',
             pl='관절 하나를 마취하려면 <b>연속한 두 레벨</b>에서 두 번 주사해야 한다'),
    ],
    caption='Bogduk & Long, J Neurosurg 1979 · Bogduk, Spine 1983 · Bogduk·Wilson·Tynan, J Anat 1982',
    foot='이중 지배(dual innervation)는 이 발표 전체의 전제다',
    rail='all',
)

add(
    t='table', eyebrow='MAPPING · 이중 지배',
    title='관절별 차단해야 할 신경과 <b>바늘이 놓일 뼈</b>',
    kick='신경 이름과 바늘 위치는 한 칸씩 어긋난다 — 여기서 대부분의 혼선이 생긴다.',
    headers=['후관절', ('차단할 신경 ①', 'nerve'), ('바늘 위치 ①', 'joint'),
             ('차단할 신경 ②', 'nerve'), ('바늘 위치 ②', 'joint')],
    rows=[
        ['L1–2', 'T12 내측지', 'L1 TP·SAP 접합부', 'L1 내측지', 'L2 TP·SAP 접합부'],
        ['L2–3', 'L1 내측지', 'L2 TP·SAP 접합부', 'L2 내측지', 'L3 TP·SAP 접합부'],
        ['L3–4', 'L2 내측지', 'L3 TP·SAP 접합부', 'L3 내측지', 'L4 TP·SAP 접합부'],
        ['L4–5', 'L3 내측지', 'L4 TP·SAP 접합부', 'L4 내측지', 'L5 TP·SAP 접합부'],
        ['L5–S1', 'L4 내측지', 'L5 TP·SAP 접합부', '<b>L5 후지</b>', '<b>천골익 × S1 SAP</b>'],
    ],
    hlrows={3: 'hl', 4: 'hl'},
    note='L4–5·L5–S1이 가장 흔한 증상 레벨이므로 <b>L3 내측지 · L4 내측지 · L5 후지</b> 3점 차단이 '
         '두 관절을 함께 덮는 표준 조합이 된다. · T12의 L1–2 기여는 여러 문헌에 기술되나 '
         '1차 해부 논문으로 확증하지 못했다 — 잠정으로 본다.',
    foot='Bogduk N. The innervation of the lumbar spine. Spine 1983;8(3):286–293 (PMID 6226119)',
    rail='all',
)

add(
    t='split', eyebrow='PITFALL · 명명법',
    title='“신경으로 말하고, 뼈로 가리켜라”',
    kick='같은 시술을 두 가지 이름으로 부르는 관행이 기록·청구 오류를 만든다.',
    items=[
        (0, '<b>해부학적 명명</b> — 내측지는 <b>모신경(분지한 척수신경)</b>의 번호를 따른다. '
            'L3 내측지는 L3 후지의 가지이며, 주행은 <b>L4</b> 횡돌기·상관절돌기 접합부다.'),
        (0, '<b>시술 명명</b> — 투시 문헌·차트에서는 <b>바늘이 얹힌 척추</b>로 부른다. '
            'L4 횡돌기 위의 바늘을 “L4 MBB”로 기록하지만 마취되는 신경은 <b>L3 내측지</b>다.'),
        (0, '두 관행이 공존하므로, 기록에는 <b>레벨 번호가 아니라 표적 뼈</b>를 함께 적는 편이 안전하다.', 'hi'),
        (-1, ''),
        (0, '실무 규칙 — <b>“L4–5 관절을 차단한다”</b>고 말하고, '
            '<b>“L4 횡돌기와 L5 횡돌기에 각각 놓는다”</b>고 실행한다.', 'hi'),
    ],
    aside=dict(title='표적 구간은 얼마나 짧은가', tone='nerve', stat=[
        ('3.4–3.6 mm', 'L1–L4 후지 분지점 ~ 횡돌기 기저 상연'),
        ('1.9 mm', 'L5 — 유의하게 더 짧다'),
        ('57 → 82 %', 'SAP 외측 경부의 골막 접촉 비율 (L1→L5)'),
    ]),
    note='Shuang F et al. Medicine (Baltimore) 2015;94(52), PMC5291620 · '
         'Tran J et al. Interv Pain Med 2024;3(2):100414',
    foot='Bogduk N. Spine 1983;8(3):286–293 · 시술 명명 관행은 투시 술기 문헌·코딩 자료에 기술',
)

add(
    t='split', eyebrow='ANATOMY · 왜 차단이 재현되는가',
    title='유두–부돌기 인대(MAL)가 신경을 뼈에 <b>가둔다</b>',
    kick='이 골섬유터널이 “경피적으로 정확히 자극·마취·파괴할 수 있다”는 근거 그 자체다.',
    items=[
        (0, 'MAL은 같은 척추의 <b>유두돌기(mamillary process)</b>와 <b>부돌기(accessory process)</b>를 '
            '잇는다. 한 뼈의 두 점을 잇기에 엄밀한 의미의 인대는 아니다.'),
        (0, '이 인대가 SAP–TP 홈을 덮어 <b>골섬유터널</b>을 만들고, 내측지는 그 안에서 '
            '뼈와 <b>일정한 관계</b>를 유지한다 — Bogduk의 표현 그대로 "이 항상성이 정확한 경피적 접근을 가능하게 한다".', 'hi'),
        (0, 'MAL <b>골화</b>는 내측지 포착성 신경병증의 원인으로 지목되며, 캐뉼라를 의도한 골막면에서 '
            '밀어내 <b>술기 실패</b>를 만들 수 있다.', 'hr_'),
        (1, '골화 빈도는 문헌마다 크게 다르다 — Bogduk 1981 "하부 요추의 10% 이상", '
            'Maigne 1991 L5 좌 26%·우 13.5%, 2024년 건조골 연구 72.7%.'),
        (0, '터널 원위부에서 후지는 이미 2–4갈래로 갈라진다 → <b>복측(전방)에서 잡아야</b> '
            '갈라지기 전 본간을 포착한다.', 'hi'),
    ],
    aside=dict(title='분지 시점', tone='nerve', items=[
        (0, 'SAP 외측 경부에서 후지는 2갈래 <b>51.1%</b> · 3갈래 <b>45.6%</b> · 4갈래 <b>3.3%</b>'),
        (0, '경부 <b>전방 1/4</b> 지점에서는 45.6%가 아직 갈라지지 않음'),
        (0, '경부 <b>중간</b>에서는 3.3%만 미분지 — 사실상 모두 갈라져 있다', 'hr_'),
        (-1, ''),
        (0, '→ 표적은 경부의 <b>전방(복측)</b>이 유리하다', 'hi'),
    ]),
    foot='Bogduk N. Spine 1981;6(2):162–167 (PMID 6456553) · Tran J et al. Interv Pain Med 2024',
)

add(
    t='figure', eyebrow='L5 · 다른 신경, 다른 표적',
    title='L5는 <b>내측지가 아니라 후지 본간</b>을 막는다',
    kick='L5 내측지는 짧고 변이가 많아, 임상 표적은 천골익과 S1 상관절돌기가 만나는 한 점이다.',
    panels=[
        dict(pt='L5 후지 표적', svg=F.l5_dorsal_ramus(), tone='n',
             pl='천골익과 <b>S1 상관절돌기 기시부</b>가 만드는 홈 — 여기서 후지 본간을 막는다'),
        dict(pt='L5가 다른 이유', svg=F.scotty_dog(), tone='',
             pl='L1–L4는 사위상 “스코티독”에서 <b>귀 뿌리~눈</b> 부위가 표적. L5는 장골능 때문에 '
                '사위상이 덜 유용해 <b>정면상</b>에서 잡는다'),
    ],
    caption='L5 후지는 L1–L4보다 <b>길고</b>, <b>외측지가 없으며</b>(L5에는 장늑근 부착이 없다), '
            '분지점이 횡돌기 기저 상연에서 <b>1.9 mm</b>로 절반 수준이다',
    foot='Dreyfuss P et al. Spine 1997;22(8):895–902 (PMID 9127924) · Bogduk·Wilson·Tynan, J Anat 1982',
    rail=['L5-S1'],
)

# ══════════════════════════════════════════════ 02 연관통
add(
    t='sec', no='02', title='연관통은 어디까지 가는가',
    desc='그리고 더 중요한 질문 — 그 지도로 책임 레벨을 고를 수 있는가. '
         '세 개의 독립된 유발 연구가 같은 답을 내놓았다.',
)

add(
    t='figure', eyebrow='REFERRED PAIN · Fukui 1997',
    title='요추 후관절 연관통의 <b>표준 지도</b>',
    kick='48명 · 관절 71개 · 내측지 91개. 단 6개 구역으로만 채점되었다.',
    panels=[
        dict(pt='Fukui가 사용한 6개 구역', svg=F.fukui_zones("fz"), tone='n',
             pl='후면 5구역 + 전면 서혜부 1구역'),
    ],
    caption='이 연구에는 <b>옆구리·장골능·무릎·무릎 아래 구역이 존재하지 않는다</b> — '
            '따라서 Fukui를 “무릎 아래로 몇 % 간다”의 근거로 인용할 수 없다',
    foot='Fukui S, Ohseto K, Shiotani M, et al. Clin J Pain 1997;13(4):303–307 (PMID 9430810)',
    rail='all',
)

add(
    t='table', eyebrow='REFERRED PAIN · 레벨별',
    title='관절 확장(joint distension) 시 레벨별 연관통 — <b>빈도 순</b>',
    kick='원위 연관통은 L3–4부터 나타나고, L1–2는 요부에 머문다.',
    dense=True,
    headers=['후관절', '요부', '둔부', '외측 대퇴', '후방 대퇴', '대전자부', '서혜부'],
    rows=[
        ['L1–2', '<b>전부</b>', '—', '—', '—', '—', '—'],
        ['L2–3', '<b>항상</b>', '드물게', '드물게', '—', '드물게', '—'],
        ['L3–4', '<b>기본</b>', '① 가장 흔함', '②', '③', '④', '⑤ 가장 드묾'],
        ['L4–5', '<b>기본</b>', '① 가장 흔함', '②', '④', '③', '⑤ 가장 드묾'],
        ['L5–S1', '<b>기본</b>', '① 가장 흔함', '②', '③', '④', '⑤ 가장 드묾'],
    ],
    hlrows={2: 'hl', 3: 'hl', 4: 'hl'},
    note='① ~ ⑤는 논문이 제시한 <b>빈도 순위</b>다. L3–4 · L4–5 · L5–S1 세 레벨은 '
         '<b>똑같은 5개 구역</b>을 때리고, 오직 대전자부와 후방 대퇴의 순위 하나만 다르다. '
         '이 한 칸의 차이로 레벨을 특정할 수는 없다. · L5–S1의 3·4위 순서는 이차 문헌 간 기술이 엇갈려 '
         '원문 확인이 필요하다.',
    foot='Fukui S et al. Clin J Pain 1997;13(4):303–307 (PMID 9430810)',
    rail='all',
)

add(
    t='cmp', eyebrow='CONTROVERSY · 관절 vs 신경',
    title='내측지를 자극하면 <b>더 멀리</b> 가는가, <b>덜</b> 가는가',
    kick='두 유발 연구가 정면으로 어긋난다 — 정리된 척 넘기지 말고 그대로 가르쳐야 한다.',
    cards=[
        dict(tone='n', name='Marks 1989', en='Pain 39(1):37–40',
             sl='신경이 관절보다 <b>더 멀리</b> 보낸다',
             items=[
                 (0, '138명 · <b>385회</b> 관찰'),
                 (0, '“관절을 지배하는 신경이 관절 자체보다 원위 연관통을 '
                     '<b>유의하게 더 자주</b> 일으켰다”'),
                 (0, '일관된 분절·경절(sclerotome) 패턴은 <b>없었다</b>'),
                 (0, '서혜부 통증은 <b>L2에서 L5까지</b> 어디서든 유발됨', 'hr_'),
             ],
             cf='화학적 침윤 — 인접 구조로의 확산 가능성'),
        dict(tone='j', name='Fukui 1997', en='Clin J Pain 13(4):303–307',
             sl='신경 자극은 <b>요부 우세</b>, 원위는 드물다',
             items=[
                 (0, 'L1–L4 내측지 자극 시 <b>주로 요부</b>'),
                 (0, '둔부·대전자·서혜부·외측 대퇴는 <b>“드물게”</b>'),
                 (0, '후방 대퇴는 <b>L4에서만</b> 나타남'),
                 (0, 'L5 내측지/후지의 구역은 확인 실패 — 지어내지 않는다', 'hj'),
             ],
             cf='RF 시술 중 최소역치 전기자극'),
    ],
    foot='Windsor RE et al. Pain Physician 2002;5(4):347–353은 방향을 명시하지 않은 채 '
         '“관절 주사 지도와 다르다”고만 결론했다',
)

add(
    t='bullets', eyebrow='MECHANISM · 왜 겹치는가',
    title='지도가 겹치는 것은 연구가 엉성해서가 아니다',
    kick='겹침은 기전상 <b>예정된 결과</b>다. 세 층위에서 설명된다.',
    items=[
        (0, '<b>① 수렴(convergence)</b> — 척수·시상의 공통 뉴런이 여러 말초에서 입력을 받는다. '
            '뇌는 출처를 특정하지 못하고 <b>그 뉴런이 담당하는 영역 전체</b>에 통증을 배정한다.'),
        (0, '<b>② 이중 지배</b> — 관절 하나가 <b>두 분절</b>의 후각으로 동시에 침해 입력을 보낸다. '
            '따라서 한 관절의 연관통 영역은 애초에 <b>두 분절 영역의 합집합</b>이다. '
            '인접 관절끼리 지도가 겹치는 것은 구조상 필연이다.', 'hi'),
        (0, '<b>③ 경절성(sclerotomal) 배열</b> — 심부 체성통은 분절을 따르되 '
            '<b>피부분절(dermatome)과 다르고 서로 크게 겹친다</b>. Feinstein 1954는 후두–천골 전 레벨 '
            '방척추 6% 식염수 주입으로 이를 보였고, 교감·체성 신경총 차단으로도 연관통이 사라지지 않아 '
            '<b>척수 통합 기전</b>임을 시사했다.'),
        (-1, ''),
        (0, '→ 크고 흐릿하게 겹치는 지도는 <b>기전이 내놓는 정답</b>이지 잡음이 아니다.', 'hi'),
    ],
    foot='Bogduk N. Pain 2009;147(1–3):17–19 · Kellgren JH. Clin Sci 1939 · Feinstein B et al. '
         'JBJS Am 1954;36(5):981–997 · ISIS Practice Guidelines, 2nd ed. 2013:559–600',
)

add(
    t='split', eyebrow='EVIDENCE · 지도의 한계',
    title='경추는 되고 요추는 안 된다',
    kick='같은 연구자, 같은 방법, 반대 결론 — 이 대조가 요추 지도의 한계를 가장 깔끔하게 보여준다.',
    items=[
        (0, '<b>경추</b> — Dwyer·Aprill·Bogduk(Spine 1990)은 C2–3~C6–7 각 관절이 '
            '“<b>임상적으로 구별되는 특징적 패턴</b>”을 만든다고 보고했고, 이 지도는 '
            '증상 관절의 <b>분절 위치 결정에 유용</b>하다고 결론했다.', 'hj'),
        (0, '<b>요추</b> — Fukui(1997) 저자들의 결론은 정반대다: 각 레벨의 분포가 '
            '“<b>서로 비슷했고, 레벨 간 연관통의 겹침이 상당했다</b>”.', 'hi'),
        (0, 'Marks 1989(385회 관찰) “일관된 분절·경절 패턴 없음”, '
            'McCall 1979 “상부와 하부 요추 사이 연관 영역이 겹친다” — '
            '<b>독립된 세 데이터셋이 같은 부정적 결론</b>에 도달했다.'),
        (-1, ''),
        (0, '<b>실무 결론</b> — 연관통 지도는 “후관절이 원인일 수 있다”까지만 말해준다. '
            '<b>어느 레벨인지는 말해주지 않는다.</b>', 'hi'),
    ],
    aside=dict(title='흔한 오해 교정', tone='crit', items=[
        (0, '“서혜부 통증 = 상부 요추”', 'hr_'),
        (1, 'Marks: 서혜부는 <b>L2~L5</b> 어디서든 유발. Fukui: L3–4·L4–5·L5–S1 모두의 구역.'),
        (-1, ''),
        (0, '“무릎 아래로 가면 후관절이 아니다”', 'hr_'),
        (1, '드물지만 <b>발까지</b> 보고된다. 다만 신뢰할 만한 <b>비율 수치는 찾지 못했다</b> — '
            '수치를 인용하려면 원문을 볼 것.'),
    ]),
    foot='Dwyer A, Aprill C, Bogduk N. Spine 1990;15(6):453–457 (PMID 2402682) · '
         'Fukui S et al. Clin J Pain 1997 · Marks R. Pain 1989 · McCall IW et al. Spine 1979;4(5):441–446',
)

add(
    t='table', eyebrow='EVIDENCE · 임상 예측인자',
    title='병력과 진찰로 후관절 통증을 골라낼 수 있는가',
    kick='한 번 성공했고, 재현에 실패했다. 그 뒤로는 계속 음성이다.',
    dense=True,
    headers=['연구', '설계', '결과', '해석'],
    rows=[
        ['Jackson 1988', '390명 · 변수 127개', '반응을 예측하는 임상 지표 <b>없음</b>',
         '무릎 아래 통증 없음이 연관되나 유발연구와 충돌'],
        ['Schwarzer 1994', '176명 · 확인차단',
         'Fairbank · Helbig&Lee 기준 <b>모두 실패</b>', '1990년 이전 “facet syndrome” 체크리스트의 사망선고'],
        ['Schwarzer 1995', '57명 · 식염수 대조', '유병률 <b>40%</b> (95% CI 27–53)',
         '“어떤 병력·진찰 소견도 구별하지 못했다”'],
        ['Revel 1998', '80명 · 무작위 대조', '7항목 중 5개 → 민감도 <b>92%</b>·특이도 <b>80%</b>',
         '유일한 양성 모델. 단 <b>연관통 패턴은 항목에 없다</b>'],
        ['Laslett 2004', 'Revel 기준 외부검증', '민감도 <b>&lt;17%</b>·특이도 90–93%',
         '“선별검사로 부적합” — 재현 실패'],
        ['Maas 2017', '체계적 문헌고찰', '근거 <b>불충분</b>',
         '“병력·진찰로 진단적 차단의 필요를 줄일 수 없다”'],
    ],
    hlrows={3: 'hl', 4: 'hlj'},
    note='Revel의 7항목은 “<b>기침·굴곡·굴곡에서 기립·신전·신전회전으로 악화되지 않고</b>, '
         '누우면 잘 완화되며, 65세 초과”다 — 즉 <b>기계적으로 유발되지 않는 통증</b>을 고르는 모델이지 '
         '연관통 패턴을 고르는 모델이 아니다.',
    foot='Jackson RP et al. Spine 1988 · Schwarzer AC et al. J Spinal Disord 1994 / Ann Rheum Dis 1995 · '
         'Revel M et al. Spine 1998 (PMID 9779530) · Laslett M et al. BMC Musculoskelet Disord 2004 · '
         'Maas ET et al. Eur J Pain 2017 (PMID 27723170)',
)


# ══════════════════════════════════════════════ 03 진단적 차단
add(
    t='sec', no='03', title='차단은 무엇을 증명하는가',
    desc='병력도 진찰도 예측하지 못한다면 남는 것은 차단뿐이다. '
         '그런데 그 차단 자체가 절반 가까이 틀린다.',
)

add(
    t='table', eyebrow='PREVALENCE · 유병률',
    title='만성 요통에서 후관절이 원인인 비율',
    kick='연구마다 15%에서 52%까지 — 대상 집단과 판정 기준이 다르기 때문이다.',
    dense=True,
    headers=['연구 · 집단', '설계', '유병률', '위양성률'],
    rows=[
        ['Schwarzer 1994 · 의뢰환자 176명', '이중 차단 (리도카인→부피바카인)', '<b>15%</b>', '<b>38%</b> · PPV 31%'],
        ['Schwarzer 1995 · 호주 만성요통 57명', '관절강내 + 식염수 대조', '<b>40%</b> (27–53)', '—'],
        ['Manchikanti 2001 · 65세 이상', '대조 비교 차단', '<b>52%</b> (성인 30%)', '33% (성인 26%)'],
        ['Manchikanti 2007 · 수술 후 117명', '대조 비교 차단', '<b>16%</b>', '<b>49%</b>'],
        ['Manchikanti 2008 · 연령별 424명', '대조 비교 차단', '18% → <b>44%</b> (51–60세)', '—'],
        ['DePalma 2011 · 척추센터 170례', '이중 차단 + 추간판조영', '<b>31%</b> (추간판 42% · 천장 18%)', '—'],
        ['ASIPP 종설 · 이중차단 17편', '통합', '<b>16–41%</b>', '<b>25–44%</b>'],
    ],
    hlrows={0: 'hl', 3: 'hl'},
    note='나이가 들수록 올라가고(대략 70세까지), <b>수술 후 집단은 유병률이 낮은데 위양성률이 가장 높다</b>. '
         'ASIPP 본문에도 27–40%/27–47%, 34–48%/42–58% 등 서로 다른 범위가 함께 인용된다 — 한 숫자로 외우지 말 것.',
    foot='Schwarzer AC et al. Pain 1994;58(2):195–200 (PMID 7816487) · Manchikanti L et al. '
         'Arch Phys Med Rehabil 2007 (PMID 17398245) / Pain Physician 2008 (PMID 18196171) · '
         'DePalma MJ et al. Pain Med 2011 (PMID 21266006)',
)

add(
    t='split', eyebrow='FALSE POSITIVE · 왜 한 번으로는 안 되나',
    title='단일 차단이 과잉진단하는 네 가지 이유',
    kick='그리고 이 중 둘은 비교 차단(리도카인→부피바카인)으로도 잡히지 않는다.',
    items=[
        (0, '<b>① 위약 반응</b> — FACTS 무작위 시험의 식염수군에서 3개월 시점 반응자가 '
            '<b>24%</b>였다. 비교 차단은 이걸 걸러내지 못한다.', 'hr_'),
        (0, '<b>② 비표적 확산</b> — 0.5 mL 조영제가 CT에서 경막외강·척추간공으로 퍼진 경우가 '
            '<b>16%</b>. 사체에서는 인접 레벨 내측지까지 마취된다. 통증이 줄어도 그게 표적 신경 때문인지 알 수 없다.', 'hr_'),
        (0, '<b>③ 진정·전신 흡수</b> — 과다한 피부 국소마취(피부 분지 마취)와 부적절한 진정.'),
        (0, '<b>④ 평균으로의 회귀와 기대 편향</b> — ①과 함께 <b>비교 차단으로 통제되지 않는다</b>. '
            '진짜 대조는 위약(식염수) 팔뿐이다.', 'hr_'),
        (-1, ''),
        (0, '그래서 이중·비교 차단은 <b>완전한 해법이 아니라 실현 가능한 차선</b>이다.', 'hi'),
    ],
    aside=dict(title='물리적 상한', tone='crit', stat=[
        ('89%', 'Kaplan 1998 — 완벽한 MBB도 관절 마취 성공은 8/9'),
        ('~11%', '이상 지배로 인한 구조적 위음성 (n=9, 불확실성 큼)'),
        ('24%', 'FACTS 식염수군 3개월 반응률'),
    ]),
    foot='Cohen SP et al. Anesthesiology 2018;129(3):517–535 (PMID 29847426) · '
         'Dreyfuss P et al. Spine 1997;22(8):895–902 · Wahezi SE et al. PM R 2018 (PMID 29174073) · '
         'Kaplan M et al. Spine 1998;23(17):1847–1852 (PMID 9762741)',
)

add(
    t='cmp', eyebrow='CONTROVERSY · 판정 역치',
    title='50%인가 80%인가 — 가이드라인이 서로 다르다',
    kick='"양성 판정 기준은 통증의학에서 가장 논쟁적인 영역"(Cohen 2020)이라는 문장이 공식 문헌에 있다.',
    cards=[
        dict(tone='n', name='이중 차단 · ≥80%', en='SIS / IPSIS · ASIPP',
             sl='정확도를 산다',
             items=[
                 (0, '두 번 모두 <b>80% 이상</b> 완화 + 이전에 아프던 동작 수행 가능(ASIPP)'),
                 (0, '2년 추적에서 <b>89.5%</b>가 여전히 후관절성 — 50% 기준군은 <b>51%</b>'),
                 (1, '이 두 수치는 이차 요약에서 얻었다. 원문 확인 권장.'),
                 (0, 'RFA 성공률이 가장 높은 선별 방식', 'hi'),
             ],
             cf='대가: 진짜 환자의 절반 가까이를 놓친다'),
        dict(tone='j', name='단일 차단 · ≥50%', en='Cohen 2020 국제 합의',
             sl='접근성과 비용을 산다',
             items=[
                 (0, '<b>한 번</b>의 차단에서 50% 이상이면 RFA로 진행'),
                 (0, '근거는 비용효과 — Cohen 2010 무작위 연구에서 '
                     '<b>차단 없이</b> 바로 RFA가 가장 비용효과적이었다'),
                 (1, '차단 0회군 33%(17/51) vs 1회군 50%(8/16) 성공'),
                 (0, 'Holz & Sehgal 2016: MBB 반응과 RFN 결과 간 <b>상관 없음</b>', 'hj'),
             ],
             cf='대가: 위양성을 안고 시술로 넘어간다'),
    ],
    foot='Cohen SP et al. Reg Anesth Pain Med 2020;45(6):424–467 (PMID 32245841) · '
         'Cohen SP et al. Anesthesiology 2010;113(2):395–405 (PMID 20613471) · '
         'Holz SC, Sehgal N. Pain Physician 2016;19(3):163–172 (PMID 27008290)',
)

add(
    t='bigfig', eyebrow='ALGORITHM · 진단 경로',
    title='표준 경로와, 그 경로가 걸러내는 것',
    svg=F.algorithm(),
    caption='ASIPP는 <b>이중 차단 + 80% 역치</b>를 Level II · 중등도 권고로 제시한다. '
            '반대편에는 "차단 0–1회" 진영이 있고, 양쪽 모두 <b>무작위 근거</b>를 갖고 있다',
    foot='Manchikanti L et al. ASIPP facet joint guidelines. Pain Physician 2020 (PMID 32503359)',
)

add(
    t='split', eyebrow='FACTS · 차단의 성격',
    title='차단은 <b>치료</b>가 아니라 <b>예후 검사</b>다',
    kick='229명 무작위 시험이 이것을 가장 분명하게 보여준다.',
    items=[
        (0, '3개월 시점 <b>평균 통증 점수</b>는 세 군이 다르지 않았다 — '
            '관절강내 3.0±2.0 · 내측지 3.2±2.5 · 대조 3.5±1.9 (<code>P=0.493</code>).', 'hr_'),
        (0, '차이는 <b>반응자 비율</b>에서만 나타났다 — 51% · 56% · 24% (<code>P=0.005</code>).'),
        (0, '저자 결론: <b>후관절 차단은 치료적이지 않다.</b> 높은 반응자 비율은 '
            'RFA 전 <b>예후적 가치</b>가 있다는 가설을 낳을 뿐이다.', 'hi'),
        (-1, ''),
        (0, '관절강내 51% vs 내측지 56% — <b>둘은 통계적으로 구별되지 않았다</b>. '
            'MBB가 선호되는 이유는 효과 크기가 아니라 <b>표적 일치</b>다. '
            'RFA가 태울 바로 그 신경을 시험하기 때문.', 'hi'),
    ],
    aside=dict(title='FACTS 3개월', tone='nerve', stat=[
        ('56%', '내측지 차단 반응자'),
        ('51%', '관절강내 반응자', 'j'),
        ('24%', '식염수 대조 반응자', 'r'),
    ]),
    note='반응 정의: 평균 요통 ≥2점 감소 + 만족도 ≥3/5',
    foot='Cohen SP, Doshi TL, Constantinescu OC, et al. Anesthesiology 2018;129(3):517–535 (PMID 29847426)',
)

# ══════════════════════════════════════════════ 04 술기
add(
    t='sec', no='04', title='정확한 주사',
    desc='표적은 뼈의 한 지점이다. 영상 각도, 바늘 끝의 위치, 그리고 주입량 — '
         '이 셋이 어긋나면 검사 자체가 무효가 된다.',
)

add(
    t='figure', eyebrow='TARGET · L1–L4',
    title='표적점 — 정면상과 사위상에서',
    kick='스코티독의 “눈”은 척추경이다. 눈 자체가 표적이 아니다.',
    panels=[
        dict(pt='정면상 (AP)', svg=F.ap_target(), tone='',
             pl='바늘 끝은 <b>SAP 외측연에 걸치거나 약간 내측</b>, 높이는 <b>횡돌기 상연</b>'),
        dict(pt='사위상 (oblique)', svg=F.scotty_dog(), tone='n',
             pl='표적은 <b>귀(SAP)와 코(TP)가 만나는 곳</b> — 척추경 그림자의 상배측 가장자리, '
                '유두–부돌기 절흔보다 <b>위</b>, 유두돌기보다 <b>외측</b>'),
    ],
    caption='SIS 계열 기술: “표적은 SAP와 TP의 접합부로, 신경이 <b>횡돌기 상연과 유두–부돌기 절흔의 중간</b>을 '
            '건너는 지점”. 종착점은 그 절흔에서의 <b>골 접촉</b>',
    foot='Musculoskeletal Key / Radiology Key, Lumbar Zygapophysial Joint Nerve Injection — Oblique Approach · '
         'Amrhein TJ et al. AJR 2016 (PMID 27276532)',
    rail=['L1-2', 'L2-3', 'L3-4', 'L4-5'],
)

add(
    t='split', eyebrow='C-ARM · 사위 각도',
    title='사위 몇 도인가 — 정해진 답이 없다',
    kick='보고된 값은 10°에서 40°까지. 모든 출처가 동의하는 것은 “숫자가 아니라 영상으로 맞춘다”뿐이다.',
    items=[
        (0, '보고된 값: <b>10–20°</b>(기술 교재) · <b>15°</b>(Wheeless) · '
            '<b>20°</b>(전통적 RFA 접근) · <b>25–35°</b> · 일부는 변곡점이 <b>약 40°</b>에서 나온다고 기술.'),
        (0, '<b>공통 원칙</b> — SAP–TP 변곡점이 뚜렷이 옆모습으로 잡히고 척추경 윤곽이 선명해질 때까지 '
            '<b>환자별로</b> 돌린다. 고정된 각도를 외우는 것이 아니다.', 'hi'),
        (0, '<b>L5는 예외</b> — 장골능이 가린다. 사위를 <b>5–10° AP 쪽으로 되돌리거나</b> '
            'C-arm을 <b>두측(cephalad)</b>으로 기울여 장골능을 미측으로 밀어낸다.', 'hr_'),
        (0, '레벨별(L1 vs L2 vs …) 권장 각도를 명시한 1차 문헌은 <b>찾지 못했다</b> — '
            '검증된 레벨 특이 규칙은 위의 L5 규칙 하나뿐이다.'),
        (0, '“종판 맞추기(squaring)”는 보편적 관행이나, 그 근거와 목표 각도를 명시한 '
            '1차 인용은 확인하지 못했다 — <b>관행으로 가르칠 것</b>.'),
    ],
    aside=dict(title='AP 우선이 낫다는 근거', tone='joint', stat=[
        ('66 vs 109', 'mGy — AP vs 사위 평균 방사선량', 'j'),
        ('28 vs 46', '초 — 평균 투시 시간', 'j'),
        ('≈20%', '혈관내 주입 — AP·사위 <b>차이 없음</b>', 'r'),
    ], note='정확도는 같고 피폭은 절반. 사위·측면은 <b>확인용</b>으로 선택적으로.'),
    foot='PMC11433151 (2024, 180명 후향 코호트) · PMID 36288582 (2022, AP vs 사위 무작위 비교) · '
         'Wheeless\' Textbook · WikiMSK',
)

add(
    t='bullets', eyebrow='PROCEDURE · 1 준비와 표적',
    title='절차 ① — 자세부터 표적 확인까지',
    kick='영상을 먼저 맞춘다. 바늘은 표적이 확정된 뒤에 든다.',
    items=[
        (0, '<b>1</b> 복와위, 복부 아래 베개로 요추 전만을 줄인다.'),
        (0, '<b>2</b> 진성 <b>AP</b>에서 해당 레벨의 <b>종판을 한 선으로</b> 맞춘다(두미측 경사).'),
        (0, '<b>3</b> 동측으로 <b>사위 회전</b> — SAP–TP 변곡점이 옆모습으로 잡히고 척추경 윤곽이 '
            '선명해질 때까지. 보통 10–25°이나 <b>환자마다 다르다</b>.'),
        (0, '<b>4</b> 표적 확인 — 스코티독의 <b>귀(SAP)와 코(TP)가 만나는 곳</b>. '
            '유두–부돌기 절흔보다 <b>위</b>, 유두돌기보다 <b>외측</b>. 눈(척추경)이 표적이 아니다.', 'hi'),
        (0, '<b>5</b> 피부 팽진은 <b>최소량</b>(≈0.5 mL)으로, 아픈 부위를 피해서. '
            '과다하면 피부 분지가 마취되어 <b>위양성</b>을 만든다.', 'hr_'),
    ],
    foot='Musculoskeletal Key oblique-approach chapter · Amrhein TJ et al. AJR 2016 (PMID 27276532)',
)

add(
    t='bullets', eyebrow='PROCEDURE · 2 바늘과 확인',
    title='절차 ② — 골 접촉에서 주입까지',
    kick='종착점은 절흔에서의 골 접촉. 그다음은 전부 확인 작업이다.',
    items=[
        (0, '<b>6</b> 22–25 G · 3.5–5 inch 굽은 Quincke 척추바늘을 <b>빔을 따라</b> 골 접촉까지. '
            '먼저 SAP·후궁에 닿게 겨눈 뒤 <b>외측·미측으로 걸어 내려</b> 절흔에 앉힌다.', 'hi'),
        (0, '<b>7</b> <b>AP</b>(끝이 SAP 외측연에 걸치거나 약간 내측, 높이는 횡돌기 상연)와 <b>사위</b>로 확인. '
            '깊이가 의심되면 <b>측면상</b>.'),
        (0, '<b>8</b> 비이온성 조영제 0.1–0.3 mL를 <b>실시간 투시</b>로. 뼈를 감싸는 음영이면 정상, '
            '혈관 유출이면 바늘을 옮긴다. <b>흡인만으로는 3분의 1만 잡힌다.</b>', 'hi'),
        (0, '<b>9</b> 신경당 국소마취제 <b>≤0.25–0.5 mL</b>. '
            '<b>진단 차단에 스테로이드를 넣지 않는다</b> — 검사의 시간적 특징이 무너진다.', 'hr_'),
        (0, '<b>10–11</b> 두 번째 신경 반복(두 관절이면 신경 3개). 마취 지속시간에 맞춰 '
            '<b>통증일지</b>를 쓰게 하고 원래 아프던 동작을 직접 해보게 한다.'),
    ],
    foot='Lee CJ et al. Anesth Analg 2008 (PMID 18349205) · Wahezi SE et al. PM R 2018 (PMID 29174073) · '
         '2024 China/US Consensus Guidelines',
)

add(
    t='figure', eyebrow='PITFALL · 깊이',
    title='복측으로 미끄러지면 <b>다른 것을 마취</b>한다',
    kick='종착점은 절흔에서의 골 접촉이다. 그 너머로 나아갈 이유가 없다.',
    panels=[
        dict(pt='올바른 깊이', svg=F.lateral_depth(True), tone='ok',
             pl='절흔에서 <b>골 접촉으로 정지</b> — 복측 진행 없음'),
        dict(pt='복측 미끄러짐', svg=F.lateral_depth(False), tone='bad',
             pl='횡돌기 상면에서 미끄러져 <b>척추간공·신경뿌리</b> 방향으로'),
    ],
    caption='예방법 — 먼저 <b>약간 내측</b>을 겨눠 SAP·후궁에 닿게 한 뒤, 거기서 '
            '<b>외측·미측으로 걸어 내려</b> 절흔에 앉힌다. 깊이가 의심되면 <b>측면상</b>을 본다',
    foot='WikiMSK, Lumbar Medial Branch Blocks · 사체 연구에서 잘못된 위치의 주입액이 '
         '척추간공을 지나 척추체 외측까지 전방 확산한 사례가 보고되었다',
)

add(
    t='figure', eyebrow='PITFALL · 주입량',
    title='0.25 mL와 0.5 mL는 <b>다른 검사</b>다',
    kick='용량이 커지면 표적을 넘어 퍼지고, 그 순간 “어느 신경이 마취됐는지” 알 수 없게 된다.',
    panels=[
        dict(pt='0.25 mL', svg=F.volume_spread("0.25 mL", True), tone='ok',
             pl='심부·중간 근층에 국한 → <b>표적 특이도 유지</b>. RFA가 태울 범위와 일치한다'),
        dict(pt='0.5 mL', svg=F.volume_spread("0.5 mL", False), tone='bad',
             pl='배측 표층근·후지 원위분지, 그리고 <b>인접 레벨 내측지</b>까지'),
    ],
    caption='CT에서 0.5 mL는 <b>16%</b>에서 경막외강·척추간공에 도달했다. 같은 용량이라도 절흔 최상연보다 '
            '<b>약간 미측</b>(유두–부돌기 쪽)을 겨누면 확산이 줄어든다 — 권고는 <b>0.25 mL(사체 최적) '
            '· &lt;0.5 mL(합의) · 0.5–0.75 mL(과거 관행)</b> 순으로 갈린다',
    foot='Dreyfuss P et al. Spine 1997;22(8):895–902 (PMID 9127924) · '
         'Wahezi SE et al. PM R 2018;10(6):616–622 (PMID 29174073) · '
         'Cohen SP et al. Reg Anesth Pain Med 2020 (PMID 32245841)',
)

add(
    t='table', eyebrow='SAFETY · 혈관내 주입',
    title='흡인은 믿을 수 없다',
    kick='혈관내로 들어가면 약이 씻겨나가 <b>위음성</b>이 된다 — 그리고 흡인은 그것의 3분의 1만 잡는다.',
    headers=['검출 방법', '연구', '검출률 / 민감도', '해석'],
    rows=[
        ['흡인(aspiration)', 'Lee 2008 · 1433건', '민감도 <b>34.1%</b> (88건 중 30건)',
         '단독으로는 부적합'],
        ['정지 방사선영상', 'Lee 2008 · 1433건', '민감도 <b>59.1%</b> (88건 중 52건)',
         '약 40%를 놓친다'],
        ['실시간 투시 + 조영', 'Lee 2008', '전체 발생률 <b>6.1%</b>/신경', '<b>권고되는 최소 기준</b>'],
        ['실시간 투시', 'Pain Med 2016 · 344건', '<b>11%</b> (95% CI 8.0–15)', 'DSA 대비 과소검출'],
        ['디지털 감산(DSA)', 'Pain Med 2016 · 344건', '<b>≈19%</b> (추가 27건 발견)', '가장 민감'],
        ['AP vs 사위 비교', 'PMID 36288582 · 2022', '양군 모두 <b>≈20%</b>', '접근법과 무관'],
    ],
    hlrows={2: 'hl'},
    note='저자들의 결론 그대로 — “흡인 검사는 정지 영상 유무와 무관하게 혈관내 조영제 흡수를 자주 놓쳤다. '
         '조영제 주입 시 <b>실시간 투시 사용을 강력히 권고</b>한다.” · 초음파는 조영 흐름을 볼 수 없어 '
         '이 문제를 원리적으로 해결하지 못한다.',
    notec='warn',
    foot='Lee CJ et al. Anesth Analg 2008;106(4):1274–1278 (PMID 18349205) · Pain Medicine 2016;17(6):1031',
)

add(
    t='split', eyebrow='ULTRASOUND · 초음파 유도',
    title='삼지창을 찾고, 90° 돌린다',
    kick='피폭이 없고 비침습적이지만, 혈관내 주입을 볼 수 없고 L5에서 가장 어렵다.',
    items=[
        (0, '<b>1단계</b> 2–5 MHz 곡선형 탐촉자를 극돌기 정중선 외측 <b>3–4 cm</b>, '
            '시상방(parasagittal)으로 — 횡돌기가 고에코 돔과 그 아래 음향음영으로 나타나는 '
            '<b>삼지창 징후(trident sign)</b>. 천골부터 세어 올라가며 각 레벨 중점을 표시한다.'),
        (0, '<b>2단계</b> 탐촉자를 <b>90° 회전</b>해 축상면으로 — 극돌기·후궁·후관절·SAP·TP를 확인.'),
        (0, '<b>표적</b> = <b>횡돌기 두측 가장자리가 SAP와 만나는 홈</b>. '
            '20–22 G 척추바늘, <b>평면내(in-plane) 외측→내측</b>, 피부와 <b>45–60°</b>.', 'hi'),
        (0, '<b>확인</b> 골 접촉 후 탐촉자를 다시 종축으로 돌려 바늘 끝이 횡돌기 두측면에 있는지 본다 — '
            '투시의 AP/측면 한 쌍을 대신하는 <b>2평면 확인</b>.'),
        (0, '<b>L5 후지</b>는 별개 문제 — 탐촉자를 S1 SAP·천골익 위에 두고 바늘을 미측에서 '
            '두측으로 진행. 검증된 변형은 <b>회전 교차축 사위 평면외</b> 접근이다.', 'hr_'),
    ],
    aside=dict(title='정확도 — 양쪽을 다 보라', tone='joint', stat=[
        ('94%', 'Greher 2004 · CT 확인 (50건 중 47)', 'j'),
        ('95% / 91.6%', 'Shim 2006 · Asian Spine J 2012 (투시 확인)', 'j'),
        ('11%p', '메타분석 — 부정확 배치 위험차 (7편)', 'r'),
    ], note='단일 연구는 90%대, <b>메타분석은 부정확 배치가 11%p 더 많다</b>고 본다 (근거수준 낮음~매우 낮음).',
        notec='warn'),
    foot='Greher M et al. Anesthesiology 2004 (PMID 15114223 / 15505456) · Shim JK et al. RAPM 2006 (PMID 16952818) · '
         'Ashmore Z et al. Pain Reports 2022 (PMID 35620250) · Greher M et al. RAPM 2015 (PMID 26414871)',
)

add(
    t='figure', eyebrow='ULTRASOUND · 소노해부',
    title='삼지창 징후 (trident sign)',
    kick='횡돌기 세 개의 고에코 돔과 그 아래 음향음영 — 그 사이가 음향창이다.',
    panels=[
        dict(pt='시상방 종축 스캔', svg=F.us_trident(), tone='',
             pl='표적은 <b>횡돌기 두측 가장자리와 SAP가 만나는 홈</b>'),
    ],
    caption='<b>한계</b> — BMI 30 미만에서 성공률 80.5%인 반면 전체는 72.5%. BMI 35 초과는 대부분 연구에서 제외된다. '
            'Greher는 BMI 36에서도 landmark가 확보됐다고 보고했고, Rauch는 비만에서 <b>신뢰할 수 없다</b>고 결론했다',
    foot='ASRA Pain Medicine, Ultrasound-Guided Lumbar Medial Branch and Intra-articular Facet Injections (2019) · '
         'Greher M et al. Anesthesiology 2004 · Rauch S et al. Reg Anesth Pain Med 2009',
)


# ══════════════════════════════════════════════ 05 관절강내 주사
add(
    t='sec', no='05', title='관절강내 주사는 무엇이 다른가',
    desc='같은 관절을 겨누지만 표적이 다르다. 신경이 아니라 관절강이고, '
         '그래서 용량 한계와 확산이라는 전혀 다른 문제를 안는다.',
)

add(
    t='figure', eyebrow='ORIENTATION · 레벨별 관절면',
    title='관절면이 미측으로 갈수록 <b>관상면</b>에 가까워진다',
    kick='그래서 관절을 여는 사위각이 레벨마다 다르고, L5–S1이 가장 어렵다.',
    panels=[
        dict(pt='축상면 (axial)', svg=F.facet_orientation(), tone='j',
             pl='관절은 평면이 아니라 축상면에서 <b>C자·J자로 굽어 있다</b> — '
                '앞 1/3은 관상면, 뒤 2/3는 점점 시상면. 투시로 “열리는” 것은 <b>뒤쪽 부분</b>뿐이다'),
    ],
    caption='기하학적으로 필요한 사위각 ≈ 90° − (관절면이 시상면과 이루는 각). 시상면에 가까운 상부 요추일수록 '
            '<b>더 큰 사위</b>가 필요하지만 55–65°는 실제로 불가능해, 실무에서는 타협한 각도에서 '
            '<b>오목(recess)</b>을 노린다. L5–S1의 어려움은 각도보다 <b>장골능·천골익·가파른 요천각</b> 때문이다',
    foot='각도 수치는 계측 시리즈마다 기준면·영상법·측정 슬라이스가 달라 같은 관절에서도 15–20° 차이가 난다 — '
         '이 발표에서는 숫자를 단정하지 않고 방향성만 제시한다',
    rail='all', railtone='onj', ebc='j', kickc='j',
)

add(
    t='split', eyebrow='TECHNIQUE · 관절강내',
    title='표적은 관절선이 아니라 <b>하부 오목</b>이다',
    kick='퇴행된 관절에서는 관절선이 열리지 않는다. 오목은 더 크고 더 잘 늘어난다.',
    items=[
        (0, '<b>하부 오목(inferior recess)</b> — 하관절돌기 하연을 걸어 내려 아래에서 진입. '
            '연골면 사이가 아니라 <b>피막 주머니</b> 안에 바늘 끝이 놓인다. '
            '퇴행 관절과 L5–S1의 표준 대안이며 치료 목적 1차 표적으로 가르쳐진다.', 'hj'),
        (0, '<b>상부 오목은 피한다</b> — 황색인대·경막외강과 척추간공에 가장 가깝다. '
            '터졌을 때 경막외강으로 새는 바로 그 오목이다.', 'hr_'),
        (0, '<b>관절조영상</b>이 유일한 증거다. 조영제 <b>0.1–0.3 mL</b>에서 위아래 오목이 부풀며 '
            '가운데가 잘록한 모양이 나와야 한다. 0.5 mL를 넣었는데 관절조영상이 없으면 '
            '거의 확실히 <b>관절 밖</b>이다.', 'hj'),
        (0, '<b>정상 용적 1–1.5 mL</b>(문헌에 따라 1–2 mL). 조영제를 포함한 '
            '<b>총 주입량을 용적 안에</b> 둔다.', 'hj'),
        (0, '피막을 뚫는 “퍽” 느낌은 퇴행 관절에서 <b>아예 없을 수 있다</b> — 촉감만으로 '
            '관절강내라고 판단하지 않는다.', 'hr_'),
    ],
    aside=dict(title='용적을 넘기면 어디로 새나', tone='crit', items=[
        (0, '<b>상부 오목 파열</b> → 경막외강 → 이어서 척추간공·신경뿌리초', 'hr_'),
        (0, '<b>하부 오목 파열</b> → 후궁간·극간 공간, 다열근', 'hr_'),
        (0, '<b>후방 피막 파열</b> → 척추주위근', 'hr_'),
        (-1, ''),
        (0, '경막외강이나 신경뿌리에 닿은 주입액은 <b>후관절이 아닌 통증</b>도 줄인다 — '
            '그 순간 진단적 의미가 사라진다.', 'hj'),
    ]),
    foot='Bogduk N (ed.), ISIS/SIS Practice Guidelines · 관절조영 기술은 Dory MA, Radiology 1981 / '
         'Destouet JM et al., Radiology 1982에 기술 — 본 세션에서 원문 확인은 하지 못했다',
    ebc='j', kickc='j',
)

add(
    t='split', eyebrow='SPECIFICITY · 실측 데이터',
    title='관절강내 주사의 <b>절반</b>은 경막외강에도 들어간다',
    kick='이 발표에서 관절강내 주사의 표적 특이도를 가장 강하게 흔드는 단일 데이터다.',
    items=[
        (0, '연속 100명 · 192회 시술을 전향적으로 관찰했다.'),
        (0, '<b>환자의 64.6%</b>(64/99), <b>시술의 49.5%</b>(95/192)에서 '
            '경막외 확산이 일어났다.', 'hr_'),
        (0, '복측 확산 <b>29.2%</b> · 척추간공 확산 <b>18.8%</b>.'),
        (-1, ''),
        (0, '해석 — 관절강내 주사가 <b>치료</b>로서 의미가 없다는 뜻은 아니다. '
            '다만 <b>“이 관절이 원인이다”를 증명하는 검사</b>로는 쓸 수 없다는 뜻이다.', 'hj'),
        (0, '그래서 학회 문서들은 <b>내측지 차단을 진단 도구</b>로, '
            '관절강내 주사는 <b>치료 목적</b>으로 위치시킨다.', 'hj'),
    ],
    aside=dict(title='Yoo 2020', tone='crit', stat=[
        ('64.6%', '경막외 확산이 있었던 환자 비율', 'r'),
        ('49.5%', '경막외 확산이 있었던 시술 비율', 'r'),
        ('18.8%', '척추간공까지 확산', 'r'),
    ]),
    foot='Yoo BR, Lee E, Lee JW, Kang Y, Ahn JM, Kang HS. Incidence and pattern of epidural spread during '
         'lumbar facet joint injection: a prospective study. Acta Radiol 2020 (PMID 31510763)',
    ebc='j', kickc='j',
)

add(
    t='table', eyebrow='EVIDENCE · 관절강내 스테로이드',
    title='관절강내 주사의 무작위 근거 — 그리고 그 한계',
    kick='고전 시험들은 대부분 음성이다. 다만 환자 선정이 오늘 기준으로는 모두 부적절했다.',
    dense=True,
    headers=['연구', '설계', '결과', '확인 상태'],
    rows=[
        ['Carette 1991 · NEJM', '단일 국소마취 차단 ≥50%로 선별 후 메틸프레드니솔론 vs 식염수',
         '“만성 요통에서 <b>가치가 거의 없다</b>”', '<b>원문 미확인</b>'],
        ['Lilius 1989 · JBJS(Br)', '관절강내 스테로이드 vs 피막주위 vs 관절강내 식염수 3군',
         '세 군 모두 호전, <b>군간 차이 없음</b>', '<b>원문 미확인</b>'],
        ['Nash 1990 · Pain Clinic', '관절강내 vs 내측지 차단 무작위',
         '차이 없음, 내측지 쪽 비유의한 우세', '<b>원문 미확인</b>'],
        ['Marks 1992 · Pain', '관절강내 vs 내측지 차단, 86명, 1·3·6개월',
         '두 술기 간 <b>유의차 없음</b>', '<b>원문 미확인</b>'],
        ['Cochrane · 주사요법', '아급성·만성 요통 주사요법 체계적 고찰',
         '“근거 <b>불충분</b>” — 단, 하위군 이득을 배제하지는 못함', '<b>원문 미확인</b>'],
        ['FACTS 2018 · Anesthesiology', '229명 무작위 (관절강내 / 내측지 / 식염수)',
         '반응자 51% / 56% / 24% · <b>평균 통증은 3군 동일</b>', '확인됨 (PMID 29847426)'],
    ],
    hlrows={5: 'hlj'},
    note='<b>정직하게 읽는 법</b> — Carette의 결정적 약점은 선정이다. '
         '단일·비대조 차단에 50% 역치로 뽑았고(오늘 기준 위양성 38%), 대조군의 관절강내 <b>식염수도 불활성이 아니며</b>, '
         '증상 레벨과 무관하게 <b>최하위 두 관절</b>에 주사했다. 즉 “효과 없음”이 아니라 '
         '“<b>효과를 검출할 수 없는 설계</b>”였을 가능성이 크다. · 위 5편은 본 세션에서 원문을 열지 못했다 — '
         '인용 전 원문 확인 필요.',
    notec='warn',
    foot='Carette S et al. NEJM 1991 · Lilius G et al. JBJS Br 1989 · Nash TP. Pain Clinic 1990 · '
         'Marks RC et al. Pain 1992 · Staal JB et al. Cochrane 2008 · Cohen SP et al. Anesthesiology 2018',
    ebc='j', kickc='j',
)

# ══════════════════════════════════════════════ 06 적응증
add(
    t='sec', no='06', title='그래서 무엇을, 언제 쓰는가',
    desc='두 주사는 경쟁 관계가 아니다. 하나는 질문을 던지는 도구이고, 다른 하나는 답이 나온 뒤의 처치다.',
)

add(
    t='cmp', eyebrow='INDICATION · 최종 정리',
    title='내측지 차단 vs 관절강내 주사 — 무엇을 언제',
    kick='RFA가 태울 신경을 시험하는가, 관절 안에 약을 두는가. 목적이 다르면 도구도 다르다.',
    cards=[
        dict(tone='n', name='내측지 차단', en='MBB',
             sl='<b>진단·예후</b> 도구',
             items=[
                 (0, '축성 요통 <b>3개월↑</b>, 보존치료 실패, 신경뿌리 증상 없음'),
                 (0, '<b>RFA 전 예후 검사</b> — 태울 바로 그 신경을 시험한다', 'hi'),
                 (0, '퇴행으로 관절선이 막힌 관절에서도 시행 가능'),
                 (0, '관절당 신경 2개 · 두 관절이면 3개'),
                 (0, '국소마취제만 · 신경당 ≤0.25–0.5 mL · <b>스테로이드 금지</b>', 'hi'),
                 (0, '실시간 투시 조영으로 혈관내 주입 배제'),
             ],
             cf='학회 문서 공통 — 진단은 MBB'),
        dict(tone='j', name='관절강내 주사', en='IA facet injection',
             sl='<b>치료</b> 목적, 선택적으로',
             items=[
                 (0, '진단이 이미 선 상태에서의 <b>치료적</b> 스테로이드 주사'),
                 (0, '<b>활막낭종</b> — 팽창·파열 또는 흡인이 목적일 때', 'hj'),
                 (0, 'MRI상 <b>급성 관절 삼출·활막염</b>이 뚜렷할 때'),
                 (0, '화농성 후관절염 의심 시 <b>배양 목적 흡인</b>', 'hj'),
                 (0, '총량 <b>1–1.5 mL</b> 이내 · 관절조영상으로 확인'),
                 (0, '진단 목적으로는 부적합 — 절반이 경막외강으로 샌다', 'hr_'),
             ],
             cf='CT 유도 — 심한 퇴행·유합술 후·낭종'),
    ],
    foot='Cohen SP et al. Reg Anesth Pain Med 2020;45(6):424–467 (PMID 32245841) — 다학제 국제 합의는 '
         'MBB가 관절강내 주사보다 RFA 반응을 더 잘 예측한다고 결론했다',
)

add(
    t='split', eyebrow='SELECTION · 환자 선정',
    title='적응증과, 검증에 실패한 “적응증”',
    kick='체크리스트로 고를 수 없다는 것이 이 분야의 가장 확실한 결론이다.',
    items=[
        (0, '<b>합리적 적응</b> — 만성 축성 요통(3개월 이상), 보존치료 실패, '
            '방사통·신경학적 결손 없음, 적색징후 없음, 영상에서 다른 원인 배제.'),
        (0, '<b>임상적으로 시사적</b>(WIP/Pain Practice 2024) — 편측 국소 요통, '
            '하퇴로 뻗지 않음, 움직임에 악화, 방척추 압통, 신경병증적 성질 없음.'),
        (0, '다만 위 소견들은 <b>차단의 필요를 줄여주지 못한다</b> — Maas 2017 체계적 고찰의 결론.', 'hr_'),
        (0, '<b>연령</b>은 유일하게 일관된 신호다 — 나이가 들수록 후관절 기여가 커진다(≈70세까지).'),
        (-1, ''),
        (0, '<b>영상 소견으로 고르지 말 것</b> — 지역사회 코호트에서 후관절 골관절염은 '
            'L4–5 45.1% · L5–S1 38.2%로 흔했지만 요통과 <b>연관이 없었다</b>.', 'hr_'),
    ],
    aside=dict(title='주의 · 감별', tone='crit', items=[
        (0, '<b>장골능·서혜부 통증</b>이면 T12–L1 흉요추 이행부(Maigne)를 함께 본다 — '
            '표준 L3/L4/L5 세트에 <b>포함되지 않는 레벨</b>이다.', 'hr_'),
        (-1, ''),
        (0, '<b>서혜부 통증 = 상부 요추</b>는 오해다. L2~L5 어디서든 유발된다.', 'hr_'),
        (-1, ''),
        (0, '금기·항응고 관련 학회 권고(ASRA/ESRA 2018 위험 계층화)는 '
            '<b>이번 문헌검색에서 확인하지 못했다</b> — 원문을 직접 확인할 것.', 'hj'),
    ]),
    foot='Maas ET et al. Eur J Pain 2017 (PMID 27723170) · van den Heuvel SAS et al. Pain Pract 2024 · '
         'Kalichman L et al. (지역사회 후관절 OA 코호트) · DePalma MJ et al. Pain Med 2011',
)

# ══════════════════════════════════════════════ 07 효과와 논쟁
add(
    t='cmp', eyebrow='CONTROVERSY · MINT',
    title='RFA는 효과가 없다는 시험, 그리고 그 반박',
    kick='요추 후관절 중재술 전체에 대한 가장 강한 반증이자, 가장 격렬하게 반박된 시험이다.',
    cards=[
        dict(tone='j', name='MINT 3부작', en='Juch, JAMA 2017',
             sl='임상적으로 의미 있는 개선 <b>없음</b>',
             items=[
                 (0, '네덜란드 16개 다학제 통증클리닉, 실용적·<b>비맹검</b> 무작위 시험 3건'),
                 (0, '3개월 통증강도 평균차 — 후관절 <b>−0.18</b> (95% CI −0.76~0.40)', 'hj'),
                 (1, '천장관절 −0.71 (−1.35~−0.06) · 복합 −0.99 (−1.73~−0.25)'),
                 (0, '후관절 시험은 <b>통계적 유의성에도 도달하지 못했다</b>'),
                 (0, '결론 — RFA + 표준 운동요법이 운동요법 단독보다 낫지 않다', 'hj'),
             ],
             cf='JAMA 2017;318(1):68–81 (PMID 28672319)'),
        dict(tone='n', name='반박', en='Kapural 2017 등',
             sl='선정과 술기의 문제라는 반론',
             items=[
                 (0, '<b>선정</b> — 이중 차단·80%가 아니라 <b>단일 차단·50%</b>로 뽑았다', 'hi'),
                 (0, '<b>비맹검</b> 실용적 설계'),
                 (0, '전극 위치·병변 생성 기법에 대한 의문'),
                 (0, '운동요법 <b>병행</b>이 신호를 희석'),
                 (0, '이 논쟁이 곧 “차단을 몇 번 할 것인가”라는 미해결 질문 그 자체다', 'hi'),
             ],
             cf='Kapural L et al. Neuromodulation 2017 (PMID 29220124)'),
    ],
    foot='ASRA Pain Medicine News 2024, “Evidence for Diagnostic Blocks Prior to RFA — None, Once, or Twice?” · '
         '국제 설문 PMID 39029928 — 이 질문은 가이드라인 수준에서 여전히 열려 있다',
)

add(
    t='key', eyebrow='SUMMARY',
    title='열 문장으로 정리하면',
    msgs=[
        ('이중 지배', '관절 하나에 신경 둘. <b>L4–5 = L3 + L4 내측지</b>. 표적 뼈는 신경 번호보다 한 칸 아래 — '
                      '신경으로 말하고 뼈로 가리켜라.'),
        ('표적', 'L1–L4는 <b>SAP–TP 접합부의 홈</b>. L5는 내측지가 아니라 <b>후지 본간</b>을 '
                 '천골익 × S1 SAP 접합부에서.'),
        ('연관통', '요부·둔부·대전자·외측/후방 대퇴·서혜부 <b>6구역</b>. L1–2는 요부에 머물고 '
                   'L3–4 이하 세 레벨은 <b>같은 다섯 구역</b>을 때린다.'),
        ('지도의 한계', '연관통으로 <b>레벨을 특정할 수 없다</b>. 경추는 되고 요추는 안 된다.'),
        ('선별 불가', '병력·진찰·영상 어느 것도 양성 차단을 예측하지 못한다(Revel 92% → Laslett &lt;17%). '
                      '단일 차단의 위양성은 <b>38%</b>, 위약 반응 24%는 비교 차단으로도 안 걸러진다.', 'j'),
        ('용량·확인', '<b>0.25 mL</b>는 표적에 머물고 <b>0.5 mL</b>는 인접 레벨·경막외강(16%)까지 간다. '
                      '흡인 민감도는 <b>34%</b> — 실시간 투시 조영이 최소 기준이다.'),
        ('관절강내', '환자의 <b>64.6%</b>에서 경막외 확산 — 진단 도구가 아니라 '
                      '<b>치료·특수 적응</b>(낭종·삼출·배양)용.', 'j'),
        ('열린 질문', '차단 <b>몇 번</b>, 역치 <b>50%인가 80%인가</b> — SIS와 국제 합의가 다르고, '
                      'MINT 논쟁의 핵심도 이것이다.'),
    ],
    foot='각 문장의 출처는 해당 슬라이드에 표기',
)

add(
    t='bullets', eyebrow='LIMITATIONS · 이 문헌고찰의 한계',
    title='확인하지 못한 것들',
    kick='발표에서 이 슬라이드를 빼지 말 것 — 어떤 수치가 아직 검증되지 않았는지가 곧 다음 과제다.',
    items=[
        (0, '<b>원문 PDF에 접근하지 못했다.</b> 네트워크 정책이 PubMed·PMC·출판사 호스트를 차단해(403), '
            '모든 근거는 <b>검색 결과에 노출된 초록·요약 텍스트</b>에서 수집했다. '
            '쪽수·저자 전체 목록·일부 저널명은 미확인이다.', 'hr_'),
        (0, '<b>관절강내 주사의 고전 무작위 시험 5편</b>(Carette·Lilius·Nash·Marks·Cochrane)은 '
            '서지사항만 확인했고 수치는 확인하지 못했다 — 인용 전 원문 필수.', 'hr_'),
        (0, '<b>금기·항응고</b>(ASRA/ESRA 2018)와 <b>합병증 발생률</b>은 다루지 못했다 — '
            '감염·출혈·척수마취 등 안전 항목은 별도 확인이 필요하다.', 'hr_'),
        (0, '<b>SIS 실무지침 원문</b>을 열지 못해 사위각·바늘 굵기·조영제 용량을 SIS에 귀속시키지 않았다. '
            '레벨별 사위각을 명시한 1차 문헌도 없었다 — 검증된 레벨 규칙은 L5의 장골능 회피뿐이다.'),
        (0, '<b>후관절통의 무릎 아래 연관 비율</b>은 신뢰할 수치를 찾지 못했다. '
            'Fukui의 구역 체계에는 무릎 아래가 아예 없다 — 어떤 %도 인용하지 말 것.', 'hr_'),
    ],
    note='원문은 <b>scripts/fetch_papers.py</b>를 네트워크 제약이 없는 환경에서 실행하면 '
         '주제별 폴더에 공개접근본으로 채워진다.',
    foot='정직한 문헌고찰의 조건은 “무엇을 모르는지”를 함께 적는 것이다',
)


# ══════════════════════════════════════════════ 참고문헌
_REFS = [
    "Bogduk N, Long DM. The anatomy of the so-called 'articular nerves' and their relationship to facet "
    "denervation. <b>J Neurosurg</b> 1979;51(2):172–177. PMID 156249",
    "Bogduk N, Wilson AS, Tynan W. The human lumbar dorsal rami. <b>J Anat</b> 1982;134(Pt 2):383–397. PMID 7076562",
    "Bogduk N. The lumbar mamillo-accessory ligament: its anatomical and neurosurgical significance. "
    "<b>Spine</b> 1981;6(2):162–167. PMID 6456553",
    "Bogduk N. The innervation of the lumbar spine. <b>Spine</b> 1983;8(3):286–293. PMID 6226119",
    "Auteroche P. Innervation of the zygapophyseal joints of the lumbar spine. <b>Anat Clin</b> 1983;5(1):17–28",
    "Shuang F, et al. Clinical anatomy and measurement of the medial branch of the spinal dorsal ramus. "
    "<b>Medicine (Baltimore)</b> 2015;94(52). PMC5291620",
    "Tran J, Lawson A, Billias N, Loh E. 3D nerve proximity mapping of the medial branch of lumbar dorsal ramus. "
    "<b>Interv Pain Med</b> 2024;3(2):100414",
    "Tran J, Conger A, Lightfoot K, McCormick ZL, Loh E. Lumbar facet joint denervation targeting the medial "
    "branch in the sub-mammillary fossa. <b>Interv Pain Med</b> 2025. PMC12051118",
    "Lau P, Mercer S, Govind J, Bogduk N. The surgical anatomy of lumbar medial branch neurotomy. "
    "<b>Pain Med</b> 2004;5(3):289–298. PMID 15367308",
    "Maigne JY, Maigne R, Guerin-Surville H. The lumbar mamillo-accessory foramen: a study of 203 lumbosacral "
    "spines. <b>Surg Radiol Anat</b> 1991. PMID 1905063",
    "Macintosh JE, Valencia F, Bogduk N, Munro RR. The morphology of the human lumbar multifidus. "
    "<b>Clin Biomech</b> 1986;1(4):196–204",
    "Dreyfuss P, Stout A, Aprill C, et al. The significance of multifidus atrophy after successful radiofrequency "
    "neurotomy. <b>PM R</b> 2009;1(8):719–722. PMID 19695523",
    "Giles LGF, Taylor JR. Human zygapophyseal joint capsule and synovial fold innervation. "
    "<b>Br J Rheumatol</b> 1987;26(2):93–98. PMID 2435355",
    "Ashton IK, Ashton BA, Gibson SJ, et al. Morphological basis for back pain: nerve fibers and neuropeptides "
    "in the lumbar facet joint capsule but not in ligamentum flavum. <b>J Orthop Res</b> 1992;10(1):72–78. PMID 1530799",
    "Kapetanakis S, Gkantsinikoudis N. Anatomy of lumbar facet joint: a comprehensive review. "
    "<b>Folia Morphol</b> 2021;80(4):799–805",
    "Fukui S, Ohseto K, Shiotani M, et al. Distribution of referred pain from the lumbar zygapophyseal joints "
    "and dorsal rami. <b>Clin J Pain</b> 1997;13(4):303–307. PMID 9430810",
    "Mooney V, Robertson J. The facet syndrome. <b>Clin Orthop Relat Res</b> 1976;115:149–156. PMID 130216",
    "McCall IW, Park WM, O'Brien JP. Induced pain referral from posterior lumbar elements in normal subjects. "
    "<b>Spine</b> 1979;4(5):441–446",
    "Marks R. Distribution of pain provoked from lumbar facet joints and related structures during diagnostic "
    "spinal infiltration. <b>Pain</b> 1989;39(1):37–40",
    "Windsor RE, King FJ, Roman SJ, et al. Electrical stimulation induced lumbar medial branch referral patterns. "
    "<b>Pain Physician</b> 2002;5(4):347–353. PMID 16886011",
    "Dwyer A, Aprill C, Bogduk N. Cervical zygapophyseal joint pain patterns I: a study in normal volunteers. "
    "<b>Spine</b> 1990;15(6):453–457. PMID 2402682",
    "Kellgren JH. On the distribution of pain arising from deep somatic structures. <b>Clin Sci</b> 1939;4:35–46",
    "Feinstein B, Langton JNK, Jameson RM, Schiller F. Experiments on pain referred from deep somatic tissues. "
    "<b>J Bone Joint Surg Am</b> 1954;36(5):981–997. PMID 13211692",
    "Bogduk N. On the definitions and physiology of back pain, referred pain, and radicular pain. "
    "<b>Pain</b> 2009;147(1–3):17–19",
    "International Spine Intervention Society. Lumbar medial branch blocks. In: Bogduk N, ed. "
    "<b>Practice Guidelines for Spinal Diagnostic and Treatment Procedures</b>, 2nd ed. 2013:559–600",
    "Schwarzer AC, Aprill CN, Derby R, et al. The false-positive rate of uncontrolled diagnostic blocks of the "
    "lumbar zygapophysial joints. <b>Pain</b> 1994;58(2):195–200. PMID 7816487",
    "Schwarzer AC, Aprill CN, Derby R, et al. Pain from the lumbar zygapophysial joints: a test of two models. "
    "<b>J Spinal Disord</b> 1994;7(4):331–336. PMID 7949701",
    "Schwarzer AC, Wang SC, Bogduk N, et al. Prevalence and clinical features of lumbar zygapophysial joint pain. "
    "<b>Ann Rheum Dis</b> 1995;54(2):100–106. PMID 7702395",
    "Jackson RP, Jacobs RR, Montesano PX. Facet joint injection in low-back pain: a prospective statistical study. "
    "<b>Spine</b> 1988;13(9):966–971",
    "Revel M, Poiraudeau S, Auleley GR, et al. Capacity of the clinical picture to characterize low back pain "
    "relieved by facet joint anesthesia. <b>Spine</b> 1998;23(18):1972–1976. PMID 9779530",
    "Laslett M, Öberg B, Aprill CN, McDonald B. Zygapophysial joint blocks in chronic low back pain: a test of "
    "Revel's model as a screening test. <b>BMC Musculoskelet Disord</b> 2004;5:43. PMID 15546487",
    "Maas ET, Juch JNS, Ostelo RWJG, et al. Systematic review of patient history and physical examination to "
    "diagnose chronic low back pain originating from the facet joints. <b>Eur J Pain</b> 2017;21(3):403–414. PMID 27723170",
    "Manchikanti L, Pampati V, Fellows B, Bakhit CE. The inability of the clinical picture to characterize pain "
    "from facet joints. <b>Pain Physician</b> 2000;3(2):158–166. PMID 16906195",
    "Manchikanti L, Manchikanti KN, Manchukonda R, et al. Prevalence of facet joint pain in chronic low back pain "
    "in postsurgical patients. <b>Arch Phys Med Rehabil</b> 2007;88(4):449–455. PMID 17398245",
    "Manchikanti L, Manchikanti KN, Cash KA, et al. Age-related prevalence of facet-joint involvement in chronic "
    "neck and low back pain. <b>Pain Physician</b> 2008;11(1):67–75. PMID 18196171",
    "Manchikanti L, Hirsch JA, Pampati V, et al. Low back pain and diagnostic lumbar facet joint nerve blocks: "
    "assessment of prevalence and false-positive rates. <b>Pain Physician</b> 2020;23(5):519–530. PMID 32967394",
    "Manchikanti L, Kaye AD, Soin A, et al. Comprehensive evidence-based guidelines for facet joint interventions "
    "(ASIPP guidelines). <b>Pain Physician</b> 2020;23:S1–S127. PMID 32503359",
    "DePalma MJ, Ketchum JM, Saullo T. What is the source of chronic low back pain and does age play a role? "
    "<b>Pain Med</b> 2011;12(2):224–233. PMID 21266006",
    "DePalma MJ, Ketchum JM, Trussell BS, et al. Does the location of low back pain predict its source? "
    "<b>PM R</b> 2011;3(1):33–39. PMID 21257131",
    "Kaplan M, Dreyfuss P, Halbrook B, Bogduk N. The ability of lumbar medial branch blocks to anesthetize the "
    "zygapophysial joint: a physiologic challenge. <b>Spine</b> 1998;23(17):1847–1852. PMID 9762741",
    "Dreyfuss P, Schwarzer AC, Lau P, Bogduk N. Specificity of lumbar medial branch and L5 dorsal ramus blocks: "
    "a computed tomographic study. <b>Spine</b> 1997;22(8):895–902. PMID 9127924",
    "Wahezi SE, Alexeev E, Georgy JS, et al. Lumbar medial branch block volume-dependent dispersion patterns as a "
    "predictor for ablation success: a cadaveric study. <b>PM R</b> 2018;10(6):616–622. PMID 29174073",
    "Lee CJ, Kim YC, Shin JH, et al. Intravascular injection in lumbar medial branch block: a prospective "
    "evaluation of 1433 injections. <b>Anesth Analg</b> 2008;106(4):1274–1278. PMID 18349205",
    "Detection of intravascular injection during lumbar medial branch blocks: aspiration vs live fluoroscopy vs "
    "digital subtraction. <b>Pain Medicine</b> 2016;17(6):1031",
    "Comparison of intravascular uptake and technical ease between anteroposterior and oblique views during "
    "lumbar medial branch block. 2022. PMID 36288582",
    "Comparison of radiation doses for different techniques in fluoroscopy-guided lumbar facet medial branch "
    "blocks: a retrospective cohort study. 2024. PMC11433151",
    "Optimal caudal needle angulation for lumbar medial branch denervation: a 3D cadaveric and clinical imaging "
    "comparison. <b>Interv Pain Med</b> 2024. PMC11536316",
    "Amrhein TJ, Kranz PG, Cantrell S, Hurley RW. Technique for CT fluoroscopy–guided lumbar medial branch blocks "
    "and radiofrequency ablation. <b>AJR</b> 2016. PMID 27276532",
    "Greher M, Scharbert G, Kamolz LP, et al. Ultrasound-guided lumbar facet nerve block: a sonoanatomic study. "
    "<b>Anesthesiology</b> 2004;100:1242–1248. PMID 15114223",
    "Greher M, Kirchmair L, Enna B, et al. Ultrasound-guided lumbar facet nerve block: accuracy confirmed by "
    "computed tomography. <b>Anesthesiology</b> 2004;101:1195–1200. PMID 15505456",
    "Greher M, Moriggl B, Peng PWH, et al. Ultrasound-guided approach for L5 dorsal ramus block and fluoroscopic "
    "evaluation in unpreselected cadavers. <b>Reg Anesth Pain Med</b> 2015;40(6):713–717. PMID 26414871",
    "Shim JK, Moon JC, Yoon KB, et al. Ultrasound-guided lumbar medial-branch block: a clinical study with "
    "fluoroscopy control. <b>Reg Anesth Pain Med</b> 2006. PMID 16952818",
    "The validation of ultrasound-guided lumbar facet nerve blocks as confirmed by fluoroscopy. "
    "<b>Asian Spine J</b> 2012;6(3):163",
    "Ashmore Z, et al. Ultrasound-guided lumbar medial branch blocks and intra-articular facet joint injections: "
    "a systematic review and meta-analysis. <b>Pain Reports</b> 2022. PMID 35620250",
    "Rauch S, et al. Ultrasound-guided lumbar medial branch block in obese patients: a fluoroscopically confirmed "
    "clinical feasibility study. <b>Reg Anesth Pain Med</b> 2009",
    "Cohen SP, Doshi TL, Constantinescu OC, et al. Effectiveness of lumbar facet joint blocks and predictive value "
    "before radiofrequency denervation (FACTS). <b>Anesthesiology</b> 2018;129(3):517–535. PMID 29847426",
    "Cohen SP, Williams KA, Kurihara C, et al. Multicenter randomized comparative cost-effectiveness study "
    "comparing 0, 1, and 2 diagnostic medial branch block paradigms. <b>Anesthesiology</b> 2010;113(2):395–405. PMID 20613471",
    "Cohen SP, Bhaskar A, Bhatia A, et al. Consensus practice guidelines on interventions for lumbar facet joint "
    "pain from a multispecialty, international working group. <b>Reg Anesth Pain Med</b> 2020;45(6):424–467. PMID 32245841",
    "Juch JNS, Maas ET, Ostelo RWJG, et al. Effect of radiofrequency denervation on pain intensity among patients "
    "with chronic low back pain: the MINT randomized clinical trials. <b>JAMA</b> 2017;318(1):68–81. PMID 28672319",
    "Kapural L, et al. RE: Juch JNS, et al. (MINT 반박). <b>Neuromodulation</b> 2017. PMID 29220124",
    "Holz SC, Sehgal N. What is the correlation between facet joint radiofrequency outcome and response to "
    "comparative medial branch blocks? <b>Pain Physician</b> 2016;19(3):163–172. PMID 27008290",
    "Diagnostic block(s) before radiofrequency ablation of the spinal facet joints: none, once or two times — "
    "an international survey of pain medicine physicians. 2024. PMID 39029928",
    "Yoo BR, Lee E, Lee JW, Kang Y, Ahn JM, Kang HS. Incidence and pattern of epidural spread during lumbar facet "
    "joint injection: a prospective study. <b>Acta Radiol</b> 2020. PMID 31510763",
    "van den Heuvel SAS, Cohen SP, de Andrès Ares J, et al. Pain originating from the lumbar facet joints "
    "(WIP 실무 가이드라인). <b>Pain Pract</b> 2024. DOI 10.1111/papr.13287",
    "2024 Consensus guidelines on lumbar facet interventions among practicing pain physicians in China and the "
    "United States. DOI 10.12290/xhyxzz.2024-0076",
    "† Carette S, Marcoux S, Truchon R, et al. A controlled trial of corticosteroid injections into facet joints "
    "for chronic low back pain. <b>N Engl J Med</b> 1991",
    "† Lilius G, Laasonen EM, Myllynen P, et al. Lumbar facet joint syndrome: a randomised clinical trial. "
    "<b>J Bone Joint Surg Br</b> 1989",
    "† Marks RC, Houston T, Thulbourne T. Facet joint injection and facet nerve block: a randomised comparison in "
    "86 patients with chronic low back pain. <b>Pain</b> 1992",
    "† Nash TP. Facet joints — intra-articular steroids or nerve block? <b>The Pain Clinic</b> 1990",
    "† Staal JB, de Bie R, de Vet HCW, et al. Injection therapy for subacute and chronic low-back pain. "
    "<b>Cochrane Database Syst Rev</b>",
    "† Dory MA. Arthrography of the lumbar facet joints. <b>Radiology</b> 1981 · Destouet JM, et al. "
    "<b>Radiology</b> 1982 (관절조영·용적)",
    "Kalichman L, et al. Facet joint osteoarthritis and low back pain in the community-based population. PMC3021980",
]

_PER = 16
for _i in range(0, len(_REFS), _PER):
    _chunk = _REFS[_i:_i + _PER]
    _n = _i // _PER + 1
    add(
        t='refs', eyebrow=f'REFERENCES · {_n}/{(len(_REFS) - 1) // _PER + 1}',
        title=f'참고문헌 <span style="font-family:PlexM,monospace;font-weight:600">{_i+1}–{_i+len(_chunk)}</span>',
        kick=('† 표시는 본 세션에서 원문을 확인하지 못한 문헌 — 인용 전 원문 확인 필요'
              if any(r.startswith('†') for r in _chunk) else None),
        refs=_chunk,
        foot='서지정보는 검색 결과에 노출된 초록·요약 텍스트로 대조했다. '
             '원문 PDF 접근은 네트워크 정책으로 차단되었다',
    )
