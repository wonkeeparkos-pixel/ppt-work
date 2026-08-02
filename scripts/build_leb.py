# -*- coding: utf-8 -*-
"""요추 경막외 차단(Lumbar Epidural Block) 문헌고찰 — 웹 덱 + PPTX 생성기.

실제 조영제 사진은 02_에셋/contrast_real/ 에 지정 파일명으로 넣으면 자동 삽입된다.
없으면 출처·직링크가 적힌 빈 플레이트가 표시된다 (모식도/AI 이미지 대체 금지).
"""
import os, re, sys, base64, mimetypes

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deck_html import render_deck

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "문헌고찰_Lumbar_Epidural_Block")
PHOTO_DIR = os.path.join(BASE, "02_에셋", "contrast_real")
FACES_CSS = os.path.join(BASE, "02_에셋", "pretendard_faces.css")
OUT_DIR = os.path.join(BASE, "03_산출물")

SERIES = "중재적 통증시술 문헌고찰 · 2026"
FOOT = "요추 경막외 차단 문헌고찰 · 2026"


def photo(file, what, ref, url):
    """사진이 있으면 data URI로, 없으면 빈 슬롯 정보로."""
    p = os.path.join(PHOTO_DIR, file)
    if os.path.isfile(p):
        mime = mimetypes.guess_type(p)[0] or "image/jpeg"
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        return {"src": f"data:{mime};base64,{b64}", "path": p, "what": what, "ref": ref,
                "url": url, "file": file,
                "caption": f"<b>{re.sub('<[^>]+>', '', what)}</b> — 출처 {ref}"}
    return {"src": None, "path": None, "what": what, "ref": ref, "url": url, "file": file}


S = []

# 01 ─ 표지
S.append(dict(t='title', eyebrow='Lumbar Epidural Block · 문헌고찰',
    title='요추 경막외 차단', sub='적응증과 효과 · 안전한 술기 · LOR 인지법 · 실패한 조영제 패턴',
    order='Indications · Efficacy · Safety · LOR Identification · Failed Contrast Patterns', series=SERIES))

# 02 ─ 목차
S.append(dict(t='bullets', eyebrow='Overview', tag=('임상 → 기술', 'ink'), title='오늘 다룰 것',
    items=[(-1, '<b>1 · 적응증과 금기</b> — 누구에게 하는가', 'accent'),
           (-1, '<b>2 · 효과</b> — 얼마나, 얼마 동안 듣는가', 'accent'),
           (1, '진단별 근거 수준 · 접근법별 효과 · 반응 예측인자'),
           (-1, '<b>3 · 해부</b> — 왜 실패가 구조적으로 일어나는가'),
           (1, '경막외강 · 황색인대 정중부 결손 · Okada 후경막강'),
           (-1, '<b>4 · LOR 인지법</b> — 5개 계열 24가지 방법 총정리'),
           (1, '음압법 · 저항소실법 · 기구 · 영상 · 전기·광학'),
           (-1, '<b>5 · 안전 술기</b> — 단계별 체크리스트'),
           (-1, '<b>6 · 조영제 패턴 판독</b> — 정상 1가지, 실패 7가지', 'red'),
           (-1, '<b>7 · 합병증과 가이드라인</b>')],
    foot=FOOT))

# 03 ─ 적응증 개관
S.append(dict(t='split', eyebrow='1 · 적응증', tag='무엇을 치료하는가',
    title='경막외 스테로이드는 무엇을 노리는가',
    items=[(-1, '<b>원리</b>'),
           (1, '경막외강에 스테로이드 → <b>신경근 주위 염증 감소</b> → 통증 완화'),
           (1, '목표는 <b>약물 감량과 수술 회피</b>, 그리고 재활이 가능한 창(window) 확보'),
           (-1, '<b>핵심 표적은 "염증성 신경근통(radicular pain)"</b>', 'accent'),
           (1, '디스크 수핵의 화학적 자극 + 기계적 압박 → 신경근 부종·염증'),
           (-1, '<b>대표 적응증</b>'),
           (1, '요추 <b>추간판 탈출증</b>에 의한 신경근통·좌골신경통', 'green'),
           (1, '요추 <b>척추관 협착증</b> — 신경인성 파행'),
           (1, '수술 후 요통 증후군(FBSS), 대상포진후신경통, 척추전방전위증 등')],
    aside=dict(title='시행 원칙', items=[
        (0, '<b>보존적 치료에 반응하지 않을 때</b>'),
        (0, '<b>영상 소견과 증상 분절이 일치</b>할 때', 'accent'),
        (0, '축성 요통(비신경근성) 단독은 <b>적응증이 아니다</b>', 'red'),
        (0, '진단적 가치도 있다 — 반응 분절이 병변 분절을 지목')]),
    foot=FOOT))

# 04 ─ 진단별 근거 수준
S.append(dict(t='table', eyebrow='1 · 적응증', tag=('근거 수준', 'ink'),
    title='진단별로 근거의 강도가 다르다',
    headers=['진단', '근거 수준', '요점'],
    rows=[['<b>추간판 탈출증 신경근통</b>', '<b>좋음 (good)</b>', '가장 확실한 적응증'],
          ['척추관 협착증', '보통 (fair)', '단기 효과는 있으나 <b>장기 논쟁</b>'],
          ['수술 후 요통 증후군 (FBSS)', '<b>나쁨 (poor)</b>', '유착 동반 — 확산 자체가 제한'],
          ['축성 요통 (비신경근성)', '근거 부족', '<b>적응증으로 보기 어렵다</b>']],
    hlrows=[0],
    note='70편을 검토한 체계적 문헌고찰 기준. <b>같은 시술이라도 진단이 결과를 가른다</b> — 적응증 선택이 술기보다 먼저다.',
    foot=FOOT))

# 05 ─ 금기
S.append(dict(t='split', eyebrow='1 · 금기', tag=('Contraindication', 'red'),
    title='금기 — 절대와 상대',
    items=[(-1, '<b>절대적 금기</b>', 'red'),
           (1, '동의를 거부하거나 동의 능력이 없는 경우', 'red'),
           (1, '<b>조영제 아나필락시스</b> 병력', 'red'),
           (1, '시술 부위의 <b>미해결 국소 감염</b>', 'red'),
           (1, '<b>전신 진균감염</b> — 스테로이드 투여 자체가 금기', 'red'),
           (1, '시술 중 협조가 불가능한 경우', 'red'),
           (-1, '<b>상대적 금기</b>'),
           (1, '투여 약물 알레르기 · <b>항응고제 사용</b> (ASRA 지침에 따라 관리)'),
           (1, '해부학적 변형(선천성 또는 수술 후)으로 안전 수행이 어려운 경우'),
           (1, '전신 감염 · 중대한 심폐 장애 · 면역억제 상태')],
    aside=dict(title='환자 선택 5가지', items=[
        (0, '의심되는 <b>기질적 병변</b>의 성격'),
        (0, '적극적 보존 치료에 대한 <b>무반응</b> 여부'),
        (0, '통증과 <b>기능 장애의 정도</b>'),
        (0, '금기에 해당하는 <b>동반 질환</b>'),
        (0, '이전 중재 시술에 대한 <b>반응</b>')]),
    foot=FOOT))

