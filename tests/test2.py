from servis import render_multiple_time_series_plot
from utils import data2 as data, OUTPATH_PREFIX, get_tags

xdata = data["xdata"]
ydata1 = data["ydata1"]
ydata2 = data["ydata2"]
tags = get_tags(data)

render_multiple_time_series_plot(
    [ydata1, ydata2],
    [xdata]*2,
    title="Example plot",
    subtitles=["Plot1", "Plot2"],
    xtitles=["X axis"]*2,
    xunits=["unit"]*2,
    ytitles=["Y axis"]*2,
    yunits=["unit"]*2,
    y_ranges=[(-5, 105)]*2,
    outpath=f"{OUTPATH_PREFIX}multipleplot",
    outputext=["png", "html"],
    tags=[tags]*2,
    tagstype="single",
    backend="matplotlib",
    is_x_timestamp=False,
    setgradientcolors=True
)
