# Tiger-AgBot
PS C:\Users\student> ssh farm-ng-user-alex-andy1@100.78.37.88
farm-ng-user-alex-andy1@key-kit:~$ cd ~/projects/follow
farm-ng-user-alex-andy1@key-kit:~/projects/follow$ python3 -m venv .venv
farm-ng-user-alex-andy1@key-kit:~/projects/follow$ source .venv/bin/activate
Live stream (DepthAI v3 → Browser MJPEG) //pip install flask-Run this server on the robot (copy/paste exactly). It streams at port 8080:
python - <<'PY'
import time
import cv2
import depthai as dai
from flask import Flask, Response

app = Flask(__name__)

pipeline = dai.Pipeline()

# Using ColorCamera (deprecated warning is OK). Works on your device.
cam = pipeline.create(dai.node.ColorCamera)
cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setPreviewSize(640, 360)
cam.setInterleaved(False)

q = cam.preview.createOutputQueue()

pipeline.start()

def gen():
    last_t = time.time()
    frames = 0
    fps = 0.0

    while pipeline.isRunning():
        pkt = q.get()
        frame = pkt.getCvFrame()

        frames += 1
        now = time.time()
        if now - last_t >= 1.0:
            fps = frames / (now - last_t)
            frames = 0
            last_t = now

        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")

@app.route("/")
def video():
    return Response(gen(), mimetype="multipart/x-mixed-replace; boundary=frame")

print("Streaming on http://0.0.0.0:8080  (open from your PC using robot IP)")
app.run(host="0.0.0.0", port=8080, threaded=True)
PY

Enter


On your Windows laptop
Open a browser to one of these (Tailscale is usually easiest):
•	http://100.78.37.88:8080
•	http://10.87.198.130:8080
If one doesn’t load, try the other.




install Jetson-compatible PyTorch and torchvision wheels,
Step 1 — activate your venv
cd ~/projects/follow
source .venv/bin/activate

Step 2 — install Jetson-compatible PyTorch
JetPack 5.1.x uses torch 2.0.0 + torchvision 0.15.1

pip install --extra-index-url https://download.pytorch.org/whl/cu118 \
torch==2.0.0 torchvision==0.15.1



Step 5 — verify everything

python - <<'PY'
import torch
import torchvision
import segmentation_models_pytorch as smp

print("torch:", torch.__version__)
print("torchvision:", torchvision.__version__)
print("smp:", smp.__version__)
print("cuda available:", torch.cuda.is_available())
PY


After this, you can run your planner
Example:
cd ~/projects/follow
source .venv/bin/activate
python planner_follow.py


C:\Users\student>ssh farm-ng-user-alex-andy1@key-kit
Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.10.104-tegra aarch64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

Expanded Security Maintenance for Infrastructure is not enabled.

0 updates can be applied immediately.

168 additional security updates can be applied with ESM Infra.
Learn more about enabling ESM Infra service for Ubuntu 20.04 at
https://ubuntu.com/20-04

-bash: npm: command not found
Your user’s .npmrc file (${HOME}/.npmrc)
has a globalconfig and/or a prefix setting, which are incompatible with nvm.
Run nvm use --delete-prefix v22.14.0 --silent to unset it.
farm-ng-user-alex-andy1@key-kit:~$ ls
deploy   edge-impulse-config.json  node-v16.13.1-linux-arm64         package.json       projects  vips-8.12.1
Desktop  farm-ng-amiga             node-v16.13.1-linux-arm64.tar.xz  package-lock.json  venv      vips-8.12.1.tar.gz
farm-ng-user-alex-andy1@key-kit:~$ cd farm-ng-amiga/
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga$ ls
build           farm-ng-amiga.code-workspace  license_header.txt  py              README.md  setup.py
CMakeLists.txt  LICENSE                       protos              pyproject.toml  setup.cfg
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga$ cd py
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py$ ls
examples  farm_ng  farm_ng_amiga.egg-info  tests
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py$ ls
examples  farm_ng  farm_ng_amiga.egg-info  tests
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py$ cd examples/
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples$ ls
camera_aruco_detector  file_converter       gps_client               service_client       track_plotter
camera_calibration     file_reader          monitor_app              service_counter      track_recorder
camera_client          file_reader_can      motor_states_stream      service_propagation  vehicle_twist
camera_pointcloud      file_reader_gps      multi_client_geoimage    square_track
camera_settings        file_reader_headers  multi_client_subscriber  tool_control
dashboard_settings     file_splitter        pendant_state            track_follower
event_recorder         filter_client        README.md                track_planner
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples$ cd vehicle_twist/
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples/vehicle_twist$ ls
main.py  README.md  requirements.txt  service_config.json
farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples/vehicle_twist$


Use scp from Windows Command Prompt (recommended)
Open Command Prompt on your laptop and run:
scp C:\Users\aa043\Downloads\controller.py farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples/vehicle_twist/

scp C:\Users\aa043\Downloads\height_follow.py farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples/vehicle_twist/