# 06 ─ 효과 숫자
S.append(dict(t='key', eyebrow='2 · 효과',
    headline='얼마나 듣는가 — <span style="color:#5FD6CC">숫자로</span>',
    msgs=[('단기 통증', '표준화 차이 <b>−24.0%</b> (95% CI −34.9 ~ −12.6) · <b>NNT 4</b>'),
          ('단기 기능장애', '표준화 차이 <b>−16.0%</b> (95% CI −26.6 ~ −5) · <b>NNT 6</b>'),
          ('근거 등급', 'AAN 지침 소위원회 기준 <b>"단기 효과는 아마도 있다(probably)"</b> 수준.'),
          ('장기 효과', '<b>3개월을 넘어서면 위약 대비 이득이 불분명</b>해진다.'),
          ('임상적 위치', '완치 수단이 아니라 <b>단기 가교(bridge) 치료</b> — 재활과 자연 경과를 위한 시간을 번다.')]))

# 07 ─ 진단별 효과
S.append(dict(t='split', eyebrow='2 · 효과', tag=('진단별', 'ink'),
    title='진단이 다르면 결과가 다르다',
    items=[(-1, '<b>추간판 탈출증 신경근통</b> — 가장 좋은 반응', 'green'),
           (1, '단기 통증·기능 개선이 일관되게 보고됨. 자연 경과와 겹치지만 회복을 앞당긴다'),
           (-1, '<b>척추관 협착증</b> — 단기에 그친다'),
           (1, '주사 후 <b>4–12주</b>에 통증·기능 개선. 장기 효과는 근거 상충'),
           (1, '<b>LESS 무작위 시험</b> (400명, 50세 이상, 16개 기관)', 'red'),
           (1, '스테로이드+리도카인 vs <b>리도카인 단독</b> — 6주 시점 기능·하지통 개선 <b>차이 없음</b>', 'red'),
           (1, 'CT·MRI상 <b>협착 중증도는 반응을 예측하지 못했다</b>', 'red'),
           (-1, '<b>FBSS</b> — 근거 빈약. 경막외 섬유화로 확산 자체가 막힌다')],
    aside=dict(title='해석', items=[
        (0, '협착증에서 효과의 상당 부분이 <b>국소마취제와 용적 효과</b>일 수 있다'),
        (0, '그렇다고 무용은 아니다 — <b>단기 완화</b>는 실재한다'),
        (0, '다만 <b>협착증에 반복 주사로 장기 관리</b>하는 전략은 근거가 약하다', 'red'),
        (0, '환자에게 <b>기대치를 정확히 설명</b>하는 것이 동의의 핵심')]),
    foot=FOOT))

# 08 ─ 접근법별 효과
S.append(dict(t='table', eyebrow='2 · 효과', tag='접근법별', title='접근법이 결과를 바꾼다',
    headers=['접근법', '복측 확산', '혈관내 주입률', '요점'],
    rows=[['정중 층간 (MIL)', '31.7%', '낮음', '전통적 · 술기 단순'],
          ['<b>방정중 층간 (PIL)</b>', '<b>89.7%</b>', '낮음', '병변측 lamina 내측연 진입'],
          ['경추간공 (TF)', '높음', '<b>11.2%</b>', '분절 선택성 우수'],
          ['미추 (Caudal)', '낮음', '<b>10.9%</b>', '가장 안전 · 대용량 필요']],
    hlrows=[1],
    note='Ghai 등(Anesth Analg 2013, 무작위 이중맹검): PIL이 MIL 대비 <b>6개월 유효 진통 68.4% vs 16.7%</b>, 총 주사 횟수 <b>29 vs 41회</b>. <b>같은 약을 써도 어디에 닿느냐가 결과를 가른다.</b>',
    foot=FOOT))

# 09 ─ 예측인자와 한계
S.append(dict(t='split', eyebrow='2 · 효과', tag='예측인자 · 한계',
    title='누가 잘 반응하는가, 무엇이 한계인가',
    items=[(-1, '<b>좋은 반응을 예측하는 인자</b>', 'green'),
           (1, '<b>MRI 소견이 최대 예측인자</b> — 체계적 문헌고찰 결론', 'green'),
           (1, '<b>낮은 등급의 신경 압박</b>일수록 결과가 좋다', 'green'),
           (1, '협착증보다 <b>추간판 탈출증</b>', 'green'),
           (-1, '<b>한계와 논쟁</b>', 'red'),
           (1, '<b>수술 회피 효과</b>는 근거가 혼재 — 확정적으로 말할 수 없다', 'red'),
           (1, '협착증의 <b>장기 효과</b>는 근거 상충', 'red'),
           (1, '다만 <b>수술 전 ESI가 수술 결과를 악화시키지는 않았다</b>는 최근 데이터'),
           (-1, '고령 협착증 환자에서 근거가 부족한 채 표준 치료화되었다는 비판도 존재')],
    aside=dict(dark=True, title='실무 결론', items=[
        (0, '<b>추간판 탈출증 신경근통</b>에 가장 자신 있게 쓴다'),
        (0, '<b>협착증</b>은 단기 완화 목적으로, 기대치를 낮춰 설명한다'),
        (0, '<b>FBSS</b>는 유착 평가·유착박리 전략과 함께 고려한다'),
        (0, '반복 주사는 <b>반응이 있었을 때만</b>')]),
    foot=FOOT))

# 10 ─ 전환
S.append(dict(t='key', eyebrow='임상에서 기술로',
    headline='이 모든 효과는 <span style="color:#5FD6CC">약이 표적에 닿았을 때</span>의 이야기다',
    msgs=[('전제', '앞의 모든 수치는 <b>"약물이 병변 분절의 경막외강에 도달했다"</b>는 전제 위에 있다.'),
          ('확산 실패', '복측 확산에 실패하면 같은 약, 같은 용량이라도 <b>효과가 희석</b>된다 — 31.7% vs 89.7%.'),
          ('위치 실패', '경막하·혈관내로 들어가면 <b>효과는 0이고 위험만 남는다</b>.'),
          ('그래서', '적응증이 절반이라면, 나머지 절반은 <b>바늘을 정확히 놓는 기술</b>이다.')]))

# 11 ─ 기술 파트 문제 제기
S.append(dict(t='key', eyebrow='3 · 기술 파트 시작',
    headline='LOR은 진단이 아니라 <span style="color:#5FD6CC">가설</span>이다',
    msgs=[('구조적 위양성', '황색인대는 정중선에서 자주 융합하지 않는다. 요추 L1–2 <b>22.2%</b>, L2–L5 약 <b>10%</b>에서 정중부 결손(midline gap).'),
          ('가짜 공간', '황색인대 <b>바로 뒤</b>에 Okada 후경막강이 있다. 경추 층간 접근에서 위양성 LOR <b>30–65%</b>.'),
          ('놓치는 혈관', '흡인 음성은 혈관내 위치를 배제하지 못한다. 실시간 투시 민감도 <b>60–71%</b>.'),
          ('검증 수단', '가설을 검증하는 것은 <b>조영제</b>다. 스테로이드 주입 전 실시간 투시 확인은 타협 대상이 아니다.')]))

