class SpectrumStruct(object):
    """Defines the data structure"""

    def __init__(self, survey, source, pos, data, identifier=None):
        self.kind = "spectrum"
        self.survey = survey
        self.source = source
        self.pos = pos
        self.identifier = identifier
        self.data = data
        self.figure = None
        self.file_name = None

    def __str__(self):
        return "<ATK Spectrum Structure>"

    def plot(self):
        from ..Plotting.plotmap import map_to_plot

        return map_to_plot(self)


class SurveyMap(object):
    """Base class for spectrum queries"""

    def __init__(self, survey, radius, pos=None):
        self.survey = survey
        self.pos = pos
        self.radius = radius

    def query(self):
        data = globals()[f"{self.survey}_query"](pos=self.pos, radius=self.radius)
        return data


def sdss_query(pos, radius):
    from astropy import coordinates as coords
    from astropy import units as u
    from astroquery.sdss import SDSS

    position = coords.SkyCoord(pos[0], pos[1], unit="deg")
    radius = radius / 3600 * u.deg

    data = SDSS.get_spectra(coordinates=position, radius=radius, timeout=120)
    if data:
        data = data[0][1].data
        wavelength = 10 ** data["loglam"]
        flux = data["flux"] * 10**-17
        return {"wavelength": list(wavelength), "flux": list(flux)}
    else:
        print("Note: SDSS spectrum query returned no data.")
        return None


def query(survey, radius, pos=None, source=None):
    if source:
        from ..Tools import correctpm

        pos = correctpm(target_survey="sdss", source=source)
        if not pos:
            return SpectrumStruct(survey=survey, source=source, pos=pos, data=None)

    data = SurveyMap(survey=survey, radius=radius, pos=pos).query()
    return SpectrumStruct(survey=survey, source=source, pos=pos, data=data)
