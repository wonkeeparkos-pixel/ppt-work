# 내 컴퓨터(로컬 Claude Code)에서 LSB 덱 만들기

웹(원격 컨테이너)에서는 힉스필드·CDN이 네트워크 정책에 막히지만,
로컬에서는 내 인터넷을 그대로 쓰므로 그 제약이 없다.

## 1. 한 번만 하는 준비

```bash
git clone <이 저장소> && cd ppt-work
git checkout claude/lsb-presentation-media-analysis-rd17du

# 파이썬 의존성
pip install fonttools brotli pillow opencv-python-headless imageio-ffmpeg playwright python-pptx
playwright install chromium

# Pretendard 폰트 (저장소 안 fonts/ 로)
mkdir -p fonts && cd fonts \
  && npm pack pretendard \
  && tar xzf pretendard-*.tgz --strip-components=4 package/dist/public/static \
  && rm -f pretendard-*.tgz && cd ..
```

## 2. 덱 생성

```bash
python3 scripts/build_lsb_web.py
# → 문헌고찰_NLC_RLS_LSB/LSB_발표_웹.html (단일 파일, 폰트·그림 내장)
```

## 3. 힉스필드 그림 (선택)

```bash
npm i -g @higgsfield/cli
higgsfield auth login          # 로컬이므로 브라우저 OAuth가 정상 동작
higgsfield workspace set <id>

python3 scripts/hf_figures.py --check    # 네트워크·인증 점검
python3 scripts/hf_figures.py            # 4종 생성 → assets/hf_*.png
python3 scripts/build_lsb_web.py         # FIG()가 SVG를 그림으로 자동 교체
```

`assets/hf_axial.png` 같은 파일이 생기면 덱이 알아서 그 그림을 쓰고,
없으면 기존 SVG 도해로 폴백한다(`build_lsb_web.py`의 `FIG()`).

## 4. PPTX·PDF

각 슬라이드를 3배 해상도로 렌더한 PNG를 모아 조립한다.

```bash
python3 scripts/build_lsb_web_pptx.py build/hires
```

## 경로에 대하여

모든 스크립트는 **저장소 위치를 기준**으로 동작한다(절대경로 없음).
폰트는 `PRETENDARD_DIR` → `<저장소>/fonts` → `/tmp/pretendard` 순서로 찾고,
없으면 받는 명령을 안내하고 멈춘다.
