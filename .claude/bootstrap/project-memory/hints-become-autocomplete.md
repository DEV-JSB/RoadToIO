---
name: hints-become-autocomplete
description: "앱의 Prompt suggestions(입력창 자동완성, Tab)가 Claude 힌트를 읽고 답을 미리 채워 준다 — 가설 질문은 힌트 없이, 막히면 한 칸씩"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f45121fa-5c36-4f97-973e-e95c6e767d32
  modified: 2026-11-02T14:13:38.001Z
---

2026-11-02 경사면 문제에서 작업자가 "그것도 사실상 너 자동완성 본 거야"라고 했다.
**뜻은 데스크톱 앱 입력창의 추천 답장(Prompt suggestions, 설정 `prompt_suggestions` = On)을 Tab으로 받았다는 것**이었다 — Claude는 처음에 "힌트가 많아서 빈칸 채우기가 됐다"로만 오해했음.
추천 답장은 대화를 읽고 다음 사용자 메시지를 따로 모델이 추측하는 기능이라, Claude 질문에 답의 모양(예: "flatN 자리에 뭐가 들어가야? 바닥을 향해 쏘는 무언가에서?")이 들어 있으면 추천에 답이 그대로 나온다.
같은 날 휨(M_Paper1 노드)·faceSign도 이해 못 하고 따라 했다며 답답해함. 반면 "절벽에 절반 걸친 종이는 중심 한 점으로 못 처진다"는 작업자가 스스로 낸 생각이었다.

**Why:** 작업자의 목표는 문제 해결 능력(쪼개기+디버깅)이다. 답이 입력창에 미리 떠 있으면 맞혀도 성장 체감이 없다. [[implement-first-review-later]] 의 "퀴즈·빈칸 금지"와도 같은 뿌리.
**How to apply:** 가설을 물을 때는 먼저 힌트 없이 "어디까지 맞고 어디가 의심스러워?"만 묻는다. 막혔다고 하면 힌트를 **한 칸씩**(위치 → 개념 → 값). Prompt suggestions를 끌지는 작업자 결정(11-02에 끄는 방법만 안내). 새 영역(머티리얼 등)은 노드 표 전에 "HLSL로 몇 줄인지"를 먼저 보여준다. 작업자가 혼자 낸 생각은 따로 짚어 준다.