# 04 ─ 해부 1
S.append(dict(t='split', eyebrow='3 · 해부', tag='기초', title='경막외강 — 잠재적 공간의 실제',
    items=[(0, '대후두공에서 <b>천골열공</b>까지 이어지는 잠재적 공간'),
           (0, '내용물: 경막외 지방, <b>Batson 정맥총</b>, 림프관, 분절 신경근'),
           (0, '후방 깊이는 <b>요추에서 5–6 mm로 최대</b>, 두측으로 갈수록 좁아짐'),
           (1, '→ 요추 접근이 경·흉추보다 구조적으로 안전한 이유'),
           (0, '피부–경막외강 거리 평균 <b>4–6 cm</b> (BMI에 비례)'),
           (0, '척수원추는 통상 <b>L1–L2</b>에서 종료', 'accent'),
           (1, '→ <b>L4–5, L5–S1</b>이 가장 안전한 천자 높이', 'accent')],
    aside=dict(title='실무 함의', items=[
        (0, '높은 분절 층간 접근은 <b>척수 손상 위험이 실재</b>한다', 'red'),
        (0, '원추 종료 위치는 <b>개인차</b>가 있으므로 영상 확인 없이 고위 접근 금지'),
        (0, '경막외강이 좁을수록 과진입 여유가 없다 — 흉추·경추에서 LOR 사고가 집중')]),
    foot=FOOT))

# 05 ─ 황색인대 정중부 결손 (표)
S.append(dict(t='table', eyebrow='3 · 해부', tag=('LOR 위음성의 근원', 'red'),
    title='황색인대는 정중선에서 자주 붙어 있지 않다',
    headers=['분절', '정중부 결손 빈도', '해석'],
    rows=[['C3–4', '66%', '경추는 과반이 결손'],
          ['C5–6', '<b>74%</b>', '최고 빈도'],
          ['C7–T1', '51%', '경흉추 이행부'],
          ['하부 흉추 (T6–9)', '2–4%', 'T10–12에서 정점'],
          ['<b>L1–2</b>', '<b>22.2%</b>', '요추 중 최다'],
          ['<b>L2–L5</b>', '<b>약 10%</b>', '드물지만 0은 아니다']],
    hlrows=[4, 5],
    note='Lirk 등 사체 연구 · 결손부 평균 폭 1.0 ± 0.3 mm → <b>엄격한 정중 접근에서 황색인대가 바늘을 막아준다고 신뢰할 수 없다.</b> 이것이 방정중 접근의 해부학적 근거다.',
    foot=FOOT))

# 06 ─ Okada
S.append(dict(t='split', eyebrow='3 · 해부', tag=('가짜 LOR의 주범', 'red'),
    title='Okada 후경막강 (Retrodural space)',
    items=[(0, '1981년 Okada가 경추 후관절 조영술 개발 중 기술'),
           (0, '<b>황색인대 배측(dorsal)</b>의 잠재적 공간 — 경막외강 바로 뒤'),
           (0, '모든 척추 분절에 존재. 동측·인접 후관절, 추간공, 협부결손, 극간 점액낭, 척추주위 조직과 <b>교통</b>'),
           (0, '여기 들어가면 <b>경막외 진입과 구별되지 않는 LOR</b>이 발생', 'red'),
           (0, '경추 층간 접근 위양성 LOR <b>30–65%</b>', 'red'),
           (0, '<b>퇴행성 후관절 변화가 심할수록</b> 빈도 증가')],
    aside=dict(dark=True, title='감별의 열쇠', items=[
        (0, 'AP 단독 판독으로는 <b>구별 불가</b>'),
        (0, '<b>lateral / CLO view 병행</b>이 유일한 실전 감별법'),
        (0, '조영제가 후관절로 <b>역류</b>하거나 인접 분절로 새는 양상이 단서'),
        (0, '경막외 특유의 <b>종축 확산 + 신경근 곁가지</b>를 만들지 않는다')]),
    foot=FOOT))

# ─ LOR 지도
S.append(dict(t='key', eyebrow='4 · Loss of Resistance', tag='총정리',
    headline='LOR 인지법 — <span style="color:#5FD6CC">5개 계열</span>로 정리한다',
    msgs=[('A · 음압 원리', 'Hanging drop(Gutierrez) · Odom · Dawkins 모세관 · Macintosh 풍선'),
          ('B · 저항 소실', 'LOR to air · saline · saline+기포 · 간헐/지속 진입 · Bromage grip'),
          ('C · 기구·자동화', 'Episure · Epidrum · Epi-Jet · EpiFaith · APAD · CompuFlo · 파형분석'),
          ('D · 영상 유도', '투시 AP/lateral/<b>CLO</b> · 조영제 · DSA · 초음파(PSO·SMI) · CT'),
          ('E · 전기·광학', 'Tsui 전기자극 · 자가형광 분광 · OCT+딥러닝 · 생체임피던스')]))

# 09 ─ A계열
S.append(dict(t='table', eyebrow='4 · LOR — A계열', tag='음압 원리',
    title='A · 경막외강의 음압을 이용하는 방법',
    headers=['기법', '원리 · 술기', '한계'],
    rows=[['<b>Hanging drop</b><br>(Gutierrez, 1933)', '바늘 허브에 식염수 한 방울 → 진입 시 <b>빨려 들어감</b>', '요추는 음압이 약해 <b>위음성 흔함</b>'],
          ['Odom\'s indicator', '유리관 내 액체·기포 주의 이동 관찰', '현재 거의 사용 안 함'],
          ['Dawkins 모세관', '모세관 압력계로 압력 강하 감지', '정량적이나 번거로움'],
          ['<b>Macintosh 풍선</b><br>(1950)', '허브의 소형 풍선이 진입 시 <b>갑자기 수축</b>', '팽창압 표준화 어려움']],
    note='주의: 음압은 <b>경막외강 고유의 성질이 아니다.</b> 바늘 끝의 경막 압박(tenting)과 흉곽내압 전달로 생기는 현상이며, <b>요추·앙와위·비만 환자에서는 약하거나 소실</b>된다.',
    foot=FOOT))

# 10 ─ B계열
S.append(dict(t='bullets', eyebrow='4 · LOR — B계열', tag='표준 술기',
    title='B · 저항 소실 — 실제로 쓰는 방법들',
    items=[(-1, '<b>B1 · LOR to air</b> (Dogliotti, 1933) — 공기 2–3 mL'),
           (1, '촉감 예민, 조영제 희석 없음 / 공기 특이 합병증 다수', 'red'),
           (-1, '<b>B2 · LOR to saline</b> — 생리식염수 2–3 mL'),
           (1, '공기 합병증 회피 / CSF와 감별 곤란(포도당·온도·pH 확인)'),
           (-1, '<b>B3 · LOR to saline + 기포</b> (compressibility test)', 'accent'),
           (1, '기포만 압축되고 주입 안 되면 <b>아직 인대 안</b> → 촉감의 객관화', 'accent'),
           (-1, '<b>B4 · 간헐적 진입</b> — 조금 전진 → 압력 확인 → 반복. 안전하나 느림'),
           (-1, '<b>B5 · 지속 압력 유지</b> — 즉시 인지 / <b>관성에 의한 과진입 위험</b>', 'red'),
           (-1, '<b>B6 · Bromage grip / 양손 고정</b> — 손을 환자 등에 고정', 'green'),
           (1, '과진입을 <b>물리적으로 차단</b>하는 가장 확실한 안전장치', 'green')],
    foot=FOOT))

