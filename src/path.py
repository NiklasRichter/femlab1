import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize


class Path:
    def __init__(self, xs, ys, max_spacing):
        self.xs = list(xs)
        self.ys = list(ys)
        self.max_spacing = max_spacing

    @property
    def points(self):
        return list(zip(self.xs, self.ys))

    def validate(self):
        if len(self.xs) != len(self.ys):
            raise ValueError(f"xs and ys differ in length ({len(self.xs)} vs {len(self.ys)})")
        if not self.xs:
            raise ValueError("path is empty")
        if (self.xs[0], self.ys[0]) != (0, 0):
            raise ValueError(f"path must start at (0, 0), got ({self.xs[0]}, {self.ys[0]})")

        pts = self.points
        for i in range(len(pts) - 1):
            d = math.dist(pts[i], pts[i + 1])
            if d > self.max_spacing:
                raise ValueError(
                    f"spacing {d:.6g} between point {i} {pts[i]} and point {i + 1} {pts[i + 1]} "
                    f"exceeds max spacing {self.max_spacing}"
                )

    def to_txt(self, filename):
        self.validate()
        values = [str(v) for p in self.points for v in p]
        values.append("0")
        with open(filename, "w") as f:
            f.write(",".join(values))

    def plot(self, ax=None):
        pts = np.array(self.points, dtype=float)
        d = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        segments = np.stack([pts[:-1], pts[1:]], axis=1)

        if ax is None:
            _, ax = plt.subplots()

        cmap = LinearSegmentedColormap.from_list("spacing", ["#86b6ef", "#0d366b"])
        norm = Normalize(0, max(self.max_spacing, d.max(initial=0)))
        lines = LineCollection(segments, cmap=cmap, norm=norm, linewidths=2)
        lines.set_array(d)
        ax.add_collection(lines)

        too_far = d > self.max_spacing
        if too_far.any():
            ax.add_collection(LineCollection(
                segments[too_far], colors="#d03b3b", linewidths=2, linestyles="--",
                label=f"> max spacing ({self.max_spacing})",
            ))
            ax.legend()

        ax.plot(pts[:, 0], pts[:, 1], "o", color="#0d366b", markersize=5, zorder=3)

        cbar = ax.figure.colorbar(lines, ax=ax, label="distance to next point")
        cbar.ax.axhline(self.max_spacing, color="#d03b3b", linewidth=1.5)

        ax.set_aspect("equal")
        ax.autoscale_view()
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        plt.show()
    


if __name__ == "__main__":
    p = Path([0, 1, 2, 3], [0, 0.5, 1, 1.5], max_spacing=1.2)
    p.to_txt("path.txt")
    p.plot()
    plt.show()
