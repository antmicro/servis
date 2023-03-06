from typing import Union, Iterable, Iterator, Optional
import itertools

DEFAULT_COLOR = '#E74A3C'


class ColorMapNotFound(Exception):
    def __init__(self, name: str, quantity: int):
        super().__init__()
        self.name = name
        self.quantity = quantity

    def __str__(self):
        return super().__str__() + \
            f"Cannot find colormap with {self.name=} and {self.quantity=}"


def get_color_iterator(name: str, quantity: int = 3):
    """
    Function for retriving colormaps from bokeh or matplotlib

    Parameters
    ----------
    name : str
        Name of the colormap
    quantity : int
        Number of colors needed

    Returns
    -------
    Iterator
        Iterator with colors from speficied colormap

    Raises
    ------
    ColorMapNotFound
        If the colormap was not found
    """
    try:
        from bokeh.palettes import all_palettes
        return iter(all_palettes[name][quantity if quantity >= 3 else 3])
    except Exception:
        pass
    try:
        from matplotlib import colormaps
        return iter(colormaps[name](
            list(map(lambda x: x / quantity, range(0, quantity)))))
    except Exception:
        pass
    raise ColorMapNotFound(name, quantity)


def _to_matplotlib(value: Union[str, Iterable]) -> Iterable:
    """
    Function converting input to proper matplotlib color format
    - tuple of 3 floats

    Parameters
    ----------
    value : Union[str, Iterable]

    Returns
    -------
    Iterable
        Color in matplotlib format
    """
    if isinstance(value, str):
        t = []
        for i in range(1, 7, 2):
            t.append(int(value[i:i + 2], 16) / 255)
        return tuple(t)
    return value


def _to_bokeh(value: Union[str, Iterable]) -> str:
    """
    Function converting input to proper bokeh color format
    - string with 3 hex numbers

    Parameters
    ----------
    value : Union[str, Iterable]

    Returns
    -------
    Iterable
        Color in bokeh format
    """
    if not isinstance(value, str):
        values = list(map(lambda x: round(x*255), value))
        return '#'+''.join(f"{v:02X}" for v in values[:3])
    return value


def get_colormap_for_bokeh(name: str, quantity: int = 3) -> Iterator[str]:
    """
    Parameters
    ----------
    name : str
        Name of the colormap
    quantity: int
        Number of colors needed

    Returns
    -------
    Iterator[str]
        Iterator with colors from specified colormap in bokeh format
    """
    return map(_to_bokeh, get_color_iterator(name, quantity))


def get_colormap_for_matplotlib(name: str, quantity: int = 3) -> Iterator:
    """
    Parameters
    ----------
    name : str
        Name of the colormap
    quantity: int
        Number of colors needed

    Returns
    -------
    Iterator[str]
        Iterator with colors from specified colormap in bokeh format
    """
    return map(_to_matplotlib, get_color_iterator(name, quantity))


def validate_colormap(
    colormap: Optional[Union[str, Iterable]],
    for_backend: str,
    quantity: int = 3
):
    """
    Function for validating and creating colormap for specified backend.

    Parameters
    ----------
    colormap : str | Iterable | None
        Name of the colormap or iterable object with colors or None
    for_backend : str
        Either 'bokeh' or 'matplotlib' - specifies in which backend this
        color will be used
    quantity : int
        Number of colors needed

    Returns
    -------
    Iterator
        Iterator with colors from chosen colormap, prepared for specified
        backend

    Raises
    ------
    ColorMapNotFound
        If the colormap was not found
    """
    assert for_backend in ('bokeh', 'matplotlib'), (
        "Only avaible options for for_backend are: bokeh, matplotlib")
    if for_backend == 'bokeh':
        get_colormap = get_colormap_for_bokeh
    elif for_backend == 'matplotlib':
        get_colormap = get_colormap_for_matplotlib

    if colormap is None and quantity == 1:
        colors = iter([DEFAULT_COLOR])
    elif colormap is None and quantity > 1:
        colors = itertools.chain(
            [DEFAULT_COLOR], get_colormap("Set1", quantity - 1))
    elif isinstance(colormap, str):
        colors = get_colormap_for_matplotlib(colormap, quantity)
    else:
        assert len(colormap) >= quantity, (
            "There has to be, at least, the same number of colors "
            "as sets of data")
        colors = iter(colormap)
    return colors
