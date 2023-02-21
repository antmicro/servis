from typing import List, Tuple, Optional
from pathlib import Path
from matplotlib import rcParams, pyplot as plt

rcParams['font.sans-serif'] = 'lato'


def create_multiple_matplotlib_plot(
        ydatas: List[List],
        xdatas: List[List],
        title: Optional[str] = None,
        subtitles: Optional[List[str]] = None,
        xtitles: Optional[List[str]] = None,
        xunits: Optional[List[str]] = None,
        ytitles: Optional[List[str]] = None,
        yunits: Optional[List[str]] = None,
        outpath: Optional[Path] = None,
        figsize: Tuple = (1500, 1080),
        bins: int = 20,
        render_one_plot: bool = False):
    """
    Draws time series plot.

    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydatas : List[List]
        The list of lists of OY values for multiple series.
    xdata : List
        The values for X dimension
    title : Optional[str]
        Title of the plot
    subtitles : Optional[List[str]]
        Titles of the subplots
    xtitles : Optional[List[str]]
        Name of the X axis
    xuints : Optional[List[str]]
        Unit for the X axis
    ytitles : Optional[List[str]]
        Name of the Y axis
    yunits : Optional[List[str]]
        Unit for the Y axis
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    render_one_plot : bool
        Use one plot to render all data, or split to one subplot for each
        set of data
    """
    # TODO: colorschemes

    if render_one_plot:
        plotsnumber = 1
        assert all(
            [len(arg) == 1 for arg in (xtitles, xunits, ytitles, yunits)]
        ), "Multiple axis not supported, when rendering on only one plot"
    else:
        plotsnumber = len(ydatas)

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
        for ydata, xdata in zip(ydatas, xdatas):
            axplot.scatter(xdata, ydata, alpha=0.5)
    else:
        for ydata, xdata, axplot in zip(ydatas, xdatas, axs[:, 0]):
            axplot.scatter(xdata, ydata, c='#E74A3C', alpha=0.5)

    if render_one_plot and subtitles is not None:
        axplot.legend(subtitles)
    elif subtitles is not None:
        for subtitle in subtitles:
            axplot.set_title(subtitle)

    xlabels = None
    if xtitles:
        xlabels = xtitles
        for i, (xunit, xlabel) in enumerate(zip(xunits, xlabels)):
            if xunits is not None:
                xlabels[i] += f' [{xunit}]'

    ylabels = None
    if ytitles:
        ylabels = ytitles
        for i, (yunit, ylabel) in enumerate(zip(yunits, ylabels)):
            if yunits is not None:
                ylabels[i] += f' [{yunit}]'

    if plotsnumber == 1:
        if xlabels:
            axplot.set_xlabel(xlabels[0], fontsize='large')
            axplot.set_ylabel(ylabels[0], fontsize='large')
            axplot.grid()

        axhist = axs[1]
        y_min = min([min(ydata) for ydata in ydatas])
        y_max = max([max(ydata) for ydata in ydatas])
        # for ydata in ydatas:
        axhist.hist(ydatas, bins=bins, orientation='horizontal',
                    range=(y_min, y_max))
        axhist.set_xscale('log')
        axhist.set_xlabel('Value histogram', fontsize='large')
        axhist.grid(which='both')
        plt.setp(axhist.get_yticklabels(), visible=False)
    else:
        if xlabels:
            for xlabel, axplot in zip(xlabels, axs[:, 0]):
                axplot.set_xlabel(xlabel, fontsize='large')
        if ylabels:
            for ylabel, axplot in zip(ylabels, axs[:, 0]):
                axplot.set_ylabel(ylabel, fontsize='large')

        for axplot in axs[:, 0]:
            axplot.grid()

        for ydata, axhist in zip(ydatas, axs[:, 1]):
            axhist.hist(ydata, bins=bins,
                        orientation='horizontal', color='#E74A3C')
            axhist.set_xscale('log')
            axhist.set_xlabel('Value histogram', fontsize='large')
            axhist.grid(which='both')
            plt.setp(axhist.get_yticklabels(), visible=False)

    if outpath is None:
        plt.show()
    else:
        plt.savefig(outpath)


def create_matplotlib_plot(
        ydata: List,
        xdata: List,
        title: str,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        outpath: Optional[Path] = None,
        figsize: Tuple = (15, 8.5),
        bins: int = 20):
    """
    Draws time series plot.

    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydata : List
        The values for Y dimension
    xdata : List
        The values for X dimension
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
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    """

    create_multiple_matplotlib_plot(
        [ydata],
        [xdata],
        title,
        None,
        [xtitle],
        [xunit],
        [ytitle],
        [yunit],
        outpath,
        figsize,
        bins
    )