# 11 ─ 공기 vs 식염수
S.append(dict(t='split', eyebrow='4 · LOR — B계열', tag=('근거', 'ink'),
    title='공기 vs 식염수 — 무엇이 맞는가',
    items=[(-1, '<b>Cochrane 체계적 문헌고찰</b> (Antibas 등, 2014)'),
           (1, '7편 RCT · 852명. 경막외강 확인 실패, 카테터 위치 이상, CSE 실패, 미차단 분절, 통증 — <b>모두 유의차 없음</b>'),
           (1, '근거 수준은 <b>낮음(low quality)</b>, 대부분 산과 환자에서 도출'),
           (-1, '<b>그러나 공기에는 특이 합병증이 있다</b>', 'red'),
           (1, '기뇌증 · 신경근/척수 압박 · 후복막 공기 · 피하기종 · 종격기종', 'red'),
           (1, '<b>정맥 공기색전</b> · 경막외 공기가 약물 확산을 막아 <b>반점상 차단</b>', 'red'),
           (-1, '<b>메타분석</b>: Epidrum 등 대체법이 공기 대비 확인 실패 유의 감소'),
           (1, 'RR 0.29 (95% CI 0.11–0.77; P=0.01)', 'accent')],
    aside=dict(title='실무 권고', items=[
        (0, '투시 유도 만성통증 시술에서는 <b>식염수 기반 LOR</b>을 기본으로', 'green'),
        (0, '공기를 쓴다면 <b>1–2 mL 이하</b>로 제한', 'green'),
        (0, '식염수는 <b>조영제 판독을 방해하지 않는다</b>는 이점도 있다')]),
    foot=FOOT))

# 12 ─ C계열 기구
S.append(dict(t='table', eyebrow='4 · LOR — C계열', tag='기구·자동화',
    title='C · 주관적 촉감을 객관적 신호로',
    headers=['장치', '원리', '근거'],
    rows=[['<b>Episure™ AutoDetect</b>', '내장 스프링이 플런저에 <b>일정 압력 지속 인가</b> → 진입 시 자동 하강', '유리주사기 5례 실패 vs 스프링 <b>0례</b>'],
          ['<b>Epidrum®</b>', '허브 부착 팽창막이 진입 시 즉시 함몰', '공기 대비 확인 실패 <b>RR 0.29</b>'],
          ['<b>Epi-Jet®</b>', '압력 지시 장치', '산과 240명 RCT에서 <b>Epidrum보다 우월</b>'],
          ['EpiFaith®', '스프링 로디드 주사기 (공기/식염수)', '임상 연구 진행 중'],
          ['<b>APAD</b>', '바늘 끝 압력을 <b>음향 + 시각 신호</b>로 실시간 변환', 'FDA 승인 · 교육·문서화에 유용']],
    note='공통 목적: "저항이 사라진 느낌"이라는 <b>술자 의존적 판단</b>을 장치가 읽는 <b>재현 가능한 신호</b>로 바꾼다.',
    foot=FOOT))

# 13 ─ CompuFlo
S.append(dict(t='split', eyebrow='4 · LOR — C계열', tag=('압력 파형', 'ink'),
    title='CompuFlo® — 압력을 연속 정량 측정한다',
    items=[(-1, '<b>판정 기준 두 가지</b>'),
           (1, '① 압력의 <b>급강하 후 저압 고평부(plateau)</b> 형성 = 경막외강 진입', 'accent'),
           (1, '② 진입 후 <b>동맥 박동과 동기화된 박동성 파형</b> 확인', 'accent'),
           (-1, '경막외압은 본래 <b>박동성</b>이며 동맥 박동과 동기화된다 — 이것이 원리'),
           (-1, '<b>근거</b>'),
           (1, '투시·전통 LOR 대비 성공률 <b>비열등</b> (무작위 대조)'),
           (1, '600례 연속 증례 보고 · 케이스 시리즈 다수'),
           (-1, '<b>경막외 파형 분석(EWA)</b> — 카테터/바늘을 압력 트랜스듀서에 연결'),
           (1, '박동성 파형 유무로 위치 확인. CSE 후 카테터 확인에 유용')],
    aside=dict(dark=True, title='왜 중요한가', items=[
        (0, 'LOR의 근본 문제는 <b>기록이 남지 않는다</b>는 것'),
        (0, '압력 파형은 <b>객관적 기록</b>이 되어 교육·문서화·의료분쟁 대응에 쓰인다'),
        (0, '다만 <b>Okada 공간에서도 저압은 나온다</b> — 조영제 확인을 대체하지 못한다', 'red')]),
    foot=FOOT))

# 14 ─ D계열 영상
S.append(dict(t='table', eyebrow='4 · LOR — D계열', tag='영상 유도',
    title='D · "느낌"에서 "확인"으로',
    headers=['방법', '무엇을 주는가', '한계'],
    rows=[['투시 AP', '분절 · 정중선 · 바늘 궤적', '<b>깊이 판단 불가</b>'],
          ['투시 True lateral', '깊이 판단', '양측 lamina 겹쳐 <b>바늘 끝 흐림</b>'],
          ['<b>투시 CLO (대측 사위)</b>', '<b>VILL</b> = 경막외강 후방경계 지표', '표적 반대측 약 45° 회전 필요'],
          ['<b>조영제 경막외조영술</b>', '<b>LOR 가설의 최종 검증</b>', '패턴 판독 능력이 필요'],
          ['DSA', '혈관내 주입 검출률 향상', '장비 · 피폭'],
          ['초음파 (PSO 사전스캔)', '분절 · 깊이 · 정중선 사전 결정', '실시간 바늘 추적 어려움'],
          ['CT 투시', '정확도 최고 · Okada 검출 유리', '피폭 · 접근성']],
    hlrows=[2, 3],
    foot=FOOT))

# 15 ─ CLO
S.append(dict(t='split', eyebrow='4 · LOR — D계열', tag=('핵심', 'green'),
    title='CLO view와 VILL — 깊이를 객관화하는 법',
    items=[(0, '표적 <b>반대측</b>으로 C-arm을 약 <b>45°</b> 회전 (경추는 <b>50°</b>)'),
           (0, 'AP에서 층간 개구부 중점에 진입, 표적측 <b>pedicle 방향</b>으로 조준'),
           (0, '<b>VILL (ventral interlaminar line)</b> = 복측 층간선', 'accent'),
           (1, 'lamina 복측면을 잇는 선 = <b>경막외강 후방 경계의 방사선학적 지표</b>', 'accent'),
           (0, '바늘 끝을 <b>1–2 mm 이내</b> 정밀도로 조준 가능'),
           (0, '조영제도 <b>VILL을 따라 lamina 복측</b>으로 흐르는지 확인'),
           (-1, '<b>근거</b>'),
           (1, 'Gill 등(Pain Med 2015): 경추·경흉추에서 <b>lateral view보다 우월</b> — 바늘 끝 가시성, 궤적 예측력, 후방경계 지표 모두', 'green'),
           (1, 'PLOS One 2021: 요추 층간 29례에서 복측 경막외강 도달률 <b>93.1%</b>, 합병증 <b>0례</b>', 'green')],
    aside=dict(title='왜 lateral보다 나은가', items=[
        (0, 'lateral은 <b>좌우 lamina가 겹쳐</b> 바늘 끝이 어디인지 모호하다'),
        (0, 'CLO는 표적측 층간 개구부를 <b>정면으로 펼쳐</b> 보여준다'),
        (0, 'ASRA도 "정밀함과 용이함의 결합"으로 <b>CLO를 선호</b>한다고 기술')]),
    foot=FOOT))

