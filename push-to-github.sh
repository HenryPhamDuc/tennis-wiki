# Tennis WIKI - One-time setup and push script
# =============================================
# Run this ONCE in your terminal from the repo root to:
#   1. Create the GitHub repo (if not already created)
#   2. Store your GitHub token securely in Windows Credential Manager
#   3. Init local git, commit, and push everything
#
# After this, future pushes just work with: git push
#
# Usage (bash / git-bash on Windows):
#   bash push-to-github.sh
# or (PowerShell):
#   .\push-to-github.ps1

set -euo pipefail

# ---- 1. Verify token ----
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo -n "Paste your GitHub token (ghp_...): "
    read -rs GITHUB_TOKEN
    echo ""
fi
if [[ ${#GITHUB_TOKEN} -lt 30 ]]; then
    echo "ERROR: token looks too short (expected 40+ chars)" >&2
    exit 1
fi

# ---- 2. Configure git user (one-time for this repo) ----
git config user.name  "Henry Phạm"
git config user.email "henryPhamDuc@users.noreply.github.com"

# ---- 3. Init + add + commit (skip if already a repo) ----
if [[ ! -d .git ]]; then
    git init -b main >/dev/null
    echo "[+] git init done"
fi
git add -A
if git diff --cached --quiet; then
    echo "[=] Nothing to commit"
else
    git commit -m "Initial commit: Tennis WIKI

- 349 articles from Obsidian vault (Vietnamese tennis content)
- Material for MkDocs static site
- Auto-deploy to GitHub Pages via GitHub Actions
- Vietnamese UI, full-text search, light/dark mode
- Categories: ky-thuat, co-sinh-hoc, chien-thuat, tam-ly,
  the-luc, tay-vot, cam-nang, tham-khao, wiki, he-thong
- Obsidian [[wikilinks]] auto-converted to relative Markdown links
- CC BY-SA 4.0 (content) / MIT (code)" >/dev/null
    echo "[+] Initial commit done"
fi

# ---- 4. Create GitHub repo via API ----
PAYLOAD=$(cat <<EOF
{
  "name": "tennis-wiki",
  "description": "🎾 Tennis WIKI — Bách khoa toàn thư mở về quần vợt hiện đại (tiếng Việt)",
  "private": false,
  "auto_init": false
}
EOF
)

HTTP_CODE=$(curl -s -o /tmp/repo_create.json -w "%{http_code}" \
    -X POST https://api.github.com/user/repos \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "User-Agent: tennis-wiki-setup" \
    -d "$PAYLOAD")

if [[ "$HTTP_CODE" == "201" ]]; then
    echo "[+] Created repo: https://github.com/henryPhamDuc/tennis-wiki"
elif [[ "$HTTP_CODE" == "422" ]]; then
    echo "[=] Repo already exists (HTTP 422). Skipping creation."
else
    echo "[!] Repo creation returned HTTP $HTTP_CODE. Trying push anyway..."
    cat /tmp/repo_create.json
fi

# ---- 5. Store token in Git Credential Manager ----
echo ""
echo "Storing token in Windows Credential Manager..."
printf "protocol=https\nhost=github.com\nusername=henryPhamDuc\npassword=%s\n" "$GITHUB_TOKEN" \
    | git credential-manager store 2>&1 || {
        echo "WARNING: GCM 'store' failed. Will use inline URL during push."
    }

# ---- 6. Push ----
REMOTE="https://github.com/henryPhamDuc/tennis-wiki.git"
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"
git push -u origin main

echo ""
echo "=== Done ==="
echo "Repo: https://github.com/henryPhamDuc/tennis-wiki"
echo ""
echo "Next step: Go to https://github.com/henryPhamDuc/tennis-wiki/settings/pages"
echo "  - Source: GitHub Actions"
echo "  - Wait 1-2 min for first deploy"
echo "  - Live URL: https://henryPhamDuc.github.io/tennis-wiki/"
echo ""
echo "Token stored in Windows Credential Manager. Future 'git push' will use it automatically."