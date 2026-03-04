(() => {
  if (window.__openclawCopilotInjected) return;
  window.__openclawCopilotInjected = true;

  const DEFAULT_LAYOUT_MODE = 'push';
  const LAYOUT_MODE_VERSION = 2;
  const DEFAULT_SESSION_KEY = 'main';
  const DEFAULT_GATEWAY_URL = 'ws://127.0.0.1:18789';
  const MAX_TIMELINE_ITEMS = 300;
  const HISTORY_STORAGE_PREFIX = 'oc-copilot-history';
  const SHORTCUTS_STORAGE_KEY = 'clawsideShortcuts';
  const SHORTCUT_COUNT = 3;
  const SHORTCUT_ACTIONS = ['chat', 'summarize', 'save-kb', 'todo'];
  const DEFAULT_LANGUAGE_PREFERENCE = 'auto';
  const DEFAULT_BUBBLE_POSITION = 'bottom-right';
  const BUBBLE_POSITIONS = ['bottom-right', 'bottom-left', 'top-right', 'top-left'];

  const I18N_STRINGS = {
    en: {
      bubbleTitle: 'Open ClawSide',
      bubbleAria: 'Open ClawSide',
      panelAria: 'ClawSide Panel',
      settings: 'Settings',
      close: 'Close',
      closeSidebarChat: 'Close sidebar chat',
      agents: 'Agents',
      editAgent: 'Edit Agent',
      addAgent: 'Add Agent',
      editCurrentAgent: 'Edit current agent',
      layoutSettings: 'Layout Settings',
      done: 'Done',
      layoutMode: 'Layout Mode',
      layoutModePushOption: 'Push (default)',
      layoutModeOverlayOption: 'Overlay',
      layoutModePushName: 'Push',
      layoutModeOverlayName: 'Overlay',
      language: 'Language',
      languageAuto: 'Auto (Chrome)',
      languageZh: 'Chinese',
      languageEn: 'English',
      defaultBubblePosition: 'Default Bubble Position',
      bubblePositionBottomRight: 'Bottom Right',
      bubblePositionBottomLeft: 'Bottom Left',
      bubblePositionTopRight: 'Top Right',
      bubblePositionTopLeft: 'Top Left',
      languageChoiceAuto: 'Auto (Chrome)',
      languageChoiceZh: 'Chinese',
      languageChoiceEn: 'English',
      context: 'Context',
      quickShortcuts: 'Quick Shortcuts',
      shortcutLabel: 'Shortcut {index} Label',
      action: 'Action',
      prompt: 'Prompt',
      actionChat: 'Chat',
      actionSummarize: 'Summarize',
      actionSaveKb: 'Save KB',
      actionTodo: 'Todo',
      saveShortcuts: 'Save Shortcuts',
      resetDefaults: 'Reset Defaults',
      shortcutsSaved: 'Shortcuts saved.',
      shortcutsReset: 'Shortcuts reset to defaults.',
      agentSettings: 'Agent Settings',
      addAgentPane: 'Add Agent',
      editAgentPane: 'Edit Agent',
      createAgent: 'Create Agent',
      saveAgent: 'Save Agent',
      deleteAgent: 'Delete Agent',
      testConnection: 'Test',
      openFullSettingsPage: 'Open Full Settings Page',
      newSession: 'New Session',
      tooltipSettings: 'Settings',
      tooltipNewSession: 'New session',
      tooltipClose: 'Close sidebar chat',
      tooltipEditAgent: 'Edit current agent',
      tooltipAddAgent: 'Add agent',
      agentName: 'Agent Name',
      gatewayUrl: 'Gateway URL',
      token: 'Token',
      sessionKey: 'Session Key',
      send: 'Send',
      captureScreenshot: 'Attach image',
      removeAttachment: 'Remove attachment',
      screenshotAttached: 'Image attached',
      screenshotAttachFailed: 'Image attach failed: {error}',
      screenshotPromptAnalyze: 'Please analyze the attached image.',
      inputPlaceholder: 'Ask anything',
      emptyChat: 'Start chatting with OpenClaw.',
      roleYou: 'You',
      roleSystem: 'System',
      noAgent: 'No agent',
      noAgentConfigured: 'No agent configured',
      fillAndCreate: 'Fill fields and click Create Agent.',
      switchedTo: 'Switched to {name}.',
      layoutSaved: 'Layout saved: {mode}.',
      bubblePositionSaved: 'Bubble position saved.',
      bubblePositionDefaultApplied: 'Default bubble position applied.',
      languageSaved: 'Language saved: {language}.',
      agentCreatedSelected: 'Agent created and selected.',
      agentSaved: 'Agent saved.',
      needOneAgent: 'At least one agent is required.',
      agentDeleted: 'Agent deleted.',
      testing: 'Testing...',
      testFailed: 'Test failed: {error}',
      testFailedWithCode: 'Test failed ({status}): {detail}',
      connectionOk: 'Connection OK ({status}). {message}',
      ready: 'Ready.',
      cannotOpenSettings: 'Cannot open full settings page automatically.',
      newSessionStarted: 'New session started. Context reset and current page loaded.',
      newSessionFailed: 'Failed to start new session: {error}',
      noResponse: 'No response from OpenClaw.',
      requestFailed: 'Request failed.',
      streaming: 'Waiting for OpenClaw output...',
      pageContextDefault: 'Current page',
      pageContextAria: 'Current page context',
      additionalRequirements: 'Additional requirements: ',
      contextAsk: 'About the following text: "{text}"',
      contextTranslate: 'Translate the following text to English (if already English, translate to Chinese):\n\n"{text}"',
      contextExplain: 'Explain the following text in simple terms:\n\n"{text}"',
      defaultPromptChat: 'Hello',
      defaultPromptSummarize: 'Summarize this page.',
      defaultPromptSaveKb: 'Save this page context to knowledge base.',
      defaultPromptTodo: 'Review: {title}',
      defaultReplyChat: 'Done.',
      defaultReplySummarize: 'Summary completed.',
      defaultReplySaveKb: 'Saved to knowledge base.',
      defaultReplyTodo: 'Todo saved.',
      agentNameTemplate: 'Agent {index}',
      shortcutSkillLabel: 'To Skill',
      shortcutSkillPrompt: 'Convert this article into a reusable OpenClaw Skill. Include skill name, goal, input, steps, and cautions.',
      shortcutSummaryLabel: 'Summarize',
      shortcutSummaryPrompt: 'Summarize the article topic, core arguments, and key conclusions.',
      shortcutKbLabel: 'Save to KB',
      shortcutKbPrompt: 'Extract key information from this article and save it to the knowledge base.'
    },
    zh: {
      bubbleTitle: '打开 ClawSide',
      bubbleAria: '打开 ClawSide',
      panelAria: 'ClawSide 面板',
      settings: '设置',
      close: '关闭',
      closeSidebarChat: '关闭边栏聊天',
      agents: 'Agents',
      editAgent: '编辑 Agent',
      addAgent: '新增 Agent',
      editCurrentAgent: '编辑当前 Agent',
      layoutSettings: '布局设置',
      done: '完成',
      layoutMode: '布局模式',
      layoutModePushOption: 'Push（默认）',
      layoutModeOverlayOption: 'Overlay',
      layoutModePushName: 'Push',
      layoutModeOverlayName: 'Overlay',
      language: '语言',
      languageAuto: '自动（跟随 Chrome）',
      languageZh: '中文',
      languageEn: 'English',
      defaultBubblePosition: '入口球默认位置',
      bubblePositionBottomRight: '右下',
      bubblePositionBottomLeft: '左下',
      bubblePositionTopRight: '右上',
      bubblePositionTopLeft: '左上',
      languageChoiceAuto: '自动（跟随 Chrome）',
      languageChoiceZh: '中文',
      languageChoiceEn: 'English',
      context: '上下文',
      quickShortcuts: '快捷动作',
      shortcutLabel: '快捷词 {index} 名称',
      action: '动作',
      prompt: '提示词',
      actionChat: '聊天',
      actionSummarize: '总结',
      actionSaveKb: '存知识库',
      actionTodo: '待办',
      saveShortcuts: '保存快捷动作',
      resetDefaults: '恢复默认',
      shortcutsSaved: '快捷动作已保存。',
      shortcutsReset: '快捷动作已恢复默认。',
      agentSettings: 'Agent 设置',
      addAgentPane: '新增 Agent',
      editAgentPane: '编辑 Agent',
      createAgent: '创建 Agent',
      saveAgent: '保存 Agent',
      deleteAgent: '删除 Agent',
      testConnection: '测试',
      openFullSettingsPage: '打开完整设置页',
      newSession: '新会话',
      tooltipSettings: '设置',
      tooltipNewSession: '新会话',
      tooltipClose: '关闭边栏聊天',
      tooltipEditAgent: '编辑当前 Agent',
      tooltipAddAgent: '新增 Agent',
      agentName: 'Agent 名称',
      gatewayUrl: '网关地址',
      token: 'Token',
      sessionKey: 'Session Key',
      send: '发送',
      captureScreenshot: '添加图片',
      removeAttachment: '移除附件',
      screenshotAttached: '已附加图片',
      screenshotAttachFailed: '图片附加失败：{error}',
      screenshotPromptAnalyze: '请分析这张已附加的图片。',
      inputPlaceholder: '有问题，尽管问',
      emptyChat: '开始和 OpenClaw 聊天吧。',
      roleYou: '你',
      roleSystem: '系统',
      noAgent: '暂无 Agent',
      noAgentConfigured: '尚未配置 Agent',
      fillAndCreate: '填写完成后点击创建 Agent。',
      switchedTo: '已切换到 {name}。',
      layoutSaved: '布局已保存：{mode}。',
      bubblePositionSaved: '入口球位置已保存。',
      bubblePositionDefaultApplied: '已应用默认入口球位置。',
      languageSaved: '语言已保存：{language}。',
      agentCreatedSelected: 'Agent 已创建并选中。',
      agentSaved: 'Agent 已保存。',
      needOneAgent: '至少需要保留一个 Agent。',
      agentDeleted: 'Agent 已删除。',
      testing: '测试中...',
      testFailed: '测试失败：{error}',
      testFailedWithCode: '测试失败（{status}）：{detail}',
      connectionOk: '连接成功（{status}）。{message}',
      ready: '已就绪。',
      cannotOpenSettings: '无法自动打开完整设置页。',
      newSessionStarted: '已开启新会话，已重置并加载当前页面上下文。',
      newSessionFailed: '新会话启动失败：{error}',
      noResponse: 'OpenClaw 无响应。',
      requestFailed: '请求失败。',
      streaming: '正在等待 OpenClaw 输出...',
      pageContextDefault: '当前页面',
      pageContextAria: '当前页面上下文',
      additionalRequirements: '附加要求：',
      contextAsk: '关于以下文本："{text}"',
      contextTranslate: '请翻译以下文本（如果是中文则翻译为英文，如果是英文则翻译为中文）：\n\n"{text}"',
      contextExplain: '请用简单易懂的方式解释以下文本：\n\n"{text}"',
      defaultPromptChat: '你好',
      defaultPromptSummarize: '请总结当前页面。',
      defaultPromptSaveKb: '请把当前页面内容保存到知识库。',
      defaultPromptTodo: '处理任务：{title}',
      defaultReplyChat: '完成。',
      defaultReplySummarize: '总结完成。',
      defaultReplySaveKb: '已保存到知识库。',
      defaultReplyTodo: '待办已保存。',
      agentNameTemplate: 'Agent {index}',
      shortcutSkillLabel: '转为 Skill',
      shortcutSkillPrompt: '请把当前文章转化为一个可复用的 OpenClaw Skill，输出 skill 名称、目标、输入、步骤和注意事项。',
      shortcutSummaryLabel: '总结主题',
      shortcutSummaryPrompt: '请总结当前文章的主题、核心观点和关键结论。',
      shortcutKbLabel: '保存知识库',
      shortcutKbPrompt: '请提炼当前文章的关键信息，并保存到知识库。'
    }
  };

  function normalizeLanguagePreference(value) {
    const raw = String(value || '').trim().toLowerCase();
    if (raw === 'zh' || raw === 'en') return raw;
    return DEFAULT_LANGUAGE_PREFERENCE;
  }

  function detectBrowserLanguage() {
    try {
      const raw = typeof chrome?.i18n?.getUILanguage === 'function'
        ? chrome.i18n.getUILanguage()
        : (navigator.language || 'en');
      return String(raw || 'en').toLowerCase().startsWith('zh') ? 'zh' : 'en';
    } catch (err) {
      console.warn('[ClawSide] detectBrowserLanguage failed, defaulting to en:', err?.message);
      return 'en';
    }
  }

  function resolveLanguage(preference = DEFAULT_LANGUAGE_PREFERENCE) {
    const normalized = normalizeLanguagePreference(preference);
    return normalized === DEFAULT_LANGUAGE_PREFERENCE ? detectBrowserLanguage() : normalized;
  }

  let languagePreference = DEFAULT_LANGUAGE_PREFERENCE;
  let activeLanguage = resolveLanguage(languagePreference);

  function t(key, vars = {}) {
    const pack = I18N_STRINGS[activeLanguage] || I18N_STRINGS.en;
    const fallback = I18N_STRINGS.en || {};
    let message = pack[key] || fallback[key] || key;
    Object.keys(vars).forEach((name) => {
      message = message.replace(new RegExp(`\\{${name}\\}`, 'g'), String(vars[name]));
    });
    return message;
  }

  function localizedDefaultShortcuts(lang = activeLanguage) {
    const pack = I18N_STRINGS[lang] || I18N_STRINGS.en;
    return [
      {
        id: 'shortcut-skill',
        label: pack.shortcutSkillLabel,
        action: 'chat',
        prompt: pack.shortcutSkillPrompt
      },
      {
        id: 'shortcut-summary',
        label: pack.shortcutSummaryLabel,
        action: 'summarize',
        prompt: pack.shortcutSummaryPrompt
      },
      {
        id: 'shortcut-kb',
        label: pack.shortcutKbLabel,
        action: 'save-kb',
        prompt: pack.shortcutKbPrompt
      }
    ];
  }

  function isBuiltInShortcutDefault(item, index) {
    const normalizedAction = normalizeShortcutAction(String(item?.action || '').trim(), 'chat');
    const label = String(item?.label || '').trim();
    const prompt = String(item?.prompt || '').trim();

    const langs = ['zh', 'en'];
    for (const lang of langs) {
      const defaults = localizedDefaultShortcuts(lang);
      const fallback = defaults[index] || defaults[0];
      if (!fallback) continue;
      if (label === fallback.label && prompt === fallback.prompt && normalizedAction === fallback.action) {
        return true;
      }
    }
    return false;
  }

  async function relocalizeBuiltinShortcutsIfNeeded() {
    const targetDefaults = localizedDefaultShortcuts(activeLanguage);
    const currentItems = Array.isArray(shortcutState.items) ? shortcutState.items : [];
    let changed = false;

    const nextItems = [];
    for (let i = 0; i < SHORTCUT_COUNT; i += 1) {
      const current = normalizeShortcut(currentItems[i] || {}, i);
      const target = targetDefaults[i] || targetDefaults[0];

      if (isBuiltInShortcutDefault(current, i) && target) {
        const nextItem = {
          ...current,
          label: target.label,
          prompt: target.prompt,
          action: target.action
        };
        if (
          nextItem.label !== current.label ||
          nextItem.prompt !== current.prompt ||
          nextItem.action !== current.action
        ) {
          changed = true;
        }
        nextItems.push(nextItem);
        continue;
      }

      nextItems.push(current);
    }

    if (!changed) return;
    const nextState = { items: nextItems };
    applyShortcutState(nextState);
    await writeSync({ [SHORTCUTS_STORAGE_KEY]: nextState });
  }

  // ── Lightweight Markdown Renderer ──────────────────────
  function renderMarkdown(text) {
    if (!text) return '';
    const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

    // Split fenced code blocks first
    const parts = text.split(/(```[\s\S]*?```)/g);
    let html = '';

    for (const part of parts) {
      if (part.startsWith('```')) {
        const match = part.match(/^```(\w*)\n?([\s\S]*?)```$/);
        const lang = match?.[1] || '';
        const code = match?.[2] || part.slice(3, -3);
        const langAttr = lang ? ` data-lang="${esc(lang)}"` : '';
        html += `<pre class="oc-md-pre"${langAttr}><code>${esc(code.replace(/\n$/, ''))}</code></pre>`;
        continue;
      }

      // Process block-level elements line by line
      const lines = part.split('\n');
      let i = 0;
      while (i < lines.length) {
        const line = lines[i];

        // Headings
        const headingMatch = line.match(/^(#{1,3})\s+(.+)$/);
        if (headingMatch) {
          const level = headingMatch[1].length;
          html += `<h${level + 2} class="oc-md-h">${inlineMarkdown(esc(headingMatch[2]))}</h${level + 2}>`;
          i++;
          continue;
        }

        // Unordered list items (collect consecutive)
        if (/^\s*[-*]\s+/.test(line)) {
          html += '<ul class="oc-md-ul">';
          while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
            const item = lines[i].replace(/^\s*[-*]\s+/, '');
            html += `<li>${inlineMarkdown(esc(item))}</li>`;
            i++;
          }
          html += '</ul>';
          continue;
        }

        // Ordered list items
        if (/^\s*\d+[.)]\s+/.test(line)) {
          html += '<ol class="oc-md-ol">';
          while (i < lines.length && /^\s*\d+[.)]\s+/.test(lines[i])) {
            const item = lines[i].replace(/^\s*\d+[.)]\s+/, '');
            html += `<li>${inlineMarkdown(esc(item))}</li>`;
            i++;
          }
          html += '</ol>';
          continue;
        }

        // Blockquote
        if (line.startsWith('> ')) {
          let quoteLines = [];
          while (i < lines.length && lines[i].startsWith('> ')) {
            quoteLines.push(lines[i].slice(2));
            i++;
          }
          html += `<blockquote class="oc-md-bq">${inlineMarkdown(esc(quoteLines.join('\n')))}</blockquote>`;
          continue;
        }

        // Horizontal rule
        if (/^[-*_]{3,}\s*$/.test(line)) {
          html += '<hr class="oc-md-hr">';
          i++;
          continue;
        }

        // Empty line → break
        if (line.trim() === '') {
          i++;
          continue;
        }

        // Regular paragraph
        html += `<p class="oc-md-p">${inlineMarkdown(esc(line))}</p>`;
        i++;
      }
    }

    return html;
  }

  function sanitizeHref(escapedUrl) {
    const raw = escapedUrl
      .replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
    const normalized = raw.replace(/[\s\x00-\x1f]/g, '');
    if (/^https?:\/\//i.test(normalized)) return escapedUrl;
    if (/^mailto:/i.test(normalized)) return escapedUrl;
    if (/^tel:/i.test(normalized)) return escapedUrl;
    if (/^#/.test(normalized)) return escapedUrl;
    if (/^[a-z][a-z0-9+\-.]*:/i.test(normalized)) return '';
    return escapedUrl;
  }

  function inlineMarkdown(html) {
    return html
      // inline code
      .replace(/`([^`]+)`/g, '<code class="oc-md-code">$1</code>')
      // bold
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/__(.+?)__/g, '<strong>$1</strong>')
      // italic
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/_(.+?)_/g, '<em>$1</em>')
      // links (with URL protocol sanitization)
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, text, url) => {
        const safe = sanitizeHref(url);
        if (!safe) return text;
        return `<a href="${safe}" target="_blank" rel="noopener noreferrer">${text}</a>`;
      });
  }

  function newAgentId() {
    return `agent-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  }

  function normalizeLayoutMode(mode) {
    return mode === 'overlay' ? 'overlay' : DEFAULT_LAYOUT_MODE;
  }

  function normalizeBubbleDefaultPosition(value) {
    const raw = String(value || '').trim().toLowerCase();
    return BUBBLE_POSITIONS.includes(raw) ? raw : DEFAULT_BUBBLE_POSITION;
  }

  function normalizeBubbleCustomPosition(value) {
    if (!value || typeof value !== 'object') return null;
    const x = Number(value.x);
    const y = Number(value.y);
    if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
    return { x, y };
  }

  function normalizeShortcutAction(action, fallback = 'chat') {
    return SHORTCUT_ACTIONS.includes(action) ? action : fallback;
  }

  function normalizeShortcut(raw = {}, index = 0) {
    const defaults = localizedDefaultShortcuts(activeLanguage);
    const fallback = defaults[index] || defaults[0];
    return {
      id: String(raw.id || fallback.id || `shortcut-${index + 1}`),
      label: String(raw.label || '').trim() || fallback.label,
      action: normalizeShortcutAction(String(raw.action || '').trim(), fallback.action),
      prompt: String(raw.prompt || '').trim() || fallback.prompt
    };
  }

  function ensureShortcutState(stored = {}) {
    const rawItems = Array.isArray(stored) ? stored : (Array.isArray(stored.items) ? stored.items : []);
    const items = [];
    for (let i = 0; i < SHORTCUT_COUNT; i += 1) {
      items.push(normalizeShortcut(rawItems[i] || {}, i));
    }
    return { items };
  }

  function normalizeAgent(raw = {}, fallbackId) {
    const id = raw.id || fallbackId || newAgentId();
    return {
      id,
      name: String(raw.name || '').trim() || 'OpenClaw Agent',
      baseUrl: String(raw.baseUrl || '').trim() || DEFAULT_GATEWAY_URL,
      token: String(raw.token || '').trim(),
      sessionKey: String(raw.sessionKey || '').trim() || DEFAULT_SESSION_KEY
    };
  }

  function ensureOpenClawState(stored = {}) {
    if (Array.isArray(stored.agents) && stored.agents.length > 0) {
      const agents = stored.agents.map((agent, index) => normalizeAgent(agent, agent.id || `agent-${index + 1}`));
      const active = stored.activeAgentId;
      const activeAgentId = agents.some((agent) => agent.id === active) ? active : agents[0].id;
      return { agents, activeAgentId };
    }

    const hasLegacyConfig = Boolean(
      stored.baseUrl || stored.token || stored.sessionKey || stored.channel || stored.target || stored.name
    );

    const legacy = normalizeAgent(stored, stored.id || 'agent-default');
    if (!hasLegacyConfig) {
      return {
        agents: [
          {
            id: 'agent-default',
            name: 'Default Agent',
            baseUrl: DEFAULT_GATEWAY_URL,
            token: '',
            sessionKey: DEFAULT_SESSION_KEY
          }
        ],
        activeAgentId: 'agent-default'
      };
    }

    return {
      agents: [legacy],
      activeAgentId: legacy.id
    };
  }

  function readSync(keys) {
    return new Promise((resolve) => {
      chrome.storage.sync.get(keys, (data) => resolve(data || {}));
    });
  }

  function writeSync(data) {
    return new Promise((resolve) => {
      chrome.storage.sync.set(data, () => resolve());
    });
  }

  function sendMessage(message) {
    return new Promise((resolve, reject) => {
      chrome.runtime.sendMessage(message, (resp) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message));
          return;
        }
        resolve(resp);
      });
    });
  }

  const root = document.createElement('div');
  root.id = 'oc-copilot-root';
  root.innerHTML = `
    <button id="oc-bubble" title="OpenClaw Copilot" aria-label="Open OpenClaw Copilot">
      <span class="oc-bubble-bot" aria-hidden="true">
        <svg class="oc-bubble-bot-svg" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M60 10 C30 10 15 35 15 55 C15 75 30 95 45 100 L45 110 L55 110 L55 100 C55 100 60 102 65 100 L65 110 L75 110 L75 100 C90 95 105 75 105 55 C105 35 90 10 60 10Z" fill="url(#oc-lobster-gradient)" class="claw-body"></path>
          <path d="M20 45 C5 40 0 50 5 60 C10 70 20 65 25 55 C28 48 25 45 20 45Z" fill="url(#oc-lobster-gradient)" class="claw-left"></path>
          <path d="M100 45 C115 40 120 50 115 60 C110 70 100 65 95 55 C92 48 95 45 100 45Z" fill="url(#oc-lobster-gradient)" class="claw-right"></path>
          <path d="M45 15 Q35 5 30 8" stroke="var(--coral-bright)" stroke-width="2" stroke-linecap="round" class="antenna"></path>
          <path d="M75 15 Q85 5 90 8" stroke="var(--coral-bright)" stroke-width="2" stroke-linecap="round" class="antenna"></path>
          <circle cx="45" cy="35" r="6" fill="var(--bg-deep)" class="eye"></circle>
          <circle cx="75" cy="35" r="6" fill="var(--bg-deep)" class="eye"></circle>
          <circle cx="46" cy="34" r="2" fill="var(--cyan-bright)" class="eye-glow"></circle>
          <circle cx="76" cy="34" r="2" fill="var(--cyan-bright)" class="eye-glow"></circle>
          <defs>
            <linearGradient id="oc-lobster-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="var(--logo-gradient-start)"></stop>
              <stop offset="100%" stop-color="var(--logo-gradient-end)"></stop>
            </linearGradient>
          </defs>
        </svg>
      </span>
    </button>

    <aside id="oc-panel" class="oc-hidden" aria-label="OpenClaw Copilot Panel">
      <div class="oc-panel-shell">
        <header class="oc-header">
          <div class="oc-title-wrap">
            <strong>ClawSide</strong>
          </div>
          <div class="oc-header-actions">
            <button id="oc-settings" class="oc-header-icon-btn" aria-label="Open settings" title="Settings">⚙</button>
            <button id="oc-new-session" class="oc-header-icon-btn" aria-label="Start new session" title="New Session">
              <svg class="oc-icon-svg" viewBox="0 0 24 24" aria-hidden="true">
                <rect x="4" y="7" width="12" height="12" rx="2.5"></rect>
                <path d="M14.5 6.5l3 3"></path>
                <path d="M12.2 16.2l1.1-3.5 5.3-5.3a1.3 1.3 0 0 0 0-1.8l-.2-.2a1.3 1.3 0 0 0-1.8 0l-5.3 5.3-3.5 1.1"></path>
              </svg>
            </button>
            <button id="oc-close" class="oc-header-icon-btn" aria-label="Close panel" title="Close">✕</button>
          </div>
        </header>

        <div class="oc-agent-row">
          <div class="oc-agent-tabs-wrap">
            <span>Agents</span>
            <div id="oc-agent-tabs" class="oc-agent-tabs" role="tablist" aria-label="OpenClaw agents"></div>
            <select id="oc-agent" class="oc-hidden-select" aria-hidden="true" tabindex="-1"></select>
          </div>
          <button id="oc-edit-agent" class="oc-agent-icon-btn" aria-label="Edit current agent" title="Edit Agent">✎</button>
          <button id="oc-add-agent" class="oc-agent-icon-btn" aria-label="Add agent" title="Add Agent">＋</button>
        </div>

        <section id="oc-layout-pane" class="oc-overlay-pane oc-hidden" aria-label="Layout settings">
          <div class="oc-pane-head">
            <strong>Layout Settings</strong>
            <button id="oc-layout-done" class="oc-ghost-btn oc-mini-btn">Done</button>
          </div>

          <label class="oc-field" for="oc-layout-mode">
            <span>Layout Mode</span>
            <select id="oc-layout-mode">
              <option value="push">Push (default)</option>
              <option value="overlay">Overlay</option>
            </select>
          </label>

          <label class="oc-field" for="oc-language">
            <span>Language</span>
            <select id="oc-language">
              <option value="auto">Auto (Chrome)</option>
              <option value="zh">中文</option>
              <option value="en">English</option>
            </select>
          </label>

          <label class="oc-field" for="oc-bubble-default-position">
            <span>Default Bubble Position</span>
            <select id="oc-bubble-default-position">
              <option value="bottom-right">Bottom Right</option>
              <option value="bottom-left">Bottom Left</option>
              <option value="top-right">Top Right</option>
              <option value="top-left">Top Left</option>
            </select>
          </label>

          <label class="oc-toggle oc-layout-toggle" for="oc-context">
            <input type="checkbox" id="oc-context" checked />
            <span>Context</span>
          </label>

          <div class="oc-shortcuts-settings">
            <div class="oc-shortcuts-title">Quick Shortcuts</div>

            <div class="oc-shortcut-item">
              <label class="oc-field" for="oc-shortcut-label-1">
                <span>Shortcut 1 Label</span>
                <input id="oc-shortcut-label-1" maxlength="20" />
              </label>
              <label class="oc-field" for="oc-shortcut-action-1">
                <span>Action</span>
                <select id="oc-shortcut-action-1">
                  <option value="chat">Chat</option>
                  <option value="summarize">Summarize</option>
                  <option value="save-kb">Save KB</option>
                  <option value="todo">Todo</option>
                </select>
              </label>
              <label class="oc-field" for="oc-shortcut-prompt-1">
                <span>Prompt</span>
                <textarea id="oc-shortcut-prompt-1" rows="2"></textarea>
              </label>
            </div>

            <div class="oc-shortcut-item">
              <label class="oc-field" for="oc-shortcut-label-2">
                <span>Shortcut 2 Label</span>
                <input id="oc-shortcut-label-2" maxlength="20" />
              </label>
              <label class="oc-field" for="oc-shortcut-action-2">
                <span>Action</span>
                <select id="oc-shortcut-action-2">
                  <option value="chat">Chat</option>
                  <option value="summarize">Summarize</option>
                  <option value="save-kb">Save KB</option>
                  <option value="todo">Todo</option>
                </select>
              </label>
              <label class="oc-field" for="oc-shortcut-prompt-2">
                <span>Prompt</span>
                <textarea id="oc-shortcut-prompt-2" rows="2"></textarea>
              </label>
            </div>

            <div class="oc-shortcut-item">
              <label class="oc-field" for="oc-shortcut-label-3">
                <span>Shortcut 3 Label</span>
                <input id="oc-shortcut-label-3" maxlength="20" />
              </label>
              <label class="oc-field" for="oc-shortcut-action-3">
                <span>Action</span>
                <select id="oc-shortcut-action-3">
                  <option value="chat">Chat</option>
                  <option value="summarize">Summarize</option>
                  <option value="save-kb">Save KB</option>
                  <option value="todo">Todo</option>
                </select>
              </label>
              <label class="oc-field" for="oc-shortcut-prompt-3">
                <span>Prompt</span>
                <textarea id="oc-shortcut-prompt-3" rows="2"></textarea>
              </label>
            </div>

            <div class="oc-shortcuts-actions">
              <button id="oc-shortcuts-save" class="oc-ghost-btn oc-primary">Save Shortcuts</button>
              <button id="oc-shortcuts-reset" class="oc-ghost-btn">Reset Defaults</button>
            </div>
          </div>

          <pre id="oc-layout-status" class="oc-pane-status"></pre>
        </section>

        <section id="oc-agent-pane" class="oc-overlay-pane oc-hidden" aria-label="Agent settings">
          <div class="oc-pane-head">
            <strong id="oc-agent-pane-title">Edit Agent</strong>
            <button id="oc-agent-done" class="oc-ghost-btn oc-mini-btn">Done</button>
          </div>

          <label class="oc-field" for="oc-set-name">
            <span>Agent Name</span>
            <input id="oc-set-name" />
          </label>

          <label class="oc-field" for="oc-set-baseurl">
            <span>Gateway URL</span>
            <input id="oc-set-baseurl" placeholder="ws://127.0.0.1:18789" />
          </label>

          <label class="oc-field" for="oc-set-token">
            <span>Token</span>
            <input id="oc-set-token" type="password" />
          </label>

          <div class="oc-pane-actions">
            <button id="oc-agent-save" class="oc-ghost-btn oc-primary">Save Agent</button>
            <button id="oc-agent-delete" class="oc-ghost-btn">Delete Agent</button>
            <button id="oc-agent-test" class="oc-ghost-btn">Test</button>
          </div>

          <button id="oc-open-options" class="oc-link-btn">Open Full Settings Page</button>
          <pre id="oc-agent-status" class="oc-pane-status"></pre>
        </section>

        <div id="oc-output" aria-live="polite"></div>

        <div class="oc-composer">
          <div id="oc-page-context-chip" class="oc-page-context-chip" aria-label="Current page context">
            <img id="oc-page-context-icon" class="oc-page-context-icon" alt="" referrerpolicy="no-referrer" />
            <span id="oc-page-context-text" class="oc-page-context-text">Current page</span>
          </div>
          <div id="oc-shortcuts-inline" class="oc-shortcuts-inline"></div>
          <div id="oc-attachment-row" class="oc-attachment-row is-empty">
            <img id="oc-attachment-preview" class="oc-attachment-preview" alt="" />
            <span id="oc-attachment-name" class="oc-attachment-name">Screenshot attached</span>
            <button
              id="oc-attachment-remove"
              class="oc-attachment-remove"
              type="button"
              aria-label="Remove attachment"
              title="Remove attachment"
            >✕</button>
          </div>
          <div class="oc-input-row">
            <button id="oc-shot-btn" class="oc-input-action-btn" type="button" aria-label="Capture screenshot" title="Capture screenshot">
              <svg class="oc-icon-svg" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 5v14"></path>
                <path d="M5 12h14"></path>
              </svg>
            </button>
            <input id="oc-image-file" class="oc-hidden-file-input" type="file" accept="image/*" />
            <textarea id="oc-input" placeholder="有问题，尽管问" rows="1"></textarea>
            <button id="oc-send-btn" class="oc-send-icon-btn" type="button" aria-label="Send">↑</button>
          </div>
        </div>
      </div>
    </aside>
  `;

  document.documentElement.appendChild(root);

  const bubble = root.querySelector('#oc-bubble');
  const panel = root.querySelector('#oc-panel');
  const closeBtn = root.querySelector('#oc-close');
  const settingsBtn = root.querySelector('#oc-settings');
  const newSessionBtn = root.querySelector('#oc-new-session');
  const editAgentBtn = root.querySelector('#oc-edit-agent');
  const addAgentBtn = root.querySelector('#oc-add-agent');

  const layoutPane = root.querySelector('#oc-layout-pane');
  const layoutDoneBtn = root.querySelector('#oc-layout-done');
  const layoutModeSelect = root.querySelector('#oc-layout-mode');
  const languageSelect = root.querySelector('#oc-language');
  const bubbleDefaultPositionSelect = root.querySelector('#oc-bubble-default-position');
  const layoutStatus = root.querySelector('#oc-layout-status');
  const shortcutLabelInputs = [
    root.querySelector('#oc-shortcut-label-1'),
    root.querySelector('#oc-shortcut-label-2'),
    root.querySelector('#oc-shortcut-label-3')
  ];
  const shortcutActionSelects = [
    root.querySelector('#oc-shortcut-action-1'),
    root.querySelector('#oc-shortcut-action-2'),
    root.querySelector('#oc-shortcut-action-3')
  ];
  const shortcutPromptInputs = [
    root.querySelector('#oc-shortcut-prompt-1'),
    root.querySelector('#oc-shortcut-prompt-2'),
    root.querySelector('#oc-shortcut-prompt-3')
  ];
  const shortcutsSaveBtn = root.querySelector('#oc-shortcuts-save');
  const shortcutsResetBtn = root.querySelector('#oc-shortcuts-reset');

  const agentPane = root.querySelector('#oc-agent-pane');
  const agentPaneTitle = root.querySelector('#oc-agent-pane-title');
  const agentDoneBtn = root.querySelector('#oc-agent-done');
  const agentSaveBtn = root.querySelector('#oc-agent-save');
  const agentDeleteBtn = root.querySelector('#oc-agent-delete');
  const agentTestBtn = root.querySelector('#oc-agent-test');
  const agentStatus = root.querySelector('#oc-agent-status');
  const openOptionsBtn = root.querySelector('#oc-open-options');

  const output = root.querySelector('#oc-output');
  const pageContextChip = root.querySelector('#oc-page-context-chip');
  const pageContextIcon = root.querySelector('#oc-page-context-icon');
  const pageContextText = root.querySelector('#oc-page-context-text');
  const shortcutsInline = root.querySelector('#oc-shortcuts-inline');
  const attachmentRow = root.querySelector('#oc-attachment-row');
  const attachmentPreview = root.querySelector('#oc-attachment-preview');
  const attachmentName = root.querySelector('#oc-attachment-name');
  const attachmentRemoveBtn = root.querySelector('#oc-attachment-remove');
  const screenshotBtn = root.querySelector('#oc-shot-btn');
  const imageFileInput = root.querySelector('#oc-image-file');
  const input = root.querySelector('#oc-input');
  const sendBtn = root.querySelector('#oc-send-btn');
  const contextToggle = root.querySelector('#oc-context');
  const agentTabs = root.querySelector('#oc-agent-tabs');
  const agentSelect = root.querySelector('#oc-agent');

  const settingsName = root.querySelector('#oc-set-name');
  const settingsBaseUrl = root.querySelector('#oc-set-baseurl');
  const settingsToken = root.querySelector('#oc-set-token');

  let layoutMode = DEFAULT_LAYOUT_MODE;
  let bubbleDefaultPosition = DEFAULT_BUBBLE_POSITION;
  let bubbleCustomPosition = null;
  let openclawState = ensureOpenClawState({});
  let agentPaneMode = 'edit';
  let agentDraftId = '';
  let timeline = [];
  let shortcutState = ensureShortcutState({});
  let pageContextSnapshot = null;
  let lastPageUrl = '';
  let lastPageTitle = '';
  let pendingScreenshot = null;
  let isCapturingScreenshot = false;
  let bubbleDragState = null;
  let bubbleSuppressClick = false;

  function languageChoiceLabel(preference = languagePreference) {
    const normalized = normalizeLanguagePreference(preference);
    if (normalized === 'zh') return t('languageChoiceZh');
    if (normalized === 'en') return t('languageChoiceEn');
    return t('languageChoiceAuto');
  }

  function layoutModeLabel(mode = layoutMode) {
    return mode === 'overlay' ? t('layoutModeOverlayName') : t('layoutModePushName');
  }

  function bubblePositionLabel(value = bubbleDefaultPosition) {
    if (value === 'bottom-left') return t('bubblePositionBottomLeft');
    if (value === 'top-right') return t('bubblePositionTopRight');
    if (value === 'top-left') return t('bubblePositionTopLeft');
    return t('bubblePositionBottomRight');
  }

  function buildUiSettingsPayload() {
    return {
      layoutMode,
      layoutModeVersion: LAYOUT_MODE_VERSION,
      languagePreference,
      bubbleDefaultPosition,
      bubbleCustomPosition: bubbleCustomPosition ? { ...bubbleCustomPosition } : null
    };
  }

  function applyLanguage(preference = languagePreference) {
    languagePreference = normalizeLanguagePreference(preference);
    activeLanguage = resolveLanguage(languagePreference);

    bubble.title = t('bubbleTitle');
    bubble.setAttribute('aria-label', t('bubbleAria'));
    panel.setAttribute('aria-label', t('panelAria'));

    const settingsTip = t('tooltipSettings');
    settingsBtn.dataset.tip = settingsTip;
    settingsBtn.title = '';
    settingsBtn.setAttribute('aria-label', settingsTip);

    const newSessionTip = t('tooltipNewSession');
    newSessionBtn.dataset.tip = newSessionTip;
    newSessionBtn.title = '';
    newSessionBtn.setAttribute('aria-label', newSessionTip);

    const closeTip = t('tooltipClose');
    closeBtn.dataset.tip = closeTip;
    closeBtn.title = '';
    closeBtn.setAttribute('aria-label', closeTip);

    const editAgentTip = t('tooltipEditAgent');
    editAgentBtn.dataset.tip = editAgentTip;
    editAgentBtn.title = '';
    editAgentBtn.setAttribute('aria-label', editAgentTip);

    const addAgentTip = t('tooltipAddAgent');
    addAgentBtn.dataset.tip = addAgentTip;
    addAgentBtn.title = '';
    addAgentBtn.setAttribute('aria-label', addAgentTip);

    const agentTitle = root.querySelector('.oc-agent-tabs-wrap > span');
    if (agentTitle) agentTitle.textContent = t('agents');

    const layoutHead = layoutPane.querySelector('.oc-pane-head strong');
    if (layoutHead) layoutHead.textContent = t('layoutSettings');
    layoutPane.setAttribute('aria-label', t('layoutSettings'));
    layoutDoneBtn.textContent = t('done');

    const layoutModeLabelEl = layoutModeSelect.closest('label')?.querySelector('span');
    if (layoutModeLabelEl) layoutModeLabelEl.textContent = t('layoutMode');
    const pushOption = layoutModeSelect.querySelector('option[value="push"]');
    const overlayOption = layoutModeSelect.querySelector('option[value="overlay"]');
    if (pushOption) pushOption.textContent = t('layoutModePushOption');
    if (overlayOption) overlayOption.textContent = t('layoutModeOverlayOption');

    const languageLabelEl = languageSelect.closest('label')?.querySelector('span');
    if (languageLabelEl) languageLabelEl.textContent = t('language');
    const languageAutoOption = languageSelect.querySelector('option[value="auto"]');
    const languageZhOption = languageSelect.querySelector('option[value="zh"]');
    const languageEnOption = languageSelect.querySelector('option[value="en"]');
    if (languageAutoOption) languageAutoOption.textContent = t('languageAuto');
    if (languageZhOption) languageZhOption.textContent = t('languageZh');
    if (languageEnOption) languageEnOption.textContent = t('languageEn');
    languageSelect.value = languagePreference;

    const bubblePositionLabelEl = bubbleDefaultPositionSelect.closest('label')?.querySelector('span');
    if (bubblePositionLabelEl) bubblePositionLabelEl.textContent = t('defaultBubblePosition');
    const bubblePosBottomRightOption = bubbleDefaultPositionSelect.querySelector('option[value="bottom-right"]');
    const bubblePosBottomLeftOption = bubbleDefaultPositionSelect.querySelector('option[value="bottom-left"]');
    const bubblePosTopRightOption = bubbleDefaultPositionSelect.querySelector('option[value="top-right"]');
    const bubblePosTopLeftOption = bubbleDefaultPositionSelect.querySelector('option[value="top-left"]');
    if (bubblePosBottomRightOption) bubblePosBottomRightOption.textContent = t('bubblePositionBottomRight');
    if (bubblePosBottomLeftOption) bubblePosBottomLeftOption.textContent = t('bubblePositionBottomLeft');
    if (bubblePosTopRightOption) bubblePosTopRightOption.textContent = t('bubblePositionTopRight');
    if (bubblePosTopLeftOption) bubblePosTopLeftOption.textContent = t('bubblePositionTopLeft');
    bubbleDefaultPositionSelect.value = bubbleDefaultPosition;

    const contextLabelEl = root.querySelector('label[for="oc-context"] span');
    if (contextLabelEl) contextLabelEl.textContent = t('context');

    const shortcutsTitleEl = layoutPane.querySelector('.oc-shortcuts-title');
    if (shortcutsTitleEl) shortcutsTitleEl.textContent = t('quickShortcuts');

    for (let i = 0; i < SHORTCUT_COUNT; i += 1) {
      const labelField = shortcutLabelInputs[i]?.closest('label')?.querySelector('span');
      const actionField = shortcutActionSelects[i]?.closest('label')?.querySelector('span');
      const promptField = shortcutPromptInputs[i]?.closest('label')?.querySelector('span');
      if (labelField) labelField.textContent = t('shortcutLabel', { index: i + 1 });
      if (actionField) actionField.textContent = t('action');
      if (promptField) promptField.textContent = t('prompt');

      const select = shortcutActionSelects[i];
      if (select) {
        const chatOption = select.querySelector('option[value="chat"]');
        const summarizeOption = select.querySelector('option[value="summarize"]');
        const saveKbOption = select.querySelector('option[value="save-kb"]');
        const todoOption = select.querySelector('option[value="todo"]');
        if (chatOption) chatOption.textContent = t('actionChat');
        if (summarizeOption) summarizeOption.textContent = t('actionSummarize');
        if (saveKbOption) saveKbOption.textContent = t('actionSaveKb');
        if (todoOption) todoOption.textContent = t('actionTodo');
      }
    }

    shortcutsSaveBtn.textContent = t('saveShortcuts');
    shortcutsResetBtn.textContent = t('resetDefaults');

    const agentHead = agentPane.querySelector('.oc-pane-head strong');
    if (agentHead && agentPaneMode === 'edit') agentHead.textContent = t('editAgentPane');
    if (agentHead && agentPaneMode === 'create') agentHead.textContent = t('addAgentPane');
    agentPane.setAttribute('aria-label', t('agentSettings'));
    agentDoneBtn.textContent = t('done');

    const agentNameLabel = settingsName.closest('label')?.querySelector('span');
    const baseUrlLabel = settingsBaseUrl.closest('label')?.querySelector('span');
    const tokenLabel = settingsToken.closest('label')?.querySelector('span');
    if (agentNameLabel) agentNameLabel.textContent = t('agentName');
    if (baseUrlLabel) baseUrlLabel.textContent = t('gatewayUrl');
    if (tokenLabel) tokenLabel.textContent = t('token');

    openOptionsBtn.textContent = t('openFullSettingsPage');
    agentDeleteBtn.textContent = t('deleteAgent');
    agentTestBtn.textContent = t('testConnection');
    if (agentPaneMode === 'create') {
      agentSaveBtn.textContent = t('createAgent');
      agentPaneTitle.textContent = t('addAgentPane');
    } else {
      agentSaveBtn.textContent = t('saveAgent');
      agentPaneTitle.textContent = t('editAgentPane');
    }

    input.placeholder = t('inputPlaceholder');
    sendBtn.setAttribute('aria-label', t('send'));
    const screenshotTip = t('captureScreenshot');
    screenshotBtn.dataset.tip = screenshotTip;
    screenshotBtn.title = '';
    screenshotBtn.setAttribute('aria-label', screenshotTip);
    const removeAttachmentTip = t('removeAttachment');
    attachmentRemoveBtn.dataset.tip = removeAttachmentTip;
    attachmentRemoveBtn.title = '';
    attachmentRemoveBtn.setAttribute('aria-label', removeAttachmentTip);
    attachmentName.textContent = t('screenshotAttached');
    pageContextChip.setAttribute('aria-label', t('pageContextAria'));

    renderAgentTabs();
    renderTimeline();
    renderPageContextChip();
    renderPendingScreenshot();
    applyBubblePosition();
  }

  function setLayoutStatus(message) {
    layoutStatus.textContent = message || '';
  }

  function setAgentStatus(message) {
    agentStatus.textContent = message || '';
  }

  function getActiveAgent(state = openclawState) {
    return state.agents.find((agent) => agent.id === state.activeAgentId) || state.agents[0] || null;
  }

  function activeHistoryAgentId() {
    return openclawState.activeAgentId || getActiveAgent()?.id || 'agent-default';
  }

  function historyStorageKey(agentId = activeHistoryAgentId()) {
    const path = `${location.origin}${location.pathname}`;
    return `${HISTORY_STORAGE_PREFIX}:${path}:${agentId}`;
  }

  function extractDeepText(payload, fallback = '') {
    const seen = new Set();

    const read = (value) => {
      if (typeof value === 'string') return value.trim();
      if (!value || typeof value !== 'object') return '';
      if (seen.has(value)) return '';
      seen.add(value);

      if (Array.isArray(value)) {
        for (const item of value) {
          const found = read(item);
          if (found) return found;
        }
        return '';
      }

      const directKeys = ['reply', 'summary', 'text', 'message', 'content', 'output', 'result', 'answer', 'error'];
      for (const key of directKeys) {
        if (Object.prototype.hasOwnProperty.call(value, key)) {
          const found = read(value[key]);
          if (found) return found;
        }
      }

      const nestedKeys = ['data', 'payload', 'response', 'raw'];
      for (const key of nestedKeys) {
        if (Object.prototype.hasOwnProperty.call(value, key)) {
          const found = read(value[key]);
          if (found) return found;
        }
      }

      return '';
    };

    return read(payload) || fallback;
  }

  function defaultPromptByAction(action) {
    if (action === 'summarize') return t('defaultPromptSummarize');
    if (action === 'save-kb') return t('defaultPromptSaveKb');
    if (action === 'todo') return t('defaultPromptTodo', { title: document.title });
    return t('defaultPromptChat');
  }

  function defaultReplyByAction(action) {
    if (action === 'save-kb') return t('defaultReplySaveKb');
    if (action === 'todo') return t('defaultReplyTodo');
    if (action === 'summarize') return t('defaultReplySummarize');
    return t('defaultReplyChat');
  }

  function extractReplyText(action, data) {
    if (action === 'chat' && typeof data?.reply === 'string' && data.reply.trim()) return data.reply.trim();
    if (action === 'summarize' && typeof data?.summary === 'string' && data.summary.trim()) return data.summary.trim();
    const deep = extractDeepText(data, '');
    return deep || defaultReplyByAction(action);
  }

  function normalizeTimelineEntry(raw) {
    if (!raw || typeof raw !== 'object') return null;
    const agentName = typeof raw.agentName === 'string' ? raw.agentName.trim() : '';
    const agentId = typeof raw.agentId === 'string' ? raw.agentId.trim() : '';

    if (typeof raw.role === 'string' && typeof raw.text === 'string') {
      return {
        id: String(raw.id || newTimelineId('msg')),
        ts: String(raw.ts || new Date().toISOString()),
        role: raw.role === 'user' || raw.role === 'assistant' || raw.role === 'system' ? raw.role : 'system',
        action: String(raw.action || 'chat'),
        text: raw.text,
        status: String(raw.status || ''),
        agentName,
        agentId
      };
    }

    if (raw.type === 'request') {
      const action = String(raw.action || 'chat');
      const payload = raw.payload || {};
      const text = action === 'todo' ?
        String(payload.task || '').trim() :
        String(payload.message || '').trim();

      return {
        id: String(raw.id || newTimelineId('msg')),
        ts: String(raw.ts || new Date().toISOString()),
        role: 'user',
        action,
        text: text || defaultPromptByAction(action),
        status: 'sent',
        agentName,
        agentId
      };
    }

    if (raw.type === 'response') {
      const action = String(raw.action || 'chat');
      const ok = raw.ok !== false;
      const text = ok ?
        extractReplyText(action, raw.data || {}) :
        String(raw.error || raw?.data?.error || t('requestFailed'));

      return {
        id: String(raw.id || newTimelineId('msg')),
        ts: String(raw.ts || new Date().toISOString()),
        role: ok ? 'assistant' : 'system',
        action,
        text,
        status: ok ? 'ok' : 'error',
        agentName,
        agentId
      };
    }

    return null;
  }

  function readTimeline(agentId = activeHistoryAgentId()) {
    try {
      const raw = sessionStorage.getItem(historyStorageKey(agentId));
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      return parsed.map((entry) => normalizeTimelineEntry(entry)).filter(Boolean);
    } catch (err) {
      console.warn('[ClawSide] readTimeline: corrupted storage data:', err?.message);
      return [];
    }
  }

  function persistTimeline() {
    try {
      sessionStorage.setItem(historyStorageKey(), JSON.stringify(timeline.slice(-MAX_TIMELINE_ITEMS)));
    } catch (err) {
      console.warn('[ClawSide] persistTimeline: storage write failed:', err?.message);
    }
  }

  function clearCurrentTimeline() {
    timeline = [];
    try {
      sessionStorage.removeItem(historyStorageKey());
    } catch (err) {
      console.warn('[ClawSide] clearCurrentTimeline: storage clear failed:', err?.message);
    }
    renderTimeline();
  }

  function timeLabel(ts) {
    const date = new Date(ts);
    if (Number.isNaN(date.getTime())) return '';
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  }

  function renderMessageContent(textEl, entry) {
    if (entry.role === 'assistant' && entry.text) {
      textEl.innerHTML = renderMarkdown(entry.text);
    } else {
      textEl.textContent = entry.text || '';
    }
  }

  function createMessageRow(entry) {
    const row = document.createElement('div');
    row.className = `oc-msg-row oc-msg-${entry.role}`;
    if (entry.status === 'streaming') {
      row.classList.add('oc-msg-streaming');
    }
    if (entry.id) row.setAttribute('data-msg-id', entry.id);

    const bubble = document.createElement('div');
    bubble.className = 'oc-msg-bubble';

    const meta = document.createElement('div');
    meta.className = 'oc-msg-meta';
    const roleLabel = entry.role === 'user'
      ? t('roleYou')
      : entry.role === 'assistant'
        ? (entry.agentName || 'OpenClaw')
        : t('roleSystem');
    const metaParts = [roleLabel, timeLabel(entry.ts)].filter(Boolean);
    meta.textContent = metaParts.join(' · ');

    const text = document.createElement('div');
    text.className = 'oc-msg-text';
    if (entry.status === 'streaming') {
      text.textContent = '';
      text.setAttribute('aria-label', t('streaming'));
    } else {
      renderMessageContent(text, entry);
    }

    bubble.append(meta, text);
    row.append(bubble);
    return row;
  }

  function renderTimeline() {
    output.innerHTML = '';

    if (!timeline.length) {
      const empty = document.createElement('div');
      empty.className = 'oc-chat-empty';
      empty.textContent = t('emptyChat');
      output.append(empty);
      return;
    }

    timeline.forEach((entry) => {
      output.append(createMessageRow(entry));
    });

    output.scrollTop = output.scrollHeight;
  }

  // Update a streaming message in-place without re-rendering the whole timeline
  function updateStreamingMessage(msgId, text) {
    const row = output.querySelector(`[data-msg-id="${msgId}"]`);
    if (!row) return;
    const textEl = row.querySelector('.oc-msg-text');
    if (!textEl) return;
    const nextText = String(text || '');
    if (!nextText) return;
    row.classList.remove('oc-msg-streaming');
    textEl.removeAttribute('aria-label');
    textEl.innerHTML = renderMarkdown(nextText);
    output.scrollTop = output.scrollHeight;
  }

  function loadTimeline(agentId = activeHistoryAgentId()) {
    timeline = readTimeline(agentId).slice(-MAX_TIMELINE_ITEMS);
    renderTimeline();
  }

  function newTimelineId(prefix = 'evt') {
    return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
  }

  function appendTimeline(entry) {
    const normalized = normalizeTimelineEntry(entry);
    if (!normalized) return normalized;

    // Remove empty-state placeholder if present
    const emptyEl = output.querySelector('.oc-chat-empty');
    if (emptyEl) emptyEl.remove();

    timeline.push(normalized);
    if (timeline.length > MAX_TIMELINE_ITEMS) {
      timeline = timeline.slice(-MAX_TIMELINE_ITEMS);
    }
    persistTimeline();

    // Append single row instead of full re-render
    output.append(createMessageRow(normalized));
    output.scrollTop = output.scrollHeight;
    return normalized;
  }

  // Update an existing timeline entry's text (for streaming finalization)
  function finalizeStreamingEntry(msgId, text) {
    const entry = timeline.find((e) => e.id === msgId);
    if (entry) {
      entry.text = text;
      entry.status = 'ok';
      persistTimeline();
    }
    const row = output.querySelector(`[data-msg-id="${msgId}"]`);
    if (row) row.classList.remove('oc-msg-streaming');
  }

  function fillShortcutSettingsForm() {
    const items = shortcutState.items || [];
    for (let i = 0; i < SHORTCUT_COUNT; i += 1) {
      const item = items[i] || normalizeShortcut({}, i);
      if (shortcutLabelInputs[i]) shortcutLabelInputs[i].value = item.label;
      if (shortcutActionSelects[i]) shortcutActionSelects[i].value = item.action;
      if (shortcutPromptInputs[i]) shortcutPromptInputs[i].value = item.prompt;
    }
  }

  function collectShortcutSettingsFromForm() {
    const items = [];
    for (let i = 0; i < SHORTCUT_COUNT; i += 1) {
      items.push(
        normalizeShortcut(
          {
            id: shortcutState.items?.[i]?.id,
            label: shortcutLabelInputs[i]?.value,
            action: shortcutActionSelects[i]?.value,
            prompt: shortcutPromptInputs[i]?.value
          },
          i
        )
      );
    }
    return { items };
  }

  function renderShortcutButtons() {
    const items = shortcutState.items || [];
    shortcutsInline.innerHTML = '';
    items.forEach((item, index) => {
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'oc-shortcut-chip';
      btn.textContent = item.label;
      btn.title = item.prompt;
      btn.setAttribute('data-shortcut-index', String(index));
      btn.setAttribute('data-shortcut-action', item.action);
      shortcutsInline.append(btn);
    });
  }

  function applyShortcutState(state) {
    shortcutState = ensureShortcutState(state);
    renderShortcutButtons();
    fillShortcutSettingsForm();
  }

  async function saveShortcutSettings() {
    const next = collectShortcutSettingsFromForm();
    await writeSync({ [SHORTCUTS_STORAGE_KEY]: next });
    applyShortcutState(next);
    setLayoutStatus(t('shortcutsSaved'));
  }

  async function resetShortcutSettings() {
    const next = ensureShortcutState({});
    await writeSync({ [SHORTCUTS_STORAGE_KEY]: next });
    applyShortcutState(next);
    setLayoutStatus(t('shortcutsReset'));
  }

  function getShortcut(index) {
    return shortcutState.items?.[index] || normalizeShortcut({}, index);
  }

  function applyAgentPaneMode(mode) {
    agentPaneMode = mode === 'create' ? 'create' : 'edit';

    if (agentPaneMode === 'create') {
      agentPaneTitle.textContent = t('addAgentPane');
      agentSaveBtn.textContent = t('createAgent');
      agentDeleteBtn.style.display = 'none';
    } else {
      agentPaneTitle.textContent = t('editAgentPane');
      agentSaveBtn.textContent = t('saveAgent');
      agentDeleteBtn.style.display = '';
    }
    agentDeleteBtn.textContent = t('deleteAgent');
    agentTestBtn.textContent = t('testConnection');
  }

  function fillAgentForm(agent) {
    if (!agent) return;
    settingsName.value = agent.name || '';
    settingsBaseUrl.value = agent.baseUrl || '';
    settingsToken.value = agent.token || '';
  }

  function renderAgentTabs() {
    agentTabs.innerHTML = '';
    const agents = openclawState.agents || [];

    if (!agents.length) {
      const empty = document.createElement('span');
      empty.className = 'oc-agent-tab-empty';
      empty.textContent = t('noAgent');
      agentTabs.append(empty);
      return;
    }

    agents.forEach((agent) => {
      const tab = document.createElement('button');
      tab.type = 'button';
      tab.className = 'oc-agent-tab';
      tab.setAttribute('role', 'tab');
      tab.setAttribute('data-agent-id', agent.id);
      tab.setAttribute('aria-selected', agent.id === openclawState.activeAgentId ? 'true' : 'false');
      tab.title = agent.name || 'OpenClaw Agent';

      if (agent.id === openclawState.activeAgentId) {
        tab.classList.add('is-active');
      }

      const label = document.createElement('span');
      label.className = 'oc-agent-tab-text';
      label.textContent = agent.name || 'OpenClaw Agent';
      tab.append(label);
      agentTabs.append(tab);
    });
  }

  function collectAgentForm() {
    const active = getActiveAgent();
    const id = agentPaneMode === 'create' ? (agentDraftId || newAgentId()) : (active?.id || agentDraftId || newAgentId());
    const existing = openclawState.agents.find((agent) => agent.id === id);
    const preservedSessionKey = agentPaneMode === 'create'
      ? DEFAULT_SESSION_KEY
      : (existing?.sessionKey || active?.sessionKey || DEFAULT_SESSION_KEY);
    return normalizeAgent(
      {
        id,
        name: settingsName.value,
        baseUrl: settingsBaseUrl.value,
        token: settingsToken.value,
        sessionKey: preservedSessionKey
      },
      id
    );
  }

  function applyAgentState(state) {
    openclawState = ensureOpenClawState(state);
    const agents = openclawState.agents;

    agentSelect.innerHTML = '';

    if (!agents.length) {
      const option = document.createElement('option');
      option.value = '';
      option.textContent = t('noAgentConfigured');
      option.disabled = true;
      option.selected = true;
      agentSelect.append(option);
      agentSelect.disabled = true;
      renderAgentTabs();
      loadTimeline('agent-default');
      return;
    }

    agents.forEach((agent) => {
      const option = document.createElement('option');
      option.value = agent.id;
      option.textContent = agent.name || 'OpenClaw Agent';
      option.selected = agent.id === openclawState.activeAgentId;
      agentSelect.append(option);
    });

    agentSelect.disabled = false;

    if (!agents.some((agent) => agent.id === openclawState.activeAgentId)) {
      openclawState.activeAgentId = agents[0].id;
      agentSelect.value = agents[0].id;
    }

    agentSelect.value = openclawState.activeAgentId;
    renderAgentTabs();
    fillAgentForm(getActiveAgent());
    loadTimeline(openclawState.activeAgentId);
  }

  function closeLayoutPane() {
    layoutPane.classList.add('oc-hidden');
    root.classList.remove('oc-pane-open');
  }

  function closeAgentPane() {
    agentPane.classList.add('oc-hidden');
    root.classList.remove('oc-pane-open');
  }

  function closeAllPanes() {
    layoutPane.classList.add('oc-hidden');
    agentPane.classList.add('oc-hidden');
    root.classList.remove('oc-pane-open');
  }

  function openLayoutPane() {
    closeAgentPane();
    layoutPane.classList.remove('oc-hidden');
    root.classList.add('oc-pane-open');
    layoutModeSelect.value = layoutMode;
  }

  function openAgentPane(mode = 'edit') {
    closeLayoutPane();

    if (mode === 'create') {
      applyAgentPaneMode('create');
      agentDraftId = newAgentId();
      fillAgentForm(
        normalizeAgent(
          {
            id: agentDraftId,
            name: t('agentNameTemplate', { index: openclawState.agents.length + 1 }),
            baseUrl: DEFAULT_GATEWAY_URL,
            token: '',
            sessionKey: DEFAULT_SESSION_KEY
          },
          agentDraftId
        )
      );
      setAgentStatus(t('fillAndCreate'));
    } else {
      applyAgentPaneMode('edit');
      agentDraftId = '';
      fillAgentForm(getActiveAgent());
      setAgentStatus('');
    }

    agentPane.classList.remove('oc-hidden');
    root.classList.add('oc-pane-open');
  }

  function getBubbleSize() {
    const rect = bubble.getBoundingClientRect();
    const fallback = window.innerWidth <= 760 ? 46 : 52;
    return {
      width: rect.width || fallback,
      height: rect.height || fallback
    };
  }

  function clampBubblePosition(rawPosition) {
    const pos = rawPosition || { x: 0, y: 0 };
    const { width, height } = getBubbleSize();
    const maxX = Math.max(0, window.innerWidth - width);
    const maxY = Math.max(0, window.innerHeight - height);
    return {
      x: Math.min(maxX, Math.max(0, Number(pos.x) || 0)),
      y: Math.min(maxY, Math.max(0, Number(pos.y) || 0))
    };
  }

  function getDefaultBubblePosition(position = bubbleDefaultPosition) {
    const { width, height } = getBubbleSize();
    const margin = window.innerWidth <= 760 ? 16 : 24;
    const maxX = Math.max(0, window.innerWidth - width);
    const maxY = Math.max(0, window.innerHeight - height);

    if (position === 'bottom-left') return { x: margin, y: maxY - margin };
    if (position === 'top-right') return { x: maxX - margin, y: margin };
    if (position === 'top-left') return { x: margin, y: margin };
    return { x: maxX - margin, y: maxY - margin };
  }

  function applyBubblePosition() {
    const target = bubbleCustomPosition || getDefaultBubblePosition();
    const clamped = clampBubblePosition(target);
    bubble.style.left = `${clamped.x}px`;
    bubble.style.top = `${clamped.y}px`;
    bubble.style.right = 'auto';
    bubble.style.bottom = 'auto';
  }

  async function persistBubblePositionState(showStatus = false) {
    await writeSync({
      clawsideUi: buildUiSettingsPayload()
    });
    if (showStatus) {
      setLayoutStatus(t('bubblePositionSaved'));
    }
  }

  async function applyDefaultBubblePosition(position) {
    bubbleDefaultPosition = normalizeBubbleDefaultPosition(position);
    bubbleCustomPosition = null;
    bubbleDefaultPositionSelect.value = bubbleDefaultPosition;
    applyBubblePosition();
    await writeSync({
      clawsideUi: buildUiSettingsPayload()
    });
    setLayoutStatus(t('bubblePositionDefaultApplied'));
  }

  function startBubbleDrag(event) {
    if (event.button !== 0) return;

    const rect = bubble.getBoundingClientRect();
    bubbleDragState = {
      pointerId: event.pointerId,
      originClientX: event.clientX,
      originClientY: event.clientY,
      originX: rect.left,
      originY: rect.top,
      moved: false
    };

    try {
      bubble.setPointerCapture(event.pointerId);
    } catch (err) {
      console.warn('[ClawSide] bubble pointer capture failed:', err?.message);
    }
  }

  function moveBubbleDrag(event) {
    if (!bubbleDragState || event.pointerId !== bubbleDragState.pointerId) return;

    const deltaX = event.clientX - bubbleDragState.originClientX;
    const deltaY = event.clientY - bubbleDragState.originClientY;
    if (!bubbleDragState.moved && (Math.abs(deltaX) > 2 || Math.abs(deltaY) > 2)) {
      bubbleDragState.moved = true;
    }

    const next = clampBubblePosition({
      x: bubbleDragState.originX + deltaX,
      y: bubbleDragState.originY + deltaY
    });
    bubble.style.left = `${next.x}px`;
    bubble.style.top = `${next.y}px`;
    bubble.style.right = 'auto';
    bubble.style.bottom = 'auto';
  }

  async function endBubbleDrag(event) {
    if (!bubbleDragState || event.pointerId !== bubbleDragState.pointerId) return;

    const wasMoved = bubbleDragState.moved;
    bubbleDragState = null;

    try {
      bubble.releasePointerCapture(event.pointerId);
    } catch (err) {
      console.warn('[ClawSide] bubble pointer release failed:', err?.message);
    }

    if (!wasMoved) return;

    const rect = bubble.getBoundingClientRect();
    bubbleCustomPosition = clampBubblePosition({ x: rect.left, y: rect.top });
    bubbleSuppressClick = true;
    await persistBubblePositionState();
    window.setTimeout(() => {
      bubbleSuppressClick = false;
    }, 0);
  }

  const syncPageShift = () => {
    const isDesktop = window.innerWidth > 760;
    const isOpen = !panel.classList.contains('oc-hidden');
    const shift = layoutMode === 'push' && isDesktop && isOpen ? Math.ceil(panel.getBoundingClientRect().width) : 0;
    const html = document.documentElement;
    const body = document.body;

    html.style.setProperty('--oc-layout-shift', `${shift}px`);
    if (body) body.style.setProperty('--oc-layout-shift', `${shift}px`);
    html.classList.toggle('oc-clawside-page-shift', shift > 0);
    if (body) body.classList.toggle('oc-clawside-page-shift', shift > 0);
  };

  const openPanel = () => {
    panel.classList.remove('oc-hidden');
    root.classList.add('oc-open');
    requestAnimationFrame(syncPageShift);
  };

  const closePanel = () => {
    panel.classList.add('oc-hidden');
    root.classList.remove('oc-open');
    closeAllPanes();
    syncPageShift();
  };

  async function saveLayoutMode(mode) {
    layoutMode = normalizeLayoutMode(mode);
    layoutModeSelect.value = layoutMode;

    await writeSync({ clawsideUi: buildUiSettingsPayload() });

    syncPageShift();
    setLayoutStatus(t('layoutSaved', { mode: layoutModeLabel(layoutMode) }));
  }

  async function saveLanguagePreference(preference) {
    applyLanguage(preference);
    await relocalizeBuiltinShortcutsIfNeeded();
    await writeSync({ clawsideUi: buildUiSettingsPayload() });
    setLayoutStatus(t('languageSaved', { language: languageChoiceLabel(languagePreference) }));
  }

  async function persistOpenClawState(nextState) {
    const normalized = ensureOpenClawState(nextState);
    await writeSync({ openclaw: normalized });
    applyAgentState(normalized);

    try {
      await sendMessage({ type: 'copilot:setActiveOpenClawInstance', agentId: normalized.activeAgentId });
    } catch (err) {
      console.warn('[ClawSide] background sync for active agent failed:', err?.message);
    }
  }

  async function startNewSession() {
    const active = getActiveAgent();
    if (!active?.id) {
      setAgentStatus(t('newSessionFailed', { error: t('noAgentConfigured') }));
      return;
    }

    syncPageContext(true);

    let resp;
    try {
      resp = await sendMessage({ type: 'copilot:newSession', agentId: active.id });
    } catch (error) {
      setAgentStatus(t('newSessionFailed', { error: String(error?.message || error) }));
      return;
    }

    if (!resp?.ok) {
      const detail = resp?.data?.error || t('requestFailed');
      setAgentStatus(t('newSessionFailed', { error: detail }));
      return;
    }

    if (resp.data?.state) {
      applyAgentState(resp.data.state);
    } else {
      await persistOpenClawState({
        ...openclawState,
        activeAgentId: active.id
      });
    }

    clearCurrentTimeline();
    input.value = '';
    syncPageContext(true);
    setAgentStatus(t('newSessionStarted'));
  }

  async function saveCurrentAgent() {
    const payload = collectAgentForm();
    const existing = openclawState.agents.some((agent) => agent.id === payload.id);

    const nextAgents = existing ?
      openclawState.agents.map((agent) => (agent.id === payload.id ? payload : agent)) :
      [...openclawState.agents, payload];

    await persistOpenClawState({
      agents: nextAgents,
      activeAgentId: payload.id
    });

    if (agentPaneMode === 'create') {
      applyAgentPaneMode('edit');
      agentDraftId = '';
      fillAgentForm(getActiveAgent());
      setAgentStatus(t('agentCreatedSelected'));
      return;
    }

    setAgentStatus(t('agentSaved'));
  }

  async function deleteCurrentAgent() {
    if (openclawState.agents.length <= 1) {
      setAgentStatus(t('needOneAgent'));
      return;
    }

    const active = getActiveAgent();
    const nextAgents = openclawState.agents.filter((agent) => agent.id !== active.id);
    const nextActive = nextAgents[0]?.id;

    await persistOpenClawState({
      agents: nextAgents,
      activeAgentId: nextActive
    });

    setAgentStatus(t('agentDeleted'));
  }

  async function testCurrentAgent() {
    const payload = collectAgentForm();
    setAgentStatus(t('testing'));

    let resp;
    try {
      resp = await sendMessage({ type: 'copilot:testConnection', agent: payload });
    } catch (error) {
      setAgentStatus(t('testFailed', { error: String(error.message || error) }));
      return;
    }

    if (!resp?.ok) {
      const detail = resp?.data?.error || JSON.stringify(resp?.data || {});
      setAgentStatus(t('testFailedWithCode', { status: resp?.status || 0, detail }));
      return;
    }

    setAgentStatus(t('connectionOk', { status: resp.status, message: resp.data?.message || t('ready') }));
  }

  async function openAdvancedSettingsPage() {
    try {
      const resp = await sendMessage({ type: 'copilot:openOptions' });
      if (resp?.ok) return;
    } catch (err) {
      console.warn('[ClawSide] openOptions via background failed, trying fallback:', err?.message);
    }

    try {
      window.open(chrome.runtime.getURL('options.html'), '_blank', 'noopener');
    } catch (err) {
      console.warn('[ClawSide] fallback openOptions also failed:', err?.message);
      setAgentStatus(t('cannotOpenSettings'));
    }
  }

  bubble.addEventListener('pointerdown', (event) => {
    startBubbleDrag(event);
  });

  bubble.addEventListener('pointermove', (event) => {
    moveBubbleDrag(event);
  });

  bubble.addEventListener('pointerup', (event) => {
    endBubbleDrag(event);
  });

  bubble.addEventListener('pointercancel', (event) => {
    endBubbleDrag(event);
  });

  bubble.addEventListener('click', (event) => {
    if (bubbleSuppressClick) {
      event.preventDefault();
      return;
    }

    if (panel.classList.contains('oc-hidden')) {
      openPanel();
      return;
    }
    closePanel();
  });

  closeBtn.addEventListener('click', closePanel);

  settingsBtn.addEventListener('click', () => {
    if (layoutPane.classList.contains('oc-hidden')) {
      openLayoutPane();
      return;
    }
    closeLayoutPane();
  });

  newSessionBtn.addEventListener('click', () => {
    startNewSession();
  });

  editAgentBtn.addEventListener('click', () => {
    openAgentPane('edit');
  });

  addAgentBtn.addEventListener('click', () => {
    openAgentPane('create');
  });

  agentTabs.addEventListener('click', async (event) => {
    const target = event.target instanceof Element ? event.target.closest('button[data-agent-id]') : null;
    if (!target) return;

    const nextId = target.getAttribute('data-agent-id');
    if (!nextId || nextId === openclawState.activeAgentId) return;

    await persistOpenClawState({
      ...openclawState,
      activeAgentId: nextId
    });

    if (!agentPane.classList.contains('oc-hidden') && agentPaneMode === 'edit') {
      fillAgentForm(getActiveAgent());
    }

    setAgentStatus(`Switched to ${getActiveAgent()?.name || 'agent'}.`);
  });

  layoutDoneBtn.addEventListener('click', closeLayoutPane);
  agentDoneBtn.addEventListener('click', closeAgentPane);

  agentSaveBtn.addEventListener('click', () => saveCurrentAgent());
  agentDeleteBtn.addEventListener('click', () => deleteCurrentAgent());
  agentTestBtn.addEventListener('click', () => testCurrentAgent());
  openOptionsBtn.addEventListener('click', () => openAdvancedSettingsPage());

  layoutModeSelect.addEventListener('change', () => {
    saveLayoutMode(layoutModeSelect.value);
  });

  languageSelect.addEventListener('change', () => {
    saveLanguagePreference(languageSelect.value);
  });

  bubbleDefaultPositionSelect.addEventListener('change', () => {
    applyDefaultBubblePosition(bubbleDefaultPositionSelect.value);
  });

  shortcutsSaveBtn.addEventListener('click', () => {
    saveShortcutSettings();
  });

  shortcutsResetBtn.addEventListener('click', () => {
    resetShortcutSettings();
  });

  document.addEventListener('keydown', (event) => {
    if (event.key !== 'Escape') return;

    if (!layoutPane.classList.contains('oc-hidden')) {
      closeLayoutPane();
      return;
    }

    if (!agentPane.classList.contains('oc-hidden')) {
      closeAgentPane();
      return;
    }

    if (!panel.classList.contains('oc-hidden')) {
      closePanel();
    }
  });

  window.addEventListener('resize', () => {
    syncPageShift();
    applyBubblePosition();
  });

  pageContextIcon.addEventListener('error', () => {
    pageContextIcon.style.display = 'none';
  });

  const onPageMaybeChanged = () => {
    syncPageContext(false);
  };

  const originalPushState = history.pushState;
  history.pushState = function pushStatePatched(...args) {
    const ret = originalPushState.apply(this, args);
    queueMicrotask(onPageMaybeChanged);
    return ret;
  };

  const originalReplaceState = history.replaceState;
  history.replaceState = function replaceStatePatched(...args) {
    const ret = originalReplaceState.apply(this, args);
    queueMicrotask(onPageMaybeChanged);
    return ret;
  };

  window.addEventListener('popstate', onPageMaybeChanged);
  window.setInterval(onPageMaybeChanged, 1200);

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== 'sync') return;

    if (changes.clawsideUi?.newValue) {
      layoutMode = normalizeLayoutMode(changes.clawsideUi.newValue.layoutMode);
      bubbleDefaultPosition = normalizeBubbleDefaultPosition(changes.clawsideUi.newValue.bubbleDefaultPosition);
      bubbleCustomPosition = normalizeBubbleCustomPosition(changes.clawsideUi.newValue.bubbleCustomPosition);
      layoutModeSelect.value = layoutMode;
      bubbleDefaultPositionSelect.value = bubbleDefaultPosition;
      applyLanguage(changes.clawsideUi.newValue.languagePreference);
    }

    if (changes.openclaw?.newValue) {
      applyAgentState(changes.openclaw.newValue);
    }

    if (changes[SHORTCUTS_STORAGE_KEY]?.newValue) {
      applyShortcutState(changes[SHORTCUTS_STORAGE_KEY].newValue);
    }

    syncPageShift();
  });

  chrome.runtime.sendMessage({ type: 'copilot:getPrivacy', url: location.href }, (p) => {
    if (p && typeof p.enabled === 'boolean') contextToggle.checked = p.enabled;
  });

  contextToggle.addEventListener('change', () => {
    chrome.runtime.sendMessage({ type: 'copilot:setSiteEnabled', url: location.href, enabled: contextToggle.checked });
  });

  // ── Handle messages from background (context menu & keyboard shortcut) ──
  chrome.runtime.onMessage.addListener((msg) => {
    if (msg?.type === 'copilot:toggleSidebar') {
      if (panel.classList.contains('oc-hidden')) {
        openPanel();
      } else {
        closePanel();
      }
      return;
    }

    if (msg?.type === 'copilot:contextMenu') {
      const selectedText = String(msg.text || '').trim();
      if (!selectedText) return;

      // Open sidebar if closed
      if (panel.classList.contains('oc-hidden')) {
        openPanel();
      }
      // Close any open panes
      closeAllPanes();

      let prompt;
      if (msg.action === 'clawside-translate') {
        prompt = t('contextTranslate', { text: selectedText });
      } else if (msg.action === 'clawside-explain') {
        prompt = t('contextExplain', { text: selectedText });
      } else {
        prompt = t('contextAsk', { text: selectedText });
      }

      dispatchAction('chat', prompt, prompt);
    }
  });

  agentSelect.addEventListener('change', async () => {
    const nextId = agentSelect.value;
    if (!nextId) return;

    await persistOpenClawState({
      ...openclawState,
      activeAgentId: nextId
    });

    if (!agentPane.classList.contains('oc-hidden') && agentPaneMode === 'edit') {
      fillAgentForm(getActiveAgent());
    }

    setAgentStatus(t('switchedTo', { name: getActiveAgent()?.name || 'agent' }));
  });

  function safeTextFromPage() {
    const article = document.querySelector('article, main, [role="main"]');
    const text = (article?.innerText || document.body.innerText || '').replace(/\s+/g, ' ').trim();
    return text.slice(0, 2400);
  }

  function pageDescriptionFromDom() {
    const meta = document.querySelector('meta[name="description"], meta[property="og:description"]');
    const metaContent = String(meta?.getAttribute('content') || '').replace(/\s+/g, ' ').trim();
    if (metaContent) return metaContent.slice(0, 320);

    const snippet = safeTextFromPage();
    if (!snippet) return '';
    const firstSentence = snippet.split(/[。！？.!?]/).map((part) => part.trim()).find(Boolean) || snippet;
    return firstSentence.slice(0, 320);
  }

  function collectContext() {
    const sel = String(window.getSelection() || '').slice(0, 800);
    return {
      url: location.href,
      title: document.title,
      contentDescription: pageDescriptionFromDom(),
      selection: sel,
      contentSnippet: safeTextFromPage()
    };
  }

  function truncateText(text, max = 42) {
    const value = String(text || '').trim();
    if (!value) return '';
    return value.length > max ? `${value.slice(0, max - 1)}…` : value;
  }

  function extractHost(url) {
    try {
      return new URL(String(url || location.href)).hostname.replace(/^www\./i, '');
    } catch {
      return '';
    }
  }

  function resolvePageFaviconUrl() {
    const iconEl = document.querySelector('link[rel~="icon"], link[rel="shortcut icon"], link[rel="apple-touch-icon"]');
    const raw = iconEl?.getAttribute('href');
    if (raw) {
      try {
        return new URL(raw, location.href).toString();
      } catch {
        // ignore
      }
    }
    try {
      return new URL('/favicon.ico', location.origin).toString();
    } catch {
      return '';
    }
  }

  function renderPageContextChip() {
    const snapshot = pageContextSnapshot || collectContext();
    const host = extractHost(snapshot.url);
    const title = String(snapshot.title || '').trim();
    const description = String(snapshot.contentDescription || '').trim();
    const label = [truncateText(title, 36), host].filter(Boolean).join(' / ') || t('pageContextDefault');
    pageContextText.textContent = label;
    pageContextChip.setAttribute('aria-label', t('pageContextAria'));
    pageContextChip.title = [title, host, description].filter(Boolean).join('\n') || t('pageContextDefault');

    const faviconUrl = resolvePageFaviconUrl();
    if (faviconUrl) {
      pageContextIcon.src = faviconUrl;
      pageContextIcon.style.display = '';
    } else {
      pageContextIcon.style.display = 'none';
    }
  }

  function syncPageContext(force = false) {
    const nextUrl = location.href;
    const nextTitle = document.title;
    if (!force && nextUrl === lastPageUrl && nextTitle === lastPageTitle) return;
    lastPageUrl = nextUrl;
    lastPageTitle = nextTitle;
    pageContextSnapshot = collectContext();
    renderPageContextChip();
  }

  function renderPendingScreenshot() {
    const hasScreenshot = Boolean(pendingScreenshot?.dataUrl);
    attachmentRow.classList.toggle('is-empty', !hasScreenshot);

    if (!hasScreenshot) {
      attachmentPreview.removeAttribute('src');
      attachmentName.textContent = t('screenshotAttached');
      return;
    }

    attachmentPreview.src = pendingScreenshot.dataUrl;
    attachmentName.textContent = pendingScreenshot.name || t('screenshotAttached');
  }

  function setPendingScreenshot(screenshot) {
    if (!screenshot?.dataUrl) {
      pendingScreenshot = null;
      renderPendingScreenshot();
      return;
    }

    pendingScreenshot = {
      dataUrl: String(screenshot.dataUrl),
      mimeType: String(screenshot.mimeType || 'image/jpeg'),
      name: String(screenshot.name || '').trim()
    };
    renderPendingScreenshot();
  }

  function clearPendingScreenshot() {
    pendingScreenshot = null;
    renderPendingScreenshot();
  }

  function consumePendingScreenshot() {
    const snapshot = pendingScreenshot ? { ...pendingScreenshot } : null;
    clearPendingScreenshot();
    return snapshot;
  }

  async function attachImageFile(file) {
    if (!file) return;
    if (isCapturingScreenshot) return;

    isCapturingScreenshot = true;
    screenshotBtn.disabled = true;
    screenshotBtn.classList.add('is-loading');

    try {
      if (!String(file.type || '').toLowerCase().startsWith('image/')) {
        throw new Error('Only image files are supported.');
      }

      const dataUrl = await new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ''));
        reader.onerror = () => reject(new Error('Read image failed.'));
        reader.readAsDataURL(file);
      });
      if (!dataUrl || !dataUrl.startsWith('data:image/')) {
        throw new Error('Invalid image data.');
      }

      setPendingScreenshot({
        dataUrl,
        mimeType: file.type || 'image/jpeg',
        name: file.name || ''
      });
    } catch (error) {
      appendTimeline({
        id: newTimelineId('res'),
        ts: new Date().toISOString(),
        role: 'system',
        action: 'chat',
        text: t('screenshotAttachFailed', { error: String(error?.message || error) }),
        status: 'error'
      });
    } finally {
      isCapturingScreenshot = false;
      screenshotBtn.disabled = false;
      screenshotBtn.classList.remove('is-loading');
      input.focus();
    }
  }

  function openImagePicker() {
    if (isCapturingScreenshot || !imageFileInput) return;
    imageFileInput.value = '';
    imageFileInput.click();
  }

  function dispatchAction(action, messageText, timelineText = '', options = {}) {
    const requestId = newTimelineId('req');
    syncPageContext(true);
    const context = pageContextSnapshot || collectContext();
    const rawInput = String(messageText || '').trim();
    const screenshot = options?.screenshot?.dataUrl ? options.screenshot : null;
    const hasScreenshot = Boolean(screenshot);
    const activeAgent = getActiveAgent();
    const activeAgentName = activeAgent?.name || 'OpenClaw';
    const activeAgentId = activeAgent?.id || '';

    if (action === 'todo') {
      const todoTask = rawInput || `Review: ${document.title}`;
      const todoTimelineText = hasScreenshot
        ? `${timelineText || todoTask}\n${t('screenshotAttached')}`
        : (timelineText || todoTask);
      appendTimeline({
        id: requestId,
        ts: new Date().toISOString(),
        role: 'user',
        action: 'todo',
        text: todoTimelineText,
        status: 'sent',
        agentName: activeAgentName,
        agentId: activeAgentId
      });

      chrome.runtime.sendMessage(
        {
          type: 'copilot:todo',
          task: todoTask,
          source: location.href,
          agentId: agentSelect.value,
          screenshot
        },
        (resp) => {
          if (!resp) {
            appendTimeline({
              id: newTimelineId('res'),
              ts: new Date().toISOString(),
              role: 'system',
              action: 'todo',
              text: t('noResponse'),
              status: 'error'
            });
            return;
          }
          if (!resp.ok) {
            appendTimeline({
              id: newTimelineId('res'),
              ts: new Date().toISOString(),
              role: 'system',
              action: 'todo',
              text: String(resp.data?.error || t('requestFailed')),
              status: 'error'
            });
            return;
          }
          appendTimeline({
            id: newTimelineId('res'),
            ts: new Date().toISOString(),
            role: 'assistant',
            action: 'todo',
            text: extractReplyText('todo', resp.data || {}),
            status: 'ok',
            agentName: activeAgentName,
            agentId: activeAgentId
          });
        }
      );
      return;
    }

    // ── Streaming path for chat / summarize / save-kb ──
    const promptText = rawInput || (hasScreenshot && action === 'chat'
      ? t('screenshotPromptAnalyze')
      : defaultPromptByAction(action));
    const userTimelineText = hasScreenshot
      ? `${timelineText || promptText}\n${t('screenshotAttached')}`
      : (timelineText || promptText);
    appendTimeline({
      id: requestId,
      ts: new Date().toISOString(),
      role: 'user',
      action,
      text: userTimelineText,
      status: 'sent',
      agentName: activeAgentName,
      agentId: activeAgentId
    });

    // Create a placeholder assistant message for streaming
    const streamMsgId = newTimelineId('res');
    const streamEntry = appendTimeline({
      id: streamMsgId,
      ts: new Date().toISOString(),
      role: 'assistant',
      action,
      text: '',
      status: 'streaming',
      agentName: activeAgentName,
      agentId: activeAgentId
    });

    const port = chrome.runtime.connect({ name: 'copilot:stream' });

    port.onMessage.addListener((msg) => {
      if (msg.type === 'stream:delta') {
        updateStreamingMessage(streamMsgId, msg.text);
        // Also keep timeline entry in sync
        if (streamEntry) streamEntry.text = msg.text;
      }

      if (msg.type === 'stream:done') {
        const finalText = extractReplyText(action, msg.data || {});
        updateStreamingMessage(streamMsgId, finalText);
        finalizeStreamingEntry(streamMsgId, finalText);
        try { port.disconnect(); } catch (err) { console.warn('[ClawSide] port.disconnect failed:', err?.message); }
      }

      if (msg.type === 'stream:error') {
        // Replace the streaming placeholder with an error message
        const entry = timeline.find((e) => e.id === streamMsgId);
        if (entry) {
          entry.role = 'system';
          entry.text = String(msg.error || t('requestFailed'));
          entry.status = 'error';
          persistTimeline();
        }
        // Re-render the changed row
        const row = output.querySelector(`[data-msg-id="${streamMsgId}"]`);
        if (row) {
          row.className = 'oc-msg-row oc-msg-system';
          const bubble = row.querySelector('.oc-msg-bubble');
          if (bubble) {
            const textEl = bubble.querySelector('.oc-msg-text');
            if (textEl) textEl.textContent = String(msg.error || t('requestFailed'));
          }
        }
        try { port.disconnect(); } catch (err) { console.warn('[ClawSide] port.disconnect failed:', err?.message); }
      }
    });

    port.postMessage({
      type: 'copilot:streamRequest',
      payload: {
        action,
        message: promptText,
        includeContext: contextToggle.checked,
        pageContext: context,
        agentId: agentSelect.value,
        screenshot
      }
    });
  }

  screenshotBtn.addEventListener('click', () => {
    openImagePicker();
  });

  attachmentRemoveBtn.addEventListener('click', () => {
    clearPendingScreenshot();
    input.focus();
  });

  imageFileInput.addEventListener('change', () => {
    const file = imageFileInput.files?.[0];
    if (!file) return;
    attachImageFile(file);
    imageFileInput.value = '';
  });

  input.addEventListener('paste', (event) => {
    const items = Array.from(event.clipboardData?.items || []);
    const imageItem = items.find((item) => String(item.type || '').startsWith('image/'));
    if (!imageItem) return;
    const file = imageItem.getAsFile();
    if (!file) return;
    event.preventDefault();
    attachImageFile(file);
  });

  sendBtn.addEventListener('click', () => {
    const rawInput = String(input.value || '').trim();
    const screenshot = consumePendingScreenshot();
    input.value = '';
    dispatchAction('chat', rawInput, '', { screenshot });
    input.focus();
  });

  input.addEventListener('keydown', (event) => {
    if (event.key !== 'Enter' || event.shiftKey || event.isComposing) return;
    event.preventDefault();
    const rawInput = String(input.value || '').trim();
    const screenshot = consumePendingScreenshot();
    input.value = '';
    dispatchAction('chat', rawInput, '', { screenshot });
    input.focus();
  });

  shortcutsInline.addEventListener('click', (event) => {
    const target = event.target instanceof Element ? event.target.closest('button[data-shortcut-index]') : null;
    if (!target) return;
    const index = Number(target.getAttribute('data-shortcut-index') || 0);
    const shortcut = getShortcut(index);
    const userText = String(input.value || '').trim();
    const basePrompt = String(shortcut.prompt || '').trim() || defaultPromptByAction(shortcut.action);
    const composedPrompt = userText ? `${basePrompt}\n\n${t('additionalRequirements')}${userText}` : basePrompt;
    const timelineText = `${shortcut.label}\n${composedPrompt}`;
    const screenshot = consumePendingScreenshot();
    input.value = '';
    dispatchAction(shortcut.action, composedPrompt, timelineText, { screenshot });
    input.focus();
  });


  (async () => {
    syncPageContext(true);

    try {
      const uiData = await readSync(['clawsideUi']);
      const storedMode = uiData?.clawsideUi?.layoutMode;
      const storedVersion = uiData?.clawsideUi?.layoutModeVersion;
      const storedBubblePosition = uiData?.clawsideUi?.bubbleDefaultPosition;
      const storedBubbleCustomPosition = uiData?.clawsideUi?.bubbleCustomPosition;
      languagePreference = normalizeLanguagePreference(uiData?.clawsideUi?.languagePreference);
      bubbleDefaultPosition = normalizeBubbleDefaultPosition(storedBubblePosition);
      bubbleCustomPosition = normalizeBubbleCustomPosition(storedBubbleCustomPosition);
      applyLanguage(languagePreference);

      if (storedVersion !== LAYOUT_MODE_VERSION) {
        layoutMode = DEFAULT_LAYOUT_MODE;
        await writeSync({ clawsideUi: buildUiSettingsPayload() });
      } else {
        layoutMode = normalizeLayoutMode(storedMode);
      }

      layoutModeSelect.value = layoutMode;
      bubbleDefaultPositionSelect.value = bubbleDefaultPosition;
      syncPageShift();
      applyBubblePosition();
    } catch (err) {
      console.warn('[ClawSide] init: failed to load UI settings, using defaults:', err?.message);
      layoutMode = DEFAULT_LAYOUT_MODE;
      languagePreference = DEFAULT_LANGUAGE_PREFERENCE;
      bubbleDefaultPosition = DEFAULT_BUBBLE_POSITION;
      bubbleCustomPosition = null;
      applyLanguage(languagePreference);
      layoutModeSelect.value = layoutMode;
      bubbleDefaultPositionSelect.value = bubbleDefaultPosition;
      syncPageShift();
      applyBubblePosition();
    }

    try {
      const shortcutData = await readSync([SHORTCUTS_STORAGE_KEY]);
      const normalizedShortcuts = ensureShortcutState(shortcutData?.[SHORTCUTS_STORAGE_KEY] || {});
      if (JSON.stringify(shortcutData?.[SHORTCUTS_STORAGE_KEY] || {}) !== JSON.stringify(normalizedShortcuts)) {
        await writeSync({ [SHORTCUTS_STORAGE_KEY]: normalizedShortcuts });
      }
      applyShortcutState(normalizedShortcuts);
      await relocalizeBuiltinShortcutsIfNeeded();
    } catch (err) {
      console.warn('[ClawSide] init: failed to load shortcuts, using defaults:', err?.message);
      const fallbackShortcuts = ensureShortcutState({});
      applyShortcutState(fallbackShortcuts);
    }

    try {
      const stateResp = await sendMessage({ type: 'copilot:getOpenClawState' });
      if (stateResp?.ok) {
        applyAgentState(stateResp.data);
      } else {
        const local = await readSync(['openclaw']);
        applyAgentState(local.openclaw || {});
      }
    } catch (err) {
      console.warn('[ClawSide] init: failed to load agent state from background, falling back to storage:', err?.message);
      const local = await readSync(['openclaw']);
      applyAgentState(local.openclaw || {});
    }
  })();
})();
