import json
from time_series_plot import render_multiple_time_series_plot

with open("data2.json", "r") as data:
    data = json.load(data)

xdata = data[0]
ydata1 = data[1]
ydata2 = data[2]

tags = []
for tag in data[3]:
    tags.append({
        'name':  tag[0],
        'timestamp': float(tag[1])
    })

render_multiple_time_series_plot(
    2,
    "example_plots/multipleplot",
    ["txt"],
    "Example plot",
    ["Plot1", "Plot2"],
    ["X axis"]*2,
    ["unit"]*2,
    ["Y axis"]*2,
    ["unit"]*2,
    xdata,
    [ydata1, ydata2],
    tags=tags,
    tagstype="single",
    figsize=(100, 20)
)

render_multiple_time_series_plot(
    2,
    "example_plots/multipleplot",
    ["png"],
    "Example plot",
    ["Plot1", "Plot2"],
    ["X axis"]*2,
    ["unit"]*2,
    ["Y axis"]*2,
    ["unit"]*2,
    xdata,
    [ydata1, ydata2],
    tags=tags,
    tagstype="single",
    figsize=(1500, 800)
)
