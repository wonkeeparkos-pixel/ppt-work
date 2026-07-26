# 힉스필드 그림 회수 진행 상태 (작업용 메모)

컨텍스트가 압축돼도 이어서 작업할 수 있게 남기는 파일. 4장 모두 들어가면 삭제한다.

## 절차 (본체에서만 가능 — 서브에이전트는 sandbox_exec가 권한 분류기에 막힌다)

각 조각마다 `mcp__Higgsfield__sandbox_exec` 를 아래 명령으로 호출한다.
샌드박스는 호출 후 ~10초에 폐기되므로 **매번 재생성**해야 한다.
Pillow WebP 인코딩은 결정론적이라 재생성해도 바이트가 같다(sha256으로 확인함).

```
set -e; cd /home/user
B=https://d8j0ntlcm91z4.cloudfront.net/user_3GT8ygzdNn4HlTmVkTms2YtAvoj
mkdir -p out
[ -f out/NAME.png ] || curl -sS -o out/NAME.png "$B/SRC"
[ -f out/NAME.b64s ] || python3 -c "
from PIL import Image; import base64
im=Image.open('/home/user/out/NAME.png').convert('RGB')
r=im.resize((1000,round(im.height*1000/im.width)),Image.LANCZOS)
r.save('/home/user/out/NAME_s.webp','WEBP',quality=72,method=6)
open('/home/user/out/NAME.b64s','w').write(base64.b64encode(open('/home/user/out/NAME_s.webp','rb').read()).decode())
"
cut -c LO-HI out/NAME.b64s
```

출력(base64)을 그대로 `scratchpad/mine_<이름>/p<i>.txt` 에 Write 하고,
즉시 `tr -d '\n\r ' < p<i>.txt | wc -c` 로 길이를 확인한다.
**9,000자를 넘기면 중간 글자가 유실된다** (18,000자로 시도했다가 실제로 1자 유실).
틀리면 그 조각만 4,500자 반씩 다시 받는다.

전부 모이면:
```
cat p1.txt p2.txt ... | tr -d '\n\r ' > all.b64
base64 -d all.b64 > <이름>.webp
sha256sum <이름>.webp        # 아래 기대값과 대조
cp <이름>.webp 문헌고찰_NLC_RLS_LSB/03_LSB/assets/
```

## 원본 (힉스필드 job 결과, 2K PNG)

| 이름 | CDN 파일명 |
|---|---|
| hf_anatomy | hf_20260726_103441_7bd0a8dc-e9f1-4cac-b99c-127f559da571.png |
| hf_axial | hf_20260726_103445_189578c2-277a-4d9f-8074-45e52e918be1.png |
| hf_avoid | hf_20260726_103448_a537936c-1f56-48af-8fde-98635f8a3602.png |
| hf_contrast | hf_20260726_103452_82e66b77-6e9b-4476-8204-c0b574255cf8.png |

## 1000px q72 WebP 기대값

| 이름 | 바이트 | b64 길이 | 조각(9000자) | 마지막 조각 | sha256 |
|---|---|---|---|---|---|
| hf_anatomy | 33782 | 45044 | 6 | 44 | a91db800d59005fdc600125468e0e0a22362515a52c5c6b9a0093e77fe7ec564 |
| hf_axial | 62266 | 83024 | 10 | 2024 | 2fd99c2ab446db53e26a174352878d46ed52b7e7f2950228ac394e4977cc76b9 |
| hf_avoid | 50674 | 67568 | 8 | 4568 | 11e27767f8de9842e422fad59c32876392629cf4f40a4a92829a2c7803a485f5 |
| hf_contrast | 21594 | 28792 | 4 | 1792 | 8c88c390157e1f581769b3827a75dd901ea2edc485705a76266dc4b8ac2e7b73 |

조각 i의 범위: LO=(i-1)*9000+1, HI=i*9000 (마지막 조각만 HI=b64 길이).

## 진행

- [x] hf_contrast — 완료·검증·커밋 (d47a028)
- [ ] hf_anatomy — p1 확보(9000자), p2~p6 남음
- [ ] hf_avoid — 미착수 (8조각)
- [ ] hf_axial — 미착수 (10조각)

## 완료 후

`python3 scripts/build_lsb_web.py` 로 덱 재생성.
`FIG()`가 assets/hf_*.webp 를 자동으로 집어 6·21·22·24쪽에 넣는다.
빌드 의존성이 없으면 scripts/HIGGSFIELD.md 6절 참고.

## 그림 품질 메모 (재생성 필요 항목)

- **hf_contrast**: 조영제가 한 마디가 아니라 여러 마디를 따라 길게 흘러내렸다.
  슬라이드 메시지(종방향 한 마디 확산)와 반대. 프롬프트 강화해 재생성해야 한다.
