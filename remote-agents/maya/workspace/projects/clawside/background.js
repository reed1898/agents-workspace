const OPENCLAW_TIMEOUT_MS = 30000;
const DEFAULT_AGENT_ID = 'agent-default';
const DEFAULT_SESSION_KEY = 'main';
const DEFAULT_GATEWAY_URL = 'ws://127.0.0.1:18789';
const GATEWAY_PROTOCOL_VERSION = 3;
const GATEWAY_CLIENT_ID = 'webchat-ui';
const GATEWAY_CLIENT_MODE = 'webchat';

// ── Context Menus ────────────────────────────────────────
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'clawside-ask',
    title: 'Ask ClawSide',
    contexts: ['selection']
  });
  chrome.contextMenus.create({
    id: 'clawside-translate',
    title: 'Translate selection',
    contexts: ['selection']
  });
  chrome.contextMenus.create({
    id: 'clawside-explain',
    title: 'Explain selection',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (!tab?.id || !info.selectionText) return;
  const menuAction = info.menuItemId;
  if (!menuAction.toString().startsWith('clawside-')) return;

  chrome.tabs.sendMessage(tab.id, {
    type: 'copilot:contextMenu',
    action: menuAction,
    text: info.selectionText
  });
});

// ── Keyboard Shortcut ────────────────────────────────────
chrome.commands.onCommand.addListener((command, tab) => {
  if (command !== 'toggle-sidebar' || !tab?.id) return;
  chrome.tabs.sendMessage(tab.id, { type: 'copilot:toggleSidebar' });
});

function domainFromUrl(url) {
  try {
    return new URL(url).hostname;
  } catch {
    return '';
  }
}

function isDomainAllowed(url, settings) {
  const host = domainFromUrl(url);
  if (!host) return false;

  const allow = settings.allowDomains || [];
  const deny = settings.denyDomains || [];

  if (deny.some((domain) => host === domain || host.endsWith(`.${domain}`))) {
    return false;
  }

  if (allow.length === 0) return settings.enabled ?? true;
  return allow.some((domain) => host === domain || host.endsWith(`.${domain}`));
}

async function getPrivacy(url) {
  const domain = domainFromUrl(url);
  const all = await chrome.storage.sync.get(['privacy', 'siteSettings']);
  const privacy = all.privacy || { allowDomains: [], denyDomains: [] };
  const siteSettings = all.siteSettings || {};
  return {
    enabled: siteSettings[domain]?.enabled ?? true,
    allowDomains: privacy.allowDomains || [],
    denyDomains: privacy.denyDomains || []
  };
}

