import json
from time_series_plot import render_time_series_plot_with_histogram

with open("data1.json", "r") as data:
    data = json.load(data)

xdata = data[0]
ydata = data[1]

tags = []
for tag in data[2]:
    tags.append({
        'name':  tag[0],
        'start': float(tag[1]),
        'end':   float(tag[2])
    })

render_time_series_plot_with_histogram(
    "example_plots/singleplot",
    ["txt", "html", "png"],
    "Example plot",
    "X axis",
    "unit",
    "Y axis",
    "unit",
    xdata,
    ydata,
    tags=tags,
    tagstype="double"
)
