# AI Agent Skills Repository

这是一个遵循 GitHub 生产级 AI 编码智能体设计标准（如 `addyosmani/agent-skills`）构建的模块化、可验证的 **AI Agent 技能库框架**。

该框架专为现代 AI 编码助手（如 Claude Code、Cursor、Copilot、Gemini CLI 等）设计，支持通过统一的命令行和物理状态文件约束，引导 Agent 严格执行标准开发生命周期，杜绝偷懒与样式/逻辑污染。

---

## 📂 目录结构与技能体系

本仓库采用“主控中心 + 独立子技能 + 物理验证脚本”的紧凑型架构：

```text
agent-skills/
├── README.md                      <-- 仓库总览与说明文档
├── config.json                    <-- 技能库配置文件
├── scripts/
│   └── pipeline_validator.py      <-- 通用物理状态锁与代码隔离静态验证器
└── skills/
    ├── web-autobuild/
    │   ├── SKILL.md               <-- [主控] 7阶段 Web 自动化构建流水线
    │   └── sub-skills/
    │       ├── 1-content-extraction.md
    │       ├── 2-narrative-alignment.md
    │       ├── 3-data-structuring.md
    │       ├── 4-geo-anchors.md
    │       ├── 5-skeleton-html.md
    │       ├── 6-web-components.md
    │       └── 7-style-separation.md
    └── common-checks/
        └── SKILL.md               <-- 通用代码规范与提单 CR 校验技能
```

---

## 🛠️ 核心设计原则

1. **物理锁契约 (State Lock Protocol)**：
   利用根目录下的 `.pipeline_state.json` 跟踪 Agent 工作进度，强制执行“前置步骤未通过 DoD (Definition of Done)，禁止继续编写代码”的物理约束。
2. **零颜色污染 (Zero Color Pollution)**：
   要求所有的网页物理骨架布局与视觉主题进行彻底分离。提供 `pipeline_validator.py` 自动化测试脚本，强力屏蔽任何 rgba/hsla/内置颜色名以及 HTML 行内样式的硬编码色彩泄露。
3. **心智对齐与 GEO 优化**：
   在技能链的前端强化内容拆解与面向买家决策心智的文案翻译；在中端强制要求为数据和 FAQ 注入唯一的语义化 HTML 锚点 ID，使 AI 生成式搜索引擎能够精准召回 Citation 跳转。

---

## 🚀 如何在项目中使用

### 1. 挂载到 Cursor
将 `skills/` 目录拷贝到你项目的 `.cursor/rules/` 目录下，Cursor 能够自动读取并应用这些规则限制。

### 2. 挂载到 Claude Code
在你的项目根目录下，将本仓库的 `skills/` 目录软链接到 `.claude/skills/` 即可按需加载：
```bash
ln -s <path_to_agent_skills_repo>/skills/ .claude/skills
```
