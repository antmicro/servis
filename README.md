# Servis

A repository for rendering time series plots in various formats.

Examples of projects using the module:

* [Kenning](https://github.com/antmicro/kenning)
* [Sargraph](https://github.com/antmicro/sargraph)

## Requirements

The module requires:

* [NumPy](https://numpy.org/),
* [plotext](https://github.com/piccolomo/plotext),
* [Bokeh](https://bokeh.org/)

Optional dependencies for exporting png/svg plots using Bokeh:

* [Selenium](https://www.selenium.dev/),
* [geckodriver](https://github.com/mozilla/geckodriver).

## Examples of running Servis

### Rendering TXT plots from standard input

Servis can be run from terminal using:

```
python -m servis -h
```

It can accept a file with space-separated values, representing Y (and optionally X) values.
It can also accept data from standard input.

For example, let's create a file `sample.txt`:

```
1 0
2 1
4 2
8 3
16 4
```

The data can be provided two ways:

```
cat sample.txt | python -m servis
```

or:

```
python -m servis sample.txt
```

It is possible to control the delimiter and plot type - check help (`python -m servis -h`) for details.

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
    [ydata1, ydata2],
    xdata,
    title="Example plot",
    subtitles=["Plot1", "Plot2"],
    xtitles=["X axis"]*2,
    xunits=["unit"]*2,
    ytitles=["Y axis"]*2,
    yunits=["unit"]*2,
    y_range=(-5, 105),
    outpath="example_plots/multipleplot",
    outputext=["png", "html"],
    tags=tags,
    tagstype="single",
    backend="matplotlib"
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
