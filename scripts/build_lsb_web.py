# -*- coding: utf-8 -*-
"""LSB(요추교감신경차단) 웹 발표 덱 전용 빌더 — Pretendard 서브셋 임베드.
build_web_decks.py의 LSB 정의를 기반으로 하되, LSB 한 덱만 재생성한다(NLC/RLS 불변).
폰트는 /tmp/pretendard 우선, 없으면 기존 업로드 경로 폴백."""
import os, sys, re, base64, io
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck
from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026"
def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
def PMC(x): return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x}/"

LSB = [
 {'t':'title','eyebrow':'Lumbar Sympathetic Block · 문헌고찰','title':'요추교감신경차단',
  'sub':'방법 · 적응증 · 효과','order':'Technique · Indications · Efficacy','series':SERIES},
 {'t':'bullets','eyebrow':'개요','tag':('배경',''),'title':'개요 · 해부 · 원리','foot':'StatPearls NBK431107; Zhang 2022 (Ibrain)','items':[
   (0,'LSB와 교감신경 신경파괴(sympatholysis)는 70년 이상 다양한 하지 통증·허혈 질환에 사용.',''),
   (0,'표적: 신경절 밀도가 가장 높은 <b>L2–L3</b>(척추체 전외측). 일부 L2/L3/L4 다분절.',''),
   (0,'원리 ①: 교감신경 차단 → 혈관 확장·측부순환 증가 → 조직 산소화 개선.',''),
   (0,'원리 ②: 교감신경 매개 통증(sympathetically-maintained pain) 경로·자율신경 동반 구심로 차단.',''),
   (-1,'국소마취제 차단(진단적/치료적)과 화학적/열적 신경파괴로 나뉜다.','accent'),
 ]},
 {'t':'split','eyebrow':'방법','tag':('기법',''),'title':'방법 (Technique)','foot':'StatPearls NBK431107 · NBK560514',
  'items':[
   (0,'<b>표준: 방척추(paravertebral) 접근 + 투시(fluoroscopy).</b> CT·초음파도 가능.',''),
   (0,"바늘 진입: 정중선에서 약 7 cm 외측. 척추체 접촉 후 전내측으로 'walk'하여 척추체 전외측으로 진입.",''),
   (0,'흡인 후 조영제 주입 → 두미측(craniocaudal) 종방향 확산 확인.',''),
   (0,'<b>성공 지표: 동측 하지 피부온도 ≥2°C 상승.</b>',''),
  ],
  'aside':{'title':'약제','items':[
   (0,'진단/치료: lidocaine 1%,',''),(0,'bupivacaine 0.25–0.5%, ropivacaine',''),
   (0,'신경파괴: 무수알코올/phenol, RFA',''),(-1,'신경파괴는 진단적 차단 양성 시에만','accent'),
  ]}},
 {'t':'table','eyebrow':'적응증','tag':('적응',''),'title':'적응증 (Indications)','foot':'StatPearls; 문헌고찰 종합',
  'note':"특발성 야간 하지경련(NLC)은 적응증 아님 — '밤 다리증상'이 허혈성 안정통(PAD/CLI)이면 적응. 원인 감별(ABI·도플러) 선행.",
  'headers':['범주','대표 적응증'],'rows':[
   ['통증증후군','하지 복합부위통증증후군(CRPS I/II) — <b>조기(≤12개월) 시행 유리</b>'],
   ['허혈질환','PAD·중증 하지허혈(CLI) 안정통·비재건성, 버거병, 색전, 동상, 혈관연축'],
   ['신경병증','당뇨병성 신경병증/당뇨발, 대상포진후신경통, 환상지통·단단통'],
   ['기타','족부 다한증, 레이노 증후군(하지)·홍색사지통증, 암성 골반/하지통'],
  ]},
 # ---------- NEW: 적응증별 환자 증상·호소 ① ----------
 {'t':'bullets','eyebrow':'적응증 · 증상','tag':('환자 증상',''),'title':'적응증별 환자 증상·호소 ① — 통증증후군·허혈','foot':'StatPearls; 문헌고찰 종합',
  'note':"‘허혈’은 <b>동맥성</b> 부족을 의미 — 하지정맥류 등 <b>정맥질환은 LSB 적응증 아님</b>(압박·정맥폐색술이 표준).",
  'items':[
   (0,'<b>하지 CRPS I/II (복합부위통증증후군)</b> — 교감신경 매개 통증의 전형',''),
   (1,'<b>작열통·이질통</b>(옷·바람 스침에도 통증)·통각과민 · 부종 · 피부색(발적↔창백)·<b>좌우 온도차</b> · 발한 이상',''),
   (1,'호소: “발이 타는 듯 화끈거려요” · “이불만 스쳐도 아파요” · “붓고 색이 자꾸 변해요”','muted'),
   (0,'<b>허혈질환 — PAD·중증 하지허혈(CLI)·버거병</b> (동맥성 허혈)','green'),
   (1,'<b>간헐적 파행</b>(걷다 종아리 통증→쉬면 완화) → 진행 시 <b>야간 안정통</b>(다리 내리면 완화) · 차고 창백한 발 · <b>비치유 궤양·괴저</b>',''),
   (1,'호소: “걸으면 종아리가 터질 듯 아파요” · “밤에 발이 시려 잠을 못 자요” · “상처가 안 아물어요”','muted'),
  ]},
 # ---------- NEW: 적응증별 환자 증상·호소 ② ----------
 {'t':'bullets','eyebrow':'적응증 · 증상','tag':('환자 증상',''),'title':'적응증별 환자 증상·호소 ② — 신경병증·기타','foot':'StatPearls; 문헌고찰 종합',
  'items':[
   (0,'<b>신경병증 — 당뇨병성 신경병증/당뇨발·대상포진후신경통·환상지통</b>',''),
   (1,'<b>저림·화끈거림·전기 오듯 찌름</b> · 이질통 · 감각저하(양말 신은 느낌) · <b>야간 악화</b> · 당뇨발 궤양·관류저하',''),
   (1,'호소: “발이 저리고 화끈거려요” · “밤에 더 심해요” · “전기가 찌릿 오는 것 같아요”','muted'),
   (0,'<b>기타 — 족부 다한증·레이노(하지)·홍색사지통증·암성 하지통</b>',''),
   (1,'다한증(과한 발땀·축축·악취) · 레이노(추위·스트레스에 <b>창백→청색→발적</b> 삼색변화·저림) · 홍색사지통증(발작적 <b>발적·작열·열감</b>, 열에 악화)',''),
   (1,'호소: “발에 땀이 너무 많아요” · “추우면 발이 하얘졌다 파래져요” · “발이 화끈 달아올라요”','muted'),
  ]},
 # ---------- NEW: 야간 신경병증통 서사 + LSB 치료 삽입 (NLC 스타일) ----------
 {'t':'split','eyebrow':'적응증 · 심화','tag':('야간 신경병증통',''),
  'title':'밤에 저리고 화끈거리는 다리 — 당뇨병성 신경병증과 LSB','foot':'Zhang 2020(RCT) PMID 32915421; 증례 PMID 22606406; StatPearls NBK442009',
  'items':[
   (0,'<b>임상상:</b> 당뇨병성 말초신경병증 — 발·종아리 <b>저림·화끈거림·전기 찌름</b>, 양측 ‘양말’ 분포.',''),
   (0,'<b>야간통:</b> 이불 온기·야간 순환·주의분산 소실 → 밤에 증폭·수면 방해.',''),
   (0,'<b>감별:</b> RLS(움직이면 완화)·NLC(경련)·허혈성 안정통과 구분.',''),
   (-1,'1차: 혈당조절+약물(가바펜틴·듀록세틴) → 난치성이면 <b>LSB 고려</b>','accent'),
  ],
  'aside':{'title':'LSB — 치료 삽입','dark':True,'items':[
   (0,'<b>기전:</b> 교감차단 → <b>미세순환↑</b> + 교감매개통 차단.',''),
   (0,'<b>근거:</b> 난치성 DPN에 LSB+신경파괴 <b>RCT</b>·증례.',''),
   (0,'<b>적용:</b> 진단차단 양성 시 선택적 시행.',''),
  ]}},
 {'t':'split','eyebrow':'효과','tag':('효과','green'),'title':'효과 ① 관류 개선 · 허혈성 통증','foot':'Dickey 2024 (Cureus); Medicina 2024; Barreto 2018',
  'items':[
   (0,'<b>관류 실측(Dickey 2024):</b> LSB 후 후경골동맥 직경 0.17→0.27 cm(+58.8%), 모세혈관 재충혈 3.92→1.30초, 족부온도 +2.8°C.',''),
   (0,'허혈성 통증(PAD): 하지 통증 최대 <b>75%↓</b>, Fontaine 분류·측부관류 개선(Medicina 2024).','green'),
   (0,'비재건성 CLI: 교감신경 신경파괴가 절단 외 대안이 없는 환자의 통증조절에 효과적·안전(Barreto 2018).',''),
  ],
  'aside':{'title':'실측 수치 (Dickey 2024)','stat':[('+58.8%','후경골동맥 직경'),('+2.8°C','족부온도'),('3.92→1.30s','모세혈관 재충혈')]}},
 {'t':'bullets','eyebrow':'효과','tag':('효과','green'),'title':'효과 ② CRPS · 기전','foot':'Choi 2024 (Sci Rep); Pain Ther 2023','items':[
   (0,'CRPS는 교감신경 매개 통증의 전형 → LSB 후 유의한 통증완화. 최적 환자 선택·조기 시행이 성공률↑.',''),
   (0,'Choi 2024(Sci Rep): 교감신경 신경파괴의 효과 지속기간을 전향 관찰로 제시.',''),
   (0,'반응 예측: <b>교감신경 피부반응(SSR)</b>이 LSB 반응 예측에 유용(Pain Ther 2023).',''),
   (0,'한계: 중추 감작이 진행되면 시간이 지날수록 효과 감소 가능.','muted'),
   (-1,'기전: 교감차단 → 측부순환 혈관확장 → 조직 산소화↑ → 통증↓ + 교감매개통 차단 + 신경파괴 직접효과.','accent'),
 ]},
 {'t':'bullets','eyebrow':'안전성 · 결론','tag':('안전성','red'),'title':'합병증 · 근거수준 · 결론','foot':'StatPearls; 문헌고찰 종합','items':[
   (0,'합병증: <b>생식대퇴신경통(신경파괴 시 5–10%)</b>, 외측대퇴피신경 손상, 기립성 저혈압.','red'),
   (0,'혈관·요관·신장 등 내장 구조 천공, 출혈, 신경축 확산, 신경파괴 후 통증성 신경염(dysesthesia).',''),
   (0,'근거수준: 대부분 관찰·증례군·소규모 전향연구, 대규모 RCT는 부족(허혈질환·CRPS Lv III~IV).',''),
   (-1,'그럼에도 조기 CRPS·재건 불가능한 중증 하지허혈(안정통)에서 임상적으로 유용.','accent'),
 ]},
 {'t':'key','eyebrow':'핵심 메시지 · LSB','headline':'표준은 투시 유도 방척추 접근, 성공은 온도 ≥2°C','msgs':[
   ('방법','L2–L3 방척추 접근·투시, 정중선 7 cm 외측, 조영제 두미측 확산, 성공지표 온도 ≥2°C.'),
   ('약제','진단/치료는 국소마취제, 신경파괴는 무수알코올/phenol·RFA — 진단차단 양성 시에만.'),
   ('적응증','조기 CRPS·PAD/CLI 안정통·신경병증·다한증 등. 특발성 NLC·정맥질환(정맥류)은 적응 아님.'),
   ('효과','관류 실측 개선(Dickey), 허혈통 최대 75%↓, CRPS 통증완화(SSR로 예측).'),
   ('근거','대규모 RCT 부족(관찰·증례 중심). 조기 CRPS·비재건성 CLI에서 유용.'),
 ]},
 {'t':'refs','title':'참고문헌 — LSB','refs':[
   ('<b>Dua & Varacallo.</b> Lumbar sympathetic block. StatPearls. 2026.','https://www.ncbi.nlm.nih.gov/books/NBK431107/'),
   ('Lumbar sympatholysis. StatPearls.','https://www.ncbi.nlm.nih.gov/books/NBK560514/'),
   ('<b>Zhang.</b> Lumbar sympathetic ganglion block in lower limb pain. Ibrain. 2022.',PM(37786587)),
   ('<b>Dickey & Sharma.</b> LSB increases arterial diameter and blood flow. Cureus. 2024.',PM(38975506)),
   ('<b>Barreto.</b> Neurolytic block of lumbar sympathetic chain in CLI. Braz J Anesthesiol. 2018.',PMC('PMC9391669')),
   ('<b>Choi.</b> Effect duration of lumbar sympathetic neurolysis in CRPS. Sci Rep. 2024.',PM(38830944)),
   ('<b>Gungor.</b> Sympathetic blocks for CRPS: case series. Medicine. 2018.',PM(29742728)),
   ('LSB on pain, Fontaine, perfusion in PAD. Medicina (Kaunas). 2024.','https://doi.org/10.3390/medicina60050682'),
   ('LSB efficacy in CRPS-1 by sympathetic skin response. Pain Ther. 2023.',PMC('PMC10199976')),
   ('<b>Continuous LSB + sympatholysis for refractory painful diabetic neuropathy — RCT.</b> 2020.',PM(32915421)),
   ('Sympathetic blocks: sustained relief in refractory painful diabetic neuropathy (case). 2012.',PM(22606406)),
   ('Lumbar sympathectomy for ischaemia·vasculitis·diabetic neuropathy·hyperhidrosis — series. 2018.',PM(29516399)),
 ]},
]

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"
TITLE = "요추교감신경차단 · 문헌고찰 발표"
FNAME = "LSB_발표_웹"

