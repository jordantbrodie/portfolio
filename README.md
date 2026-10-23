# Jordan Brodie — Systems Engineering for Robotics & Autonomy

BSc Integrated Engineering (Mechatronics) student at Tallinn University of Technology (TalTech), graduating June 2027. I want to work as a **systems engineer** on robots and vehicles that operate on their own in remote places: underwater, in the air and in space. My coursework and projects cover the whole chain a systems engineer has to hold together: requirements, mechanical design, kinematics, control software, simulation, and testing on real hardware.

📍 Tallinn, Estonia · Estonian (EU) and US citizen · 📧 jobrod@taltech.ee

---

## Highlights

| Project | What it shows | Tools |
|---|---|---|
| [**ABB robot: simulation to real hardware**](industrial-robotics/abb-robotstudio-rapid/) | Programmed an IRB 1600 in RobotStudio, then ran it on the real robot, diagnosed four faults from the output and fixed them over five test runs, ending at 100 % speed. | RAPID, ABB RobotStudio |
| [**Electric winch design**](mechanical-design/electric-winch/) | From requirements (750 kg, 0.11 m/s) to component selection, strength and fatigue checks, SolidWorks CAD and drawing, plus a Python calculator that re-checks the design when requirements change. | SolidWorks, Python |
| [**RPR manipulator kinematics**](robot-kinematics/rpr-manipulator/) | Forward kinematics, workspace, inverse kinematics and Simscape simulation in MATLAB; Python port with a closed-form IK and 56 tests. | MATLAB, Simulink, Python |
| [**ROS 2 wheel odometry & simulation**](ros2/) | Pose estimation from encoder ticks, differential-drive robot in MuJoCo, bag recording and replay. Updated weekly. | ROS 2, Python, MuJoCo |
| [**Object detection with YOLO + OpenCV**](computer-vision/object-detection-yolo-opencv/) | Train → detect → log pipeline for a custom dataset, plus a classic OpenCV tracker with tests. | Python, YOLOv8, OpenCV |
| [**Digital twin of a machining cell**](digital-manufacturing/visual-components-cell/) | Robot-tended CNC cell with conveyors, gantries and storage, simulated before build. | Visual Components |
| [**Pneumatic control sequences**](fluid-power/pneumatics-fluidsim/) | Nine circuits up to two-cylinder automatic sequences with limit-switch interlocks. | FluidSIM |
| [**Mitsubishi pick-and-place**](industrial-robotics/mitsubishi-melfa-basic/) | Four-station gripper routine with safe approach and retreat moves. | MELFA BASIC, CIROS |
| [**Embedded C / C++**](embedded-cpp/) | Arduino keypad calculator with PC unit tests; first-year C coursework. | C, C++, Arduino |
| [**Proposals, concepts & reports**](docs/) | Green-hydrogen energy system, autonomous lunar settlement, solar pilots, amphibious drone concept, and coursework reports. | — |
| [**AI-assisted tools**](ai-assisted-tools/) | Personal knowledge system with an MCP server, Home Assistant smart home, dashboards. | MCP, n8n, Home Assistant |

## In progress

| Project | Status |
|---|---|
| [**Untethered navigation & docking for a resident underwater vehicle**](thesis-auv/): bachelor's thesis at NTNU's Applied Underwater Robotics Laboratory | Starts Jan 2027 |
| **FPV drone with onboard computer vision**: TalTech Drone Club build with a YOLO detection payload | In progress |
| **Bike frame**: MER0150 group CAD project | Autumn 2026 |

## Skills

- **Systems:** requirements to design to verification, design calculations, test planning (EMC / LVD, environmental), simulation-first development
- **Programming:** Python, C, C++, MATLAB, JavaScript, RAPID, MELFA BASIC
- **Robotics:** ROS 2, MuJoCo, Gazebo, ABB RobotStudio, CIROS Studio, Simscape Multibody; kinematics, odometry, sensors and actuators
- **Vision / ML:** YOLO, OpenCV, Roboflow
- **Design & simulation:** SolidWorks, AutoCAD, Fusion, KiCad, Simulink, Visual Components, FluidSIM

## How this repository is organised

Each folder has its own README explaining the problem, what I did and the results. Where a project was a team effort, rebuilt later, or written with AI help, its README says so.

```
portfolio/
├── industrial-robotics/   ABB RAPID (sim + real robot), Mitsubishi MELFA
├── robot-kinematics/      MATLAB / Simulink kinematics + Python port
├── ros2/                  ROS 2 coursework (links to the live repo)
├── mechanical-design/     electric winch: calculations, CAD, drawings
├── computer-vision/       YOLO and OpenCV
├── digital-manufacturing/ Visual Components digital twin
├── fluid-power/           FluidSIM pneumatic circuits
├── embedded-cpp/          Arduino / C / C++
├── thesis-auv/            NTNU thesis (from 2027)
├── ai-assisted-tools/     software built with AI coding assistants
└── docs/                  proposals, concepts and coursework reports
```
