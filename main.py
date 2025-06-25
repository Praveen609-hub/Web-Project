import cv2
import mediapipe as mp
import pyautogui

# Setup
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
drawing_utils = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

# Previous coordinates for smooth movement
prev_x, prev_y = 0, 0
smooth_factor = 0.2

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hand_detector.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Get index and middle finger tips
            index = hand_landmarks.landmark[8]
            middle = hand_landmarks.landmark[12]

            # Get pixel position for index finger
            x = int(index.x * frame.shape[1])
            y = int(index.y * frame.shape[0])

            # Convert to screen coordinates
            screen_x = int(index.x * screen_w)
            screen_y = int(index.y * screen_h)

            # Smooth movement
            curr_x = prev_x + (screen_x - prev_x) * smooth_factor
            curr_y = prev_y + (screen_y - prev_y) * smooth_factor
            pyautogui.moveTo(curr_x, curr_y)
            prev_x, prev_y = curr_x, curr_y

            # Scroll detection (vertical distance between fingers)
            scroll_diff = int((middle.y - index.y) * frame.shape[0])

            if abs(scroll_diff) > 40:
                if scroll_diff > 0:
                    pyautogui.scroll(-20)  # Scroll down
                else:
                    pyautogui.scroll(20)   # Scroll up

            # Click if fingers are very close
            distance = abs(index.y - middle.y)
            if distance < 0.03:
                pyautogui.click()

            # Draw pointer
            cv2.circle(frame, (x, y), 8, (255, 0, 0), cv2.FILLED)

    cv2.imshow("Virtual Mouse with Scroll", frame)

    # Exit on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
