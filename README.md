<div align="center">

# 🚀 SpaceStation Survival — Necrostation

**Trò chơi bắn súng sinh tồn Sci-Fi dạng pixel 64×64 được xây dựng bằng Python & Pygame**  
*Xuất phát từ dự án tham dự LowRezJam 2022 — được mở rộng, nâng cấp và cải tiến đáng kể*

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=for-the-badge&logo=pygame&logoColor=white)](https://www.pygame.org/)
[![Nền tảng](https://img.shields.io/badge/Nền_tảng-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Giấy phép](https://img.shields.io/badge/Giấy_phép-MIT-F7DF1E?style=for-the-badge)](LICENSE)
[![LowRezJam](https://img.shields.io/badge/LowRezJam-2022-FF6B6B?style=for-the-badge)](https://itch.io/jam/lowrezjam2022)

</div>

---

## 📸 Ảnh chụp màn hình

<div align="center">

| 🏠 Màn hình chính | 🎮 Màn hình chơi game |
|:---:|:---:|
| ![Màn hình chính](https://github.com/khanhly-dn/SpaceStation_Survival_PyGame/blob/main/GD1.png?raw=true) | ![Gameplay](https://github.com/khanhly-dn/SpaceStation_Survival_PyGame/blob/main/GD2.png?raw=true) |

</div>

---

## 🎯 Giới thiệu trò chơi

**Necrostation** là trò chơi bắn súng sinh tồn nhìn từ trên xuống theo phong cách retro, diễn ra trên một trạm vũ trụ bị bỏ hoang tràn đầy sinh vật ngoài hành tinh. Người chơi vào vai một phi hành gia đơn độc, chiến đấu qua nhiều phòng liên kết nhau, quản lý kho vũ khí, giải các câu đố mã số, và đối mặt với những kẻ thù ngày càng nguy hiểm hơn để thoát ra ngoài.

Trò chơi hiển thị ở độ phân giải nội bộ **64×64 pixel** — được phóng to để vừa cửa sổ — tạo ra phong cách pixel art lo-fi đặc trưng lấy cảm hứng từ các trò chơi arcade 8-bit kinh điển. Trò chơi hỗ trợ cả điều khiển bằng **bàn phím/chuột** lẫn **cử chỉ tay qua webcam thời gian thực**.

---

## ✨ Tính năng nổi bật

### 🕹️ Gameplay chính

<div align="center">

| Tính năng | Mô tả |
|:---:|:---|
| 🗺️ **Khám phá đa phòng** | Di chuyển qua các phòng liên kết nhau thông qua cửa tương tác |
| ⚔️ **Chiến đấu thời gian thực** | Bắn, đấm tay và né tránh kẻ thù với điều khiển mượt mà |
| 🎒 **Hệ thống kho đồ** | Nhặt và chuyển đổi giữa các vũ khí trong 8 ô chứa |
| 🔢 **Câu đố mã số** | Nhập mã để mở khóa các khu vực bảo mật và tiến tiếp |
| 🤖 **Trí tuệ nhân tạo kẻ thù** | Nhiều loại sinh vật bao gồm cả boss kích thước lớn |
| ❤️ **Hệ thống máu** | Hiệu ứng nhận sát thương, hoạt ảnh bị thương và chuỗi tử vong |
| 💀 **Hệ thống xác chết** | Kẻ thù và người chơi để lại xác chết tồn tại trong màn chơi |
| 🎬 **Kết thúc điện ảnh** | Ảnh kết thúc toàn màn hình và màn hình credits |

</div>

---

### 🔫 Vũ khí

<div align="center">

| Vũ khí | Tốc độ bắn | Sát thương | Đạn | Đặc điểm |
|:---:|:---:|:---:|:---:|:---:|
| 🔫 Súng ngắn (Handgun) | Trung bình | Trung bình | Vô hạn | Cân bằng, đáng tin cậy |
| 💥 Súng hoa cải (Shotgun) | Chậm | Cao | Giới hạn | Tầm gần, bắn tản |
| ⚡ Súng điện (Stungun) | Chậm | Thấp | Rất giới hạn | Làm choáng kẻ thù |
| 🎯 Súng lục (Revolver) | Chậm | Rất cao | Giới hạn | Tầm xa, chính xác |
| 🔥 Súng máy (Minigun) | Rất nhanh | Trung bình | Vô hạn | Mở khóa bằng cheat code |

</div>

---

### 🖥️ Hai chế độ điều khiển

<div align="center">

| Chế độ | Cách hoạt động |
|:---:|:---|
| ⌨️ **Bàn phím & Chuột** | Điều khiển PC tiêu chuẩn — chính xác và phản hồi nhanh |
| 🤚 **Cử chỉ / Thị giác** | Nhận diện cử chỉ tay qua webcam bằng AI — chơi không cần chạm tay |

</div>

---

## 🧑‍💻 Điểm kỹ thuật nổi bật

<div align="center">

| Hệ thống | Cách triển khai |
|:---:|:---|
| 🎥 **Rendering** | Camera tùy chỉnh với biến đổi tọa độ world-to-screen |
| 💥 **Va chạm** | Pygame mask collision pixel-perfect kết hợp AABB |
| 🎞️ **Hoạt ảnh** | Hệ thống animation từ spritesheet, hỗ trợ ping-pong & global timer |
| ⚙️ **Action Pipeline** | Hàng đợi action bất đồng bộ (tweening, callback, overlay) |
| ✨ **Particle** | Bộ phát hạt tùy chỉnh cho khói, ánh sáng và hiệu ứng điện |
| 🔊 **Âm thanh** | Pygame mixer với hệ thống quản lý âm thanh theo tên |
| 🤚 **Nhận diện cử chỉ** | Phát hiện điểm mốc bàn tay thời gian thực qua webcam |
| 💾 **Serialization** | Hệ thống pickle/unpickle tùy chỉnh cho đối tượng Pygame Surface |
| 🎮 **Hệ thống Control** | Registry Control/Element mở rộng được cho toàn bộ UI |

</div>

---

## 🕹️ Hướng dẫn điều khiển

### ⌨️ Bàn phím & Chuột

<div align="center">

| Phím | Hành động |
|:---:|:---|
| `A` / `D` | Di chuyển trái / phải |
| `Click chuột trái` | Tấn công / Bắn |
| `Click chuột phải` | Tương tác với vật thể |
| `E` / `Space` | Tương tác với vật thể gần nhất |
| `I` | Mở / đóng kho đồ |
| `1` – `8` | Chọn ô vật phẩm |
| `Scroll Wheel` | Cuộn văn bản |
| `ESC` | Dừng game (Pause) |

</div>

### 🤚 Chế độ cử chỉ (Webcam)

<div align="center">

| Cử chỉ | Hành động |
|:---:|:---|
| ✋ Bàn tay mở | Di chuyển con trỏ |
| ✊ Nắm tay | Tấn công / Bắn |
| ☝️ Giơ ngón trỏ | Tương tác |
| 👍 Ngón cái lên | Vật phẩm tiếp theo |
| 👎 Ngón cái xuống | Vật phẩm trước |
| ✌️ Chữ V | Mở kho đồ |
| `F2` | Bật / tắt chế độ cử chỉ |

</div>

### 🎲 Mã cheat

<div align="center">

| Tổ hợp phím | Hiệu ứng |
|:---:|:---|
| `G` + `H` | Hồi máu về tối đa |
| `G` + `T` | Mở khóa Minigun đạn vô hạn |

</div>

---

## 🚀 Hướng dẫn cài đặt & chạy game

### Yêu cầu hệ thống

- Python **3.10** trở lên
- pip
- *(Tùy chọn)* Webcam để dùng chế độ cử chỉ

### Các bước cài đặt

```bash
# 1. Clone repository
git clone https://github.com/khanhly-dn/SpaceStation_Survival_PyGame.git
cd SpaceStation_Survival_PyGame

# 2. Tạo môi trường ảo (khuyến nghị)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
# source .venv/bin/activate

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Chạy game
python main.py
```

> 💡 **Lưu ý:** Chế độ cử chỉ yêu cầu webcam. Chọn ở màn hình mode hoặc bấm `F2` trong game để bật/tắt.

---

## 📁 Cấu trúc dự án

```
SpaceStation_Survival_PyGame/
│
├── 🎮 main.py              # Điểm khởi động — vòng lặp game & xử lý input
├── 🖥️ controls.py          # Toàn bộ UI: nút, popup, menu, HUD, màn hình pause
├── 👾 creatures.py         # Các loại kẻ thù, AI hành vi, logic boss
├── 🧑‍🚀 players.py          # Logic người chơi, quản lý kho đồ, vũ khí
├── 🗺️ levels.py            # Tải màn, cửa, bàn phím số, cấu trúc màn chơi
├── 📦 entities.py          # Entity cơ sở với vật lý & va chạm
├── 🔫 items.py             # Định nghĩa vũ khí và vật phẩm có thể nhặt
├── ⚙️ actions.py           # Pipeline action bất đồng bộ (tween, callback)
├── ✨ particles.py         # Hiệu ứng hạt: khói, ánh sáng, điện
├── 🎥 cameras.py           # Biến đổi camera và pipeline rendering
├── 🖼️ graphics.py          # Tải ảnh, spritesheet, render chữ
├── 🔊 sounds.py            # Quản lý âm thanh và nhạc nền
├── 🌟 arteffects.py        # Hậu kỳ và hiệu ứng overlay màn hình
├── 🤚 gesture_input.py     # Nhận diện cử chỉ qua webcam (AI)
├── 🌐 global_values.py     # Trạng thái game chia sẻ và hằng số
├── 📋 elements.py          # Registry element cơ sở cho toàn bộ control
├── 🧮 utilities.py         # Tiện ích toán học: góc, khoảng cách, nội suy
│
├── res/
│   ├── gfx/               # Sprite, spritesheet, đồ họa UI
│   ├── sounds/            # Âm thanh (.wav) và nhạc nền
│   └── fonts/             # Font bitmap pixel
│
└── levels/                # File dữ liệu layout màn chơi
```

---

## 🔧 Những cải tiến so với bản gốc

Dự án này mở rộng bản tham dự **LowRezJam 2022** gốc với các cải tiến sau:

<div align="center">

| # | Cải tiến | Mô tả |
|:---:|:---:|:---|
| 1 | 🚪 **Sửa lỗi cửa** | Cửa không còn bị khóa vĩnh viễn sau khi người chơi từ chối mở |
| 2 | 🖼️ **Ảnh kết thúc toàn màn hình** | Ảnh kết thúc điện ảnh hiển thị đúng kích thước toàn màn hình |
| 3 | ⏸️ **Menu Pause** | Nhấn `ESC` để dừng — Chơi tiếp, Chơi lại hoặc về Màn hình chính |
| 4 | 📖 **Màn hình Hướng dẫn** | Hướng dẫn cuộn được trong game cho cả bàn phím lẫn cử chỉ |
| 5 | 🔢 **Sửa lỗi nhập đôi** | Nút số trên bàn phím số không còn đăng ký hai lần mỗi lần nhấn |
| 6 | 🎲 **Mã cheat** | `G+H` (hồi máu) và `G+T` (minigun) để thử nghiệm |
| 7 | 🔥 **Vũ khí Minigun** | Thêm vũ khí bắn nhanh mới vào hệ thống vật phẩm |
| 8 | 🧹 **Chất lượng code** | Cải thiện quản lý trạng thái, luồng điều khiển rõ ràng hơn |

</div>

---

## 👥 Tác giả & Đóng góp

<div align="center">

| Vai trò | Người đóng góp |
|:---:|:---:|
| 💻 Lập trình (Bản gốc) | [Baconinvader](https://github.com/Baconinvader) |
| 🎨 Đồ họa (Bản gốc) | Ghast |
| 🔧 Cải tiến & Sửa lỗi | [khanhly-dn](https://github.com/khanhly-dn) |
| 🤝 Đồng phát triển | Trần Hải Long |

</div>

---

## 🏆 Game Jam

Dự án này ban đầu được tạo ra cho **[LowRezJam 2022](https://itch.io/jam/lowrezjam2022)** — cuộc thi game jam nơi tất cả các trò chơi phải vừa trong độ phân giải 64×64 pixel.

Repository gốc: [github.com/Baconinvader/LowRez2022](https://github.com/Baconinvader/LowRez2022)

---

## 📄 Giấy phép

Dự án này là mã nguồn mở theo [Giấy phép MIT](LICENSE).  
Trò chơi gốc © 2022 Baconinvader & Ghast — được mở rộng với sự tôn trọng đối với các tác giả ban đầu.

---

<div align="center">

*Được xây dựng bằng Python + Pygame*  
*"Hãy sinh tồn trên trạm. Đừng tin vào bóng tối."*

</div>
