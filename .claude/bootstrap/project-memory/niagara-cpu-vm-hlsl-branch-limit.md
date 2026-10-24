---
name: niagara-cpu-vm-hlsl-branch-limit
description: UE5.4 Niagara CPU Sim의 Custom HLSL에서 if 안에 벡터 일부/생성자 대입 시 Vector VM 컴파일 실패 — step/max로 분기 없이 써야 함
metadata:
  node_type: memory
  type: reference
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-10-19T13:36:09.113Z
---

UE 5.4 Niagara **CPU Sim(Vector VM)** 의 Custom HLSL 노드에서 `if` 블록 안에 벡터를 쓰면 컴파일 실패한다.
2026-10-19 ProjectF `PaperSim`에서 실제로 겪고 확인함.

- `if(...) { OutPos.z = h; }` → `Component x of variable branch_flatten_temp has no valid offset. Possibly uninitialized data being used.`
- `if(...) { OutPos = float3(OutPos.x, OutPos.y, h); }` → `Component x/y/z of variable vec_ctor has no valid offset.`
- 원인: VM은 if를 양쪽 계산 후 선택하는 식으로 펴는데(flatten), 그 임시 벡터를 처리 못 함
- **해결(통과 확인):** 분기 없이 수학으로 고르기
  `float airborne = step(rest, OutPos.z); OutPos.z = max(rest, OutPos.z); OutVel *= airborne;`
- 삼항 `? :`: **float 하나를 고르는 건 통과**(2026-10-24 `float floorZ = FloorHit ? FloorPos.z : -100000.0f;` 컴파일·동작 확인). 벡터를 고르는 삼항은 미검증이라 lerp 권장
- Interpolated Spawning이 켜져 있으면 Update 스크립트 에러가 "Particle Spawn Script Interpolated"에도 한 번 더 찍힘 (원인은 하나)

처음엔 "벡터를 통째로 대입하면 된다"고 잘못 처방했다가 한 번 더 실패함.
**How to apply:** Niagara CPU Custom HLSL을 안내할 때 처음부터 if 대신 step/max/lerp로 가르친다. [[projectf-pareidolia-clone]]
