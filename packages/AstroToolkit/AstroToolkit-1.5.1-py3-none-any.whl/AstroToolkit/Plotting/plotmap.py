class Dimensions(object):
    def __init__(self, height, width):
        self.height = height
        self.width = width


def map_to_plot(
    struct,
    kind=None,
    colours=None,
    bands=None,
    spectrum_overlay=False,
    survey=None,
    freq=None,
):
    if not struct.data:
        print("Note: Plot() missing data, suggests that no data was returned")
        struct.plot = None
        plot_success = False
    else:
        plot_success = True

    if plot_success:
        if struct.kind == "lightcurve":
            if kind == "lightcurve":
                from .lightcurveplotting import plot_lightcurve

                plot = plot_lightcurve(struct, colours, bands)
                dimensions = Dimensions(height=1, width=2)
            elif kind == "powspec":
                from ..Timeseries.lomb_scargle import lomb_scargle

                plot = lomb_scargle(struct.data, freq).powspec_plot
                dimensions = Dimensions(height=1, width=1)
            elif kind == "phase":
                from ..Timeseries.lomb_scargle import lomb_scargle

                plot = lomb_scargle(struct.data, freq).phasefold_plot
                dimensions = Dimensions(height=1, width=1)
            else:
                raise Exception("Invalid plotting kind for ATK Lightcurve data.")
        elif struct.kind == "image":
            from .imageplotting import plot_image

            plot = plot_image(struct)
            dimensions = Dimensions(height=2, width=2)
        elif struct.kind == "sed":
            from .sedplotting import plot_sed

            plot = plot_sed(struct, spectrum_overlay, survey)
            dimensions = Dimensions(height=1, width=2)
        elif struct.kind == "spectrum":
            from .spectrumplotting import plot_spectrum

            plot = plot_spectrum(struct)
            dimensions = Dimensions(height=1, width=2)
        elif struct.kind == "hrd":
            from .hrdplotting import plot_hrd

            plot = plot_hrd(struct)
            dimensions = Dimensions(height=1, width=1)

        text_size = "12pt"
        plot.axis.axis_label_text_font_size = text_size
        plot.axis.major_label_text_font_size = text_size
        plot.axis.major_label_text_font = "Times New Roman"
        plot.legend.label_text_font_size = text_size
        plot.legend.label_text_font = "Times New Roman"
        plot.axis.axis_label_text_font_style = "normal"
        plot.axis.axis_label_text_font = "Times New Roman"

        from ..Configuration.baseconfig import ConfigStruct

        config = ConfigStruct()
        config.read_config()
        plot.width = int(config.unit_size) * dimensions.width
        plot.height = int(config.unit_size) * dimensions.height
        plot.output_backend = "svg"

    if hasattr(struct, "subkind"):
        suffix = struct.subkind
    else:
        suffix = struct.kind

    if hasattr(struct, "source"):
        if struct.source:
            fname = f"{struct.identifier}_{struct.source}_ATK{suffix}"
        elif struct.pos:
            fname = f"{struct.identifier}_ATK{suffix}"
    elif hasattr(struct, "sources"):
        if len(struct.identifiers) > 1:
            fname = f"{struct.identifiers[0]}_AndOtherSource(s)_ATK{suffix}"
        else:
            fname = f"{struct.identifiers[0]}_ATK{suffix}"

    if plot_success:
        from bokeh.plotting import output_file

        output_file(f"{fname}.html")
        struct.figure = plot

    struct.file_name = f"{fname}.html"

    import types

    from bokeh.plotting import save as bokeh_save
    from bokeh.plotting import show as bokeh_show

    def show(self):
        if hasattr(self, "plot"):
            if self.figure:
                bokeh_show(self.figure)
            else:
                print(
                    "Note: No plot to show. Suggests necesesary data was not retrieved."
                )
        else:
            print("Note: No plot to show. Create one using .plot()")

        return self

    struct.show = types.MethodType(show, struct)

    def save(self):
        if hasattr(self, "plot"):
            if self.figure:
                bokeh_save(self.figure)
            else:
                print("Note: No plot to save.")
        else:
            print("Note: No plot to show. Create one using .plot()")

        return self

    struct.save = types.MethodType(save, struct)

    return struct
