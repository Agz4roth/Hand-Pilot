import cv2
import mediapipe as mp
import pyautogui
import time
import math
import pyttsx3

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)


def speak(text):
    engine.say(text)
    engine.runAndWait()


# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

finger_tips = [4, 8, 12, 16, 20]


def get_finger_states(lm):
    states = []
    states.append(1 if lm[4].x < lm[3].x else 0)  # Thumb
    for tip in finger_tips[1:]:
        base = tip - 2
        states.append(1 if lm[tip].y < lm[base].y else 0)
    return states


def is_fist(states):
    return sum(states) == 0


def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def recognize_custom_gestures(lm, states):
    thumb_tip = lm[4]
    index_tip = lm[8]
    pinky_tip = lm[20]
    wrist = lm[0]

    if states == [0, 1, 1, 0, 0]:
        return "Victory"
    if states == [1, 0, 0, 0, 0] and thumb_tip.y < wrist.y:
        return "Like"
    if states == [1, 0, 0, 0, 0] and thumb_tip.y > wrist.y:
        return "Dislike"
    if distance(thumb_tip, index_tip) < 0.05 and states[2:] == [1, 1, 1]:
        return "OK"
    if states == [1, 0, 0, 0, 1]:
        return "Call Me"
    if states == [0, 1, 0, 0, 1]:
        return "Devil Horns"
    if sum(states) == 5 and abs(lm[5].x - lm[17].x) > 0.2:
        return "Stop"
    if states == [0, 1, 0, 0, 0]:
        return "Pointing"
    return None


def get_finger_count(states):
    return sum(states)


prev_x = None
gesture_cooldown = 0
scroll_mode = False
scroll_last = 0

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_counter = 0
process_interval = 5  # Process every 5 frames

while True:
    time.sleep(0.05)  # Add slight delay to reduce processing load

    success, frame = cap.read()
    if not success:
        break

    frame_counter += 1
    if frame_counter % process_interval != 0:  # Skip some frames
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    h, w, _ = frame.shape
    cx = None
    now = time.time()

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm = handLms.landmark
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            cx = int(lm[0].x * w)
            states = get_finger_states(lm)

            custom_gesture = recognize_custom_gestures(lm, states)
            if custom_gesture:
                speak(custom_gesture)
                cv2.putText(frame, custom_gesture, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 255), 3)

            finger_count = get_finger_count(states)
            if 1 <= finger_count <= 5:
                cv2.putText(frame, f"Number: {finger_count}", (10, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                
                speak(f"Number {finger_count}")

            if is_fist(states) and lm[4].y < lm[3].y:
                cv2.putText(frame, "Start Slideshow", (10, 140),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
                pyautogui.press("f5")
                speak("Start Slideshow")
                time.sleep(1)

            elif not is_fist(states) and states == [0, 1, 0, 0, 0]:
                scroll_mode = True
                dy = lm[8].y - lm[6].y
                if now - scroll_last > 0.5:
                    if dy < -0.03:
                        pyautogui.scroll(300)
                        speak("Scrolling Up")
                        scroll_last = now
                    elif dy > 0.03:
                        pyautogui.scroll(-300)
                        speak("Scrolling Down")
                        scroll_last = now
                cv2.putText(frame, "Scroll Mode", (10, 180),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
            else:
                scroll_mode = False

            if cx is not None and prev_x is not None and now - gesture_cooldown > 1.0:
                delta = cx - prev_x
                if abs(delta) > 100:
                    if delta > 0:
                        pyautogui.press("left")
                        speak("Previous Slide")
                        cv2.putText(frame, "Previous Slide", (10, 220),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    else:
                        pyautogui.press("right")
                        speak("Next Slide")
                        cv2.putText(frame, "Next Slide", (10, 220),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                    gesture_cooldown = now

            prev_x = cx

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()