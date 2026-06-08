#2 driver


import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

# 1. Grab your physical webcam
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

print(f"Physical camera initialized at {width}x{height} @ {fps}FPS")

# 2. Write strictly to /dev/video4
with pyvirtualcam.Camera(width=width, height=height, fps=fps, device='/dev/video4', fmt=PixelFormat.RGB) as vcam:
    print(f"Virtual Camera Writer is active on: {vcam.device}")
    print("Press Ctrl+C to stop and modify code safely at any time.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Your custom text overlay
        cv2.putText(frame, "Himal fuchee bhaiiiii", (50, height - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            
        # Convert BGR (OpenCV) to RGB (Browser Standard)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        vcam.send(rgb_frame)
        vcam.sleep_until_next_frame()

cap.release()
print("Clean exit.")