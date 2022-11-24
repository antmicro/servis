from typing import List, Tuple, Optional
import datetime


def create_ascii_plot(
        ydata: List,
        xdata: List,
        title: Optional[str] = None,
        xtitle: Optional[str] = None,
        xunit: Optional[str] = None,
        ytitle: Optional[str] = None,
        yunit: Optional[str] = None,
        x_range: Optional[Tuple] = (0, 10),
        y_range: Optional[Tuple] = (0, 100),
        figsize: Optional[Tuple] = None,
        plottype: str = 'scatter',
        is_x_timestamp: bool = True,
        canvas_color='black',
        axes_color='black',
        ticks_color='white',
        color='white'):
    """
    Draws ASCII time series plot in terminal.

    Used i.e. to draw time series plot during CI.

    Parameters
    ----------
    ydata : List
        The values for Y dimension
    xdata : List
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
    plottype : str
        Can be 'scatter', 'bar' or 'line'
    is_x_timestamp:
        True if x should be a timestamp,
        False if x should be converted to datetime
    canvas_color:
        Name of color of the plot background
    axes_color:
        Name of color of the background of labels surrounding plot
    ticks_color:
        Name of color of the axes ticks and of the grid lines
    """
    assert plottype in ['scatter', 'bar', 'line']
    import plotext
    plotext.clear_figure()

    if is_x_timestamp is True:
        plotext.date_form('H:M:S')
        xdata = [datetime.datetime.fromtimestamp(
            x).strftime("%H:%M:%S") for x in xdata
        ]

    xlabel = xtitle
    if xunit is not None:
        xlabel += f' [{xunit}]'
    ylabel = ytitle
    if yunit is not None:
        ylabel += f' [{yunit}]'

    if plottype == 'bar':
        plotext.bar(xdata, ydata, width=0.1, color=(231, 74, 60))
    elif plottype == 'scatter':
        plotext.scatter(xdata, ydata, color=(231, 74, 60))
    elif plottype == 'line':
        plotext.plot(xdata, ydata)

    if figsize is not None:
        plotext.limit_size(False)
        plotext.plot_size(figsize[0], figsize[1])

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
    plotext.show()
