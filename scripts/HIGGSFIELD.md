# 힉스필드 연결 상태와 이미지 로컬 저장 방법

실측일 2026-07-26 · 이 저장소의 Claude Code 원격 실행 환경 기준

## 요약

| 항목 | 상태 |
|---|---|
| 자연어로 이미지·영상 생성 요청 | **가능** — MCP 서버가 이미 연결돼 있다 |
| 생성물을 프로젝트 로컬 파일로 저장 | **가능하나 우회 필요** — 아래 "회수 경로" 참조 |
| 힉스필드 CLI 사용 | **불가** — 네트워크 차단 + CLI에 저장 기능 자체가 없음 |
| CDN을 curl로 직접 다운로드 | **불가** — 조직 egress 정책이 CloudFront를 차단 |

## 1. 자연어 생성 — 이미 된다

힉스필드 MCP 서버가 세션에 붙어 있다. 컨테이너의 네트워크 정책과 무관하게 동작한다.

- 이미지: `mcp__Higgsfield__generate_image`
- 영상: `mcp__Higgsfield__generate_video`
- 잔액: `mcp__Higgsfield__balance`
- 클라우드 샌드박스(ffmpeg·ImageMagick·Pillow·인터넷 가능): `mcp__Higgsfield__sandbox_exec`

공식 스킬도 설치돼 있다(`.claude/skills/higgsfield-*`). 다만 스킬은 **CLI를 전제**로
쓰여 있어 이 환경에서는 그대로 동작하지 않는다. MCP 툴을 직접 쓰는 편이 확실하다.

## 2. 네트워크 실측

`curl`이 `CONNECT tunnel failed, response 403`을 받으면 조직 egress 정책상 차단이다
(프록시 문서 `/root/.ccr/README.md` 기준: 재시도·우회 금지, 보고 대상).

**차단**
```
higgsfield.ai              fnf-api-gw.higgsfield.ai   clerk.higgsfield.ai
cloud.higgsfield.ai        upload.higgsfield.ai       *.cloudfront.net
```
**허용**
```
github.com   raw.githubusercontent.com   pypi.org   registry.npmjs.org
s3.amazonaws.com   www.googleapis.com
```

## 3. CLI가 답이 아닌 이유 — 두 가지 모두 확인함

CLI는 설치된다(npm 레지스트리는 허용). 하지만:

1. **API에 못 닿는다.**
   ```
   $ higgsfield workspace list
   Error: higgsfield: request failed (no response received)
   $ higgsfield auth login          # clerk.higgsfield.ai 도달 불가 → 행(hang)
   ```
2. **CLI에 로컬 저장 기능이 없다.** v1.1.19 바이너리의 플래그를 전수 조사했으나
   `--output-dir` · `--download` · `--save` · `--out` 중 **어느 것도 존재하지 않는다.**
   `generate create --help`도 `--wait`에 대해 "print the result URL(s)"라고만 적는다.
   공식 스킬 문서에서도 로컬 경로는 **입력(자동 업로드)** 용으로만 나온다.

   즉 CLI를 쓰더라도 마지막에는 CDN을 `curl` 해야 하는데, 그 CDN이 막혀 있다.

## 4. 실제로 동작하는 회수 경로 (현재 표준)

CDN을 컨테이너에서 직접 받지 않는다. 힉스필드 **클라우드 샌드박스**가 받아서
덱 크기로 줄인 뒤, MCP 툴 결과를 통해 base64로 회수한다.

1. `generate_image` 로 생성 (`resolution: "2k"`)
2. `show_generations` 로 `results.rawUrl` 확보
3. `sandbox_exec` 에서 내려받아 표시 크기에 맞춰 인코딩
   (덱 스테이지가 1200px이므로 가로 1400px WebP q80이면 충분하고 용량이 작다)
4. base64를 18,000자씩 잘라 회수 — MCP 툴 출력 상한이 약 20KB다
5. 로컬에서 이어붙여 `base64 -d`, **sha256으로 무결성 검증**
6. `assets/<이름>.webp` 로 저장하면 `build_lsb_web.py`의 `FIG()`가 자동으로 집는다

한 장(60~110KB)당 5~9회 왕복이면 된다. 장수가 많으면 회수 전용 서브에이전트에
맡겨 본 대화의 컨텍스트를 보호하는 편이 안전하다.

## 5. 근본 해결 — 정책에 호스트 허용

아래를 환경 네트워크 정책에 추가하면 CLI도, 직접 다운로드도 정상화된다.

```
fnf-api-gw.higgsfield.ai        API
clerk.higgsfield.ai             OAuth 로그인
upload.higgsfield.ai            업로드
d8j0ntlcm91z4.cloudfront.net    생성물 CDN  (또는 *.cloudfront.net)
```

설정 위치는 Claude Code 웹의 환경(Environment) 네트워크 정책이다.
**정책은 컨테이너 부팅 시 적용되므로 바꾼 뒤에는 새 세션에서 실행해야 한다.**

## 6. 빌드 환경 메모

새 컨테이너에서는 덱 빌드 의존성이 비어 있다. 다음을 먼저 실행한다.

```bash
pip install fonttools pillow python-pptx
curl -sSL -o /tmp/p.zip https://github.com/orioncactus/pretendard/releases/download/v1.3.9/Pretendard-1.3.9.zip
mkdir -p /tmp/pretendard && unzip -oq /tmp/p.zip -d /tmp/pretendard
cp /tmp/pretendard/public/static/Pretendard-{Black,ExtraBold,Bold,Light}.otf /tmp/pretendard/
python3 scripts/build_lsb_web.py
```
