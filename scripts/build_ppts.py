# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from ppt_lib import Deck, TEAL, TEALD, NAVY2, GREEN, AMBER, RED, INK, MUTE, MINT, WHITE
from pptx.util import Inches

BASE = "/home/user/ppt-work/문헌고찰_NLC_RLS_LSB"

# ============================================================ DECK 1 — NLC
d = Deck()
d.title_slide("야간 하지경련 (Nocturnal Leg Cramps)",
    ["병태생리 · 주된 호소 ·", "근거 기반 치료"],
    "Pathophysiology, Presentation, and Evidence-based Treatment (ESWT · Injection · Oral drugs)",
    "구성: 병태생리 → 주된 호소 → 치료(ESWT · 주사기법 · 경구약제) → 결론",
    "교육·연구 참고용. 개별 환자의 진료 결정은 담당 의사의 판단에 따른다.  |  작성 2026-07")

d.bullets_slide("병태생리 ① — 운동신경 과흥분", "병태생리", "기전", [
    (0,"NLC는 운동신경의 폭발적 과흥분에 의한 불수의적·유통성 근수축이다.",INK,True),
    (0,"진성 근경련은 원위 운동축삭 종말의 자발적·고빈도(최대 ~150 Hz) 방전에서 기원(Miller & Layzer 2005).",INK),
    (0,"Minetto 2011: 후경골신경 차단 하에서도 경련은 유발되나 더 높은 자극빈도가 필요·지속이 짧음.",INK),
    (1,"→ 경련 유지에는 척수 회로(운동뉴런 과흥분의 양성 되먹임)가 필수. 중추+말초 복합 기전.",TEALD,True),
    (0,"이차(유발) 요인: 요추관협착·신경근병증(Matsumoto·Ohtori·Handa), 정맥부전, 신경병증, 전해질, 약물(LABA·이뇨제·statin).",INK),
], "Miller & Layzer 2005; Minetto 2011; Garrison 2012")

d.split_slide("병태생리 ② — 반사 불균형과 근단축", "병태생리", "기전", [
    (0,"근방추(Ia) 흥분성 되먹임 증가 + 골지건기관(Ib) 억제성 되먹임 감소의 불균형이 경련을 촉발·유지.",INK,True),
    (0,"경련은 근육이 '단축'된 위치(수면 중 발 저측굴곡)에서 거의 배타적으로 발생, 신전으로 완화.",INK),
    (0,"단축 시 GTO 억제가 약해지고 운동종판 흥분 역치가 낮아진다(Minetto 2013).",INK),
    (0,"Khan & Burne 2007: 아킬레스건 전기자극이 진행 중 경련을 반사적으로 억제.",INK),
], ("왜 스트레칭이 듣는가", [
    (0,"신전·건 자극이 Ib 구심성을 통해 경련 회로를 직접 억제.",None),
    (0,"→ 스트레칭·족배굴곡이 급성 완화와 예방의 생리적 근거.",MINT,True),
], None), "Minetto 2013; Khan & Burne 2007", dark_card=True)

d.bullets_slide("환자들의 주된 호소", "임상 양상", "호소", [
    (0,"수면 중 갑작스러운 종아리·발의 강한 통증성 경련으로 각성.",INK,True),
    (0,"해당 근육이 단단하게 뭉침(촉지되는 근경직), 발끝을 몸쪽으로 당기면(족배굴곡) 완화.",INK),
    (0,"지속 수초~최대 10분, 이후 잔통(subsequent pain)이 남음.",INK),
    (0,"수면 분절·각성 → 불면·주간 피로·삶의 질 저하.",INK),
    (0,"위치는 후종아리(비복근)·발이 대부분(허벅지·햄스트링은 드묾).",INK),
    (0,"유병률: 50세+ 경증 24~25%·중등도이상 ~6%, 요추관협착 동반 시 최대 65%.",INK),
    (-1,"감별: RLS(움직임 충동·움직이면 완화·근경직 없음)와 반드시 구분.",TEALD,True),
], "Hallegraeff 2017; Grandner & Winkelman 2017")

d.table_slide("치료 개관 — 3축 근거", "총괄", "요약", [
    ("치료","대표","야간경련 근거","위치"),
    ("ESWT","종아리 표적 충격파","Li 2021(후향)+경직 RCT/MA","보조·근거형성 중"),
    ("주사","보툴리눔(비복근)","Park 2017·Restivo 2018 RCT","불응성 선택(Level II)"),
    ("주사","국소마취제 유발점/dry needling","Kim 2015·Temel 2023","MTrP 동반 시"),
    ("주사","심비골신경 내측분지 차단","Imura 2015(직접근거)","선택적"),
    ("경구약제","quinine / 비타민 B·diltiazem","El-Tawil / Chan·Voon","효과O·독성 / Level C"),
    ("비약물","취침 전 스트레칭","Hallegraeff 2012 RCT","1차·최우선"),
], [Inches(2.0),Inches(3.5),Inches(3.9),Inches(2.45)], "문헌고찰 종합", size=11.5, row_h=Inches(0.6))

