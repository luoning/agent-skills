# 《高扩展性 Web 物理框架与视觉 Token 分离设计白皮书》

在面向多品类、多长尾页面的 Web 开发中，“页面错漏百出”、“风格微调侵占开发精力”的根本原因在于**物理布局（Layout）与视觉特征（Theme/Colors）的深层耦合**。

本白皮书旨在提供一套放之四海而皆准的 CSS 物理分离方法论，明确定义其核心架构、跨行业落地范围以及规避“微调陷阱”的判定准则。

---

## 一、 核心架构：三层物理分离体系

本方法论要求将 CSS 物理拆分为三个职责单一、互不污染的文件：

```
css/
├── variables.css   <-- [设计令牌 Token 层]：纯变量，无布局逻辑，全站唯一允许硬编码色值的地方。
├── layout.css      <-- [物理骨架 Layout 层]：纯骨架，决定尺寸、网格、间距，严禁出现具体颜色。
└── theme.css       <-- [视觉特征 Theme 层]：纯质感，决定过渡、流光、阴影，所有颜色均引用 Token 变量。
```

### 1. variables.css (设计令牌层)
*   **职责**：定义品牌色、辅助色、文字对比色、高精度边框色以及阴影深度。
*   **示例**：
    ```css
    :root {
      --brand-color: #005bb5;       /* 主品牌色 */
      --accent-color: #ff6600;      /* 即时转化色 */
      --text-main: #1e293b;         /* 主正文色 */
      --border-fine: rgba(15, 23, 42, 0.08); /* 极细网格线 */
    }
    ```

### 2. layout.css (物理骨架层)
*   **职责**：定义全站统一的排版布局骨架（Grid, Flex, Table 结构），限制最大宽度与间距。
*   **示例**：
    ```css
    .container {
      width: 100%;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 2rem;
    }
    .grid-3 {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 2.5rem;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      border: 1px solid var(--border-fine);
    }
    ```

### 3. theme.css (视觉特征与动效层)
*   **职责**：定义卡片阴影、Hover 升起、流光背景、GEO 锚点高亮等微交互，取色必须使用 `var(...)`。
*   **示例**：
    ```css
    .pedestal-card {
      background: var(--panel-bg);
      border: 1px solid var(--border-fine);
      border-bottom: 4px solid var(--brand-color);
      transition: all 0.3s ease;
    }
    .pedestal-card:hover {
      border-bottom-color: var(--accent-color);
      transform: translateY(-8px);
    }
    ```

---

## 二、 跨行业落地适用范围矩阵

本方法论并不适用于所有的 Web 页面。必须根据**结构复用度**与**状态复杂度**进行判定。以下是四大主流行业的适用范围细分：

### 1. 游戏行业 (Gaming)
*   **黄金适用范围 (Class A)：**
    *   **角色/装备数据库与技能百科 (Wiki & Databases)**：如各英雄的技能数据表、属性参数对照表。页面物理骨架完全一致，通过 `variables.css` 的不同变量为不同属性的角色（如火属性用暖橙色，冰属性用冷蓝色）进行一键换肤。
    *   **游戏补丁公告与版本更新日志 (Patch Notes)**：版本更新日志页面。结构固定为“版本概述 + 平衡性调整表格 + 皮肤插画卡片”。
*   **不适用范围 (Class B)：**
    *   **大版本宣传活动页 / 节日 H5**：视觉天马行空，要求极强的创意视觉冲击力与非标动态特效，强套标准化骨架会限制设计自由。

### 2. 电商行业 (E-Commerce)
*   **黄金适用范围 (Class A)：**
    *   **标准化商品参数规格书 (Product Datasheets)**：尤其是 3C 数码、家电、汽车等需要详细对比参数的商品页。物理骨架规范比例，通过 `variables.css` 区分高端线（曜石黑/金配色）与青春版（多彩渐变）。
    *   **退换货政策与保障服务页 (SLA Policies & Help Center)**：格式高度统一的文本与规则说明页。
*   **不适用范围 (Class B)：**
    *   **个性化买家秀社区 / 动态交互瀑布流**：包含高度复杂的组件状态控制与多媒体动态交互加载。

### 3. 内容与媒体行业 (Content & Media)
*   **黄金适用范围 (Class A)：**
    *   **知识库与长尾百科条目 (Knowledge Base / Wiki Pages)**：如企业 Wiki、开发文档（类似 MDN）。其页面结构高度一致（左侧目录树 + 中间阅读区），layout.css 规范排版字体比例和行高，确保极佳的阅读舒适度。
    *   **专栏汇总与文章列表页 (Collection & Category Pages)**：将同类主题的文章以卡片形式汇聚的落地页。
*   **不适用范围 (Class B)：**
    *   **富媒体互动叙事H5 (Interactive Storytelling)**：需要随着鼠标滚动产生复杂 3D 视差、视轨动画的互动式页面。

### 4. 产品与 SaaS 软件行业 (Product & SaaS)
*   **黄金适用范围 (Class A)：**
    *   **多版本价格对比与功能矩阵页 (Pricing Matrix Pages)**：展示 Free, Pro, Enterprise 各个版本功能差异的对比表格。其物理骨架是通用的，利用 `variables.css` 可以轻松在不同的子品牌或不同国家站点中一键微调品牌高亮色。
    *   **API 接口与集成文档 (API Reference Docs)**：标准化展示请求参数、响应结构、代码示例的文档页面。
*   **不适用范围 (Class B)：**
    *   **SaaS 产品的核心操作控制台 (SaaS App Console)**：用户实际进行配置、拖拽看板、协同编辑的复杂操作后台，这类应用应该依赖状态驱动的组件库（如 Tailwind, UI 组件库）。

---

## 三、 落地决策卡 (Decision Matrix)

| 判定维度 | 推荐采用本方法论 (Class A) | 需引入其他方案 (Class B) |
| :--- | :--- | :--- |
| **内容本质** | 信息陈述、规格指南、参数公示、FAQ问答 | 复杂交互、状态变化、数据看板、逻辑判断 |
| **视觉一致性** | 必须与母品牌严丝合缝，要求高精细规格感 | 需要独特的、颠覆常规的视觉创意或大图插画风格 |
| **开发规模** | 需要在短期内快速铺设 10+ 个同类服务长尾页 | 只有 1 个独立的、生命周期短暂的营销活动页 |
| **技术栈** | 轻量级 Vanilla JS, Web Components, 静态 HTML | React, Vue, Next.js 复杂应用框架 |

---

## 四、 规避“微调陷阱”的开发红线

1.  **红线一：严禁在 HTML 页面内或 JavaScript 中使用内联样式编码具体颜色值。** 
    *   ❌ 错误：`<div style="color: #ff6600;">`
    *   *  正确：`<div style="color: var(--accent-color);">`
2.  **红线二：物理骨架 layout.css 中严禁包含任何 `background`, `color`, `border-color`, `box-shadow` 属性。**
    *   布局文件只管骨架尺寸与定位，任何视觉质感属性必须归入 `theme.css` 或通过 `variables.css` 的变量间接引入。
3.  **红线三：通用组件框架必须封装为 Web Components。**
    *   头尾导航、小挂件等公共框架不允许在每个 HTML 页面里重复复制，一律使用 Web Components 挂载，确保相同框架使用相同的 CSS。