# 16 ─ 초음파 + E계열
S.append(dict(t='split', eyebrow='4 · LOR — D·E계열', tag='보조·신기술',
    title='초음파 · 전기자극 · 광학',
    items=[(-1, '<b>초음파 — 방정중 시상 사위(PSO)</b>'),
           (1, 'lamina 사이로 <b>황색인대–경막 복합체(posterior complex)</b>가 선상 고에코로 보임'),
           (1, '분절 · <b>깊이</b> · 정중선을 <b>천자 전에</b> 결정 → 시도 횟수 감소'),
           (1, 'SMI·color Doppler로 주입 시 <b>황색인대 파열 신호</b> 관찰 가능'),
           (-1, '<b>Tsui test — 전기자극</b>', 'accent'),
           (1, '0→10 mA 증가. <b>1–10 mA 근절 반응 = 경막외 정상</b>', 'accent'),
           (1, '<b>&lt;1 mA</b> = 지주막하 또는 신경근 직접 접촉 / <b>&gt;10 mA</b> = 경막외강 밖', 'red'),
           (1, '민감도 <b>80–100%</b>'),
           (-1, '<b>광학 · 임피던스 (연구 단계)</b>'),
           (1, '자가형광: <b>황색인대 형광 강도가 타 조직의 최소 10배</b> → 성공률 87%'),
           (1, 'OCT(해상도 ~10 µm, 초음파·투시의 10–100배) + 딥러닝 / 생체임피던스')],
    aside=dict(title='정리', items=[
        (0, '모든 신기술의 방향은 하나 — <b>주관적 촉감을 객관적 신호로</b>'),
        (0, '그러나 현재 임상 표준은 여전히 <b>영상 + 조영제 확인</b>이다'),
        (0, '장비는 LOR을 <b>보조</b>할 뿐 조영제 확인을 <b>대체하지 않는다</b>', 'red')]),
    foot=FOOT))

# 17 ─ 안전술기 전
S.append(dict(t='bullets', eyebrow='5 · 안전 술기', tag=('시술 전', 'green'),
    title='시술 전 — 준비가 안전의 절반',
    items=[(-1, '<b>1 · 적응증·금기 재확인</b>'),
           (1, '영상(MRI/CT)에서 황색인대 결손 · 유착 · 수술 기왕력 확인'),
           (-1, '<b>2 · 항혈전제 관리 — ASRA 가이드라인</b>', 'accent'),
           (1, '<i>Interventional Spine and Pain Procedures in Patients on Antiplatelet and Anticoagulant Medications</i> (2015 초판 · 2018 개정 · <b>2022 제2판</b>)'),
           (1, '시술을 출혈위험 <b>저·중·고위험</b>으로 층화 — 층간 경막외 주입은 고위험군에 준하여 관리'),
           (-1, '<b>3 · 비입자성 스테로이드(dexamethasone) 우선</b>', 'green'),
           (1, '동물실험에서 <b>입자성 스테로이드의 동맥내 주입만</b> 영구적 중추신경 손상 유발'),
           (1, '효능은 대등 → <b>안전성이 선택을 결정</b>한다', 'green'),
           (-1, '<b>4 · 깊은 진정 금지</b>', 'red'),
           (1, '환자와의 <b>의사소통 유지</b>가 신경손상 조기 인지의 핵심 안전장치 (MSIS 2015)', 'red')],
    foot=FOOT))

# 18 ─ 안전술기 진입
S.append(dict(t='split', eyebrow='5 · 안전 술기', tag=('진입', 'green'),
    title='진입 — 되돌릴 수 없는 순간을 관리한다',
    items=[(0, '<b>가능한 낮은 분절</b> (L4–5, L5–S1) — 척수원추 아래', 'green'),
           (0, '<b>방정중 / 외측방시상 접근</b> — 황색인대 정중부 결손 회피 + 복측 확산 우수', 'green'),
           (0, '<b>CLO view(≈45°)에서 VILL을 지표로</b> 바늘 전진 — 깊이 인지의 객관화', 'green'),
           (0, '<b>양손 고정(Bromage grip)</b> — 과진입을 물리적으로 차단', 'green'),
           (0, '바늘을 <b>회전시키지 말 것</b>, 반복 천자 최소화', 'red'),
           (0, 'LOR은 <b>식염수 기반</b>, 공기 사용 시 최소량'),
           (0, '시술 중 <b>이상감각·심한 통증</b> 호소 시 즉시 중단', 'red')],
    aside=dict(dark=True, title='기억할 것', items=[
        (0, '경막외강 후방 깊이는 요추에서도 <b>5–6 mm</b>에 불과하다'),
        (0, '과진입 여유는 <b>밀리미터 단위</b>다'),
        (0, '그래서 손 고정과 CLO 깊이 확인이 <b>장비보다 먼저</b>다')]),
    foot=FOOT))

# 19 ─ 확인 단계
S.append(dict(t='key', eyebrow='5 · 안전 술기 · 확인',
    headline='LOR을 느꼈다 ≠ <span style="color:#FF9B8A">확인했다</span>',
    msgs=[('흡인', '혈액·CSF 확인. <b>단, 음성 흡인은 혈관내 위치를 배제하지 못한다.</b>'),
          ('실시간 투시', '조영제는 반드시 <b>live fluoroscopy</b> 하에. 정지 영상만으로는 혈관내 주입을 놓친다.'),
          ('DSA', '고위험 분절에서는 <b>디지털 감산</b>을 고려한다.'),
          ('패턴 확인', '<b>전형적 경막외 패턴을 확인한 뒤에만</b> 스테로이드를 주입한다.'),
          ('환자 반응', '테스트 용량 + 주입 중 증상 지속 확인. 대화가 되는 진정 수준을 유지한다.')]))

# 20 ─ 정상 조영 패턴 (사진)
S.append(dict(t='photo', eyebrow='6 · 조영제 판독', tag=('정상', 'green'),
    title='정상 경막외 패턴 — 어떻게 퍼지는가로 판정한다',
    photos=[photo('01_normal_epidural_ap.jpg',
                  'AP — 종축 확산 + 신경근 곁가지<br>("크리스마스 트리")',
                  'G1 · Epidural Contrast Patterns: An Educational Review (PMC12078379)',
                  'https://pmc.ncbi.nlm.nih.gov/articles/PMC12078379/'),
            photo('02_normal_epidural_clo.jpg',
                  'CLO — VILL을 따라 lamina 복측으로 흐르는 조영제',
                  'F3 · PLOS One 2021 (CC BY)',
                  'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0244992')],
    aside=dict(title='정상의 3요소', items=[
        (0, '<b>척추관 중심의 종축 확산</b> — 몸통'),
        (0, '<b>신경근을 따라가는 곁가지</b> — 가지', 'accent'),
        (0, 'AP에서 <b>지방 공포화(fat vacuolization)</b> — 양호한 위치의 방증'),
        (0, 'CLO에서 조영제가 <b>VILL을 따라 lamina 복측</b>으로'),
        (0, '이 셋이 없으면 <b>경막외가 아니다</b>', 'red')]),
    foot=FOOT))

# 21 ─ 혈관내 (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ①', tag=('혈관내', 'red'), warn=True,
    title='혈관내 주입 (Intravascular) — 씻겨 나간다',
    photos=[photo('03_vascular.jpg',
                  '<b>혈관내</b> — 가는 혈관 음영, 즉시 washout, 잔류 음영 없음',
                  'H1 · Accuracy of Live Fluoroscopy to Detect Intravascular Injection (PMC2884208)',
                  'https://pmc.ncbi.nlm.nih.gov/articles/PMC2884208/')],
    aside=dict(title='판독 포인트', items=[
        (0, '가늘게 흐르며 <b>즉시 사라진다</b>'),
        (0, '정맥총 따라 두미측 <b>빠른 유출</b>'),
        (0, '<b>잔류 음영 없음</b> — 결정적'),
        (0, '빈도 요천추 TF <b>11.2%</b> · 미추 <b>10.9%</b>'),
        (0, '흡인 → 재위치 → 재확인')]),
    foot=FOOT))