d.split_slide("치료 ① 체외충격파(ESWT) — 근거", "치료 · ESWT", "근거형성중", [
    (0,"Li 2021(후향 n=126): 요추퇴행성 동반 하지경련. 2,000 shocks/session, 8–10/sec, 2일 간격 4주.",INK,True),
    (1,"경련 빈도 5.7→1.3회/시간, 지속 57.6→10.6초, VAS 7.6→1.7 (P<0.001).",GREEN,True),
    (0,"인접 근거(종아리 경직): Otero-Luis 2024 SR/MA 하지 MAS −0.40; Mihai 2020 SMD 0.53.",INK),
    (0,"특발성 NLC만을 표적한 ESWT RCT는 아직 없음(직접 근거 공백).",RED),
], ("Li 2021 결과(ESWT군)", [
    (0,"빈도 5.7 → 1.3 회/시간",None),
    (0,"지속 57.6 → 10.6 초",None),
    (0,"통증 VAS 7.6 → 1.7",None),
    (0,"모두 대조군 대비 P<0.001",MINT,True),
], None), "Li 2021(Biomed Res Int); Otero-Luis 2024", tag_color=AMBER, dark_card=True)

d.bullets_slide("ESWT — 기전 · 프로토콜 · 한계", "치료 · ESWT", "기전", [
    (0,"기전(Yang 2021): NO 합성↑, 신경근접합부 ACh수용체 변성(CMAP↓ 6–8주), 운동신경원 흥분성↓, 유변학적 변화, 미세순환 개선.",INK),
    (0,"프로토콜: 비복근 내·외측두·가자미근 운동점, radial 1.5–2.5 bar 또는 focused ~0.10 mJ/mm², 2,000–3,000 pulses/근육, 주 1–2회 3–4주(세션수 의존).",INK),
    (0,"안전: 대체로 안전(일시적 국소통증). 상대 금기 — 항응고제·심부정맥혈전·감염·악성종양 부위·임신.",INK),
    (-1,"한계: 특발성 NLC 직접 RCT 부재, 효과 대개 12주 이내 단기 → 생물학적 타당성은 높으나 보조·실험적.",TEALD,True),
], "Yang 2021(J Clin Med, 기전 리뷰)")

d.split_slide("치료 ② 주사기법 (1) 국소마취제 유발점주사", "치료 · 주사기법", "효과 있음", [
    (0,"개념: 비복근 근막통증유발점(MTrP)에 소량 국소마취제 → 국소 근이완·유발점 비활성화·구심성 되먹임 차단.",INK,True),
    (0,"결과(Kim 2015, n=12): NRS·경련 빈도·불면지수(ISI) 모두 유의 개선(P<0.01), 임상적 불면 10명→4주째 1명.",GREEN),
    (0,"Prateepavanich 1999(무작위 n=24): xylocaine 주사 vs quinine — 지속효과 면에서 주사군 우월.",INK),
], ("기법(Kim 2015)", [
    (0,"약제: 0.25% lidocaine 1–2 mL",None),
    (0,"바늘: 25 G, 피부 30° 접근",None),
    (0,"표적: 비복근 유발점(최대 압통점)",None),
    (0,"빈도: 주 1회",None),
], None), "Kim 2015(J Am Board Fam Med); Prateepavanich 1999", tag_color=GREEN)

d.bullets_slide("치료 ② 주사기법 (2) 건침(Dry Needling)", "치료 · 주사기법", "효과 있음", [
    (0,"기법: 비복근 유발점에 약물 없이 자침, 국소연축반응 유도·소실 → taut band 이완, 압력통증역치 상승. 주 1회 약 3회기.",INK,True),
    (0,"Temel 2023 RCT(n=42): 스트레칭 단독 vs 스트레칭+DN → DN 병용군이 3개월 경련 횟수(P=0.016)·강도·압력통증역치·수면질(PSQI) 우월.",GREEN),
    (0,"Bagcier 2021 증례: 주1회 3회기 후 경련 지속 60초→10초, VAS 8→1, 빈도 '매일'→'주간'.",INK),
    (-1,"저침습·저비용·무약물. 근거는 소규모 RCT·증례(Level III~). 초음파 유도 권장.",TEALD,True),
], "Temel 2023(Turk J Osteoporos); Bagcier 2021", tag_color=GREEN, gap=11)

