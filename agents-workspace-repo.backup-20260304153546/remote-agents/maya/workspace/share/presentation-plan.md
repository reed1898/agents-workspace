# OpenClaw 实践分享演示文稿创建计划

## 已生成文件
- 大纲文件: `/Users/rain/.openclaw/workspace/share/openclaw-presentation-outline.md`

## 创建 Google Slides 演示文稿

由于 Google Slides API 创建幻灯片比较复杂，建议使用以下方式快速创建：

### 方式1: 使用 Google Slides 导入
1. 打开 Google Slides: https://slides.new
2. 选择 "文件" → "导入幻灯片"
3. 从大纲文件复制内容，按 Slide 分隔粘贴

### 方式2: 使用 Markdown 转 PPT 工具
```bash
# 安装 marp（Markdown 转 PPT）
npm install -g @marp-team/marp-cli

# 生成 PPT
marp openclaw-presentation.md --pptx -o openclaw-presentation.pptx
```

### 方式3: 我直接帮你创建 Google Slides
需要你先授权访问 Google Slides API，然后我可以调用 API 创建。

## 幻灯片结构（14页）

1. 封面 — OpenClaw 实践分享
2. 什么是 OpenClaw？
3. "活人感" — 这不是一个聊天机器人
4. 我用它做了什么？（上）
5. 我用它做了什么？（下）
6. 网友脑洞分享
7. 核心感受 — 本地 vs 云端
8. 核心感受 — 交互方式变革
9. 核心感受 — 数据形式演进
10. 核心感受 — 效率对比
11. 核心感受 — 安全与限制
12. 终极问题 — 如何赚钱？
13. 总结
14. Q&A

## 演讲建议

- **开场演示**: 现场展示 AI 查邮件/生成日报
- **重点案例**: Syncthing 同步、让 AI 了解你
- **引发讨论**: Software is Dead? 商业模式
- **时长控制**: 30-40 分钟（每页 2-3 分钟）

## 后续支持

需要我：
1. 生成可直接导入的 PowerPoint 文件？
2. 细化某个 Slide 的内容？
3. 准备演讲备注（Speaker Notes）？
4. 生成演示用的截图/素材？
