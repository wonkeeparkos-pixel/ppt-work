# -*- coding: utf-8 -*-
"""하지불안증후군(RLS) 웹 발표 덱 — NLC/LSB와 '동일 템플릿'(deck_html.py, Clinical Ledger).
세로 스크롤-스냅 · Pretendard 임베드(기존 생성 덱에서 재사용) · 자체 완결형 HTML(외부 리소스 0).
콘텐츠는 02_RLS 문헌고찰 근거 기반, 프리미엄 PPT와 동일 규격."""
import os, re, sys, json
sys.path.insert(0, os.path.dirname(__file__))
from deck_html import render_deck

# 울트라 업그레이드: 기전 SVG 도식(멀티에이전트 생성 + 검토)
_FIGD = json.load(open(os.path.join(os.path.dirname(__file__), "rls_figures.json"), encoding="utf-8"))
FIG  = {f['id']: f['svg']     for f in _FIGD}
FIGC = {f['id']: f['caption'] for f in _FIGD}

TITLE = "하지불안증후군(RLS) 근거 기반 치료"
SERIES = "고령 하지증상 문헌고찰 시리즈 · 2026"
OUT = "/home/user/ppt-work/하지불안증후군_치료_발표.html"
FONT_SRC = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB/RLS_발표_웹.html"

def PM(pmid): return f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
def PMC(x):   return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{x}/"

