---
hide:
 - toc
 - edit
---

# 🎨 Thư Viện Hình Ảnh Tennis

<style>
  :root {
    --primary-color: #4CAF50;
    --secondary-color: #8BC34A;
    --accent-color: #FF9800;
    --text-dark: #212121;
    --text-light: #757575;
    --bg-light: #fafafa;
    --card-shadow: 0 4px 20px rgba(0,0,0,0.08);
    --card-shadow-hover: 0 8px 30px rgba(0,0,0,0.12);
  }
  
  .hero-section {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: var(--card-shadow);
    border: 1px solid #e0e0e0;
  }
  
  .hero-title {
    font-size: 2.5em;
    font-weight: 700;
    color: var(--text-dark);
    margin-bottom: 0.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2em;
    color: var(--text-light);
    margin-bottom: 1rem;
  }
  
  .hero-description {
    font-size: 1.1em;
    color: var(--text-dark);
    line-height: 1.6;
  }
  
  .stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
  }
  
  .stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: var(--card-shadow);
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid #f0f0f0;
  }
  
  .stat-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--card-shadow-hover);
  }
  
  .stat-number {
    font-size: 2.5em;
    font-weight: 700;
    color: var(--primary-color);
    display: block;
  }
  
  .stat-label {
    font-size: 0.9em;
    color: var(--text-light);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
  }
  
  .section-header {
    position: relative;
    padding-bottom: 0.5rem;
    margin: 2rem 0 1rem 0;
    border-bottom: 3px solid var(--primary-color);
  }
  
  .section-header h2 {
    color: var(--text-dark);
    font-weight: 600;
  }
  
  .gallery-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
    margin: 1rem 0;
  }
  
  .gallery-card {
    display: block;
    background: white;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: var(--card-shadow);
    transition: all 0.3s ease;
    border: 1px solid #f0f0f0;
    text-decoration: none;
    color: inherit;
  }
  
  .gallery-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--card-shadow-hover);
    border-color: var(--primary-color);
  }
  
  .gallery-card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-bottom: 1px solid #f0f0f0;
    transition: transform 0.3s ease;
  }
  
  .gallery-card:hover img {
    transform: scale(1.05);
  }
  
  .gallery-card-content {
    padding: 1rem;
  }
  
  .gallery-card strong {
    display: block;
    font-size: 0.95em;
    color: var(--text-dark);
    margin-bottom: 0.25rem;
    line-height: 1.4;
  }
  
  .gallery-card em {
    display: block;
    font-size: 0.85em;
    color: var(--text-light);
    line-height: 1.4;
  }
  
  .gallery-source {
    display: inline-block;
    margin: 0.5rem 0;
    padding: 0.25rem 0.75rem;
    background: #f5f5f5;
    color: var(--text-light);
    border-radius: 4px;
    font-size: 0.85em;
    text-decoration: none;
    transition: all 0.2s ease;
  }
  
  .gallery-source:hover {
    background: var(--primary-color);
    color: white;
  }
  
  .nav-section {
    background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
    border: 1px solid #d0e8d0;
  }
  
  .nav-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 0.75rem;
  }
  
  .nav-section li {
    padding: 0.5rem 1rem;
    border-radius: 6px;
    transition: all 0.2s ease;
  }
  
  .nav-section li:hover {
    background: rgba(76, 175, 80, 0.1);
  }
  
  .nav-section a {
    text-decoration: none;
    color: var(--text-dark);
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .nav-section a:hover {
    color: var(--primary-color);
  }
  
  .category-badge {
    display: inline-block;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8em;
    font-weight: 600;
    color: white;
  }
  
  .badge-forehand { background: #4CAF50; }
  .badge-backhand { background: #FF9800; }
  .badge-serve { background: #2196F3; }
  .badge-footwork { background: #9C27B0; }
  .badge-fundamentals { background: #607D8B; }
  .badge-slice { background: #795548; }
  .badge-strategy { background: #E91E63; }
  
  .resources-section {
    background: #fafafa;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 2rem 0;
    border: 1px solid #e0e0e0;
  }
  
  .resources-section h3 {
    color: var(--text-dark);
    margin-bottom: 1rem;
  }
  
  .resources-section ul {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 0.75rem;
  }
  
  .resources-section li {
    padding: 0.5rem 0;
    border-bottom: 1px solid #e0e0e0;
  }
  
  .resources-section a {
    text-decoration: none;
    color: var(--primary-color);
    font-weight: 500;
  }
  
  .resources-section a:hover {
    color: var(--secondary-color);
    text-decoration: underline;
  }
  
  .footer-note {
    text-align: center;
    padding: 1.5rem;
    color: var(--text-light);
    font-size: 0.85em;
    margin-top: 2rem;
    border-top: 1px solid #e0e0e0;
  }
  
  @media (max-width: 768px) {
    .hero-title {
      font-size: 1.8em;
    }
    
    .gallery-grid {
      grid-template-columns: 1fr;
    }
    
    .stats-container {
    grid-template-columns: repeat(2, 1fr);
    }
    }
    .footer.border-top.border-gray-light.mt-5.pt-3.text-right.text-gray {
    display: none !important;
    }
    </style>

## 🌟 Visual Coaching Library

> **40 Infographics — Biomechanics & Strategy for Modern Tennis**

Tổng hợp **40 sơ đồ infographic** chất lượng cao từ chuỗi nghiên cứu sinh học và chiến thuật tennis. Mỗi sơ đồ có **trang riêng** với ảnh full HD + mô tả song ngữ EN-VI, giúp bạn hiểu sâu về kỹ thuật, chiến thuật và cơ sinh học tennis hiện đại.

---

<div class="stats-container">
<div class="stat-card">
  <span class="stat-number">40</span>
  <span class="stat-label">Sơ đồ Infographic</span>
</div>
<div class="stat-card">
  <span class="stat-number">7</span>
  <span class="stat-label">Chủ đề Chính</span>
</div>
<div class="stat-card">
  <span class="stat-number">40</span>
  <span class="stat-label">Trang Detail</span>
</div>
<div class="stat-card">
  <span class="stat-number">100%</span>
  <span class="stat-label">Song ngữ EN-VI</span>
</div>
</div>

---

## 🗂️ Danh Mục Theo Chủ Đề / Categories

<div class="nav-section">
<ul>
<li><a href="#forehand">🎯 <span class="category-badge badge-forehand">Forehand</span> — 6 sơ đồ</a></li>
<li><a href="#backhand">↩️ <span class="category-badge badge-backhand">Backhand</span> — 3 sơ đồ</a></li>
<li><a href="#serve">🚀 <span class="category-badge badge-serve">Serve</span> — 6 sơ đồ</a></li>
<li><a href="#footwork">🦶 <span class="category-badge badge-footwork">Footwork & Kinetic Chain</span> — 7 sơ đồ</a></li>
<li><a href="#fundamentals">✋ <span class="category-badge badge-fundamentals">Nền tảng kỹ thuật</span> — 4 sơ đồ</a></li>
<li><a href="#slice">🔪 <span class="category-badge badge-slice">Slice</span> — 2 sơ đồ</a></li>
<li><a href="#strategy">🧠 <span class="category-badge badge-strategy">Chiến thuật & Tư duy</span> — 12 sơ đồ</a></li>
</ul>
</div>

---

## 🎯 Forehand (Thuận tay) / Forehand

**6 sơ đồ trong chủ đề — Forehand diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="complete_process_forehand_biomechanics/" class="gallery-card">
 <img alt="Quy Trình Hoàn Chỉnh: Cầm Vợt → Điểm Tiếp Xúc → Đường Vung → Xoáy → Quỹ Đạo" src="../../assets/thu-vien/complete_process_forehand_biomechanics.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Hoàn Chỉnh: Cầm Vợt → Điểm Tiếp Xúc → Đường Vung → Xoáy → Quỹ Đạo</strong>
 <em>Complete Process: Grip → Contact → Swing → Spin → Trajectory</em>
 </div>
</a>
<a href="../../assets/thu-vien/complete_process_forehand_biomechanics.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="racquet_head_speed_drop_figure8_45whip/" class="gallery-card">
 <img alt="Quy Trình Tạo Tốc Độ Đầu Vợt — Drop • Figure-8 • 45° Whip" src="../../assets/thu-vien/racquet_head_speed_drop_figure8_45whip.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Tạo Tốc Độ Đầu Vợt — Drop • Figure-8 • 45° Whip</strong>
 <em>Racquet Head Speed Process — Drop • Figure-8 • 45° Whip</em>
 </div>
</a>
<a href="../../assets/thu-vien/racquet_head_speed_drop_figure8_45whip.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="rotational_vs_linear_engine_open_vs_closed_stance/" class="gallery-card">
 <img alt="Động Cơ Xoay vs Động Cơ Tuyến — Open vs Closed Stance" src="../../assets/thu-vien/rotational_vs_linear_engine_open_vs_closed_stance.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Động Cơ Xoay vs Động Cơ Tuyến — Open vs Closed Stance</strong>
 <em>Rotational Engine vs Linear Engine — Open vs Closed Stance</em>
 </div>
</a>
<a href="../../assets/thu-vien/rotational_vs_linear_engine_open_vs_closed_stance.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="complete_process_forehand_grip_contact/" class="gallery-card">
 <img alt="Quy Trình Hoàn Chỉnh: Cầm Vợt → Điểm Tiếp Xúc → Quỹ Đạo → Chất Lượng Cú Đánh" src="../../assets/thu-vien/complete_process_forehand_grip_contact.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Hoàn Chỉnh: Cầm Vợt → Điểm Tiếp Xúc → Quỹ Đạo → Chất Lượng Cú Đánh</strong>
 <em>Complete Process: Grip → Contact → Trajectory → Shot Quality</em>
 </div>
</a>
<a href="../../assets/thu-vien/complete_process_forehand_grip_contact.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="full_process_coil_load_uncoil_release/" class="gallery-card">
 <img alt="Quy Trình Hoàn Chỉnh: Coil / Load → Uncoil / Release (Hip-Led Wave Mechanics)" src="../../assets/thu-vien/full_process_coil_load_uncoil_release.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Hoàn Chỉnh: Coil / Load → Uncoil / Release (Hip-Led Wave Mechanics)</strong>
 <em>Full Process: Coil / Load → Uncoil / Release (Hip-Led Wave Mechanics)</em>
 </div>
</a>
<a href="../../assets/thu-vien/full_process_coil_load_uncoil_release.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="rotational_vs_linear_engine_open_vs_closed/" class="gallery-card">
 <img alt="Động Cơ Xoay vs Động Cơ Tuyến: Open Stance vs Closed Stance" src="../../assets/thu-vien/rotational_vs_linear_engine_open_vs_closed.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Động Cơ Xoay vs Động Cơ Tuyến: Open Stance vs Closed Stance</strong>
 <em>Rotational Engine vs Linear Engine: Open Stance vs Closed Stance</em>
 </div>
</a>
<a href="../../assets/thu-vien/rotational_vs_linear_engine_open_vs_closed.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## ↩️ Backhand (Trái tay) / Backhand

**3 sơ đồ trong chủ đề — Backhand diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="master_two_handed_backhand_complete_system/" class="gallery-card">
 <img alt="Master Backhand Hai Tay — Hệ Thống Cơ Sinh Học Hoàn Chỉnh" src="../../assets/thu-vien/master_two_handed_backhand_complete_system.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Master Backhand Hai Tay — Hệ Thống Cơ Sinh Học Hoàn Chỉnh</strong>
 <em>Master Two-Handed Backhand — The Complete Biomechanical System</em>
 </div>
</a>
<a href="../../assets/thu-vien/master_two_handed_backhand_complete_system.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="one_handed_backhand_essential_process/" class="gallery-card">
 <img alt="Backhand Một Tay — Quy Trình Cốt Lõi" src="../../assets/thu-vien/one_handed_backhand_essential_process.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Backhand Một Tay — Quy Trình Cốt Lõi</strong>
 <em>One-Handed Backhand — The Essential Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/one_handed_backhand_essential_process.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="two_handed_backhand_biomechanics_sequential/" class="gallery-card">
 <img alt="Cơ Sinh Học Backhand Hai Tay — Trình Tự Hoàn Chỉnh" src="../../assets/thu-vien/two_handed_backhand_biomechanics_sequential.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Cơ Sinh Học Backhand Hai Tay — Trình Tự Hoàn Chỉnh</strong>
 <em>Two-Handed Backhand Biomechanics — Sequential Breakdown</em>
 </div>
</a>
<a href="../../assets/thu-vien/two_handed_backhand_biomechanics_sequential.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## 🚀 Serve (Giao bóng) / Serve

**6 sơ đồ trong chủ đề — Serve diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="cam_nang_giao_bong_4_phases/" class="gallery-card">
 <img alt="Cẩm Nang Kỹ Thuật Giao Bóng — 4 Giai Đoạn Cốt Lõi" src="../../assets/thu-vien/cam_nang_giao_bong_4_phases.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Cẩm Nang Kỹ Thuật Giao Bóng — 4 Giai Đoạn Cốt Lõi</strong>
 <em>Tennis Serve Manual — 4 Core Phases</em>
 </div>
</a>
<a href="../../assets/thu-vien/cam_nang_giao_bong_4_phases.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="tennis_serve_frame_by_frame_shelton_djokovic_nadal/" class="gallery-card">
 <img alt="Phân Tích Cú Giao Bóng Từng Khung Hình — Shelton vs Djokovic vs Nadal" src="../../assets/thu-vien/tennis_serve_frame_by_frame_shelton_djokovic_nadal.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Phân Tích Cú Giao Bóng Từng Khung Hình — Shelton vs Djokovic vs Nadal</strong>
 <em>Tennis Serve Frame-by-Frame Biomechanics — Shelton vs Djokovic vs Nadal</em>
 </div>
</a>
<a href="../../assets/thu-vien/tennis_serve_frame_by_frame_shelton_djokovic_nadal.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="kinetic_chain_spiral_serve_ground_up/" class="gallery-card">
 <img alt="Kinetic Chain & Spiral Process Trong Tennis Serve: Build → Load → Unwind → Release" src="../../assets/thu-vien/kinetic_chain_spiral_serve_ground_up.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Kinetic Chain & Spiral Process Trong Tennis Serve: Build → Load → Unwind → Release</strong>
 <em>Kinetic Chain & Spiral Process in Tennis Serve (Build → Load → Unwind → Release)</em>
 </div>
</a>
<a href="../../assets/thu-vien/kinetic_chain_spiral_serve_ground_up.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="knee_biomechanics_serve_process_overview/" class="gallery-card">
 <img alt="Cơ Sinh Học Đầu Gối Trong Tennis Serve – Process Overview" src="../../assets/thu-vien/knee_biomechanics_serve_process_overview.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Cơ Sinh Học Đầu Gối Trong Tennis Serve – Process Overview</strong>
 <em>Knee Biomechanics in Tennis Serve – Process Overview</em>
 </div>
</a>
<a href="../../assets/thu-vien/knee_biomechanics_serve_process_overview.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="knee_complete_process_serve/" class="gallery-card">
 <img alt="Cơ Sinh Học Đầu Gối Trong Tennis Serve – Quy Trình Hoàn Chỉnh" src="../../assets/thu-vien/knee_complete_process_serve.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Cơ Sinh Học Đầu Gối Trong Tennis Serve – Quy Trình Hoàn Chỉnh</strong>
 <em>Knee Biomechanics in the Tennis Serve – The Complete Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/knee_complete_process_serve.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="serve_frame_by_frame_shelton_djokovic_nadal/" class="gallery-card">
 <img alt="Tennis Serve – Phân Tích Từng Khung Hình: Shelton vs Djokovic vs Nadal" src="../../assets/thu-vien/serve_frame_by_frame_shelton_djokovic_nadal.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Tennis Serve – Phân Tích Từng Khung Hình: Shelton vs Djokovic vs Nadal</strong>
 <em>Tennis Serve – Frame-by-Frame Biomechanical Analysis (Shelton / Djokovic / Nadal)</em>
 </div>
</a>
<a href="../../assets/thu-vien/serve_frame_by_frame_shelton_djokovic_nadal.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## 🦶 Footwork & Kinetic Chain / Footwork

**7 sơ đồ trong chủ đề — Footwork diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="footwork_kinetic_chain_complete_process/" class="gallery-card">
 <img alt="Bước Chân & Chuỗi Động Lực — Toàn Bộ Quá Trình" src="../../assets/thu-vien/footwork_kinetic_chain_complete_process.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Bước Chân & Chuỗi Động Lực — Toàn Bộ Quá Trình</strong>
 <em>Footwork & Kinetic Chain — The Complete Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/footwork_kinetic_chain_complete_process.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="split_step_complete_process/" class="gallery-card">
 <img alt="Split Step — Quy Trình Hoàn Chỉnh" src="../../assets/thu-vien/split_step_complete_process.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Split Step — Quy Trình Hoàn Chỉnh</strong>
 <em>Split Step — The Complete Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/split_step_complete_process.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="force_transmission_heel_to_hand/" class="gallery-card">
 <img alt="Quá Trình Truyền Lực: Từ Gót Chân Lên Tay" src="../../assets/thu-vien/force_transmission_heel_to_hand.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quá Trình Truyền Lực: Từ Gót Chân Lên Tay</strong>
 <em>Force Transmission Process: From Heel to Hand</em>
 </div>
</a>
<a href="../../assets/thu-vien/force_transmission_heel_to_hand.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="kinetic_chain_tennis_ground_to_racket/" class="gallery-card">
 <img alt="The Kinetic Chain In Tennis: Ground → Legs → Hips → Trunk → Arm → Racket" src="../../assets/thu-vien/kinetic_chain_tennis_ground_to_racket.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>The Kinetic Chain In Tennis: Ground → Legs → Hips → Trunk → Arm → Racket</strong>
 <em>The Kinetic Chain in Tennis (Ground → Legs → Hips → Trunk → Arm → Racket)</em>
 </div>
</a>
<a href="../../assets/thu-vien/kinetic_chain_tennis_ground_to_racket.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="knee_time_gate_kinetic_chain/" class="gallery-card">
 <img alt="Gối – Cổng Thời Gian Của Kinetic Chain (Từ Ground Reaction Đến Whip)" src="../../assets/thu-vien/knee_time_gate_kinetic_chain.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Gối – Cổng Thời Gian Của Kinetic Chain (Từ Ground Reaction Đến Whip)</strong>
 <em>Knee – The Time Gate of the Kinetic Chain (from GRF to Whip)</em>
 </div>
</a>
<a href="../../assets/thu-vien/knee_time_gate_kinetic_chain.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="spiral_chain_heel_mingmen_hand/" class="gallery-card">
 <img alt="Đường Truyền Lực: Gót → Mingmen → Tay (Spiral Chain)" src="../../assets/thu-vien/spiral_chain_heel_mingmen_hand.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Đường Truyền Lực: Gót → Mingmen → Tay (Spiral Chain)</strong>
 <em>Force Transmission Path: Heel → Mingmen → Hand (Spiral Chain)</em>
 </div>
</a>
<a href="../../assets/thu-vien/spiral_chain_heel_mingmen_hand.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="universal_footwork_process_standard_prep/" class="gallery-card">
 <img alt="Quy Trình Footwork Phổ Quát: Từ Tư Thế Chuẩn Bị Đến Mọi Cú Đánh" src="../../assets/thu-vien/universal_footwork_process_standard_prep.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Footwork Phổ Quát: Từ Tư Thế Chuẩn Bị Đến Mọi Cú Đánh</strong>
 <em>Universal Footwork Process: From Standard Prep Stance to Any Shot</em>
 </div>
</a>
<a href="../../assets/thu-vien/universal_footwork_process_standard_prep.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## ✋ Nền tảng kỹ thuật / Fundamentals

**4 sơ đồ trong chủ đề — Fundamentals diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="grip_forearm_turn_racquet_face_4_strokes/" class="gallery-card">
 <img alt="Cầm Vợt – Xoay Cẳng Tay – Mặt Vợt: 4 Cú Đánh Chính" src="../../assets/thu-vien/grip_forearm_turn_racquet_face_4_strokes.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Cầm Vợt – Xoay Cẳng Tay – Mặt Vợt: 4 Cú Đánh Chính</strong>
 <em>Grip – Forearm Turn – Racquet Face for 4 Main Strokes</em>
 </div>
</a>
<a href="../../assets/thu-vien/grip_forearm_turn_racquet_face_4_strokes.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="neuromechanical_process_tennis_stroke/" class="gallery-card">
 <img alt="Quá Trình Cơ Sinh Học Thần Kinh Của Cú Đánh Tennis" src="../../assets/thu-vien/neuromechanical_process_tennis_stroke.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quá Trình Cơ Sinh Học Thần Kinh Của Cú Đánh Tennis</strong>
 <em>Neuromechanical Process of a Tennis Stroke (From Perception to Performance)</em>
 </div>
</a>
<a href="../../assets/thu-vien/neuromechanical_process_tennis_stroke.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="dantian_mingmen_center_of_gravity/" class="gallery-card">
 <img alt="Dantian, Mingmen & Center of Gravity — Hệ Thống Cơ Sinh Học" src="../../assets/thu-vien/dantian_mingmen_center_of_gravity_biomechanics.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Dantian, Mingmen & Center of Gravity — Hệ Thống Cơ Sinh Học</strong>
 <em>Dantian, Mingmen & Center of Gravity Biomechanics System</em>
 </div>
</a>
<a href="../../assets/thu-vien/dantian_mingmen_center_of_gravity_biomechanics.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="tennis_universal_movement_system/" class="gallery-card">
 <img alt="Tennis Universal Movement System — Hệ Thống Di Chuyển Toàn Diện" src="../../assets/thu-vien/tennis_universal_movement_system.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Tennis Universal Movement System — Hệ Thống Di Chuyển Toàn Diện</strong>
 <em>Tennis Universal Movement System Complete Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/tennis_universal_movement_system.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## 🔪 Slice (Bóng xoáy âm) / Slice

**2 sơ đồ trong chủ đề — Slice diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="returning_low_balls_slice_supination_pronation/" class="gallery-card">
 <img alt="Trả Bóng Thấp: FH Slice (Supination) & BH Slice (Pronation)" src="../../assets/thu-vien/returning_low_balls_slice_supination_pronation.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Trả Bóng Thấp: FH Slice (Supination) & BH Slice (Pronation)</strong>
 <em>Returning Low Balls: FH Slice (Supination) + BH Slice (Pronation)</em>
 </div>
</a>
<a href="../../assets/thu-vien/returning_low_balls_slice_supination_pronation.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="returning_low_balls_fh_bh_slice/" class="gallery-card">
 <img alt="Trả Bóng Thấp: Forehand Slice (Supination) & Backhand Slice (Pronation)" src="../../assets/thu-vien/returning_low_balls_fh_bh_slice.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Trả Bóng Thấp: Forehand Slice (Supination) & Backhand Slice (Pronation)</strong>
 <em>Returning Low Balls: Forehand Slice (with Supination) and Backhand Slice (with Pronation)</em>
 </div>
</a>
<a href="../../assets/thu-vien/returning_low_balls_fh_bh_slice.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## 🧠 Chiến thuật & Tư duy / Strategy & Mental

**12 sơ đồ trong chủ đề — Strategy & Mental diagrams**

Click thumbnail để mở trang detail. Có thêm link Xem file gốc bên dưới mỗi ảnh.

<div class="gallery-grid" markdown>

<a href="complete_tennis_system_technique_patterns_decisions_results/" class="gallery-card">
 <img alt="Hệ Thống Tennis Hoàn Chỉnh: Kỹ Thuật → Mẫu → Quyết Định → Kết Quả" src="../../assets/thu-vien/complete_tennis_system_technique_patterns_decisions_results.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Tennis Hoàn Chỉnh: Kỹ Thuật → Mẫu → Quyết Định → Kết Quả</strong>
 <em>The Complete Tennis System: Technique → Patterns → Decisions → Results</em>
 </div>
</a>
<a href="../../assets/thu-vien/complete_tennis_system_technique_patterns_decisions_results.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="exposed_angles_geometry_court_control/" class="gallery-card">
 <img alt="Góc Mở Trong Tennis — Hình Học Kiểm Soát Sân" src="../../assets/thu-vien/exposed_angles_geometry_court_control.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Góc Mở Trong Tennis — Hình Học Kiểm Soát Sân</strong>
 <em>Exposed Angles — The Geometry of Court Control</em>
 </div>
</a>
<a href="../../assets/thu-vien/exposed_angles_geometry_court_control.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="federer_adaptation_adaptive_process/" class="gallery-card">
 <img alt="Hệ Thống Thích Nghi Federer — Quy Trình Thích Nghi Trong Tennis" src="../../assets/thu-vien/federer_adaptation_adaptive_process.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Thích Nghi Federer — Quy Trình Thích Nghi Trong Tennis</strong>
 <em>Federer Adaptation System — The Adaptive Tennis Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/federer_adaptation_adaptive_process.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="pressure_cascade_atp_system/" class="gallery-card">
 <img alt="Hệ Thống Áp Lực Liên Hoàn — Cách ATP Tạo Lỗi & Thắng Điểm" src="../../assets/thu-vien/pressure_cascade_atp_system.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Áp Lực Liên Hoàn — Cách ATP Tạo Lỗi & Thắng Điểm</strong>
 <em>The Pressure Cascade System — How ATP Players Create Errors</em>
 </div>
</a>
<a href="../../assets/thu-vien/pressure_cascade_atp_system.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="analyze_apply_elite_player_sinner_3_0/" class="gallery-card">
 <img alt="Quy Trình Phân Tích & Áp Dụng Phong Cách Elite – Player Level 3.0 (Sinner Case Study)" src="../../assets/thu-vien/analyze_apply_elite_player_sinner_3_0.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Phân Tích & Áp Dụng Phong Cách Elite – Player Level 3.0 (Sinner Case Study)</strong>
 <em>Process for Analyzing & Applying Elite Player Style – Level 3.0 (Sinner Case Study)</em>
 </div>
</a>
<a href="../../assets/thu-vien/analyze_apply_elite_player_sinner_3_0.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="complete_tennis_system_technique_patterns_decisions/" class="gallery-card">
 <img alt="Hệ Thống Tennis Hoàn Chỉnh: Kỹ Thuật → Patterns → Quyết Định → Kết Quả" src="../../assets/thu-vien/complete_tennis_system_technique_patterns_decisions.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Tennis Hoàn Chỉnh: Kỹ Thuật → Patterns → Quyết Định → Kết Quả</strong>
 <em>Complete Tennis System: Technique → Patterns → Decisions → Results</em>
 </div>
</a>
<a href="../../assets/thu-vien/complete_tennis_system_technique_patterns_decisions.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="endurance_tennis_system_5_pillars/" class="gallery-card">
 <img alt="Hệ Thống Tennis Sức Bền: 5 Trụ Cột (Chân · Tay · Thở · Nhịp · Mệt)" src="../../assets/thu-vien/endurance_tennis_system_5_pillars.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Tennis Sức Bền: 5 Trụ Cột (Chân · Tay · Thở · Nhịp · Mệt)</strong>
 <em>Endurance Tennis System: 5 Pillars (Legs · Arm · Breath · Rhythm · Fatigue)</em>
 </div>
</a>
<a href="../../assets/thu-vien/endurance_tennis_system_5_pillars.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="federer_adaptation_process_3_variables/" class="gallery-card">
 <img alt="Hệ Thống Thích Ứng Federer: Quy Trình Tennis Thích Ứng" src="../../assets/thu-vien/federer_adaptation_process_3_variables.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Thích Ứng Federer: Quy Trình Tennis Thích Ứng</strong>
 <em>Federer Adaptation System: The Adaptive Tennis Process</em>
 </div>
</a>
<a href="../../assets/thu-vien/federer_adaptation_process_3_variables.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="federer_adaptive_system_full_loop/" class="gallery-card">
 <img alt="Hệ Thống Thích Ứng Federer – Quy Trình Tennis Thích Ứng (Quan Sát → Quyết Định → Thực Hiện → Hồi Phục → Lặp Lại)" src="../../assets/thu-vien/federer_adaptive_system_full_loop.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Hệ Thống Thích Ứng Federer – Quy Trình Tennis Thích Ứng (Quan Sát → Quyết Định → Thực Hiện → Hồi Phục → Lặp Lại)</strong>
 <em>Federer Adaptive System – Adaptive Tennis Process (Observe → Decide → Execute → Recover → Repeat)</em>
 </div>
</a>
<a href="../../assets/thu-vien/federer_adaptive_system_full_loop.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="federer_opponent_adaptation_3_variables/" class="gallery-card">
 <img alt="Quy Trình Federer Thích Ứng Đối Thủ: 3 Biến Số (Thời Gian · Chiều Cao · Vị Trí Sân)" src="../../assets/thu-vien/federer_opponent_adaptation_3_variables.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Quy Trình Federer Thích Ứng Đối Thủ: 3 Biến Số (Thời Gian · Chiều Cao · Vị Trí Sân)</strong>
 <em>Federer Opponent Adaptation Process: 3 Variables (Time · Height · Court Position)</em>
 </div>
</a>
<a href="../../assets/thu-vien/federer_opponent_adaptation_3_variables.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="federer_os_complete_process_diagram/" class="gallery-card">
 <img alt="Federer OS – Quy Trình Hoàn Chỉnh: Từ Point → Evolution → Zero Mode" src="../../assets/thu-vien/federer_os_complete_process_diagram.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Federer OS – Quy Trình Hoàn Chỉnh: Từ Point → Evolution → Zero Mode</strong>
 <em>Federer OS – Complete Process Diagram: From Point to Evolution to Zero Mode</em>
 </div>
</a>
<a href="../../assets/thu-vien/federer_os_complete_process_diagram.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

<a href="playbook_doubles_3_complete_process/" class="gallery-card">
 <img alt="Playbook Đánh Đôi 3.0 – Toàn Bộ Quy Trình (Từ Giao Bóng Đến Kết Thúc)" src="../../assets/thu-vien/playbook_doubles_3_complete_process.png" loading="lazy" />
 <div class="gallery-card-content">
 <strong>Playbook Đánh Đôi 3.0 – Toàn Bộ Quy Trình (Từ Giao Bóng Đến Kết Thúc)</strong>
 <em>Doubles 3.0 Playbook – The Complete Process (From Serve to Finish)</em>
 </div>
</a>
<a href="../../assets/thu-vien/playbook_doubles_3_complete_process.png" target="_blank" class="gallery-source">📂 Xem file gốc / View source PNG</a>

</div>

---

## 🔗 Tài nguyên liên quan / Related Resources

<div class="resources-section">
<h3>📚 Tài Liệu Tham Khảo</h3>
<ul>
<li><a href="https://henryphamduc.github.io/tennis/">📚 Tennis Ebook — Thư Viện Hoàn Chỉnh</a> — 35+ tài liệu tennis song ngữ</li>
<li><a href="https://henryphamduc.github.io/tennis/">📘 Tennis Manual (Master Reference v2)</a> — 22 deep dives + cơ sinh học</li>
<li><a href="https://tennis-doctor.henry-phamduc.workers.dev/">🤖 Tennis Doctor — AI Chat</a> — Hỏi đáp tennis bằng AI</li>
<li><a href="https://henryphamduc.github.io/tennis/">🎯 Cẩm nang Tennis (Wiki hub)</a></li>
</ul>
</div>

---

<div class="footer-note">
<sub>© 2026 Henry Phạm Đức · Tennis Future Lab · All site content is for educational purposes.</sub>
</div>

