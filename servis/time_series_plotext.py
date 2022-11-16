from typing import List, Tuple, Optional
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