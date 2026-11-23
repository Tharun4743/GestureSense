# GestureSense 
### A Dual-Hand Gesture-Based Laptop Controller

GestureSense is a Python-based computer vision application that allows users to control laptop brightness and system volume using hand gestures captured through a webcam.

## Features

- Control screen brightness using the left hand.
- Control system volume using the right hand.
- Increase or decrease levels using thumb-index finger distance.
- Lock individual controls by raising the corresponding pinky finger.
- Track both hands simultaneously in real time.
- Display real-time brightness, volume, and hand-detection status on an interactive HUD.

## Gesture Controls

| Hand | Gesture | Action |
|---|---|---|
| **Left Hand** | Pinch thumb and index finger | Decrease screen brightness |
| **Left Hand** | Spread thumb and index finger | Increase screen brightness |
| **Left Hand** | Raise pinky finger | Lock current screen brightness |
| **Left Hand** | Lower pinky finger | Unlock screen brightness |
| **Right Hand** | Pinch thumb and index finger | Decrease system volume |
| **Right Hand** | Spread thumb and index finger | Increase system volume |
| **Right Hand** | Raise pinky finger | Lock current system volume |
| **Right Hand** | Lower pinky finger | Unlock system volume |

## Technologies Used

- **Python** (3.10 / 3.11)
- **OpenCV** – Webcam capture, image processing, and visual HUD
- **MediaPipe** – Real-time multi-hand landmark detection
- **NumPy** – Numerical operations and exponential smoothing
- **Pycaw** – Windows Core Audio API volume control
- **Screen Brightness Control** – Monitor backlight adjustment

## Project Structure

```text
GestureSense/
│
├── combined_controller_clean.py
├── hand_landmarker.task
├── requirements.txt
├── run.bat
├── .gitignore
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Tharun4743/GestureSense.git
cd GestureSense
```

2. Create and activate a Python virtual environment:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure `hand_landmarker.task` is in the project directory.

## Run the Application

You can launch the application in two ways:

### Option 1: Using the Batch Launcher (Windows)
Double-click `run.bat` or run:

```cmd
run.bat
```

### Option 2: Using Python
```bash
python combined_controller_clean.py
```

Press **Q** while the webcam window is active to close the application.

## Platform

Designed for Windows 10 and Windows 11 laptops with a built-in or USB webcam.

## Future Enhancements

- Gesture-based media controls (play, pause, next track).
- Customizable gesture sensitivity and smoothing sliders.
- Support for multi-monitor setups.
- Additional accessibility shortcuts and profiles.

---

**GestureSense — Control your laptop with gestures.**