# ---- font sources: /tmp/pretendard 우선, 없으면 업로드 경로 폴백 ----
TMP = "/tmp/pretendard"
UP = "/root/.claude/uploads/bb19d1cb-d1ba-542e-8235-38fcac774773/"
def pick(tmp_name, up_name):
    p = os.path.join(TMP, tmp_name)
    return p if os.path.exists(p) else (UP + up_name)
FONTS = {
  "__F900__": pick("Pretendard-Black.otf",     "c71b728f-PretendardBlack.otf"),
  "__F800__": pick("Pretendard-ExtraBold.otf", "3a19e05c-PretendardExtraBold.otf"),
  "__F700__": pick("Pretendard-Bold.otf",      "1121d3ff-PretendardBold.otf"),
  "__F300__": pick("Pretendard-Light.otf",     "82c21b19-PretendardLight.otf"),
}

htmlc = render_deck(TITLE, LSB)

# collect glyphs actually used
vis = re.sub(r'<style.*?</style>', '', htmlc, flags=re.S)
vis = re.sub(r'<script.*?</script>', '', vis, flags=re.S)
vis = re.sub(r'<[^>]+>', ' ', vis)
chars = set(vis)
chars |= set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,:;!?()[]{}<>/'\"%+-=~·•—–…→←↑↓≥≤±×°#&*@▲▼✕✳“”")
text = ''.join(sorted(chars))
print("glyphs:", len(chars))

uris = {}
for ph, path in FONTS.items():
    o = Options(); o.flavor = 'woff2'; o.desubroutinize = True
    o.name_IDs = []; o.name_legacy = False; o.name_languages = []
    f = TTFont(path); s = Subsetter(options=o); s.populate(text=text); s.subset(f)
    buf = io.BytesIO(); f.save(buf)
    uris[ph] = "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()
    print(ph, f"{len(buf.getvalue())/1024:.0f}KB  <- {os.path.basename(path)}")

for ph, uri in uris.items():
    htmlc = htmlc.replace(ph, uri)
out = os.path.join(BASE, FNAME + ".html")
open(out, 'w', encoding='utf-8').write(htmlc)
print("slides:", len(LSB), "->", out, f"({len(htmlc.encode())/1024:.0f}KB)")