# 22 ─ 혈관내 검출 근거
S.append(dict(t='table', eyebrow='6 · 실패 패턴 ①', tag=('검출력', 'red'),
    title='흡인과 눈으로는 부족하다 — 숫자로 보는 검출력',
    headers=['검출 방법', '검출률 · 민감도', '함의'],
    rows=[['흡인 (aspiration)', '—', '음성이어도 <b>배제 불가</b>'],
          ['간헐적 투시', '낮음', '정지 영상은 놓친다'],
          ['실시간 투시 (요추 TF)', '민감도 <b>71.0%</b>', 'DSA가 잡은 9례를 놓침'],
          ['실시간 투시 (경막외 확산 동시 발생 시)', '민감도 <b>60%</b>', '가장 위험한 상황에서 가장 약함'],
          ['<b>DSA 추가 (경추 TF)</b>', '17.9% → <b>32.8%</b>', '검출률 <b>거의 2배</b> (P=.0471)'],
          ['<b>DSA 추가 (요추)</b>', '+<b>2.25%</b> 추가 검출', '실시간 투시 음성 증례 중']],
    hlrows=[3],
    note='요약: <b>혈관내 주입은 흡인으로 배제되지 않으며, 실시간 투시로도 3–4건 중 1건을 놓친다.</b> 경막외 확산과 동시에 일어날 때 검출력이 가장 낮다는 점이 특히 위험하다.',
    foot=FOOT))

# 23 ─ 경막하 (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ②', tag=('경막하', 'red'), warn=True,
    title='경막하 주입 (Subdural) — 가장 속기 쉬운 패턴',
    photos=[photo('04_subdural_ap.jpg',
                  '<b>경막하 AP</b> — 좌우대칭 선상 음영 "railroad / tram track", 다분절',
                  'G2 · Fluoroscopic Subdural Contrast Flow Pattern in the Lumbar Spine, Pain Med 2018',
                  'https://academic.oup.com/painmedicine/article/19/12/2571/5115550'),
            photo('05_subdural_lat.jpg',
                  '<b>경막하 측면</b> — 진하고 오래 잔류, 신경근 곁가지 없음',
                  'G6 · Inadvertent Subdural Injection during Cervical TFESI (PMC3893774, CC BY)',
                  'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3893774/')],
    aside=dict(title='판독 포인트', items=[
        (0, 'AP: <b>좌우 대칭의 가늘고 긴 선상 음영</b>'),
        (0, '같은 용량으로 <b>훨씬 여러 분절</b> 두측 확산'),
        (0, '<b>신경근 곁가지가 없다</b> — 결정적 차이', 'red'),
        (0, 'CSF에 희석 안 돼 <b>더 진하고 더 오래</b> 남음'),
        (0, '빈도 <b>0.8–1.6%</b> — 드물지 않다')]),
    foot=FOOT))

# 24 ─ 경막하 임상
S.append(dict(t='split', eyebrow='6 · 실패 패턴 ②', tag=('경막하 · 임상', 'red'),
    title='경막하 주입이 위험한 이유',
    items=[(0, '경막과 지주막 사이의 <b>잠재적 공간</b>에 약물이 갇힌다'),
           (0, '<b>예상보다 광범위한 차단</b> — 소량으로도 여러 분절', 'red'),
           (0, '<b>지연성 발현</b> — 주입 직후가 아니라 15–30분 뒤 나타날 수 있다', 'red'),
           (0, '감각·운동 차단, 신경 자극 증상, 자율신경 반응'),
           (0, '드물게 <b>호흡마비 · 혈역학 불안정</b>까지', 'red'),
           (-1, '<b>배측에 국한된 경우</b>'),
           (1, 'AP에서 <b>경계가 뚜렷한 둥근 덩어리</b> 모양 — 경막층이 갈라지지 않은 형태'),
           (1, '종괴 효과로 <b>신경 압박</b>을 일으킬 수 있다', 'red')],
    aside=dict(dark=True, title='발견했다면', items=[
        (0, '<b>즉시 주입 중단</b>'),
        (0, '바늘 제거 후 <b>관찰</b> — 지연성 발현 가능성 때문에 조기 귀가 금지'),
        (0, '활력징후 · 호흡 · 운동 감각 <b>연속 감시</b>'),
        (0, '그날은 <b>재시도하지 않는다</b>')]),
    foot=FOOT))

# 25 ─ 지주막하 (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ③', tag=('지주막하', 'red'), warn=True,
    title='지주막하 주입 (Subarachnoid / Intrathecal)',
    photos=[photo('06_intrathecal.jpg',
                  '<b>지주막하</b> — 척수조영(myelogram) 양상, 정중 대칭, CSF에 희석',
                  'G8 · Contrast mimicking SAH after lumbar percutaneous epidural neuroplasty (PMC3637364)',
                  'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3637364/')],
    aside=dict(title='판독 포인트', items=[
        (0, '<b>척수조영술 양상</b> — 경막낭을 채운다'),
        (0, '정중부 <b>좌우 대칭</b>, CSF에 빠르게 희석'),
        (0, '<b>lamina 내측연 음영 없음</b> — 감별점', 'red'),
        (0, '신경근이 <b>음영결손</b>으로 드러남'),
        (0, '빈도 최대 <b>1.2%</b> · 마미증후군·지주막염 위험', 'red')]),
    foot=FOOT))

# 26 ─ Okada (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ④', tag=('Okada', 'red'), warn=True,
    title='Okada 후경막강 주입 — 가짜 LOR의 결과물',
    photos=[photo('07_okada.jpg',
                  '<b>Okada 후경막강</b> — 황색인대 배측, 후관절로 역류',
                  'G4 · Contrast flow pattern in the space of Okada (PMC11646783)',
                  'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11646783/')],
    aside=dict(title='판독 포인트', items=[
        (0, '<b>초기엔 경막외와 유사해 보인다</b>', 'red'),
        (0, '<b>후관절로 역류</b>·인접 분절로 새는 양상이 단서'),
        (0, '<b>종축 확산도 신경근 곁가지도 없다</b>'),
        (0, '<b>lateral/CLO에서 황색인대 배측</b>임이 확인', 'accent'),
        (0, '위험인자 <b>퇴행성 후관절</b> · AP 단독 판독 금물', 'red')]),
    foot=FOOT))

# 27 ─ 근육/후관절 (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ⑤⑥', tag=('연부조직·후관절', 'amber'),
    title='근육·연부조직 / 후관절내 주입 — 퍼지지 않는다',
    photos=[photo('08_muscle_softtissue.jpg',
                  '<b>근육·연부조직</b> — 무정형 얼룩(blush), 확산 없음',
                  'G3 · ECR 2015 전자포스터 C-1816',
                  'https://epos.myesr.org/poster/esr/ecr2015/C-1816/findings%20and%20procedure%20details'),
            photo('09_facet.jpg',
                  '<b>후관절내</b> — 관절 윤곽을 그리는 국한된 조영',
                  'B10 · Inadvertent Intrafacet Injection during Lumbar ILESI, AJNR 2017',
                  'https://www.ajnr.org/content/38/2/398')],
    aside=dict(title='판독 포인트', items=[
        (0, '<b>근육·연부조직</b> — 국소 무정형 얼룩'),
        (1, '조직면 따라 <b>깃털·줄무늬</b>. 바늘이 얕거나 외측'),
        (0, '<b>후관절내</b> — <b>관절낭 모양</b>의 국한된 조영'),
        (1, '통상 투시가 CT 투시보다 더 흔하다'),
        (0, '공통점: <b>확산이 없다</b> → 재위치', 'red')]),
    foot=FOOT))

