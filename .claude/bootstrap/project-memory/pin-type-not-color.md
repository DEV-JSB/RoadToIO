---
name: pin-type-not-color
description: "Niagara/BP 핀·변수를 안내할 때 색(초록/노랑)이 아니라 자료형(float, Vector, Quat, Position)을 먼저 쓴다"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-10-24T10:12:17.906Z
---

핀이나 변수를 만들라고 안내할 때는 **자료형 이름을 쓴다**: `NormalDrag` (float), `Vel` (Vector), `Q` (Quat), `Position` (Position).
"초록", "노랑" 같은 색으로만 말하지 않는다. 색은 필요하면 확인용으로 괄호 뒤에 덧붙이는 정도.

**Why:** 2026-10-22 사용자가 "INPUT NormalDrag (초록)"을 보고 뭘 만들라는지 몰라서 "다음부터는 초록 이딴식으로 하지 말고 자료형을 써라"라고 함. 만들 때 메뉴에서 고르는 건 자료형 이름이다.

Custom HLSL 핀은 **"왼쪽(입력)" / "오른쪽(출력)"** 처럼 노드 위 위치까지 같이 쓴다. 2026-10-24 3-4에서 "입력 핀 SettleSpeed"라고만 써서 사용자가 오른쪽(출력)에 만들고 `Out_SettleSpeed ... uninitialized` 컴파일 에러가 남.

**태그(PARTICLES / INPUT / USER / ENGINE)는 한 번도 빼먹지 않는다.** 2026-10-24 "Map Get에 `Landed` (float) 추가"라고만 써서 PARTICLES/INPUT 혼동 위험을 만들었고, 사용자가 "왜 안 붙이는 거임? 신경써라"라고 강하게 지적. Map Get/Map Set/Custom HLSL 핀 지시 하나하나마다 태그 + 이름 + 자료형 + (HLSL 핀이면) 왼쪽/오른쪽을 전부 쓴다. 이전 단계에서 같은 걸 했더라도 생략하지 않는다.

**How to apply:** 노드/핀 생성 지시는 항상 `태그 이름 (자료형)` 형식. 예: INPUT `TiltDeg` (float), PARTICLES `Velocity` (Vector). [[unreal-teaching-mode]]의 "화면에 보이는 이름으로 말하기"와 같은 원칙.
