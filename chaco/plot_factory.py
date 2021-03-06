"""
Contains convenience functions to create ready-made PlotRenderer
and PlotFrame instances of various types.
"""

from numpy import array, ndarray, transpose, cos, sin

# Local relative imports
from .abstract_data_source import AbstractDataSource
from .array_data_source import ArrayDataSource
from .axis import PlotAxis
from .barplot import BarPlot
from .data_range_1d import DataRange1D
from .grid import PlotGrid
from .linear_mapper import LinearMapper
from .scatterplot import ScatterPlot
from .polar_mapper import PolarMapper
from .lineplot import LinePlot
from .polar_line_renderer import PolarLineRenderer


def _create_data_sources(data, index_sort="none"):
    """
    Returns datasources for index and value based on the inputs.  Assumes that
    the index data is unsorted unless otherwise specified.
    """
    if (type(data) == ndarray) or (len(data) == 2):
        index, value = data
        if type(index) in (list, tuple, ndarray):
            index = ArrayDataSource(array(index), sort_order=index_sort)
        elif not isinstance(index, AbstractDataSource):
            raise RuntimeError(
                "Need an array or list of values or a DataSource, got %s instead."
                % type(index))

        if type(value) in (list, tuple, ndarray):
            value = ArrayDataSource(array(value))
        elif not isinstance(value, AbstractDataSource):
            raise RuntimeError(
                "Need an array or list of values or a DataSource, got %s instead."
                % type(index))

        return index, value
    else:
        raise RuntimeError("Unable to create datasources.")


def create_scatter_plot(data=[],
                        index_bounds=None,
                        value_bounds=None,
                        orientation="h",
                        color="green",
                        marker="square",
                        marker_size=4,
                        bgcolor="transparent",
                        outline_color="black",
                        border_visible=True,
                        add_grid=False,
                        add_axis=False,
                        index_sort="none"):
    """
    Creates a ScatterPlot from a single Nx2 data array or a tuple of
    two length-N 1-D arrays.  The data must be sorted on the index if any
    reverse-mapping tools are to be used.

    Pre-existing "index" and "value" datasources can be passed in.
    """

    index, value = _create_data_sources(data)

    if index_bounds is not None:
        index_range = DataRange1D(low=index_bounds[0], high=index_bounds[1])
    else:
        index_range = DataRange1D()
    index_range.add(index)
    index_mapper = LinearMapper(range=index_range)

    if value_bounds is not None:
        value_range = DataRange1D(low=value_bounds[0], high=value_bounds[1])
    else:
        value_range = DataRange1D()
    value_range.add(value)
    value_mapper = LinearMapper(range=value_range)

    plot = ScatterPlot(
        index=index,
        value=value,
        index_mapper=index_mapper,
        value_mapper=value_mapper,
        orientation=orientation,
        marker=marker,
        marker_size=marker_size,
        color=color,
        bgcolor=bgcolor,
        outline_color=outline_color,
        border_visible=border_visible, )

    if add_grid:
        add_default_grids(plot, orientation)
    if add_axis:
        add_default_axes(plot, orientation)
    return plot


def create_line_plot(data=[],
                     index_bounds=None,
                     value_bounds=None,
                     orientation="h",
                     color="red",
                     width=1.0,
                     dash="solid",
                     value_mapper_class=LinearMapper,
                     bgcolor="transparent",
                     border_visible=False,
                     add_grid=False,
                     add_axis=False,
                     index_sort="none"):

    index, value = _create_data_sources(data, index_sort)

    if index_bounds is not None:
        index_range = DataRange1D(low=index_bounds[0], high=index_bounds[1])
    else:
        index_range = DataRange1D()
    index_range.add(index)
    index_mapper = LinearMapper(range=index_range)

    if value_bounds is not None:
        value_range = DataRange1D(low=value_bounds[0], high=value_bounds[1])
    else:
        value_range = DataRange1D()
    value_range.add(value)
    value_mapper = value_mapper_class(range=value_range)

    plot = LinePlot(
        index=index,
        value=value,
        index_mapper=index_mapper,
        value_mapper=value_mapper,
        orientation=orientation,
        color=color,
        bgcolor=bgcolor,
        line_width=width,
        line_style=dash,
        border_visible=border_visible)

    if add_grid:
        add_default_grids(plot, orientation)
    if add_axis:
        add_default_axes(plot, orientation)
    return plot


