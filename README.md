# Servis

A repository for rendering time series plots in various formats.

Examples of projects using the module:

* [Kenning](https://github.com/antmicro/kenning)
* [Sargraph](https://github.com/antmicro/sargraph)

## Requirements

The module requires:

* [NumPy](https://numpy.org/),
* [plotext](https://github.com/piccolomo/plotext),
* [Bokeh](https://bokeh.org/),
* [Selenium](https://www.selenium.dev/),
* [geckodriver](https://github.com/mozilla/geckodriver).

## Examples of running Servis

### Rendering single plot in all possible extensions

example script:

```python
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
    tagstype="double"
)
```

running script from terminal:


```bash
python3 test1.py
```

Generated plot with PNG extension:

![inference plot](example_plots/singleplot.png)


### Rendering double plot:

example script:

```python
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
    yrange=(-5, 105),
    tags=tags,
    tagstype="single",
    figsize=(100, 20)
)
```

running script from terminal:


```bash
python3 test2.py
```

Generated TXT plot:

![txt plot](example_plots/txtplot.png)

Example PNG double plot:

![interactive sargraph](example_plots/multipleplot.png)