function normalizeAgent(raw = {}, fallbackId) {
  const id = raw.id || fallbackId || `agent-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
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
    const agents = stored.agents.map((agent, index) => normalizeAgent(agent, agent.id || `${DEFAULT_AGENT_ID}-${index + 1}`));
    const fallbackId = agents[0]?.id || DEFAULT_AGENT_ID;
    const activeAgentId = stored.activeAgentId || fallbackId;
    const foundActive = agents.some((item) => item.id === activeAgentId);

    return {
      agents,
      activeAgentId: foundActive ? activeAgentId : fallbackId
    };
  }

  const hasLegacyConfig = Boolean(
    stored.baseUrl || stored.token || stored.sessionKey || stored.channel || stored.target || stored.name
  );

  const legacyCandidate = hasLegacyConfig ?
    normalizeAgent(stored, stored.id || DEFAULT_AGENT_ID) :
    {
      id: DEFAULT_AGENT_ID,
      name: 'Default Agent',
      baseUrl: DEFAULT_GATEWAY_URL,
      token: '',
      sessionKey: DEFAULT_SESSION_KEY
    };

  return {
    agents: [legacyCandidate],
    activeAgentId: legacyCandidate.id
  };
}

async function getOpenClawState() {
  const all = await chrome.storage.sync.get(['openclaw']);
  const raw = all.openclaw || {};
  const state = ensureOpenClawState(raw);

  if (JSON.stringify(raw) !== JSON.stringify(state)) {
    await chrome.storage.sync.set({ openclaw: state });
  }

  return state;
}

async function getOpenClawInstance(agentId) {
  const state = await getOpenClawState();
  const explicit = state.agents.find((agent) => agent.id === agentId);
  if (explicit) return explicit;
  const active = state.agents.find((agent) => agent.id === state.activeAgentId);
  return active || state.agents[0];
}

async function setActiveOpenClawInstance(agentId) {
  const state = await getOpenClawState();
  if (!state.agents.some((agent) => agent.id === agentId)) {
    return { ok: false, error: 'Agent not found.' };
  }

  await chrome.storage.sync.set({
    openclaw: {
      ...state,
      activeAgentId: agentId
    }
  });

  return { ok: true };
}

function buildRequestMessage(action, payload) {
  const includeContext = !!payload.includeContext;

  if (action === 'chat') {
    const message = String(payload.message || 'Hello from extension');
    if (!includeContext) {
      return `[ClawSide Chat]\nUser message: ${message}`;
    }

    const context = payload.pageContext || {};
    const description = String(
      context.contentDescription || context.description || context.contentSnippet || ''
    ).trim();
    const lines = [
      '[ClawSide Chat]',
      `User message: ${message}`,
      'Current page context (replaced whenever URL changes):',
      context.url ? `- URL: ${context.url}` : '',
      context.title ? `- Title: ${context.title}` : '',
      description ? `- Description: ${description}` : '',
      context.selection ? `- Selected text: ${context.selection}` : '',
      'Instruction: answer user naturally. Use page context only when relevant to the user request.'
    ].filter(Boolean);

    return lines.join('\n');
  }

  if (action === 'summarize') {
    const text = includeContext ? (payload.pageContext?.contentSnippet || payload.message || '') : (payload.message || '');
    return `[ClawSide Summarize]\n${text}`;
  }

  if (action === 'save-kb') {
    const source = includeContext ? (payload.pageContext?.url || '') : '';
    const text = includeContext ? (payload.pageContext?.contentSnippet || payload.message || '') : (payload.message || '');
    return `[ClawSide Save KB]\nSource: ${source}\n${text}`.trim();
  }

  if (action === 'todo') {
    return `[ClawSide Todo]\nTask: ${payload.message || ''}\nSource: ${payload.source || ''}`.trim();
  }

  return `[ClawSide ${action}] ${payload.message || ''}`.trim();
}

function extractTextFromOpenClaw(payload, fallback = '') {
  const seen = new Set();

  const read = (value) => {
    if (value === null || value === undefined) return '';
    if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') return String(value);
    if (typeof value !== 'object') return '';
    if (seen.has(value)) return '';

    seen.add(value);

    if (Array.isArray(value)) {
      for (const item of value) {
        const found = read(item);
        if (found) return found;
      }
      return '';
    }

    const directKeys = ['reply', 'summary', 'text', 'message', 'content', 'output', 'result', 'answer', 'errorMessage'];
    for (const key of directKeys) {
      if (Object.prototype.hasOwnProperty.call(value, key)) {
        const found = read(value[key]);
        if (found) return found;
      }
    }

    const nestedKeys = ['data', 'payload', 'body', 'response', 'error'];
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

function classifyFetchError(error) {
  if (error?.name === 'AbortError') return 'Request timed out.';
  const msg = String(error?.message || error).toLowerCase();
  if (msg.includes('failed to fetch')) return 'Network error: cannot reach OpenClaw gateway.';
  if (msg.includes('cors')) return 'CORS error connecting to OpenClaw gateway.';
  if (msg.includes('networkerror')) return 'Network error while reaching OpenClaw gateway.';
  return `Network error: ${String(error?.message || error)}`;
}

function classifyWsCloseError(code, reason = '') {
  if (code === 1000) return reason || 'Connection closed by gateway.';
  if (code === 1006) return 'Connection dropped unexpectedly.';
  if (code === 1008) return 'Policy violation. Check token and gateway auth mode.';
  if (code === 1011) return 'Gateway internal error.';
  if (code === 4008) return 'Gateway connect failed. Check token/password or gateway policy.';
  return reason ? `Gateway closed (${code}): ${reason}` : `Gateway closed (${code}).`;
}

function normalizeGatewayWsUrl(rawUrl) {
  const raw = String(rawUrl || '').trim();
  if (!raw) return '';

  try {
    if (/^wss?:\/\//i.test(raw)) {
      return new URL(raw).toString();
    }

    if (/^https?:\/\//i.test(raw)) {
      const url = new URL(raw);
      url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:';
      return url.toString();
    }

    return new URL(`ws://${raw}`).toString();
  } catch {
    return '';
  }
}

function normalizeGatewayHttpBase(rawUrl) {
  const wsUrl = normalizeGatewayWsUrl(rawUrl);
  if (!wsUrl) return '';

  try {
    const url = new URL(wsUrl);
    url.protocol = url.protocol === 'wss:' ? 'https:' : 'http:';
    const pathname = url.pathname.replace(/\/+$/, '');
    return `${url.origin}${pathname}`;
  } catch {
    return '';
  }
}

