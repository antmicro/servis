"""
Functions to creating and rendering time series plots in various formats
"""

from pathlib import Path
from typing import List, Dict, Tuple, Optional


def render_time_series_plot_with_histogram(
        ydata: List,
        xdata: Optional[List] = None,
        title: Optional[str] = None,
        xtitle: Optional[str] = None,
        xunit: Optional[str] = None,
        ytitle: Optional[str] = None,
        yunit: Optional[str] = None,
        x_range: Optional[Tuple] = None,
        y_range: Optional[Tuple] = None,
        outpath: Optional[Path] = None,
        outputext: Optional[List[str]] = ['txt'],
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 850),
        bins: int = 20,
        is_x_timestamp: bool = True,
        plottype: str = 'bar',
        tags: List = [],
        tagstype: str = "single",
        backend: str = "plotext",
        setgradientcolors: bool = False):
    """
    Draws time series plot.

    Used i.e. for timeline of resource usage.
    It also draws the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydata : List
        The values for Y dimension
    xdata : Optional[List]
        The values for X dimension
    title : Optional[str]
        Title of the plot
    xtitle : Optional[str]
        Name of the X axis
    xuint : Optional[str]
        Unit for the X axis
    ytitle : Optional[str]
        Name of the Y axis
    yunit : Optional[str]
        Unit for the Y axis
    x_range : Optional[Tuple]
        The range of zoom on X axis
    y_range : Optional[Tuple]
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
    plottype: str
        Type of the plot. Depends on backend
    tags: list
        List of tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    backend: str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    setgradientcolors:
        True if gradient colors instead of one color should be set
        in plot rendered using Bokeh.
        False otherwise.
    """
    assert backend in ['bokeh', 'matplotlib', 'plotext']

    if xdata is None:
        xdata = [i for i in range(len(ydata))]
    start = 1 if skipfirst else 0
    xdata = xdata[start:]
    ydata = ydata[start:]

    offset = 0
    if trimxvalues:
        offset = min(xdata)
        xdata = [x - offset for x in xdata]

    if "txt" in outputext:
        from servis.time_series_plotext import render_ascii_plot

        render_ascii_plot(
            [ydata],
            [xdata],
            titles=[title],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            x_ranges=[x_range],
            y_ranges=[y_range],
            outpath=f'{outpath}.ascii',
            figsize=figsize,
            is_x_timestamp=is_x_timestamp,
            plottype=plottype
        )

    if "png" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_matplotlib_plot
        create_matplotlib_plot(
            ydata,
            xdata,
            title=title,
            xtitle=xtitle,
            xunit=xunit,
            ytitle=ytitle,
            yunit=yunit,
            outpath=f'{outpath}.png',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib import create_matplotlib_plot
        create_matplotlib_plot(
            ydata,
            xdata,
            title=title,
            xtitle=xtitle,
            xunit=xunit,
            ytitle=ytitle,
            yunit=yunit,
            outpath=f'{outpath}.svg',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "html" in outputext:
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            ydatas=[ydata],
            xdatas=[xdata],
            title=title,
            subtitles=[title],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            x_ranges=[x_range],
            y_ranges=[y_range],
            outpath=outpath,
            outputext=["html"],
            trimxvaluesoffsets=[offset],
            plottype=plottype,
            figsize=figsize,
            bins=bins,
            tags=[tags],
            tagstype=tagstype
        )

    if backend == "bokeh":
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            ydatas=[ydata],
            xdatas=[xdata],
            title=title,
            subtitles=[title],
            xtitles=[xtitle],
            xunits=[xunit],
            ytitles=[ytitle],
            yunits=[yunit],
            x_ranges=[x_range],
            y_ranges=[y_range],
            outpath=outpath,
            outputext=outputext,
            trimxvaluesoffsets=[offset],
            plottype=plottype,
            figsize=figsize,
            bins=bins,
            tags=[tags],
            tagstype=tagstype,
            setgradientcolors=setgradientcolors
        )


