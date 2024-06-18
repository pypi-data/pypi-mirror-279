"""Visualization of DOB curves."""

from pathlib import Path
from typing import Optional

import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from limax.model import LX


# ------------------------------------------------------------------------------
SMALL_SIZE = 12
MEDIUM_SIZE = 15
BIGGER_SIZE = 25

matplotlib.rc("font", size=SMALL_SIZE)  # controls default text sizes
matplotlib.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
matplotlib.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
matplotlib.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
matplotlib.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
matplotlib.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
matplotlib.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title
# ------------------------------------------------------------------------------


def plot_lx_matplotlib(lx: LX, fig_path: Optional[Path] = None) -> None:
    """Plot DOB curve using matplotlib."""
    metadata = lx.metadata
    ax1: Axes
    ax2: Axes
    f: Figure
    f, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))
    f.subplots_adjust(hspace=0.3)

    f.suptitle(
        f"mid: {lx.metadata.mid}",
        fontdict={
            "fontsize": 11,
        },
    )

    sex_text = "∅ (NA)"
    if metadata.sex == "M":
        sex_text = "♂ (M)"
    elif metadata.sex == "F":
        sex_text = "♀ (F)"
    text = "\n".join(
        [
            f"{'mid':<16}: {metadata.mid}",
            f"{'datetime':<16}: {metadata.datetime}",
            f"{'height':<16}: {metadata.height}",
            f"{'weight':<16}: {metadata.weight}",
            f"{'sex':<16}: {sex_text}",
            f"{'smoking':<16}: {'✓ (Yes)' if metadata.smoking else 'x (No)'}",
            f"{'oxygen':<16}: {'✓ (Yes)' if metadata.oxygen else 'x (No)'}",
            f"{'ventilation':<16}: {'✓ (Yes)' if metadata.ventilation else 'x (No)'}",
            f"{'medication':<16}: {'✓ (Yes)' if metadata.medication else 'x (No)'}",
            f"{'food abstinence':<16}: {metadata.food_abstinence}",
        ]
    )
    ax1.annotate(
        text,
        xy=(0.05, 0.4),
        xycoords="figure fraction",
        family="monospace",
        size=14,
    )

    for ax in (ax2, ax3):
        ax.plot(
            np.array(lx.data.time) / 60,
            lx.data.dob,
            "-o",
            color="black",
            markeredgecolor="black",
            markerfacecolor="tab:blue",
        )
        ax.grid(True)

        ax.set_xlabel("Time [min]", fontdict={"weight": "bold"})

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.spines["bottom"].set_visible(False)
    ax1.spines["left"].set_visible(False)

    ax2.set_ylabel("DOB", fontdict={"weight": "bold"})
    ax3.set_yscale("log")
    ax3.set_ylim(bottom=1.0)

    plt.show()
    if fig_path:
        f.savefig(fig_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    from limax import EXAMPLE_LIMAX_PATIENT1_PATH
    from limax.io import parse_limax_file

    lx: LX = parse_limax_file(EXAMPLE_LIMAX_PATIENT1_PATH)
    print(lx.to_df())
    plot_lx_matplotlib(lx)
