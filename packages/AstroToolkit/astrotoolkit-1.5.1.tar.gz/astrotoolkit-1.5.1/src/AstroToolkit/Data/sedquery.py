class SedStruct(object):
    def __init__(self, source, pos, data, identifier=None):
        self.kind = "sed"
        self.source = source
        self.pos = pos
        self.identifier = identifier
        self.data = data
        self.figure = None
        self.file_name = None

    def __str__(self):
        return "<ATK SED Structure>"

    def plot(self,spectrum_overlay=False,survey=None):
        from ..Plotting.plotmap import map_to_plot
        
        return map_to_plot(self,spectrum_overlay=spectrum_overlay,survey=survey)


def mag_to_flux(mag, zp, wl):
    # sometimes overflows if a bad mag is passed (e.g. -999 for some surveys)
    try:
        flux = zp * 10 ** (-0.4 * mag)
    except:
        return None
    #convert to mjy
    c = 2.988 * 10**18
    fnl = 1 * 10 ** (-23)
    flux = flux / ((fnl * c) / wl**2) * 1000

    return flux


def format_data(survey, photometry, filter_wavelengths, mag_names, error_names):
    import numpy as np

    if survey != "gaia":
        zero_points = [
            10 ** ((5 * np.log10(x) + 2.406) / -2.5) for x in filter_wavelengths
        ]
    else:
        zero_points = [2.5e-9, 4.11e-9, 1.24e-9]

    sed_datapoints = {
        "survey": survey,
        "wavelength": [],
        "flux": [],
        "flux_rel_err": [],
    }
    for filter_wavelength, mag_name, error_name, zero_point in zip(
        filter_wavelengths, mag_names, error_names, zero_points
    ):
        mag, mag_err = photometry[mag_name][0], photometry[error_name][0]

        flux = mag_to_flux(mag=mag, zp=zero_point, wl=filter_wavelength)
        if flux:
            rel_err = flux * mag_err / mag

            sed_datapoints["wavelength"].append(filter_wavelength)
            sed_datapoints["flux"].append(flux)
            sed_datapoints["flux_rel_err"].append(rel_err)

    return sed_datapoints


def query(radius, pos=None, source=None):
    from ..Data.dataquery import SurveyInfo
    from ..Tools import query

    sed_params = SurveyInfo().sed_param_names
    
    bulkphot = query(
        kind="bulkphot", pos=pos, source=source, radius=radius, level="internal"
    )
    if bulkphot.data:
        pos = bulkphot.data["gaia"]["ra"][0], bulkphot.data["gaia"]["dec"][0]

        bulkphot.data = {
            key: value for key, value in bulkphot.data.items() if value is not None
        }

    sed_data = []
    for survey in bulkphot.data:
        filter_wavelengths, mag_names, error_names = (
            sed_params[survey]["filter_wavelengths"],
            sed_params[survey]["mag_names"],
            sed_params[survey]["error_names"],
        )

        sed_data.append(
            format_data(
                survey=survey,
                photometry=bulkphot.data[survey],
                filter_wavelengths=filter_wavelengths,
                mag_names=mag_names,
                error_names=error_names,
            )
        )

    data_struct = SedStruct(pos=pos, source=source, data=sed_data)
    return data_struct