function parseImageDataUrl(rawDataUrl) {
  const value = String(rawDataUrl || '').trim();
  const match = value.match(/^data:(image\/[a-z0-9.+-]+);base64,([a-z0-9+/=]+)$/i);
  if (!match) return null;
  return {
    mimeType: match[1].toLowerCase(),
    base64: match[2]
  };
}

const IMAGE_MAX_BASE64_BYTES = 380 * 1024;
const IMAGE_MAX_DIMENSION = 1280;
const IMAGE_MIN_QUALITY = 0.3;

async function compressImageDataUrl(dataUrl, maxBase64Bytes = IMAGE_MAX_BASE64_BYTES) {
  const parsed = parseImageDataUrl(dataUrl);
  if (!parsed) return dataUrl;

  if (parsed.base64.length <= maxBase64Bytes) return dataUrl;

  try {
    const resp = await fetch(dataUrl);
    const blob = await resp.blob();
    const bitmap = await createImageBitmap(blob);
    let { width, height } = bitmap;

    if (width > IMAGE_MAX_DIMENSION || height > IMAGE_MAX_DIMENSION) {
      const scale = IMAGE_MAX_DIMENSION / Math.max(width, height);
      width = Math.round(width * scale);
      height = Math.round(height * scale);
    }

    for (let quality = 0.7; quality >= IMAGE_MIN_QUALITY; quality -= 0.1) {
      const canvas = new OffscreenCanvas(width, height);
      const ctx = canvas.getContext('2d');
      ctx.drawImage(bitmap, 0, 0, width, height);

      const outBlob = await canvas.convertToBlob({ type: 'image/jpeg', quality });
      const buf = await outBlob.arrayBuffer();
      const b64 = btoa(String.fromCharCode(...new Uint8Array(buf)));

      if (b64.length <= maxBase64Bytes) {
        bitmap.close();
        return `data:image/jpeg;base64,${b64}`;
      }

      if (width > 640) {
        width = Math.round(width * 0.75);
        height = Math.round(height * 0.75);
      }
    }

    const canvas = new OffscreenCanvas(Math.min(width, 640), Math.min(height, Math.round(640 * height / width)));
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
    bitmap.close();

    const outBlob = await canvas.convertToBlob({ type: 'image/jpeg', quality: IMAGE_MIN_QUALITY });
    const buf = await outBlob.arrayBuffer();
    const b64 = btoa(String.fromCharCode(...new Uint8Array(buf)));
    return `data:image/jpeg;base64,${b64}`;
  } catch (err) {
    console.warn('[ClawSide] image compression failed, sending original:', err?.message);
    return dataUrl;
  }
}

