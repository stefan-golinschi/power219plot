# power219plot

> **Legacy notice:** This `master` branch is kept for historical/legacy use.
> Active development and newer releases live on other branches (currently
> [`v0.2-11.2026`](https://github.com/stefan-golinschi/power219plot/tree/v0.2-11.2026)).
> Prefer a newer branch unless you specifically need this older setup.

---

This project uses an `ina219` sensor to plot the current draw across a period of time using matplotlib.

```
conda create \
 --name power219plot \
 --yes \
 python=3.7 \
 matplotlib=3.1 \
 numpy=1.18 \
 pyserial=3.4
```
