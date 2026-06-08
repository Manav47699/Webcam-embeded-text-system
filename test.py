import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

# 1. Grab physical webcam
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

print(f"Physical camera initialized at {width}x{height} @ {fps}FPS")

# 2. Change 'fmt' to PixelFormat.RGB (Browsers love standard RGB)
with pyvirtualcam.Camera(width=width, height=height, fps=fps, device='/dev/video4', fmt=PixelFormat.RGB) as vcam:
    print(f"Virtual Camera is LIVE on: {vcam.device}")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # 1. Inject the text onto the raw frame FIRST
        cv2.putText(frame, "Himal fuchee bhaiiiii", (50, height - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
        
        # 2. NOW flip the entire combined frame horizontally (1 means horizontal flip)
        # This mirrors both your face AND the text together, so the browser un-flips both perfectly!
        frame = cv2.flip(frame, 1)
            
        # Convert BGR (OpenCV standard) to RGB (Browser standard)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        vcam.send(rgb_frame)
        vcam.sleep_until_next_frame()

cap.release()