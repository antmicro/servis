from utils import data1 as data, OUTPATH_PREFIX, get_tags
from servis import render_time_series_plot_with_histogram

xdata = data["xdata"]
ydata = data["ydata"]
tags = get_tags(data, 'double')

render_time_series_plot_with_histogram(
    ydata,
    xdata,
    "Example plot",
    "X axis",
    "unit",
    "Y axis",
    "unit",
    outpath=f"{OUTPATH_PREFIX}singleplot",
    outputext=["txt", "html", "png", "svg"],
    tags=tags,
    tagstype="double",
    backend="matplotlib"
)