# ==================================================== RLS 슬라이드
RLS = [
 {'t':'title','eyebrow':'하지불안증후군 · Willis–Ekbom Disease',
  'title':'철분 교정을 기반으로 한<br>근거 기반 치료 정리',
  'sub':'Restless Legs Syndrome — Evidence-based Iron · Injection · Pharmacotherapy (AASM 2025)',
  'order':'진단·감별 → 병태생리 → 치료(철분 · 주사 · 경구약제 · ESWT) → 알고리즘',
  'series':SERIES},

 {'t':'bullets','eyebrow':'배경 · 임상 문제','tag':('배경',''),'title':'하지불안증후군(RLS)이란 무엇인가',
  'foot':'Allen 2014 (Sleep Med, IRLSSG); AASM 2025','items':[
   (0,'<b>정의:</b> 다리를 ‘움직이고 싶은 충동’을 핵심으로 하는 감각-운동 신경질환. 대개 불쾌한 다리 이상감각을 동반한다.',''),
   (0,'통증보다 ‘불편·안절부절·벌레가 기어가는 느낌’ 등 <b>이상감각</b>이 주. 만져지는 근경직은 없다.',''),
   (0,'유병률 성인 약 5~10%(여성·고령 증가). 수면개시·유지 장애로 삶의 질 저하.',''),
   (0,'수면 중 주기성 사지운동(PLMS)이 흔히 동반된다.',''),
   (-1,'관리의 성패는 정확한 진단(IRLSSG 5기준)과 철분 상태 평가에서 시작된다.','accent'),
  ],'stat':[('5–10%','성인 유병률'),('여성·고령','위험 증가군'),('5','IRLSSG 필수기준'),('저녁·밤','증상 악화')]},

 {'t':'table','eyebrow':'진단 · 감별','tag':('감별',''),'title':'RLS vs NLC 상세 감별표',
  'foot':'Allen 2014 (IRLSSG); AASM 2025; 문헌고찰 감별',
  'headers':['항목','하지불안증후군(RLS)','야간 하지경련(NLC)'],'rows':[
   ['핵심 증상','움직이고 싶은 충동 + 이상감각','통증성 근수축, 만져지는 근경직'],
   ['주 증상','불편·안절부절(통증 아님)','강한 통증'],
   ['완화','걷기·움직임(멈추면 재발)','스트레칭·족배굴곡'],
   ['근경직','<b>없음</b>','있음'],
   ['일주기·가족력','저녁~밤 악화 / 가족력 흔함','야간·수면초반 / 가족력 드묾'],
   ['1차 치료','<b>철분 교정 + α2δ 리간드</b>','비약물·원인교정 · 개별 약물'],
  ]},

 {'t':'bullets','eyebrow':'진단 · 기준','tag':('진단',''),'title':'진단 — IRLSSG 2014 필수 5기준',
  'foot':'Allen RP, et al. IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73.','items':[
   (0,'<b>① 움직이고 싶은 충동</b> — 대개 불쾌한 다리 감각을 동반한다.',''),
   (0,'<b>② 안정·비활동 시</b> 시작·악화된다.',''),
   (0,'<b>③ 움직이면 완화</b> — 걷기·스트레칭으로 부분적·일시적으로 완화(움직이는 동안 지속).',''),
   (0,'<b>④ 저녁·밤 악화</b> — 뚜렷한 일주기(circadian) 패턴.',''),
   (0,'<b>⑤ mimic 배제</b> — 다리경련·자세성 불편·근육통·정맥울혈 등으로 더 잘 설명되지 않음.',''),
   (-1,'5가지를 모두 충족해야 진단. 통증보다 이상감각이 주이며 촉지되는 근경직은 없다.','accent'),
  ]},

 {'t':'split','eyebrow':'진단 · workup','tag':('철분 평가',''),'title':'진단 확정 후 — 철분 평가와 악화요인',
  'foot':'Allen 2018 (IRLSSG iron task force); AASM 2025','items':[
   (0,'<b>혈청 철분:</b> ferritin · TSAT 측정 — 치료의 출발점.',''),
   (0,'이차 요인 선별: 철결핍·임신·말기신부전·갑상선.',''),
   (0,'악화 약물(항히스타민·항우울제·도파민 차단제) 조정.',''),
   (-1,'진단은 임상 5기준, 검사는 치료 방향 결정용.','accent'),
  ],'aside':{'title':'철분 판정 기준','stat':[('≤75','경구 철분 고려(ferritin)'),('≤100','정맥 철분(또는 경구 부적절)'),('TSAT','함께 평가')]}},

 {'t':'split','eyebrow':'병태생리 · 기전','tag':('핵심 기전',''),'title':'병태생리 ① 뇌 철분 결핍 — 핵심',
  'foot':'IRLSSG; Allen 2018 (Sleep Med); 문헌고찰 Part 1-1','items':[
   (0,'혈청 철분이 정상이어도 <b>뇌 국소 철분 부족</b> → 도파민 신호 이상.',''),
   (0,'‘철분 보충’ 치료의 생물학적 근거 — 전신 빈혈과는 다르다.',''),
   (0,'철결핍 동반 시 악화, 철분 교정으로 호전되는 경우가 많다.',''),
   (-1,'치료의 기반은 ferritin/TSAT 평가와 철분 교정.','accent'),
  ],'aside':{'title':'왜 철분인가','dark':True,'items':[
   (0,'철분은 도파민 합성효소(tyrosine hydroxylase)의 <b>보조인자</b>.',''),
   (0,'뇌 철분 부족 → 도파민 신호 이상 → 야간 감각-운동 증상.',''),
   (-1,'철분 교정이 이 상류(上流) 병태를 직접 겨냥한다.','accent'),
  ]}},

 {'t':'bullets','eyebrow':'병태생리 · 기전','tag':('기전',''),'title':'병태생리 ② 도파민 · 아데노신 가설',
  'foot':'IRLSSG; Garcia-Borreguero 2021 (아데노신); 문헌고찰 Part 1-2·1-3','items':[
   (0,'<b>흐름:</b> 뇌 국소 철분 결핍 → 도파민 신호 이상 / 아데노신 신호↓ → 글루타메이트·도파민 과흥분 → 야간 증상·PLMS.',''),
   (0,'<b>도파민 조절이상:</b> 주간 과잉·D2 하향조절 + 일주기 야간 저점. 도파민제 단기효과·장기 augmentation.','red'),
   (0,'<b>아데노신 저하 가설(최근):</b> 뇌 철분 결핍이 아데노신 신호를 낮춰 과흥분을 유발한다는 가설.',''),
   (-1,'아데노신 가설은 dipyridamole 등 도파민 비의존 표적 치료의 이론적 근거가 된다.','accent'),
  ]},

 {'t':'figure','eyebrow':'병태생리 · 도식','tag':('한눈에',''),'title':'RLS 기전 — 뇌 철분 결핍의 이중 경로',
  'foot':'문헌고찰 병태생리 종합 · IRLSSG · 아데노신 가설','svg':FIG['rls-pathophysiology-flow'],'caption':FIGC['rls-pathophysiology-flow']},

 {'t':'split','eyebrow':'병태생리 · 위험요인','tag':('위험요인',''),'title':'병태생리 ③ 유전 · 이차 요인 · 악화 약물',
  'foot':'IRLSSG; 문헌고찰 Part 1-4','items':[
   (0,'가족력 흔함(<b>상염색체 우성 경향</b>) — 조기 발병일수록 유전 기여 큼.',''),
   (0,'<b>이차 요인:</b> 철결핍·임신·말기신부전(투석)·갑상선 이상.',''),
   (0,'<b>악화 약물:</b> 항히스타민·항우울제·도파민 차단제.',''),
   (-1,'원인·악화약물 교정이 약물치료보다 앞선다.','accent'),
  ],'aside':{'title':'실무 포인트','dark':True,'items':[
   (0,'항우울제가 꼭 필요하면 RLS 악화가 적은 약제를 고려.',''),
   (0,'임신·신부전 동반 RLS는 안전한 치료(철분 등)를 우선.',''),
   (-1,'‘원인 교정’이 약물치료보다 앞선다.','accent'),
  ]}},

 {'t':'table','eyebrow':'총괄','tag':('요약',''),'title':'치료 근거 한눈에 — 무엇이 되고 무엇이 안 되나',
  'foot':'AASM 2025 지침 종합 · 02_RLS 문헌고찰 근거표',
  'headers':['치료','RLS 직접 근거','근거·권고','위치'],'rows':[
   ['철분 교정(경구/정맥)','Earley 2024 · IRLSSG 2018','<b>강한 권고</b>','기반·필수'],
   ['α2δ 리간드','Allen 2014 등 RCT','<b>강한 권고·1차</b>','1차 약물'],
   ['IV 철분(FCM)','Earley 2024 · 메타분석','<b>강한 권고</b>','철결핍 시'],
   ['dipyridamole','Garcia-Borreguero 2021','조건부','신규·아데노신'],
   ['비골신경 자극(TOMAC)','Charlesworth 2023 sham','조건부','비약물 대안'],
   ['도파민 작용제','Winkelman 2006 RCT','장기 권고 안 함','후순위'],
   ['보툴리눔독소','Mittal 2018 교차RCT','근거 약함','연구 단계'],
   ['체외충격파(ESWT)','없음','—','RLS 근거 없음'],
  ],'hlrows':[7]},

 {'t':'split','eyebrow':'치료 · 기반','tag':('효과 있음','green'),'title':'기반 치료: 철분 교정 — 경구와 정맥',
  'foot':'Allen 2018 (IRLSSG iron); Earley 2024; AASM 2025','items':[
   (0,'<b>경구 철분:</b> ferritin ≤75에서 고려(+비타민 C). ≥75엔 흡수 미미.',''),
   (0,'<b>정맥 철분(FCM):</b> ferritin ≤100 또는 경구 부적절/불내 시.','green'),
   (1,'FCM 1000 mg 단회(또는 750×2), 1시간 점적 · AASM 강한 권고.',''),
   (-1,'철분 교정은 ‘기반’ — 경구로 부족하면 정맥 전환.','accent'),
  ],'aside':{'title':'용량 · 적응','stat':[('1000 mg','FCM 단회(또는 750×2)'),('≤100','정맥 적응(ferritin)'),('1시간','점적 시간')]}},

 {'t':'split','eyebrow':'치료 · 주사','tag':('효과 있음','green'),'title':'주사 ① 정맥 철분(IV FCM) — 근거 최강',
  'foot':'Earley CJ, et al. Sleep. 2024;47(7):zsae095. PMID 38625730','items':[
   (0,'뇌 철분 결핍(핵심 병태)을 직접 교정 — 주사 중 근거 최강.',''),
   (0,'<b>Earley 2024(Sleep) RCT(n=209):</b> FCM 750mg → 42일 IRLS 유의 개선(p=0.004).','green'),
   (1,'단, CGI-I는 위약과 유의차 없어 공동 1차 평가변수는 미충족.','muted'),
   (0,'메타분석 2024(537명)은 효과·안전성 확인.',''),
   (-1,'철결핍·경구 부적절 시 AASM 2025 강한 권고.','accent'),
  ],'aside':{'title':'Earley 2024 (RCT 핵심)','dark':True,'stat':[('n=209','다기관 RCT'),('750 mg','FCM 0일·5일'),('42일','IRLS 개선(CGI 미달)'),('537명','메타분석')]}},

 {'t':'split','eyebrow':'치료 · 주사','tag':('연구 단계','amber'),'title':'주사 ② 보툴리눔 · ③ 정맥 경화요법',
  'foot':'Mittal 2018 (Toxins); Sundaresan 2019 (Cureus); Pyne 2023 (정맥류–RLS 연관성)','items':[
   (0,'<b>보툴리눔(Mittal 2018 교차, n=24):</b> incoA 100U → 전경골근·비복근·대퇴이두근, 4·6주 IRLS·VAS 개선.',''),
   (1,'SR/MA 2021: RCT 2편·27명, SMD −0.819. 표본 작아 확정 불가.','muted'),
   (0,'<b>정맥 경화요법(정맥류/CVI):</b> 하지정맥 치료 후 IRLS 19.83→7.89(Sundaresan 2019, 63%↓).','green'),
   (-1,'두 방법 모두 표현형·연구단계 — 특발성 RLS 표준치료 아님.','accent'),
  ],'aside':{'title':'정맥 경화 — 핵심 수치','stat':[('19.83→7.89','IRLS 점수'),('약 63%↓','호전'),('정맥류/CVI','적응 표현형')]}},

 {'t':'split','eyebrow':'치료 · 경구약제','tag':('약제',''),'title':'경구약제 개관 — 1차 패러다임 전환',
  'foot':'Winkelman 2025 (AASM, J Clin Sleep Med); 문헌고찰 Part 5','items':[
   (0,'2024/2025 AASM 지침의 핵심: 1차 약물을 <b>도파민제 → α2δ 리간드</b>로 전환.',''),
   (0,'이유: 도파민제의 장기 augmentation(연 7~10%) 위험이 α2δ 리간드보다 크다.','red'),
   (0,'철분 교정을 기반으로 하고, 그 위에 경구약제를 얹는다.',''),
   (-1,'고령·신기능 저하: 낙상·진정·부종을 고려해 저용량에서 서서히 적정.','accent'),
  ],'aside':{'title':'약물군 · 권고','items':[
   (0,'<b>α2δ 리간드</b> — 1차 · 강한 권고','green'),
   (0,'<b>철분(경구)</b> — 기반 · 필수','green'),
   (0,'<b>dipyridamole</b> — 조건부 · 신규',''),
   (0,'<b>오피오이드</b> — 난치성 · 조건부',''),
   (0,'<b>도파민 작용제</b> — 장기 권고 안 함','red'),
  ]}},

 {'t':'split','eyebrow':'치료 · 경구약제','tag':('1차','green'),'title':'경구약제 ① α2δ 리간드 — 1차',
  'foot':'Allen 2014 (NEJM); Winkelman 2011 (Mov Disord); AASM 2025','items':[
   (0,'gabapentin enacarbil · gabapentin · pregabalin. AASM 2025 1차 강한 권고.',''),
   (0,'<b>Allen 2014(NEJM) 52주:</b> pregabalin 효과적, augmentation 1.7% vs 9.0%.','green'),
   (0,'Gabapentin enacarbil: PSG 각성·PLM 감소(Winkelman 2011).',''),
   (0,'부작용: 어지럼·졸림·부종. 고령·신기능 저하 시 감량.',''),
  ],'aside':{'title':'왜 1차인가','dark':True,'items':[
   (0,'도파민제보다 augmentation이 유의하게 적다(1.7% vs 9.0%).','accent'),
   (0,'수면·감각증상을 함께 개선한다.',''),
   (0,'철분 교정과 병행이 기반이다.',''),
   (-1,'장기 관리에 유리한 프로파일.','accent'),
  ]}},

 {'t':'table','eyebrow':'치료 · 경구약제 · 기법','tag':('기법',''),'title':'α2δ 리간드 — 약물 · 특징 · 주의',
  'foot':'Allen 2014 (NEJM); Winkelman 2011; Bogan 2010 (Mayo Clin Proc)',
  'headers':['약물','특징 · 근거'],'rows':[
   ['Gabapentin enacarbil','전구약물로 흡수 안정적. PSG상 각성·PLM 감소(Winkelman 2011), 장기 유지(Bogan 2010)'],
   ['Pregabalin','<b>Allen 2014 NEJM 52주: 300 mg 효과적, augmentation 1.7%</b>'],
   ['Gabapentin','저비용·범용. 흡수 변동 있어 분할·적정 필요'],
   ['공통 부작용','어지럼 · 졸림 · 말초부종 · 체중증가'],
   ['고령·신기능','용량 감량 · 저용량에서 서서히 적정 · 낙상 주의'],
  ],'note':'소결: augmentation 위험이 낮고 수면·감각을 함께 개선 → 철분 교정 위의 1차 약물.'},

 {'t':'split','eyebrow':'치료 · 경구약제','tag':('후순위','red'),'title':'경구약제 ② 도파민 작용제 — augmentation',
  'foot':'Winkelman 2006 (Neurology); Allen 2014 (NEJM); AASM 2025','items':[
   (0,'pramipexole(미라펙스) · ropinirole · rotigotine — 단기 효능 확립.',''),
   (0,'Winkelman 2006: pramipexole 12주 IRLS·CGI 개선.',''),
   (0,'수개월~수년 후 <b>augmentation</b>(악화·전이, 연 7~10%)이 문제 → 장기 권고 안 함.','red'),
   (-1,'복용 중이면 철분 재평가 · α2δ로 단계적 전환.','accent'),
  ],'aside':{'title':'Augmentation','dark':True,'items':[
   (0,'증상이 더 이르게·더 넓은 부위로 악화.',''),
   (0,'용량을 올릴수록 악화되는 악순환.',''),
   (0,'연 7~10%에서 발생.',''),
   (-1,'장기 1차로 권고되지 않음.','accent'),
  ]}},

 {'t':'split','eyebrow':'RLS 치료 · 안전관리','tag':('단계적 관리','green'),'title':'도파민제 Augmentation — 단계적 관리',
  'foot':'AASM 2025; Allen 2014(NEJM, PMID 24521108); Garcia-Borreguero 2021','items':[
   (0,'<b>정의:</b> 도파민제 중 증상이 더 이르게·넓게·강하게 악화.',''),
   (0,'<b>단서:</b> 오후 조기 발현·부위 확산·증량 후 악화.',''),
   (0,'<b>위험:</b> 고용량 도파민제·저ferritin(&lt;50~75).','red'),
   (-1,'조기 인지 + 도파민제 의존 최소화가 핵심.','accent'),
  ],'aside':{'title':'단계적 대응 사다리','dark':True,'items':[
   (0,'① 도파민제 감량·분할·시점 조정',''),
   (0,'② 철분 재평가·보충(ferritin↑)',''),
   (0,'③ α2δ 리간드로 전환(1차)','green'),
   (0,'④ 난치: 오피오이드·dipyridamole','red'),
   (-1,'조기 인지 → 도파민제 이탈','accent'),
  ]}},

 {'t':'figure','eyebrow':'안전 · 도식','tag':('경과',''),'title':'Augmentation은 어떻게 진행되나',
  'foot':'Allen 2014(NEJM, PMID 24521108); 문헌고찰 augmentation','svg':FIG['dopamine-augmentation-timeline'],'caption':FIGC['dopamine-augmentation-timeline']},

 {'t':'split','eyebrow':'치료 · 경구약제','tag':('조건부','amber'),'title':'경구약제 ③ Dipyridamole · ④ 오피오이드',
  'foot':'Garcia-Borreguero 2021 (Mov Disord); AASM 2025','items':[
   (0,'<b>Dipyridamole(신규·아데노신):</b> Garcia-Borreguero 2021 교차 RCT.',''),
   (1,'IRLS 24.1→11.1(위약 18.7). augmentation 우려 적음(조건부).','green'),
   (0,'<b>오피오이드(난치성):</b> 서방형 oxycodone-naloxone(Trenkwalder 2013) — 조건부.',''),
   (1,'부프레노르핀은 상대적 저위험. 진정·호흡 위험 신중.','muted'),
   (-1,'두 약제 모두 1차 아님 — 특정 상황의 선택지.','accent'),
  ],'aside':{'title':'Dipyridamole 수치','stat':[('24.1→11.1','IRLS(약물군)'),('18.7','위약군 IRLS'),('교차 RCT','설계')]}},

 {'t':'table','eyebrow':'RLS 약물치료','tag':('요약',''),'title':'주요 약물 — 시작 · 적정 · 주의 요약',
  'foot':'AASM 2025; Allen 2014(NEJM, PMID 24521108); Earley 2024(Sleep, PMID 38625730)',
  'headers':['약물','위치','요지 · 주의'],'rows':[
   ['Gabapentin enacarbil','1차 α2δ','저녁 1회 · 어지럼/부종 · 신기능↓ 감량'],
   ['Pregabalin','1차 α2δ','300mg 저녁 · 신기능↓ 감량 · aug 1.7%'],
   ['Gabapentin','1차 α2δ','저녁 · 분할 · 신기능↓ 감량'],
   ['Pramipexole/Rotigotine','후순위 DA','augmentation 연 7~10% · 장기 지양'],
   ['경구 철분','기반 교정','ferritin ≤75 · +Vit C · 격일 투여'],
   ['FCM (IV)','기반 교정','ferritin ≤100 · 1000mg 단회/750×2'],
  ],'note':'사다리: 철분 기반 → α2δ 1차 → 도파민제 후순위(augmentation).'},

 {'t':'table','eyebrow':'RLS · 특수상황','tag':('개별화','amber'),'title':'동반질환·특수상황별 접근',
  'foot':'AASM 2025; IRLSSG 2014; Allen 2014(NEJM, PMID 24521108)',
  'headers':['범주','핵심 접근','주의'],'rows':[
   ['공통 기반','ferritin/TSAT → 철분 교정','모든 상황 선행(치료 기반)'],
   ['임신','경구 철분 우선','IV FCM은 1분기 회피·자료 제한'],
   ['말기신부전·투석','RLS 흔함 · 철분 교정','α2δ 신기능 따라 감량'],
   ['말초신경병증 동반','IRLSSG 5기준 감별 후 치료','이상감각 중복 주의'],
   ['우울증(SSRI/SNRI)','RLS 악화 가능 → 대안','부프로피온 등 · RLS 재평가'],
  ],'note':'철분 교정이 기반, α2δ 1차, 도파민제 후순위. IV FCM(중등도~중증)만 AASM 강한 권고이며 특수집단 전반에 동일 등급이 적용되진 않는다.'},

 {'t':'split','eyebrow':'RLS 관리 · 추적','tag':('정기 재평가','green'),'title':'장기 추적 — 악화·부작용 조기 포착',
  'foot':'AASM 2025; Allen 2014(NEJM, PMID 24521108, 52주 aug 1.7% vs 9.0%)','items':[
   (0,'<b>ferritin/TSAT 재평가</b> — 철분 교정의 기반 지표.','accent'),
   (0,'<b>Augmentation 정기 점검</b> — 도파민제 연 7~10%.','red'),
   (0,'<b>도파민제 복용자:</b> 충동조절장애(도박·쇼핑)·주간 졸음발작 문진.','red'),
   (0,'<b>α2δ 부작용</b> — 졸림·부종·체중↑, 신기능↓ 감량.','muted'),
   (-1,'생활·악화약물(카페인·SSRI·항히스타민) 재검토.','accent'),
  ],'aside':{'title':'모니터링 체크리스트','dark':True,'items':[
   (0,'ferritin/TSAT 재평가·반응',''),
   (0,'Augmentation 4징후(조기화·강도·부위·잠복기)','red'),
   (0,'도파민제: 충동조절장애·졸음발작','red'),
   (0,'α2δ: 부종·체중·졸림','muted'),
   (0,'생활·악화약물 재검토',''),
  ]}},

 {'t':'split','eyebrow':'치료 · ESWT','tag':('근거 없음','red'),'title':'체외충격파(ESWT) — RLS 직접 근거 없음',
  'foot':'문헌고찰 Part 3(직접 근거 부재); Charlesworth 2023(대안)','items':[
   (0,'RLS 결과변수로 ESWT를 평가한 연구는 없다(<b>직접 근거 없음</b>).','red'),
   (0,'ESWT 근거는 근골격계 통증·경직 영역 — RLS와 병태가 다르다.',''),
   (0,'이론상 거론되나 RLS 핵심 병태와 직접 연결하는 근거는 없다.',''),
   (-1,'근거를 창작하지 않는다 → RLS에 ESWT 권고 불가.','accent'),
  ],'aside':{'title':'근거 있는 대안','dark':True,'items':[
   (0,'비약물이 필요하면 충격파가 아니라 <b>말초 비골신경 자극</b>.','accent'),
   (0,'Charlesworth 2023: sham 대조에서 증상 개선·수면 무방해.',''),
   (-1,'AASM 2025 조건부 권고.','accent'),
  ]}},

 {'t':'bullets','eyebrow':'비약물 · 기기','tag':('조건부','green'),'title':'근거 있는 비약물 — 말초 비골신경 자극(TOMAC)',
  'foot':'Charlesworth JD, et al. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064','items':[
   (0,'<b>Charlesworth 2023(J Clin Sleep Med):</b> 양측 고빈도 비침습적 비골신경 자극(NPNS/TOMAC).',''),
   (0,'중등도~중증 RLS에서 sham(가짜자극) 대조로 평가.',''),
   (0,'다리 근육의 긴장성 활성을 유발하여, 수면을 방해하지 않고 증상을 개선.','green'),
   (0,'약물 부작용(augmentation·진정)이 없는 비약물 옵션.',''),
   (-1,'AASM 2025 조건부 권고 → 비약물이 필요할 때의 우선 고려 대상.','accent'),
  ]},

 {'t':'table','eyebrow':'근거 부재 · 감별','tag':('비권고','red'),'title':'RLS에 근거 없는 시술 — 정직한 평가',
  'foot':'StatPearls NBK560514·431107; Charlesworth 2023; 문헌고찰 — 근거 창작 안 함',
  'headers':['시술','RLS 직접 근거','실제 위치 · 감별'],'rows':[
   ['체외충격파(ESWT)','없음','근골격계 통증·경직용 — RLS와 병태 다름'],
   ['요추교감신경차단(LSB)','없음','교감신경 매개 통증·허혈(CRPS·PAD·CLI)용 — RLS 아님'],
   ['신경차단 주사(경골/비골)','없음','말초는 ‘자극(TOMAC)’이 근거 — 주사 아님'],
   ['심비골신경 차단(Imura)','—','NLC(야간경련) 근거이지 RLS 근거 아님'],
   ['근육내 보툴리눔','약함','소규모 RCT · 연구단계'],
  ],'hlrows':[0,1,2],
  'note':'공통 원칙: 근거를 창작하지 않는다. PAD·CLI·CRPS·정맥질환이 확인되면 그 원인 표적치료로서만 의미 — 그때는 RLS가 아니라 다른 진단이다.'},

 {'t':'table','eyebrow':'종합 · 근거표','tag':('요약',''),'title':'근거 요약표 — RLS 치료',
  'foot':'02_RLS 참고문헌 근거 요약표 · PubMed 대조',
  'headers':['영역','대표 문헌','설계','핵심 결과'],'rows':[
   ['IV 철분','Earley 2024','다기관 RCT n=209','42일 IRLS 개선(CGI 미달)'],
   ['IV 철분','메타분석 2024','SR/MA 537명','효과·안전 확인'],
   ['α2δ 리간드','Allen 2014','RCT n=719','<b>augmentation 1.7% vs 9.0%</b>'],
   ['도파민제(미라펙스)','Winkelman 2006','RCT n=344','단기 개선(장기 aug)'],
   ['dipyridamole','Garcia-Borreguero 2021','교차 RCT','IRLS 24.1→11.1'],
   ['보툴리눔','Mittal 2018','교차 RCT n=24','4·6주 IRLS·VAS 개선'],
   ['비골신경 자극','Charlesworth 2023','sham 대조','증상 개선·수면 무방해'],
   ['ESWT','—','RLS 표적 연구 없음','직접 근거 없음'],
  ],'hlrows':[7]},

 {'t':'figure','eyebrow':'종합 · 도식','tag':('사다리',''),'title':'단계적 치료 접근 — 한눈에',
  'foot':'AASM 2025 지침 · 문헌고찰 치료 사다리','svg':FIG['rls-treatment-ladder'],'caption':FIGC['rls-treatment-ladder']},

 {'t':'key','eyebrow':'핵심 메시지 · RLS','headline':'철분 교정이 기반, α2δ 리간드가 1차 — 도파민제는 후순위','msgs':[
   ('병태생리','뇌 국소 철분 결핍 → 도파민·아데노신 신호 이상. 유전·이차요인이 악화.'),
   ('진단·감별','IRLSSG 5기준(움직임 충동·안정 시 악화·움직이면 완화·저녁 악화·mimic 배제). NLC와 감별.'),
   ('기반·1차','철분 교정(경구≤75/정맥≤100)이 기반, α2δ 리간드가 1차 강한 권고.'),
   ('주사·비약물','IV 철분(FCM)이 근거 최강. 보툴리눔·정맥경화는 표현형·연구단계. 비약물은 비골신경 자극.'),
   ('주의','도파민제는 augmentation로 장기 후순위. ESWT는 RLS 근거 없음 — 근거를 창작하지 않는다.'),
 ]},

 {'t':'refs','title':'참고문헌 — RLS','refs':[
   ('<b>Allen.</b> RLS/WED diagnostic criteria: updated IRLSSG consensus. Sleep Med. 2014.',PM(25023924)),
   ('<b>Winkelman.</b> RLS/PLMD treatment: AASM guideline. J Clin Sleep Med. 2025.',PM(39324694)),
   ('<b>Allen.</b> IRLSSG task force: iron treatment of RLS. Sleep Med. 2018.',PM(29425576)),
   ('<b>Earley.</b> IV ferric carboxymaltose for RLS: multicenter RCT. Sleep. 2024.',PM(38625730)),
   ('IV ferric carboxymaltose in RLS: meta-analysis of 537 patients. Sleep Med. 2024.',PM(39326219)),
   ('<b>Mittal.</b> Botulinum toxin in RLS: crossover RCT. Toxins. 2018.',PMC('PMC6215171')),
   ('Botulinum toxin A in RLS: SR & meta-analysis. Healthcare. 2021.',PMC('PMC8623507')),
   ('<b>Pyne.</b> Varicose veins with RLS & nocturnal leg cramps. J Vasc Interv Radiol. 2023.',PM(36526075)),
   ('<b>Sundaresan.</b> Treatment of leg veins for RLS: retrospective. Cureus. 2019.',PM(31192073)),
   ('<b>Charlesworth.</b> Peroneal nerve stimulation for RLS. J Clin Sleep Med. 2023.',PM(36856064)),
   ('<b>Allen.</b> Pregabalin vs pramipexole for RLS. N Engl J Med. 2014.',PM(24521108)),
   ('<b>Winkelman.</b> Pramipexole in RLS. Neurology. 2006.',PM(16931507)),
   ('<b>Winkelman.</b> Gabapentin enacarbil PSG study in RLS. Mov Disord. 2011.',PM(21611981)),
   ('<b>Bogan.</b> Long-term gabapentin enacarbil in RLS: RCT. Mayo Clin Proc. 2010.',PM(20511481)),
   ('<b>Garcia-Borreguero.</b> Dipyridamole for RLS: crossover RCT. Mov Disord. 2021.',PM(34137476)),
   ('<b>Buchfuhrer.</b> Noninvasive peroneal nerve stimulation (TOMAC) for RLS: sham-controlled RCT. J Clin Sleep Med. 2021;17(8):1685-94.',''),
   ('<b>Trenkwalder.</b> Prolonged-release oxycodone-naloxone for refractory RLS: RCT. Lancet Neurol. 2013;12(12):1141-50.',''),
 ]},
]

