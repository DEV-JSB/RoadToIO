---
name: projectf-pareidolia-clone
description: "사용자는 Mining 외에 E:\\Unreal\\RoadToIO\\ProjectF (UE5.4, '파레이돌리아' 모작)도 작업한다 — 종이 연출을 NS_Paper(Niagara)로 구현 중"
metadata:
  node_type: memory
  type: project
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-10-24T11:05:56.037Z
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
화면 태그 이름(INPUT 등)으로 말할 것 — 내부 이름(Module.)으로 말했다가 지적받음. 3단계 전에 내적/외적을 그림으로 따로 설명하기로 약속함.

**Why:** 다음 세션에서 같은 영상을 다시 분석하거나 바닥 하강을 "국소 함몰"로 잘못 해석하지 않기 위해.
**How to apply:** ProjectF 종이/바닥 질문이 오면 위 구조를 전제로 이어서 안내한다. [[unreal-teaching-mode]] 규칙은 ProjectF에도 그대로 적용.
