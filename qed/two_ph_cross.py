from feynman import Diagram
import matplotlib.pyplot as plt


fig = plt.figure(figsize=(5, 5))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)

l = 0.245  # Length of the propagator
txt_l = 0.05  # Padding around the symbol
op_l = 0.08  # Size of the operator

electron_line = dict(arrow=False, style="double")
photon_line = dict(arrow=False, style="wiggly", nwiggles=10)

D = Diagram(ax)

in1 = D.vertex(xy=[0.05, 0.01], marker="")
v11 = D.vertex(in1.xy, dy=l)
v12 = D.vertex(v11.xy, dy=2 * l)
out1 = D.vertex(v12.xy, dy=l, marker="")

# in1.text("a", x=-0.04, fontsize=30)
# out1.text("a", x=-0.04, y=-0.025, fontsize=30)

D.line(in1, v11, **electron_line)
D.line(v11, v12, **electron_line)
D.line(v12, out1, **electron_line)

in2 = D.vertex(xy=[0.95, 0.01], marker="")
v21 = D.vertex(in2.xy, dy=l)
v22 = D.vertex(v21.xy, dy=2 * l)
out2 = D.vertex(v22.xy, dy=l, marker="")

# in2.text("b", x=0.04, fontsize=30)
# out2.text("b", x=0.04, y=-0.025, fontsize=30)

D.line(in2, v21, **electron_line)
D.line(v21, v22, **electron_line)
D.line(v22, out2, **electron_line)

D.line(v11, v22, **photon_line)
D.line(v12, v21, **photon_line)


# Plot and show
D.plot()
plt.show()

fig.savefig("two_ph_cross.pdf")
