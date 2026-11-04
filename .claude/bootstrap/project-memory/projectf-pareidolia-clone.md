---
name: projectf-pareidolia-clone
description: "ProjectF (E:\Unreal\RoadToIO\ProjectF, UE5.4, 파레이돌리아 모작) — 종이 연출(Niagara)은 4-1b-1에서 멈춤(11-04), 다음은 대화 연출(모션·눈동자)"
metadata:
  node_type: memory
  type: project
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-11-02T14:02:45.467Z
---

사용자는 Mining과 별개로 `E:\Unreal\RoadToIO\ProjectF` (UE 5.4, C++ 모듈 ProjectF) 에서
게임 '파레이돌리아'를 모작하며 UE5를 학습 중이다. **2026-10-24부터 ProjectF 세션은 `E:\Unreal\RoadToIO` 에서 연다**
(규약: `RoadToIO/CLAUDE.md`, 일지: `RoadToIO/docs/devlog/`). 그 전 세션은 Mining 폴더에서 열렸다.

2026-10-11 기준 종이 연출 작업:
- 에셋: `Content/MovingPaper/` 의 `NS_Paper`(CPU sim, Scratch 모듈 + Collision + Gravity), `BP_PaperArea`(Tick에서 User.PlayerPosition/Velocity 전달), `M_Paper`
- Codex 안내를 사용자가 직접 따라 만든 것 (Codex가 만든 게 아님)
- 레퍼런스 영상 분석 결론: "바닥이 꺼진다" = 발밑이 패이는 게 아니라 **방 바닥 전체가 가구째 엘리베이터처럼 ~3m 하강**.
  종이가 솟구치는 건 착시(종이는 제자리, 카메라가 바닥과 같이 내려감). 이후 종이는 판 공기저항으로 펄럭이며 ~2.5초간 낙하,
  캐릭터 캡슐(발~머리) 전체와 상호작용
- 권장 구조: BP_SinkingFloor(Timeline) → FloorPosition을 NS User 파라미터로 → 종이는 FloorZ 클램프로 착지 판정
- 사용자의 핵심 목표는 바닥 연출이 아니라 **종이 자체**(눕기 / 펄럭 낙하 / 다시 눕기 / 몸 반응)
- 상호작용 결론: 범위(영향 볼륨) 개념은 맞지만 "허리 한 점 + 큰 원 + 고정 세기"는 틀림.
  영상 근거: 서 있으면 반응 없음, 달릴 때 **휘두르는 발**이 지나간 종이만 모서리로 섬, 머리 옆 종이는 휩쓸림.
  → 부위별 작은 구(발L/R·골반·가슴·머리) × **그 부위의 속도**, 바닥 종이는 밀기 대신 뒤집기(회전).
  NS에선 PaperInfluence 스크래치 모듈 하나를 스택에 부위 수만큼 쌓는 방식으로 안내함

버전관리: git 저장소는 ProjectF가 아니라 **상위 `E:\Unreal\RoadToIO`** 에 있다 (origin: github.com/DEV-JSB/RoadToIO, main).
ProjectF 폴더만 보고 "git 없음"이라고 잘못 말한 적 있음 — 항상 `git rev-parse --show-toplevel`로 확인할 것.
2026-10-11 기준 Git LFS 미설정(.gitattributes 없음), .git 939MB(커밋 8개), .sln 추적 중.

학습 방식 (2026-10-11 합의): 종이 연출을 **처음부터 다시** 만든다. BP 노드·HLSL은 사용자가 직접 짜고,
Claude는 막힐 때 짚어주는 역할(티키타카). 로드맵 0~5단계:
0 준비(테스트맵·SM_Paper) → 1 종이 깔기 → 2 FloorZ로 떨어지기 → 3 판 공기저항·펄럭 → 4 부위별 몸 반응 → 5 다듬기(선택).
사용자가 "N단계 막힘"이라고 오면 그 단계 기준으로 이어서 안내. 완성 코드는 먼저 주지 말고 수식·순서로 안내.

