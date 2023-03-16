"""
Functions to creating and rendering time series plots in various formats
"""

from pathlib import Path
from typing import List, Dict, Tuple, Optional, Union, Iterable


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
        colormap: Optional[Union[List, str]] = None,
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
    outputext : Optional[List[str]]
        Extensions of generated files.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst : bool
        True if the first entry should be removed from plotting.
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    is_x_timestamp : bool
        Used in txt plot.
        True if x should be a timestamp,
        False if x should be converted to datetime
    plottype : str
        Type of the plot. Depends on backend
    tags : list
        List of tags and their timestamps
    tagstype : str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    backend : str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    setgradientcolors : bool
        True if gradient colors instead of one color should be set
        in plot rendered using Bokeh.
        False otherwise.
    """

    render_multiple_time_series_plot(
        ydata,
        xdata,
        title,
        None,
        [xtitle] if xtitle else None,
        [xunit] if xunit else None,
        [ytitle] if ytitle else None,
        [yunit] if yunit else None,
        [x_range] if x_range else None,
        [y_range] if y_range else None,
        outpath,
        outputext,
        trimxvalues,
        skipfirst,
        figsize,
        bins,
        is_x_timestamp,
        plottype,
        [tags] if len(tags) > 0 else [],
        [tagstype],
        backend,
        colormap,
        setgradientcolors,
    )


def render_multiple_time_series_plot(
        ydatas: Union[List, List[List], List[List[List]]],
        xdatas: Union[List, List[List], List[List[List]]],
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
        tagstype: Union[str, List[str]] = "single",
        backend: str = "plotext",
        colormap: Optional[List] = None,
        setgradientcolors: bool = False,
        legend_labels: List[str] = []):
    """
    Draws multiple time series plot.

    Used i.e. for timeline of resource usage.

    It also draws the histograms of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydatas : List | List[List] | List[List[List]]
        Data with values of Y dimension for every plot.
        If data is in List format:
        - only one plot will be generated
        If data is in List[List] format:
        - one figure (with one plot) will be generated for each sub-list
        If data is in List[List[List]] format:
        - one figure will be generated for each sub-list and this figure will
          contain plots of all data from lists in sub-list
    xdatas : List | List[List] | List[List[List]]
        Data with values for X dimension for every plot, has to have the same
        structure as ydatas
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
    outputext : List[str]
        Extension of generated file.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvalues : bool
        True if all values for the X dimension should be subtracted by
        the minimal value on this dimension
    skipfirst : bool
        True if the first entry should be removed from plotting.
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    is_x_timestamp : bool
        Used in txt plot.
        True if x should be a timestamp,
        False if x should be converted to datetime
    plottype : str
        Type of the plot. Depends on backend
    tags : list
        List of tags and their timestamps for each X-axis
    tagstype : str | List[str]
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps or list with described values.
    backend : str
        "bokeh" for rendering png/svg plot using Bokeh
        "matplotlib" for rendering png/svg plot using Matplotlib
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    setgradientcolors : bool
        True if gradient colors instead of one color should be set
        in plot rendered using Bokeh.
        False otherwise.
    legend_labels : List[str]
        List with names used as labels in legend
    """
    assert backend in ['bokeh', 'matplotlib', 'plotext']

    # List -> List[List]
    if not isinstance(xdatas[0], (List, Tuple, Iterable)):
        xdatas = [xdatas]
        ydatas = [ydatas]

    # List[List] -> List[List[List]]
    if not isinstance(xdatas[0][0], (List, Tuple, Iterable)):
        for i, (xdata, ydata) in enumerate(zip(xdatas, ydatas)):
            xdatas[i] = [xdata]
            ydatas[i] = [ydata]

    # Fill xdatas with default values (from 0 to n) in shape of ydatas
    if xdatas is None:
        xdatas = []
        for sub_ydatas in ydatas:
            xdatas.append([list(range(len(ydata))) for ydata in sub_ydatas])

    # Skip first
    start = 1 if skipfirst else 0
    for sub_xdatas, sub_ydatas in zip(xdatas, ydatas):
        for i, (xdata, ydata) in enumerate(zip(sub_xdatas, sub_ydatas)):
            sub_xdatas[i] = xdata[start:]
            sub_ydatas[i] = ydata[start:]

    # Trim values, so they begin at 0
    offsets = []
    if trimxvalues:
        for sub_xdatas in xdatas:
            for i, xdata in enumerate(sub_xdatas):
                minx = min(xdata)
                sub_xdatas[i] = [x - minx for x in xdata]
                offsets.append(minx)

    figsnumber = len(ydatas)
    # Default values for None parameters
    if y_ranges is None:
        y_ranges = [None for _ in range(figsnumber)]
    if x_ranges is None:
        x_ranges = [None for _ in range(figsnumber)]
    if xtitles is None:
        xtitles = [None for _ in range(figsnumber)]
    if ytitles is None:
        ytitles = [None for _ in range(figsnumber)]
    if xunits is None:
        xunits = [None for _ in range(figsnumber)]
    if yunits is None:
        yunits = [None for _ in range(figsnumber)]
    if subtitles is None:
        subtitles = [None for _ in range(figsnumber)]

    figsize_copy = figsize
    for ext in outputext:
        figsize = figsize_copy
        if ext == "txt":
            # Use plotext and set backend specific params
            from servis.time_series_plotext import render_ascii_plot
            renderer = render_ascii_plot
            outpath_form = "{}.ascii"
            figsize = (figsize[0] // 10, figsize[1] // 10)
        elif ext == "html" or backend == "bokeh":
            # Use bokeh and set backend specific params
            from servis.time_series_bokeh import create_bokeh_plot
            renderer = create_bokeh_plot
            outpath_form = "{}"
        else:
            # Use matplotlib and set backend specific params
            from servis.time_series_matplotlib import \
                create_multiple_matplotlib_plot
            renderer = create_multiple_matplotlib_plot
            outpath_form = f"{{}}.{ext}"
            figsize = (figsize[0] / 100, figsize[1] / 100)

        renderer(
            ydatas=ydatas,
            xdatas=xdatas,
            title=title,
            subtitles=subtitles,
            xtitles=xtitles,
            xunits=xunits,
            ytitles=ytitles,
            yunits=yunits,
            x_ranges=x_ranges,
            y_ranges=y_ranges,
            outpath=outpath_form.format(outpath) if outpath else None,
            outputext=[ext],
            trimxvaluesoffsets=offsets,
            figsize=figsize,
            bins=bins,
            is_x_timestamp=is_x_timestamp,
            plottype=plottype,
            tags=tags,
            tagstype=tagstype,
            colormap=colormap,
            setgradientcolors=setgradientcolors,
            legend_labels=legend_labels,
        )
