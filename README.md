# 🎾 Tennis WIKI

> **Bách khoa toàn thư mở về quần vợt hiện đại — tiếng Việt**
>
> Tổng hợp từ hệ thống nghiên cứu của Henry Phạm

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material-MkDocs-blue)](https://squidfunk.github.io/mkdocs-material/)
[![Vietnamese](https://img.shields.io/badge/Lang-Tiếng%20Việt-red)](#)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-green)](#)

## 🌐 Hệ sinh thái Tennis / Tennis Ecosystem

> **Mạng lưới các site tennis của Henry / Henry's tennis network:**

- 🏥 **[Tennis Doctor](https://tennis-doctor.henry-phamduc.workers.dev/)** — Trang chính, AI Chat tennis đa ngôn ngữ / Main hub, multilingual AI tennis chat
- 📚 **[Henry's Tennis Knowledge Vault](https://henryphamduc.github.io/tennis/)** — Cẩm nang tennis đầy đủ 14 phần / Complete tennis manual, 14 Parts
- 📖 **[Tennis Wiki EN](https://henryphamduc.github.io/tennis-wiki-en/)** — Bách khoa tennis tiếng Anh / English version
- 🔬 **[Tennis Future Lab](https://henryphamduc.github.io/tennis-future-lab/)** — Khung sinh học + AI phân tích video / Biomechanics + AI video analyzer
- 🤖 **[AI Video Analyzer (HF Space)](https://huggingface.co/spaces/HenryPhamDuc/tennis-analyzer)** — Upload video tennis, AI phân tích so với Federer / Upload tennis video, AI analyzes vs Federer

## 🌟 Tổng quan

Tennis WIKI là một **wiki tĩnh (static wiki)** được xây dựng với [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) — framework documentation phổ biến nhất thế giới, được dùng bởi Google, AWS, Kubernetes. Wiki chứa **~350 bài viết chuyên sâu** về quần vợt hiện đại, được dịch và biên soạn từ kho tài liệu cá nhân của **Henry Phạm** — huấn luyện viên quần vợt và nhà nghiên cứu cơ sinh học thể thao tại Việt Nam.

### 🎾 Các chủ đề chính

- **Kỹ thuật** — Forehand, Backhand, Serve, Volley, Footwork
- **Cơ sinh học** — Kinetic chain, Tensegrity, Wave Theory, Proprioception
- **Chiến thuật** — 70% Rule, 3-Shot Patterns, First Strike Tennis
- **Tâm lý** — Pre-Performance Routine, Breathing, Pressure Management
- **Thể lực** — Proprioception programs, Spiral Chain, age-50+ safety
- **Tay vợt chuyên nghiệp** — Federer, Nadal, Djokovic, Alcaraz, Sinner, Rublev, Shelton, Sampras
- **Cẩm nang đầy đủ** — 80+ manuals co-authored với Claude, ChatGPT, Gemini, Ollama, NotebookLM

### ⚡ Tính năng

✅ Tìm kiếm toàn văn tiếng Việt  
✅ Theme sáng/tối (light/dark mode)  
✅ Mobile-responsive (đọc trên điện thoại)  
✅ Code syntax highlighting  
✅ Auto-deploy lên GitHub Pages qua GitHub Actions  
✅ Tự động sinh TOC, breadcrumb, anchor links  
✅ Material Design — UI đẹp như các docs framework lớn  

## 🚀 Bắt đầu nhanh (5 phút)

### Yêu cầu
- Python 3.10+ ([tải tại python.org](https://python.org))
- Git

### Cài đặt local

```bash
# 1. Clone repo (sau khi push lên GitHub)
git clone https://github.com/henryPhamDuc/tennis-wiki.git
cd tennis-wiki

# 2. Cài dependencies
pip install mkdocs mkdocs-material pymdown-extensions

# 3. Xem trước trên máy (với hot-reload)
mkdocs serve
# → Mở http://127.0.0.1:8000
```

### Rebuild sau khi cập nhật nội dung

```bash
# Cập nhật từ Obsidian vault → docs/
python scripts/convert_obsidian.py --out docs

# Xem lại (live-reload tại http://127.0.0.1:8000)
mkdocs serve

# Build production
mkdocs build
```

> **Mẹo**: Chỉnh sửa thẳng trong `docs/` cũng được — bạn không nhất thiết phải luôn đi qua Obsidian.

### Deploy lên GitHub Pages

```bash
git add .
git commit -m "Update content"
git push origin main
# → GitHub Actions tự động deploy trong 1-2 phút
# → Site live tại: https://henryPhamDuc.github.io/tennis-wiki/
```

> **Lần đầu tiên**: Vào **Settings → Pages** trong GitHub repo, chọn **Source: GitHub Actions** để cho phép workflow deploy.

## 📦 Cấu trúc repo

```
tennis-wiki/
├── mkdocs.yml                         # Cấu hình MkDocs (theme, nav, plugins)
├── README.md                          # File này
├── LICENSE                            # CC BY-SA 4.0
├── docs/                              # 📂 Nội dung Markdown (input cho mkdocs)
│   ├── index.md                       # Trang chủ
│   ├── assets/
│   │   ├── tennis-extra.css           # CSS tennis theme
│   │   └── tennis-extra.js            # JS tiện ích
│   ├── ky-thuat/                      # 🎾 Kỹ thuật (193 files)
│   ├── co-sinh-hoc/                   # 🦴 Cơ sinh học (46 files)
│   ├── chien-thuat/                   # 🎯 Chiến thuật (4 files)
│   ├── tam-ly/                        # 🧠 Tâm lý (2 files)
│   ├── the-luc/                       # 🏃 Thể lực (10 files)
│   ├── tay-vot/                       # 👤 Tay vợt (5 files + 7 player subdirs)
│   ├── cam-nang/                      # 📚 Cẩm nang
│   ├── tham-khao/                     # 📖 Tham khảo
│   ├── wiki/                          # 🗒️ Wiki gốc (71 files)
│   └── he-thong/                      # ⚙️ Hệ thống
├── scripts/
│   └── convert_obsidian.py            # Obsidian MD → MkDocs MD converter
├── .github/
│   ├── workflows/
│   │   ├── deploy.yml                 # Auto-deploy to GitHub Pages
│   │   └── refresh-from-obsidian.yml  # Scheduled refresh (manual setup)
│   └── ISSUE_TEMPLATE.md
├── push-to-github.sh                  # One-command push (with token storage)
├── push-to-github.ps1                 # Same, for PowerShell
└── site/                              # Build output (gitignored — auto-built)
```

## 🎨 Theme & tuỳ chỉnh

Wiki sử dụng **Material for MkDocs** với:
- **Light mode**: Xanh cỏ tennis (`#2e7d32`) + accent vàng (`#d4e157`)
- **Dark mode**: Slate theme với green accents
- **Vietnamese UI**: Toàn bộ giao diện dịch sang tiếng Việt
- **Custom CSS** trong `docs/assets/tennis-extra.css` (thêm border tennis, hover effects, etc.)

Để tuỳ chỉnh theme, sửa `mkdocs.yml` → section `theme:`.

## 📊 Thống kê nội dung

| Metric | Value |
|--------|-------|
| Tổng số bài viết | **349** |
| Số trang HTML generated | **360** |
| Kích thước site | **17 MB** (đã nén) |
| Search index | **2.1 MB** (Vietnamese) |
| Thời gian build | **~10 giây** |
| Source folders | 6 (Obsidian vault) |
| Ngôn ngữ chính | Tiếng Việt + technical English terms |

### Phân bố theo chủ đề

| Chủ đề | Số bài |
|---|---|
| Kỹ thuật | 193 |
| Wiki gốc | 71 |
| Cơ sinh học | 46 |
| Thể lực | 10 |
| Tay vợt | 26 (5 + 7 player sub-dirs) |
| Chiến thuật | 4 |
| Tâm lý | 2 |
| Cẩm nang / Tham khảo / Hệ thống | tùy vault |

## 🔄 Quy trình cập nhật nội dung

```
1. Sửa file .md trong Obsidian vault
       ↓
2. Chạy: python scripts/convert_obsidian.py --out docs
       ↓
3. (Tùy chọn) Xem trước: mkdocs serve
       ↓
4. Commit + push:
   git add docs/
   git commit -m "Cập nhật từ Obsidian vault"
   git push origin main
       ↓
5. GitHub Actions tự động:
   - Cài mkdocs-material
   - Build site
   - Deploy lên https://henryPhamDuc.github.io/tennis-wiki/
       ↓
6. Trong 1-2 phút, wiki online với nội dung mới
```

### Thêm nguồn nội dung mới

Mở `scripts/convert_obsidian.py`, thêm vào `DEFAULT_SOURCES`:

```python
DEFAULT_SOURCES = [
    {'path': r'C:\path\to\your\new\folder', 'label': 'My Source'},
    # ...
]
```

Rồi chạy `python scripts/convert_obsidian.py --out docs`.

## 🚢 Deploy

### A. GitHub Pages (Khuyến nghị — đã cấu hình sẵn)

**Tự động** qua GitHub Actions (file `.github/workflows/deploy.yml`).

Sau khi push code, vào **Settings → Pages** trong GitHub repo:
1. Source: **GitHub Actions**
2. (Tuỳ chọn) Custom domain: nhập `tennis-wiki.example.com` rồi tạo CNAME trỏ về `henryPhamDuc.github.io`

**URL mặc định**: `https://henryPhamDuc.github.io/tennis-wiki/`

### B. Self-host (VPS / server riêng)

```bash
mkdocs build
# Upload site/ directory lên web server
rsync -avz site/ user@server:/var/www/tennis-wiki/
```

Web server config mẫu (nginx):

```nginx
server {
    listen 80;
    server_name tennis-wiki.example.com;
    root /var/www/tennis-wiki;
    index index.html;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

### C. Netlify / Vercel / Cloudflare Pages

1. Connect repo vào Netlify/Vercel/Cloudflare Pages
2. Build command: `mkdocs build`
3. Publish directory: `site`
4. Done — auto-deploy trên mỗi push

## 🤝 Đóng góp

1. Fork repo
2. Tạo branch: `git checkout -b feature/improve-forehand`
3. Sửa file trong `docs/` (hoặc sửa Obsidian + chạy converter)
4. Commit + push
5. Mở Pull Request

Hoặc đơn giản hơn: edit trực tiếp trên GitHub (icon bút chì trên mỗi file `.md`).

## 📜 Giấy phép

Nội dung: [Creative Commons Attribution-ShareAlike 4.0](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0)

Khi sử dụng lại, vui lòng ghi công: *"Tennis WIKI by Henry Phạm"*

## 📞 Liên hệ

- **GitHub**: [github.com/henryPhamDuc](https://github.com/henryPhamDuc)
- **Wiki**: Sau khi deploy: `https://henryPhamDuc.github.io/tennis-wiki/`
- **Blog**: [tennis-for-everyone.blogspot.com](https://tennis-for-everyone.blogspot.com/)
- **Facebook**: [Tennis knowlegebase](https://www.facebook.com/share/1BmokPQjf2/)

---

*Tennis WIKI — xây dựng với ❤️ cho cộng đồng quần vợt Việt Nam* 🎾