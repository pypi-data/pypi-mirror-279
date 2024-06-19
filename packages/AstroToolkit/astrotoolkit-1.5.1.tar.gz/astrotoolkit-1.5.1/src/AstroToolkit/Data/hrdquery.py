class HrdStruct(object):
    def __init__(self, sources, data, identifiers=None, survey="gaia"):
        self.kind = "hrd"

        self.survey = survey
        self.sources = sources
        self.identifiers = identifiers
        self.data = data
        self.figure = None
        self.file_name = None

    def __str__(self):
        return "<ATK HRD Structure>"

    def plot(self):
        from ..Plotting.plotmap import map_to_plot

        return map_to_plot(self)


def gather_data(sources):
    import numpy as np

    if not isinstance(sources, list):
        sources = [sources]

    x, y = [], []

    from ..Tools import query

    bad_indices = []
    for index, source in enumerate(sources):
        gaia_data = query(
            kind="data", source=source, survey="gaia", level="internal"
        ).data
        if gaia_data:
            gmag, bpmag, rpmag, parallax = (
                gaia_data["phot_g_mean_mag"][0],
                gaia_data["phot_bp_mean_mag"][0],
                gaia_data["phot_rp_mean_mag"][0],
                gaia_data["parallax"][0],
            )

            x.append(bpmag - rpmag)
            y.append(gmag + 5 * np.log10(parallax / 1000) + 5)
        else:
            bad_indices.append(index)

    sources_formatted = [
        source for i, source in enumerate(sources) if i not in bad_indices
    ]

    return HrdStruct(sources=sources_formatted, data={"bp-rp": x, "absg": y})
