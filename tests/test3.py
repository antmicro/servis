import json
from servis import render_multiple_time_series_plot

with open("data1.json", "r") as data:
    data = json.load(data)

xdata0 = data["xdata"]
ydata0 = data["ydata"]

tags1 = []
for tag in data["tags"]:
    tags1.append({
        'name':  tag[0],
        'start': float(tag[1]),
        'end':   float(tag[2])
    })

with open("data2.json", "r") as data:
    data = json.load(data)

xdata1 = data["xdata"]
ydata1 = data["ydata1"]
ydata2 = data["ydata2"]

tags2 = []
for tag in data["tags"]:
    tags2.append({
        'name':  tag[0],
        'timestamp': float(tag[1])
    })

COLORS = [
    "#ab47bd",  # purple
    "#4051b5",  # indigo
    "#ef5552",  # red
]

render_multiple_time_series_plot(
    [[ydata0], [ydata1, ydata2]],
    [[xdata0], [xdata1]*2],
    title="Example plot",
    subtitles=["Plot1", "Plot2"],
    xtitles=["X axis"]*2,
    xunits=["unit"]*2,
    ytitles=["Y axis"]*2,
    yunits=["unit"]*2,
    outpath="example_plots/multifigures",
    outputext=["png", "svg", "html", "txt"],
    tags=[tags1, tags2],
    tagstype=["double", "single"],
    backend="matplotlib",
    colormap=COLORS,
    legend_labels=["Data1", "Data2", "Data3"]
)