d.split_slide("치료 ② 주사기법 (3) 심비골신경 내측분지 차단", "치료 · 주사기법 · 직접근거", "직접 근거", [
    (0,"Imura 2015: 야간경련에 말초 운동신경가지를 직접 표적한, 현재 유일한 전향적 비교연구.",INK,True),
    (0,"대상: 요추수술 후 지속 경련 66명(차단군 41 vs 대조 25), 평균 60.9세.",INK),
    (0,"기법: 제1–2 중족골 사이 간극의 원위 2/3 지점, 1.0% lidocaine 5.0 mL(무에피네프린)를 1.0–1.5 cm 깊이에 서서히 주입.",INK,True),
    (0,"부작용 41명 전원 없음. 저위험·간편.",INK),
], ("결과(2주)", [
    (0,"빈도 1/4↓: 61.0% vs 20.0%",MINT,True),
    (0,"1/2↓: 80.5% (P<0.01)",None),
    (0,"강도↓: 63.4% vs 8.0%",None),
    (0,"12주 이상 지속 63.4%",None),
], None), "Imura 2015(Brain Behav; PMID 26445706)", dark_card=True)

d.bullets_slide("치료 ② 주사기법 (4) 보툴리눔 + 안전성", "치료 · 주사기법", "효과 있음", [
    (0,"Park 2017 RCT(n=50): 요추관협착 동반 야간 종아리경련. 비복근 BTX-A vs gabapentin → 전 시점 다리통증·빈도·강도 유의 감소(P<0.01), 불면·기능 개선.",GREEN,True),
    (0,"Restivo 2018 RCT: 당뇨병성 신경병증 경련에서 위약 대비 개선(1주부터 16주 지속).",INK),
    (0,"주사 계열 중 근거 최고(Level II)이나 고가·반복·근력약화 우려 → 선택적.",INK),
    (-1,"안전(고령): 경골신경→족저굴곡 약화, 총비골신경→족하수→낙상. 항응고제 시 출혈. 초음파 유도·혈관내 주입 회피.",RED,True),
], "Park 2017·Restivo 2018 (Arch Phys Med Rehabil / Ann Neurol)", tag_color=GREEN)

d.table_slide("치료 ③ 효과 좋은 경구 약제", "치료 · 경구약제", "약제", [
    ("약제","근거","평가"),
    ("Quinine","El-Tawil 2015 Cochrane(23시험)","효과 O이나 FDA 미승인·혈소판감소/TTP → 최후·선별"),
    ("비타민 B 복합","Chan 1998 RCT(고령 28명)","빈도·강도·지속 감소, Level C·안전 → 우선 시도"),
    ("Diltiazem 30mg","Voon 2001 교차(n=13)","빈도 5.8→0.16/2주, Level C"),
    ("Vitamin K2","Tan 2024(JAMA IM)","빈도 2.60→0.96 (⚠정정·교체 통지, 과대해석 금지)"),
    ("Gabapentin·Baclofen","Kim 2024 등","LSS 동반 시 제한적"),
    ("마그네슘(특발성)","Garrison 2020 Cochrane","임상적 이득 없음 — 권고 안 함"),
], [Inches(2.2),Inches(4.0),Inches(5.65)], "AAN(Katzberg 2010); Cochrane 종합", size=11, row_h=Inches(0.58))

d.bullets_slide("1차 비약물 치료 (참고)", "비약물", "1차", [
    (0,"취침 전 스트레칭(Hallegraeff 2012 RCT): 종아리·햄스트링 6주 → 경련 빈도(−1.2회/야간)·강도(−1.3 cm VAS) 감소.",GREEN,True),
    (0,"위험 거의 없고 무비용 → 모든 고령 NLC 환자의 1차.",INK),
    (0,"급성 발작: 족배굴곡 수동 신장·걷기·마사지.",INK),
    (0,"자세·환경: 이불을 발 위로 팽팽히 덮지 않기, 발끝 중립, 수분·온열.",INK),
    (0,"원인 교정: 유발약물(LABA·이뇨제·statin) 검토, 이차 원인(협착·정맥부전·전해질) 교정.",INK),
], "Hallegraeff 2012(J Physiother); Allen & Kirby 2012", tag_color=GREEN)

