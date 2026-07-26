# 프로젝트 규칙

문헌고찰(NLC · RLS · LSB) 발표자료 빌드 저장소입니다.
아래 두 가지는 이 저장소의 확립된 규칙이며, 세션마다 다시 확인받지 않습니다.

## 1. 저장소는 구글 드라이브 한 곳만 쓴다

**완성된 산출물은 구글 드라이브에만 보관한다. 다른 클라우드는 쓰지 않는다.**

GitHub은 저장소가 아니라 빌드 소스 관리용이다. 따라서:

| 위치 | 담는 것 |
| --- | --- |
| **GitHub (이 레포)** | 빌드 스크립트(`scripts/*.py`), 빌드 입력 에셋(`**/assets/*`), 설정·규칙 파일 |
| **구글 드라이브** | 완성된 `.pptx` · `.docx` · `.pdf` · 발표용 HTML · 영상 등 모든 산출물 |

지켜야 할 것:

- 산출물을 GitHub에 커밋하지 않는다. `.gitignore`가 `*.pptx` / `*.docx` / `*.pdf`,
  그리고 `문헌고찰_NLC_RLS_LSB/` 아래 생성된 `.md` · `.html`을 막고 있다.
- 빌드해서 새 산출물이 나오면 구글 드라이브에 올린다.
- `.gitignore`를 우회해 산출물을 강제로 커밋(`git add -f`)하지 않는다.
- 예외: `**/assets/` 안의 이미지·영상은 산출물이 아니라 **빌드 입력물**이므로
  반드시 GitHub에 남긴다. `build_nlc_v*.py`가 이 파일들을 base64로 읽어
  HTML에 심기 때문에, 지우면 빌드가 깨진다.

산출물을 지우거나 옮기기 전에는 구글 드라이브에 사본이 있는지 먼저 확인한다.

## 2. 힉스필드는 자유롭게 쓴다

**Higgsfield MCP는 별도 승인 없이 자유롭게 사용한다.**

영상·이미지·오디오 생성, 업스케일, 리프레임, 잔액 조회 등 모든 도구를 바로 호출하면 된다.
접근 권한을 다시 묻거나 확인받을 필요가 없다.

단, 크레딧이 실제로 소모되는 생성 작업은 실행 전에 예상 비용과 잔액을 한 줄로 알린다
(접근을 막으려는 게 아니라, 지출을 눈에 보이게 하려는 것).

## 빌드 방법

```bash
python scripts/build_all.py          # 3개 주제 문헌고찰 docx + md 생성
python scripts/build_web_decks.py    # 발표용 웹 HTML 덱 생성
python scripts/build_nlc_v27.py      # NLC 발표자료 최신 버전
```

`scripts/content_nlc.py` · `content_rls.py` · `content_lsb.py`가 원문 콘텐츠이고,
`docx_lib.py` · `ppt_lib.py` · `deck_html.py`가 렌더링 라이브러리다.
**내용을 고칠 때는 생성된 `.docx`나 `.md`가 아니라 `content_*.py`를 고친다.**

의존 패키지: `pip install python-docx python-pptx fonttools`

## 폰트

`assets/fonts/`에 Pretendard 4종(Black · ExtraBold · Bold · Light)이 들어 있다.
`build_nlc_v*.py`와 `build_web_decks.py`가 이 폰트를 서브셋해 woff2로 HTML에 심는다.
스크립트는 `__file__` 기준 상대경로로 찾으므로 어느 디렉터리에서 실행해도 된다.

폰트도 빌드 **입력물**이므로 GitHub에 두고, 지우지 않는다.
Pretendard는 SIL Open Font License 1.1이라 재배포에 문제가 없다
(`assets/fonts/LICENSE.txt`).

이전에는 이 경로가 `/root/.claude/uploads/<세션 UUID>/`로 하드코딩되어 있었다.
그 디렉터리는 세션이 끝나면 사라지므로 다른 세션에서는 빌드가 전부 실패했다.
**빌드 입력물을 세션 임시 경로에서 참조하지 않는다** — 저장소 안에 두거나
구글 드라이브에서 받아온다.
