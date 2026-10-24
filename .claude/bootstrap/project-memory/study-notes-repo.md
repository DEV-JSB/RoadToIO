---
name: study-notes-repo
description: 학습 기록(일지 md + HTML 그림 노트)의 정본은 공개 레포 E:\Unreal\study-notes (GitHub Pages). 생성·커밋·푸시는 Claude 담당
metadata:
  node_type: memory
  type: reference
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-10-24T11:45:21.723Z
---

- 로컬: `E:\Unreal\study-notes` (main, origin https://github.com/DEV-JSB/study-notes.git, Public), 사이트: https://dev-jsb.github.io/study-notes/
- 폴더: `game-math/`(dot-product, vector-ops — 프로젝트와 상관없는 수학), `projectf/`(paper-drag 등 개념 노트 + `devlog/YYYY-MM-DD-ProjectF.md` 일지 + `devlog/_TEMPLATE.md`), 루트 `index.html` 목차, `.nojekyll`
- **2026-10-24부터 study-notes가 정본.** 일지·그림 노트를 여기에 바로 만든다 (RoadToIO에는 두지 않음, Mining의 ProjectF 일지 사본은 삭제).
  예전 HTML 원본(아티팩트 원본)은 `E:\Unreal\Mining\docs\devlog\*.html`에 남아 있고, 외적 노트 초안(`2026-10-22-ProjectF-CrossProduct.*`)도 거기 보관 — 작업자가 외적을 이해한 뒤 올린다.
- HTML은 바로 열리게 맨 앞에 `<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" …><style>body{margin:0}</style>`. 파일명은 짧은 kebab-case, md 링크는 study-notes 안 상대 경로.
- 새 노트가 생기면 index.html 목차에 추가.
- push는 `timeout 90 git push` (자격 증명 창에서 멈춘 적 있음).

**Why:** 작업자가 클로드 로그인 없이 링크만으로 열리고 영구 보존되는 걸 원함. RoadToIO는 비공개 게임 레포라 분리. 2026-10-24 작업자: "study-notes는 너한테 본격적으로 생성 및 커밋을 맡길 거다. 내가 HTML을 할 것도 아니잖아".
**How to apply:** study-notes는 Claude가 만들고 커밋·푸시까지 한다(게임 레포 커밋 금지 규칙의 예외). 일지는 하루 한 번 `/devlog` 요청 시. [[projectf-pareidolia-clone]] [[user-commits-game-projects]]
