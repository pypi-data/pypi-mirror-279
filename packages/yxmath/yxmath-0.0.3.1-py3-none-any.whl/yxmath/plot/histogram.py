import numpy as np
import matplotlib.pyplot as plt


def histogram_ploter(data, bins='auto', save_file=None, ax=None):
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.get_figure()

    data = np.array(data)

    n, bins = np.histogram(data, bins=bins)

    ax.hist(data, bins=bins)

    if save_file:
        fig.savefig(save_file, format='png', facecolor='none', dpi=300,
                    edgecolor='none', bbox_inches='tight')

    if ax is None:
        plt.show()    

    return n, bins