d.key_slide("핵심 메시지 — NLC", "감별과 원인교정이 먼저, 스트레칭이 1차", [
    ("병태생리","운동신경 과흥분 + Ia/Ib 반사 불균형. 단축된 근육에서 유발, 신전으로 완화."),
    ("주된 호소","수면 중 통증성 경련·촉지 근경직·족배굴곡 완화·잔통·수면장애. RLS와 감별."),
    ("ESWT","경직 근거는 강하나 경련 직접근거는 약함 → 보조·근거형성 중."),
    ("주사","BTX(RCT)·유발점/dry needling(MTrP)·심비골신경 차단(Imura)이 불응성에 선택적."),
    ("경구약제","quinine 효과O·독성으로 회피, 비타민B/diltiazem 비교적 안전, 마그네슘 특발성 무효."),
])

d.refs_slide("참고문헌 — NLC", [
 "Miller TM, Layzer RB. Muscle cramps. Muscle Nerve. 2005;32(4):431-442. PMID 15902691.",
 "Minetto MA, et al. Mechanisms of cramp contractions: peripheral or central generation? J Physiol. 2011;589:5759-73. PMID 21969448.",
 "Khan SI, Burne JA. Reflex inhibition of cramp by tendon stimulation. J Neurophysiol. 2007;98(3):1102-7. PMID 17634341.",
 "Hallegraeff JM, et al. Stretching before sleep reduces nocturnal leg cramps in older adults: RCT. J Physiother. 2012;58(1):17-22. PMID 22341378.",
 "Li BZ, et al. ESWT reduces leg cramps in lumbar degenerative disorders: retrospective. Biomed Res Int. 2021;2021:3554397. PMID 34734084.",
 "Otero-Luis I, et al. ESWT for spasticity: SR & meta-analysis. J Clin Med. 2024;13(5):1323. PMID 38592705.",
 "Kim DH, et al. Myofascial trigger point injections on nocturnal calf cramps. J Am Board Fam Med. 2015;28(1):21-7. PMID 25567819.",
 "Temel MH, et al. Dry needling on nocturnal calf cramps: RCT. Turk J Osteoporos. 2023;29(3):170-6.",
 "Imura T, et al. Nocturnal leg cramps treated by deep peroneal nerve medial branch block. Brain Behav. 2015;5(9):e00370. PMID 26445706.",
 "Park SJ, et al. Botulinum toxin for nocturnal calf cramps in LSS: RCT. Arch Phys Med Rehabil. 2017;98(5):957-63. PMID 28209505.",
 "El-Tawil S, et al. Quinine for muscle cramps. Cochrane Database Syst Rev. 2015;(4):CD005044. PMID 25842375.",
 "Garrison SR, et al. Magnesium for skeletal muscle cramps. Cochrane Database Syst Rev. 2020;9:CD009402. PMID 32956536.",
 "Chan P, et al. Vitamin B complex for nocturnal leg cramps: RCT. J Clin Pharmacol. 1998;38(12):1151-4. PMID 11301568.",
 "Voon WC, Sheu SH. Diltiazem for nocturnal leg cramps. Age Ageing. 2001;30(1):91-2. PMID 11322688.",
])
n1 = d.save(os.path.join(BASE,"01_NLC","NLC_발표.pptx"))

# ============================================================ DECK 2 — RLS
d = Deck()
d.title_slide("하지불안증후군 (Restless Legs Syndrome)",
    ["병태생리 · 주된 호소 ·", "근거 기반 치료"],
    "Pathophysiology, Presentation, and Evidence-based Treatment (ESWT · Injection · Oral drugs)",
    "구성: 병태생리 → 주된 호소 → 치료(ESWT · 주사 · 경구약제) → 결론",
    "교육·연구 참고용. 개별 환자의 진단·처방 결정은 담당 의사의 판단에 따른다.  |  작성 2026-07")

d.bullets_slide("병태생리", "병태생리", "기전", [
    (0,"뇌 철분 결핍(핵심): 혈청 철분이 정상이어도 흑질·기저핵 등 뇌 국소 철분이 부족 → 도파민 신호 이상.",INK,True),
    (0,"도파민 이상: 야간 도파민 기능 저하 가설. 도파민제 단기 효과, 장기 사용 시 augmentation 유발.",INK),
    (0,"아데노신 저하 가설(최근): 뇌 철분 결핍이 아데노신 신호를 낮춰 과흥분 유발 → dipyridamole의 근거.",INK),
    (0,"유전(가족력 흔함)·이차 요인(철결핍·임신·말기신부전·특정 약물).",INK),
    (-1,"→ 치료의 기반은 철분 교정, 약물 축은 도파민에서 α2δ 리간드로 이동.",TEALD,True),
], "IRLSSG; AASM 2025 지침 방향")

