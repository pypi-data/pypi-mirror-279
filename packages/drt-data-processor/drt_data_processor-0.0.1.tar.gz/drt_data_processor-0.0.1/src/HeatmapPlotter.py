import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def heatmap(data, row_labels, col_labels, step, valfmt="{x:.2f}", ax=None, cbar_kw=None, cbarlabel="", **kwargs):
    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    im = ax.imshow(data, **kwargs)

    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")

    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    kw = dict(horizontalalignment="center", verticalalignment="center")

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            im.axes.text(j, i, valfmt(data[i, j], None), kw)

    plt.savefig(fname=f"heatmap_step№{step}")
    plt.clf()
    return im, cbar


def gen_xticklabels(countX, delta):
    xticklabels = []
    i = 0
    labels = 0
    while i < countX:
        xticklabels.append(labels)
        labels += delta
        labels = round(labels, 2)
        i += 1
    return xticklabels


def gen_yticklabels(deltaZ, countZ):
    yticklabels = []
    i = 0
    labels = 0
    delta = deltaZ
    while i < countZ:
        yticklabels.append(labels)
        labels += delta
        labels = round(labels, 2)
        i += 1
    return yticklabels
