from typing import List, Tuple, Optional, Union
from sys import stdout
import datetime
from contextlib import redirect_stdout
from pathlib import Path
import logging

from servis.utils import (
    validate_colormap, validate_kwargs, histogram
)

BAR_WIDTH = 0.1
LOGGER = logging.getLogger(__name__)
NOT_SUPPORTED_PARAMS = {
    'title', 'outputext', 'tags', 'tagstype',
    'setgradientcolors', 'trimxvaluesoffsets'
}


def _set_plot_attributes(
        title: Optional[str] = None,
        xtitle: Optional[str] = None,
        xunit: Optional[str] = None,
        ytitle: Optional[str] = None,
        yunit: Optional[str] = None,
        x_range: Optional[Tuple] = None,
        y_range: Optional[Tuple] = None,
        figsize: Optional[Tuple] = None,
        canvas_color: Union[str, Tuple] = (51, 45, 55),
        axes_color: Union[str, Tuple] = (51, 45, 55),
        ticks_color: Union[str, Tuple] = 'white'):
    """
    Sets attributes (like title, axes labels or plot size) for currently
    active plot.

    Parameters
    ----------
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
    figsize : Optional[Tuple]
        The size of the figure
    canvas_color : str | Tuple[int]
        Name of color of the plot background or
        its representation in 3 integers
    axes_color : str | Tuple[int]
        Name of color of the background of labels surrounding plot or
        its representation in 3 integers
    ticks_color : str | Tuple[int]
        Name of color of the axes ticks and of the grid lines or
        its representation in 3 integers
    """
    import plotext

    if figsize is not None:
        plotext.limit_size(False)
        plotext.plot_size(*figsize)

    if x_range is not None:
        plotext.xlim(x_range[0], x_range[1])

    if y_range is not None:
        plotext.ylim(y_range[0], y_range[1])

    if title:
        plotext.title(title)

    if xtitle:
        xlabel = xtitle
        if xunit is not None:
            xlabel += f' [{xunit}]'
        plotext.xlabel(xlabel)
    if ytitle:
        ylabel = ytitle
        if yunit is not None:
            ylabel += f' [{yunit}]'
        plotext.ylabel(ylabel)

    plotext.canvas_color(canvas_color)
    plotext.axes_color(axes_color)
    plotext.ticks_color(ticks_color)


def create_ascii_histogram(
        sub_ydatas: List[List],
        title: Optional[str] = None,
        xtitle: Optional[str] = None,
        y_range: Optional[Tuple] = None,
        figsize: Optional[Tuple] = None,
        bins: int = 20,
        histtype: str = 'line',
        hidden_y_ticks: bool = False,
        canvas_color: Union[str, Tuple] = (51, 45, 55),
        axes_color: Union[str, Tuple] = (51, 45, 55),
        ticks_color: Union[str, Tuple] = 'white',
        data_colors: List[Tuple] = [(231, 74, 60)]):
    """
    Draws ASCII histogram of time series data in terminal.

    Used i.e. to draw histogram plot during CI.

    Parameters
    ----------
    sub_ydatas : List[List]
        The values for Y dimension
    title : Optional[str]
        Title of the plot
    xtitle : Optional[str]
        Name of the X axis
    y_range : Optional[Tuple]
        The range of zoom on Y axis
    figsize : Optional[Tuple]
        The size of the figure
    bins : int
        The number of bins used for histogram
    histtype : str
        Can be 'scatter', 'bar' or 'line'
    hidden_y_ticks : bool
        Should ticks on y axis be hidden
    canvas_color : str | Tuple[int]
        Name of color of the plot background or
        its representation in 3 integers
    axes_color : str | Tuple[int]
        Name of color of the background of labels surrounding plot or
        its representation in 3 integers
    ticks_color : str | Tuple[int]
        Name of color of the axes ticks and of the grid lines or
        its representation in 3 integers
    data_colors : List[Tuple[int]]
        List with colors used to plot different sets of data
    """
    import plotext

    # Prepare histogram data
    hist_data = []
    min_y = min([min(ydata) for ydata in sub_ydatas])
    max_y = max([max(ydata) for ydata in sub_ydatas])
    for ydata in sub_ydatas:
        values, bin_edges = histogram(
            ydata, bins=bins,
            bounds=(min_y, max_y))
        hist_data.append(values)
    bin_middles = [(b_start + b_end) / 2 for b_start,
                   b_end in zip(bin_edges[:-1], bin_edges[1:])]

    # Draw histogram
    if histtype == 'bar':
        plotext.multiple_bar(
            bin_middles, hist_data,
            orientation='horizontal', width=BAR_WIDTH, color=data_colors)
    else:
        if histtype == 'scatter':
            draw_hist = plotext.scatter
        elif histtype == 'line':
            draw_hist = plotext.plot

        for quantities, color in zip(hist_data, data_colors):
            draw_hist(quantities, bin_middles, color=color)

    min_x = min([min(data) for data in hist_data])
    max_x = max([max(data) for data in hist_data])
    _set_plot_attributes(
        title=title,
        xtitle=xtitle,
        x_range=(min_x, max_x + 1),
        y_range=y_range,
        figsize=figsize,
        canvas_color=canvas_color,
        axes_color=axes_color,
        ticks_color=ticks_color,
    )
    # Set non-float xticks and hide yticks
    step = (max_x - min_x) / 5
    plotext.xticks([int(min_x + tick*step) for tick in range(6)])
    if hidden_y_ticks:
        plotext.yticks([], [])

    plotext.show()


