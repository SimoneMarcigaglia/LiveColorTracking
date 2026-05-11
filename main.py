import cv2
import numpy as np
from PIL import Image

def get_limits(RGBColor):
    c = np.uint8([[RGBColor]])
    HSVColor = cv2.cvtColor(c, cv2.COLOR_RGB2HSV)

    hue = HSVColor[0][0][0]

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 10:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
        
    return lowerLimit, upperLimit


cap = cv2.VideoCapture(0)
trackedColor = (255, 255, 0)  # yellow color in RGB

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_limit, upper_limit = get_limits(trackedColor)  
    mask = cv2.inRange(hsvFrame, lower_limit, upper_limit)

    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (w, h), (0, 0, 255), 1)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()