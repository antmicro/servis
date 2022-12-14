from typing import List, Dict, Tuple, Optional
from bokeh.plotting import output_file, show, save, figure as bkfigure
from bokeh.models import Range1d, ColumnDataSource, Span, LabelSet, Div
from numpy import histogram, float_
from bokeh.io import export_png, export_svg
from pathlib import Path
from bokeh.layouts import gridplot
import re


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

    colors = [
        "#09B194",
        "#1FB59C",
        "#34BBA4",
        "#45BFAA",
        "#5DC5B3",
        "#6FC9B9",
        "#82CDC0",
        "#98D3C9",
        "#ABD7D0",
        "#C9DAD6",
        "#E3CFCD",
        "#E5C0BD",
        "#E6B2AD",
        "#E7A6A0",
        "#E6968F",
        "#E68880",
        "#E77B72",
        "#E66E64",
        "#E65F52",
        "#E74C3E",
    ]

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
            trimmed_tagstimestamps.append({
                'name': t['name'],
                'timestamp': t['timestamp']+trimxvaluesoffset})
        tags = trimmed_tagstimestamps

        for t in tags:
            span = Span(location=t["timestamp"],
                        line_dash='dashed',
                        dimension='height',
                        line_color='#424B54',
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
            trimmed_tagstimestamps.append({
                'name': t['name'],
                'start': t['start']+trimxvaluesoffset,
                'end': t['end']+trimxvaluesoffset})
            tags = trimmed_tagstimestamps

        tags_names = list()

        for d in tags:
            if d['name'] not in tags_names:
                tags_names.append(d['name'])

        palette = ["#01B47E",
                   "#332D37",
                   "#4088F4",
                   "#F15F32"]

        colors = palette[0:len(tags_names)]
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
        plot.legend.title_text_font = "Lato"
        plot.legend.label_text_font = "Lato"

    return plot


def time_series_plot(
        ydata: List,
        xdata: List,
        title: Optional[str],
        xtitle: Optional[str],
        xunit: Optional[str],
        ytitle: Optional[str],
        yunit: Optional[str],
        x_range: Optional[Tuple] = None,
        y_range: Optional[Tuple] = None,
        trimxvaluesoffset: float = 0.0,
        figsize: Tuple = (1500, 850),
        tags: List = [],
        tagstype: str = 'single',
        setgradientcolors: bool = False,
        plottype: str = 'scatter'):
    """
    Returns time series plot.

    Used i.e. for timeline of resource usage.

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
    trimxvaluesoffset: float
        The number by which the values will be trimmed
    figsize: Tuple
        The size of the figure
    tags: list
        List of tags and their timestamps
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    setgradientcolors:
        True if gradient colors instead of one color should be set.
        False otherwise.
    plottype: str
        Can be 'scatter' or 'bar'

    Returns
    -------
    plot: bkfigure
        Returns time series plot
    """
    assert plottype in ['scatter', 'bar']
    xlabel = None
    if xtitle:
        xlabel = xtitle
        if xunit is not None:
            xlabel += f' [{xunit}]'

    ylabel = None
    if ytitle:
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

    if x_range is not None:
        plot.x_range = Range1d(x_range[0], x_range[1])
    if y_range is not None:
        plot.y_range = Range1d(y_range[0], y_range[1])

    # adding tagging visualizations to the plot
    if len(tags) > 0:
        plot = add_tags(plot,
                        tags,
                        tagstype,
                        trimxvaluesoffset=-trimxvaluesoffset,
                        max_y_value=max(ydata),
                        min_y_value=min(ydata),
                        yrange=y_range)

    if title:
        plot.title.text_font_size = '18pt'
        plot.title.text_font = 'Lato'
    if xtitle:
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font_style = 'normal'
        plot.xaxis.axis_label_text_font = 'Lato'
    if ytitle:
        plot.yaxis.axis_label_text_font_size = '14pt'
        plot.yaxis.axis_label_text_font_style = 'normal'
        plot.yaxis.axis_label_text_font = 'Lato'

    data_colors = "#E74A3C"
    if setgradientcolors is True:
        data_colors = get_colors(ydata[0:-1])

    if plottype == 'bar':
        plot.quad(top=ydata[:-1],
                  bottom=0,
                  left=xdata[:-1],
                  right=xdata[1:],
                  fill_color=data_colors,
                  line_color=data_colors)
    elif plottype == 'scatter':
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
    plot.xaxis.axis_label_text_font_style = 'normal'
    plot.xaxis.axis_label_text_font = 'Lato'

    hist, edges = histogram(ydata, bins=bins)

    data_colors = "#E74A3C"
    if setgradientcolors is True:
        data_colors = get_colors(edges[:-1])

    plot.quad(top=edges[1:], bottom=edges[:-1], left=hist, right=0.00001,
              fill_color=data_colors, line_color=data_colors, alpha=1)

    return plot


def add_font_url_to_html(filename: Path):
    """
    Adds font url to created html file

    Parameters
    ----------
    filename : Path
    the path to html file to which the link will be added
    """

    pattern = '<head>'
    head_location = None
    font_line = r'    <link rel="preload" href="https://fonts.googleapis.com/css?family=Lato">'+"\n"  # noqa: E501
    with open(filename, 'r') as file:
        content = file.readlines()

    for line in content:
        r = re.search(pattern, line)
        if r is not None:
            head_location = r.span()[0]

    if head_location is None:
        raise Exception("Head not found in HTML file")

    content.insert(head_location+1, font_line)

    with open(filename, 'w') as file:
        content = "".join(content)
        file.write(content)


def create_bokeh_plot(
        ydatas: List[List],
        xdatas: List[List],
        title: Optional[str],
        subtitles: Optional[List[str]],
        xtitles: Optional[List[str]],
        xunits: Optional[List[str]],
        ytitles: Optional[List[str]],
        yunits: Optional[List[str]],
        x_ranges: Optional[List[Tuple]] = None,
        y_ranges: Optional[List[Tuple]] = None,
        outpath: Optional[Path] = None,
        outputext: Optional[List[str]] = ['html'],
        trimxvaluesoffsets: Optional[List[float]] = [],
        figsize: Tuple = (1500, 1080),
        bins: int = 20,
        plottype: str = 'scatter',
        tags: List[List[Dict]] = [],
        tagstype: str = "single",
        setgradientcolors: bool = False):
    """
    Draws and saves time series plot using Bokeh

    Parameters
    ----------
    ydatas : List[List]
        The list of lists of values for Y dimension for every plot
    xdatas : List[List]
        The list of lists of values for X dimension for every plot
    title : Optional[List[str]]
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
    outputext: List[str]
        Extension of generated file.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvaluesoffsets: List[float]
        The  list of offsets - numbers by which the tags timestamps values
        will be trimmed
    figsize: Tuple
        The size of the figure
    bins: int
        Number of bins for value histograms
    plottype: str
        Can be 'scatter' or 'bar'
    tags: list
        List of tags and their timestamps for each X-axis
    tagstype: str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    """

    ts_plots = []
    val_histograms = []

    plotsnumber = len(ydatas)

    if xtitles is None:
        xtitles = [None for _ in range(plotsnumber)]
    if xunits is None:
        xunits = [None for _ in range(plotsnumber)]
    if ytitles is None:
        ytitles = [None for _ in range(plotsnumber)]
    if yunits is None:
        yunits = [None for _ in range(plotsnumber)]
    if len(trimxvaluesoffsets) == 0:
        trimxvaluesoffsets = [0 for i in range(plotsnumber)]
    if len(tags) == 0:
        tags = [[] for i in range(plotsnumber)]

    for subtitle, xtitle, xunit, ytitle, yunit, xdata, ydata, \
            trimxvaluesoffset, tags_for_one_plot, x_range, y_range in \
            zip(subtitles, xtitles, xunits, ytitles, yunits, xdatas,
                ydatas, trimxvaluesoffsets, tags, x_ranges, y_ranges):
        ts_plots.append(time_series_plot(
            ydata,
            xdata,
            subtitle,
            xtitle,
            xunit,
            ytitle,
            yunit,
            x_range,
            y_range,
            trimxvaluesoffset=trimxvaluesoffset,
            # plots should be in a ratio of 8:3
            figsize=(figsize[0]*8/11, figsize[1]//plotsnumber),
            tags=tags_for_one_plot,
            tagstype=tagstype,
            setgradientcolors=setgradientcolors,
            plottype=plottype
        ))

        val_histograms.append(value_histogram(
            list(float_(ydata)),
            ts_plots[-1].y_range,
            # plots should be in a ratio of 8:3
            figsize=(figsize[0]*3/11, figsize[1]//plotsnumber),
            bins=bins,
            setgradientcolors=setgradientcolors
        ))

    if title:
        div = Div(text=f'<p style="font-family:Lato"> {title}')
        plots = [[div]]
    else:
        plots = []

    for ts_plot, val_hist in zip(ts_plots, val_histograms):
        plots.append([ts_plot, val_hist])

    multiple_plot = gridplot(plots, merge_tools=True)
    if outpath is None:
        show(multiple_plot)

    if "html" in outputext:
        output_file_name = f"{outpath}.html"
        output_file(output_file_name, title=title, mode='inline')
        save(multiple_plot)

        add_font_url_to_html(output_file_name)

    multiple_plot = gridplot(
        plots, merge_tools=True, toolbar_location=None)

    if "png" in outputext:
        export_png(multiple_plot, filename=f"{outpath}.png")

    if "svg" in outputext:
        export_svg(multiple_plot, filename=f"{outpath}.svg")
