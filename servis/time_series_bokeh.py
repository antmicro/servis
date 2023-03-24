from typing import List, Dict, Tuple, Optional, Iterator, Union
from bokeh.plotting import (
    output_file, show, save, figure as bkfigure, Figure, column
)
from bokeh.models import (
    Range1d, ColumnDataSource, Span, LabelSet, Div,
    Legend, BoxAnnotation, LegendItem, CustomJS
)
from bokeh.io import export_png, export_svg
from pathlib import Path
from bokeh.layouts import gridplot
from collections import defaultdict
import re

from servis.utils import (
    validate_colormap, DEFAULT_COLOR,
    DEFAULT_ANNOTATION_COLORS, validate_kwargs,
    range_over_lists, histogram
)

BETWEEN_SECTION_MARGIN_PERCENT = 0.1
BETWEEN_BAR_MARGIN_PERCENT = 0.
LEGEND_COLUMNS = 3
NOT_SUPPORTED_PARAMS = {
    'is_x_timestamp'
}


def get_colors(data: List):
    """
    Generates list of colors for elements in data,
    depending on their value.

    Elements with value between 0 and 5 are turquoise
    and the color changes to redder every 5 percentage
    points.

    Parameters
    ----------
    data : List
        List of values for which the colors will be generated.

    Returns
    -------
    data_colors : List
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
        data_colors.append(colors[round(float(d)) // 5])
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
    tagstype : str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    trimxvaluesoffset : float
        The number by which the values will be trimmed
    max_y_value : float
        The highest value in ydata
    min_y_value : float
        The lowest value in ydata
    yrange : Optional[Tuple]
        The range of zoom on Y axis

    Returns
    -------
    plot : bkfigure
        plot with added tags
    """
    if tagstype == 'single':
        trimmed_tagstimestamps = list()
        for t in tags:
            trimmed_tagstimestamps.append({
                'name': t['name'],
                'timestamp': t['timestamp'] + trimxvaluesoffset})
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
            first_row = (max_y_value - min_y_value) * 0.96 + min_y_value
            second_row = (max_y_value - min_y_value) * 0.9 + min_y_value
        else:
            first_row = (yrange[1] - yrange[0]) * 0.96 + yrange[0]
            second_row = (yrange[1] - yrange[0]) * 0.9 + yrange[0]

        tags_ylocations = [second_row, first_row] * \
            (int(len(tags) / 2)) + [second_row] * (len(tags) % 2)

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
                'start': t['start'] + trimxvaluesoffset,
                'end': t['end'] + trimxvaluesoffset})
        tags = trimmed_tagstimestamps
        tags_names = set(tag['name'] for tag in tags)

        palette = DEFAULT_ANNOTATION_COLORS  # TODO: param for annotaion colors
        assert len(palette) >= len(tags_names), (
            f"Number of colors avaiable ({len(palette)}) has to be greater"
            f" or equal number of tags ({len(tags_names)})")
        tags_colors = {name: palette[id] for id, name in enumerate(tags_names)}

        tags_annotations = defaultdict(list)
        for tag in tags:
            tags_annotations[tag['name']].append(
                BoxAnnotation(left=tag['start'], right=tag['end'],
                              fill_color=tags_colors[tag['name']],
                              fill_alpha=0.2, line_alpha=0.0)
            )
            plot.add_layout(tags_annotations[tag['name']][-1])
        legend_items = []
        for name in sorted(tags_names):
            # Creating dummy object for legend
            renderer = plot.rect(
                x=0, y=0,
                width=0, height=0,
                color=tags_colors[name],
                alpha=0.2, muted_alpha=0.0)
            # Event hidding annotations if dummy object is hidden
            renderer.js_on_change('muted', CustomJS(
                args=dict(boxes=tags_annotations[name]),
                code="""
                    const m = cb_obj.muted;
                    for (let box of boxes){
                        box.visible = !m;
                }
                """
            ))
            legend_items.append(LegendItem(label=name, renderers=[renderer]))
        # Add legend to the plot
        plot.add_layout(Legend(
            location="top_left",
            label_text_font="Lato",
            click_policy='mute',
            items=legend_items,
        ))

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
        colors: Optional[Iterator[str]] = None,
        setgradientcolors: bool = False,
        plottype: str = 'scatter',
        figure: Optional[Figure] = None):
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
    figsize : Tuple
        The size of the figure
    tags : list
        List of tags and their timestamps
    tagstype : str
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps.
    colors : Optional[Iterator[str]]
        Iteretor with colors for sets of data
    setgradientcolors : bool
        True if gradient colors instead of one color should be set.
        False otherwise.
    plottype : str
        Can be 'scatter' or 'bar'
    figure : Optional[bokeh.plotting.Figure]
        Figure to make plot

    Returns
    -------
    plot : bkfigure
        Bokeh figure with time series plot
    glyph :
        Glyph containing reference to scatter or bar plot, which can be
        connected with legend entry
    """
    assert plottype in ['scatter', 'bar']

    if figure is None:
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
                        output_backend='webgl',)

        if title:
            plot.title.text_font_size = '18pt'
            plot.title.text_font = 'Lato'
        if xtitle:
            plot.xaxis.axis_label_text_font_size = '14pt'
            plot.xaxis.axis_label_text_font = 'Lato'
        if ytitle:
            plot.yaxis.axis_label_text_font_size = '14pt'
            plot.yaxis.axis_label_text_font = 'Lato'

        if x_range is not None:
            plot.x_range = Range1d(x_range[0], x_range[1])
        if y_range is not None:
            plot.y_range = Range1d(y_range[0], y_range[1])

    else:
        plot = figure

    # adding tagging visualizations to the plot
    if tags and len(tags) > 0:
        plot = add_tags(plot,
                        tags,
                        tagstype,
                        trimxvaluesoffset=-trimxvaluesoffset,
                        max_y_value=max(ydata),
                        min_y_value=min(ydata),
                        yrange=y_range)

    if setgradientcolors is True:
        data_colors = get_colors(ydata[:-1])
    elif colors is not None:
        data_colors = next(colors)
    else:
        data_colors = DEFAULT_COLOR

    if title is None:
        title = ""
    if plottype == 'bar':
        glyph = plot.quad(top=ydata[:-1],
                          bottom=0,
                          left=xdata[:-1],
                          right=xdata[1:],
                          fill_color=data_colors,
                          line_color=data_colors)
    elif plottype == 'scatter':
        glyph = plot.scatter(x=xdata, y=ydata, size=6,
                             alpha=0.5, line_color=None,
                             color=data_colors)

    return plot, glyph


def value_histogram(
        ydata: List,
        yrange: Optional[Range1d] = None,
        figsize: Tuple = (1500, 850),
        bins: int = 20,
        colors: Optional[Iterator[str]] = None,
        setgradientcolors: bool = False,
        histogram_range: Tuple = None,
        data_id: Optional[int] = None,
        data_len: Optional[int] = None,
        figure: Optional[Figure] = None):
    """
    Returns the histogram of values that appeared throughout the
    experiment.

    Parameters
    ----------
    ydata : List
        The values for Y dimension
    yrange : Optional[Tuple]
        The range of zoom on Y axis
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    colors : Optional[Iterator[str]]
        Iteretor with colors for sets of data
    setgradientcolors : bool
        True if gradient colors from turquoise to raspberry red
        instead of one color should be set. False otherwise.
    histogram_range : Optional[Tuple]
        Union of ranges of all sets of data
    data_id : Optional[int]
        Number of set
    data_len : Optional[int]
        Quantity of sets
    figure : Optional[bokeh.plotting.Figure]
        Figure to make plot

    Returns
    -------
    plot : bkfigure
        Bokeh figure with histogram plot with logarithmic scale
    glyph :
        Glyph containing reference to histogram plot, which can be
        connected with legend entry
    """

    if figure is None:
        plot = bkfigure(plot_width=int(figsize[0]),
                        plot_height=figsize[1],
                        min_border=10,
                        x_axis_type='log',
                        toolbar_location="above",
                        tools="save",
                        y_range=yrange,
                        output_backend='webgl',)

        plot.yaxis.major_tick_line_color = None
        plot.yaxis.minor_tick_line_color = None
        plot.yaxis.major_label_text_color = None
        plot.x_range.start = 0.75
        plot.xaxis.axis_label_text_font_size = '14pt'
        plot.xaxis.axis_label_text_font = 'Lato'
    else:
        plot = figure

    hist, edges = histogram(ydata, bins=bins, bounds=histogram_range)

    if setgradientcolors is True:
        data_colors = get_colors(edges[1:])
    elif colors is not None:
        data_colors = next(colors)
    else:
        data_colors = DEFAULT_COLOR

    if data_id is None or data_len is None:
        tops = edges[1:]
        bottoms = edges[:-1]
    else:
        space_between = edges[1] - edges[0]
        margin = space_between * BETWEEN_SECTION_MARGIN_PERCENT
        bar_width = (space_between - 2*margin) / data_len
        bar_margin = bar_width * BETWEEN_BAR_MARGIN_PERCENT
        bottoms = [e + margin + data_id *
                   bar_width + bar_margin for e in edges[:-1]]
        tops = [b + bar_width - 2*bar_margin for b in bottoms]
    glyph = plot.quad(top=tops, bottom=bottoms,
                      right=hist, left=0.00001, alpha=1,
                      fill_color=data_colors, line_color=data_colors)

    return plot, glyph


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

    content.insert(head_location + 1, font_line)

    with open(filename, 'w') as file:
        content = "".join(content)
        file.write(content)


def create_bokeh_plot(
        ydatas: List[List[List]],
        xdatas: List[List[List]],
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
        tagstype: Union[str, List[str]] = "single",
        colormap: Optional[Union[List, str]] = None,
        setgradientcolors: bool = False,
        legend_labels: List[str] = [],
        **kwargs):
    """
    Draws and saves time series plot using Bokeh

    Parameters
    ----------
    ydatas : List[List[List]]
        The list of lists of lists with values for Y dimension for every plot
    xdatas : List[List[List]]
        The list of lists of lists with values for X dimension for every plot
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
    outputext : List[str]
        Extension of generated file.
        "html" for HTML file,
        "png" for PNG file,
        "svg" for SVG file,
        "txt" for TXT file
    trimxvaluesoffsets : List[float]
        The  list of offsets - numbers by which the tags timestamps values
        will be trimmed
    figsize : Tuple
        The size of the figure
    bins : int
        Number of bins for value histograms
    plottype : str
        Can be 'scatter' or 'bar'
    tags : list
        List of tags and their timestamps for each X-axis
    tagstype : str | List[str]
        "single" if given list contain tags with only one timestamp
        "double" if given list contain tags with two (start and end)
        timestamps or list with desribred values.
    colormap : Optional[Union[List, str]]
        List with colors (in form of sring with hashes or tuple with floats)
        or name of colormap defined in matplotlib or bokeh
    setgradientcolors : bool
        True if gradient colors instead of one color should be set.
        False otherwise.
    legend_labels : List[str]
        List with names used as labels in legend
    """
    validate_kwargs(NOT_SUPPORTED_PARAMS, **kwargs)
    assert not (setgradientcolors and colormap is not None), (
        "setgradientcolors and colormap cannot be used at the same time")

    ts_plots = []
    val_histograms = []

    figsnumber = len(ydatas)

    if len(trimxvaluesoffsets) == 0:
        trimxvaluesoffsets = [0 for i in range(figsnumber)]
    if len(tags) == 0:
        tags = [[] for i in range(figsnumber)]
    if isinstance(tagstype, str):
        tagstype = [tagstype] * figsnumber

    legend_data = []
    for (sub_ydatas, sub_xdatas, subtitle, ytitle, yunit, xtitle, xunit,
         trimxvaluesoffset, tag, tagtype, y_range, x_range) in zip(
        ydatas, xdatas, subtitles, ytitles, yunits, xtitles, xunits,
            trimxvaluesoffsets, tags, tagstype, y_ranges, x_ranges):
        plotsnumbers = len(sub_ydatas)
        plot_colors = validate_colormap(colormap, 'bokeh', plotsnumbers)
        hist_colors = validate_colormap(colormap, 'bokeh', plotsnumbers)
        plot, hist = None, None
        hist_range = range_over_lists(sub_ydatas)
        for i, (ydata, xdata) in enumerate(zip(sub_ydatas, sub_xdatas)):
            plot, points = time_series_plot(
                ydata,
                xdata,
                subtitle,
                xtitle,
                xunit,
                ytitle,
                yunit,
                x_range,
                y_range,
                trimxvaluesoffset,
                colors=plot_colors,
                figsize=(figsize[0] * 8/11, figsize[1] // figsnumber),
                tags=tag,
                tagstype=tagtype,
                setgradientcolors=setgradientcolors,
                plottype=plottype,
                figure=plot
            )
            hist, bars = value_histogram(
                ydata,
                plot.y_range,
                figsize=(figsize[0] * 3/11, figsize[1] // figsnumber),
                bins=bins,
                colors=hist_colors,
                setgradientcolors=setgradientcolors,
                histogram_range=hist_range,
                data_id=i,
                data_len=len(sub_ydatas),
                figure=hist
            )

            tag = None
            legend_data.append([points, bars])
            if xtitle is not None:
                hist.xaxis.axis_label = "Value histogram"

        ts_plots.append(plot)
        val_histograms.append(hist)

    if title:
        div = Div(
            text=f'<h1> {title} </h1>',
            style={
                'font-family': 'Lato',
            }
        )
        plots = [[div]]
    else:
        plots = []

    for ts_plot, val_hist in zip(ts_plots, val_histograms):
        plots.append([ts_plot, val_hist])

    multiple_plot = gridplot(
        plots, merge_tools=True, toolbar_location='above',
        toolbar_options={'logo': None},
    )

    if len(legend_labels) > 0:
        legend_data = [(label, data)
                       for label, data in zip(legend_labels, legend_data)]
        # Creating fake figure for legend
        legend_fig = bkfigure(
            min_border_left=plots[-1][0].width // 5,
            frame_width=0,
            frame_height=11*len(legend_data),
            toolbar_location=None)
        # Creating few columns with legends
        legends = []
        for offset in range(LEGEND_COLUMNS):
            legends.append(
                Legend(items=legend_data[offset::LEGEND_COLUMNS],
                       orientation='vertical',
                       location='center',
                       click_policy='hide')
            )

        legend_fig.xaxis.visible = False
        legend_fig.yaxis.visible = False
        legend_fig.outline_line_alpha = 0.0
        legend_fig.renderers += (
            [legend_item[1][0] for legend_item in legend_data] +
            [legend_item[1][1] for legend_item in legend_data])
        [legend_fig.add_layout(legend, place='right') for legend in legends]
        multiple_plot = column(multiple_plot, legend_fig)

    if outpath is None:
        show(multiple_plot)

    if "html" in outputext:
        output_file_name = f"{outpath}.html"
        output_file(output_file_name, title=title, mode='inline')
        save(multiple_plot)

        add_font_url_to_html(output_file_name)

    multiple_plot = gridplot(
        plots, merge_tools=True,
        toolbar_location=None)
    if len(legend_labels) > 1:
        multiple_plot = column(multiple_plot, legend_fig)

    if "png" in outputext:
        export_png(multiple_plot, filename=f"{outpath}.png")

    if "svg" in outputext:
        export_svg(multiple_plot, filename=f"{outpath}.svg")
