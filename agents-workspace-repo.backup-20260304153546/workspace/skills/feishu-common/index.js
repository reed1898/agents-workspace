const TOKEN_ENDPOINT = 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal';

let cachedToken = null;
let cachedTokenExpiresAt = 0;

async function fetchTenantAccessToken() {
    const appId = process.env.FEISHU_APP_ID || process.env.LARK_APP_ID;
    const appSecret = process.env.FEISHU_APP_SECRET || process.env.LARK_APP_SECRET;

    if (!appId || !appSecret) {
        throw new Error('Missing Feishu app credentials: FEISHU_APP_ID/FEISHU_APP_SECRET');
    }

    const now = Date.now();
    if (cachedToken && now < cachedTokenExpiresAt - 60 * 1000) {
        return cachedToken;
    }

    const res = await fetch(TOKEN_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ app_id: appId, app_secret: appSecret })
    });

    const data = await res.json();
    if (!res.ok || data.code !== 0 || !data.tenant_access_token) {
        throw new Error('Failed to obtain tenant_access_token: ' + (data.msg || res.statusText));
    }

    cachedToken = data.tenant_access_token;
    const expiresIn = Number(data.expire || 7200);
    cachedTokenExpiresAt = Date.now() + expiresIn * 1000;
    return cachedToken;
}

async function fetchWithAuth(url, options) {
    const token = await fetchTenantAccessToken();
    const request = options || {};
    const headers = {
        ...(request.headers || {}),
        Authorization: 'Bearer ' + token
    };

    return fetch(url, {
        ...request,
        headers
    });
}

module.exports = { fetchWithAuth };
