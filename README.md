# **Virtual Hand-Tracking Keyboard using OpenCV, CVZone & Mediapipe**

This project implements a **virtual keyboard controlled entirely by hand
gestures** using a webcam.\
It detects your index and middle finger positions, highlights keys when
you hover over them, and registers a key press when you *pinch* your
fingers together.

The system uses: - **OpenCV** -- for video capture and display\
- **CVZone + Mediapipe** -- for hand tracking\
- **Pynput** -- to simulate real keyboard input\
- **Custom UI** -- dynamic virtual keyboard interface

------------------------------------------------------------------------

##  **Features**

### ✔ Hand-gesture-based typing

-   Use **index finger** to hover\
-   Perform a **pinch gesture** (index & middle finger distance \<
    threshold) to click the key

### ✔ Dynamic virtual keyboard layout

Includes: - QWERTY keys\
- Space\
- Backspace\
- Enter

### ✔ Real-time visual feedback

-   Key lighting and color change when pressed\
-   Fingertip pulse animation for a natural click feel\
-   FPS counter

### ✔ Real keyboard press simulation

Uses `pynput.Controller()` to trigger actual key presses on your system.

------------------------------------------------------------------------

## 🛠️ **Tech Stack**

  Technology            Purpose
  --------------------- ---------------------------
  Python                Implementation
  OpenCV                Webcam & UI drawing
  CVZone HandTracking   Hand detection & tracking
  Mediapipe             Landmark extraction
  Pynput                Virtual key presses

------------------------------------------------------------------------

## **Installation**

###  **Clone the repository**

``` bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

###  **Install required packages**

``` bash
pip install opencv-python cvzone mediapipe pynput
```

###  **Run the script**

``` bash
python your_script_name.py
```

------------------------------------------------------------------------

##  **How to Use**

1.  Start the program --- your webcam will open.
2.  Hold your **hand in front of the camera**.
3.  Move your **index finger** to hover over a key.
4.  **Pinch** your index & middle fingers to select the key.
5.  Typed text appears in the preview bar at the bottom.
6.  Press **Q** to quit (window active).

------------------------------------------------------------------------

##  **How It Works**

###  Hand Landmark Detection

Using CVZone (powered by Mediapipe), it reads: - Index fingertip
(landmark 8)\
- Middle fingertip (landmark 12)

###  Click Detection

``` python
length = euclid_dist(index_tip, middle_tip)
if length < PINCH_THRESHOLD:
    # register key press
```

###  Button Mapping

Each key is defined with: - Position (x, y) - Size (w, h) - Label (text)

All keys render dynamically using OpenCV's drawing functions.

###  Keyboard Input

`pynput` triggers system keystrokes when a virtual key is pressed.

------------------------------------------------------------------------

##  **Project Structure**

    │── virtual_keyboard.py        # Main script
    │── README.md                  # Project documentation
    └── assets/ (optional)         # Store screenshots/video

------------------------------------------------------------------------

##  Future Improvements

-   Add multi-language keyboard\
-   Add numeric keypad\
-   Sound feedback for each key\
-   Predictive text using NLP\
-   Full-screen mode UI

------------------------------------------------------------------------

##  License

This project is open-source and free to use under the **MIT License**.

------------------------------------------------------------------------

## Author

**Sai Charan Reddy**
** Tharun Rao **
**Chandrakala **
