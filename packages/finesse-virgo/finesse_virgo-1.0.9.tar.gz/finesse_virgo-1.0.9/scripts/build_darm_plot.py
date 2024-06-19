#!/usr/bin/env python
import finesse
import finesse.virgo
import matplotlib.pyplot as plt

finesse.init_plotting()

"""
Build and save DARM plot using current default.
"""
print("Building DARM plot...")

OUTPUT_PATH = "files/DARM.png"

print("modes off...")
virgo = finesse.virgo.Virgo()
virgo.model.modes("off")
virgo.make(dc_lock=False)

ax = virgo.plot_DARM(label="Modes off")

for x in [2,5]:
    print(f"{x} modes...")
    virgo2 = virgo.deepcopy()
    virgo2.model.modes(maxtem=x)
    virgo2.make(dc_lock=False)
    ax = virgo2.plot_DARM(ax=ax, label=f"Maxtem={x}", linestyle="--" if x == 5 else "-")

print(f"saving to {OUTPUT_PATH}...")
plt.savefig(OUTPUT_PATH)
print("DONE.")