d.bullets_slide("환자들의 주된 호소 — IRLSSG 2014 필수 5기준", "임상 양상", "진단", [
    (0,"① 다리를 움직이고 싶은 충동(대개 불쾌한 다리 감각 동반).",INK,True),
    (0,"② 안정·비활동 시 시작·악화.",INK),
    (0,"③ 움직임(걷기·스트레칭)으로 부분적·일시적 완화.",INK),
    (0,"④ 저녁·밤에 악화되는 뚜렷한 일주기(circadian).",INK),
    (0,"⑤ 다른 질환(다리경련 등)으로 더 잘 설명되지 않음(mimic 배제).",INK),
    (0,"통증보다 이상감각이 주, 촉지되는 근경직 없음. PLMS 동반. 유병률 5~10%.",INK),
    (-1,"감별: NLC(통증성 근수축·근경직·족배굴곡 완화)와 구분.",TEALD,True),
], "Allen 2014(Sleep Med, IRLSSG)")

d.table_slide("치료 개관 — 3축 근거", "총괄", "요약", [
    ("치료","대표","RLS 근거","위치"),
    ("ESWT","체외충격파","RLS 표적 연구 없음","권고 불가(비골신경자극 대안)"),
    ("주사","IV 철분(FCM)","Earley 2024 RCT·메타분석","철결핍 시 강한 권고"),
    ("주사","보툴리눔 / 정맥경화","Mittal 2018 / Pyne 2023","연구단계 / 정맥질환 동반"),
    ("경구약제","α2δ 리간드","Allen 2014 등 RCT","1차(강한 권고)"),
    ("경구약제","도파민 작용제","Winkelman 2006","단기효과·augmentation로 후순위"),
    ("경구약제","dipyridamole","Garcia-Borreguero 2021","조건부(신규)"),
], [Inches(2.0),Inches(3.2),Inches(3.7),Inches(2.95)], "AASM 2025 지침 종합", size=11.5, row_h=Inches(0.6))

d.split_slide("치료 ① 체외충격파(ESWT)", "치료 · ESWT", "근거 없음", [
    (0,"RLS를 결과변수로 ESWT를 평가한 RCT·전향연구·증례는 검색되지 않음(직접 근거 없음).",RED,True),
    (0,"ESWT의 확립된 근거는 근골격계 통증·경직 영역으로 RLS(뇌 철분·도파민·아데노신)와 병태가 다르다.",INK),
    (0,"근거를 창작하지 않는다 → RLS에 ESWT는 권고할 수 없다.",INK,True),
], ("근거 있는 대안", [
    (0,"말초 비골신경 자극(TOMAC)",MINT,True),
    (0,"Charlesworth 2023: sham 대조에서 증상 개선·수면 무방해.",None),
    (0,"AASM 2025 조건부 권고.",None),
    (0,"→ 비약물이 필요하면 충격파가 아니라 비골신경 자극.",MINT,True),
], None), "Charlesworth 2023(J Clin Sleep Med); AASM 2025", tag_color=RED, dark_card=True)

d.split_slide("치료 ② 주사 (1) 정맥 철분 — 근거 최강", "치료 · 주사", "효과 있음", [
    (0,"뇌 철분 결핍을 직접 교정하는, RLS 주사 치료 중 근거 최강.",INK,True),
    (0,"Earley 2024(Sleep) 다기관 RCT(n=209): FCM 750 mg(0·5일) vs 위약 → 42일 IRLS·CGI 유의 개선.",GREEN),
    (0,"메타분석 2024(537명)도 효과·안전성 확인. AASM 2025 강한 권고.",INK),
    (0,"안전: 일과성 저인산혈증 모니터링.",INK),
], ("용량·적응", [
    (0,"FCM 1000 mg 단회(또는 750 mg×2)",None),
    (0,"1시간 이내 점적",None),
    (0,"적응: ferritin ≤100 또는 경구 부적절",None),
    (0,"경구는 ferritin ≥75에서 흡수 미미",None),
], None), "Earley 2024(Sleep); IRLSSG iron 2018", tag_color=GREEN)

d.bullets_slide("치료 ② 주사 (2) 보툴리눔 · 정맥 경화요법", "치료 · 주사", "제한적", [
    (0,"보툴리눔(Mittal 2018 이중맹검 교차 n=24): incoA 100U를 전경골근·비복근·대퇴이두근에 주사 → 4·6주 IRLS·통증(VAS) 유의 개선.",INK,True),
    (1,"SR/MA(Healthcare 2021): RCT 2편 27명 IRLS SMD −0.819. 표본 매우 작아 확정 불가 → 표준치료 아님.",MUTE),
    (0,"정맥 경화요법(정맥류/CVI 동반): Pyne 2023·Sundaresan 2019 → 하지정맥 치료 후 IRLS 19.83→7.89(약 63%↓).",INK),
    (-1,"두 방법 모두 특정 표현형·연구단계. 특발성 RLS 전반의 표준치료는 아님.",TEALD,True),
], "Mittal 2018(Toxins); Pyne 2023(JVIR); Sundaresan 2019", tag_color=AMBER)

