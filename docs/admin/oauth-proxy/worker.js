// Sveltia CMS GitHub OAuth proxy — Cloudflare Worker.
// Single file, ~50 lines. Deploys in <30s.
//
// Why: Sveltia CMS in the browser cannot directly call
// github.com/login/oauth/* (CORS / no client_secret handling).
// This Worker holds the client_secret and proxies both
// the authorize redirect and the access_token exchange.

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const { pathname, searchParams } = url;
    const GITHUB_AUTHORIZE = "https://github.com/login/oauth/authorize";
    const GITHUB_TOKEN     = "https://github.com/login/oauth/access_token";
    const HEADERS_JSON     = { "Content-Type": "application/json" };
    const cors = {
      "Access-Control-Allow-Origin":  env.ALLOWED_ORIGIN || "*",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    // 1) /login/oauth/authorize  →  302 to github.com
    if (pathname === "/login/oauth/authorize") {
      const params = new URLSearchParams({
        client_id:     env.GITHUB_CLIENT_ID,
        redirect_uri:  searchParams.get("redirect_uri") || "",
        scope:         searchParams.get("scope") || "repo,user",
        state:         searchParams.get("state") || "",
        allow_signup:  searchParams.get("allow_signup") || "true",
      });
      return Response.redirect(`${GITHUB_AUTHORIZE}?${params}`, 302);
    }

    // 2) /login/oauth/access_token  →  POST to github, return token JSON
    if (pathname === "/login/oauth/access_token") {
      const body = await request.json();
      const ghRes = await fetch(GITHUB_TOKEN, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          client_id:     env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code:          body.code,
          redirect_uri:  body.redirect_uri,
        }),
      });
      const token = await ghRes.json();
      return new Response(JSON.stringify(token), { headers: { ...cors, ...HEADERS_JSON } });
    }

    // 3) /  →  health check
    if (pathname === "/") {
      return new Response(
        JSON.stringify({ ok: true, proxy: "sveltia-cms-github-oauth", version: 1 }),
        { headers: { ...cors, ...HEADERS_JSON } }
      );
    }

    return new Response("Not found", { status: 404, headers: cors });
  },
};
