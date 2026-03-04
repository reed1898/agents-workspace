# 小耳👂Jane｜Xiaoer on X: "为 Seedance 2.0 备好弹药：一键直出国际范大牌广告片skill（详细教程）" / X

- Source: x
- URL: https://x.com/xiaoerzhan/status/2022293273738633707
- IngestedAt: 2026-02-14T09:30:42Z
- Tags: #source:x #type:tweet #x #twitter #lang:zh #lang:en #ai #coding-agent #engineering #devtools #product #trading #claude-code
- Status: ok

## 备注

from Telegram message_id:2029

## 内容

Title: 小耳👂Jane｜Xiaoer on X: "为 Seedance 2.0 备好弹药：一键直出国际范大牌广告片skill（详细教程）" / X

URL Source: https://x.com/xiaoerzhan/status/2022293273738633707

Markdown Content:
> 核心价值：4 个 Skills 串联，6 步出片，从静态图到 30 秒成片。

AI做视频的人都知道痛点：图片一致性，画面视频提示词，剪辑手动卡点，一个 30 秒的广告片要搞几天。

我用 Claude Code 的 Skill 系统，把 4 个独立工具串成一条自动化流水线：

*   即梦 — 图生视频

*   ElevenLabs — AI 配音 + 音效

*   Remotion — React 声明式合成

*   Claude — 剧本 + 提示词 + 编排

最终成果：一条 30 秒品牌广告片（Equation 初始方程·香薰蜡烛）,1080p,6 镜头，4 段配音，6 个音效。

这不是一个「广告 Skill」，而是 4 个独立 Skills 的首次组合——像乐高，不是套模板。

如果需要，请留言，需求量大我会考虑开源～～

完整的视频生产流程如下：

Plain Text① 剧本 → Claude 生成镜头脚本 ② 提示词 → 每镜头的画面描述 + 运镜指令 ③ 静态帧 → AI 生图(Nano Banana / Midjourney) ④ 图生视频 → 即梦 API(5秒/镜头) ⑤ 配音+音效 → ElevenLabs TTS + Sound Effects ⑥ 合成 → Remotion 声明式编排 → 渲染输出

每一步都有独立的 Skill 文档和脚本模板，可以单独使用，也可以串联。

最终沉淀为一个完整的项目仓库：ai-video-studio。

给 Claude 品牌信息，它会输出一张镜头脚本表：

