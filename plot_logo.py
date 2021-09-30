#!/usr/bin/env python

import matplotlib as mpl
from matplotlib.text import TextPath
from matplotlib.patches import PathPatch
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import seaborn as sns

fp = FontProperties(family="Arial", weight="bold")
globscale = 1.35
LETTERS = { "T" : TextPath((-0.305, 0), "T", size=1, prop=fp),
            "G" : TextPath((-0.384, 0), "G", size=1, prop=fp),
            "A" : TextPath((-0.35, 0), "A", size=1, prop=fp),
            "C" : TextPath((-0.366, 0), "C", size=1, prop=fp), 
            "N" : TextPath((-0.350, 0), "N", size=1, prop=fp)}
COLOR_SCHEME = {'G': 'orange',
                'A': 'red',
                'C': 'blue',
                'T': 'darkgreen',
                'N': 'yellow'}

def letterAt(letter, x, y, yscale=1, ax=None):
    text = LETTERS[letter]

    t = mpl.transforms.Affine2D().scale(1*globscale, yscale*globscale) + \
        mpl.transforms.Affine2D().translate(x,y) + ax.transData
    p = PathPatch(text, lw=0, fc=COLOR_SCHEME[letter],  transform=t)
    if ax != None:
        ax.add_artist(p)
    return p


def plot_logo(ax, all_scores):

    x = 1
    maxi = 0
    for scores in all_scores:
        y = 0
        #for base, score in scores:
        for base, score in sorted(scores, key=lambda x:x[1]):
            letterAt(base, x,y, score, ax)
            y += score
        x += 1
        maxi = max(maxi, y)

    ax.set_xticks(range(1,x))
    ax.set_xlim((0, x))
    ax.set_ylim((0, maxi))
    plt.tight_layout()
    sns.despine(offset=10, trim=True)
    ax.set_ylabel('bits', fontsize=24)
    ax.set_xlabel('position', fontsize=24)