d.split_slide("치료 ③ 경구약제 (1) α2δ 리간드 — 1차", "치료 · 경구약제", "1차", [
    (0,"gabapentin enacarbil·gabapentin·pregabalin. AASM 2025 1차 강한 권고.",INK,True),
    (0,"Allen 2014(NEJM) 52주 RCT: pregabalin 300 mg 효과적, augmentation 1.7% vs pramipexole 9.0%.",GREEN),
    (0,"Gabapentin enacarbil: Winkelman 2011(PSG) 각성·PLM 감소, Bogan 2010 장기 유지.",INK),
    (0,"부작용: 어지럼·졸림·부종·체중증가. 고령·신기능 저하 시 감량.",INK),
], ("왜 1차인가", [
    (0,"도파민제보다 augmentation이 유의하게 적음.",MINT,True),
    (0,"수면·감각증상 함께 개선.",None),
    (0,"철분 교정과 병행이 기반.",None),
], None), "Allen 2014(NEJM); AASM 2025", tag_color=GREEN, dark_card=True)

d.table_slide("치료 ③ 경구약제 (2) 도파민제·신규·요약", "치료 · 경구약제", "약제", [
    ("약물군","위치 · 근거"),
    ("도파민 작용제(pramipexole·ropinirole·rotigotine)","단기 효능O(Winkelman 2006) — augmentation(연 7~10%)로 장기 권고 안 함(AASM 2025 against)"),
    ("Dipyridamole","Garcia-Borreguero 2021 교차 RCT: IRLS 24.1→11.1(위약 18.7). 아데노신 가설, 조건부"),
    ("오피오이드(서방형 oxycodone·부프레노르핀)","난치성·augmentation에 조건부. 진정·호흡 위험 신중"),
    ("철분(경구)","ferritin ≤75에서 기반 치료. 흡수 부족 시 정맥 전환"),
], [Inches(4.6),Inches(7.25)], "AASM 2025(J Clin Sleep Med)", size=11.5, row_h=Inches(0.72))

d.key_slide("핵심 메시지 — RLS", "철분 교정이 기반, α2δ 리간드가 1차", [
    ("병태생리","뇌 국소 철분 결핍 → 도파민·아데노신 신호 이상."),
    ("주된 호소","움직임 충동·안정 시 악화·움직이면 완화·저녁 악화(IRLSSG 5기준). NLC와 감별."),
    ("주사","IV 철분(FCM)이 근거 최강. 보툴리눔은 연구단계, 정맥경화는 정맥질환 동반 시."),
    ("ESWT","RLS 직접근거 없음 → 비약물은 비골신경 자극(근거 있음)."),
    ("경구약제","α2δ 리간드 1차. 도파민제는 augmentation로 후순위. dipyridamole 조건부."),
])

d.refs_slide("참고문헌 — RLS", [
 "Allen RP, et al. RLS/WED diagnostic criteria: updated IRLSSG consensus criteria. Sleep Med. 2014;15(8):860-73. PMID 25023924.",
 "Winkelman JW, et al. Treatment of RLS/PLMD: AASM clinical practice guideline. J Clin Sleep Med. 2025;21(1):137-52. PMID 39324694.",
 "Allen RP, et al. IRLSSG task force: iron treatment of RLS/WED. Sleep Med. 2018;41:27-44. PMID 29425576.",
 "Earley CJ, et al. IV ferric carboxymaltose for RLS: multicenter RCT. Sleep. 2024;47(7):zsae095. PMID 38625730.",
 "Mittal SO, et al. Botulinum toxin in RLS: crossover RCT. Toxins (Basel). 2018;10(10):401. PMC6215171.",
 "Effectiveness/safety of botulinum toxin A in RLS: SR & meta-analysis. Healthcare. 2021;9(11):1538. PMC8623507.",
 "Pyne R, et al. Varicose veins with RLS and nocturnal leg cramps. J Vasc Interv Radiol. 2023;34(4):534-42. PMID 36526075.",
 "Charlesworth JD, et al. Bilateral high-frequency noninvasive peroneal nerve stimulation for RLS. J Clin Sleep Med. 2023;19(7):1199-209. PMID 36856064.",
 "Allen RP, et al. Comparison of pregabalin with pramipexole for RLS. N Engl J Med. 2014;370(7):621-31. PMID 24521108.",
 "Winkelman JW, et al. Efficacy and safety of pramipexole in RLS. Neurology. 2006;67(6):1034-9. PMID 16931507.",
 "Winkelman JW, et al. Randomized PSG study of gabapentin enacarbil in RLS. Mov Disord. 2011;26(11):2065-72. PMID 21611981.",
 "Garcia-Borreguero D, et al. Dipyridamole for RLS: placebo-controlled crossover. Mov Disord. 2021;36(10):2387-92. PMID 34137476.",
])
n2 = d.save(os.path.join(BASE,"02_RLS","RLS_발표.pptx"))

