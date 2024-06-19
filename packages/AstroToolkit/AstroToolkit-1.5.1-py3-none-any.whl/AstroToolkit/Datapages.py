from .Configuration.baseconfig import ConfigStruct

config = ConfigStruct()
config.read_config()


def buttons(radius="config", grid_size="config", pos=None, source=None):
    from .DatapageElements.datapage_buttons import get_search_buttons
    from .Input.input_validation import check_inputs

    inputs = check_inputs(
        {"radius": radius, "pos": pos, "source": source, "grid_size": grid_size},
        "buttons",
    )
    radius, pos, source, grid_size = (
        inputs["radius"],
        inputs["pos"],
        inputs["source"],
        inputs["grid_size"],
    )

    config.read_config()
    if radius == "config":
        radius = float(config.datapage_search_button_radius)
    if grid_size == "config":
        grid_size = int(config.datapage_grid_size)

    return get_search_buttons(
        radius=radius, source=source, pos=pos, grid_size=grid_size
    )


def datatable(selection, source=None, pos=None, radius="config"):
    from .DatapageElements.metadata_table import gettable
    from .Input.input_validation import check_inputs

    inputs = check_inputs(
        {"selection": selection, "source": source, "pos": pos, "radius": radius},
        "datatable",
    )
    selection, source, pos, radius = (
        inputs["selection"],
        inputs["source"],
        inputs["pos"],
        inputs["radius"],
    )

    config.read_config()

    if radius == "config":
        radius = float(config.datapage_datatable_radius)

    return gettable(selection=selection, source=source, pos=pos, radius=radius)


def gridsetup(dimensions, plots, grid_size="config"):
    from .Input.input_validation import check_inputs
    from .Misc.gridsetup import format_grid_plots

    inputs = check_inputs(
        {"dimensions": dimensions, "plots": plots, "grid_size": grid_size}, "gridsetup"
    )
    dimensions, plots, grid_size = (
        inputs["dimensions"],
        inputs["plots"],
        inputs["grid_size"],
    )

    config.read_config()
    if grid_size == "config":
        grid_size = int(config.datapage_grid_size)

    return format_grid_plots(dimensions, plots, grid_size)
