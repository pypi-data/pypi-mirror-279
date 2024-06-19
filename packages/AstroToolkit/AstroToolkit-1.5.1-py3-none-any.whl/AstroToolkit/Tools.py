from .Configuration.baseconfig import ConfigStruct

"""
Changelog:
- fixed bug with CRTS light curve queries
- Can now choose a frequency to plot in phase folded light curves
- fixed a bug in input checking that made readfits unusable
- fixed ATLAS light curve queries, extended MJD
- changed GALEX time from [2007,0] to [2006,8], seems to fit high PM object detections better.
- other bug fixes
- added reddening to README, forgot in last version
"""

"""
To-Do:
- fix (especially tracer) query radius in overlays
- update README
- input validation for config values
- add "features" list to README
- add support for selecting a section of light curve to include in peridogram etc.
- add check for missing data in savedata
- currently, incorrect username/password in ATLAS just says experiencing issues
- allow user to choose a file name to save file as
- check atlas query + powspec
- add piggyback radius to config for image detection overlays
- add a config option for font size
- add a config option for svg/png output
"""

config = ConfigStruct()
config.read_config()
newline = "\n"


# 'pos' has epoch of 2000 if given as input, 2016 if found as a result of source query. 'identifier' is therefore always J2000
def query(
    kind,
    survey=None,
    radius="config",
    pos=None,
    source=None,
    size="config",
    band="config",
    username="config",
    password="config",
    overlays="config",
    sources=None,
    level="external",
):
    from .Data.dataquery import query as data_query

    config.read_config()

    from .Input.input_validation import check_inputs

    if not isinstance(overlays, (list, dict)) and overlays != "config":
        overlays = [overlays]

    inputs = check_inputs(
        {
            "survey": survey,
            "radius": radius,
            "pos": pos,
            "source": source,
            "size": size,
            "band": band,
            "username": username,
            "password": password,
            "overlays": overlays,
            "sources": sources,
        },
        kind,
    )

    survey, radius, pos, source, size, band, username, password, overlays, sources = (
        inputs["survey"],
        inputs["radius"],
        inputs["pos"],
        inputs["source"],
        inputs["size"],
        inputs["band"],
        inputs["username"],
        inputs["password"],
        inputs["overlays"],
        inputs["sources"],
    )

    if radius == "config" and kind != "image" and kind != "hrd":
        radius = float(getattr(config, f"query_{kind}_radius"))
    if size == "config":
        size = int(config.query_image_size)
    if band == "config":
        band = config.query_image_band
    if overlays == "config":
        overlays = config.query_image_overlays
    if username == "config":
        username = config.query_lightcurve_atlas_username
    if password == "config":
        password = config.query_lightcurve_atlas_password
    if kind == "hrd":
        survey = "Gaia"
        radius = None

    if (
        config.enable_notifications == "True"
        and level != "internal"
        and kind not in ["image", "bulkphot", "sed"]
    ):
        print(
            f"Running {survey} {kind} query{newline}source = {source}{newline}pos = {pos}{newline}radius = {radius}{newline}"
        )
    elif (
        config.enable_notifications == "True"
        and level != "internal"
        and kind == "image"
    ):
        print(
            f"Running {survey} {kind} query{newline}source = {source}{newline}pos = {pos}{newline}size = {size}{newline}"
        )
    elif (
        config.enable_notifications == "True"
        and level != "internal"
        and kind in ["bulkphot", "sed"]
    ):
        print(
            f"Running {kind} query{newline}source = {source}{newline}pos = {pos}{newline}radius = {radius}{newline}"
        )

    if kind == "data":
        data = data_query(survey=survey, radius=radius, pos=pos, source=source)
        if source and survey == "gaia" and data.data:
            data.pos = [data.data["ra"][0], data.data["dec"][0]]
        elif source and survey != "gaia":
            gaia_data = data_query(survey="gaia", radius=radius, pos=pos, source=source)
            if gaia_data.data:
                data.pos = [gaia_data.data["ra"][0], gaia_data.data["dec"][0]]
            else:
                return data

    elif kind == "spectrum":
        from .Data.spectrumquery import query as spectrum_query

        data = spectrum_query(survey=survey, radius=radius, pos=pos, source=source)

    elif kind == "image":
        from .Data.imagequery import query as image_query

        if survey == "any":
            for survey in ["panstarrs", "skymapper", "dss"]:
                data = image_query(
                    survey=survey,
                    size=size,
                    band=band,
                    pos=pos,
                    source=source,
                    overlays=overlays,
                )
                if data.data:
                    break
        else:
            data = image_query(
                survey=survey,
                size=size,
                band=band,
                pos=pos,
                source=source,
                overlays=overlays,
            )

    elif kind == "lightcurve":
        from .Data.lightcurvequery import query as lightcurve_query

        data = lightcurve_query(
            survey=survey,
            radius=radius,
            pos=pos,
            source=source,
            username=username,
            password=password,
        )

    elif kind == "phot":
        from .Data.photquery import query as phot_query

        data = phot_query(pos=pos, source=source, radius=radius, survey=survey)
    elif kind == "bulkphot":
        from .Data.photquery import bulkphot_query

        data = bulkphot_query(pos=pos, source=source, radius=radius)
    elif kind == "sed":
        from .Data.sedquery import query as sed_query

        data = sed_query(pos=pos, source=source, radius=radius)
    elif kind == "reddening":
        from .Data.reddeningquery import query as reddening_query

        data = reddening_query(survey=survey, source=source, pos=pos, radius=radius)
    elif kind == "hrd":
        from .Data.hrdquery import gather_data

        data = gather_data(sources)
    else:
        raise Exception("Invalid kind passed to query.")

    from .Misc.identifier_generation import identifier_from_pos

    if hasattr(data, "source"):
        if data.source and data.data:
            gaia_data = data_query(survey="gaia", radius=radius, pos=pos, source=source)
            if gaia_data.data:
                ra, dec = gaia_data.data["ra2000"][0], gaia_data.data["dec2000"][0]
                data.identifier = identifier_from_pos([ra, dec])
        else:
            data.identifier = identifier_from_pos(data.pos)
    elif hasattr(data, "sources") and data.data:
        identifiers = []
        for source in data.sources:
            gaia_data = data_query(
                survey="gaia", radius=radius, pos=pos, source=source
            ).data
            ra, dec = gaia_data["ra2000"][0], gaia_data["dec2000"][0]
            identifiers.append(identifier_from_pos([ra, dec]))
        data.identifiers = identifiers
    else:
        data.identifier = identifier_from_pos(data.pos)

    return data