# ==================================================== render + font embed
html = render_deck(TITLE, RLS)

# 기존 생성 덱에서 Pretendard woff2 4종(data URI)을 추출해 __F___ 자리표시자 치환
src = open(FONT_SRC, encoding="utf-8").read()
faces = dict(re.findall(
    r'@font-face\{font-family:Pretendard;font-weight:(\d+);src:url\((data:font/woff2;base64,[^)]+)\)', src))
missing = [w for w in ("900","800","700","300") if w not in faces]
if missing:
    raise SystemExit(f"폰트 가중치 누락: {missing} (FONT_SRC 확인)")
for w in ("900","800","700","300"):
    html = html.replace(f"__F{w}__", faces[w])

# RLS 콘텐츠가 원본(NLC/LSB)보다 촘촘해 세로 오버플로 방지용 미세 압축(템플릿 룩은 유지)
OVERRIDE = ("/* RLS density fit */"
            ".snap .pad{padding-bottom:4.2cqw}"
            "ul.b{gap:1.18cqw}"
            "ul.b li{font-size:2.34cqw;line-height:1.23}"
            "ul.b li.sub2{font-size:2.16cqw}"
            ".aside{padding:2.3cqw 2.6cqw}"
            ".aside ul.b li{font-size:2.06cqw;line-height:1.2}"
            ".foot{padding-top:1.5cqw}"
            ".content .foot,.split .foot,.tableS .foot{margin-top:1.1cqw}"
            # 8행 표가 16:9 스테이지에 들어가도록 컴팩트화
            "table.t{margin-top:0.5cqw}"
            "table.t th{padding:0.9cqw 1.3cqw;font-size:1.9cqw}"
            "table.t td{padding:0.82cqw 1.3cqw;font-size:1.8cqw;line-height:1.16}"
            # key 슬라이드 5개 메시지 세로 맞춤
            ".key h2.kh{margin:1.2cqw 0 1.7cqw;font-size:4.4cqw}"
            ".key .msg{padding:1.02cqw 0}"
            ".key .msg .ml{font-size:2.4cqw}"
            ".key .msg .md{font-size:2.12cqw}")
html = html.replace("</style>", OVERRIDE + "</style>", 1)

assert "__F" not in html, "폰트 자리표시자가 남아 있음"
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, "|", len(RLS), "slides |", round(len(html)/1024), "KB")
