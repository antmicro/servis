from typing import List, Tuple, Optional
import datetime
from contextlib import redirect_stdout
from pathlib import Path


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
        canvas_color=(51, 45, 55),
        axes_color=(51, 45, 55),
        ticks_color='white',
        data_color=(231, 74, 60)):
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
        plotext.bar(xdata, ydata, width=0.1, color=data_color)
    elif plottype == 'scatter':
        plotext.scatter(xdata, ydata, color=data_color)
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


def render_ascii_plot(
        ydatas: List,
        xdatas: List,
        titles: List[str],
        xtitles: List[str],
        xunits: List[str],
        ytitles: List[str],
        yunits: List[str],
        x_ranges: Optional[List[Tuple]] = None,
        y_ranges: Optional[List[Tuple]] = None,
        outpath: Optional[Path] = None,
        figsize: Tuple = None,
        is_x_timestamp: bool = True,
        plottype: str = 'bar'):
    """
    Draws multiple ASCII time series plot in terminal.

    Used i.e. to draw time series plot during CI.

    Parameters
    ----------
    ydatas : List
        The values for Y dimension
    xdatas : List
        The values for X dimension
    titles : Optional[str]
        Title of the plots
    xtitles : Optional[str]
        Names of the X axes
    xuints : Optional[str]
        Units for the X axes
    ytitles : Optional[str]
        Names of the Y axes
    yunits : Optional[str]
        Units for the Y axes
    x_ranges : Optional[Tuple]
        The ranges of zoom on X axes
    y_ranges : Optional[Tuple]
        The ranges of zoom on Y axes
    outpath : Optional[Path]
        Output path for the plot image. If None, the plot will be displayed.
    figsize : Optional[Tuple]
        The size of the figure
    is_x_timestamp:
        True if x should be a timestamp,
        False if x should be converted to datetime
    plottype : str
        Can be 'scatter', 'bar' or 'line'
    """

    if outpath is not None:
        with open(outpath, 'w') as outfile:
            with redirect_stdout(outfile):
                print('\n\n')
                for title, xtitle, xunit, ytitle, yunit, ydata, xdata, \
                    x_range, y_range in zip(
                        titles, xtitles, xunits, ytitles, yunits,
                        ydatas, xdatas, x_ranges, y_ranges):
                    create_ascii_plot(
                        ydata=ydata,
                        xdata=xdata,
                        title=title,
                        xtitle=xtitle,
                        xunit=xunit,
                        ytitle=ytitle,
                        yunit=yunit,
                        x_range=x_range,
                        y_range=y_range,
                        figsize=figsize,
                        plottype=plottype,
                        is_x_timestamp=is_x_timestamp
                    )
                    print('\n\n')

    else:
        print('\n\n')
        for title, xtitle, xunit, ytitle, yunit, ydata, xdata, \
            x_range, y_range in zip(
                titles, xtitles, xunits, ytitles, yunits,
                ydatas, xdatas, x_ranges, y_ranges):
            create_ascii_plot(
                ydata=ydata,
                xdata=xdata,
                title=title,
                xtitle=xtitle,
                xunit=xunit,
                ytitle=ytitle,
                yunit=yunit,
                x_range=x_range,
                y_range=y_range,
                figsize=figsize,
                plottype=plottype,
                is_x_timestamp=is_x_timestamp
            )
            print('\n\n')
