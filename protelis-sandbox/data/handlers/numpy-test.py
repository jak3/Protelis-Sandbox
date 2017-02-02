import glob
import matplotlib.pyplot as plt
import numpy as np

# Data -------------------------------------------------------------------- {{{

variables = [ "seed", "offset" ]
nvariables = { 'nseed': 2, 'noffset': 10 }

healthyRegex = "mhealthy*"
sickDistRegex = "sick-distance*"

plots = [
        { "outName": "plot-sick-distance",
            "title": "Malevolent area at different distance",
            "x": "Distance",
            "y": "Error $(\mu)$",
            #  (xmin,xmax) xmax = areaWidth or gradient max distance
            "xlim": (-1, 20),
            "ylim": (-0.25, 5) },

        { "outName": "plot-sick-magnitude",
            "title": "Malevolent area with different size",
            "x": "Size",
            "y": "Error",
            "xlim": (),
            "ylim": () },

        { "outName": "plot-sick-badness",
            "title": "Smart malevolent area",
            "x": "",
            "y": "Error",
            "xlim": (),
            "ylim": () },

        ]

# }}}

# Functions --------------------------------------------------------------- {{{

def plot(example, what, save=False):
    plt.grid(True)
    plt.title(example['title'])
    plt.xlabel(example['x'])
    plt.ylabel(example['y'])
    plt.xlim(example['xlim'])
    plt.ylim(example['ylim'])
    # https://it.mathworks.com/help/matlab/ref/linespec.html
    plt.plot([0,10], what, '--or')
    plt.tight_layout()
    if save:
        plt.savefig(example['outName'] + '.pdf')
    plt.show()

def genfromtxtSimul(fsname):
    return [np.genfromtxt(fd, dtype=float) for fd in
            sorted(glob.glob(fsname))]

def keepLastLine(arrayOflistOflist):
    return map(lambda v: v[-1][-1], arrayOflistOflist)

def correlate(healthy, sick):
    return abs(np.sum(healthy) - np.sum(sick))

def debug(msg):
    print(msg + '\n')
    print(healthy)
    print(sickDist)

def subListVariables(vlist, nvar):
    return [vlist[x:x+nvar] for x in range(0, len(vlist), nvar)]

# }}}

# Loading ----------------------------------------------------------------- {{{

## Whole Content
healthy = np.genfromtxt(glob.glob(healthyRegex)[0], dtype=float)
sickDist = genfromtxtSimul("msick-*")
#for i in range(nvariables['noffset']+1):
#    sr = sickDistRegex + "offset-" + str(i) + ".*"
#    sickDist.append(genfromtxtSimul(sr))
sickMagn = [] # TODO
sickBadn = [] # TODO

## Only last line (algorithm is stable) and a single value
healthy = np.mean(healthy[-1])
sickDist = [np.mean(s[-1]) for s in sickDist]

## Create error values (1 per len(healthy))
errors = []
for s in sickDist:
    errors.append(abs(healthy-s))

plot(plots[0], errors)
# }}}

# EOF vim: set ts=4 sw=4 tw=79 foldmethod=marker :
