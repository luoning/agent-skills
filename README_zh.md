# 🛡️ AI Agent Skills Framework

> **The Physical Sandbox & Aesthetic Governance Suite for Coding Agents**  
> 停止让 AI 靠“感觉”写代码。这是一个为 Cursor, Claude Code, Windsurf 和 Copilot 设计的契约式开发、防样式污染与运行时自愈的 AI 智能体技能规范库。

[English](./README.md)

<p align="center">
  <img src="https://img.shields.io/badge/Cursor-MDC%20Ready-0ea5e9?style=for-the-badge&logo=cursor" alt="Cursor MDC Ready">
  <img src="https://img.shields.io/badge/Claude%20Code-Compatible-6366f1?style=for-the-badge&logo=anthropic" alt="Claude Code Compatible">
  <img src="https://img.shields.io/badge/Windsurf-Supported-10b981?style=for-the-badge&logo=windsurf" alt="Windsurf Supported">
  <img src="https://img.shields.io/badge/Autopilot-Sandboxed-f43f5e?style=for-the-badge" alt="Autopilot Sandboxed">
</p>

---

## 💡 为什么需要它？

在大上下文或复杂任务下，传统的 AI 编码助理（如 Cursor Rules）极易发生**“指令漂移（Instruction Drift）”**，导致：
*   **规避与偷懒**：AI 找借口把视觉颜色硬编码在 HTML `style` 中，或在布局文件中塞满 hex/rgb。
*   **设计解耦破碎**：结构骨架与主题样式严重混杂，妨碍通用化换肤与解耦。
*   **运行期异常**：动态生成的 UI 组件挂载流程中产生 Console 崩溃且缺乏自愈机制。

### 🚨 规避对抗方案对比 (Anti-Evasion Matrix)

| 场景 | 传统做法（Soft Rules） | 本框架做法（Hard Sandboxing） | 结果 |
| :--- | :--- | :--- | :--- |
| **阻断绝对路径** | 技能文档包含绝对链接 | **元审计器**：`skill_integrity_auditor.py` 扫描并阻断任何带有本地绝对盘符的链接（确保全员环境通用性）。 | **项目纯净** |
| **行内样式硬编码** | Prompt 申明："请勿写行内样式" | **DoD 静态拦截**：`pipeline_validator.py` 扫描 HTML 中任何带有 color 等修饰的 style 属性，直接报错阻断。 | **AI 妥协重写** |
| **数据事实幻觉** | 文案及价格中发生 AI 虚构 | **双向事实锁**：提取并匹配页面所有数字常数至 `.extracted_facts.json`，拦截虚假业务参数。 | **事实一致** |
| **无源事实/血缘断裂** | 页面硬编码数据且无来源追溯 | **数据血缘网关**：要求页面数值标明 `data-fact-source` 路径，阻断未声明来源的无源常数。 | **100% 可追溯** |
| **流水线越界跳步骤** | AI 自由发挥，直接生成页面 | **物理状态锁**：必须满足前置 `.pipeline_state.json` 阶段 DoD 并写盘，才能加载下一步技能。 | **步步为营** |
| **并行子代理代码合并** | 发生 Git 冲突与状态锁污染 | **Gatekeeper 隔离门**：强制 `workspace = branch` 隔离，主 Agent 扮演 Gatekeeper 校验合并。 | **安全归档** |

---

## 📂 技能库目录架构

```text
agent-skills/
├── README.md                      <-- 极客视觉包装说明书
├── config.json                    <-- 技能库配置文件
├── scripts/
│   ├── install.sh                 <-- 一键 Curl 极速安装挂载脚本
│   ├── pipeline_validator.py      <-- 静态 DoD 物理校验网关（防 CSS 泄露与数据幻觉）
│   ├── skill_integrity_auditor.py <-- 技能元完备性审计器（阻断本地绝对路径）
│   └── generate_mdc.py            <-- MDC 编译器（将技能自动编译为 Cursor 原生规则）
└── skills/
    ├── web-autobuild/
    │   ├── SKILL.md               <-- [主控] 10阶段网页工业化流水线
    │   └── sub-skills/
    │       ├── 1-content-extraction.md
    │       ├── 2-narrative-alignment.md
    │       ├── 3-data-structuring.md
    │       ├── 4-geo-anchors.md
    │       ├── 5-skeleton-html.md
    │       ├── 6-web-components.md
    │       ├── 7-style-separation.md
    │       ├── 8-merging-gatekeeper.md <-- Phase 8: 并行子代理隔离与合并网关
    │       ├── 9-runtime-debugging.md  <-- Phase 9: 运行时自愈与 Console 降噪契约
    │       └── 10-vibecoding-defense.md <-- Phase 10: Vibe Coding 事实锁与决策网关
    ├── web-design/
    │   └── SKILL.md               <-- [视觉审美] B2B 工业级无障碍高对比度 Token 规范
    └── common-checks/
        └── SKILL.md               <-- 技能生命周期元审计与死链校验门
```

---

## ⚡ 极速起步 (1分钟挂载)

### 选项 1：一键挂载到你当前的项目 (推荐)
在你的**目标项目根目录**下运行以下命令，即可全自动拉取规范、部署验证器并**编译出适合当前项目目录的 Cursor MDC 规则**：

```bash
curl -fsSL https://raw.githubusercontent.com/username/agent-skills/main/scripts/install.sh | bash
```