def create_bar_plot(data=[],
                    index_bounds=None,
                    value_bounds=None,
                    orientation="h",
                    color="red",
                    bar_width=10.0,
                    value_mapper_class=LinearMapper,
                    line_color="black",
                    fill_color="red",
                    line_width=1,
                    bgcolor="transparent",
                    border_visible=False,
                    antialias=True,
                    add_grid=False,
                    add_axis=False):

    index, value = _create_data_sources(data)

    if index_bounds is not None:
        index_range = DataRange1D(low=index_bounds[0], high=index_bounds[1])
    else:
        index_range = DataRange1D()
    index_range.add(index)
    index_mapper = LinearMapper(range=index_range)

    if value_bounds is not None:
        value_range = DataRange1D(low=value_bounds[0], high=value_bounds[1])
    else:
        value_range = DataRange1D()
    value_range.add(value)
    value_mapper = value_mapper_class(range=value_range)

    # Create the plot
    plot = BarPlot(
        index=index,
        value=value,
        value_mapper=value_mapper,
        index_mapper=index_mapper,
        orientation=orientation,
        line_color=line_color,
        fill_color=fill_color,
        line_width=line_width,
        bar_width=bar_width,
        antialias=antialias, )

    if add_grid:
        add_default_grids(plot, orientation)
    if add_axis:
        add_default_axes(plot, orientation)
    return plot


def create_polar_plot(data,
                      orientation='h',
                      color='black',
                      width=1.0,
                      dash="solid",
                      grid="dot",
                      value_mapper_class=PolarMapper):
    if (type(data) != ndarray) and (len(data) == 2):
        data = transpose(array(data))

    r_data, t_data = transpose(data)
    index_data = r_data * cos(t_data)
    value_data = r_data * sin(t_data)

    index = ArrayDataSource(index_data, sort_order='ascending')
    # Typically the value data is unsorted
    value = ArrayDataSource(value_data)

    index_range = DataRange1D()
    index_range.add(index)
    index_mapper = PolarMapper(range=index_range)

    value_range = DataRange1D()
    value_range.add(value)
    value_mapper = value_mapper_class(range=value_range)

    plot = PolarLineRenderer(
        index=index,
        value=value,
        index_mapper=index_mapper,
        value_mapper=value_mapper,
        orientation=orientation,
        color=color,
        line_width=width,
        line_style=dash,
        grid_style=grid)

    return plot


def add_default_axes(plot,
                     orientation="normal",
                     vtitle="",
                     htitle="",
                     axis_class=PlotAxis):
    """
    Creates left and bottom axes for a plot.  Assumes that the index is
    horizontal and value is vertical by default; set *orientation* to
    something other than "normal" if they are flipped.
    """
    if orientation in ("normal", "h"):
        v_mapper = plot.value_mapper
        h_mapper = plot.index_mapper
    else:
        v_mapper = plot.index_mapper
        h_mapper = plot.value_mapper

    left = axis_class(
        orientation='left', title=vtitle, mapper=v_mapper, component=plot)

    bottom = axis_class(
        orientation='bottom', title=htitle, mapper=h_mapper, component=plot)

    plot.underlays.append(left)
    plot.underlays.append(bottom)
    return left, bottom


def add_default_grids(plot, orientation="normal"):
    """
    Creates horizontal and vertical gridlines for a plot.  Assumes that the
    index is horizontal and value is vertical by default; set orientation to
    something other than "normal" if they are flipped.
    """
    if orientation in ("normal", "h"):
        v_mapper = plot.index_mapper
        h_mapper = plot.value_mapper
    else:
        v_mapper = plot.value_mapper
        h_mapper = plot.index_mapper

    vgrid = PlotGrid(
        mapper=v_mapper,
        orientation='vertical',
        component=plot,
        line_color="lightgray",
        line_style="dot")

    hgrid = PlotGrid(
        mapper=h_mapper,
        orientation='horizontal',
        component=plot,
        line_color="lightgray",
        line_style="dot")

    plot.underlays.append(vgrid)
    plot.underlays.append(hgrid)
    return hgrid, vgrid


# EOF
