import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller
from time import time
import math

# ----------------- Config -----------------
FRAME_W, FRAME_H = 1280, 720
DETECTION_CONFIDENCE = 0.8
MAX_HANDS = 2
PINCH_THRESHOLD = 45          # Distance to trigger click
# ------------------------------------------

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, FRAME_W)
cap.set(4, FRAME_H)

# Initialize detector and keyboard controller
detector = HandDetector(detectionCon=DETECTION_CONFIDENCE, maxHands=MAX_HANDS)
keyboard = Controller()

# Define keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    ["Z", "X", "C", "V", "B", "N", "M"],
    ["Space", "Backspace", "Enter"]
]

finalText = ""
pressed = False  # Tracks click state

# Button class
class Button:
    def _init_(self, pos, text, size=(85, 85)):
        self.pos = pos
        self.size = size
        self.text = text


# Build button layout dynamically
buttonList = []
keyboard_top = 120
y_spacing = 110
x_start = 160

for i, row in enumerate(keys):
    x = x_start
    for key in row:
        if key == "Space":
            w = 520
        elif key == "Backspace":
            w = 200
        elif key == "Enter":
            w = 200
        else:
            w = 90
        h = 85

        buttonList.append(Button([x, keyboard_top + i * y_spacing], key, size=(w, h)))
        x += w + 20  # dynamic horizontal spacing


# Draw all buttons
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + int(h * 0.7)),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    return img


# Euclidean distance
def euclid_dist(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


# Process key press
def processKeyPress(key):
    global finalText
    if key == "Space":
        finalText += " "
    elif key == "Backspace":
        finalText = finalText[:-1]
    elif key == "Enter":
        finalText += "\n"
    else:
        finalText += key

    try:
        if len(key) == 1:
            keyboard.press(key)
    except Exception:
        pass


# Main loop
pTime = 0
pulse_start_time = 0
pulse_duration = 0.2  # seconds for fingertip pulse animation

while True:
    success, img = cap.read()
    if not success:
        print("Camera not available.")
        break

    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    img = drawAll(img, buttonList)

    if hands:
        for hand in hands:
            lmList = hand.get("lmList", [])
            if not lmList or len(lmList) < 13:
                continue

            index_tip = lmList[8]
            middle_tip = lmList[12]
            length = euclid_dist(index_tip, middle_tip)

            # Default fingertip visuals
            fingertip_color = (255, 0, 0)
            fingertip_radius = 12

            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < index_tip[0] < x + w and y < index_tip[1] < y + h:
                    # Hover highlight
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5),
                                  (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + int(h * 0.7)),
                                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                    # ✅ Click detection (with press-release logic)
                    if length < PINCH_THRESHOLD and not pressed:
                        processKeyPress(button.text)
                        pressed = True
                        pulse_start_time = time()

                        # Visual feedback on button
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + int(h * 0.7)),
                                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

                        # Change fingertip to green (click indicator)
                        fingertip_color = (0, 255, 0)
                        fingertip_radius = 20

            # Reset pressed state once fingers separate again
            if length > PINCH_THRESHOLD + 20:
                pressed = False

            # 🟢 Finger pulse animation for a natural click feel
            if pressed and (time() - pulse_start_time) < pulse_duration:
                fingertip_radius = 22
            else:
                fingertip_radius = 12

            # Draw fingertips and connecting line
            cv2.circle(img, (index_tip[0], index_tip[1]), fingertip_radius, fingertip_color, cv2.FILLED)
            cv2.circle(img, (middle_tip[0], middle_tip[1]), fingertip_radius, fingertip_color, cv2.FILLED)
            cv2.line(img, (index_tip[0], index_tip[1]), (middle_tip[0], middle_tip[1]), fingertip_color, 3)

    # Typed text display
    cv2.putText(img, "Typed Text:", (100, FRAME_H - 140),
                cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
    cv2.rectangle(img, (100, FRAME_H - 120), (FRAME_W - 100, FRAME_H - 30), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText[-60:], (120, FRAME_H - 55),
                cv2.FONT_HERSHEY_PLAIN, 3.5, (255, 255, 255), 3)

    # FPS counter
    cTime = time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) else 0
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (FRAME_W - 150, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Virtual Keyboard (Two Hands)", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()