# Phase 10: Vibe Coding Engineering Defense (事实锁与决策网关)

## Trigger
Use when conducting code audits, local test validations, or before merging PRs. This sub-skill provides a fail-safe defensive layer for Vibe Coding teams to block LLM hallucinations and manage cognitive load.

---

## 1. 🔒 事实双向锁定规则 (Bidirectional Fact Enforcement)

为了防止 Vibe Coder 盲目信任 AI 导致代码中引入幻觉数据或丢失关键业务参数，验证流水线必须执行双向锁定：

1. **正向覆盖 (Forward Coverage)**：
   * 所有在 `.extracted_facts.json` 中定义的核心字段（如运价、港口三字码、仓库代码、时效）必须 100% 出现在生成的 HTML/JS 页面中。
2. **反向防幻觉 (Reverse Anti-Hallucination)**：
   * 任何在 HTML/JS 中出现的**数值常量、价格金额（如 `$900`）、专有名词码**，必须能在 `.extracted_facts.json` 中找到对应的事实映射。
   * 如果页面中包含了 `.extracted_facts.json` 之外凭空捏造的数据，校验器必须拒绝通过。

---

## 2. ⚖️ 决策槽降噪卡点 (Decision Gateway Guard)

AI 提供的设计建议和技术方案可能增加系统的复杂性。所有非事实性建议必须通过决策网关：

1. **自动生成待办**：AI 探测到缺失需求时，自动在 `.decision_pending.json` 中创建决策提案。
2. **非侵入式确认**：初级 Vibe Coder 无需修改复杂代码，只需在 `.decision_pending.json` 中将 `human_approved` 标记为 `true` 或 `false`。
3. **物理阻断**：若代码中检测到已实施的逻辑，但对应的 `proposal_id` 在 `.decision_pending.json` 中为 `false`，构建流水线必须物理拦截。

---

## 3. DoD 校验实现规约

当处于 Vibe Coding 验证阶段时，必须运行 `pipeline_validator.py` 对以下两项进行阻断式拦截：
1. 检测是否有未批准决策（`human_approved: false`）。
2. 检测是否有未定义的事实数据泄露到网页中（例如，虚假报价、未记录的港口名称等）。
