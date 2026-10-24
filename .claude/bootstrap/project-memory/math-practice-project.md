---
name: math-practice-project
description: GameMathLab = 게임 수학 전반을 직접 만들어 보며 배우는 UE 5.4 C++ 학습 프로젝트(ProjectF와 분리, 2026-10-24 결정). 내적·외적·회전 연습 4개는 첫 과정일 뿐, 범위를 한정하지 않음
metadata:
  type: project
---

2026-10-24 결정: ProjectF(종이) 세션과 분리해서 **게임 수학 학습용 프로젝트 GameMathLab**을 따로 판다.
**성격: 앞으로 이런저런 수학 지식을 써 보며 배우는 상설 연습장.** 내적·외적·회전에 한정하지 않는다
(작업자: "꼭 내적 외적 회전 기능에 국한하지 말아 줘. 앞으로도 이런저런 수학적 지식을 학습하기 위한 프로젝트라고 해 줘").
안내·문서에서 "세 가지만 하는 프로젝트"처럼 들리게 쓰지 않는다.

- 형태: UE 5.4 Blank, **C++**로 짜고 `DrawDebugDirectionalArrow` 등으로 화면에 그리며 확인
- 위치: `E:\Unreal\GameMathLab` 예정 (새 레포, 처음부터 Git LFS). 생성 전일 수 있음
- 만들면 Claude가 `.gitignore` / `.gitattributes`(LFS) / `CLAUDE.md`(RoadToIO 규약 바탕) 초안 준비. 커밋은 작업자
- 배운 것은 study-notes `game-math/` 에 그림 노트로 (Claude가 생성·커밋)

**첫 과정 (지금 정해진 것):** 종이 코드에서 아직 손에 안 붙은 내적·외적·회전
- 기준 자료: study-notes **PaperAero 한 장 지도** (`E:\Unreal\study-notes\projectf\paper-aero-map.html`)
- 연습 1 적 시야각(내적, 0.71) → 2 맞은 방향 앞뒤좌우(내적 + 외적 부호) → 3 경사면 미끄러짐(vn/vt) → 4 포탑 회전(외적 + 쿼터니언)
- 지도 연결: 1·2 → ②의 dot, ③의 cross / 3 → ② 전체 / 4 → ③ settle + ④. 목표는 지도의 "2층"을 손에 붙이기
- 이후 주제는 그때그때 정함 (예: 보간·이징, 행렬·좌표계 변환, 충돌 판정, 곡선 등 — 작업자가 고르는 대로)

**Why:** 작업자가 "HLSL은 Claude가 대부분 짜 줬고 이해를 못 했다", "학습이라기보다 활용해서 뭔가를 만들어 봐야"라고 함. 종이 세션은 종이 구현용으로 두고 싶어 함.
**How to apply:** 연습마다 실제 게임에서 어디에 쓰는지, 종이 코드나 이전 노트의 어디와 같은지 먼저 짚고 시작. [[projectf-pareidolia-clone]] [[implement-first-review-later]] [[study-notes-repo]]
