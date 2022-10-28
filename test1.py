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
    "example_plots/singleplot",
    ["txt", "html", "png", "svg"],
    "Example plot",
    "X axis",
    "unit",
    "Y axis",
    "unit",
    xdata,
    ydata,
    tags=tags,
    tagstype="double",
    backend="matplotlib"
)
