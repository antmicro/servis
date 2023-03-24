import json
from servis import render_time_series_plot_with_histogram

with open("data1.json", "r") as data:
    data = json.load(data)

xdata = data["xdata"]
ydata = data["ydata"]

tags = []
for tag in data["tags"]:
    tags.append({
        'name':  tag[0],
        'start': float(tag[1]),
        'end':   float(tag[2])
    })

render_time_series_plot_with_histogram(
    ydata,
    xdata,
    "Example plot",
    "X axis",
    "unit",
    "Y axis",
    "unit",
    outpath="example_plots/singleplot",
    outputext=["txt", "html", "png", "svg"],
    tags=tags,
    tagstype="double",
    backend="matplotlib"
)