def create_ascii_plot(
        sub_ydatas: List[List],
        sub_xdatas: List[List],
        title: Optional[str] = None,
        xtitle: Optional[str] = None,
        xunit: Optional[str] = None,
        ytitle: Optional[str] = None,
        yunit: Optional[str] = None,
        x_range: Optional[Tuple] = (0, 10),
        y_range: Optional[Tuple] = (0, 100),
        figsize: Optional[Tuple] = None,
        bins: int = 0,
        plottype: Union[str, Tuple[str]] = ('scatter', 'line'),
        is_x_timestamp: bool = True,
        canvas_color: Union[str, Tuple[int]] = (51, 45, 55),
        axes_color: Union[str, Tuple[int]] = (51, 45, 55),
        ticks_color: Union[str, Tuple[int]] = 'white',
        data_colors: List[Tuple[int]] = [(231, 74, 60)],
        legend_labels: List[str] = []):
    """
    Draws ASCII time series plot in terminal.

    Used i.e. to draw time series plot during CI.

    Parameters
    ----------
    sub_ydatas : List[List]
        The values for Y dimension
    sub_xdatas : List[List]
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
    figsize : Optional[Tuple]
        The size of the figure
    plottype : str | Tuple[str]
        Type of plot or (plot, histogram). Values can be either:
        'scatter', 'bar' or 'line'
    is_x_timestamp : bool
        True if x should be a timestamp,
        False if x should be converted to datetime
    canvas_color : str | Tuple[int]
        Name of color of the plot background or
        its representation in 3 integers
    axes_color : str | Tuple[int]
        Name of color of the background of labels surrounding plot or
        its representation in 3 integers
    ticks_color : str | Tuple[int]
        Name of color of the axes ticks and of the grid lines or
        its representation in 3 integers
    data_colors : List[Tuple[int]]
        List with colors used to plot different sets of data
    legend_labels : List[str]
        List with names used as labels in legend
    """
    # Getting plottype and histtype
    if isinstance(plottype, str):
        histtype = plottype
    elif len(plottype) == 1:
        histtype = plottype = plottype[0]
    else:
        histtype = plottype[1]
        plottype = plottype[0]

    assert all([type in ('scatter', 'bar', 'line')
               for type in (plottype, histtype)])
    import plotext
    _CHOOSE_DRAW_FUNCTION = {
        'bar': lambda x, y, **kwargs:
        plotext.bar(x, y, width=BAR_WIDTH, **kwargs),
        'scatter': plotext.scatter,
        'line': plotext.plot,
    }

    plotext.clear_figure()
    if bins != 0:
        # If histogram should be drawn, create subplots and choose one
        # for time series
        plotext.subplots(1, 2)
        plotext.subplot(1, 1)

    if is_x_timestamp is True:
        plotext.date_form('H:M:S')
        sub_xdatas = [[datetime.datetime.fromtimestamp(x).strftime("%H:%M:%S")
                       for x in xdata] for xdata in sub_xdatas]

    # Draw plot
    first_x = sub_xdatas[0]
    if (plottype == 'bar' and
            all([first_x == xdata for xdata in sub_xdatas[1:]])):
        # If bar type and all x coordinates are the same, use multiple_bar
        # function to prevent overlapping bars
        plotext.multiple_bar(
            first_x, sub_ydatas,
            orientation='vertical', width=BAR_WIDTH, color=data_colors,
            label=legend_labels)
    else:
        draw_plot = _CHOOSE_DRAW_FUNCTION[plottype]
        for ydata, xdata, data_color, label in zip(
                sub_ydatas, sub_xdatas, data_colors, legend_labels):
            draw_plot(xdata, ydata, color=data_color, label=label)

    _set_plot_attributes(
        title=title,
        xtitle=xtitle,
        xunit=xunit,
        ytitle=ytitle,
        yunit=yunit,
        x_range=x_range,
        y_range=y_range,
        figsize=((11 if bins == 0 else 8) * figsize[0] // 11, figsize[1]),
        canvas_color=canvas_color,
        axes_color=axes_color,
        ticks_color=ticks_color,
    )

    if bins == 0:
        # Do not draw historgram
        plotext.show()
        return

    plotext.subplot(1, 2)
    create_ascii_histogram(
        sub_ydatas=sub_ydatas,
        title="Histogram" if title else None,
        xtitle="Quantity" if xtitle or ytitle else None,
        y_range=y_range,
        figsize=(3*figsize[0] // 11, figsize[1]),
        bins=bins,
        histtype=histtype,
        hidden_y_ticks=True,
        canvas_color=canvas_color,
        axes_color=axes_color,
        ticks_color=ticks_color,
        data_colors=data_colors,
    )


def render_ascii_plot(
        ydatas: List[List[List]],
        xdatas: List[List[List]],
        subtitles: List[Optional[str]],
        xtitles: List[Optional[str]],
        xunits: List[Optional[str]],
        ytitles: List[Optional[str]],
        yunits: List[Optional[str]],
        x_ranges: Optional[List[Tuple]] = None,
        y_ranges: Optional[List[Tuple]] = None,
        outpath: Optional[Path] = None,
        figsize: Optional[Tuple] = None,
        bins: int = 0,
        is_x_timestamp: bool = True,
        plottype: Union[str, Tuple[str]] = 'line',
        colormap: Optional[Union[List, str]] = None,
        legend_labels: List[str] = [],
        **kwargs):
    """
    Draws multiple ASCII time series plot in terminal.

    Used i.e. to draw time series plot during CI.

    Parameters
    ----------
    ydatas : List[List[List]]
        The values for Y dimension
    xdatas : List[List[List]]
        The values for X dimension
    subtitles : List[Optional[str]]
        Title of the plots
    xtitles : List[Optional[str]]
        Names of the X axes
    xuints : List[Optional[str]]
        Units for the X axes
    ytitles : List[Optional[str]]
        Names of the Y axes
    yunits : List[Optional[str]]
        Units for the Y axes
    x_ranges : Optional[List[Tuple]]
        The ranges of zoom on X axes
    y_ranges : Optional[List[Tuple]]
        The ranges of zoom on Y axes
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    figsize : Optional[Tuple]
        The size of the figure
    is_x_timestamp : bool
        True if x should be a timestamp,
        False if x should be converted to datetime
    plottype : str | Tuple[str]
        Type of plot or (plot, histogram). Values can be either:
        'scatter', 'bar' or 'line'
    colormap : List | str | None
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    legend_labels : List[str]
        List with names used as labels in legend
    """
    validate_kwargs(NOT_SUPPORTED_PARAMS, **kwargs)

    plotsnumber = sum([len(ydata) for ydata in ydatas])

    if len(legend_labels) == 0:
        legend_labels = [None for _ in range(plotsnumber)]

    try:
        if outpath is not None:
            outfile = open(outpath, 'w')
        else:
            outfile = stdout

        labels = iter(legend_labels)
        with redirect_stdout(outfile):
            for title, xtitle, xunit, ytitle, yunit, ydata, xdata, \
                x_range, y_range in zip(
                    subtitles, xtitles, xunits, ytitles, yunits,
                    ydatas, xdatas, x_ranges, y_ranges):
                colors = validate_colormap(
                    colormap,
                    'plotext',
                    quantity=len(ydata)
                )
                create_ascii_plot(
                    sub_ydatas=ydata,
                    sub_xdatas=xdata,
                    title=title,
                    xtitle=xtitle,
                    xunit=xunit,
                    ytitle=ytitle,
                    yunit=yunit,
                    x_range=x_range,
                    y_range=y_range,
                    figsize=(figsize[0], figsize[1] // len(ydatas)),
                    bins=bins,
                    plottype=plottype,
                    is_x_timestamp=is_x_timestamp,
                    data_colors=[next(colors) for _ in ydata],
                    legend_labels=[next(labels) for _ in ydata],
                )
    except OSError as error:
        LOGGER.error(
            f'Plot in TXT format cannot be created, error occured:\n{error}')
    finally:
        if outpath is not None:
            outfile.close()
