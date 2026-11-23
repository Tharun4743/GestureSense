
import cv2
import mediapipe as mp
import numpy as np
import math
import time

import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities


# =====================================================
# GESTURESENSE 2.0 | CONFIGURATION
# =====================================================

CAMERA_INDEX = 0

MIN_RATIO = 0.20
MAX_RATIO = 1.00

SMOOTHING_FACTOR = 0.15

LOCK_THRESHOLD = 5

BRIGHTNESS_UPDATE_DELAY = 0.08
VOLUME_UPDATE_THRESHOLD = 0.005

WINDOW_NAME = "GestureSense | Dual-Hand Controller"


# =====================================================
# 1. INITIALIZE SYSTEM CONTROLS
# =====================================================

print("\n" + "=" * 48)
print("       GESTURESENSE 2.0")
print("       Dual-Hand Laptop Controller")
print("=" * 48)

# Get current screen brightness
smooth_brightness = float(sbc.get_brightness()[0])

# Connect to Windows audio
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume

# Get current volume
smooth_volume = float(
    volume.GetMasterVolumeLevelScalar()
)

print(f"Brightness : {smooth_brightness:.0f}%")
print(f"Volume     : {smooth_volume * 100:.0f}%")

print("\nInitializing hand detection...")


# =====================================================
# 2. INITIALIZE MEDIAPIPE
# =====================================================

BaseOptions = mp.tasks.BaseOptions

HandLandmarker = mp.tasks.vision.HandLandmarker

HandLandmarkerOptions = (
    mp.tasks.vision.HandLandmarkerOptions
)

RunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path="hand_landmarker.task"
    ),

    running_mode=RunningMode.VIDEO,

    num_hands=2,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5
)


# =====================================================
# 3. APPLICATION STATE
# =====================================================

brightness_locked = False
volume_locked = False

left_lock_frames = 0
right_lock_frames = 0

previous_brightness_update = 0
previous_volume_update = smooth_volume

last_brightness_update_time = 0

start_time = time.monotonic()

print("GestureSense initialized successfully!\n")


# =====================================================
# 4. HAND CONNECTIONS
# =====================================================

connections = [

    (0, 1), (1, 2), (2, 3), (3, 4),

    (0, 5), (5, 6), (6, 7), (7, 8),

    (5, 9), (9, 10), (10, 11), (11, 12),

    (9, 13), (13, 14), (14, 15), (15, 16),

    (13, 17), (17, 18), (18, 19), (19, 20),

    (0, 17)
]


# =====================================================
# 5. DISTANCE CALCULATION
# =====================================================

def calculate_distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


# =====================================================
# 6. GESTURE RECOGNITION
# =====================================================

def recognize_gesture(hand):

    # Thumb and index fingertips
    thumb = hand[4]
    index = hand[8]

    # Palm reference points
    wrist = hand[0]
    middle_mcp = hand[9]

    # Calculate distances
    finger_distance = calculate_distance(
        thumb, index
    )

    palm_size = calculate_distance(
        wrist, middle_mcp
    )

    if palm_size < 0.001:
        return 0.0, 0.0, "UNKNOWN"

    # Normalize finger distance
    ratio = finger_distance / palm_size

    # Map normalized distance to 0-100%
    target = np.interp(
        ratio,
        [MIN_RATIO, MAX_RATIO],
        [0.0, 100.0]
    )

    target = float(
        np.clip(target, 0.0, 100.0)
    )

    # Identify gesture
    if ratio < MIN_RATIO:
        gesture = "PINCH"

    elif ratio > MAX_RATIO:
        gesture = "SPREAD"

    else:
        gesture = "ADJUSTING"

    return target, ratio, gesture


# =====================================================
# 7. PINKY DETECTION
# =====================================================

def is_pinky_up(hand):

    pinky_tip = hand[20]
    pinky_pip = hand[18]

    return pinky_tip.y < pinky_pip.y


# =====================================================
# 8. IDENTIFY HAND
# =====================================================

def identify_hand(result, hand_index):

    original_label = (
        result.handedness[hand_index][0].category_name
    )

    # Label correction based on webcam testing
    if original_label == "Left":
        return "Right"

    return "Left"


