#!/usr/bin/env python
import finesse
import finesse.virgo
import matplotlib.pyplot as plt

finesse.init_plotting()

OUTPUT_PATH = "files/QNLS.png"

# build QNLS plot using current default
print("Building QNLS plot...")
virgo = finesse.virgo.Virgo()
virgo.make(dc_lock=False)

print("with RP...")
ax = virgo.plot_QNLS()

print("shot noise only...")
ax = virgo.plot_QNLS(ax=ax, shot_noise_only=True, linestyle="--")

virgo.apply_dc_offset()

print("with RP (dc offset)...")
ax = virgo.plot_QNLS(ax=ax, label="NSR (dc offset)")

print("shot noise only (dc offset)...")
ax = virgo.plot_QNLS(ax=ax, shot_noise_only=True, label="NSR (dc offset, shot noise only)")

print(f"saving to {OUTPUT_PATH}...")
plt.savefig(OUTPUT_PATH)
print("DONE.")