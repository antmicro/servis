"""
Functions to creating and rendering time series plots in various formats
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional


def render_time_series_plot_with_histogram(
        title: str,
        xdata: List,
        ydata: List,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        xrange: Optional[Tuple] = None,
        yrange: Optional[Tuple] = None,
        outpath: Optional[Path] = None,
        outputext: Optional[List[str]] = ['txt'],
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 850),
        bins: int = 20,
        is_x_timestamp: bool = True,
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
    title : str
        Title of the plot
    xdata : List
        The values for X dimension
    ydata : List
        The values for Y dimension
    xtitle : str
        Name of the X axis
    xuint : str
        Unit for the X axis
    ytitle : str
        Name of the Y axis
    yunit : str
        Unit for the Y axis
    xrange : Optional[Tuple]
        The range of zoom on X axis
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    outputext: Optional[List[str]]
        Extensions of generated files.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst: bool
        True if the first entry should be removed from plotting.
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    is_x_timestamp:
        Used in txt plot.
        True if x should be a timestamp,
        False if x should be converted to datetime
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
        from servis.time_series_plotext import create_ascii_plot
        create_ascii_plot(
            title,
            xdata,
            ydata,
            xtitle,
            xunit,
            ytitle,
            yunit,
            xrange,
            yrange,
            is_x_timestamp=is_x_timestamp
        )

    if "png" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_matplotlib_plot
        create_matplotlib_plot(
            title,
            xdata,
            ydata,
            xtitle,
            xunit,
            ytitle,
            yunit,
            outpath=f'{outpath}.png',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_matplotlib_plot
        create_matplotlib_plot(
            title,
            xdata,
            ydata,
            xtitle,
            xunit,
            ytitle,
            yunit,
            outpath=f'{outpath}.svg',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "html" in outputext:
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber=1,
            title="",
            subtitles=[title],
            xdata=xdata,
            ydatas=[ydata],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            xrange=xrange,
            yrange=yrange,
            outpath=outpath,
            outputext=["html"],
            trimxvaluesoffset=minx,
            switchtobarchart=False,
            figsize=figsize,
            bins=bins,
            tags=tags,
            tagstype=tagstype
        )

    if backend == "bokeh":
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber=1,
            title="",
            subtitles=[title],
            xdata=xdata,
            ydatas=[ydata],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            xrange=xrange,
            yrange=yrange,
            outpath=outpath,
            outputext=outputext,
            trimxvaluesoffset=minx,
            switchtobarchart=False,
            figsize=figsize,
            bins=bins,
            tags=tags,
            tagstype=tagstype
        )


def render_multiple_time_series_plot(
        plotsnumber: int,
        title: str,
        subtitles: List[str],
        xdata: List,
        ydatas: List,
        xtitles: List[str],
        xunits: List[str],
        ytitles: List[str],
        yunits: List[str],
        xrange: Optional[Tuple] = None,
        yrange: Optional[Tuple] = None,
        outpath: Optional[Path] = None,
        outputext: Optional[List[str]] = ['txt'],
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 1080),
        bins: int = 20,
        is_x_timestamp: bool = True,
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
    title : List[str]
        Title of the plot
    subtitles : List[str]
        Titles of the subplots
    xdata : List
        The values for X dimension
    ydatas : List
        The values for Y dimension
    xtitles : List[str]
        Name of the X axis
    xuints : List[str]
        Unit for the X axis
    ytitles : List[str]
        Name of the Y axis
    yunits : List[str]
        Unit for the Y axis
    xrange : Optional[Tuple]
        The range of zoom on X axis
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    outputext: List[str]
        Extension of generated file.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst: bool
        True if the first entry should be removed from plotting.
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    is_x_timestamp:
        Used in txt plot.
        True if x should be a timestamp,
        False if x should be converted to datetime
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
        from servis.time_series_plotext import create_ascii_plot
        for title, xtitle, xunit, ytitle, yunit, ydata in zip(subtitles, xtitles, xunits, ytitles, yunits, ydatas):  # noqa: E501
            create_ascii_plot(
                title=title,
                xtitle=xtitle,
                xunit=xunit,
                ytitle=ytitle,
                yunit=yunit,
                xdata=xdata,
                ydata=ydata,
                x_range=xrange,
                y_range=yrange,
                figsize=figsize,
                switchtobarchart=switchtobarchart,
                is_x_timestamp=is_x_timestamp
            )
            print('\n\n')

    if "png" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_multiple_matplotlib_plot  # noqa: E501
        create_multiple_matplotlib_plot(
            plotsnumber,
            title,
            subtitles,
            xdata,
            ydatas,
            xtitles,
            xunits,
            ytitles,
            yunits,
            f'{outpath}.png',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_multiple_matplotlib_plot  # noqa: E501
        create_multiple_matplotlib_plot(
            plotsnumber,
            title,
            subtitles,
            xdata,
            ydatas,
            xtitles,
            xunits,
            ytitles,
            yunits,
            f'{outpath}.svg',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "html" in outputext:
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber,
            title,
            subtitles,
            xdata,
            ydatas,
            xtitles,
            xunits,
            ytitles,
            yunits,
            xrange,
            yrange,
            outpath,
            ["html"],
            minx,
            figsize,
            bins,
            switchtobarchart,
            tags,
            tagstype,
            setgradientcolors=True
        )
    if backend == "bokeh":
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            plotsnumber,
            title,
            subtitles,
            xdata,
            ydatas,
            xtitles,
            xunits,
            ytitles,
            yunits,
            xrange,
            yrange,
            outpath,
            outputext,
            minx,
            figsize,
            bins,
            switchtobarchart,
            tags,
            tagstype,
            setgradientcolors=True
        )
