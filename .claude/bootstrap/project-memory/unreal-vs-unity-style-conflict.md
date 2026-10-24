---
name: unreal-vs-unity-style-conflict
description: "TBH(Unity/C#)의 _camelCase 등 코딩 규칙을 Unreal/C++ (ProjectF, Mining)에 적용하면 안 됨 — Epic 표준은 정반대"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ef4c02f6-9f23-42a6-9ca3-ae5071b46bd9
  modified: 2026-09-02T14:52:11.856Z
---

사용자는 TBH(Unity/C#)와 Unreal/C++ (ProjectF, Mining)을 병행한다. 두 프로젝트의 코딩 규칙이
**정면으로 충돌**하므로 언리얼 파일을 다룰 때 TBH 규칙을 적용하면 안 된다.

| 항목 | TBH (Unity/C#) | Unreal/C++ |
|------|----------------|---------------------|
| private 멤버 | `_camelCase` | 접두사 없는 **PascalCase** |
| bool 변수 | `isMining` | **`bIsMining`** |
| 클래스명 | `OreBlock` | **`AOreBlock`** (U/A/F/I/E/T 접두사 필수) |
| 생성 | `new`, `Instantiate` | `NewObject` / `SpawnActor` / `CreateDefaultSubobject` |
| null 검사 | `!= null` | `IsValid()` |
| 문자열 | `"text"` | `TEXT("text")` |
| 매 프레임 | `Update()` 자유 | Tick은 기본 끔 (`bCanEverTick = false`) |

공통으로 유지되는 것: 축약 금지, 단문에도 중괄호 `{}`, 루프 인덱스 `i, j, k` 순서.

**Why:** 사용자가 언리얼 입문자이고 Unity 감각이 몸에 배어 있어서, 두 규칙이 섞이면
코드 리뷰에서 가장 먼저 티가 나는 종류의 나쁜 습관이 굳는다. 특히 `UPROPERTY()` 없이
UObject 포인터를 멤버로 들고 있으면 GC가 수거해가 런타임에 널이 되는데, Unity 감각으로는
예측이 안 되는 사고다.

**How to apply:** 언리얼 C++ 코드를 리뷰하거나 예시를 보여줄 때 이 표의 오른쪽 열을
쓴다. 사용자가 왼쪽 열 습관으로 쓴 게 보이면 `🚨 습관 경보` 로 즉시 지적한다.
요약: `E:\Unreal\RoadToIO\CLAUDE.md` §2.4. 전체 표(Mining 문서): `E:\Unreal\Mining\docs\ue-conventions.md` §7.
관련: [[unreal-teaching-mode]]
