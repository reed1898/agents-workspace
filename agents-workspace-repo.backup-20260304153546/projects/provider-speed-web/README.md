# Provider Speed Web (Direct Only)

Local web UI to test multiple AI provider URLs from your machine.

## Start

```bash
cd /Users/rain/.openclaw/workspace/provider-speed-web
node server.js 8899
```

Open:

```text
http://127.0.0.1:8899
```

## Notes

- Direct only (no local proxy mode).
- Server enforces direct requests by:
  - clearing `HTTP_PROXY/HTTPS_PROXY/ALL_PROXY` and lowercase variants
  - adding `curl --noproxy '*'`
