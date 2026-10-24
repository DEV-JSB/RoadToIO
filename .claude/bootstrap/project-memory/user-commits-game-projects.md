---
name: user-commits-game-projects
description: 언리얼·유니티 게임 프로젝트 저장소의 git commit/push는 작업자만 한다. Claude는 커밋 메시지 초안만 쓴다. 학습 노트(study-notes)는 Claude가 커밋해도 됨
metadata:
  node_type: memory
  type: feedback
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-10-24T10:20:11.195Z
---

언리얼(RoadToIO/ProjectF, Mining 등)과 유니티(TBH 등) **게임 프로젝트 저장소에는 Claude가 `git commit`·`git push`를 하지 않는다.** 커밋할 때가 되면 **커밋 메시지 초안**과 무엇을 스테이징할지(`git status`로 확인한 파일 목록)만 제시한다.

예외: **학습 노트 저장소 `E:\Unreal\study-notes`** 는 Claude가 커밋·푸시해도 된다 ([[study-notes-repo]]).

**Why:** 2026-10-24 3-4 완료 직전 사용자가 "앞으로 커밋은 나만 할 수 있도록 해줘… 너는 커밋 메시지 초안만 작성해줘. 학습 노트는 너가 커밋을 해줘도 상관없어"라고 명시. 직접 커밋하는 습관을 들이려는 것으로 보임 ([[unreal-teaching-mode]]의 "대신 하지 말고 가르쳐라"와 같은 방향).

**How to apply:** 게임 프로젝트에서 "커밋하자"가 나오면 → `git status`/`git diff --stat`로 변경 확인(읽기는 해도 됨) → 메시지 초안 + 포함할 파일 + 주의점(.uasset 저장 여부, Intermediate 등 제외)만 준다. `git add`/`commit`/`push`는 실행하지 않는다. 사용자 전역 `~/.claude/CLAUDE.md`에도 같은 규칙을 적어 유니티 세션에서도 적용되게 함.
