# 🖐️ GestureSense

**Dual-Hand Gesture-Based Laptop Controller — Real-time spatial tracking for touchless monitor brightness and master audio volume control.**

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8.svg?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-007ACC.svg?style=flat-square&logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-0078D6.svg?style=flat-square&logo=windows&logoColor=white)](https://microsoft.com/windows)
[![Architecture](https://img.shields.io/badge/Architecture-Dual--Hand%20Spatial-success.svg?style=flat-square)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)

---

## 💡 What is GestureSense?

**GestureSense** is a high-performance computer vision system that turns your standard laptop webcam into an intuitive touchless controller. Utilizing Google MediaPipe's high-fidelity hand landmarker model and OpenCV, GestureSense enables independent, simultaneous adjustment of system volume and screen brightness using natural hand gestures.

- **Independent Dual-Hand Control:** Left hand controls monitor backlight brightness; right hand controls master audio gain.
- **Palm-Normalized Spatial Dynamics:** Calculates Euclidean distance between thumb and index fingertips normalized against palm size (wrist to middle MCP), ensuring consistent sensitivity regardless of hand distance from the webcam.
- **Pinky State Lock:** Raise your pinky finger above the PIP joint to instantly freeze the current setting, preventing unintended drift when resting or moving hands.
- **Exponential Moving Average (EMA) Filtering:** Applies algorithmic smoothing ($a = 0.15$) to eradicate sensor noise and produce fluid level transitions.
- **Dark-Mode Visual HUD:** Minimalist, high-contrast overlay displaying live percentage metrics, dynamic fill bars, and hand presence indicators.
- **Windows 11 Code Integrity Compliant:** Configured with verified MediaPipe binaries to prevent Windows Smart App Control (SAC) policy blocks (`WinError 4551`).

```
┌─────────────────────────────────┐
│     Live Webcam Stream (720p)   │
└────────────────┬────────────────┘
                 │ Frame Capture & Mirroring (cv2)
                 ▼
┌─────────────────────────────────┐
│ MediaPipe HandLandmarker Model  │
│  (21 3D Landmarks per Hand)     │
└────────┬────────────────┬───────┘
         │                │
   [Left Hand]      [Right Hand]
         │                │
         ▼                ▼
┌─────────────────┐┌─────────────────┐
│  Brightness     ││  Volume         │
│  Spatial Engine ││  Spatial Engine │
└────────┬────────┘└────────┬────────┘
         │                  │
         ▼                  ▼
┌─────────────────┐┌─────────────────┐
│ Screen Brightness││ Windows Core   │
│ Control (DDC/CI)││ Audio (Pycaw)   │
└─────────────────┘└─────────────────┘
```

---

## 🎮 Gesture Control & Interaction Matrix

```
       LEFT HAND (Brightness)                       RIGHT HAND (Volume)
   ┌───────────────────────────────┐           ┌───────────────────────────────┐
   │  Pinch (Thumb + Index):  0%   │           │  Pinch (Thumb + Index):  0%   │
   │  Spread (Thumb + Index): 100% │           │  Spread (Thumb + Index): 100% │
   │  Pinky Up: Lock Brightness    │           │  Pinky Up: Lock Volume        │
   │  Pinky Down: Unlock Control   │           │  Pinky Down: Unlock Control   │
   └───────────────────────────────┘           └───────────────────────────────┘
```

| Hand | Gesture | Action | Operational Mechanism | Level Dynamics |
| :--- | :--- | :--- | :--- | :--- |
| **Left Hand** | **Pinch** (Thumb + Index) | **Decrease Brightness** | Normalized ratio $< 0.20$ | Decreases down to 0% |
| **Left Hand** | **Spread** (Thumb + Index) | **Increase Brightness** | Normalized ratio up to $1.00$ | Increases up to 100% |
| **Left Hand** | **Pinky Raised** (Tip above PIP) | **Lock Brightness** | Threshold $\ge 5$ frames | Holds current level steady |
| **Left Hand** | **Pinky Lowered** | **Unlock Brightness** | Resumes active tracking | Dynamically tracks gestures |
| **Right Hand** | **Pinch** (Thumb + Index) | **Decrease Volume** | Normalized ratio $< 0.20$ | Lowers master audio volume |
| **Right Hand** | **Spread** (Thumb + Index) | **Increase Volume** | Normalized ratio up to $1.00$ | Raises master audio volume |
| **Right Hand** | **Pinky Raised** (Tip above PIP) | **Lock Volume** | Threshold $\ge 5$ frames | Holds current level steady |
| **Right Hand** | **Pinky Lowered** | **Unlock Volume** | Resumes active tracking | Dynamically tracks gestures |
| **Keyboard** | **Press `Q`** | **Exit Application** | Releases capture device | Safe window teardown |

---

## 📊 Comparison With Traditional Laptop Controls

| Capability | Hardware Fn Keys | Touchpad Gestures | Single-Hand CV Tools | 🖐️ GestureSense |
| :--- | :---: | :---: | :---: | :---: |
| **Touchless / Hands-Free Operation** | ❌ (Physical contact) | ❌ (Physical contact) | ✅ | ✅ **Full dual-hand spatial** |
| **Simultaneous Volume + Brightness** | ❌ (Sequential keypresses) | ❌ (Single focus) | ❌ (One parameter) | ✅ **Concurrent dual tracking** |
| **Distance Invariance (Palm Sizing)** | N/A | N/A | ❌ (Raw pixel dist) | ✅ **Normalized Euclidean ratio** |
| **Accidental Drift Prevention** | N/A | N/A | ❌ (Constant drift) | ✅ **Dedicated Pinky Lock** |
| **Windows 11 SAC / Code Integrity** | N/A | N/A | ❌ (WinError 4551) | ✅ **Validated binaries** |
| **Zero Cloud Telemetry** | ✅ | ✅ | ⚠️ (Some require cloud) | ✅ **100% Local execution** |

---

## 📁 Project Directory Structure

```text
GestureSense/
├── combined_controller_clean.py   # Main computer vision pipeline & Windows API integrations
├── hand_landmarker.task           # Pretrained MediaPipe hand landmark detection model
├── requirements.txt               # Pinned package dependencies (with SAC compliance)
├── run.bat                        # One-click Windows virtual environment launcher
├── .gitignore                     # Strict exclusion rules (zero secrets / venv isolation)
└── README.md                      # Comprehensive technical architecture & documentation
```

---

## 🚀 Installation & Quick Start

### Prerequisites
- **Operating System:** Windows 10 or Windows 11 (64-bit)
- **Python Version:** Python 3.10 or 3.11
- **Hardware:** Laptop integrated webcam or external USB camera

### 1. Clone the Repository
```bash
git clone https://github.com/Tharun4743/GestureSense.git
cd GestureSense
```

### 2. Set Up Virtual Environment & Dependencies
```powershell
# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> 🛡️ **Windows 11 Note:** `requirements.txt` strictly pins `mediapipe==0.10.14` to ensure binary signatures comply with Windows 11 Smart App Control (SAC) and prevent `[WinError 4551]` policy rejections.

---

## 🎬 Running the Application

### Option A: One-Click Windows Launcher (Recommended)
Double-click `run.bat` in the project root directory or run:
```cmd
run.bat
```

### Option B: Terminal Execution
```powershell
.\.venv\Scripts\activate
python combined_controller_clean.py
```

*Press **`Q`** at any time while the window is focused to exit cleanly.*

---

## ⚙️ Configuration & Engineering Tuning

Key parameters in `combined_controller_clean.py` can be tuned for your environment:

```python
CAMERA_INDEX = 0             # Camera ID (use 1 or 2 for external USB webcams)
MIN_RATIO = 0.20             # Pinch distance threshold representing 0%
MAX_RATIO = 1.00             # Spread distance threshold representing 100%
SMOOTHING_FACTOR = 0.15      # Exponential Moving Average factor (0.01 - 1.0)
LOCK_THRESHOLD = 5           # Minimum consecutive frames to engage pinky lock
BRIGHTNESS_UPDATE_DELAY = 0.08  # Cooldown rate-limiter for screen brightness API
VOLUME_UPDATE_THRESHOLD = 0.005 # Sensitivity delta required to trigger volume write
```

---

## 🛡️ Security, Privacy & Performance

- **100% Local Processing:** Video frames are processed entirely in volatile memory and immediately discarded. No video, images, or biometric features are ever stored to disk or transmitted over the network.
- **Hardware Efficiency:** Utilizes lightweight CPU-optimized inference with MediaPipe's TFLite framework, running at steady real-time 30+ FPS on standard laptop processors.
- **Protected API Calls:** Throttles DDC/CI monitor commands and Core Audio COM calls to prevent I/O saturation and eliminate UI stutter.

---

## 👨‍💻 Author & Engineering Credentials

<table border="0" itemscope itemtype="https://schema.org/Person">
  <tr>
    <td width="130" align="center" valign="middle">
      <img src="https://github.com/Tharun4743.png" width="105" style="border-radius: 6px;" alt="Tharunkumar K — Full Stack Developer & AI Systems Engineer at V.S.B. Engineering College" title="Tharunkumar K — V.S.B. Engineering College (VSBEC)" itemprop="image" />
    </td>
    <td>
      <h3 itemprop="name">Tharunkumar K</h3>
      <p>
        <b itemprop="jobTitle">Full Stack Developer & AI Systems Engineer</b> | <b>V.S.B. Engineering College (VSBEC)</b><br/>
        🎓 <b>B.Tech in Information Technology</b> — <b>V.S.B. Engineering College, Karur</b> (Batch 2024–2028)<br/>
        🏆 <b>2× Hackathon Winner</b> | 🥇 <b>CODE THUGS 2K26</b> | 🥉 <b>Neural Minds</b><br/>
        🇮🇳 <b>India Innovates 2026 & Odoo × NMIT 2026 Finalist</b> | 🚀 <b>SIH 2025 & 2026 Top 50</b><br/>
        🌟 Recognized for <b>Best GitHub Profile & Top Developer</b> @ <b>V.S.B. ENGINEERING COLLEGE</b>
      </p>
      <p>
        🚀 <b>Top Flagship Engineering Projects:</b><br/>
        • 🏛️ <b>TaskManager (VSBEC IT Vault)</b> — Institutional Task Governance & LeetCode/GitHub Sync &nbsp;<a href="https://github.com/Tharun4743/Taskmanager"><img src="https://img.shields.io/badge/Code-181717?style=flat-square&logo=github&logoColor=white" alt="Code" /></a>&nbsp;<a href="https://it-taskmanager.vercel.app/"><img src="https://img.shields.io/badge/Live_Demo-10B981?style=flat-square&logo=vercel&logoColor=white" alt="Live Demo" /></a><br/>
        • 🧠 <b>TK-Vault</b> — Sovereign Document Intelligence & Air-Gapped RAG Engine &nbsp;<a href="https://github.com/Tharun4743/TK-Vault"><img src="https://img.shields.io/badge/Code-181717?style=flat-square&logo=github&logoColor=white" alt="Code" /></a><br/>
        • ⚡ <b>TK Code Studio</b> — Visual In-Browser Live Editing Studio for Web Apps &nbsp;<a href="https://github.com/Tharun4743/TK_CodeStudio"><img src="https://img.shields.io/badge/Code-181717?style=flat-square&logo=github&logoColor=white" alt="Code" /></a><br/>
        • 🪖 <b>Smart Helmet IoT</b> — SIH Top 50 Dual-Unit Motorcycle Accident Prevention System &nbsp;<a href="https://github.com/Tharun4743/SmartHelmet-IoT"><img src="https://img.shields.io/badge/Code-181717?style=flat-square&logo=github&logoColor=white" alt="Code" /></a>
      </p>
      <p>
        <a href="https://tharunkumark4743.netlify.app/"><img src="https://img.shields.io/badge/Portfolio-0284c7?style=flat-square&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>&nbsp;
        <a href="https://github.com/Tharun4743"><img src="https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>&nbsp;
        <a href="https://www.linkedin.com/in/tharunkumark4743"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>&nbsp;
        <a href="https://leetcode.com/u/Tharunkumar__K/"><img src="https://img.shields.io/badge/LeetCode-FFA116?style=flat-square&logo=leetcode&logoColor=white" alt="LeetCode" /></a>&nbsp;
        <a href="mailto:tharunkumark42007@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
      </p>
    </td>
  </tr>
</table>

---

## 📄 License & Attribution

- Engineered and maintained by **Tharunkumar K** ([@Tharun4743](https://github.com/Tharun4743)).
- Released under the **MIT License**. Free for educational, research, and personal use.