# ============================================================ DECK 3 — LSB
d = Deck()
d.title_slide("요추교감신경차단 (Lumbar Sympathetic Block)",
    ["방법 · 적응증 · 효과", ""],
    "Lumbar Sympathetic Block / Sympatholysis — Technique, Indications, and Efficacy",
    "구성: 개요/해부 → 방법 → 적응증 → 효과 → 합병증 → 결론",
    "교육·연구 참고용. 개별 환자의 진료 결정은 담당 의사의 판단에 따른다.  |  작성 2026-07")

d.bullets_slide("개요 · 해부 · 원리", "개요", "배경", [
    (0,"LSB와 교감신경 신경파괴(sympatholysis)는 70년 이상 다양한 하지 통증·허혈 질환에 사용.",INK,True),
    (0,"표적: 신경절 밀도가 가장 높은 L2–L3(보통 'L2 하 1/3 ~ L3 상 1/3'), 척추체 전외측. 일부 L2/L3/L4 다분절.",INK),
    (0,"원리 ①: 교감신경 차단 → 혈관 확장·측부순환 증가 → 조직 산소화 개선.",INK),
    (0,"원리 ②: 교감신경 매개 통증(sympathetically-maintained pain) 경로 및 자율신경 동반 침해 구심로 차단.",INK),
    (-1,"국소마취제 차단(진단적/치료적)과 화학적/열적 신경파괴로 나뉜다.",TEALD,True),
], "StatPearls NBK431107; Zhang 2022(Ibrain)")

d.split_slide("방법 (Technique)", "방법", "기법", [
    (0,"표준: 방척추(paravertebral) 접근 + 투시(fluoroscopy). CT·초음파도 가능.",INK,True),
    (0,"바늘 진입: 정중선에서 약 7 cm 외측. 척추체 접촉 후 전내측으로 'walk'하여 척추체 전외측으로 진입.",INK),
    (0,"흡인 후 조영제 주입 → 두미측(craniocaudal) 종방향 확산 확인.",INK),
    (0,"성공 지표: 동측 하지 피부온도 ≥2°C 상승.",INK,True),
], ("약제", [
    (0,"진단/치료: lidocaine 1%,",None),
    (0,"  bupivacaine 0.25–0.5%, ropivacaine",None),
    (0,"신경파괴: 무수알코올/phenol, RFA",None),
    (0,"원칙: 신경파괴는 진단적 차단 양성 시에만",None),
], None), "StatPearls; Lumbar Sympatholysis NBK560514", tag_color=TEALD)

d.table_slide("적응증 (Indications)", "적응증", "적응", [
    ("범주","대표 적응증"),
    ("통증증후군","하지 복합부위통증증후군(CRPS I/II) — 조기(≤12개월) 시행이 유리"),
    ("허혈질환","PAD·중증 하지허혈(CLI) 안정통·비재건성, 버거병, 색전, 동상, 혈관연축"),
    ("신경병증","당뇨병성 신경병증/당뇨발, 대상포진후신경통, 환상지통·단단통"),
    ("기타","족부 다한증, 레이노 증후군(하지)·홍색사지통증, 암성 골반/하지통"),
], [Inches(2.4),Inches(9.45)], "StatPearls; 문헌고찰 종합", size=12, row_h=Inches(0.7),
    note="특발성 야간 하지경련(NLC)은 적응증 아님 — '밤 다리증상'이 허혈성 안정통(PAD/CLI)이면 적응. 원인 감별(ABI·도플러) 선행.")

d.split_slide("효과 (1) 관류 개선 · 허혈성 통증", "효과", "효과", [
    (0,"관류 실측(Dickey 2024): LSB 후 후경골동맥 직경 0.17→0.27 cm(+58.8%), 모세혈관 재충혈 3.92→1.30초, 족부온도 +2.8°C.",INK,True),
    (0,"허혈성 통증(PAD): 하지 통증 최대 75%↓, Fontaine 분류·측부관류 개선(Medicina 2024).",GREEN),
    (0,"비재건성 CLI: 교감신경 신경파괴가 절단 외 대안이 없는 환자의 통증조절에 효과적·안전(Barreto 2018).",INK),
], ("실측 수치(Dickey 2024)", [
    (0,"후경골동맥 +58.8%",MINT,True),
    (0,"모세혈관 재충혈 3.92→1.30초",None),
    (0,"족부온도 +2.8°C",None),
    (0,"→ 관류 개선의 객관 근거",MINT,True),
], None), "Dickey 2024(Cureus); Medicina 2024; Barreto 2018", tag_color=GREEN, dark_card=True)

