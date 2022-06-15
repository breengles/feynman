from feynman import Diagram
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)

l = 0.48  # Length of the propagator
txt_l = 0.05  # Padding around the symbol
op_l = 0.08  # Size of the operator

electron_line = dict(arrow=False, style="double")
photon_line = dict(arrow=False, style="wiggly", nwiggles=8)
vac_line = dict(arrow=False, shape="circular", style="double", circle_angle=0.0, circle_radius=0.2)

D = Diagram(ax)

in1 = D.vertex(xy=[0.05, 0.01], marker="")
v11 = D.vertex(in1.xy, dy=l)
out1 = D.vertex(v11.xy, dy=l, marker="")

vac = D.vertex(v11.xy, dx=l)

# in1.text("a", x=-0.04, fontsize=30)
# out1.text("a", x=-0.04, y=-0.025, fontsize=30)

D.line(in1, v11, **electron_line)
D.line(v11, out1, **electron_line)

D.line(vac, vac, **vac_line)

D.line(v11, vac, **photon_line)

# Plot and show
D.plot()
plt.show()

fig.savefig("vacuum-polarization.pdf")
