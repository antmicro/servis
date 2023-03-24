import json
from servis import render_multiple_time_series_plot

with open("data2.json", "r") as data:
    data = json.load(data)

xdata = data["xdata"]
ydata1 = data["ydata1"]
ydata2 = data["ydata2"]

tags = []
for tag in data["tags"]:
    tags.append({
        'name':  tag[0],
        'timestamp': float(tag[1])
    })

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
    outpath="example_plots/multipleplot",
    outputext=["txt", "html"],
    tags=[tags]*2,
    tagstype="single",
    backend="matplotlib",
    is_x_timestamp=False,
    setgradientcolors=True
)
