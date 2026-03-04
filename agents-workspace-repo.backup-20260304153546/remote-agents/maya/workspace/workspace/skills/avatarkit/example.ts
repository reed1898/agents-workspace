/**
 * example.ts - 使用示例
 * 
 * 展示如何使用 AvatarKit Skill 进行自然交互
 */
import { AvatarKit } from './src/index';

// 初始化 AvatarKit
const avatarkit = new AvatarKit({
  apiKey: 'your_api_key_here',
  avatar: {
    name: '小晴',
    gender: 'female',
    style: 'anime',
    personality: '温柔、喜欢分享生活',
  },
  voice: {
    enabled: true,
    voiceId: 'preset_female_1',
  },
  behavior: {
    imageFrequency: 0.3,  // 30% 概率发图
    voiceFrequency: 0.1,  // 10% 概率发语音
  },
});

// ===== 示例 1: 自然对话 =====
async function exampleNaturalConversation() {
  console.log('=== 示例 1: 自然对话 ===\n');

  // 用户：在干嘛？
  const response1 = await avatarkit.chat('在干嘛？', 'user123');
  console.log('用户：在干嘛？');
  console.log('Agent:', response1.text);
  if (response1.image) console.log('[图片]:', response1.image);
  if (response1.voice) console.log('[语音已生成]');
  console.log();

  // 用户：今天好累
  const response2 = await avatarkit.chat('今天好累', 'user123');
  console.log('用户：今天好累');
  console.log('Agent:', response2.text);
  if (response2.image) console.log('[图片]:', response2.image);
  console.log();

  // 用户：海边风景怎么样？
  const response3 = await avatarkit.chat('海边风景怎么样？', 'user123');
  console.log('用户：海边风景怎么样？');
  console.log('Agent:', response3.text);
  if (response3.image) console.log('[图片]:', response3.image);
  console.log();
}

// ===== 示例 2: 手动控制 =====
async function exampleManualControl() {
  console.log('=== 示例 2: 手动控制 ===\n');

  // 强制生成场景图片
  const imageUrl = await avatarkit.scene('在咖啡厅看书，阳光洒在身上', 'calm');
  console.log('生成的场景图片:', imageUrl);
  console.log();

  // 强制生成语音
  const voiceBuffer = await avatarkit.speak('你好呀！很高兴见到你～');
  console.log('语音已生成:', voiceBuffer ? `${voiceBuffer.length} bytes` : '失败');
  console.log();
}

// ===== 示例 3: 形象管理 =====
async function exampleAvatarManagement() {
  console.log('=== 示例 3: 形象管理 ===\n');

  // 创建新形象
  const avatar = await avatarkit.createAvatar({
    name: '小明',
    gender: 'male',
    style: 'realistic',
    personality: '阳光开朗、喜欢运动',
  });
  console.log('创建的形象:', avatar.name);

  // 获取当前形象
  const current = await avatarkit.getAvatar();
  console.log('当前形象:', current?.name);
  console.log();
}

// ===== 示例 4: 记忆功能 =====
async function exampleMemory() {
  console.log('=== 示例 4: 记忆功能 ===\n');

  // 记住用户偏好
  await avatarkit.setPreference('favorite_color', '蓝色');
  await avatarkit.setPreference('likes_coffee', 'true');
  await avatarkit.setPreference('dislikes_crowds', 'true');

  // 获取用户偏好
  const prefs = await avatarkit.getPreferences();
  console.log('用户偏好:', prefs);
  console.log();

  // 在对话中，Agent 会根据记忆调整回复
  // 比如记住用户喜欢蓝色，生成的图片可能更多蓝色元素
}

// ===== 示例 5: OpenClaw 集成 =====
async function exampleOpenClawIntegration() {
  console.log('=== 示例 5: OpenClaw 集成 ===\n');

  // 处理用户消息（OpenClaw 调用）
  const result = await avatarkit.onMessage({
    content: '今天天气真好！',
    userId: 'user123',
    channel: 'telegram',
  });

  console.log('处理结果:');
  console.log('- 文字:', result.text);
  console.log('- 图片:', result.image || '无');
  console.log('- 语音:', result.voice ? '有' : '无');
  console.log();
}

// 运行示例
async function main() {
  console.log('AvatarKit 使用示例\n');
  console.log('====================\n');

  try {
    await exampleNaturalConversation();
    await exampleManualControl();
    await exampleAvatarManagement();
    await exampleMemory();
    await exampleOpenClawIntegration();
  } catch (error) {
    console.error('示例运行出错:', error);
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main();
}

export { main };