[![Image 1: Image](https://pbs.twimg.com/media/HBCd0pvbIAA1Rmw?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022289760572874752)

关键经验

不要每个镜头都有旁白。留白更高级。

开头让画面先说话，结尾一句品牌名收住。

[![Image 2: Image](https://pbs.twimg.com/media/HBCfD9qbcAA5yLZ?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022291123130298368)

每个镜头需要两种提示词：

画面提示词（英文，给生图 AI）

> Plain TextA mathematical equation crystallizing into a spiral form, golden particles converging, dark background, muted grey-white tones with gold accents, cinematic lighting, shot on ARRI Alexa, Aesop-inspired minimalism, 16:9

运镜提示词（中文，给即梦 API）

> Plain Text镜头缓缓推近,金色粒子环绕飘散,烟雾缭绕

为什么运镜用中文？

因为即梦是字节跳动的产品，对中文运镜指令的理解更准确。

提示词公式

Plain Text[场景] + [产品细节] + [光线] + [色调hex] + [技术参数] + [品牌锚点]

比起「高级、优雅、精致」这些形容词，品牌锚点（如 Aesop、Byredo）更有效——AI 已经理解了这些品牌的视觉语言。

[![Image 3: Image](https://pbs.twimg.com/media/HBCfOYpbcAAidKK?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022291302172553216)

用 AI 生成 8-10 张关键帧图片，然后筛选最好的 5-6 张。

筛选标准（按优先级）

1.   色调统一 — 所有帧必须是同一套色彩体系

2.   构图 — 是否有视觉冲击力

3.   产品准确度 — 是否忠实于产品参考图

4.   光线 — 是否一致

这比「精心写一条提示词生成一张完美图」效率高得多。

[![Image 4: Image](https://pbs.twimg.com/media/HBCfWQebAAAMEEo?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022291437417857024)

核心代码（火山引擎签名）

```
JavaScript// generate_videos.mjs
const body = JSON.stringify({
  req_key: "jimeng_ti2v_v30_pro",
  binary_data_base64: [imageBase64],
  prompt: "镜头缓缓推近,产品轮廓在暗处逐渐清晰",
  frames: 121,  // 5秒 @24fps
  aspect_ratio: "16:9"
});

const taskId = await submitTask(imageBase64, prompt, options);
// 轮询等待(通常 1-3 分钟)
const videoUrl = await waitForVideo(taskId);
```

每张静态帧 → 5 秒视频片段。6 个镜头全部生成后进入下一步。

踩过的坑

*   QPS 超限 → 加 2-3 秒延时

*   任务超时 → 轮询等待最长放到 5 分钟

*   运镜没效果 → 简化为单一动作，不要又推又绕又升

[![Image 5: Image](https://pbs.twimg.com/media/HBCfdr_a8AA22K3?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022291565063106560)

配音（TTS）

```
JavaScript// generate_voiceover.js
const audio = await client.textToSpeech.convert(VOICE_ID, {
  text: "Restrained fragrance. Rational allure.",
  model_id: "eleven_turbo_v2_5",
  voice_settings: {
    stability: 0.75,
    similarity_boost: 0.8,
    style: 0.3
  }
});
```

音效（Sound Effects API）

```
JavaScript// generate_sfx.js
const audio = await client.textToSoundEffects.convert({
  text: "gentle match strike followed by soft candle flame",
  duration_seconds: 6,
  prompt_influence: 0.5
});
```

6 个镜头各生成一段音效（电子脉冲、低频共鸣、石材摩擦、火柴声、空灵 pad、品牌收尾音），然后交给 Remotion 混合。

关键发现

英文配音比中文更有「大牌感」。

v1 用中文旁白评分 3 分，v2 切换英文后评分直接到 5 分。

Remotion 的核心优势：用 React 写视频。

不再是拖拽时间线，而是用代码声明式地编排每个镜头的位置、时长、特效、音频。

项目结构

```
Plain Textremotion/
├── src/
│   ├── Root.tsx          # 注册 Composition
│   └── EquationAd.tsx    # 主合成组件
├── public/
│   ├── videos/           # 6 个视频片段
│   └── audio/            # 配音 + 音效 + BGM
└── package.json
```

核心组件：VideoClip

```
TypeScriptconst VideoClip: React.FC<{
  src: string;
  durationInFrames: number;
  playbackRate?: number;
  fadeIn?: number;
  fadeOut?: number;
}> = ({ src, durationInFrames, playbackRate = 1,
        fadeIn = 15, fadeOut = 15 }) => {
  const frame = useCurrentFrame();

  // 处理 fadeIn=0 的边界情况(重要!)
  const fadeInOpacity = fadeIn > 0
    ? interpolate(frame, [0, fadeIn], [0, 1],
        { extrapolateRight: "clamp" })
    : 1;
  const fadeOutOpacity = fadeOut > 0
    ? interpolate(frame,
        [durationInFrames - fadeOut, durationInFrames],
        [1, 0], { extrapolateLeft: "clamp" })
    : 1;

  return (
    <AbsoluteFill style={{ opacity: Math.min(fadeInOpacity, fadeOutOpacity) }}>
      <Video src={src} volume={0} playbackRate={playbackRate} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    </AbsoluteFill>
  );
};
```

主合成：声明式编排

```
TypeScriptexport const EquationAd: React.FC = () => {
  const { fps } = useVideoConfig();
  const sec = (s: number) => Math.round(s * fps);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* 全片 BGM */}
      <Audio src={staticFile("audio/bgm.mp3")} volume={0.3} />

      {/* 镜头 1: 公式浮现 (0-5s) */}
      <Sequence from={0} durationInFrames={sec(5)}>
        <VideoClip src={staticFile("videos/01_equations.mp4")} durationInFrames={sec(5)} fadeIn={0} fadeOut={15} />
      </Sequence>

      {/* 镜头 3: 产品开盖 (10-16s) + 配音延迟0.5s */}
      <Sequence from={sec(10)} durationInFrames={sec(6)}>
        <VideoClip src={staticFile("videos/03_product_opening.mp4")} durationInFrames={sec(6)} playbackRate={0.85} />
        <Sequence from={sec(0.5)}>
          <Audio src={staticFile("audio/voiceover_03.mp3")} volume={1} />
        </Sequence>
      </Sequence>

      {/* 镜头 4: 点燃蜡烛 — 慢镜头 */}
      <Sequence from={sec(16)} durationInFrames={sec(6)}>
        <VideoClip src={staticFile("videos/04_candle.mp4")} durationInFrames={sec(6)} playbackRate={0.7} />
      </Sequence>

      {/* 暗角效果 */}
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,0.4) 100%)`, pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
```

渲染命令

```
Bash# 预览
npx remotion studio

# 渲染
npx remotion render EquationAd out/equation-ad.mp4
```

输出规格：1920x1080 / H.264 + AAC / 30 秒 / 44.8 MB

[![Image 6: Image](https://pbs.twimg.com/media/HBCfpdnagAAjj7_?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022291767362748416)

我做了两次广告测试，进行了提升效果的迭代尝试。

v1：脚本驱动（评分 3/5）

*   55 秒 / 11 镜头 / 中文配音

*   先写剧本 → 按脚本出图 → 最后配音乐

*   问题：上下文爆炸、中文配音缺乏大牌感、太长、串行瓶颈

v2：画面驱动（评分 5/5）

*   30 秒 / 5 镜头 / 英文配音 / Aesop 风格

*   先定视觉标杆 → 多生少选 → 音乐先行

*   团队： Art Director (Opus) + Editor (Sonnet) 并行

关键差异对比

[![Image 7: Image](https://pbs.twimg.com/media/HBCeoIPakAAzGkI?format=jpg&name=small)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022290644933447680)

核心教训

1.   品牌锚点 > 形容词 — 写「Aesop 风格」比写「克制、极简、优雅」有效 10 倍

2.   多生少选 > 精雕一张 — 生 8 张选 5 张比反复修改一张快得多

3.   英文配音 > 中文配音 — 对于高端品牌广告来说

4.   30 秒 = 5 镜头 — 这是黄金比例

广告片之外，同一套工具链也能做 MV 剪辑。

核心差异：卡点

```
Python# 用 librosa 分析音乐节拍
import librosa
y, sr = librosa.load("music.mp3")
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
# 输出鼓点帧数,供 Remotion 卡点用
```

MV 的速度控制法则

段落playbackRatefadeIn/Out舒缓/开场0.5-0.725-40 帧正常叙述0.8-1.020-25 帧高潮快切1.0 8 帧（快切）回落/尾声0.4-0.530-40 帧

关键原则

鼓点换镜头，不要用闪白。

每个镜头至少 2-3 秒，太碎会生硬。

[![Image 8: Image](https://pbs.twimg.com/media/HBCgYDraoAADPU-?format=jpg&name=900x900)](https://x.com/xiaoerzhan/article/2022293273738633707/media/2022292567854063616)

整个系统的一个核心设计是 Provider 抽象。

改一行配置就能换工具：

```
YAML# config/providers.yaml
voiceover:
  default: elevenlabs    # ← 改这里
  providers:
    elevenlabs: { strengths: [英文优秀, 音效API] }
    minimax:    { strengths: [全球第一, 中文极佳, 6秒克隆] }
    index-tts:  { strengths: [开源免费, 本地GPU] }

image_to_video:
  default: jimeng
  providers:
    jimeng:    { strengths: [运镜控制好, 国内访问] }
    runway:    { strengths: [质量高, Gen-3 Alpha] }
    seedance:  { strengths: [质量极高, 2.0版本], status: planned }

composition:
  default: remotion
  providers:
    remotion: { strengths: [React声明式, 精确控制] }
    ffmpeg:   { strengths: [轻量, 命令行] }
```

今天用 ElevenLabs 配音，明天发现 MiniMax 更好，后天 Seedance 2.0 开放 API——只需要改配置，不改工作流。

问题原因解决方案interpolate [0,0] 报错fadeIn=0 导致区间 [0,0]加判断：fadeIn > 0 ? interpolate(...) : 1渲染时符号链接失败Remotion 不支持 symlink直接复制素材到 public/音画不同步配音时长 ≠ 镜头时长先生成配音，根据实际时长调整 durationInFrames即梦运镜没效果提示词太复杂一个镜头一个主要动作中文配音「土」不是技术问题，是定位问题高端品牌用英文

```
Plain Textai-video-studio/
├── SKILL.md                    # 入口文件
├── config/providers.yaml       # Provider 切换
├── workflows/                  # 5 种场景工作流
│   ├── ad-commercial.md        # 品牌广告
│   ├── mv-music-video.md       # MV 剪辑
│   └── ...
├── modules/                    # 能力模块
│   ├── script-writing/         # 剧本生成
│   ├── prompt-engineering/     # 提示词工程
│   ├── image-to-video/         # 图生视频
│   ├── voiceover/              # 配音
│   ├── sound-effects/          # 音效
│   └── composition/            # 合成(Remotion)
├── templates/                  # 可运行的脚本模板
├── evolution/                  # 进化系统
│   ├── learnings.jsonl         # 学习记录
│   └── best-practices.md       # 提炼的最佳实践
└── knowledge/                  # 领域知识
    ├── motion-vocabulary.md    # 运镜词汇表
    └── troubleshooting.md      # 问题排查
```

这套系统的本质不是「AI 帮你做视频」，而是 「AI 帮你搭建一条可复用的视频生产线」。

Skills 就该这么用——不是一个万能的大 Skill，而是多个小 Skill 的灵活组合。

像乐高一样拼接，每次组合都可能产生新的玩法。

下一步：等 Seedance 2.0 API 开放后，替换掉即梦，画面质量会再上一个台阶。配置已经预留好了。

基于 Equation 品牌广告片和 Flower MV 两个实战项目的经验总结 工具链： Claude Code + Remotion + 即梦 + ElevenLabs