# =====================================================
# 9. DRAW HAND LANDMARKS
# =====================================================

def draw_hand(frame, hand, color):

    h, w, _ = frame.shape

    for start, end in connections:

        p1 = hand[start]
        p2 = hand[end]

        pt1 = (
            int(p1.x * w),
            int(p1.y * h)
        )

        pt2 = (
            int(p2.x * w),
            int(p2.y * h)
        )

        cv2.line(
            frame,
            pt1,
            pt2,
            color,
            2,
            cv2.LINE_AA
        )

    for landmark_id, point in enumerate(hand):

        x = int(point.x * w)
        y = int(point.y * h)

        if landmark_id in [4, 8, 20]:
            radius = 7
        else:
            radius = 4

        cv2.circle(
            frame,
            (x, y),
            radius,
            color,
            -1,
            cv2.LINE_AA
        )


# =====================================================
# 10. DRAW DASHBOARD PANEL
# =====================================================

def draw_panel(frame, x, y, width, height):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x, y),
        (x + width, y + height),
        (25, 30, 40),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.80,
        frame,
        0.20,
        0,
        frame
    )

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (90, 100, 115),
        1
    )


# =====================================================
# 11. DRAW PROGRESS BAR
# =====================================================

def draw_bar(frame, x, y, width, value, color):

    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + 12),
        (65, 70, 80),
        -1
    )

    fill_width = int(
        width * np.clip(value / 100, 0, 1)
    )

    if fill_width > 0:

        cv2.rectangle(
            frame,
            (x, y),
            (x + fill_width, y + 12),
            color,
            -1
        )


# =====================================================
# 12. START WEBCAM
# =====================================================

cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():

    raise RuntimeError(
        "Unable to access webcam. Check camera permissions."
    )

# Set webcam resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# =====================================================
# 13. MAIN APPLICATION
# =====================================================