d.bullets_slide("효과 (2) CRPS · 기전", "효과", "효과", [
    (0,"CRPS는 교감신경 매개 통증의 전형 → LSB 후 유의한 통증완화가 축적된 근거. 최적 환자 선택·조기 시행이 성공률↑.",INK,True),
    (0,"Choi 2024(Sci Rep): 교감신경 신경파괴의 효과 지속기간을 전향 관찰로 제시.",INK),
    (0,"반응 예측: 교감신경 피부반응(sympathetic skin response)이 LSB 반응 예측에 유용(Pain Ther 2023).",INK),
    (0,"한계: 중추 감작이 진행되면 시간이 지날수록 효과 감소 가능.",MUTE),
    (-1,"기전 요약: 교감차단 → 측부순환 혈관확장 → 조직 산소화↑ → 통증↓ + 교감매개통 차단 + 신경파괴 직접효과.",TEALD,True),
], "Choi 2024(Sci Rep); Pain Ther 2023")

d.bullets_slide("합병증 · 안전성 · 근거수준", "안전성 · 결론", "안전성", [
    (0,"합병증: 생식대퇴신경통(신경파괴 시 5–10%), 외측대퇴피신경 손상, 기립성 저혈압.",RED,True),
    (0,"혈관·요관·신장 등 내장 구조 천공, 출혈, 신경축(neuraxial) 확산, 신경파괴 후 통증성 신경염(dysesthesia).",INK),
    (0,"근거수준: 대부분 관찰·증례군·소규모 전향연구, 대규모 RCT는 부족(허혈질환·CRPS Level III~IV).",INK),
    (-1,"그럼에도 조기 CRPS·재건 불가능한 중증 하지허혈(안정통)에서 임상적으로 유용.",TEALD,True),
], "StatPearls; 문헌고찰 종합", tag_color=RED)

d.key_slide("핵심 메시지 — LSB", "표준은 투시 유도 방척추 접근, 성공은 온도 ≥2°C", [
    ("방법","L2–L3 방척추 접근·투시, 정중선 7 cm 외측, 조영제 두미측 확산, 성공지표 온도 ≥2°C."),
    ("약제","진단/치료는 국소마취제, 신경파괴는 무수알코올/phenol·RFA — 진단차단 양성 시에만."),
    ("적응증","조기 CRPS·PAD/CLI 안정통·신경병증·다한증 등. 특발성 NLC는 적응 아님."),
    ("효과","관류 실측 개선(Dickey), 허혈통 최대 75%↓, CRPS 통증완화(교감피부반응으로 예측)."),
    ("근거","대규모 RCT 부족(관찰·증례 중심). 조기 CRPS·비재건성 CLI에서 유용."),
])

d.refs_slide("참고문헌 — LSB", [
 "Dua A, Varacallo MA. Lumbar sympathetic block. StatPearls. 2026. NBK431107.",
 "Lumbar sympatholysis. StatPearls. NBK560514.",
 "Zhang JH, Deng YP, Geng MJ. Efficacy of the lumbar sympathetic ganglion block in lower limb pain. Ibrain. 2022;8(4):442-52. PMID 37786587.",
 "Dickey Z, Sharma N. Lumbar sympathetic block leading to increased arterial diameter and blood flow. Cureus. 2024;16(6):e61755. PMID 38975506.",
 "Barreto Junior EPS, et al. Neurolytic block of the lumbar sympathetic chain in critical lower limb ischemia. Braz J Anesthesiol. 2018;68(1):100-3. PMC9391669.",
 "Choi EJ, et al. Effect duration of lumbar sympathetic ganglion neurolysis in CRPS. Sci Rep. 2024;14(1):12693. PMID 38830944.",
 "Gungor S, et al. Sympathetic blocks for CRPS: a case series. Medicine (Baltimore). 2018;97(19):e0705. PMID 29742728.",
 "Effect of lumbar sympathetic blockade on pain, Fontaine classification, collateral perfusion in PAD. Medicina (Kaunas). 2024;60(5):682.",
 "Prediction of LSB efficacy in CRPS type 1 by sympathetic skin response. Pain Ther. 2023;12(3):809-22. PMC10199976.",
])
n3 = d.save(os.path.join(BASE,"03_LSB","LSB_발표.pptx"))

print("NLC", n1, "RLS", n2, "LSB", n3, "slides")
