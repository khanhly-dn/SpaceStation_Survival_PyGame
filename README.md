# 🚀 SpaceStation Survival — Necrostation

> A 64×64 pixel Sci-Fi survival shooter built with **Python & Pygame**  
> Originally a **LowRezJam 2022** entry — expanded, upgraded, and enhanced.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?logo=windows)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📸 Screenshots

| Main Menu | Gameplay | Pause Menu |
|-----------|----------|------------|
| ![menu](res/gfx/space_background.png) | *(in-game)* | *(ESC to pause)* |

---

## 🎮 About the Game

**Necrostation** is a retro-style top-down survival shooter set aboard a derelict space station overrun by alien creatures. You play as a lone astronaut fighting through multiple rooms, managing a limited inventory of weapons, solving keypad puzzles, and trying to survive long enough to reach the end.

The game renders at an internal resolution of **64×64 pixels** (upscaled to fit the window), giving it a distinctive lo-fi pixel-art aesthetic inspired by classic 8-bit games.

---

## ✨ Features

### 🕹️ Core Gameplay
- **Multi-room level exploration** — navigate through interconnected rooms via interactive doors
- **Real-time combat** — shoot, punch, and dodge enemies with fluid controls
- **Inventory system** — pick up and switch between multiple weapon types (8 slots)
- **Keypad puzzles** — enter codes to unlock secured doors
- **Enemy AI** — various creature types including large boss-like enemies
- **Health & damage system** — visual damage overlays and death animations
- **Corpse system** — enemies and player leave behind corpses

### 🔫 Weapons
| Weapon | Type | Notes |
|--------|------|-------|
| Handgun | Pistol | Balanced, reliable |
| Shotgun | Spread | High spread, close-range |
| Stungun | Special | Stuns enemies |
| Revolver | Pistol | High damage, slow fire |
| Minigun | Heavy | Rapid fire, cheat-unlockable |

### 🖥️ Input Modes
- **Keyboard & Mouse** — traditional PC controls
- **Gesture / Visual (Webcam)** — control the game using hand gestures via webcam (AI-powered)

### 🎬 Game Screens
- **Main Menu** with animated space background
- **How To Play** screen with scrollable controls guide (keyboard + gesture)
- **Pause Menu** (ESC) — Resume / Restart / Main Menu
- **Cinematic end sequence** with full-screen illustrated slides
- **Game Over** screen

---

## 🧑‍💻 Technical Highlights

| Feature | Implementation |
|---------|---------------|
| Rendering | Custom camera system with world-to-screen transforms |
| Collision | Pixel-perfect mask collision + AABB |
| Animation | Spritesheet-based animation system with ping-pong support |
| Actions | Pipe-based action queue (tweening, function calls, overlays) |
| Particles | Custom particle emitter (smoke, flash, stun effects) |
| Sound | Pygame mixer with named sound management |
| Gesture | Real-time hand landmark detection via webcam |
| Serialization | Custom pickle/unpickle system for Pygame surfaces |

---

## 🕹️ Controls

### Keyboard & Mouse

| Key | Action |
|-----|--------|
| `A` / `D` | Move left / right |
| `Left Click` | Attack / Fire |
| `Right Click` | Interact with object |
| `E` / `Space` | Interact with nearest object |
| `I` | Open / close inventory |
| `1` – `8` | Select item slot |
| `Scroll Wheel` | Scroll text |
| `ESC` | Pause game |

### Gesture Mode (Webcam)

| Gesture | Action |
|---------|--------|
| Open hand | Move pointer |
| Fist | Attack |
| Index finger up | Interact |
| Thumbs up | Next item |
| Thumbs down | Previous item |
| Peace sign ✌️ | Open inventory |
| `F2` | Toggle gesture mode |

### 🎲 Cheat Codes

| Keys | Effect |
|------|--------|
| `G` + `H` | Restore full health |
| `G` + `T` | Unlock Minigun |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/khanhly-dn/SpaceStation_Survival_PyGame.git
cd SpaceStation_Survival_PyGame

# Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Run the Game

```bash
python main.py
```

> **Note:** Gesture mode requires a working webcam. Press `F2` in-game to toggle.

---

## 📁 Project Structure

```
SpaceStation_Survival_PyGame/
│
├── main.py              # Entry point, game loop, input handling
├── controls.py          # UI controls: buttons, popups, menus, HUD
├── creatures.py         # Enemy and creature AI
├── players.py           # Player logic, inventory, weapons
├── levels.py            # Level management, doors, structures
├── entities.py          # Base entity class with collision
├── items.py             # Weapon and item definitions
├── actions.py           # Action/tween pipeline system
├── particles.py         # Particle effects
├── cameras.py           # Camera and world-to-screen transforms
├── graphics.py          # Image loading, animation, text rendering
├── sounds.py            # Sound management
├── arteffects.py        # Screen effects and post-processing
├── gesture_input.py     # Webcam gesture recognition
├── global_values.py     # Shared game state
├── elements.py          # Base element/control registry
├── utilities.py         # Math helpers (angle, distance, lerp)
│
├── res/
│   ├── gfx/             # Sprites, spritesheets, backgrounds
│   ├── sounds/          # Sound effects and music
│   └── fonts/           # Pixel fonts
│
└── levels/              # Level data files
```

---

## 🔧 Key Improvements Over Original

This fork extends the original **LowRezJam 2022** submission with:

- ✅ **Bug fix** — Door interaction state reset (doors no longer lock permanently after declining)
- ✅ **Full-screen end slides** — cinematic ending images now scale correctly to fill the screen
- ✅ **Pause Menu** — press ESC anytime to Resume / Restart / return to Main Menu
- ✅ **How To Play screen** — scrollable guide accessible from the main menu
- ✅ **Keypad double-input fix** — numeric buttons no longer register twice per press
- ✅ **Cheat codes** — G+H (heal) and G+T (minigun) for testing and fun
- ✅ **Minigun weapon** — new high-fire-rate weapon type added to the item system
- ✅ **Code quality** — improved state management, cleaner control flow

---

## 🏆 Original Game Jam

This project is based on **[Necrostation](https://github.com/Baconinvader/LowRez2022)** submitted to **LowRezJam 2022**.

| Role | Contributor |
|------|-------------|
| Programming (original) | [Baconinvader](https://github.com/Baconinvader) |
| Art (original) | Ghast |
| Enhancements & Bug Fixes | [khanhly-dn](https://github.com/khanhly-dn) |

---

## 📄 License

This project is open-source under the [MIT License](LICENSE).  
Original game © 2022 Baconinvader & Ghast — used and extended with respect to the original creators.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

*Built with ❤️ using Python + Pygame*
