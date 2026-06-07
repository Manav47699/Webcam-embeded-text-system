# Minor-Project

# Creating a virtual webcam (FOR UBUNTU LINUX)

- Step 1: Install the required dependencies
```
# 1. Install the tools if you haven't already
sudo apt update && sudo apt install -y v4l2loopback-dkms v4l2loopback-utils python3-pip

# 2. Remove any existing instances of the module just in case
sudo rmmod v4l2loopback

# 3. Load it fresh with the "Integrated Camera" label hack 
sudo modprobe v4l2loopback exclusive_caps=1 card_label="Integrated Camera"

```

- Step 2: To see which video device file the virtual camera just claimed

```
v4l2-ctl --list-devices


```
