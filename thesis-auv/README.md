# Bachelor's thesis: untethered navigation and docking for a resident underwater vehicle

**Where:** Applied Underwater Robotics Laboratory (AUR-Lab), NTNU, Trondheim · **When:** January–June 2027 (Erasmus) · **Supervisors:** NTNU AUR-Lab, with TalTech-side supervision

## The problem

A *resident* underwater vehicle lives on the seabed next to a docking station and goes out on inspection missions without a ship on the surface. Today these vehicles often stay connected by a tether, which limits range and can snag. The goal of my thesis is to let the vehicle **find its way back to the dock and dock without the tether**, using onboard acoustic positioning, and to compare that against the tethered setup.

## Starting point

The AUR-Lab has already shown autonomous docking with a tethered mini-ROV at 90 m depth: USBL acoustic navigation to approach the dock, ArUco-marker visual localisation fused with an Extended Kalman Filter for the final approach, and a 90 % autonomous docking success rate.

> L. Günzel et al., *Docking and Persistent Operations for a Resident Underwater Vehicle*, arXiv:2602.16360 (2026). https://arxiv.org/abs/2602.16360

## Planned approach (to be confirmed with my supervisors)

1. Reproduce the existing navigation and docking pipeline in simulation (ROS 2, Gazebo).
2. Move acoustic positioning onboard so the vehicle no longer depends on data through the tether.
3. Test untethered return-to-dock and compare accuracy, success rate and mission time against the tethered baseline.

Code, results and the thesis will be added here as the work progresses.
