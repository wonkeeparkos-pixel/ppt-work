# -*- coding: utf-8 -*-
"""LSB 덱 그림 4종의 힉스필드 프롬프트 원본 + 회수 경로 기록.

■ 그림 4종
    hf_anatomy   6쪽   관상면+축상면 통합 해부도        16:9
    hf_axial    21쪽   L2 축상면 해부도                 3:2
    hf_avoid    22쪽   대혈관·신장 회피(위험구조 강조)  3:2
    hf_contrast 24쪽   조영제 종방향 확산(투시상)       3:2
  모델 nano_banana_pro(= nano_banana_2), resolution 2k.
  한글 라벨은 모델이 깨뜨리므로 '문자 없이 그림만' 생성하고 라벨은 덱에서 얹는다.

■ 이 컨테이너의 네트워크 실측 (2026-07-26)
  차단(에이전트 프록시가 CONNECT를 403으로 거부 = 조직 egress 정책):
      higgsfield.ai / fnf-api-gw.higgsfield.ai / clerk.higgsfield.ai
      cloud.higgsfield.ai / upload.higgsfield.ai
      d8j0ntlcm91z4.cloudfront.net  ← 생성물 CDN
  허용:
      github.com / raw.githubusercontent.com / pypi.org / registry.npmjs.org
      s3.amazonaws.com / www.googleapis.com

■ 힉스필드 CLI로는 안 된다 — 두 가지 이유 모두 실측 확인
  1) 인증·API 호출 자체가 막힌다.
       higgsfield workspace list -> "request failed (no response received)"
       higgsfield auth login      -> clerk.higgsfield.ai 도달 불가로 행
  2) CLI에 로컬 저장 기능이 아예 없다. v1.1.19 바이너리의 플래그를 전수
     조사했으나 --output-dir / --download / --save / --out 이 존재하지 않는다.
     `generate create --help`도 "print the result URL(s)"라고만 적혀 있다.
     즉 CLI를 쓰더라도 결국 CDN을 curl 해야 하는데, 그 CDN이 막혀 있다.

■ 그래서 실제로 쓴 경로 (MCP)
  힉스필드 MCP 서버는 세션에 연결돼 있고 정상 동작한다(컨테이너 egress와 무관).
    1. mcp__Higgsfield__generate_image 로 4장 생성 (2크레딧/장)
    2. mcp__Higgsfield__sandbox_exec (힉스필드 클라우드 샌드박스, 인터넷 가능)
       에서 CDN PNG를 받아 가로 1400px WebP q80으로 축소·인코딩
    3. base64로 쪼개 MCP 툴 결과를 통해 회수 → sha256으로 무결성 검증
  결과물은 assets/hf_*.webp 로 저장되고 build_lsb_web.py의 FIG()가 자동으로 집는다.

■ 이 파일을 다시 자동화하려면 (권장)
  환경 네트워크 정책에 아래 호스트를 허용하면 CLI/직접 다운로드가 살아난다.
      fnf-api-gw.higgsfield.ai   API
      clerk.higgsfield.ai        OAuth
      d8j0ntlcm91z4.cloudfront.net (또는 *.cloudfront.net)  생성물 CDN
      upload.higgsfield.ai       업로드
  정책은 컨테이너 부팅 시 적용되므로 바꾼 뒤에는 새 세션에서 실행할 것.
"""

MODEL = "nano_banana_pro"
RESOLUTION = "2k"

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

if __name__ == "__main__":
    import os
    ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "문헌고찰_NLC_RLS_LSB", "03_LSB", "assets")
    for k, v in FIGURES.items():
        have = next((e for e in ("webp", "jpg", "png")
                     if os.path.exists(os.path.join(ASSETS, f"{k}.{e}"))), None)
        print(f"  {k:<14} {v['aspect']:<6} {'assets/%s.%s' % (k, have) if have else '없음(SVG 폴백)'}")
