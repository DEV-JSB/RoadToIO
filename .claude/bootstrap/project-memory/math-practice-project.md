---
name: math-practice-project
description: 내적·외적·회전을 써 보는 연습용 UE 5.4 C++ 프로젝트를 ProjectF와 따로 만들기로 결정(2026-10-24). 위치·레포 미정. 연습 4개 순서 확정
metadata:
  type: project
---

2026-10-24 결정: ProjectF(종이) 세션과 분리해서 **연습 프로젝트를 따로 판다.** 목적은 공부가 아니라 내적·외적·회전을 **써서 작은 기능을 만들며** 복습.

- 형태: UE 5.4 Blank, **C++**로 짜고 `DrawDebugDirectionalArrow`로 화살표를 그리며 확인
- 위치·레포: **미정** (Claude 추천은 새 레포 `E:\Unreal\GameMathLab` 같은 이름 + 처음부터 Git LFS. RoadToIO 안 폴더도 후보)
- 만들면 Claude가 `.gitignore` / `.gitattributes`(LFS) / `CLAUDE.md`(RoadToIO 규약을 바탕으로) 초안을 준비. 커밋은 작업자
- 연습 순서: 1 적 시야각(내적, 판정값 0.71) → 2 맞은 방향 앞뒤좌우(내적 + 외적 부호) → 3 경사면 미끄러짐(vn/vt 분리·따로 감쇠) → 4 포탑 회전(외적 + 쿼터니언, 초당 90°)
- 각 연습이 끝나면 study-notes에 그림 노트로 정리 (원하면)

**Why:** 작업자가 "HLSL은 Claude가 대부분 짜 줬고 이해를 못 했다", "학습이라기보다 활용해서 뭔가를 만들어 봐야 하지 않을까"라고 함. 종이 세션은 종이 구현용으로 두고 싶어 함.
**How to apply:** 작업자가 연습 프로젝트 얘기를 꺼내면 위치부터 확인하고 위 순서로 진행. 줄별 설명에 종이 코드의 어느 줄과 같은지 연결. [[projectf-pareidolia-clone]] [[implement-first-review-later]]