def correctpm(
    input_survey=None,
    target_survey=None,
    pos=None,
    source=None,
    input_time=None,
    target_time=None,
    pmra=None,
    pmdec=None,
):
    from .Input.input_validation import check_inputs

    inputs = check_inputs(
        {
            "input_survey": input_survey,
            "target_survey": target_survey,
            "pos": pos,
            "source": source,
            "input_time": input_time,
            "target_time": target_time,
            "pmra": pmra,
            "pmdec": pmdec,
        },
        "correctpm",
    )

    input_survey, target_survey, pos, source, input_time, target_time, pmra, pmdec = (
        inputs["input_survey"],
        inputs["target_survey"],
        inputs["pos"],
        inputs["source"],
        inputs["input_time"],
        inputs["target_time"],
        inputs["pmra"],
        inputs["pmdec"],
    )

    if source and target_time:
        from .Misc.pmcorrection import autocorrect_source

        corrected_pos = autocorrect_source(source=source, target_time=target_time)
    elif source and target_survey:
        from .Misc.pmcorrection import autocorrect_source

        corrected_pos = autocorrect_source(source=source, target_survey=target_survey)

    elif pos and input_time and target_time:
        from .Misc.pmcorrection import correctpm

        corrected_pos = correctpm(input_time, target_time, pos[0], pos[1], pmra, pmdec)
    elif pos and input_survey and target_survey:
        from .Misc.pmcorrection import autocorrect_survey

        corrected_pos = autocorrect_survey(
            input_survey, target_survey, ra=pos[0], dec=pos[1], pmra=pmra, pmdec=pmdec
        )
    else:
        raise Exception("Invalid input combination passed to correctpm.")

    return corrected_pos


def savedata(data):
    from .FileHandling.file_writing import generate_local_file

    fname = generate_local_file(data)

    config.read_config()
    if config.enable_notifications == "True":
        print(f"Saving data to local storage: {fname}{newline}")

    return fname


def readdata(fname):
    from .FileHandling.file_reading import read_local_file
    from .Input.input_validation import check_inputs

    inputs = check_inputs({"fname": fname}, "readdata")
    fname = inputs["fname"]

    config.read_config()
    if config.enable_notifications == "True":
        print(f"Recreating data from local storage: {fname}{newline}")

    return read_local_file(fname)


def search(kind, radius="config", source=None, pos=None):
    from .Input.input_validation import check_inputs
    from .Misc.search import do_search

    inputs = check_inputs(
        {"kind": kind, "radius": radius, "source": source, "pos": pos}, "search"
    )
    kind, radius, source, pos = (
        inputs["kind"],
        inputs["radius"],
        inputs["source"],
        inputs["pos"],
    )

    config.read_config()
    if radius == "config":
        radius = float(config.search_radius)

    if config.enable_notifications == "True":
        print(
            f"Running {kind} query{newline}source = {source}{newline}pos = {pos}{newline}radius = {radius}{newline}"
        )

    do_search(kind=kind, radius=radius, source=source, pos=pos)


def readfits(fname, columns):
    from .Input.input_validation import check_inputs
    from .Misc.fitsfiles import get_columns

    inputs = check_inputs({"fname": fname, "columns": columns}, "readfits")
    fname, columns = inputs["fname"], inputs["columns"]

    config.read_config()
    if config.enable_notifications:
        print(f"Reading local .fits file: {fname}")

    return get_columns(filename=fname, columns=columns)


def deg2hms(pos):
    from .Input.input_validation import check_inputs
    from .Misc.identifier_generation import identifier_from_pos

    inputs = check_inputs({"pos": pos}, "deg2hms")
    pos = inputs["pos"]

    return identifier_from_pos(pos, kind="conversion")


def hms2deg(pos):
    from .Input.input_validation import check_inputs
    from .Misc.coordinate_conversions import conv_hms_to_deg

    inputs = check_inputs({"pos": pos}, "hms2deg")
    pos = inputs["pos"]

    return conv_hms_to_deg(pos)