# 28 ─ 유착 (사진)
S.append(dict(t='photo', eyebrow='6 · 실패 패턴 ⑦', tag=('유착·편측', 'amber'),
    title='유착 · 편측 · 국소화 — 실패인 동시에 진단 정보',
    photos=[photo('10_adhesion_defect.jpg',
                  '<b>유착 / filling defect</b> — 편측 확산, 분절 결손',
                  'L1 · Clinical Significance of Epidurography Contrast Patterns after Adhesiolysis (PMC5901487)',
                  'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5901487/')],
    aside=dict(title='판독 포인트', items=[
        (0, '<b>한쪽으로만</b> 가거나 분절에서 <b>끊긴다</b>'),
        (0, '"크리스마스 트리"의 <b>가지가 결손</b>된 형태'),
        (0, '경막외 <b>섬유화·유착</b> — 특히 FBSS'),
        (0, '<b>결손이 증상 분절과 일치</b> → 진단적 가치', 'accent'),
        (0, '단, 확산 개선이 <b>통증 완화를 보장하진 않는다</b>', 'red')]),
    foot=FOOT))

# 29 ─ 감별 요약표
S.append(dict(t='table', eyebrow='6 · 조영제 판독', tag=('한 장 요약', 'ink'),
    title='조영제 패턴 감별표 — 시술대에서 볼 것',
    headers=['패턴', 'AP 소견', '결정적 감별점', '조치'],
    rows=[['<b>정상 경막외</b>', '종축 확산 + 신경근 곁가지', '곁가지 <b>있음</b>', '진행'],
          ['혈관내', '가늘게 흐르다 소실', '잔류 음영 <b>없음</b>', '흡인·재위치'],
          ['<b>경막하</b>', '좌우대칭 선상, 다분절', '곁가지 <b>없음</b> + 광범위', '<b>중단</b>·관찰'],
          ['지주막하', '정중 대칭, CSF 희석', 'lamina 내측연 음영 <b>없음</b>', '<b>중단</b>·관찰'],
          ['Okada', '경막외와 유사 가능', 'lateral/CLO에서 <b>배측</b>', '재천자'],
          ['근육·연부조직', '국소 얼룩', '<b>확산 없음</b>', '재위치'],
          ['후관절내', '관절 윤곽', '관절 모양', '재위치'],
          ['유착·편측', '분절 결손', '결손이 증상과 일치', '진단 활용']],
    hlrows=[2, 3],
    foot=FOOT))

# 30 ─ 합병증
S.append(dict(t='table', eyebrow='7 · 합병증', tag=('대응', 'red'),
    title='합병증 — 인지와 대응',
    headers=['합병증', '인지 단서', '대응'],
    rows=[['경막천자 / PDPH', 'CSF 역류 · 체위성 두통', '보존적 → 혈액봉합술(EBP)'],
          ['<b>경막외 혈종</b>', '시술 후 <b>진행성 하지 마비</b>·요통', '<b>응급 MRI + 신경외과</b> — 시간이 예후'],
          ['경막외 농양', '발열 · 국소압통 · 신경증상', '영상 + 항생제 ± 배농'],
          ['척수·신경근 손상', '시술 중 <b>이상감각·심한 통증</b>', '즉시 중단 — 깊은 진정 금지의 이유'],
          ['색전성 경색', '입자성 스테로이드 동맥내 주입', '<b>비입자성 스테로이드로 예방</b>'],
          ['기뇌증 · 공기색전', '공기 LOR 후 두통·의식저하', '공기 최소화 · 식염수 대체'],
          ['반점상 차단', '미차단 분절', '공기량 감소']],
    hlrows=[1],
    foot=FOOT))

# 31 ─ MSIS
S.append(dict(t='split', eyebrow='7 · 가이드라인', tag=('합의', 'ink'),
    title='다학제 합의 — FDA Safe Use Initiative (2015)',
    items=[(0, 'FDA Safe Use Initiative + 다학제 전문가 그룹 + <b>13개 전문학회</b> 협력'),
           (0, 'Rathmell 등, <i>Anesthesiology</i> 2015 — 경막외 스테로이드 주입의 <b>신경학적 합병증 예방</b> 합의 권고'),
           (-1, '<b>핵심 네 가지</b>', 'accent'),
           (1, '① <b>영상 유도</b> 없이 시행하지 않는다', 'green'),
           (1, '② <b>조영제 확인</b> 후에만 스테로이드를 주입한다', 'green'),
           (1, '③ <b>비입자성 스테로이드</b>를 우선한다', 'green'),
           (1, '④ <b>의사소통 가능한 진정 수준</b>을 유지한다', 'green'),
           (-1, '함께 볼 것: ASRA 항혈전제 가이드라인(2022 2판), WIP Benelux 권고(2018)')],
    aside=dict(dark=True, title='배경', items=[
        (0, '드물지만 <b>뇌졸중·척수 손상</b> 등 치명적 신경 손상이 실제로 발생했다'),
        (0, '경추 TF에서 <b>입자성 스테로이드의 추골동맥 분지 주입</b>이 색전성 뇌졸중을 유발'),
        (0, '이 합의는 <b>사고에서 역산된 권고</b>다 — 그래서 지킬 값어치가 있다')]),
    foot=FOOT))

# 32 ─ Take-home
S.append(dict(t='key', eyebrow='Take-home',
    headline='기억할 <span style="color:#5FD6CC">여덟 가지</span>',
    msgs=[('1 · 적응증이 먼저', '<b>추간판 탈출증 신경근통</b>에 근거가 가장 좋고, 협착증은 보통, FBSS는 나쁘다. 축성 요통은 적응증이 아니다.'),
          ('2 · 효과의 크기와 기간', '단기 통증 <b>NNT 4</b>, 기능 <b>NNT 6</b>. 그러나 <b>3개월을 넘으면 이득이 불분명</b>하다 — 가교 치료다.'),
          ('3 · 효과는 도달의 함수', '복측 확산 <b>89.7%(PIL) vs 31.7%(MIL)</b>. 같은 약이라도 어디에 닿느냐가 결과를 가른다.'),
          ('4 · LOR은 가설', '황색인대 정중부 결손(L1–2 22%, L2–5 약 10%)과 Okada 공간 때문에 위양성은 <b>구조적으로</b> 발생한다.'),
          ('5 · 검증은 조영제', '스테로이드 주입 전 <b>실시간 투시 하 조영제 확인</b>은 타협 대상이 아니다.'),
          ('6 · CLO와 VILL', '바늘 깊이를 객관화하는 가장 실용적 도구. <b>lateral보다 우월</b>하다.'),
          ('7 · 혈관내와 경막하', '흡인으로 배제되지 않는다(민감도 <b>60–71%</b>). 경막하는 "railroad track" + <b>곁가지 없음</b>, 빈도 <b>0.8–1.6%</b>.'),
          ('8 · 기본 안전장치', '<b>비입자성 스테로이드 + 얕은 진정 + 낮은 분절 + 방정중 접근</b>.')]))

