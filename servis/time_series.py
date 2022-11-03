"""
Functions to creating and rendering time series plots in various formats
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from bokeh.plotting import figure as bkfigure, output_file, show, save
from bokeh.palettes import d3 as palette
from bokeh.layouts import gridplot
from bokeh.models import Div, Range1d, Span, LabelSet, ColumnDataSource
from bokeh.io import export_png, export_svg
import plotext
from matplotlib import pyplot as plt
import datetime


def get_colors(data: List):
    """
    Generates list of colors for elements in data,
    depending on their value.

    Elements with value between 0 and 5 are turquoise
    and the color changes to redder every 5 percentage
    points.

    Parameters:
    ----------

    data: List
        List of values for which the colors will be generated.

    Returns:
    --------

    data_colors: List
        List of colors for values given in input.
    """
    colors = ["#53FFD1",
              "#5CF3CB",
              "#65E8C5",
              "#6EDCBF",
              "#77D1B9",
              "#80C5B2",
              "#89BAAC",
              "#92AEA6",
              "#9BA2A0",
              "#A4979A",
              "#AE8B94",
              "#B7808E",
              "#C07488",
              "#C96882",
              "#D25D7C",
              "#DB5175",
              "#E4466F",
              "#ED3A69",
              "#F62F63",
              "#FF235D"]
    data_colors = []
    for d in data:
        # there are 20 colors and the values are between 0 and 100,
        # so it has to be divided by 5 to create 20 ranges
        data_colors.append(colors[round(float(d))//5])
    return data_colors


def add_tags(
        plot: bkfigure,
        tags: List[Dict],
        tagstype: str = "single",
        trimxvaluesoffset: float = 0,
        max_y_value: float = 100,
        min_y_value: float = 0,
        yrange: Optional[Tuple] = None):
    """
    Adds tags and returns plot with them.

    Parameters
    ----------
    plot : bkfigure
        Bokeh figure to which tags will be added
    tags : List
        List with tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    trimxvaluesoffset: float
        The number by which the values will be trimmed
    max_y_value: float
        The highest value in ydata
    min_y_value: float
        The lowest value in ydata
    yrange: Optional[Tuple]
        The range of zoom on Y axis

    Returns
    -------
    plot: bkfigure
        plot with added tags
    """
    if tagstype == 'single':
        trimmed_tagstimestamps = list()
        for t in tags:
            trimmed_tagstimestamps.append({'name': t['name'],
                                           'timestamp': t['timestamp']+trimxvaluesoffset})  # noqa: 501
        tags = trimmed_tagstimestamps

        for t in tags:
            span = Span(location=t["timestamp"],
                        line_dash='dashed',
                        dimension='height',
                        line_color='thistle',
                        line_width=2)
            plot.add_layout(span)

        # Calculating the tags positions, so that they are
        # in two rows for better readability
        if yrange is None:
            first_row = (max_y_value-min_y_value)*0.96 + min_y_value
            second_row = (max_y_value-min_y_value)*0.9 + min_y_value
        else:
            first_row = (yrange[1]-yrange[0])*0.96 + yrange[0]
            second_row = (yrange[1]-yrange[0])*0.9 + yrange[0]

        tags_ylocations = [second_row, first_row] * \
            (int(len(tags)/2)) + [second_row]*(len(tags) % 2)

        source = ColumnDataSource(data={"timestamps": [tag["timestamp"]
                                                       for tag in tags],
                                        "y": tags_ylocations,
                                        "names": [tag["name"]
                                                  for tag in tags]})

        labels = LabelSet(x='timestamps', y='y', text='names',
                          source=source)
        plot.add_layout(labels)

    else:
        trimmed_tagstimestamps = list()
        for t in tags:
            trimmed_tagstimestamps.append({'name': t['name'],
                                           'start': t['start']+trimxvaluesoffset,  # noqa: 501
                                           'end': t['end']+trimxvaluesoffset})
            tags = trimmed_tagstimestamps

        tags_names = list()

        for d in tags:
            if d['name'] not in tags_names:
                tags_names.append(d['name'])

        # 3 is minimum number of colors in the palette
        colors = palette['Category10'][max(3, len(tags_names))]
        tags_colors = dict()

        for id, name in enumerate(tags_names):
            tags_colors[name] = colors[id]

        xdatatags = dict()
        widths = dict()

        for tn in tags_names:
            xdatatags[tn] = list()
            widths[tn] = list()

        for t in tags:
            xdatatags[t['name']].append((t['start']+t['end'])/2)
            widths[t['name']].append(t['start']-t['end'])

        for t in tags_names:
            plot.rect(x=xdatatags[t], y=(min_y_value+max_y_value)/2,
                      height=(max_y_value-min_y_value), width=widths[t],
                      color=tags_colors[t], alpha=0.2,
                      muted_color=tags_colors[t], muted_alpha=0,
                      legend_label=t)

        plot.legend.location = "top_left"
        plot.legend.click_policy = "mute"
        plot.legend.location = "top_left"

    return plot


def time_series_plot(
        title: str,
        xtitle: str,
        xunit: str,
        ytitle: str,
        yunit: str,
        xdata: List,
        ydata: List,
        xrange: Optional[Tuple] = None,
        yrange: Optional[Tuple] = None,
        trimxvaluesoffset: float = 0.0,
        figsize: Tuple = (1500, 850),
        tags: List = [],
        tagstype: str = 'single',
        data_colors: List = [],
        switchtobarchart: bool = False):
    """
    Returns time series plot.

    Used i.e. for timeline of resource usage.

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
    trimxvaluesoffset : float
        Value of the minimum x before trimming
    figsize: Tuple
        The size of the figure
    tags: list
        List of tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    data_colors:
        List of colors for which the data in the plot will be colored
    switchtobarchart:
        True if we want to change the plot type to barchart

    Returns
    -------
    plot: bkfigure
        Returns time series plot
    """

    xlabel = xtitle
    if xunit is not None:
        xlabel += f' [{xunit}]'
    ylabel = ytitle
    if yunit is not None:
        ylabel += f' [{yunit}]'

    plot = bkfigure(width=int(figsize[0]),
                    height=figsize[1],
                    min_border=10,
                    title=title,
                    x_axis_label=xlabel,
                    y_axis_label=ylabel,
                    x_axis_type="datetime",
                    toolbar_location=None,
                    output_backend='webgl')

    if xrange is not None:
        plot.x_range = Range1d(xrange[0], xrange[1])
    if yrange is not None:
        plot.y_range = Range1d(yrange[0], yrange[1])

    # adding tagging visualizations to the plot
    if len(tags) > 0:
        plot = add_tags(plot,
                        tags,
                        tagstype,
                        trimxvaluesoffset=-trimxvaluesoffset,
                        max_y_value=max(ydata),
                        min_y_value=min(ydata),
                        yrange=yrange)

    plot.title.text_font_size = 'large'
    plot.xaxis.axis_label_text_font_size = '14pt'
    plot.yaxis.axis_label_text_font_size = '14pt'

    if len(data_colors) == 0:
        data_colors = "navy"

    if switchtobarchart is True:
        plot.quad(top=ydata[:-1],
                  bottom=0,
                  left=xdata[:-1],
                  right=xdata[1:],
                  fill_color=data_colors,
                  line_color=data_colors)
    else:
        plot.scatter(x=xdata, y=ydata, size=10, color=data_colors)

    return plot


def value_histogram(
        ydata: List,
        yrange: Optional[Range1d] = None,
        figsize: Tuple = (1500, 850),
        bins: int = 20,
        setgradientcolors: bool = False):
    """
    Returns the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydata : List
        The values for Y dimension
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    setgradientcolors: bool
        True if gradient colors from turquoise to raspberry red
        instead of one color should be set. False otherwise.

    Returns
    -------
    plot: bkfigure
        the histogram with logarithmic scale on x-axis
    """

    plot = bkfigure(plot_width=int(figsize[0]),
                    plot_height=figsize[1],
                    min_border=10,
                    x_axis_label='Value histogram',
                    x_axis_type='log',
                    toolbar_location="above",
                    tools="save",
                    y_range=yrange,
                    output_backend='webgl')

    plot.yaxis.visible = False
    plot.x_range.start = 1
    plot.xaxis.axis_label_text_font_size = '14pt'

    hist, edges = np.histogram(ydata, bins=bins)

    data_colors = "navy"
    if setgradientcolors is True:
        data_colors = get_colors(edges[:-1])

    plot.quad(top=edges[1:], bottom=edges[:-1], left=hist, right=0.00001,
              fill_color=data_colors, line_color=data_colors, alpha=1)

    return plot


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
        axhist.hist(ydatas[0], bins=bins, orientation='horizontal', color='purple')
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

    ts_plot = time_series_plot(
        title,
        xtitle,
        xunit,
        ytitle,
        yunit,
        xdata,
        ydata,
        xrange,
        yrange,
        minx,
        # plots should be in a ratio of 8:3
        figsize=(figsize[0]*8/11, figsize[1]),
        tags=tags,
        tagstype=tagstype
    )

    val_hist = value_histogram(
        ydata,
        ts_plot.y_range,
        # plots should be in a ratio of 8:3
        figsize=(figsize[0]*3/11, figsize[1]),
        bins=bins
    )

    plot = gridplot([ts_plot, val_hist], ncols=2)
    if outpath is None:
        show(plot)
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

    if "html" in outputext:
        output_file(f'{outpath}.html', title=title, mode='inline')
        save(plot)

    plot = gridplot([ts_plot, val_hist], ncols=2, toolbar_location=None)

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

    if "png" in outputext and backend == "bokeh":
        export_png(plot, filename=f'{outpath}.png')
    if "svg" in outputext and backend == "bokeh":
        export_svg(plot, filename=f'{outpath}.svg')


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


    ts_plots = []
    val_histograms = []

    for subtitle, xtitle, xunit, ytitle, yunit, ydata in zip(subtitles, xtitles, xunits, ytitles, yunits, ydatas):  # noqa: E501
        ts_plots.append(time_series_plot(
            subtitle,
            xtitle,
            xunit,
            ytitle,
            yunit,
            xdata,
            ydata,
            xrange,
            yrange,
            trimxvaluesoffset=minx,
            # plots should be in a ratio of 8:3
            figsize=(figsize[0]*8/11, figsize[1]//plotsnumber),
            data_colors=get_colors(ydata[0:-1]),
            switchtobarchart=switchtobarchart,
            tags=tags,
            tagstype=tagstype
        ))

        val_histograms.append(value_histogram(
            list(np.float_(ydata)),
            ts_plots[-1].y_range,
            # plots should be in a ratio of 8:3
            figsize=(figsize[0]*3/11, figsize[1]//plotsnumber),
            bins=bins,
            setgradientcolors=True
        ))

    div = Div(text=title)

    plots = [[div]]
    for ts_plot, val_hist in zip(ts_plots, val_histograms):
        plots.append([ts_plot, val_hist])

    multiple_plot = gridplot(plots, merge_tools=True)
    if outpath is None:
        show(multiple_plot)

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

    if "html" in outputext:
        output_file(f"{outpath}.html", title=title, mode='inline')
        save(multiple_plot)

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

    multiple_plot = gridplot(
        plots, merge_tools=True, toolbar_location=None)

    if "png" in outputext and backend == "bokeh":
        export_png(multiple_plot, filename=f"{outpath}.png")

    if "svg" in outputext and backend == "bokeh":
        export_svg(multiple_plot, filename=f"{outpath}.svg")
