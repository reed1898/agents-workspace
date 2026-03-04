function newId(prefix = 'agent') {
  return `${prefix}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}

function trim(v) {
  return String(v || '').trim();
}

const DEFAULT_LAYOUT_MODE = 'push';
const LAYOUT_MODE_VERSION = 2;
const DEFAULT_SESSION_KEY = 'main';
const DEFAULT_GATEWAY_URL = 'ws://127.0.0.1:18789';
const DEFAULT_LANGUAGE_PREFERENCE = 'auto';
const DEFAULT_BUBBLE_POSITION = 'bottom-right';
const BUBBLE_POSITIONS = ['bottom-right', 'bottom-left', 'top-right', 'top-left'];
const AGENT_EXPORT_TYPE = 'clawside/openclaw-agents';
const AGENT_EXPORT_VERSION = 1;

const I18N = {
  en: {
    pageTitle: 'ClawSide Settings',
    titleMain: 'ClawSide Settings',
    subtitleMain: 'Manage OpenClaw agents, layout mode, and privacy rules.',
    agentsTitle: 'OpenClaw Agents',
    agentsDesc: 'Choose current agent and maintain multiple OpenClaw endpoints.',
    labelCurrentAgent: 'Current Agent',
    labelAgentName: 'Agent Name',
    labelGatewayUrl: 'Gateway URL',
    labelToken: 'Token',
    newAgent: 'New Agent',
    saveAgent: 'Save Agent',
    deleteAgent: 'Delete Agent',
    testConnection: 'Test Connection',
    exportAgents: 'Export Agents',
    importAgents: 'Import Agents',
    layoutTitle: 'UI Layout',
    layoutDesc: 'Default is Push. Overlay keeps page position unchanged.',
    labelLayoutMode: 'Layout Mode',
    layoutPush: 'Push (default)',
    layoutOverlay: 'Overlay',
    labelLanguage: 'Language',
    languageAuto: 'Auto (Chrome)',
    languageZh: 'Chinese',
    languageEn: 'English',
    labelBubbleDefaultPosition: 'Default Bubble Position',
    bubbleBottomRight: 'Bottom Right',
    bubbleBottomLeft: 'Bottom Left',
    bubbleTopRight: 'Top Right',
    bubbleTopLeft: 'Top Left',
    privacyTitle: 'Privacy Domains',
    privacyDesc: 'Use comma-separated domains.',
    labelAllowList: 'Allow list',
    labelDenyList: 'Deny list',
    savePreferences: 'Save Preferences',
    statusPreferencesSaved: 'Preferences saved.',
    statusAgentSaved: 'Agent saved.',
    statusNewAgentAdded: 'New agent added and selected.',
    statusNeedOneAgent: 'At least one agent is required.',
    statusAgentDeleted: 'Agent deleted.',
    statusTestFailed: 'Test failed ({status}): {detail}',
    statusConnectionOk: 'Connection OK ({status}). {message}',
    statusAgentsExported: 'Exported {count} agent(s).',
    statusAgentsImported: 'Imported {count} agent(s).',
    statusImportFailed: 'Import failed: {detail}',
    statusImportInvalidJson: 'Invalid JSON file.',
    statusImportInvalidPayload: 'Invalid agent config format.',
    statusImportReadFailed: 'Failed to read import file.',
    statusSwitchedTo: 'Switched to {name}.',
    statusLoaded: 'Loaded.',
    ready: 'Ready.',
    defaultAgentName: 'Default Agent',
    openclawAgent: 'OpenClaw Agent',
    agentNameTemplate: 'Agent {index}'
  },
  zh: {
    pageTitle: 'ClawSide 设置',
    titleMain: 'ClawSide 设置',
    subtitleMain: '管理 OpenClaw Agent、布局模式和隐私规则。',
    agentsTitle: 'OpenClaw Agents',
    agentsDesc: '选择当前 Agent，并维护多个 OpenClaw 端点。',
    labelCurrentAgent: '当前 Agent',
    labelAgentName: 'Agent 名称',
    labelGatewayUrl: '网关地址',
    labelToken: 'Token',
    newAgent: '新增 Agent',
    saveAgent: '保存 Agent',
    deleteAgent: '删除 Agent',
    testConnection: '测试连接',
    exportAgents: '导出 Agent',
    importAgents: '导入 Agent',
    layoutTitle: '界面布局',
    layoutDesc: '默认是 Push。Overlay 不会改变网页原始布局。',
    labelLayoutMode: '布局模式',
    layoutPush: 'Push（默认）',
    layoutOverlay: 'Overlay',
    labelLanguage: '语言',
    languageAuto: '自动（跟随 Chrome）',
    languageZh: '中文',
    languageEn: 'English',
    labelBubbleDefaultPosition: '入口球默认位置',
    bubbleBottomRight: '右下',
    bubbleBottomLeft: '左下',
    bubbleTopRight: '右上',
    bubbleTopLeft: '左上',
    privacyTitle: '隐私域名',
    privacyDesc: '使用逗号分隔多个域名。',
    labelAllowList: '允许列表',
    labelDenyList: '拒绝列表',
    savePreferences: '保存偏好',
    statusPreferencesSaved: '偏好已保存。',
    statusAgentSaved: 'Agent 已保存。',
    statusNewAgentAdded: '新 Agent 已添加并选中。',
    statusNeedOneAgent: '至少需要保留一个 Agent。',
    statusAgentDeleted: 'Agent 已删除。',
    statusTestFailed: '测试失败（{status}）：{detail}',
    statusConnectionOk: '连接成功（{status}）。{message}',
    statusAgentsExported: '已导出 {count} 个 Agent。',
    statusAgentsImported: '已导入 {count} 个 Agent。',
    statusImportFailed: '导入失败：{detail}',
    statusImportInvalidJson: 'JSON 文件格式无效。',
    statusImportInvalidPayload: 'Agent 配置格式无效。',
    statusImportReadFailed: '读取导入文件失败。',
    statusSwitchedTo: '已切换到 {name}。',
    statusLoaded: '已加载。',
    ready: '已就绪。',
    defaultAgentName: '默认 Agent',
    openclawAgent: 'OpenClaw Agent',
    agentNameTemplate: 'Agent {index}'
  }
};

let languagePreference = DEFAULT_LANGUAGE_PREFERENCE;
let activeLanguage = 'en';
let bubbleDefaultPosition = DEFAULT_BUBBLE_POSITION;
let bubbleCustomPosition = null;

function normalizeLanguagePreference(value) {
  const raw = trim(value).toLowerCase();
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

function t(key, vars = {}) {
  const pack = I18N[activeLanguage] || I18N.en;
  const fallback = I18N.en || {};
  let message = pack[key] || fallback[key] || key;
  Object.keys(vars).forEach((name) => {
    message = message.replace(new RegExp(`\\{${name}\\}`, 'g'), String(vars[name]));
  });
  return message;
}

function setText(id, value) {
  const node = document.getElementById(id);
  if (node) node.textContent = value;
}

function applyOptionsLanguage() {
  document.title = t('pageTitle');

  setText('titleMain', t('titleMain'));
  setText('subtitleMain', t('subtitleMain'));
  setText('agentsTitle', t('agentsTitle'));
  setText('agentsDesc', t('agentsDesc'));
  setText('labelCurrentAgent', t('labelCurrentAgent'));
  setText('labelAgentName', t('labelAgentName'));
  setText('labelGatewayUrl', t('labelGatewayUrl'));
  setText('labelToken', t('labelToken'));
  setText('layoutTitle', t('layoutTitle'));
  setText('layoutDesc', t('layoutDesc'));
  setText('labelLayoutMode', t('labelLayoutMode'));
  setText('labelLanguage', t('labelLanguage'));
  setText('labelBubbleDefaultPosition', t('labelBubbleDefaultPosition'));
  setText('privacyTitle', t('privacyTitle'));
  setText('privacyDesc', t('privacyDesc'));
  setText('labelAllowList', t('labelAllowList'));
  setText('labelDenyList', t('labelDenyList'));

  setText('newAgent', t('newAgent'));
  setText('saveAgent', t('saveAgent'));
  setText('deleteAgent', t('deleteAgent'));
  setText('testAgent', t('testConnection'));
  setText('exportAgents', t('exportAgents'));
  setText('importAgents', t('importAgents'));
  setText('savePrivacy', t('savePreferences'));

  const layoutMode = document.getElementById('layoutMode');
  if (layoutMode) {
    const pushOption = layoutMode.querySelector('option[value="push"]');
    const overlayOption = layoutMode.querySelector('option[value="overlay"]');
    if (pushOption) pushOption.textContent = t('layoutPush');
    if (overlayOption) overlayOption.textContent = t('layoutOverlay');
  }

  const language = document.getElementById('languagePreference');
  if (language) {
    const autoOption = language.querySelector('option[value="auto"]');
    const zhOption = language.querySelector('option[value="zh"]');
    const enOption = language.querySelector('option[value="en"]');
    if (autoOption) autoOption.textContent = t('languageAuto');
    if (zhOption) zhOption.textContent = t('languageZh');
    if (enOption) enOption.textContent = t('languageEn');
    language.value = languagePreference;
  }

  const bubblePosition = document.getElementById('bubbleDefaultPosition');
  if (bubblePosition) {
    const bottomRightOption = bubblePosition.querySelector('option[value="bottom-right"]');
    const bottomLeftOption = bubblePosition.querySelector('option[value="bottom-left"]');
    const topRightOption = bubblePosition.querySelector('option[value="top-right"]');
    const topLeftOption = bubblePosition.querySelector('option[value="top-left"]');
    if (bottomRightOption) bottomRightOption.textContent = t('bubbleBottomRight');
    if (bottomLeftOption) bottomLeftOption.textContent = t('bubbleBottomLeft');
    if (topRightOption) topRightOption.textContent = t('bubbleTopRight');
    if (topLeftOption) topLeftOption.textContent = t('bubbleTopLeft');
    bubblePosition.value = bubbleDefaultPosition;
  }
}

function setStatus(message) {
  document.getElementById('status').textContent = message;
}

function normalizeLayoutMode(mode) {
  return mode === 'overlay' ? 'overlay' : DEFAULT_LAYOUT_MODE;
}

function normalizeBubbleDefaultPosition(value) {
  const raw = trim(value).toLowerCase();
  return BUBBLE_POSITIONS.includes(raw) ? raw : DEFAULT_BUBBLE_POSITION;
}

function normalizeBubbleCustomPosition(value) {
  if (!value || typeof value !== 'object') return null;
  const x = Number(value.x);
  const y = Number(value.y);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
  return { x, y };
}

function buildUiState(layoutMode, languagePreference, bubbleDefaultPosition, bubbleCustomPosition) {
  return {
    layoutMode,
    layoutModeVersion: LAYOUT_MODE_VERSION,
    languagePreference,
    bubbleDefaultPosition,
    bubbleCustomPosition: bubbleCustomPosition ? { ...bubbleCustomPosition } : null
  };
}

function normalizeAgent(raw = {}, fallbackId) {
  const id = trim(raw.id) || fallbackId || newId('agent');
  return {
    id,
    name: trim(raw.name) || t('openclawAgent'),
    baseUrl: trim(raw.baseUrl) || DEFAULT_GATEWAY_URL,
    token: trim(raw.token),
    sessionKey: trim(raw.sessionKey) || DEFAULT_SESSION_KEY
  };
}

function normalizeState(raw = {}) {
  if (Array.isArray(raw.agents) && raw.agents.length > 0) {
    const agents = raw.agents.map((a, index) => normalizeAgent(a, a.id || `agent-${index + 1}`));
    const active = trim(raw.activeAgentId);
    const activeAgentId = agents.some((a) => a.id === active) ? active : agents[0].id;
    return { agents, activeAgentId };
  }

  const hasLegacyConfig = Boolean(
    raw.baseUrl || raw.token || raw.sessionKey || raw.channel || raw.target || raw.name
  );

  const legacy = normalizeAgent(raw, raw.id || 'agent-default');
  if (!hasLegacyConfig) {
    return {
      agents: [
        {
          id: 'agent-default',
          name: t('defaultAgentName'),
          baseUrl: DEFAULT_GATEWAY_URL,
          token: '',
          sessionKey: DEFAULT_SESSION_KEY
        }
      ],
      activeAgentId: 'agent-default'
    };
  }

  return {
    agents: [normalizeAgent({ ...legacy, name: legacy.name || t('defaultAgentName') }, 'agent-default')],
    activeAgentId: 'agent-default'
  };
}

async function loadState() {
  const data = await chrome.storage.sync.get(['privacy', 'openclaw', 'clawsideUi']);
  const p = data.privacy || { allowDomains: [], denyDomains: [] };
  const layoutMode = normalizeLayoutMode(data.clawsideUi?.layoutMode);
  const layoutModeVersion = data.clawsideUi?.layoutModeVersion;

  languagePreference = normalizeLanguagePreference(data.clawsideUi?.languagePreference);
  bubbleDefaultPosition = normalizeBubbleDefaultPosition(data.clawsideUi?.bubbleDefaultPosition);
  bubbleCustomPosition = normalizeBubbleCustomPosition(data.clawsideUi?.bubbleCustomPosition);
  activeLanguage = resolveLanguage(languagePreference);
  applyOptionsLanguage();

  const state = normalizeState(data.openclaw || {});
  const updates = {};
  if (JSON.stringify(state) !== JSON.stringify(data.openclaw || {})) {
    updates.openclaw = state;
  }
  if (
    data.clawsideUi?.layoutMode !== layoutMode ||
    layoutModeVersion !== LAYOUT_MODE_VERSION ||
    normalizeLanguagePreference(data.clawsideUi?.languagePreference) !== languagePreference ||
    normalizeBubbleDefaultPosition(data.clawsideUi?.bubbleDefaultPosition) !== bubbleDefaultPosition ||
    JSON.stringify(normalizeBubbleCustomPosition(data.clawsideUi?.bubbleCustomPosition)) !== JSON.stringify(bubbleCustomPosition)
  ) {
    updates.clawsideUi = buildUiState(layoutMode, languagePreference, bubbleDefaultPosition, bubbleCustomPosition);
  }
  if (Object.keys(updates).length) await chrome.storage.sync.set(updates);

  document.getElementById('allow').value = p.allowDomains.join(',');
  document.getElementById('deny').value = p.denyDomains.join(',');
  document.getElementById('layoutMode').value = layoutMode;
  document.getElementById('languagePreference').value = languagePreference;
  document.getElementById('bubbleDefaultPosition').value = bubbleDefaultPosition;

  renderAgentSelect(state.agents, state.activeAgentId);
  return state;
}

function getCurrentState() {
  return new Promise((resolve) => {
    chrome.storage.sync.get(['openclaw'], (data) => {
      resolve(normalizeState(data.openclaw || {}));
    });
  });
}

function makeUniqueAgentIds(agents = []) {
  const used = new Set();
  return agents.map((agent, index) => {
    const base = trim(agent.id) || `agent-${index + 1}`;
    let nextId = base;
    let suffix = 2;
    while (used.has(nextId)) {
      nextId = `${base}-${suffix}`;
      suffix += 1;
    }
    used.add(nextId);
    return { ...agent, id: nextId };
  });
}

function sanitizeFileNamePart(value, fallback = 'agent') {
  const cleaned = String(value || '')
    .trim()
    .replace(/[\\/:*?"<>|]+/g, '-')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-+|-+$/g, '');
  return cleaned || fallback;
}

function extractImportSource(raw = null) {
  if (Array.isArray(raw)) {
    return { agents: raw };
  }

  if (!raw || typeof raw !== 'object') {
    return null;
  }

  if (raw.type === AGENT_EXPORT_TYPE && raw.openclaw && typeof raw.openclaw === 'object') {
    return raw.openclaw;
  }

  if (raw.openclaw && typeof raw.openclaw === 'object') {
    return raw.openclaw;
  }

  if (Array.isArray(raw.agents)) {
    return raw;
  }

  return null;
}

function parseImportedAgentState(rawText) {
  let parsed;
  try {
    parsed = JSON.parse(String(rawText || ''));
  } catch {
    throw new Error(t('statusImportInvalidJson'));
  }

  const source = extractImportSource(parsed);
  if (!source || !Array.isArray(source.agents) || source.agents.length === 0) {
    throw new Error(t('statusImportInvalidPayload'));
  }

  const normalized = normalizeState(source);
  const agents = makeUniqueAgentIds(normalized.agents || []);
  if (agents.length === 0) {
    throw new Error(t('statusImportInvalidPayload'));
  }

  const requestedActive = trim(normalized.activeAgentId);
  const activeAgentId = agents.some((agent) => agent.id === requestedActive)
    ? requestedActive
    : agents[0].id;

  return {
    agents,
    activeAgentId
  };
}

function readFileAsText(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result || ''));
    reader.onerror = () => reject(new Error(t('statusImportReadFailed')));
    reader.readAsText(file);
  });
}

async function exportAgents() {
  const state = await getCurrentState();
  const activeAgent = state.agents.find((agent) => agent.id === state.activeAgentId) || state.agents[0] || null;
  const namePart = sanitizeFileNamePart(activeAgent?.name, 'agent');
  const payload = {
    type: AGENT_EXPORT_TYPE,
    version: AGENT_EXPORT_VERSION,
    exportedAt: new Date().toISOString(),
    openclaw: state
  };

  const jsonText = JSON.stringify(payload, null, 2);
  const blob = new Blob([jsonText], { type: 'application/json' });
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const stamp = new Date().toISOString().slice(0, 10);
  link.href = objectUrl;
  link.download = `${namePart}-${stamp}.json`;
  document.body.append(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(objectUrl);

  setStatus(t('statusAgentsExported', { count: state.agents.length }));
}

function importAgents() {
  const input = document.getElementById('importAgentsFile');
  if (input) input.click();
}

async function onImportAgentsFileChange(event) {
  const input = event?.target;
  const file = input?.files?.[0];
  if (!file) return;

  try {
    const text = typeof file.text === 'function' ? await file.text() : await readFileAsText(file);
    const nextState = parseImportedAgentState(text);
    await chrome.storage.sync.set({ openclaw: nextState });
    await loadState();
    setStatus(t('statusAgentsImported', { count: nextState.agents.length }));
  } catch (error) {
    setStatus(t('statusImportFailed', { detail: error?.message || String(error) }));
  } finally {
    input.value = '';
  }
}

function renderAgentSelect(agents, activeAgentId) {
  const select = document.getElementById('agentSelect');
  select.innerHTML = '';

  agents.forEach((agent) => {
    const option = document.createElement('option');
    option.value = agent.id;
    option.textContent = agent.name;
    option.selected = agent.id === activeAgentId;
    select.append(option);
  });

  select.disabled = agents.length === 0;

  const active = agents.find((item) => item.id === activeAgentId) || agents[0];
  if (active) fillAgentFields(active);
}

function collectAgentFromForm() {
  const id = document.getElementById('agentSelect').value;
  return {
    id,
    name: trim(document.getElementById('agentName').value) || t('openclawAgent'),
    baseUrl: trim(document.getElementById('baseUrl').value),
    token: trim(document.getElementById('token').value)
  };
}

function fillAgentFields(agent) {
  document.getElementById('agentName').value = agent.name || t('openclawAgent');
  document.getElementById('baseUrl').value = agent.baseUrl || '';
  document.getElementById('token').value = agent.token || '';
}

async function savePrivacy() {
  const allowDomains = trim(document.getElementById('allow').value).split(',').map((x) => x.trim()).filter(Boolean);
  const denyDomains = trim(document.getElementById('deny').value).split(',').map((x) => x.trim()).filter(Boolean);
  const layoutMode = normalizeLayoutMode(document.getElementById('layoutMode').value);
  languagePreference = normalizeLanguagePreference(document.getElementById('languagePreference').value);
  bubbleDefaultPosition = normalizeBubbleDefaultPosition(document.getElementById('bubbleDefaultPosition').value);
  activeLanguage = resolveLanguage(languagePreference);
  applyOptionsLanguage();

  await chrome.storage.sync.set({
    privacy: { allowDomains, denyDomains },
    clawsideUi: buildUiState(layoutMode, languagePreference, bubbleDefaultPosition, bubbleCustomPosition)
  });
  setStatus(t('statusPreferencesSaved'));
}

async function saveAgent() {
  const state = await getCurrentState();
  const payload = collectAgentFromForm();
  const normalized = normalizeAgent(payload, payload.id);
  const existing = state.agents.find((agent) => agent.id === normalized.id);
  const normalizedWithSession = {
    ...normalized,
    sessionKey: existing?.sessionKey || normalized.sessionKey || DEFAULT_SESSION_KEY
  };

  const nextAgents = state.agents
    .filter((agent) => agent.id !== normalizedWithSession.id)
    .concat(normalizedWithSession)
    .sort((a, b) => (a.id > b.id ? 1 : -1));

  await chrome.storage.sync.set({
    openclaw: {
      agents: nextAgents,
      activeAgentId: normalizedWithSession.id
    }
  });

  await loadState();
  setStatus(t('statusAgentSaved'));
}

async function newAgent() {
  const state = await getCurrentState();
  const next = normalizeAgent({
    name: t('agentNameTemplate', { index: state.agents.length + 1 }),
    baseUrl: DEFAULT_GATEWAY_URL,
    token: '',
    sessionKey: DEFAULT_SESSION_KEY
  }, newId('agent'));

  const nextState = {
    agents: [...state.agents, next],
    activeAgentId: next.id
  };

  await chrome.storage.sync.set({ openclaw: nextState });
  await loadState();
  setStatus(t('statusNewAgentAdded'));
}

async function deleteAgent() {
  const state = await getCurrentState();
  const id = document.getElementById('agentSelect').value;

  if (state.agents.length <= 1) {
    setStatus(t('statusNeedOneAgent'));
    return;
  }

  const filtered = state.agents.filter((agent) => agent.id !== id);
  const nextActive = state.activeAgentId === id ? filtered[0].id : state.activeAgentId;

  await chrome.storage.sync.set({
    openclaw: {
      agents: filtered,
      activeAgentId: nextActive
    }
  });

  await loadState();
  setStatus(t('statusAgentDeleted'));
}

async function testAgent() {
  const payload = collectAgentFromForm();

  const res = await new Promise((resolve) => {
    chrome.runtime.sendMessage({ type: 'copilot:testConnection', agent: payload }, (resp) => {
      if (chrome.runtime.lastError) {
        resolve({ ok: false, status: 0, data: { error: chrome.runtime.lastError.message } });
        return;
      }
      resolve(resp);
    });
  });

  if (!res || !res.ok) {
    const detail = res?.data?.error || JSON.stringify(res?.data || {});
    setStatus(t('statusTestFailed', { status: res?.status || 0, detail }));
    return;
  }

  setStatus(t('statusConnectionOk', { status: res.status, message: res.data?.message || t('ready') }));
}

async function onSelectAgent() {
  const state = await getCurrentState();
  const id = document.getElementById('agentSelect').value;
  const active = state.agents.find((agent) => agent.id === id) || state.agents[0];

  if (!active) return;

  await chrome.storage.sync.set({
    openclaw: {
      ...state,
      activeAgentId: active.id
    }
  });

  fillAgentFields(active);
  setStatus(t('statusSwitchedTo', { name: active.name }));
}

function onLanguagePreferenceChange() {
  languagePreference = normalizeLanguagePreference(document.getElementById('languagePreference').value);
  activeLanguage = resolveLanguage(languagePreference);
  applyOptionsLanguage();
}

document.getElementById('newAgent').addEventListener('click', newAgent);
document.getElementById('saveAgent').addEventListener('click', saveAgent);
document.getElementById('deleteAgent').addEventListener('click', deleteAgent);
document.getElementById('testAgent').addEventListener('click', testAgent);
document.getElementById('exportAgents').addEventListener('click', exportAgents);
document.getElementById('importAgents').addEventListener('click', importAgents);
document.getElementById('importAgentsFile').addEventListener('change', onImportAgentsFileChange);
document.getElementById('savePrivacy').addEventListener('click', savePrivacy);
document.getElementById('agentSelect').addEventListener('change', onSelectAgent);
document.getElementById('languagePreference').addEventListener('change', onLanguagePreferenceChange);

loadState().then(() => {
  setStatus(t('statusLoaded'));
});
