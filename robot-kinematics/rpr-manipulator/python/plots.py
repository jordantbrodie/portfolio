"""Make the README figures: workspace point cloud and both IK solutions for the home target."""
import matplotlib
matplotlib.use("Agg")
import math
import matplotlib.pyplot as plt
import numpy as np

from rpr8 import fk, ik_analytic, workspace

pts = workspace(n=24)
fig = plt.figure(figsize=(12, 5))
ax = fig.add_subplot(1, 2, 1, projection="3d")
ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], c=pts[:, 2], s=2, cmap="viridis")
ax.set(title=f"Collision-free workspace ({len(pts)} sampled poses)", xlabel="x", ylabel="y", zlabel="z")
ax.set_box_aspect((np.ptp(pts[:,0]), np.ptp(pts[:,1]), np.ptp(pts[:,2])))
ax.view_init(20, -60)

ax = fig.add_subplot(1, 2, 2, projection="3d")
target = (6, 5, 8)
for (a, b, l2), colour in zip(ik_analytic(target), ("tab:blue", "tab:orange")):
    p = fk(math.radians(a), math.radians(b), l2).points()
    ax.plot(p[:, 0], p[:, 1], p[:, 2], "-o", color=colour, lw=2.5, label=f"A={a:.0f}°, B={b:.0f}°, L2={l2:.0f}")
ax.scatter(*target, marker="*", s=250, color="red", label="target (6, 5, 8)")
ax.set(title="Analytic IK: two arm configurations reach the target", xlabel="x", ylabel="y", zlabel="z")
ax.legend(loc="upper left", fontsize=8)
ax.set_xlim(0, 7); ax.set_ylim(-1, 6); ax.set_zlim(0, 9)
ax.set_box_aspect((7, 7, 9))
ax.view_init(18, -50)
fig.tight_layout()
fig.savefig("../images/python_workspace_and_ik.png", dpi=130)
print("saved")
