from typing import List, Tuple, Optional, Union
from pathlib import Path
from matplotlib import rcParams, pyplot as plt
import numpy as np

from servis.utils import validate_colormap, validate_kwargs

rcParams['font.sans-serif'] = 'lato'
RANGE_BORDER_SCALE = 0.04
NOT_SUPPORTED_PARAMS = {
    'outputext', 'trimxvaluesoffsets', 'is_x_timestamp',
    'tags', 'tagstype', 'setgradientcolors', 'plottype',
}


def create_multiple_matplotlib_plot(
        ydatas: List[List[List]],
        xdatas: List[List[List]],
        title: Optional[str] = None,
        subtitles: Optional[List[str]] = None,
        xtitles: Optional[List[str]] = None,
        xunits: Optional[List[str]] = None,
        ytitles: Optional[List[str]] = None,
        yunits: Optional[List[str]] = None,
        x_ranges: Optional[List[Tuple]] = None,
        y_ranges: Optional[List[Tuple]] = None,
        outpath: Optional[Path] = None,
        figsize: Tuple = (15, 8.5),
        bins: int = 20,
        colormap: Optional[Union[List, str]] = None,
        legend_labels: List[str] = [],
        **kwargs):
    """
    Draws time series plot.

    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydatas : List[List[List]]
        The list of lists of lists with OY values for multiple series.
    xdata : List[List[List]]
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
    x_ranges : Optional[List[Tuple]]
        The list of ranges of zoom for each X axis
    y_ranges : Optional[List[Tuple]]
        The list of ranges of zoom for each Y axis
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    legend_labels : List[str]
        List with names used as labels in legend
    """
    validate_kwargs(NOT_SUPPORTED_PARAMS, **kwargs)

    figsnumber = len(ydatas)

    plotsnumber = sum([len(sub_ydatas) for sub_ydatas in ydatas])
    if len(legend_labels) > 0:
        labels = iter(legend_labels)
    else:
        labels = iter([None] * plotsnumber)

    fig, axs = plt.subplots(
        ncols=2,
        nrows=figsnumber,
        tight_layout=True,
        figsize=figsize,
        gridspec_kw={'width_ratios': (8, 3)}
    )
    bbox_extras = []

    bbox_extras.append(fig.suptitle(title, fontsize='x-large'))
    if figsnumber == 1:
        axs = axs[np.newaxis, :]

    for sub_ydatas, sub_xdatas, y_range, x_range, axplot, axhist in zip(
            ydatas, xdatas, y_ranges, x_ranges, axs[:, 0], axs[:, 1]):
        plotsnumber = len(sub_ydatas)
        plot_colors = validate_colormap(colormap, 'matplotlib', plotsnumber)
        hist_colors = validate_colormap(colormap, 'matplotlib', plotsnumber)
        axplot.grid()
        axhist.grid(which='both')
        # Drawing points
        for ydata, xdata in zip(sub_ydatas, sub_xdatas):
            axplot.scatter(xdata, ydata, color=next(plot_colors),
                           alpha=0.5, label=next(labels))
        # Drawing histogram
        y_min, y_max = np.min(sub_ydatas), np.max(sub_ydatas)
        axhist.hist(
            sub_ydatas, bins=bins,
            orientation='horizontal', range=(y_min, y_max),
            color=[next(hist_colors) for _ in sub_ydatas])
        # Histogram settings
        axhist.set_xscale('log')
        plt.setp(axhist.get_yticklabels(), visible=False)
        # Set ranges for OX and OY
        if y_range is None:
            border = (y_max - y_min) * RANGE_BORDER_SCALE
            y_range = (y_min - border, y_max + border)
        axplot.set_ylim(*y_range)
        axhist.set_ylim(*y_range)
        if x_range is None:
            x_min, x_max = np.min(sub_xdatas), np.max(sub_xdatas)
            border = (x_max - x_min) * RANGE_BORDER_SCALE
            x_range = (x_min - border, x_max + border)
        axplot.set_xlim(*x_range)

    # Adding legend
    if len(legend_labels) > 0:
        bbox_extras.append(fig.legend(
            bbox_to_anchor=[.5, 0.],
            ncols=3,
            loc="upper center"))

    # Adding sub-titles
    for subtitle, axplot in zip(subtitles, axs[:, 0]):
        axplot.set_title(subtitle)

    # Adding x-labels
    xlabels = None
    if xtitles:
        xlabels = xtitles
        for i, (xunit, xlabel, axplot, axhist) in enumerate(
                zip(xunits, xlabels, axs[:, 0], axs[:, 1])):
            if xlabel is None:
                continue
            if xunit is not None:
                xlabel += f' [{xunit}]'
            bbox_extras.extend(
                [axplot.set_xlabel(xlabel, fontsize='large'),
                 axhist.set_xlabel('Value histogram', fontsize='large')])

    # Adding y-labels
    ylabels = None
    if ytitles:
        ylabels = ytitles
        for i, (yunit, ylabel, axplot) in enumerate(
                zip(yunits, ylabels, axs[:, 0])):
            if ylabel is None:
                continue
            if yunit is not None:
                ylabel += f' [{yunit}]'
            bbox_extras.append(axplot.set_ylabel(ylabel, fontsize='large'))

    if outpath is None:
        plt.show()
    else:
        plt.savefig(outpath,
                    bbox_extra_artists=bbox_extras,
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
        x_range: Optional[Tuple] = None,
        y_range: Optional[Tuple] = None,
        outpath: Optional[Path] = None,
        figsize: Tuple = (15, 8.5),
        bins: int = 20,
        colormap: Optional[Union[List, str]] = None,
        **kwargs):
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
    x_range : Optional[Tuple]
        The range of zoom for each X axis
    y_range : Optional[Tuple]
        The range of zoom for each Y axis
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
        [[ydata]],
        [[xdata]],
        title,
        None,
        [xtitle],
        [xunit],
        [ytitle],
        [yunit],
        [x_range],
        [y_range],
        outpath,
        figsize,
        bins,
        colormap
    )
