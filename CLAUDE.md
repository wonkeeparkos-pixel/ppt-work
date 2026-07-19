# ppt-work 프로젝트 지침

## 산출물 저장소: Google Drive (필수)

이 저장소의 모든 산출물(PPTX, DOCX, PDF, MD 등)은 GitHub 커밋과 별도로,
사용자의 Google Drive `claude` 폴더에도 **반드시 업로드**해야 한다.

- Drive 루트 폴더: `claude` — https://drive.google.com/drive/folders/1RlTMMQvpQTVw6pxHyBmVT6NFM0_wkKAB
- 이 저장소 전용 폴더: `claude/ppt-work` — folderId `16ulVmy9w176a6-Ncyhkf1n1ml9Eku8V5`

### Drive 폴더 ID 매핑 (저장소 구조와 1:1 대응)

| 저장소 경로 | Drive 폴더 | folderId |
|---|---|---|
| `/` (루트) | `claude/ppt-work` | `16ulVmy9w176a6-Ncyhkf1n1ml9Eku8V5` |
| `scripts/` | `claude/ppt-work/scripts` | `1SN1jIXnE5CiCdEKdCTh7xrFvG6af-Umd` |
| `문헌고찰_NLC_RLS_LSB/` | `claude/ppt-work/문헌고찰_NLC_RLS_LSB` | `1zVulAIZ76vqDyrQEY0x-NkysGqTSmDQN` |
| `문헌고찰_NLC_RLS_LSB/01_NLC/` | `.../01_NLC` | `1z4-PWxX1n1JYAj86DBFaFaKTRAQL2Brp` |
| `문헌고찰_NLC_RLS_LSB/02_RLS/` | `.../02_RLS` | `1oLppOQBYKr-3fgHiNqOGgXapHXDiNTBB` |
| `문헌고찰_NLC_RLS_LSB/03_LSB/` | `.../03_LSB` | `1RT0XdLQFDSTg6Tm5qY9cF2BBR4b2fMMQ` |

새 하위 디렉터리를 만들면 Drive에도 같은 이름의 폴더를 만들고
(`mcp__Google_Drive__create_file`, contentMimeType `application/vnd.google-apps.folder`)
위 표에 folderId를 추가할 것.

### 업로드 방법

`mcp__Google_Drive__create_file` MCP 도구 사용 (ToolSearch로 스키마 로드):

- `title`: 파일명 그대로, `parentId`: 위 표의 folderId
- `disableConversionToGoogleType: true` (원본 형식 유지)
- 바이너리(pptx/docx/pdf): `base64 -w0 <file>` 결과를 `base64Content`에
- 텍스트(md/py): 내용을 `textContent`에
- contentMimeType: pptx `application/vnd.openxmlformats-officedocument.presentationml.presentation`,
  docx `application/vnd.openxmlformats-officedocument.wordprocessingml.document`,
  pdf `application/pdf`, md `text/markdown`, py `text/plain`

### 크기 제한 주의

- 업로드 내용이 도구 호출에 인라인으로 들어가므로 **~150KB를 넘는 바이너리는 실패할 수 있다.**
- 큰 파일은 서브에이전트에게 업로드를 위임해 메인 컨텍스트를 아낄 것 (파일당 1회 호출).
- 큰 미리보기 PDF는 pikepdf로 재압축(`compress_streams=True`,
  `object_stream_mode=generate`, `recompress_flate=True`) 후 업로드하고,
  그래도 크면 업로드를 생략해도 된다 — Drive는 pptx/docx를 자체 미리보기로 열 수 있다.

## 비디오 스킬 (/watch)

`.claude/skills/watch/`에 [bradautomates/claude-video](https://github.com/bradautomates/claude-video)의
`/watch` 스킬이 설치되어 있다 (영상 URL·로컬 파일 → 프레임 + 대본 → 내용 분석).

**새 세션에서 처음 사용할 때 의존성 설치가 필요하다** (컨테이너가 임시라 매번 초기화됨):

```bash
pip install yt-dlp imageio-ffmpeg av cffi --upgrade
ln -sf "$(python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" /usr/local/bin/ffmpeg
cp .claude/ffprobe-shim.py /usr/local/bin/ffprobe && chmod +x /usr/local/bin/ffprobe
mkdir -p ~/.config/watch && printf 'WATCH_DETAIL=balanced\nSETUP_COMPLETE=true\n' > ~/.config/watch/.env
```

- `ffprobe-shim.py`는 apt로 ffmpeg를 못 깔기 때문에 PyAV로 ffprobe를 흉내내는 스크립트다 (스킬이 쓰는 JSON 필드만 지원).
- **주의: 이 원격 환경의 네트워크 정책은 YouTube 등 외부 영상 사이트를 차단한다** (프록시 403).
  URL 다운로드는 사용자가 환경 네트워크 정책을 완화해야 가능하고, 로컬 비디오 파일 분석은 바로 된다.
- Whisper API 키(GROQ_API_KEY/OPENAI_API_KEY)는 선택 사항 — 자막 없는 영상의 대본 추출에만 필요.

### 작업 완료 체크리스트

1. 산출물 생성/수정 → git 커밋·푸시 (기존 규칙대로)
2. 생성·변경된 산출물을 위 매핑에 따라 Drive에 업로드 (같은 파일명이면 새 버전으로 업로드)
3. 최종 응답에 Drive 링크 포함: https://drive.google.com/drive/folders/16ulVmy9w176a6-Ncyhkf1n1ml9Eku8V5