# 33 ─ 참고문헌
S.append(dict(t='refs', title='주요 참고문헌', refs=[
    ('<b>Chou R 등.</b> Epidural Corticosteroid Injections for Radiculopathy and Spinal Stenosis: Systematic Review and Meta-analysis. <i>Ann Intern Med</i> 2015', 'https://www.acpjournals.org/doi/10.7326/M15-0934'),
    ('<b>AAN Guidelines Subcommittee.</b> Epidural Steroids for Cervical and Lumbar Radicular Pain and Spinal Stenosis: Systematic Review Summary. 2025', 'https://pubmed.ncbi.nlm.nih.gov/39938000/'),
    ('<b>Friedly JL 등.</b> A Randomized Trial of Epidural Glucocorticoid Injections for Spinal Stenosis (LESS). <i>N Engl J Med</i> 2014', 'https://www.nejm.org/doi/full/10.1056/NEJMoa1313265'),
    ('<b>LESS 추가분석.</b> Lumbar Spinal Stenosis Severity by CT or MRI Does Not Predict Response to Epidural Corticosteroid vs Lidocaine', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC7053900/'),
    ('Factors associated with improved outcomes after lumbar transforaminal ESI for radicular pain: systematic review. 2025', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11891702/'),
    ('Efficacy of ESI in sciatica secondary to lumbar disc herniation: systematic review and meta-analysis. 2024', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11150834/'),
    ('The clinical impact of lumbar ESI prior to spine surgery for lumbar spinal stenosis. 2024', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC11373000/'),
    ('<b>Epidural Steroid Injections</b> — StatPearls (적응증·금기·환자 선택)', 'https://www.ncbi.nlm.nih.gov/books/NBK470189/'),
    ('<b>Rathmell JP 등.</b> Safeguards to prevent neurologic complications after epidural steroid injections. <i>Anesthesiology</i> 2015', 'https://pubmed.ncbi.nlm.nih.gov/25668411/'),
    ('<b>ASRA.</b> Interventional Spine and Pain Procedures in Patients on Antiplatelet and Anticoagulant Medications, 2nd ed. 2022', 'https://asra.com/news-publications/asra-updates/blog-landing/guidelines/2022/12/14/interventional-spine-and-pain-procedures-in-patients-on-antiplatelet-and-anticoagulant-medications-(second-edition)'),
    ('<b>Antibas PL 등.</b> Air versus saline in the loss of resistance technique. <i>Cochrane Database Syst Rev</i> 2014', 'https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD008938.pub2/full'),
    ('<b>Lirk P 등.</b> Cervical and high thoracic ligamentum flavum frequently fails to fuse in the midline. <i>Anesthesiology</i> 2003', 'https://pubmed.ncbi.nlm.nih.gov/14639154/'),
    ('<b>Lirk P 등.</b> Incidence of lower thoracic ligamentum flavum midline gaps. <i>Br J Anaesth</i> 2005', 'https://academic.oup.com/bja/article/94/6/852/326275'),
    ('The Incidence of <b>Lumbar</b> Ligamentum Flavum Midline Gaps', 'https://www.researchgate.net/publication/8658490_The_Incidence_of_Lumbar_Ligamentum_Flavum_Midline_Gaps'),
    ('<b>Retrodural space of Okada</b> in the posterior ligamentous complex region. 2022', 'https://pubmed.ncbi.nlm.nih.gov/36241348/'),
    ('Contrast flow pattern in the <b>space of Okada</b> during interlaminar lumbar epidural injection', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11646783/'),
    ('<b>Epidural Contrast Patterns and Clinical Implications:</b> An Educational Review', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC12078379/'),
    ('<b>Fluoroscopic Subdural Contrast Flow Pattern</b> in the Lumbar Spine. <i>Pain Med</i> 2018', 'https://academic.oup.com/painmedicine/article/19/12/2571/5115550'),
    ('<b>Gill JS 등.</b> Contralateral oblique view is superior to lateral view for interlaminar epidural access. <i>Pain Med</i> 2015', 'https://academic.oup.com/painmedicine/article/16/1/68/2460452'),
    ('Novel method for modified interlaminar approach using <b>contralateral oblique view</b>. <i>PLOS One</i> 2021', 'https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0244992'),
    ('<b>Ghai B 등.</b> Lateral parasagittal versus midline interlaminar lumbar ESI. <i>Anesth Analg</i> 2013', 'https://pubmed.ncbi.nlm.nih.gov/23632053/'),
    ('Comparison between <b>DSA</b> and real-time fluoroscopy to detect intravascular injection. 2014', 'https://pubmed.ncbi.nlm.nih.gov/24918333/'),
    ('The rate of detection of intravascular injection with and without <b>DSA</b>. 2009', 'https://pubmed.ncbi.nlm.nih.gov/19627957/'),
    ('Accuracy of <b>live fluoroscopy</b> to detect intravascular injection', 'https://pmc.ncbi.nlm.nih.gov/articles/PMC2884208/'),
    ('Identification of the epidural space: is <b>loss of resistance to air</b> a safe technique? 1997', 'https://pubmed.ncbi.nlm.nih.gov/9010941/'),
    ('<b>Commonly-used versus less commonly-used methods</b> in the LOR technique: meta-analysis. 2017', 'https://pubmed.ncbi.nlm.nih.gov/28372676/'),
    ('Comparison of <b>Epidrum, Epi-Jet, and LOR syringe</b> in obstetric patients. 2017', 'https://pubmed.ncbi.nlm.nih.gov/28891544/'),
    ('Identification of the epidural space using pressure waveform analysis (<b>CompuFlo®</b>). 2019', 'https://pubmed.ncbi.nlm.nih.gov/31541259/'),
    ('<b>Acoustic puncture assist device (APAD):</b> a novel technique to identify the epidural space', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4799610/'),
    ('Electrophysiological stimulation (<b>Tsui test</b>) for epidural catheter positioning. 2013', 'https://pubmed.ncbi.nlm.nih.gov/23912567/'),
    ('<b>Autofluorescence</b> + fiberoptics for epidural space detection. <i>Sensors</i> 2018', 'https://doi.org/10.3390/s18113592'),
    ('Epidural anesthesia needle guidance by <b>OCT and deep learning</b>. <i>Sci Rep</i> 2022', 'https://www.nature.com/articles/s41598-022-12950-7'),
    ('<b>Systematic Review:</b> Particulate vs Nonparticulate Corticosteroids in Epidural Injections. 2016', 'https://pubmed.ncbi.nlm.nih.gov/27915069/'),
    ('<b>Park CH 등.</b> Epidurography Contrast Patterns after Adhesiolysis. <i>Pain Res Manag</i> 2018', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5901487/'),
]))


def build_html():
    css = open(FACES_CSS, encoding='utf-8').read()
    title = "요추 경막외 차단 · 문헌고찰"
    doc = render_deck(title, S)
    # deck_html의 폰트 플레이스홀더 4줄을 실제 @font-face 블록으로 교체
    doc = re.sub(r'@font-face\{font-family:Pretendard;font-weight:\d+;src:url\(__F\d+__\)[^}]*\}', '', doc, count=4)
    doc = doc.replace('<style>', '<style>' + css, 1)
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "LEB_발표_웹.html")
    open(out, 'w', encoding='utf-8').write(doc)
    n_photo = sum(1 for s in S if s['t'] == 'photo')
    n_filled = sum(1 for s in S if s['t'] == 'photo' for p in s['photos'] if p.get('src'))
    n_slots = sum(1 for s in S if s['t'] == 'photo' for p in s['photos'])
    print(f"HTML  → {out}  ({len(doc)/1024:.0f} KB, {len(S)}장)")
    print(f"사진 슬롯 {n_slots}개 중 {n_filled}개 채워짐 (사진 슬라이드 {n_photo}장)")
    return out


if __name__ == '__main__':
    build_html()
