---
title: Sveltia CMS GitHub OAuth Proxy
lang: en
---


# Sveltia CMS GitHub OAuth Proxy

Tiny Cloudflare Worker (~50 lines) that proxies the two GitHub OAuth
endpoints Sveltia CMS needs:

| Worker route | Calls |
|---|---|
| `GET  /login/oauth/authorize`    | 302 → `github.com/login/oauth/authorize?client_id=...` |
| `POST /login/oauth/access_token` | `github.com/login/oauth/access_token` (adds client_secret) |
| `GET  /`                        | health check JSON |

## Setup (5 minutes)

### 1. Register a GitHub OAuth App
- Go to https://github.com/settings/developers → **New OAuth App**
- **Application name:** `Sveltia CMS — tennis-wiki`
- **Homepage URL:** `https://henryphamduc.github.io/tennis-wiki/`
- **Authorization callback URL:** `https://sveltia-cms-github-oauth.<your-cf-subdomain>.workers.dev/callback`
  (Sveltia will hit `/callback` on the proxy — GitHub redirects back to it after user approves)
- Click **Register application** → copy the **Client ID** and generate a **Client secret**

### 2. Deploy the Worker
```bash
cd docs/admin/oauth-proxy
npm install -g wrangler          # if not already
wrangler login                   # one-time, opens browser
wrangler deploy                  # outputs the *.workers.dev URL
wrangler secret put GITHUB_CLIENT_ID        # paste client_id
wrangler secret put GITHUB_CLIENT_SECRET    # paste client_secret
wrangler secret put ALLOWED_ORIGIN          # paste: https://henryphamduc.github.io
```

### 3. Patch `docs/admin/config.yml`
Change the `backend:` block to:
```yaml
backend:
  name: github
  repo: HenryPhamDuc/tennis-wiki
  branch: main
  base_url: https://sveltia-cms-github-oauth.<your-subdomain>.workers.dev
  auth_endpoint: /login/oauth/authorize
```

### 4. Commit + push
The `mirror-admin.yml` workflow will copy the Worker files into
`site/admin/oauth-proxy/` so the repo carries them, but the Worker
itself is deployed from the Cloudflare side — it does NOT run from
the repo. Keep the proxy files in `docs/admin/oauth-proxy/` as
source-of-truth so you can redeploy after edits.

## Why this is needed

Sveltia CMS runs in the browser. Browsers can't safely hold
`client_secret` (it'd be visible to every visitor). So the
browser-side app talks to a tiny proxy that holds the secret, and
the proxy talks to GitHub. This Worker IS that proxy.

## CORS

GitHub's OAuth endpoints return CORS headers that browsers reject
for cross-origin XHR. By going through the Worker, the browser only
talks to `*.workers.dev` (same origin as the Worker), and the Worker
talks to GitHub server-to-server (no CORS issues).

## Cost

Free tier: 100,000 requests/day. Sveltia CMS makes ~5 OAuth requests
per editor session. **Effectively free** for this use case.

---

**English** | Tiếng Việt: [xem bản dịch](../vi/)

---

**English** | Tiếng Việt: [xem bản dịch](../vi/)
