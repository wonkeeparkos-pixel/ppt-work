# 정형외과 통증과 보툴리눔 톡신 — 문헌고찰 발표 (40슬라이드)

## 이 폴더에 뭐가 있나

| 파일 | 용도 |
|---|---|
| `보툴리눔_정형외과통증_발표_웹.html` | **웹 덱** — 브라우저로 열면 바로 발표. 폰트까지 전부 파일 안에 들어 있어 인터넷 없이도 열린다 |
| `보툴리눔_정형외과통증_발표.pptx` | **PowerPoint** — 40쪽, 각 쪽이 16:9 이미지. 어느 PC에서든 열리고 저장된다 |
| `보툴리눔_정형외과통증_발표_미리보기.pdf` | 인쇄·공유용 |
| `참고문헌.md` | 34편 문헌 표 + 부위별 용량 요약 |

**그냥 발표만 할 거면 위 파일들만 있으면 된다.** 아래는 내용을 고쳐서 다시 뽑을 때 이야기.

---

## 내 컴퓨터에서 이어서 작업하기

### 1. 저장소 받기

```bash
git clone https://github.com/wonkeeparkos-pixel/ppt-work.git
cd ppt-work
git checkout claude/botox-orthopedic-pain-treatment-6rd0qo
```

그 폴더에서 Claude Code를 실행하면(`claude`) 이 작업을 그대로 이어받는다.

### 2. 필요한 것 설치 (최초 1회)

```bash
pip install python-pptx fonttools playwright pillow
playwright install chromium
```

- Python 3.9 이상
- Pretendard 폰트는 `assets/fonts/`에 동봉되어 있다(SIL OFL 1.1) — 따로 설치할 필요 없음
- 스크립트는 저장소 위치를 스스로 찾으므로 어느 경로에 두든 동작한다

### 3. 고치고 다시 뽑기

내용은 **`scripts/content_botox.py` 한 파일**에 다 있다. 슬라이드 하나가 딕셔너리 하나다.

```bash
python3 scripts/build_botox_v1.py     # 내용 → 웹 덱 HTML (폰트 서브셋 임베드)
python3 scripts/check_overflow.py     # 40쪽 중 글자가 넘치는 쪽이 있는지 검사
python3 scripts/render_botox_png.py   # 각 쪽을 2560×1440 PNG로
python3 scripts/build_botox_pptx.py   # PNG → PPTX + 미리보기 PDF
```

`check_overflow.py`가 `0 / 40 slides overflow`라고 나와야 정상이다. 넘치면 해당 쪽 문장을 줄이거나 표에 `'dense': True`를 준다.

### 4. 슬라이드 종류

`scripts/deck_botox_html.py`가 이 덱 전용 렌더러다(테마 **차단 / Blockade**).
NLC·RLS·LSB 덱은 그대로 `scripts/deck_html.py`(Clinical Ledger)를 쓴다 — 두 테마는 서로 독립이다.

`content_botox.py`에서 쓰는 타입:

| `'t'` | 모양 |
|---|---|
| `title` | 표지 |
| `bullets` | 제목 + 불릿 (+ `note`, `stat`) |
| `split` | 왼쪽 불릿 + 오른쪽 카드(`aside`: `items` 또는 `stat`) |
| `table` | 표 (+ `hlrows` 강조행, `dense` 조밀 모드) |
| `figure` | 나란한 패널 2–3개 (SVG 일러스트) |
| `bigfig` | 넓은 SVG 한 장 |
| `key` | 짙은 배경 요약 |
| `refs` | 참고문헌 2단 (PubMed 링크) |

일러스트는 두 종류다.

- **인라인 SVG** — `content_botox.py` 상단에 직접 그린 주사기법 도해(승모근·사각근·비복근·족저근막·요추·이상근 등).
- **생성 일러스트** — `assets/fig/*.webp` (03쪽 기전 2장). Higgsfield로 **글자 없이** 생성하고,
  한글 라벨은 `.figimg .lb`로 % 좌표에 얹는다. AI 생성기는 한글을 깨뜨리므로 그림 안에 글자를 넣지 않는다.

둘 다 빌드 시 HTML에 임베드되므로 외부 참조가 하나도 없다 — HTML 한 파일만 옮겨도 그대로 보인다.

### 5. 테마 규칙 — "차단 / Blockade"

| 요소 | 값 | 뜻 |
|---|---|---|
| 구조색 | 인디고 `#463A96` | 신경계 |
| 바탕 | `#F4F3F8` | 100 U 바이알 유리 |
| 벽돌 `#A8352A` | 독소·차단·경고 | 기흉, 근력약화, 박스경고 |
| 모스 `#2E6B3E` | 검증된 근거 | Level A·B |
| 앰버 `#B0701A` | 근거 상충 | Level C |
| 슬레이트 `#6B7280` | 근거 없음 | Level U |

- **슬라이드 최상단 2px 라인 = 그 쪽 태그의 색.** 즉 색이 곧 근거등급이다. `'tag': ('Level B · RCT', 'green')` 처럼 태그에 색을 주면 상단 라인이 자동으로 따라간다.
- **용량·단위·라벨은 JetBrains Mono**, 본문은 Pretendard. 숫자가 열을 맞춰야 하는 곳은 `tabular-nums`.
- 표지의 **100칸 격자 = 한 바이알 100 U**. 장식이 아니라 이 발표의 기준 단위를 뜻한다.
- 본문은 **목 → 발** 해부학적 순서로 내려가고(목·어깨 → 어깨 → 팔 → 허리 → 엉덩이 → 무릎 → 종아리 → 발), 부위를 가리지 않는 **수술후 절개부 신경통**을 맨 뒤에 둔다.

---

## 주의

- 정형외과 통증에서 보툴리눔은 **대부분 허가초과(off-label)** 사용이다. 국내 급여는 뇌졸중 후 상지경직(발병 3년 내, MAS 2–3등급, 1회 ≤300 U, 간격 ≥3개월) 등에 한정된다.
- 발표 전 `참고문헌.md`의 PMID로 핵심 수치를 한 번 대조할 것.