### 选项 2：手动编译导出 MDC 规则
If you cloned this repository, compile the relative skills into Cursor native rules `.cursor/rules/*.mdc`:
```bash
python scripts/generate_mdc.py
```
编译后，Cursor 将在修改 HTML/CSS/JS 文件时**自动匹配、按需懒加载**对应的分阶段技能规则，大幅节省 Token 消耗。

---

## 🔌 核心开发流

### 流派 1：直接构建模式 (Direct Build)
直接启动 `web-autobuild` 主控技能，Agent 将按部就班地引导你完成：数据提取 ➔ 骨架 HTML 5 搭建 ➔ 组件挂载 ➔ 静态 DoD 校验 ➔ 合并校验。

### 流派 2：豪华设计-构建模式 (Premium Design-Build)
1. 启动 `web-design` 技能，AI 助手将进入“顶尖 UI 设计师”人格，规划页面设计 Token。
2. 随后启动 `web-autobuild`，将提取出的审美风格锁入 Phase 1，输出具备流光溢彩（Glassmorphism）、微光边框及多层阴影的高级 B2B 工业展品级落地页。

---

## 🔬 静态与元审计双门闸机制

### Gate 1：项目级 `pipeline_validator.py`
自动在 CI 或 pre-commit 中运行，扫描网页中的样式泄露与事实数据偏差：
*   **阻断**：`layout.css` 中任何硬编码的 hex、rgb、rgba、hsl 或内置颜色关键字。
*   **阻断**：HTML 页面中任何包含颜色的行内 style 声明。
*   **阻断**：未在 `.extracted_facts.json` 注册的业务数值，或未声明血缘归属的无源数据 (`data-fact-source`)。
*   **自愈闭环**：当发生任何拦截阻断时，自动在工作区根目录下输出 `.pipeline_fix_suggestions.json`，给出对决策进行一键获批或代码回滚的指引卡片。

### Gate 2：技能级 `skill_integrity_auditor.py`
用于审查 AI 编写的技能规范自身：
*   **阻断**：任何带有绝对物理路径、本地绝对盘符的 markdown 链接或代码片段（保证全员环境通用性）。
*   **阻断**：不含 trigger 触发条件、死链或描述不合规的技能。学与交互 Token 规范
    └── common-checks/
        └── SKILL.md               <-- 技能生命周期元审计与死链校验门
```

---

## ⚡ 极速起步 (1分钟挂载)

### 选项 1：一键挂载到你当前的项目 (推荐)
在你的**目标项目根目录**下运行以下命令，即可全自动拉取规范、部署验证器并**编译出适合当前项目目录的 Cursor MDC 规则**：

```bash
curl -fsSL https://raw.githubusercontent.com/username/agent-skills/main/scripts/install.sh | bash
```

### 选项 2：手动编译导出 MDC 规则
如果你克隆了本仓库，可直接运行以下命令一键编译生成原生 `.cursor/rules/*.mdc` 文件：
```bash
python scripts/generate_mdc.py
```
编译后，Cursor 将在修改 HTML/CSS/JS 文件时**自动匹配、按需懒加载**对应的分阶段技能规则，大幅节省 Token 消耗。

---

## 🔌 核心开发流

### 流派 1：直接构建模式 (Direct Build)
直接启动 `web-autobuild` 主控技能，Agent 将按部就班地引导你完成：数据提取 ➔ 骨架 HTML 5 搭建 ➔ 组件挂载 ➔ 静态 DoD 校验 ➔ 合并校验。

### 流派 2：豪华设计-构建模式 (Premium Design-Build)
1. 启动 `web-design` 技能，AI 助手将进入“顶尖 UI 设计师”人格，规划页面设计 Token。
2. 随后启动 `web-autobuild`，将提取出的审美风格锁入 Phase 1，输出具备流光溢彩（Glassmorphism）、微光边框及多层阴影的高级 B2B 工业展品级落地页。

---

## 🔬 静态与元审计双门闸机制

### Gate 1：项目级 `pipeline_validator.py`
自动在 CI 或 pre-commit 中运行，扫描网页中的样式泄露：
*   **阻断**：`layout.css` 中任何硬编码的 hex、rgb、rgba、hsl 或内置颜色关键字。
*   **阻断**：HTML 页面中任何包含颜色的行内 style 声明。
*   **阻断**：组件 JS 包含行内样式声明。

### Gate 2：技能级 `skill_integrity_auditor.py`
用于审查 AI 编写的技能规范自身，防止包含私有项目数据和不便移植的配置：
*   **阻断**：任何带有绝对物理路径、本地绝对盘符的 markdown 链接或代码片段（保证全员环境通用性）。
*   **阻断**：不含 trigger 触发条件、死链或描述不合规的技能。
*   **阻断**：包含 `.skill_audit_blacklist` 中配置的任何自定义敏感关键词或本地专属物理路径（如特定项目名称、特定私有环境命名）。

---

## 🚫 自定义元审计黑名单 (`.skill_audit_blacklist`)
为防止特定项目的特有业务名词、私有命名空间意外泄露进可复用的通用 Skill 库中，你可以在本仓库根目录下配置 `.skill_audit_blacklist` 排除文件：
*   在其中写入需要排除拦截的敏感词/路径特征（每行一个）。
*   以 `#` 起头的行会被视作注释而忽略。
*   元审计器在运行时会自动匹配。一旦任何 Skill 文档或生成的 MDC 规则包含黑名单词汇，元审计将物理拦截报错。