try:

    with HandLandmarker.create_from_options(options) as landmarker:

        while True:

            success, frame = cap.read()

            if not success:
                print("Unable to capture webcam frame.")
                break

            # Mirror webcam
            frame = cv2.flip(frame, 1)

            h, w, _ = frame.shape

            # Convert BGR to RGB
            rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            # Create MediaPipe image
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb
            )

            # Generate timestamp
            timestamp = int(
                (time.monotonic() - start_time) * 1000
            )

            # Detect hands
            result = landmarker.detect_for_video(
                mp_image,
                timestamp
            )

            # Hand detection status
            left_detected = False
            right_detected = False

            # =================================================
            # 14. PROCESS DETECTED HANDS
            # =================================================

            if result.hand_landmarks:

                for hand_index, hand in enumerate(
                    result.hand_landmarks
                ):

                    label = identify_hand(
                        result,
                        hand_index
                    )

                    # Recognize gesture
                    target, ratio, gesture = recognize_gesture(hand)

                    # Detect pinky
                    pinky_up = is_pinky_up(hand)

                    # =================================================
                    # LEFT HAND - BRIGHTNESS
                    # =================================================

                    if label == "Left":

                        left_detected = True

                        if pinky_up:

                            left_lock_frames += 1

                        else:

                            left_lock_frames = 0

                        brightness_locked = (
                            left_lock_frames >= LOCK_THRESHOLD
                        )

                        if not brightness_locked:

                            target_brightness = target

                            smooth_brightness = (
                                (1 - SMOOTHING_FACTOR)
                                * smooth_brightness
                                +
                                SMOOTHING_FACTOR
                                * target_brightness
                            )

                            brightness_value = int(
                                np.clip(
                                    smooth_brightness,
                                    0,
                                    100
                                )
                            )

                            current_time = time.monotonic()

                            if (
                                brightness_value != previous_brightness_update
                                and current_time - last_brightness_update_time
                                >= BRIGHTNESS_UPDATE_DELAY
                            ):

                                sbc.set_brightness(
                                    brightness_value
                                )

                                previous_brightness_update = brightness_value

                                last_brightness_update_time = current_time

                        # Draw left hand
                        color = (
                            (0, 0, 255)
                            if brightness_locked
                            else (0, 220, 255)
                        )

                        draw_hand(frame, hand, color)

                    # =================================================
                    # RIGHT HAND - VOLUME
                    # =================================================

                    elif label == "Right":

                        right_detected = True

                        if pinky_up:

                            right_lock_frames += 1

                        else:

                            right_lock_frames = 0

                        volume_locked = (
                            right_lock_frames >= LOCK_THRESHOLD
                        )

                        if not volume_locked:

                            target_volume = target / 100.0

                            smooth_volume = (
                                (1 - SMOOTHING_FACTOR)
                                * smooth_volume
                                +
                                SMOOTHING_FACTOR
                                * target_volume
                            )

                            smooth_volume = float(
                                np.clip(
                                    smooth_volume,
                                    0.0,
                                    1.0
                                )
                            )

                            if (
                                abs(
                                    smooth_volume -
                                    previous_volume_update
                                ) >= VOLUME_UPDATE_THRESHOLD
                            ):

                                volume.SetMasterVolumeLevelScalar(
                                    smooth_volume,
                                    None
                                )

                                previous_volume_update = smooth_volume

                        # Draw right hand
                        color = (
                            (0, 0, 255)
                            if volume_locked
                            else (80, 220, 100)
                        )

                        draw_hand(frame, hand, color)

            # =================================================
            # 15. BRIGHTNESS DASHBOARD
            # =================================================

            panel_y = 100

            draw_panel(
                frame,
                20,
                panel_y,
                330,
                125
            )

            cv2.putText(
                frame,
                "BRIGHTNESS",
                (40, panel_y + 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 220, 255),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                f"{int(smooth_brightness)}%",
                (40, panel_y + 75),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            draw_bar(
                frame,
                40,
                panel_y + 95,
                270,
                smooth_brightness,
                (0, 220, 255)
            )

            brightness_status = (
                "LOCKED" if brightness_locked
                else "ACTIVE" if left_detected
                else "WAITING"
            )

            cv2.putText(
                frame,
                brightness_status,
                (220, panel_y + 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 0, 255) if brightness_locked
                else (100, 230, 130),
                1
            )

            # =================================================
            # 16. VOLUME DASHBOARD
            # =================================================

            draw_panel(
                frame,
                20,
                panel_y + 140,
                330,
                125
            )

            volume_percentage = int(
                smooth_volume * 100
            )

            cv2.putText(
                frame,
                "VOLUME",
                (40, panel_y + 170),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (100, 230, 130),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                f"{volume_percentage}%",
                (40, panel_y + 215),
                cv2.FONT_HERSHEY_DUPLEX,
                1.0,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            draw_bar(
                frame,
                40,
                panel_y + 235,
                270,
                volume_percentage,
                (100, 230, 130)
            )

            volume_status = (
                "LOCKED" if volume_locked
                else "ACTIVE" if right_detected
                else "WAITING"
            )

            cv2.putText(
                frame,
                volume_status,
                (220, panel_y + 175),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                (0, 0, 255) if volume_locked
                else (100, 230, 130),
                1
            )

            # =================================================
            # 17. HAND DETECTION STATUS
            # =================================================

            cv2.putText(
                frame,
                f"LEFT HAND: {'DETECTED' if left_detected else 'NOT DETECTED'}",
                (w - 340, h - 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 220, 255) if left_detected
                else (150, 150, 150),
                2
            )

            cv2.putText(
                frame,
                f"RIGHT HAND: {'DETECTED' if right_detected else 'NOT DETECTED'}",
                (w - 340, h - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (100, 230, 130) if right_detected
                else (150, 150, 150),
                2
            )

            # =================================================
            # 18. DISPLAY APPLICATION
            # =================================================

            cv2.imshow(
                WINDOW_NAME,
                frame
            )

            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


finally:

    # Release webcam
    cap.release()

    # Close OpenCV windows
    cv2.destroyAllWindows()

    print("\n" + "=" * 48)
    print("       GESTURESENSE CLOSED")
    print("=" * 48)