function makeRequestId() {
  try {
    if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
      return crypto.randomUUID();
    }
  } catch (err) {
    console.warn('[ClawSide] crypto.randomUUID unavailable, using fallback:', err?.message);
  }

  return `req-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

function mapGatewayError(errorLike, fallback = 'Gateway request failed.') {
  const message = extractTextFromOpenClaw(errorLike, fallback);
  const lower = message.toLowerCase();

  if (lower.includes('unauthorized')) {
    return { status: 401, message: 'Unauthorized. Check gateway token.' };
  }

  if (lower.includes('forbidden')) {
    return { status: 403, message: 'Forbidden. Check gateway token scope/role.' };
  }

  if (lower.includes('invalid')) {
    return { status: 400, message };
  }

  return { status: 500, message };
}

function safeJsonStringify(value) {
  try {
    return JSON.stringify(value);
  } catch {
    return '';
  }
}

function shouldFallbackToHttpFromWsChatError(result) {
  if (!result || result.ok) return false;

  const status = Number(result.status || result?.data?.status || 0);
  const searchText = [
    extractTextFromOpenClaw(result?.data, ''),
    extractTextFromOpenClaw(result?.data?.raw, ''),
    safeJsonStringify(result?.data),
    safeJsonStringify(result?.data?.raw)
  ]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();

  if (!searchText.includes('operator.write')) {
    return false;
  }

  return (
    searchText.includes('missing scope') ||
    searchText.includes('insufficient scope') ||
    searchText.includes('forbidden') ||
    status === 401 ||
    status === 403
  );
}

function buildGatewayConnectParams(instance) {
  const auth = instance.token ? { token: instance.token } : undefined;

  return {
    minProtocol: GATEWAY_PROTOCOL_VERSION,
    maxProtocol: GATEWAY_PROTOCOL_VERSION,
    client: {
      id: GATEWAY_CLIENT_ID,
      version: 'clawside-0.1.0',
      platform: (typeof navigator !== 'undefined' && navigator.platform) || 'browser-extension',
      mode: GATEWAY_CLIENT_MODE,
      instanceId: instance.id
    },
    caps: [],
    auth,
    locale: (typeof navigator !== 'undefined' && navigator.language) || undefined,
    userAgent: (typeof navigator !== 'undefined' && navigator.userAgent) || undefined
  };
}

function makeSessionKey() {
  return `session-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`;
}

async function startNewOpenClawSession(agentId) {
  const state = await getOpenClawState();
  const targetId = state.agents.some((agent) => agent.id === agentId) ? agentId : state.activeAgentId;
  const nextAgents = state.agents.map((agent) => {
    if (agent.id !== targetId) return agent;
    return {
      ...agent,
      sessionKey: makeSessionKey()
    };
  });

  const nextState = {
    ...state,
    agents: nextAgents,
    activeAgentId: targetId
  };

  await chrome.storage.sync.set({ openclaw: nextState });
  return nextState;
}

async function probeOpenClawGateway(instance) {
  if (!instance || !instance.baseUrl) {
    return {
      ok: false,
      status: 0,
      data: { error: 'OpenClaw settings are incomplete. Set gateway URL for the selected agent.' }
    };
  }

  const wsUrl = normalizeGatewayWsUrl(instance.baseUrl);
  if (!wsUrl) {
    return {
      ok: false,
      status: 0,
      data: { error: 'Invalid gateway URL. Use ws://, wss://, http://, or https://.' }
    };
  }

  try {
    const result = await new Promise((resolve) => {
      let settled = false;
      let ws;
      let connectRequestId = '';
      let healthRequestId = '';

      const done = (payload) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);

        try {
          if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
            ws.close(1000, 'done');
          }
        } catch (err) {
          console.warn('[ClawSide] probe: error closing WebSocket:', err?.message);
        }

        resolve(payload);
      };

      const fail = (message, status = 0, raw = null) => {
        done({
          ok: false,
          status,
          data: {
            error: message,
            status,
            raw
          }
        });
      };

      const succeed = (payload, status = 200) => {
        done({ ok: true, status, data: payload });
      };

      const sendFrame = (method, params, id) => {
        ws.send(
          JSON.stringify({
            type: 'req',
            id,
            method,
            params
          })
        );
      };

      const timer = setTimeout(() => {
        fail('OpenClaw gateway connection timed out.', 408);
      }, OPENCLAW_TIMEOUT_MS);

      try {
        ws = new WebSocket(wsUrl);
      } catch (error) {
        clearTimeout(timer);
        fail(`Cannot open WebSocket: ${String(error?.message || error)}`, 0, String(error?.message || error));
        return;
      }

      ws.onopen = () => {
        connectRequestId = makeRequestId();
        sendFrame('connect', buildGatewayConnectParams(instance), connectRequestId);
      };

      ws.onmessage = (event) => {
        let frame;
        try {
          frame = JSON.parse(String(event.data || ''));
        } catch (err) {
          console.warn('[ClawSide] probe: non-JSON frame received:', err?.message);
          return;
        }

        if (frame?.type !== 'res') {
          return;
        }

        if (frame.id === connectRequestId) {
          if (!frame.ok) {
            const mapped = mapGatewayError(frame.error || frame, 'Gateway connect failed.');
            fail(mapped.message, mapped.status, frame.error || frame);
            return;
          }

          healthRequestId = makeRequestId();
          sendFrame('health', {}, healthRequestId);
          return;
        }

        if (frame.id === healthRequestId) {
          if (!frame.ok) {
            const mapped = mapGatewayError(frame.error || frame, 'Gateway health check failed.');
            fail(mapped.message, mapped.status, frame.error || frame);
            return;
          }

          succeed({
            ok: true,
            message: 'Connected to OpenClaw gateway.',
            response: frame.payload || {}
          });
        }
      };

      ws.onerror = () => {
        // onclose handles final error mapping
      };

      ws.onclose = (event) => {
        if (settled) return;
        fail(classifyWsCloseError(event.code, event.reason), 0, {
          code: event.code,
          reason: event.reason || '',
          wasClean: event.wasClean
        });
      };
    });

    return result;
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: { error: classifyFetchError(error), status: 0, raw: String(error?.message || error) }
    };
  }
}

async function sendToOpenClaw(instance, actionMessage, onDelta) {
  if (instance && actionMessage && onDelta && typeof onDelta !== 'function') {
    console.warn('[ClawSide] sendToOpenClaw received unexpected onDelta argument type.');
  }

  return sendToOpenClawWithOptionalScreenshot(instance, actionMessage, onDelta);
}

async function sendToOpenClawWithOptionalScreenshot(instance, actionMessage, onDelta, screenshot = null) {
  if (!instance || !instance.baseUrl) {
    return {
      ok: false,
      status: 0,
      data: { error: 'OpenClaw settings are incomplete. Set gateway URL for the selected agent.' }
    };
  }

  const wsUrl = normalizeGatewayWsUrl(instance.baseUrl);
  if (!wsUrl) {
    return {
      ok: false,
      status: 0,
      data: { error: 'Invalid gateway URL. Use ws://, wss://, http://, or https://.' }
    };
  }

  const sessionKey = String(instance.sessionKey || DEFAULT_SESSION_KEY).trim() || DEFAULT_SESSION_KEY;

  try {
    const result = await new Promise((resolve) => {
      let settled = false;
      let ws;
      let connectRequestId = '';
      let chatRequestId = '';
      let expectedRunId = makeRequestId();
      let latestText = '';
      let connectSent = false;
      let sendAcked = false;

      const done = (payload) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);

        try {
          if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
            ws.close(1000, 'done');
          }
        } catch (err) {
          console.warn('[ClawSide] chat: error closing WebSocket:', err?.message);
        }

        resolve(payload);
      };

      const fail = (message, status = 0, raw = null) => {
        done({
          ok: false,
          status,
          data: {
            error: message,
            status,
            raw
          }
        });
      };

      const succeed = (payload, status = 200) => {
        done({ ok: true, status, data: payload });
      };

      const sendFrame = (method, params, id) => {
        ws.send(
          JSON.stringify({
            type: 'req',
            id,
            method,
            params
          })
        );
      };

      const sendConnect = () => {
        if (connectSent || !ws || ws.readyState !== WebSocket.OPEN) return;
        connectSent = true;
        connectRequestId = makeRequestId();
        sendFrame('connect', buildGatewayConnectParams(instance), connectRequestId);
      };

      const sendChat = async () => {
        if (!ws || ws.readyState !== WebSocket.OPEN) {
          fail('Gateway connection is not open.', 0);
          return;
        }

        chatRequestId = makeRequestId();
        const chatParams = {
          sessionKey,
          message: actionMessage,
          deliver: false,
          idempotencyKey: expectedRunId
        };

        if (screenshot?.dataUrl) {
          const compressed = await compressImageDataUrl(screenshot.dataUrl);
          const parsed = parseImageDataUrl(compressed);
          chatParams.attachments = [{
            type: 'image',
            mimeType: parsed ? parsed.mimeType : (screenshot.mimeType || 'image/jpeg'),
            content: compressed
          }];
        }

        sendFrame('chat.send', chatParams, chatRequestId);
      };

      const timer = setTimeout(() => {
        fail('OpenClaw gateway request timed out.', 408);
      }, OPENCLAW_TIMEOUT_MS);

      try {
        ws = new WebSocket(wsUrl);
      } catch (error) {
        clearTimeout(timer);
        fail(`Cannot open WebSocket: ${String(error?.message || error)}`, 0, String(error?.message || error));
        return;
      }

      ws.onopen = () => {
        sendConnect();
      };

      ws.onmessage = (event) => {
        let frame;
        try {
          frame = JSON.parse(String(event.data || ''));
        } catch (err) {
          console.warn('[ClawSide] chat: non-JSON frame received:', err?.message);
          return;
        }

        if (frame?.type === 'event') {
          if (frame.event === 'connect.challenge') {
            return;
          }

          if (frame.event !== 'chat') {
            return;
          }

          const payload = frame.payload || {};
          if (payload.sessionKey !== sessionKey) {
            return;
          }

          const runId = typeof payload.runId === 'string' ? payload.runId : '';
          if (expectedRunId && runId && runId !== expectedRunId) {
            return;
          }

          if (payload.state === 'delta') {
            const nextText = extractTextFromOpenClaw(payload.message, '');
            if (nextText && nextText.length >= latestText.length) {
              latestText = nextText;
              if (typeof onDelta === 'function') {
                try { onDelta(latestText); } catch (err) { console.warn('[ClawSide] onDelta callback error:', err?.message); }
              }
            }
            return;
          }

          if (payload.state === 'final') {
            const finalText = extractTextFromOpenClaw(payload.message, latestText);
            succeed({
              runId: runId || expectedRunId,
              status: 'ok',
              reply: finalText || latestText,
              message: payload.message,
              rawEvent: payload
            });
            return;
          }

          if (payload.state === 'error') {
            const mapped = mapGatewayError(payload, payload.errorMessage || 'OpenClaw chat error.');
            fail(mapped.message, mapped.status, payload);
            return;
          }

          if (payload.state === 'aborted') {
            fail('OpenClaw run aborted.', 499, payload);
          }
          return;
        }

        if (frame?.type !== 'res') {
          return;
        }

        if (frame.id === connectRequestId) {
          if (!frame.ok) {
            const mapped = mapGatewayError(frame.error || frame, 'Gateway connect failed.');
            fail(mapped.message, mapped.status, frame.error || frame);
            return;
          }

          sendChat();
          return;
        }

        if (frame.id === chatRequestId) {
          if (!frame.ok) {
            const mapped = mapGatewayError(frame.error || frame, 'chat.send failed.');
            fail(mapped.message, mapped.status, frame.error || frame);
            return;
          }

          sendAcked = true;
          const payload = frame.payload || {};
          if (typeof payload.runId === 'string' && payload.runId) {
            expectedRunId = payload.runId;
          }

          const status = String(payload.status || '');
          if (status === 'ok') {
            const text = extractTextFromOpenClaw(payload, latestText);
            succeed({
              runId: expectedRunId,
              status,
              reply: text,
              response: payload
            });
          }
        }
      };

      ws.onerror = () => {
        // onclose handles final error mapping
      };

      ws.onclose = (event) => {
        if (settled) return;
        fail(classifyWsCloseError(event.code, event.reason), 0, {
          code: event.code,
          reason: event.reason || '',
          wasClean: event.wasClean
        });
      };
    });

    if (!result.ok && shouldFallbackToHttpFromWsChatError(result)) {
      console.warn('[ClawSide] chat.send via WebSocket missing operator.write scope, retrying via HTTP /v1/responses.');
      const httpResult = await sendToOpenClawViaResponsesHttp(instance, actionMessage, screenshot);
      if (httpResult.ok && typeof onDelta === 'function') {
        const reply = extractTextFromOpenClaw(httpResult.data, '');
        if (reply) {
          try { onDelta(reply); } catch (err) { console.warn('[ClawSide] onDelta callback error during HTTP fallback:', err?.message); }
        }
      }
      return httpResult;
    }

    return result;
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: { error: classifyFetchError(error), status: 0, raw: String(error?.message || error) }
    };
  }
}

async function sendToOpenClawViaResponsesHttp(instance, actionMessage, screenshot) {
  if (!instance || !instance.baseUrl) {
    return {
      ok: false,
      status: 0,
      data: { error: 'OpenClaw settings are incomplete. Set gateway URL for the selected agent.' }
    };
  }

  const httpBase = normalizeGatewayHttpBase(instance.baseUrl);
  if (!httpBase) {
    return {
      ok: false,
      status: 0,
      data: { error: 'Invalid gateway URL. Use ws://, wss://, http://, or https://.' }
    };
  }

  let imageDataUrl = String(screenshot?.dataUrl || '').trim();
  if (imageDataUrl) {
    const parsedImage = parseImageDataUrl(imageDataUrl);
    if (!parsedImage) {
      return {
        ok: false,
        status: 400,
        data: { error: 'Invalid screenshot data format.' }
      };
    }

    imageDataUrl = await compressImageDataUrl(imageDataUrl);
  }

  const sessionKey = String(instance.sessionKey || DEFAULT_SESSION_KEY).trim() || DEFAULT_SESSION_KEY;
  const endpoint = `${httpBase.replace(/\/+$/, '')}/v1/responses`;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), OPENCLAW_TIMEOUT_MS);

  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (instance.token) {
      headers.Authorization = `Bearer ${instance.token}`;
    }

    const content = [{ type: 'input_text', text: actionMessage }];
    if (imageDataUrl) {
      content.push({ type: 'input_image', image_url: imageDataUrl });
    }

    const body = {
      input: [{ role: 'user', content }],
      user: sessionKey
    };

    const response = await fetch(endpoint, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      signal: controller.signal
    });

    const rawText = await response.text();
    let data = {};
    if (rawText) {
      try {
        data = JSON.parse(rawText);
      } catch {
        data = { raw: rawText };
      }
    }

    if (!response.ok) {
      return {
        ok: false,
        status: response.status,
        data: {
          error: extractTextFromOpenClaw(data, rawText || `OpenClaw HTTP error (${response.status}).`),
          status: response.status,
          raw: data
        }
      };
    }

    return {
      ok: true,
      status: response.status,
      data: {
        reply: extractTextFromOpenClaw(data, ''),
        response: data
      }
    };
  } catch (error) {
    return {
      ok: false,
      status: 0,
      data: { error: classifyFetchError(error), status: 0, raw: String(error?.message || error) }
    };
  } finally {
    clearTimeout(timer);
  }
}

function normalizeSuccessResponse(action, data, fallbackMessage = '') {
  if (action === 'summarize') {
    return {
      summary: extractTextFromOpenClaw(data, fallbackMessage)
    };
  }

  if (action === 'save-kb' || action === 'todo') {
    return {
      saved: true,
      response: data
    };
  }

  return {
    reply: extractTextFromOpenClaw(data, fallbackMessage)
  };
}

function redactSensitive(text) {
  if (!text) return '';
  return text
    .replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[REDACTED_SSN]')
    .replace(/bearer\s+[a-z0-9\-_.]+/gi, 'bearer [REDACTED]')
    .replace(/api[_-]?key\s*[:=]\s*\S+/gi, 'api_key=[REDACTED]');
}

chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  (async () => {
    if (msg?.type === 'copilot:captureScreenshot') {
      try {
        if (!chrome.tabs?.captureVisibleTab) {
          throw new Error('Screenshot API is unavailable in current browser runtime.');
        }

        const captureOptions = { format: 'jpeg', quality: 78 };
        const windowId = Number.isFinite(sender?.tab?.windowId) ? sender.tab.windowId : undefined;
        const dataUrl = await new Promise((resolve, reject) => {
          const callback = (image) => {
            if (chrome.runtime.lastError) {
              reject(new Error(chrome.runtime.lastError.message));
              return;
            }
            resolve(String(image || ''));
          };

          if (typeof windowId === 'number') {
            chrome.tabs.captureVisibleTab(windowId, captureOptions, callback);
            return;
          }

          chrome.tabs.captureVisibleTab(captureOptions, callback);
        });

        if (!dataUrl || !dataUrl.startsWith('data:image/')) {
          throw new Error('Empty screenshot result.');
        }

        sendResponse({
          ok: true,
          status: 200,
          data: {
            dataUrl,
            mimeType: 'image/jpeg'
          }
        });
      } catch (error) {
        sendResponse({
          ok: false,
          status: 500,
          data: {
            error: String(error?.message || error)
          }
        });
      }
      return;
    }

    if (msg?.type === 'copilot:request') {
      const page = msg.payload?.pageContext || {};
      const privacy = await getPrivacy(page.url || sender?.tab?.url || '');
      const action = msg.payload?.action || 'chat';
      const includeContext = !!msg.payload?.includeContext;
      const instance = await getOpenClawInstance(msg.payload?.agentId);
      const sanitizedPageContext = {
        ...page,
        selection: redactSensitive(page.selection),
        contentSnippet: redactSensitive(page.contentSnippet)
      };

      if (includeContext && !isDomainAllowed(page.url || sender?.tab?.url || '', privacy)) {
        sendResponse({ ok: false, status: 403, data: { error: 'Context disabled by privacy settings' } });
        return;
      }

      try {
        const requestMessage = buildRequestMessage(action, {
          ...msg.payload,
          pageContext: sanitizedPageContext
        });

        const openRes = await sendToOpenClawWithOptionalScreenshot(
          instance,
          requestMessage,
          undefined,
          msg.payload?.screenshot || null
        );
        if (!openRes.ok) {
          sendResponse({ ok: false, status: openRes.status, data: openRes.data });
          return;
        }

        sendResponse({
          ok: true,
          status: openRes.status,
          data: normalizeSuccessResponse(
            action,
            openRes.data,
            action === 'summarize' ? 'No summary from OpenClaw.' : 'No reply from OpenClaw.'
          )
        });
      } catch (error) {
        sendResponse({ ok: false, status: 500, data: { error: String(error?.message || error), details: 'Unexpected error while handling OpenClaw request.' } });
      }
      return;
    }

    if (msg?.type === 'copilot:todo') {
      const instance = await getOpenClawInstance(msg.agentId);
      const taskText = String(msg.task || '').trim();

      if (!taskText) {
        sendResponse({ ok: false, status: 400, data: { error: 'Task is required' } });
        return;
      }

      try {
        const requestMessage = buildRequestMessage('todo', { message: taskText, source: msg.source });
        const openRes = await sendToOpenClawWithOptionalScreenshot(
          instance,
          requestMessage,
          undefined,
          msg.screenshot || null
        );
        if (!openRes.ok) {
          sendResponse({ ok: false, status: openRes.status, data: openRes.data });
          return;
        }

        sendResponse({
          ok: true,
          status: openRes.status,
          data: normalizeSuccessResponse('todo', openRes.data, 'Todo saved.')
        });
      } catch (error) {
        sendResponse({ ok: false, status: 500, data: { error: String(error?.message || error), details: 'Unexpected error while saving todo.' } });
      }
      return;
    }

    if (msg?.type === 'copilot:testConnection') {
      const instance = msg?.agent ? normalizeAgent(msg.agent) : await getOpenClawInstance();
      const openRes = await probeOpenClawGateway(instance);

      if (!openRes.ok) {
        sendResponse({ ok: false, status: openRes.status, data: openRes.data });
        return;
      }

      sendResponse({
        ok: true,
        status: openRes.status,
        data: {
          ok: true,
          message: extractTextFromOpenClaw(openRes.data, 'Connected to OpenClaw gateway.')
        }
      });
      return;
    }

    if (msg?.type === 'copilot:getOpenClawState') {
      const state = await getOpenClawState();
      sendResponse({ ok: true, status: 200, data: state });
      return;
    }

    if (msg?.type === 'copilot:setActiveOpenClawInstance') {
      const result = await setActiveOpenClawInstance(msg.agentId);
      sendResponse(result.ok ? { ok: true, status: 200 } : { ok: false, status: 400, data: result });
      return;
    }

    if (msg?.type === 'copilot:newSession') {
      try {
        const state = await startNewOpenClawSession(msg.agentId);
        sendResponse({ ok: true, status: 200, data: { state } });
      } catch (error) {
        sendResponse({ ok: false, status: 500, data: { error: String(error?.message || error) } });
      }
      return;
    }

    if (msg?.type === 'copilot:openOptions') {
      try {
        const optionsUrl = chrome.runtime.getURL('options.html');
        if (chrome.tabs?.create) {
          await chrome.tabs.create({ url: optionsUrl });
        } else if (typeof chrome.runtime.openOptionsPage === 'function') {
          await chrome.runtime.openOptionsPage();
        } else {
          throw new Error('Cannot open options page in this browser runtime.');
        }
        sendResponse({ ok: true, status: 200 });
      } catch (error) {
        sendResponse({ ok: false, status: 500, data: { error: String(error?.message || error) } });
      }
      return;
    }

    if (msg?.type === 'copilot:getPrivacy') {
      sendResponse(await getPrivacy(msg.url));
      return;
    }

    if (msg?.type === 'copilot:setSiteEnabled') {
      const domain = domainFromUrl(msg.url);
      const current = await chrome.storage.sync.get(['siteSettings']);
      const siteSettings = current.siteSettings || {};
      siteSettings[domain] = { enabled: !!msg.enabled };
      await chrome.storage.sync.set({ siteSettings });
      sendResponse({ ok: true });
      return;
    }
  })();

  return true;
});

// ── Streaming port handler ───────────────────────────────
chrome.runtime.onConnect.addListener((port) => {
  if (port.name !== 'copilot:stream') return;

  port.onMessage.addListener(async (msg) => {
    if (msg?.type !== 'copilot:streamRequest') return;

    const payload = msg.payload || {};
    const action = payload.action || 'chat';
    const page = payload.pageContext || {};
    const includeContext = !!payload.includeContext;

    const privacy = await getPrivacy(page.url || '');
    const instance = await getOpenClawInstance(payload.agentId);

    const sanitizedPageContext = {
      ...page,
      selection: redactSensitive(page.selection),
      contentSnippet: redactSensitive(page.contentSnippet)
    };

    if (includeContext && !isDomainAllowed(page.url || '', privacy)) {
      try { port.postMessage({ type: 'stream:error', error: 'Context disabled by privacy settings' }); } catch (err) { console.warn('[ClawSide] port disconnected:', err?.message); }
      return;
    }

    const requestMessage = buildRequestMessage(action, {
      ...payload,
      pageContext: sanitizedPageContext
    });

    const onDelta = (text) => {
      try { port.postMessage({ type: 'stream:delta', text }); } catch (err) { console.warn('[ClawSide] port disconnected during stream:', err?.message); }
    };

    const result = await sendToOpenClawWithOptionalScreenshot(
      instance,
      requestMessage,
      onDelta,
      payload.screenshot || null
    );

    if (!result.ok) {
      try { port.postMessage({ type: 'stream:error', error: result.data?.error || 'Request failed.' }); } catch (err) { console.warn('[ClawSide] port disconnected:', err?.message); }
      return;
    }

    const normalized = normalizeSuccessResponse(
      action,
      result.data,
      action === 'summarize' ? 'No summary from OpenClaw.' : 'No reply from OpenClaw.'
    );

    try { port.postMessage({ type: 'stream:done', data: normalized }); } catch (err) { console.warn('[ClawSide] port disconnected:', err?.message); }
  });
});
