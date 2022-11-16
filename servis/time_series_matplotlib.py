from typing import List, Tuple, Optional
from pathlib import Path


def create_multiple_matplotlib_plot(
        plotsnumber: int,
        outpath: Optional[Path],
        title: str,
        subtitles: Optional[List[str]],
        xtitles: List[str],
        xunits: List[str],
        ytitles: List[str],
        yunits: List[str],
        xdata: List,
        ydatas: List,
        figsize: Tuple = (1500, 1080),
        bins: int = 20):
    """
    Draws time series plot.

    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    plotsnumber: int
        Number of time series plots in the figure.
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    title : List[str]
        Title of the plot
    subtitles : List[str]
        Titles of the subplots
    xtitles : List[str]
        Name of the X axis
    xuints : List[str]
        Unit for the X axis
    ytitles : List[str]
        Name of the Y axis
    yunits : List[str]
        Unit for the Y axis
    xdata : List
        The values for X dimension
    ydatas : List
        The values for Y dimension
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    """
    from matplotlib import pyplot as plt

    fig, axs = plt.subplots(
        ncols=2,
        nrows=plotsnumber,
        tight_layout=True,
        figsize=figsize,
        sharey=True,
        gridspec_kw={'width_ratios': (8, 3)}
    )
    fig.suptitle(title, fontsize='x-large')

    if plotsnumber == 1:
        axplot = axs[0]
        axplot.scatter(xdata, ydatas[0], c='purple', alpha=0.5)
    else:
        for ydata, axplot in zip(ydatas, axs[:, 0]):
            axplot.scatter(xdata, ydata, c='purple', alpha=0.5)

    if subtitles is not None:
        for subtitle in subtitles:
            axplot.set_title(subtitle)

    xlabels = xtitles
    for xunit, xlabel in zip(xunits, xlabels):
        if xunits is not None:
            xlabel += f' [{xunit}]'

    ylabels = ytitles
    for yunit, ylabel in zip(yunits, ylabels):
        if yunits is not None:
            ylabel += f' [{yunit}]'

    if plotsnumber == 1:
        axplot.set_xlabel(xlabel, fontsize='large')
        axplot.set_ylabel(ylabel, fontsize='large')
        axplot.grid()

        axhist = axs[1]
        axhist.hist(ydatas[0], bins=bins,
                    orientation='horizontal', color='purple')
        axhist.set_xscale('log')
        axhist.set_xlabel('Value histogram', fontsize='large')
        axhist.grid(which='both')
        plt.setp(axhist.get_yticklabels(), visible=False)
    else:
        for xlabel, ylabel, axplot in zip(xlabels, ylabels, axs[:, 0]):
            axplot.set_xlabel(xlabel, fontsize='large')
            axplot.set_ylabel(ylabel, fontsize='large')
            axplot.grid()

        for ydata, axhist in zip(ydatas, axs[:, 1]):
            axhist.hist(ydata, bins=bins,
                        orientation='horizontal', color='purple')
            axhist.set_xscale('log')
            axhist.set_xlabel('Value histogram', fontsize='large')
            axhist.grid(which='both')
            plt.setp(axhist.get_yticklabels(), visible=False)

    if outpath is None:
        plt.show()
    else:
        plt.savefig(outpath)


def create_matplotlib_plot(
        outpath: Optional[Path],
        title: str,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        xdata: List,
        ydata: List,
        figsize: Tuple = (15, 8.5),
        bins: int = 20):
    """
    Draws time series plot.

    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    title : str
        Title of the plot
    xtitle : str
        Name of the X axis
    xuint : str
        Unit for the X axis
    ytitle : str
        Name of the Y axis
    yunit : str
        Unit for the Y axis
    xdata : List
        The values for X dimension
    ydata : List
        The values for Y dimension
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    """

    create_multiple_matplotlib_plot(
        1,
        outpath,
        title,
        None,
        [xtitle],
        [xunit],
        [ytitle],
        [yunit],
        xdata,
        [ydata],
        figsize,
        bins
    )
