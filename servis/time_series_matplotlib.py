from typing import List, Tuple, Optional, Union
from pathlib import Path
from matplotlib import rcParams, pyplot as plt

from servis.utils import validate_colormap

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
        colormap: Optional[Union[List, str]] = None,
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
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    render_one_plot : bool
        Use one plot to render all data, or split to one subplot for each
        set of data
    """

    if render_one_plot:
        plotsnumber = 1
        assert all(
            [len(arg) == 1 for arg in (xtitles, xunits, ytitles, yunits)]
        ), "Multiple axis not supported, when rendering on only one plot"
    else:
        plotsnumber = len(ydatas)

    plot_colors = validate_colormap(colormap, 'matplotlib', len(ydatas))
    hist_colors = validate_colormap(colormap, 'matplotlib', len(ydatas))

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
        for ydata, xdata, color in zip(ydatas, xdatas, plot_colors):
            axplot.scatter(xdata, ydata, alpha=0.5, c=color)
    else:
        for ydata, xdata, axplot, color in zip(
                ydatas, xdatas, axs[:, 0], plot_colors):
            axplot.scatter(xdata, ydata, c=color, alpha=0.5)

    legend = None
    if render_one_plot and subtitles is not None:
        legend = fig.legend(
            subtitles,
            bbox_to_anchor=[.5, 0.],
            ncols=3,
            loc="upper center"
        )
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
        if len(ydatas) == 1:
            hist_colors = next(hist_colors)
        else:
            hist_colors = list(hist_colors)[:len(ydatas)]
        axhist.hist(ydatas, bins=bins, orientation='horizontal',
                    range=(y_min, y_max), color=hist_colors)
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

        for ydata, axhist, color in zip(ydatas, axs[:, 1], hist_colors):
            axhist.hist(ydata, bins=bins,
                        orientation='horizontal', color=color)
            axhist.set_xscale('log')
            axhist.set_xlabel('Value histogram', fontsize='large')
            axhist.grid(which='both')
            plt.setp(axhist.get_yticklabels(), visible=False)

    if outpath is None:
        plt.show()
    else:
        plt.savefig(outpath,
                    bbox_extra_artists=(legend,) if legend else None,
                    bbox_inches='tight')
    plt.close()


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
        bins: int = 20,
        colormap: Optional[Union[List, str]] = None):
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
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
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
        bins,
        colormap
    )