If "key-kit" doesn’t resolve, use the Tailscale IP instead
	
scp C:\Users\aa043\Downloads\controller.py farm-ng-user-alex-andy1@100.87.161.11:~/farm-ng-amiga/py/examples/vehicle_twist/

scp C:\Users\aa043\Downloads\height_follow.py farm-ng-user-alex-andy1@100.87.161.11:~/farm-ng-amiga/py/examples/vehicle_twist/


Method 2 — Copy both at once

scp C:\Users\aa043\Downloads\controller.py C:\Users\aa043\Downloads\height_follow.py farm-ng-user-alex-andy1@key-kit:~/farm-ng-amiga/py/examples/vehicle_twist/

Verify on the Amiga
SSH into Amiga:
ssh farm-ng-user-alex-andy1@key-kit
Go to folder:
cd ~/farm-ng-amiga/py/examples/vehicle_twist
Check files:
ls
You should see:
controller.py
height_follow.py
service_config.json
Method 3 — Easiest method using VS Code (drag & drop)
Since you're already using VS Code SSH:
Open VS Code
Connect to Amiga via SSH
Navigate to:
farm-ng-amiga/py/examples/vehicle_twist
Drag files from:
C:\Users\aa043\Downloads
into that folder
Done.
Best practice after copying

Make sure permissions are correct:
chmod +x controller.py
chmod +x height_follow.py
Then run on Amiga
Terminal 1:
python3 controller.py --service-config service_config.json
Terminal 2:
python3 height_follow.py
If you'd like, I can also show a one-click auto-deploy command so every time you edit locally, it syncs

To display/ browser streaming (Flask/MJPEG) 

Nice — that MJPEG server is exactly the right idea for Windows→SSH workflows (no cv2.imshow() headaches).

Two things to know:

That exact snippet has one issue: cam.preview.createOutputQueue() + pipeline.start() aren’t the usual DepthAI API pattern. The reliable pattern is XLinkOut + dai.Device.

You can also stream your annotated frames (pose boxes / segmentation overlay) the same way, so you see what the follower/planner “sees” from your Windows browser.

Below are two “copy/paste” servers that work reliably.

A)	Clean DepthAI MJPEG stream (raw camera) — runs on Amiga

python3 - <<'PY'
import time
import cv2
import depthai as dai
from flask import Flask, Response
app = Flask(__name__)
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.CAM_A)
cam.setPreviewSize(640, 360)
cam.setInterleaved(False)
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)
def gen(q):
    last_t = time.time()
    frames = 0
    fps = 0.0
    while True:
        pkt = q.get()
        frame = pkt.getCvFrame()
        frames += 1
        now = time.time()
        if now - last_t >= 1.0:
            fps = frames / (now - last_t)
            frames = 0
            last_t = now
        cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        ok, jpg = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
@app.route("/")
def video():
    return Response(gen(video_q), mimetype="multipart/x-mixed-replace; boundary=frame")
with dai.Device(pipeline) as device:
    video_q = device.getOutputQueue(name="video", maxSize=4, blocking=True)
    print("Streaming on http://0.0.0.0:8080  (open from your PC using robot IP)")
    app.run(host="0.0.0.0", port=8080, threaded=True)
PY





Open on Windows:
http://100.87.161.11:8080

B) MJPEG stream of your pose follower overlay (boxes + dots) — runs on Amiga

This is the one you’ll actually want while testing the follower.

python3 - <<'PY'
import cv2
import depthai as dai
from flask import Flask, Response
from cvzone.PoseModule import PoseDetector
app = Flask(__name__)
detector = PoseDetector()
pipeline = dai.Pipeline()
cam = pipeline.createColorCamera()
cam.setBoardSocket(dai.CameraBoardSocket.RGB)
cam.setPreviewSize(640, 480)
cam.setInterleaved(False)
xout = pipeline.createXLinkOut()
xout.setStreamName("video")
cam.preview.link(xout.input)
def gen(q):
    while True:
        pkt = q.get()
        frame = pkt.getCvFrame()
        # Pose detection + overlay
        img = detector.findPose(frame)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=True)
        ok, jpg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        if not ok:
            continue
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + jpg.tobytes() + b"\r\n")
@app.route("/")
def video():
    return Response(gen(video_q), mimetype="multipart/x-mixed-replace; boundary=frame")
with dai.Device(pipeline) as device:
    video_q = device.getOutputQueue(name="video", maxSize=4, blocking=True)
    print("Streaming annotated view on http://0.0.0.0:8080")
    app.run(host="0.0.0.0", port=8080, threaded=True)
PY



Now you can run:
Terminal 1: controller.py
Terminal 2: follower/planner (sending commands)
Windows browser: view the annotated video stream at :8080
One important tip
If you run the follower/planner on the robot, set:
CONTROLLER_IP = "127.0.0.1"
But for the MJPEG stream in your browser, still use:
http://100.87.161.11:8080
If you tell me which camera socket you’re actually using for your follower (CAM_A vs RGB), I’ll align the stream to match it exactly.
