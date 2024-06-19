import astropy.units as u
import numpy as np
from astropy.timeseries import LombScargle
from bokeh import events
from bokeh.models import CustomJS
from bokeh.plotting import figure

newline = "\n"


def lomb_scargle(data, freq=None):
    class timeseries_data(object):
        def __init__(self, time, mag, mag_err, power, frequency, freq):
            self.time = time
            self.mag = mag
            self.mag_err = mag_err
            self.power = power
            self.frequency = frequency
            self.phase_freq = freq

        @property
        def powspec_plot(self):
            plot = figure(
                width=400,
                height=400,
                x_axis_label=r"Frequency \[\text{days}^{-1}\]",
                y_axis_label="Lomb-Scargle Power",
            )

            max_freq = self.frequency[np.nanargmax(self.power)]
            period = 24 / max_freq

            plot.line(
                x=self.frequency,
                y=self.power,
                legend_label=f"Max Frequency: {round(max_freq.value,2)} 1/d {newline}Period: {round(period.value,2)} h",
            )

            toggle_legend_js = CustomJS(
                args=dict(leg=plot.legend[0]),
                code="""
                    if (leg.visible) {
                        leg.visible = false
                        }
                    else {
                        leg.visible = true
                    }
            """,
            )

            plot.js_on_event(events.DoubleTap, toggle_legend_js)

            return plot

        @property
        def phasefold_plot(self):
            if not self.phase_freq:
                best_frequency = self.frequency[np.nanargmax(self.power)]
            else:
                best_frequency = self.phase_freq / u.day

            t_fit = np.linspace(0, 1, 1000) * u.day
            ls = LombScargle(self.time, self.mag, self.mag_err)
            y_fit = ls.model(t=t_fit, frequency=best_frequency)

            phase = (self.time % (1 / best_frequency)) * best_frequency

            t_fit = t_fit * best_frequency
            cut_indices = [i for i, val in enumerate(t_fit) if val > 1]

            t_fit_formatted = [
                val for i, val in enumerate(t_fit) if i not in cut_indices
            ]
            y_fit_formatted = [
                val for i, val in enumerate(y_fit) if i not in cut_indices
            ]

            median_mag = np.median(self.mag).value

            phase = [x.value for x in phase]
            self.mag = [x.value - median_mag for x in self.mag]
            t_fit_formatted = [x.value for x in t_fit_formatted]
            y_fit_formatted = [x.value - median_mag for x in y_fit_formatted]
            self.mag_err = [x.value for x in self.mag_err]

            err_xs = [[x, x] for x in phase]
            err_ys = [
                [y - y_err, y + y_err] for y, y_err in zip(self.mag, self.mag_err)
            ]

            plot = figure(
                width=400,
                height=400,
                x_axis_label="Phase",
                y_axis_label="Magnitude (relative to median)",
            )
            plot.scatter(x=phase, y=self.mag, level="guide")
            plot.line(
                x=t_fit_formatted,
                y=y_fit_formatted,
                line_width=2,
                line_color="black",
                level="underlay",
                legend_label=f"Period: {round(24/(best_frequency.value),2)} h",
            )
            plot.multi_line(
                xs=err_xs,
                ys=err_ys,
                line_width=0.5,
                level="glyph",
                line_cap="square",
            )

            plot.y_range.flipped = True

            toggle_legend_js = CustomJS(
                args=dict(leg=plot.legend[0]),
                code="""
                    if (leg.visible) {
                        leg.visible = false
                        }
                    else {
                        leg.visible = true
                    }
            """,
            )

            plot.js_on_event(events.DoubleTap, toggle_legend_js)

            return plot

    if not data:
        print(
            "Note: Empty data structure passed to timeseries tool. Suggests that no data was found."
        )
        return None

    from .timeseries_formatting import format_data

    time, mag, mag_err = format_data(data)
    time, mag, mag_err = time * u.day, mag * u.mag, mag_err * u.mag

    freqs = np.linspace(0, 15, 150000) / u.day
    power = LombScargle(time, mag, mag_err, fit_mean=False).power(freqs)

    data_class = timeseries_data(time, mag, mag_err, power, freqs, freq)

    return data_class
