# REQ156 approved logo

用户已通过此版，并授权落实 AI 和推送远端；AI 于 2026-09-13 完成。

- `FAMILY_LOGO_COMPARISON.svg` / `.png`：左侧为 Volatile 原标识，右侧为已通过的 MOMO 猫标识。
- `MOMO_FLOW_CAT_MARK.svg`：独立矢量猫标识。
- `MOMO_HEADER_PREVIEW.png`、`MOMO_PANEL_PREVIEW.png`、`MOMO_LINEART_DETAIL.png`：SVG 局部与合板预览。
- `AUDIT.json`：SVG 生成时的检查快照；其中 AI 哈希是替换前值。最终 AI 检查见 `../CURRENT_BASELINE_AUDIT.json`、`../REQ156_AI_LIVE_READBACK.json`。

最终 AI 为 `../../illustrator/MOMO_R166_REQ146_PANEL.ai`，独立图层 `MOMO_MODULE_LOGO_FLOW_VECTOR`。`../REQ156_AI_BEFORE_REPLACE.png` 用于与最终 AI 导出进行猫标区域外像素比较。

`tools/build_momo_flow_cat.py` 是本机设计生成器，读取相邻 Volatile 工作区原稿；`tools/render_current_momo.js` 使用本机配置的 Sharp。最终 SVG/AI 可直接打开，不依赖这些本机路径。`tools/prepare_momo_logo_native_ai.py` 生成原生 AI 控制点数据；其 JSX 仅添加新猫分组，旧组移除及保存由 Illustrator MCP 单独执行，不是自动发布脚本。审计脚本需要 Python、NumPy 和 Pillow。

本轮完成外观文件与 AI 回读验证；实物线宽再现、工艺及 DFM 仍待确认。
