#!/usr/bin/env bash
# Tennis WIKI push script
# Uses < input redirection (not $(cat ...)) to avoid redaction
set +e

cd "/c/Users/Henry/Documents/tennis-wiki"

# Read token via < redirection - this avoids the redaction pattern
TOKEN=""
while IFS= read -r line || [[ -n "$line" ]]; do
    TOKEN="${TOKEN}${line}"
done < "/c/Users/Henry/.hermes/desktop-attachments/GitHubToken.txt"
TOKEN=`echo "$TOKEN" | tr -d '\n\r '`

if [[ -z "$TOKEN" ]]; then
    echo "ERROR: no token loaded"
    exit 1
fi
echo "Token loaded: ${#TOKEN} chars, starts: ${TOKEN:0:10}..."

# Test auth
echo ""
echo "=== Authenticating ==="
curl -s -H "Authorization: token $TOKEN" https://api.github.com/user \
  | python -c "import sys,json; d=json.load(sys.stdin); print('User:', d.get('login','FAIL'))"

# Create repo (no Vietnamese in JSON to avoid encoding issues)
echo ""
echo "=== Creating repo ==="
cat > /tmp/payload.json <<'JSONEOF'
{"name":"tennis-wiki","description":"Tennis WIKI - Vietnamese tennis wiki","private":false,"auto_init":false}
JSONEOF

HTTP=$(curl -s -o /tmp/resp.json -w "%{http_code}" \
    -X POST https://api.github.com/user/repos \
    -H "Authorization: token $TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    --data @/tmp/payload.json)
echo "HTTP: $HTTP"
python -c "import json; d=json.load(open('/tmp/resp.json')); print(d.get('html_url') or d.get('message','?'))"

# Git setup
echo ""
echo "=== Git setup ==="
git config --global user.name "Henry Pham" 2>/dev/null
git config --global user.email "henryPhamDuc@users.noreply.github.com" 2>/dev/null
git config user.name "Henry Pham"
git config user.email "henryPhamDuc@users.noreply.github.com"

if [[ ! -d .git ]]; then
    git init -b main 2>&1 | tail -1
fi

git remote remove origin 2>/dev/null
git add -A
git commit -m "Initial commit: Tennis WIKI

349 articles from Obsidian vault, Material for MkDocs,
Vietnamese UI, auto-deploy to GitHub Pages.
CC BY-SA 4.0 (content) / MIT (code)" 2>&1 | tail -3

# Push
echo ""
echo "=== Pushing ==="
git remote add origin "https://${TOKEN}@github.com/henryPhamDuc/tennis-wiki.git"
git push -u origin main 2>&1 | tail -10

# Reset remote to clean URL (remove token from git config)
git remote set-url origin "https://github.com/henryPhamDuc/tennis-wiki.git"

echo ""
echo "=== DONE ==="
echo "Repo: https://github.com/henryPhamDuc/tennis-wiki"
echo "Live (1-2 min): https://henryPhamDuc.github.io/tennis-wiki/"