진행 (2026-10-12): 0단계·1단계 완료. 에셋은 `Content/PaperFX/` (SM_Paper 21x29.7 4x6분할, M_Paper, NS_PaperField),
구버전은 `Content/LegacyMovingPaper/`. 별도 테스트맵 없이 ThirdPersonMap에서 작업.
NS_PaperField: 이미터 PaperEmitter(CPU, Local Space 끔, Life Cycle System + System State Loop Once),
Spawn Burst 150, Shape Location Box 400x400x0, 스크래치 PaperSpawnInit(Random yaw 0~360, Lift 0.1~0.6 → Custom HLSL로 Z축 쿼터니언),
Particle State kill 끔, Mesh Renderer SM_Paper.
학습 특성: sin/cos·HLSL 지식 없음 → 쿼터니언은 "Z축용 Quaternion.Euler" 블랙박스로, C#→HLSL 대조표로 가르침.
의사코드를 그대로 붙여넣은 적 있음 → 코드와 설명을 명확히 구분해서 줄 것. 값마다 "왜"를 한 줄 붙일 것(사용자 요청).
Attribute Spreadsheet로 값 확인하는 습관을 들임.
2026-10-19: 2단계 진행 중. User.FloorZ(시스템 User Param) 생성, PaperSpawnInit에 Particles.FloorLift·Velocity(0) 추가,
Particle Update에 PaperSim(INPUT Gravity/FloorZ, FloorZ는 스택에서 User.FloorZ에 Link) 작성·컴파일 통과. 다음: PIE 낙하 테스트.
2단계(2-1~2-4) 완료·커밋: PIE에서 낙하·착지 확인. 2-5(BP가 User.FloorZ 자동 주입, BP_PaperRoom + Timeline 하강)는
사용자 결정으로 **보류** — 당분간 FloorZ는 Details 수동값. 나중에 2-5a/2-5b로 이어서 할 것.
내적은 2026-10-19에 "그림자 길이" 비유 + 인터랙티브 위젯(화살표 2개, -1~1)으로 설명 완료(확인 문제 2개는 미풀이). 다음 세션: 외적 → 3단계.
devlog는 날짜-ProjectF.md + 개념 노트는 별도 md(예: 2026-10-19-ProjectF-DotProduct.md)로 분리 — 사용자가 노션에서 하위 페이지로 넣음.
2026-10-22: 외적 페이지(artifact Pex4fDANGiXhRJZAuYTfxT) 만들었으나 사용자는 "잘 모름, 넘어감" — 확인 문제 그만하자고 함(퀴즈 남발 금지).
외적은 3-3에서 문 경첩 비유로 다시. 3단계 계획: 3-1 N 구하기 → 3-2 판 공기저항 → 3-3 회전(펄럭) → 3-4 착지 시 다시 눕기.
Particle Update에 스크래치 `PaperAero`(PaperSim 위)를 만들고 쿼터니언→N 공식으로 Particles.PaperNormal 출력, (0,0,1) 확인 = 3-1 완료.
3-2(TiltDeg ±25 스폰, vn=dot(Vel,N)*N 분리, NormalDrag/PlaneDrag)·3-3(torque=dot(N,v)*cross(N,v)*FlipStrength, AngVel, SpinDrag, moving=step, 쿼터니언 누적) 완료 —
사용자 매우 만족("반할 것 같다"). 커밋 0c649ce(미push). 값: NormalDrag 8, PlaneDrag 0.5, FlipStrength 30, SpinDrag 3.
회고 1층 중 공기저항 편 완료(그림·벡터 덧셈 비유로 이해함) → 아티팩트 H41ic9B8yJwfxAFXrgeU1N + 2026-10-22-ProjectF-PaperDrag.md.
devlog 2026-10-22-ProjectF.md 작성(세션은 10-23 새벽까지). 사용자는 그림+코드+설명 묶음을 매우 좋아함, 기호·추상 비유는 싫어함.
남은 것: 회고 2층(vn=dot 한 줄) → 회고 회전 편(외적, 아직 이해 못함) → 3-4 착지 시 다시 눕기. TiltDeg 0이면 흔들림 시작 안 되는 문제 미정.
2026-10-24: 3-4 완료(사용자 커밋). PaperSim이 PARTICLES Landed(float) 기록, PaperAero는 바닥이면 cross(N,flatN)*SettleSpeed(8)로 눕기, moving 제거.
이어서 **종이가 발밑 바닥을 직접 감지**하도록 변경: PaperSim 그래프에 Custom Hlsl 001(Pos→Start +50cm/End -100m) → Perform Collision Query Sync CPU(INPUT FloorQuery) → CollisionValid/CollisionPosWorld를 FloorHit/FloorPos로 받아 floorZ 계산. 큐브 위 착지 확인.
캐릭터 머리 위에 얹히는 문제 → 트레이스 채널 PaperFloor(기본 Block, Pawn/CharacterMesh Ignore) 안내함(완료 여부 미확인). USER FloorZ는 이제 안 씀.
**범위 결정(사용자): "바닥은 신경 쓰지 말자, 우리는 종이를 구현하는 거다"** → 2-5(바닥 하강 BP)는 범위 밖. 종이 쪽만 진행.
Particle State kill은 1단계에서 꺼 둠 → Spreadsheet의 Lifetime 5는 종이를 지우지 않음(10-24에 잘못 경고했음).
"닿기 전에 서서히 눕기"(PARTICLES Height + SettleHeight lerp) 코드는 안내만 하고 미적용.
2026-10-29: 코드 작업 없음. 지도 ③ 복습(torque = 내적 부호로 꼬챙이 앞뒤 결정, "N·V 평면에 수직으로 꽂고 앞뒤는 내적" — 작업자 문장) + 거속시·소수 나눗셈 복습.
4-1 설계(작업자가 쪼갬): 발 위치 = `GetMesh()->GetSocketLocation("foot_l")`(뼈 이름은 스켈레톤에서 확인 필요), 발 속도 = (지금−이전)/DeltaTime(BeginPlay에서 이전 위치 초기화, DeltaTime>0 확인),
BP가 USER FootPos/FootVel로 NS에 넘김, 종이는 `length(FootPos - Pos)` vs INPUT FootRadius → `step`으로 inside 0/1, 닿으면 **속도를 줌**(작업자 제안).
함정 공유함: 옆으로만 주면 PaperSim `OutVel *= airborne`가 바로 0으로 만듦 → 위쪽 성분 필요, 떠오르면 기존 torque로 저절로 뒤집힐 수 있음. 바닥(Landed=1)에선 settle이 각속도를 덮어씀.
2026-10-30~31: **4-1a 완료.** C++ `UPaperToucherComponent`(Source/ProjectF, BoneName·TouchRadius·bDrawDebug, PartPos/PartVel, DoesSocketExist 검사)를 BP_MateCharacter에 붙임(같은 클래스 3명).
`BP_PaperField`(Content/PaperFX, Niagara 컴포넌트)가 레벨의 NS 액터를 대체, BeginPlay에 Get Player Character→Toucher, Tick에 Set Niagara Variable(Position/Vector3)로 USER FootPos/FootVel.
NS: 새 스크래치 `PaperInfluence`(Particle Update 맨 위) — INPUT FootPos/FootVel은 스택에서 User에 Link, FootRadius 20(디버그 구는 15로 둠), PushStrength 0.5, LiftStrength 0.6 (10-31 개명: KickStrength·LiftRatio → 짝 맞춤), WakeSpeed 100. 속도 방향 ② FootVel+위쪽(|FootVel| 비례), lerp로 "바꾸기", PARTICLES Touched 출력. 떠올라 3단계 torque로 잘 뒤집힘.
배운 함정: PIE 중 Details 패널은 실시간 갱신 안 됨(다시 선택하면 갱신). Rider 2026.2가 번들 MSBuild로 v180을 찾음 → VS2022 MSBuild로 지정.
작업자는 PaperInfluence HLSL을 아직 다 이해 못 함(10-31). 다음: 커밋 2개 확인 → 4-1b(3명×발2 = 6개, 모듈 6번 쌓고 USER Link 방식 유력). 4-1b 쪼개기는 작업자가 먼저.
2026-10-31: **4-1b-1 완료(조작 캐릭터 양발).** BP_MateCharacter에 Toucher_FootL/FootR, BP_PaperField는 `Touchers` 배열(Get Components By Class) → GET[0]/[1] → USER FootPos0/FootVel0/FootPos1/FootVel1,
NS는 PaperInfluence를 2번 쌓음(스크래치 스크립트 이름도 PaperInfluence로 개명 — 목록에서 느린 두 번 클릭). 스택 INPUT이 아직 KickStrength=1.0으로 보였음(개명 미적용?) — 확인 필요.
함정: 와일드카드 GET을 Is Valid 출력 쪽에서 거꾸로 끌어내면 Object로 굳음(작업자가 재현 실험으로 확정), 배열로 타입 변경 후 "Can't parse default value None" 경고.
열린 질문(작업자 제기): **종이가 캐릭터 몸을 관통** — 로드맵에 명시 없음. 작업자: 영상에선 통과 안 함. 판 휘어짐(WPO)도 로드맵에 없음 → 작업자 결정: 로드맵에 넣지 않고 **"디테일 후보"로만** 기록(CLAUDE.md §4).
다음: 4-1b-2(3명×양발) — 작업자가 "변수·모듈을 늘린다"로 답함 → 부위까지 늘면 모듈 15개, 배열 방식(B) 재검토 시점.
2026-11-02 영상 재분석(`C:\Users\mvat1\Videos\화면 녹화\화면 녹화 중 2026-10-11 215421.mp4`, 9.2초, 모니터를 찍은 저해상도. ffmpeg·python·node 없음 →
scratchpad에 PowerShell HttpListener + canvas로 프레임 뽑아 브라우저 패널로 봄): 1.5초 방 전체 종이 동시 상승(바닥 하강 착시, 범위 밖), 2~4.4초 낙하.
**공중 종이는 면이 휘어 있다** — 대부분 한 축으로 둥근 C/U자, 일부는 거의 반 접힌 V(펼친 책). 물결 이동은 해상도상 확인 불가. 바닥에 누운 종이는 평평.
발에 걸린 종이는 모서리로 서고(6.0s, 3.8~4.1s) 서 있는 종이도 살짝 휨. 영상엔 경사면 위 종이 장면 없음(경사 눕기 버그는 우리 맵 문제).
작업자 결정(11-02): 4-1b-2 전에 **판 휘어짐(종이다움)을 먼저** 한다. **C/U 휨만, V 접힘은 안 함**("매일 종이만 구현하겠다" — 범위 걱정, 최소판으로).
**NS Mesh Renderer는 `SM_Paper1`을 씀**(SM_Paper 아님. Approx Size 29×21×0 — 첫 스크린샷을 20×21로 잘못 읽었음, 버텍스 35/삼각형 48 = 4×6 분할). SM_Paper1의 머티리얼 슬롯은 **`M_Paper1`**(M_Paper 아님). Two Sided는 M_Paper에서만 확인함 → M_Paper1도 확인 필요. CLAUDE.md §4 에셋 표(SM_Paper/M_Paper)는 실제와 다름.
휨 최소판 계획: 1단계 M_Paper1 WPO(TexCoord→Mask(R, 긴 쪽 확인됨)→ConstantBiasScale(-0.5,2)→c×c→×BendTest→×BendDepth(3)→×VertexNormalWS) → 2단계 Niagara 종이마다 랜덤 휨 → Dynamic Parameter → 3단계 Landed면 0.
작업자 질문 "이게 클라 프로그래머 일인가?" → 보통 TA 영역이라고 답함. 작업자 결정: **B = 최소판 3단계까지 완주 후 멈춤**(법선 재계산·물결 등 TA 깊이는 안 감), 그다음 4-1b-2.
**11-02 휨 최소판 완료**: Particle Spawn에 Set `PARTICLES PaperBend`(Random Range Float -1~1), Particle Update 맨 아래 Dynamic Material Parameters Index0 Param1 = New Expression `Particles.PaperBend * (1.0 - Particles.Landed)`,
M_Paper1은 BendTest 대신 Dynamic Parameter 첫 출력(Param1). 공중 ∪/∩ 제각각, 바닥 평평 확인. 착지 순간 툭 펴짐 → 디테일 후보 최후순위(작업자).
**11-02 경사면 눕기 완료**: PaperSim이 트레이스 법선 → `OutFloorN = lerp((0,0,1), FloorNrm, hitF)` → PARTICLES FloorN, Spawn Set FloorN=(0,0,1),
PaperAero `flatN = FloorN * (step(0, dot(N,FloorN))*2-1)`. 작업자가 스스로 "중심 한 점이라 절벽에 걸친 종이는 못 처진다" 한계를 짚음 → 절벽 끝 처짐은 디테일 후보.
작업자 가설("바닥 법선을 flatN에")은 맞았음. 연결 안 된 핀(입력 칸 보임) 규칙을 FloorNrm에서 다시 씀. 다음: 4-1b-2.
11-02 회고: 작업자가 faceSign·M_Paper1 노드를 "이해 못 하고 따라 했다", 경사면 가설도 "자동완성"이었다며 답답해함. 진단: GameMathLab 연습 2(내적 부호로 앞뒤 판정)를 건너뜀 + faceSign이 막는 문제를 본 적 없음 + 한 줄에 4단계.
"망가뜨려 보기"(flatN=FloorN) 실험은 실패 — 양면이 같은 색이라 뒤집혀도 결과가 같아 보임, 발차기·TiltDeg 140~160으로도 작업자는 차이를 못 봄. 다음엔 실험 전에 "무엇이 보일지"를 Claude가 먼저 검증할 것(뒷면 색 구분 등). 작업자가 faceSign 실험 후 원복했는지 확인 필요(flatN 두 줄, TiltDeg ±25).
작업자: "Material 쪽은 아예 몰라서 기초부터 배워야 할 것 같다"(11-02) — 머티리얼 기초 학습 트랙 희망. 아직 언제·어디서(GameMathLab? 별도?) 할지는 미정. **다음 순서(작업자 11-03): 머티리얼 기초 먼저 → 휨 노드 다시 짜기 회고는 기초 뒤 → 4-1b-2.** 경사면에서 안 기우는 문제도 제기(PaperAero flatN이 월드 위 고정일 것 — 가설은 작업자에게 맡김).
화면 태그 이름(INPUT 등)으로 말할 것 — 내부 이름(Module.)으로 말했다가 지적받음. 3단계 전에 내적/외적을 그림으로 따로 설명하기로 약속함.

**2026-11-04 결정(작업자): 종이 연출은 여기서 멈춤** (4-1b-1까지, 휨 노드 회고·4-1b-2는 보류). **머티리얼 기초는 종이와 별개로 따로 학습**(작업자 11-04, 어디서·언제는 미정). **다음은 대화 연출** — 대사마다 맞는 모션 + 말하는 사람 쪽으로 다른 캐릭터 눈동자 이동. "모작이니까" ProjectF 안에서 한다. 쪼개기는 작업자가 먼저(대사 한 줄 넘어갈 때 바뀌는 것 전부 적기 → 하나 골라 필요한 값 적기)를 요청해 둠. 파레이돌리아 실제 구현 방식은 Claude도 모른다고 밝힘.

**Why:** 다음 세션에서 같은 영상을 다시 분석하거나 바닥 하강을 "국소 함몰"로 잘못 해석하지 않기 위해.
**How to apply:** ProjectF 종이/바닥 질문이 오면 위 구조를 전제로 이어서 안내한다. [[unreal-teaching-mode]] 규칙은 ProjectF에도 그대로 적용.
