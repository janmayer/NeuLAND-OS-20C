import logging
import matplotlib as mpl

logging.getLogger("matplotlib").setLevel(logging.WARNING)

mpl.use("pgf")

# https://matplotlib.org/users/customizing.html
mpl.rcParams.update({
    "pgf.texsystem": "lualatex",
    "pgf.preamble": [
        r"\usepackage{fontspec, unicode-math, isotope}",
        r"\setmainfont{Libertinus Serif}",
        r"\setsansfont{Libertinus Sans}",
        r"\setmonofont[Scale=MatchLowercase]{Source Code Pro}",
        r"\setmathfont{Libertinus Math}",
    ],
    "text.usetex": True,
    "font.size": 20,
    "font.family": "serif",
    "font.serif": "Libertinus Serif",
    "font.sans-serif": "Libertinus Sans",
    "font.monospace": "Source Code Pro",
    "axes.spines.left": True,
    "axes.spines.bottom": True,
    "axes.spines.top": True,
    "axes.spines.right": True,
    "legend.fancybox": False,
    "legend.edgecolor": "#FFFFFF",
    "xtick.top": True,
    "xtick.minor.visible": True,
    "ytick.right": True,
    "ytick.minor.visible": True,
})

import matplotlib.pyplot as plt

import palettable
import numpy as np
import re
from collections import defaultdict

import ROOT
import rootpy.io
from rootpy.plotting import Canvas, Graph, Hist
from rootpy.plotting.style import get_style, set_style
import rootpy.plotting.root2matplotlib as rplt

#logging.getLogger().setLevel(level=logging.WARNING)
