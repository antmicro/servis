"""
Functions to creating and rendering time series plots in various formats
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import datetime

def create_ascii_plot(
        title: str,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        xdata: List,
        ydata: List,
        x_range: Optional[Tuple] = (0, 10),
        y_range: Optional[Tuple] = (0, 100),
        figsize: Optional[Tuple] = None,
        switchtobarchart: bool = False,
        canvas_color='black',
        axes_color='black',
        ticks_color='white'):
    """
    Draws ASCII time series plot in terminal.

    Used i.e. to draw time series plot during CI.

    Parameters
    ----------
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
    xrange : Optional[Tuple]
        The range of zoom on X axis
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    figsize: Optional[Tuple]
        The size of the figure
    switchtobarchart:
        True if we want to change the plot type to barchart
    canvas_color:
        Name of color of the plot background
    axes_color:
        Name of color of the background of labels surrounding plot
    ticks_color:
        Name of color of the axes ticks and of the grid lines
    """
    import plotext
    plotext.clear_figure()

    plotext.date_form('H:M:S')
    xdata = [datetime.datetime.fromtimestamp(
        x).strftime("%H:%M:%S") for x in xdata]

    xlabel = xtitle
    if xunit is not None:
        xlabel += f' [{xunit}]'
    ylabel = ytitle
    if yunit is not None:
        ylabel += f' [{yunit}]'

    if switchtobarchart is True:
        plotext.bar(xdata, ydata, width=0.1)
    else:
        plotext.scatter(xdata, ydata)
    if figsize is not None:
        plotext.limit_size(False)
        plotext.plot_size(figsize[0], figsize[1])

    if x_range is not None:
        plotext.xlim(x_range[0], x_range[1])
    if y_range is not None:
        plotext.ylim(y_range[0], y_range[1])
    plotext.title(title)
    plotext.xlabel(xlabel)
    plotext.ylabel(ylabel)
    plotext.canvas_color(canvas_color)
    plotext.axes_color(axes_color)
    plotext.ticks_color(ticks_color)
    plotext.show()


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


def render_time_series_plot_with_histogram(
        outpath: Optional[Path],
        outputext: Optional[List[str]],
        title: str,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        xdata: List,
        ydata: List,
        xrange: Optional[Tuple] = None,
        yrange: Optional[Tuple] = None,
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 850),
        bins: int = 20,
        tags: List = [],
        tagstype: str = "single",
        backend: str = "bokeh"):
    """
    Draws time series plot.

    Used i.e. for timeline of resource usage.
    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    outputext: Optional[List[str]]
        Extensions of generated files.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
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
    xrange : Optional[Tuple]
        The range of zoom on X axis
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst: bool
        True if the first entry should be removed from plotting.
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    tags: list
        List of tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    backend: str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    """
    start = 1 if skipfirst else 0
    xdata = np.array(xdata[start:], copy=True)
    ydata = np.array(ydata[start:], copy=True)

    minx = 0
    if trimxvalues:
        minx = min(xdata)
        xdata = [x - minx for x in xdata]

    if "txt" in outputext:
        create_ascii_plot(
            title,
            xtitle,
            xunit,
            ytitle,
            yunit,
            xdata,
            ydata,
            xrange,
            yrange
        )

    if "png" in outputext and backend == "matplotlib":
        create_matplotlib_plot(
            f'{outpath}.png',
            title,
            xtitle,
            xunit,
            ytitle,
            yunit,
            xdata,
            ydata,
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        create_matplotlib_plot(
            f'{outpath}.svg',
            title,
            xtitle,
            xunit,
            ytitle,
            yunit,
            xdata,
            ydata,
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if backend == "bokeh" or "html" in outputext:
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber=1,
            outpath=outpath,
            outputext=outputext,
            title="",
            subtitles=[title],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            xdata=xdata,
            ydatas=[ydata],
            xrange=xrange,
            yrange=yrange,
            trimxvaluesoffset=minx,
            switchtobarchart=False,
            figsize=figsize,
            bins=bins,
            tags=tags,
            tagstype=tagstype
        )


def render_multiple_time_series_plot(
        plotsnumber: int,
        outpath: Optional[Path],
        outputext: Optional[List[str]],
        title: str,
        subtitles: List[str],
        xtitles: List[str],
        xunits: List[str],
        ytitles: List[str],
        yunits: List[str],
        xdata: List,
        ydatas: List,
        xrange: Optional[Tuple] = None,
        yrange: Optional[Tuple] = None,
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 1080),
        bins: int = 20,
        switchtobarchart: bool = True,
        tags: List[Dict] = [],
        tagstype: str = "single",
        backend: str = "bokeh"):
    """
    Draws multiple time series plot.

    Used i.e. for timeline of resource usage.

    It also draws the histograms of values that appeared throughout the
    experiment.

    Parameters
    ----------
    plotsnumber: int
        Number of time series plots in the figure.
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    outputext: List[str]
        Extension of generated file.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
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
    xrange : Optional[Tuple]
        The range of zoom on X axis
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst: bool
        True if the first entry should be removed from plotting.
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    tags: list
        List of tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    backend: str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    """
    start = 1 if skipfirst else 0
    xdata = np.array(xdata[start:], copy=True)
    for ydata in ydatas:
        ydata = np.array(ydata[start:], copy=True)

    if trimxvalues:
        minx = min(xdata)
        xdata = [x - minx for x in xdata]

    if "txt" in outputext:
        print('\n\n')
        for title, xtitle, xunit, ytitle, yunit, ydata in zip(subtitles, xtitles, xunits, ytitles, yunits, ydatas):  # noqa: E501
            create_ascii_plot(
                title,
                xtitle,
                xunit,
                ytitle,
                yunit,
                xdata,
                ydata,
                x_range=xrange,
                y_range=yrange,
                figsize=figsize,
                switchtobarchart=switchtobarchart
            )
            print('\n\n')

    if "png" in outputext and backend == "matplotlib":
        create_multiple_matplotlib_plot(
            plotsnumber,
            f'{outpath}.png',
            title,
            subtitles,
            xtitles,
            xunits,
            ytitles,
            yunits,
            xdata,
            ydatas,
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        create_multiple_matplotlib_plot(
            plotsnumber,
            f'{outpath}.svg',
            title,
            subtitles,
            xtitles,
            xunits,
            ytitles,
            yunits,
            xdata,
            ydatas,
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if backend == "bokeh" or "html" in outputext:
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber,
            outpath,
            outputext,
            title,
            subtitles,
            xtitles,
            xunits,
            ytitles,
            yunits,
            xdata,
            ydatas,
            xrange,
            yrange,
            minx,
            figsize,
            bins,
            switchtobarchart,
            tags,
            tagstype,
            setgradientcolors=True
        )
