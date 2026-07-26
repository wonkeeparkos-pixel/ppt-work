# -*- coding: utf-8 -*-
"""힉스필드 CLI로 LSB 덱 그림을 생성·내려받아 assets/에 넣는다.

전제
  npm i -g @higgsfield/cli
  higgsfield auth login          # 브라우저 OAuth (PKCE)
  higgsfield workspace set <id>

네트워크
  이 스크립트는 아래 호스트에 직접 나간다. 환경 네트워크 정책에 모두 열려 있어야 한다.
    fnf-api-gw.higgsfield.ai   API 게이트웨이
    clerk.higgsfield.ai        OAuth
    higgsfield.ai / cloud.higgsfield.ai
    *.cloudfront.net           생성물 CDN
  정책은 컨테이너 부팅 시점에 적용되므로, 정책을 바꿨으면 새 세션에서 실행할 것.

사용
  python3 scripts/hf_figures.py --list            # 정의된 그림 목록
  python3 scripts/hf_figures.py --check           # 네트워크·인증만 점검
  python3 scripts/hf_figures.py --only hf_axial   # 하나만 생성
  python3 scripts/hf_figures.py                   # 전부 생성

생성이 끝나면 assets/<이름>.png 가 놓이고, build_lsb_web.py 의 FIG()가
자동으로 SVG 대신 이 파일을 쓴다. 덱 재생성:
  python3 scripts/build_lsb_web.py
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.request

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "문헌고찰_NLC_RLS_LSB", "03_LSB", "assets")
MODEL = "nano_banana_pro"          # 도해·텍스트에 가장 강한 모델
HOSTS = ["fnf-api-gw.higgsfield.ai", "clerk.higgsfield.ai", "higgsfield.ai"]

# 라벨은 모델에게 맡기지 않는다 — 한글이 깨지므로 그림만 받고 라벨은 우리가 얹는다.
NO_TEXT = ("절대 금지: 어떤 문자·숫자·라벨·화살표·워터마크도 넣지 말 것. "
           "absolutely NO text, NO letters, NO numbers, NO labels, NO watermark.")

FIGURES = {
    # 6쪽 — 두 내용(요추 레벨 + 신경간과 대혈관 관계)을 한 장에 담은 해부도
    "hf_anatomy": dict(aspect="16:9", prompt=(
        "Single unified medical textbook anatomical illustration that combines TWO views "
        "side by side within one continuous scene, Netter-style, flat muted anatomical "
        "colors, plain white background.\n"
        "LEFT HALF — coronal (frontal) view of the lumbar spine T12 to L5: vertebral bodies "
        "stacked in the midline, the abdominal aorta descending just left of the midline and "
        "bifurcating at L4, the inferior vena cava to its right, and the paired lumbar "
        "sympathetic trunks as pale-yellow beaded chains running vertically along the "
        "anterolateral corners of the vertebral bodies, hugging the aorta on the left.\n"
        "RIGHT HALF — axial (transverse) cross-section at the L2 level of the same patient: "
        "vertebral body centre, spinal canal behind it, psoas major muscles anterolateral, "
        "quadratus lumborum and erector spinae posteriorly, aorta anterior-left, inferior "
        "vena cava anterior-right, both kidneys posterolateral, and the sympathetic ganglion "
        "sitting in the groove at the anterolateral corner of the vertebral body between the "
        "bone and the medial edge of psoas.\n"
        "The two halves must read as one coherent figure, same drawing style and palette, "
        "separated only by generous white space. " + NO_TEXT)),

    # 21쪽 — L2·L3 축상면 해부도
    "hf_axial": dict(aspect="3:2", prompt=(
        "Medical textbook anatomical illustration: axial (transverse) cross-section of the "
        "human abdomen at the L2 lumbar vertebral level. Netter style, flat muted anatomical "
        "colors, crisp outlines, plain white background.\n"
        "Precise relationships: vertebral body centre with spinous process posteriorly and "
        "paired transverse processes laterally; triangular spinal canal with cauda equina "
        "immediately behind the body; psoas major muscles hugging the anterolateral corners; "
        "quadratus lumborum lateral to psoas; erector spinae posteriorly; abdominal aorta "
        "anterior and slightly LEFT of the body; inferior vena cava anterior and RIGHT of it; "
        "both kidneys in the posterolateral retroperitoneum; ureters on the anterior surface "
        "of each psoas; a small pale-yellow sympathetic ganglion in the groove at each "
        "anterolateral corner of the vertebral body. " + NO_TEXT)),

    # 22쪽 — 혈관·신장 회피 (위험 구조 강조)
    "hf_avoid": dict(aspect="3:2", prompt=(
        "Medical textbook axial cross-section at the L2 lumbar level, same Netter style and "
        "palette as a standard anatomy atlas, plain white background. The danger structures "
        "must be visually dominant and unambiguous: the abdominal aorta anterior-LEFT of the "
        "vertebral body rendered in strong red, the inferior vena cava anterior-RIGHT in "
        "strong blue, and both kidneys large and clearly separated in the posterolateral "
        "retroperitoneum. The vertebral body, psoas major, spinal canal and transverse "
        "processes are present but rendered in quiet neutral tones so the vessels and kidneys "
        "stand out. Leave clear empty space around the posterolateral approach corridor "
        "running from the skin of the back down to the anterolateral corner of the vertebral "
        "body. " + NO_TEXT)),

    # 24쪽 — 조영제 종방향 확산 (한 마디 정도)
    "hf_contrast": dict(aspect="3:2", prompt=(
        "Realistic C-arm fluoroscopy still, LATERAL view of the lumbar spine, authentic "
        "grayscale radiograph with image-intensifier vignetting, circular field of view.\n"
        "Lumbar bodies L1-L4 in true lateral profile. A fine spinal needle enters from behind "
        "with its tip at the ANTERIOR margin of the L2 body. Radiopaque contrast forms a THIN "
        "NARROW LINEAR streak hugging the anterior surface of the bone, spreading only "
        "craniocaudally and spanning only about ONE vertebral body height in total — a tight "
        "restrained band, NOT a blob, NOT a wide cloud, NOT running the length of the spine, "
        "and NOT entering the disc space or the spinal canal. " + NO_TEXT)),
}


def run(*args, timeout=180):
    p = subprocess.run(["higgsfield", *args], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def check():
    """네트워크·인증을 먼저 점검한다 — 실패 원인을 분명히 갈라 보여준다."""
    ok = True
    for h in HOSTS:
        rc = subprocess.run(["curl", "-sS", "-o", "/dev/null", "--max-time", "12",
                             f"https://{h}/"], capture_output=True).returncode
        state = "열림" if rc == 0 else "차단"
        if rc != 0:
            ok = False
        print(f"  {h:<30} {state}")
    if not ok:
        print("\n→ 네트워크 정책이 막고 있다. 정책을 바꿨다면 '새 세션'에서 실행할 것"
              "(정책은 컨테이너 부팅 시 적용된다).")
        return False
    rc, out, err = run("auth", "token")
    if rc != 0:
        print("\n→ 인증이 없다. 실행: higgsfield auth login")
        return False
    print("  인증 상태                        정상")
    return True


def generate(name, spec):
    print(f"[{name}] 생성 요청 …")
    rc, out, err = run("generate", "create", MODEL, "--prompt", spec["prompt"],
                       "--aspect-ratio", spec["aspect"], "--json")
    if rc != 0:
        print(f"[{name}] 실패: {err or out}")
        return False
    job = json.loads(out)
    jid = job.get("id") or (job.get("results") or [{}])[0].get("id")
    print(f"[{name}] job {jid} — 대기 중 …")
    rc, out, err = run("generate", "wait", jid, "--json", timeout=900)
    if rc != 0:
        print(f"[{name}] 대기 실패: {err or out}")
        return False
    res = json.loads(out)
    url = (res.get("results") or {}).get("rawUrl") if isinstance(res.get("results"), dict) else None
    if not url:  # 응답 형태가 배열인 경우
        items = res if isinstance(res, list) else res.get("results") or []
        for it in items:
            url = (it.get("results") or {}).get("rawUrl")
            if url:
                break
    if not url:
        print(f"[{name}] 결과 URL을 찾지 못했다: {out[:300]}")
        return False
    dest = os.path.join(ASSETS, f"{name}.png")
    urllib.request.urlretrieve(url, dest)
    print(f"[{name}] 저장 → {dest} ({os.path.getsize(dest)/1024:.0f}KB)")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", action="append", default=[])
    a = ap.parse_args()

    if a.list:
        for k, v in FIGURES.items():
            have = "있음" if os.path.exists(os.path.join(ASSETS, f"{k}.png")) else "없음"
            print(f"  {k:<14} {v['aspect']:<6} assets/{k}.png: {have}")
        return
    if a.check:
        sys.exit(0 if check() else 1)
    if not check():
        sys.exit(1)

    targets = a.only or list(FIGURES)
    fails = [n for n in targets if not generate(n, FIGURES[n])]
    print("\n완료." if not fails else f"\n실패: {', '.join(fails)}")
    print("이제 실행: python3 scripts/build_lsb_web.py")


if __name__ == "__main__":
    main()
