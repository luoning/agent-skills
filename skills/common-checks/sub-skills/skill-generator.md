# Skill Generator & Auto-Registrar (技能派生与自注册规约)

## Trigger
Use when a user requests the creation of a new agent skill, or when expanding/refactoring existing skill blocks.

---

## 1. Skill Creation Modes (双模型生成模式)

在创建新技能时，Agent 必须首先评估运行环境的技能能力：

### 模式 1：环境内存在其他第三方/自定义 Skill 生成工具
1. **模板检索**：读取 `skills/boilerplate-skill.md` 获取通用标准模板。
2. **外部规约学习**：分析当前环境中由第三方提供的 Skill 定义描述。
3. **元合并与派生**：将外部指南中的“方法论”提炼出来，转化为符合我们 DoD 拦截标准的标准化技能文件。
4. **自注册与元审计**：将新技能路径注册至 `config.json`，并执行 `skill_integrity_auditor.py` 与 `generate_mdc.py`。

### 模式 2：环境内无任何创建 Skill 技能（冷启动）
1. **模板检索**：读取 `skills/boilerplate-skill.md`。
2. **依存与层次分析**：分析当前项目的骨架与数据链路，识别新技能的“触发场景（Trigger）”。
3. **编写与物理落盘**：在 `skills/[category-name]/SKILL.md` 中生成核心主控与分步规约。
4. **自注册与元审计**：将新技能路径注册至 `config.json`，并执行 `skill_integrity_auditor.py` 与 `generate_mdc.py`。

---

## 2. Auto-Registration Rule (自动注册协议)

新技能生成后，**不得要求人类手动编辑配置**。Agent 必须通过脚本或自动代码修改，将新技能的主路径追加到仓库根目录的 `config.json` 中：

```json
  "modules": [
    "skills/web-autobuild",
    "skills/common-checks",
    "skills/web-design",
    "skills/[new-skill-category]"  <-- 必须物理追加到 modules 数组中
  ]
```

---

## 3. Definition of Done (DoD)
- [ ] Read and applied the layout format defined in `skills/boilerplate-skill.md`.
- [ ] Created the new `SKILL.md` file under a descriptive `skills/[category-name]/` folder.
- [ ] Appended `"skills/[category-name]"` inside the `modules` array of `config.json`.
- [ ] Successfully ran `python scripts/skill_integrity_auditor.py` with passing results.
- [ ] Successfully compiled rule sets via `python scripts/generate_mdc.py`.