def render_multiple_time_series_plot(
        ydatas: List[List],
        xdatas: List[List],
        title: str,
        subtitles: List[str],
        xtitles: List[str],
        xunits: List[str],
        ytitles: List[str],
        yunits: List[str],
        x_ranges: Optional[List[Tuple]] = None,
        y_ranges: Optional[List[Tuple]] = None,
        outpath: Optional[Path] = None,
        outputext: Optional[List[str]] = ['txt'],
        trimxvalues: bool = True,
        skipfirst: bool = False,
        figsize: Tuple = (1500, 1080),
        bins: int = 20,
        is_x_timestamp: bool = True,
        plottype: str = 'bar',
        tags: List[List[Dict]] = [],
        tagstype: str = "single",
        backend: str = "plotext",
        setgradientcolors: bool = False):
    """
    Draws multiple time series plot.

    Used i.e. for timeline of resource usage.

    It also draws the histograms of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydatas : List[List]
        The list of list of values for Y dimension for every plot
    xdatas : List[List]
        The list of list of values for X dimension for every plot
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
    x_ranges : Optional[List[Tuple]]
        The list of ranges of zoom for each X axis
    y_ranges : Optional[List[Tuple]]
        The list of ranges of zoom for each Y axis
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
    plottype: str
        Type of the plot. Depends on backend
    tags: list
        List of tags and their timestamps for each X-axis
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    backend: str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    setgradientcolors:
        True if gradient colors instead of one color should be set
        in plot rendered using Bokeh.
        False otherwise.
    """
    assert backend in ['bokeh', 'matplotlib', 'plotext']

    if xdatas is None:
        xdatas = [list(range(len(ydatas[0]))) for _ in range(len(ydatas))]

    start = 1 if skipfirst else 0

    for xdata in xdatas:
        xdata = xdata[start:]

    for ydata in ydatas:
        ydata = ydata[start:]

    offsets = []
    if trimxvalues:
        for xdata in xdatas:
            minx = min(xdata)
            xdata = [x - minx for x in xdata]
            offsets.append(minx)

    if y_ranges is None:
        y_ranges = [None for _ in range(len(ydatas))]
    if x_ranges is None:
        x_ranges = [None for _ in range(len(ydatas))]

    if "txt" in outputext:
        from servis.time_series_plotext import render_ascii_plot

        render_ascii_plot(
            ydatas=ydatas,
            xdatas=xdatas,
            titles=subtitles,
            xtitles=xtitles,
            xunits=xunits,
            ytitles=ytitles,
            yunits=yunits,
            x_ranges=x_ranges,
            y_ranges=y_ranges,
            outpath=f'{outpath}.ascii',
            figsize=figsize,
            is_x_timestamp=is_x_timestamp,
            plottype=plottype
        )

    if "png" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib \
            import create_multiple_matplotlib_plot
        create_multiple_matplotlib_plot(
            ydatas,
            xdatas,
            title,
            subtitles,
            xtitles,
            xunits,
            ytitles,
            yunits,
            f'{outpath}.png',
            figsize=(figsize[0]/100, figsize[1]/100),
            bins=bins
        )

    if "svg" in outputext and backend == "matplotlib":
        from servis.time_series_matplotlib \
            import create_multiple_matplotlib_plot
        create_multiple_matplotlib_plot(
            ydatas,
            xdatas,
            title,
            subtitles,
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
            ydatas,
            xdatas,
            title=title,
            subtitles=subtitles,
            xtitles=xtitles,
            xunits=xunits,
            ytitles=ytitles,
            yunits=yunits,
            x_ranges=x_ranges,
            y_ranges=y_ranges,
            outpath=outpath,
            outputext=["html"],
            trimxvaluesoffsets=offsets,
            figsize=figsize,
            bins=bins,
            plottype=plottype,
            tags=tags,
            tagstype=tagstype,
            setgradientcolors=setgradientcolors
        )
    if backend == "bokeh":
        from servis.time_series_bokeh import create_bokeh_plot
        create_bokeh_plot(
            ydatas,
            xdatas,
            title=title,
            subtitles=subtitles,
            xtitles=xtitles,
            xunits=xunits,
            ytitles=ytitles,
            yunits=yunits,
            x_ranges=x_ranges,
            y_ranges=y_ranges,
            outpath=outpath,
            outputext=outputext,
            trimxvaluesoffsets=offsets,
            figsize=figsize,
            bins=bins,
            plottype=plottype,
            tags=tags,
            tagstype=tagstype,
            setgradientcolors=setgradientcolors
        )
