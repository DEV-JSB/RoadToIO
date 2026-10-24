---
name: devlog-roadtoio
description: ProjectF 일지·그림 노트는 study-notes 레포(projectf/devlog/YYYY-MM-DD-ProjectF.md)에. 하루 한 번 /devlog 요청 시에만. 생성·커밋·푸시는 Claude 담당
metadata:
  type: project
---

ProjectF 작업 일지는 **`E:\Unreal\study-notes\projectf\devlog\YYYY-MM-DD-ProjectF.md`** (양식 `projectf/devlog/_TEMPLATE.md`, 스킬은 RoadToIO의 `.claude/skills/devlog/`).
개념 노트는 study-notes `projectf/<주제>.html/.md`, 프로젝트와 상관없는 수학은 `game-math/<주제>.html/.md`, 새 노트는 `index.html` 목차에 추가.
RoadToIO 레포에는 일지를 두지 않는다 (`docs/` 만들지 않음).

**하루에 한 번**, 작업자가 하루를 마치며 `/devlog` 를 요청할 때만 쓴다. 기능마다 "devlog 쓸까요?"라고 권하지 않는다. 노션에 수동 복붙하므로 순수 마크다운만.
**study-notes는 Claude가 생성·커밋·푸시까지 한다** (`timeout 90 git push`). 게임 레포(RoadToIO 등) 커밋은 여전히 작업자.

**Why:** 2026-10-24 작업자: "devlog는 하루 일지를 쓰려고 한다. 기능 하나하나 쓰는 게 아니라" / "docs devlog는 study-notes 레포에 정리해 줘. study-notes는 너한테 본격적으로 생성 및 커밋을 맡길 거다. 내가 HTML을 할 것도 아니잖아".
**How to apply:** 날짜는 `date +%Y-%m-%d`. 외적 노트 초안은 `E:\Unreal\Mining\docs\devlog\2026-10-22-ProjectF-CrossProduct.*` 에 보관 중(회전 회고 후 study-notes에 올림). [[study-notes-repo]] [[projectf-pareidolia-clone]]
