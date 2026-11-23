# GestureSense 2.0 🖐️🎛️

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-007ACC?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6?logo=windows&logoColor=white)](https://microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**GestureSense** is a real-time computer vision application that turns your laptop webcam into a touchless controller. Using MediaPipe hand landmark tracking and OpenCV, GestureSense allows you to independently control your Windows laptop's **screen brightness** and **master audio volume** using dual-hand spatial gestures.

---

## ⚡ Key Features

- 🖐️ **Simultaneous Dual-Hand Tracking**: Processes both left and right hands concurrently in real-time.
- ☀️ **Left Hand &rarr; Screen Brightness**: Smoothly adjust monitor backlight level.
- 🔊 **Right Hand &rarr; System Volume**: Precision audio gain control via Windows Core Audio APIs (`pycaw`).
- 📏 **Palm-Normalized Pinch Dynamics**: Uses the Euclidean ratio between thumb & index fingertips normalized against palm size (wrist to middle MCP), ensuring consistent sensitivity regardless of how close or far your hand is from the camera.
- 🔒 **Pinky Gesture Lock**: Raise your pinky finger above the PIP joint to lock the current level in place—preventing accidental adjustments while repositioning.
- 📈 **Exponential Moving Average (EMA) Smoothing**: Eliminates jitter with dynamic interpolation for fluid adjustments.
- 🖥️ **Task-Manager Style HUD**: Sleek dark-mode overlay showing real-time feedback gauges, percentage readouts, and hand detection indicators.
- ⚡ **Windows 11 Code Integrity Ready**: Pre-configured with compatible MediaPipe binaries to avoid Smart App Control (SAC) policy blocks (`WinError 4551`).

---

## 🎮 Gesture Control Mapping

```
       LEFT HAND (Brightness)                       RIGHT HAND (Volume)
   ┌───────────────────────────────┐           ┌───────────────────────────────┐
   │  Pinch (Thumb + Index):  0%   │           │  Pinch (Thumb + Index):  0%   │
   │  Spread (Thumb + Index): 100% │           │  Spread (Thumb + Index): 100% │
   │  Pinky Up: Lock Brightness    │           │  Pinky Up: Lock Volume        │
   │  Pinky Down: Unlock Control   │           │  Pinky Down: Unlock Control   │
   └───────────────────────────────┘           └───────────────────────────────┘
```

| Gesture | Hand | Action | Description |
| :--- | :--- | :--- | :--- |
| **Pinch** (Thumb + Index close) | **Left Hand** | **Decrease Brightness** | Lower screen brightness down to 0% |
| **Spread** (Thumb + Index wide) | **Left Hand** | **Increase Brightness** | Raise screen brightness up to 100% |
| **Pinky Raised** (Tip above PIP) | **Left Hand** | **Lock Brightness** | Freezes brightness at current level |
| **Pinch** (Thumb + Index close) | **Right Hand** | **Decrease Volume** | Lower Windows audio volume |
| **Spread** (Thumb + Index wide) | **Right Hand** | **Increase Volume** | Increase Windows audio volume |
| **Pinky Raised** (Tip above PIP) | **Right Hand** | **Lock Volume** | Freezes master volume at current level |
| **Press `Q`** | Keyboard | **Exit** | Releases camera and closes interface safely |

---

## 📁 Project Architecture

```text
GestureSense/
├── combined_controller_clean.py   # Core controller logic, HUD rendering, & system APIs
├── hand_landmarker.task           # MediaPipe pretrained vision model asset
├── requirements.txt               # Pinned Python package dependencies
├── run.bat                        # One-click Windows batch launcher
├── .gitignore                     # Git ignore rules & security boundaries
└── README.md                      # Documentation & user guide
```

---

## 🚀 Quick Start & Installation

### Prerequisites
- **Operating System**: Windows 10 or Windows 11 (64-bit)
- **Python**: Version 3.10 or 3.11 installed
- **Hardware**: Integrated webcam or external USB camera

### 1. Clone the Repository
```bash
git clone https://github.com/Tharun4743/GestureSense.git
cd GestureSense
```

### 2. Set Up Virtual Environment & Dependencies

Using standard `pip` or modern fast `uv`:

```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Note on MediaPipe version**: `mediapipe==0.10.14` is specifically pinned in `requirements.txt` to guarantee compatibility with Windows 11 Smart App Control (SAC) and prevent `[WinError 4551]` policy rejections.

---

## 🎬 Running GestureSense

### Option A: One-Click Launcher (Windows)
Double-click `run.bat` in the project root directory.

### Option B: Terminal Execution
```powershell
# Activate venv if not already active
.\.venv\Scripts\activate

# Launch controller
python combined_controller_clean.py
```

Press **`Q`** at any time to exit cleanly.

---

## ⚙️ Configuration & Customization

You can tune performance, camera resolution, and responsiveness directly in `combined_controller_clean.py`:

```python
CAMERA_INDEX = 0             # Change to 1 or 2 if using an external USB webcam
MIN_RATIO = 0.20             # Pinch ratio threshold for 0%
MAX_RATIO = 1.00             # Spread ratio threshold for 100%
SMOOTHING_FACTOR = 0.15      # EMA smoothing factor (lower = smoother, higher = faster)
LOCK_THRESHOLD = 5           # Consecutive frames required to engage gesture lock
BRIGHTNESS_UPDATE_DELAY = 0.08  # Rate-limiting cooldown for screen brightness API
VOLUME_UPDATE_THRESHOLD = 0.005 # Minimum volume delta required to trigger OS change
```

---

## 🛠️ Troubleshooting

- **`WinError 4551` (Application Control policy blocked this file)**:
  - This occurs if Windows 11 Smart App Control (SAC) blocks dynamically loaded unsigned C++ libraries from unverified packages. GestureSense resolves this by pinning `mediapipe==0.10.14`.
- **Webcam Access Error (`Unable to access webcam`)**:
  - Ensure Windows Camera Privacy Settings allow desktop apps to access the camera (*Settings &rarr; Privacy & Security &rarr; Camera*).
  - Verify that no other application (Zoom, Teams, Discord) is currently holding an exclusive lock on the camera.
  - If using an external camera, set `CAMERA_INDEX = 1` in `combined_controller_clean.py`.
- **Brightness Control Not Changing External Monitor**:
  - `screen-brightness-control` communicates over DDC/CI or Windows WMI. External HDMI/DisplayPort monitors may require DDC/CI enabled in their physical on-screen display (OSD) settings.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
