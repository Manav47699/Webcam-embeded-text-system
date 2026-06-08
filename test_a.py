import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat
import subprocess
import sys
import time

DEVICE_PATH = '/dev/video4'

# --- AUTOMATIC DRIVER RESET WITH TIMING FIX ---
print("Resetting v4l2loopback driver for clean browser handshake...")
try:
    # 1. Kill any active processes holding onto the video device
    subprocess.run(['sudo', 'fuser', '-k', DEVICE_PATH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Force unload the kernel module
    subprocess.run(['sudo', 'rmmod', 'v4l2loopback'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Reload with strict browser-friendly flags
    subprocess.run(['sudo', 'modprobe', 'v4l2loopback', 'exclusive_caps=1', 'card_label=Integrated Camera'], check=True)
    
    # 4. CRUCIAL COOLDOWN: Give the OS kernel 1 second to register the device nodes cleanly
    print("Waiting for Linux kernel to map device nodes...")
    time.sleep(1.0)
    print("Driver reset successfully!")
    
except subprocess.CalledProcessError:
    print("\n[Error] Failed to reset driver. Make sure to run the script targeting your venv with sudo.")
    sys.exit(1)

# --- START THE MAIN PIPELINE ---
# 1. Grab physical webcam
cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 30

print(f"Physical camera initialized at {width}x{height} @ {fps}FPS")

# 2. Change 'fmt' to PixelFormat.RGB (Browsers love standard RGB)
with pyvirtualcam.Camera(width=width, height=height, fps=fps, device=DEVICE_PATH, fmt=PixelFormat.RGB) as vcam:
    print(f"Virtual Camera is LIVE on: {vcam.device}")
    print("Press Ctrl+C to stop.")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Inject your custom text onto the frame
        cv2.putText(frame, "Himal fuchee bhaiiiii", (50, height - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3, cv2.LINE_AA)
            
        # Convert BGR (OpenCV standard) to RGB (Browser standard)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        vcam.send(rgb_frame)
        vcam.sleep_until_next_frame()

cap.release()
print("Clean exit.")