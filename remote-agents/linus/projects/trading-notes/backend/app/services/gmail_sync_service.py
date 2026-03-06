"""Gmail OAuth/Gmail API 同步服务"""

import base64
import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlencode

import httpx

logger = logging.getLogger(__name__)

GOOGLE_OAUTH_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_OAUTH_TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API_BASE = "https://gmail.googleapis.com/gmail/v1"

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]


class GmailOAuthError(Exception):
    """Gmail OAuth 错误"""


def build_gmail_oauth_url(
    client_id: str,
    redirect_uri: str,
    state: str
) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "access_type": "offline",
        "prompt": "consent",
        "scope": " ".join(GMAIL_SCOPES),
        "state": state,
    }
    return f"{GOOGLE_OAUTH_AUTH_URL}?{urlencode(params)}"


def exchange_code_for_tokens(
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    code: str
) -> Dict[str, Any]:
    data = {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }
    response = httpx.post(GOOGLE_OAUTH_TOKEN_URL, data=data, timeout=20.0)
    if response.status_code != 200:
        raise GmailOAuthError(response.text)
    return response.json()


def refresh_access_token(
    client_id: str,
    client_secret: str,
    refresh_token: str
) -> str:
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    }
    response = httpx.post(GOOGLE_OAUTH_TOKEN_URL, data=data, timeout=20.0)
    if response.status_code != 200:
        raise GmailOAuthError(response.text)
    payload = response.json()
    access_token = payload.get("access_token")
    if not access_token:
        raise GmailOAuthError("Missing access token")
    return access_token


def _decode_base64url(data: str) -> bytes:
    if not data:
        return b""
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _extract_attachments(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    attachments: List[Dict[str, Any]] = []
    filename = payload.get("filename")
    body = payload.get("body", {})
    attachment_id = body.get("attachmentId")

    if filename:
        attachments.append({
            "filename": filename,
            "attachment_id": attachment_id,
            "inline_data": body.get("data"),
        })

    for part in payload.get("parts", []) or []:
        attachments.extend(_extract_attachments(part))

    return attachments


class GmailApiService:
    """Gmail API 客户端"""

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.access_token}"}

    def fetch_attachments(
        self,
        sender: str,
        subject_prefix: str,
        since_days: int = 7,
        max_messages: int = 50
    ) -> List[Dict[str, Any]]:
        query = (
            f"from:{sender} subject:{subject_prefix} newer_than:{since_days}d has:attachment"
        )
        params = {"q": query, "maxResults": max_messages}

        with httpx.Client(timeout=20.0) as client:
            response = client.get(
                f"{GMAIL_API_BASE}/users/me/messages",
                headers=self._headers(),
                params=params,
            )
            if response.status_code != 200:
                raise GmailOAuthError(response.text)

            messages = response.json().get("messages", []) or []
            attachments: List[Dict[str, Any]] = []

            for message in messages:
                message_id = message.get("id")
                if not message_id:
                    continue

                msg_resp = client.get(
                    f"{GMAIL_API_BASE}/users/me/messages/{message_id}",
                    headers=self._headers(),
                    params={"format": "full"},
                )
                if msg_resp.status_code != 200:
                    logger.warning("Failed to fetch message %s: %s", message_id, msg_resp.text)
                    continue

                payload = msg_resp.json().get("payload", {}) or {}
                attachment_meta = _extract_attachments(payload)

                for item in attachment_meta:
                    filename = item.get("filename") or ""
                    ext = filename.lower().rsplit(".", 1)
                    if len(ext) != 2 or f".{ext[1]}" not in {".csv", ".xls", ".xlsx"}:
                        continue

                    data = item.get("inline_data")
                    if not data and item.get("attachment_id"):
                        attach_resp = client.get(
                            f"{GMAIL_API_BASE}/users/me/messages/{message_id}/attachments/{item['attachment_id']}",
                            headers=self._headers(),
                        )
                        if attach_resp.status_code != 200:
                            logger.warning(
                                "Failed to fetch attachment %s for %s: %s",
                                item["attachment_id"],
                                message_id,
                                attach_resp.text,
                            )
                            continue
                        data = attach_resp.json().get("data")

                    if not data:
                        continue

                    attachments.append({
                        "message_id": message_id,
                        "filename": filename,
                        "content": _decode_base64url(data),
                    })

        return attachments
