# Tennis WIKI - One-time setup and push script (PowerShell)
# ===========================================================
# Run this ONCE in PowerShell from the repo root.
# Creates the GitHub repo, stores your token securely, and pushes everything.

$ErrorActionPreference = 'Stop'

# ---- 1. Verify token is set ----
$token = $env:GITHUB_TOKEN
if (-not $token) {
    $secure = Read-Host "Paste your GitHub token (ghp_...)" -AsSecureString
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secure)
    $token = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) | Out-Null
}
if ($token.Length -lt 30) {
    Write-Error "Token looks too short. Aborting."
    exit 1
}

# ---- 2. Configure git user (one-time) ----
git config user.name  "Henry Phạm"
git config user.email "henryPhamDuc@users.noreply.github.com"

# ---- 3. Init + commit ----
if (-not (Test-Path ".git")) {
    git init -b main | Out-Null
    Write-Host "[+] git init done"
}
git add -A
$changes = git diff --cached
if ($changes) {
    git commit -m "Initial commit: Tennis WIKI

- 349 articles from Obsidian vault (Vietnamese tennis content)
- Material for MkDocs static site
- Auto-deploy to GitHub Pages via GitHub Actions
- Vietnamese UI, full-text search, light/dark mode
- Categories: ky-thuat, co-sinh-hoc, chien-thuat, tam-ly,
  the-luc, tay-vot, cam-nang, tham-khao, wiki, he-thong
- Obsidian [[wikilinks]] auto-converted to relative Markdown links
- CC BY-SA 4.0 (content) / MIT (code)" | Out-Null
    Write-Host "[+] Initial commit done"
} else {
    Write-Host "[=] Nothing to commit"
}

# ---- 4. Create GitHub repo via API ----
$headers = @{
    Authorization = "token $token"
    Accept        = "application/vnd.github+json"
    "User-Agent"  = "tennis-wiki-setup"
}
$body = @{
    name        = "tennis-wiki"
    description = "🎾 Tennis WIKI — Bách khoa toàn thư mở về quần vợt hiện đại (tiếng Việt)"
    private     = $false
    auto_init   = $false
} | ConvertTo-Json

try {
    $resp = Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Headers $headers -Method Post -Body $body -ContentType "application/json"
    Write-Host "[+] Created repo: $($resp.html_url)"
} catch {
    $code = $_.Exception.Response.StatusCode.value__
    if ($code -eq 422) {
        Write-Host "[=] Repo already exists (HTTP 422). Skipping creation."
    } else {
        Write-Host "[!] Repo creation returned HTTP $code. Trying push anyway..."
    }
}

# ---- 5. Store token in Git Credential Manager ----
Write-Host ""
Write-Host "Storing token in Windows Credential Manager..."
$credInput = "protocol=https`nhost=github.com`nusername=henryPhamDuc`npassword=$token`n"
$credInput | git credential-manager store 2>&1 | Out-Null

# ---- 6. Push ----
$remote = "https://github.com/henryPhamDuc/tennis-wiki.git"
git remote remove origin 2>$null
git remote add origin $remote
git push -u origin main

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host "Repo: https://github.com/henryPhamDuc/tennis-wiki"
Write-Host ""
Write-Host "Next step: Go to https://github.com/henryPhamDuc/tennis-wiki/settings/pages"
Write-Host "  - Source: GitHub Actions"
Write-Host "  - Wait 1-2 min for first deploy"
Write-Host "  - Live URL: https://henryPhamDuc.github.io/tennis-wiki/"
Write-Host ""
Write-Host "Token stored in Windows Credential Manager. Future 'git push' will use it automatically."