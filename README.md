# Jordan Brodie — Robotics & Autonomy Engineering

BSc Integrated Engineering (Mechatronics) student at Tallinn University of Technology (TalTech), graduating June 2027. I work on robots that have to operate on their own in remote, communication-limited places: underwater, in the air and, one day, on the Moon. My focus is navigation, fault detection and recovery, and control.

📍 Tallinn, Estonia · Estonian (EU) and US citizen · 📧 jobrod@taltech.ee

---

## Highlights

| Project | What it shows | Tools |
|---|---|---|
| [**ROS 2 wheel odometry & robot simulation**](ros2/) | Pose estimation from encoder ticks (wrap-around, quaternions, midpoint integration), a differential-drive robot in MuJoCo, bag recording and replay. Updated weekly. | ROS 2, Python, MuJoCo, RViz |
| [**ABB robot drawing program**](industrial-robotics/abb-robotstudio-rapid/) | An IRB 1600 arm draws a circle and "JB": AutoPath and free targets, work objects, tool orientation, pen-up/pen-down moves. | RAPID, ABB RobotStudio |
| [**Mitsubishi pick-and-place**](industrial-robotics/mitsubishi-melfa-basic/) | Four-station gripper routine with safe approach/retreat moves and an external start signal. | MELFA BASIC IV, CIROS Studio |
| [**Object detection with YOLO + OpenCV**](computer-vision/object-detection-yolo-opencv/) | Train → detect → log pipeline for a custom dataset, plus a classic OpenCV tracker with unit tests. | Python, YOLOv8, OpenCV, pytest |
| [**Arduino keypad calculator**](embedded-cpp/arduino-keypad-calculator/) | Hardware-independent C++ logic, unit-tested on a PC, running on an Arduino with keypad and LCD. | C++, Arduino, Make |
| [**Proposals & concept studies**](docs/) | Green-hydrogen energy system for Estonia, autonomous lunar settlement, solar pilots, amphibious drone concept. | — |
| [**AI-assisted tools**](ai-assisted-tools/) | Personal knowledge system with an MCP server, Home Assistant smart home, dashboards. | MCP, n8n, Home Assistant |

## In progress

| Project | Status |
|---|---|
| **Untethered navigation & docking for a resident underwater vehicle** — bachelor's thesis at NTNU's Applied Underwater Robotics Laboratory: onboard acoustic positioning so the vehicle can return to its dock without a tether. | Starts Jan 2027 |
| **FPV drone with onboard computer vision** — TalTech Drone Club build with a YOLO detection payload. | In progress |

## Skills

- **Programming:** Python, C, C++, Java, JavaScript, RAPID, MELFA BASIC
- **Robotics:** ROS 2, MuJoCo, Gazebo, Webots, ABB RobotStudio, CIROS Studio; sensors, actuators, system integration
- **Vision / ML:** YOLO, OpenCV, Roboflow
- **Design & simulation:** SolidWorks, AutoCAD, Fusion, KiCad, MATLAB, Simulink, Simscape, Visual Components
- **Testing:** EMC / LVD test planning, environmental and materials testing

## How this repository is organised

Each folder has its own README explaining the problem, what I did and the results. Where a project was a team effort, rebuilt later, or written with AI help, its README says so.

```
portfolio/
├── ros2/                 ROS 2 coursework (links to the live repo)
├── industrial-robotics/  ABB RAPID and Mitsubishi MELFA programs
├── computer-vision/      YOLO and OpenCV
├── embedded-cpp/         Arduino / C++
├── ai-assisted-tools/    software built with AI coding assistants
└── docs/                 proposals, concepts and lab reports (PDF, images)
```
