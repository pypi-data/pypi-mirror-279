import pandas as pd


def CreateLocalData(struct, fname):
    data_dict = {
        "atk_survey": struct.survey,
        "atk_source": struct.source,
        "atk_catalogue": struct.catalogue,
        "atk_pos_ra": struct.pos[0],
        "atk_pos_dec": struct.pos[1],
        "atk_identifier": struct.identifier,
    }
    for key in struct.data:
        data_dict[key] = struct.data[key]

    fname = f"{fname}.csv"

    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv(fname, index=False)

    return fname


def CreateLocalPhot(struct, fname):
    fname = CreateLocalData(struct, fname)
    return fname


def CreateLocalBulkphot(struct, fname):
    data = []
    for survey in struct.data:
        data_dict = {
            "atk_survey": survey,
            "atk_source": struct.source,
            "atk_pos_ra": struct.pos[0],
            "atk_pos_dec": struct.pos[1],
            "atk_identifier": struct.identifier,
        }

        if struct.data[survey]:
            for key in struct.data[survey]:
                data_dict[key] = struct.data[survey][key]
            data.append(data_dict)

    fname = f"{fname}.csv"

    with open(fname, "w") as file:
        for survey in data:
            df = pd.DataFrame.from_dict(survey)
            df.to_csv(file, index=False, lineterminator="\n")
            file.write("\n")

    return fname


def CreateLocalLightcurve(struct, fname):
    data = []
    for band in struct.data:
        if band["mag"] is not None:
            data_dict = {
                "atk_survey": struct.survey,
                "atk_source": struct.source,
                "atk_pos_ra": struct.pos[0],
                "atk_pos_dec": struct.pos[1],
                "atk_identifier": struct.identifier,
            }
            for key in band:
                data_dict[key] = band[key]
            data.append(data_dict)

    fname = f"{fname}.csv"

    with open(fname, "w") as file:
        for band in data:
            df = pd.DataFrame.from_dict(band)
            df.to_csv(file, index=False, lineterminator="\n")
            file.write("\n")

    return fname


def CreateLocalImage(struct, fname):
    pos_ra, pos_dec, source, survey = (
        float(struct.pos[0]),
        float(struct.pos[1]),
        struct.source,
        struct.survey,
    )

    from astropy.io import fits

    hdu = fits.PrimaryHDU(struct.data["image_data"], header=struct.data["image_header"])

    hdu.header["atk_pos_ra"], hdu.header["atk_pos_dec"] = pos_ra, pos_dec
    hdu.header["atk_source"], hdu.header["atk_survey"] = source, survey
    hdu.header["atk_image_focus_ra"], hdu.header["atk_image_focus_dec"] = (
        struct.data["image_focus"][0],
        struct.data["image_focus"][1],
    )
    hdu.header["atk_identifier"] = struct.identifier
    (
        hdu.header["atk_size"],
        hdu.header["atk_time_year"],
        hdu.header["atk_time_month"],
    ) = (
        struct.data["size"],
        struct.data["image_time"][0],
        struct.data["image_time"][1],
    )

    if "overlay" in struct.data:
        overlay_data = struct.data["overlay"]
        for i, element in enumerate(overlay_data):
            hdu.header[f"atk_overlay_type_{i}"] = element["overlay_type"]
            hdu.header[f"atk_overlay_marker_type_{i}"] = element["marker_type"]
            hdu.header[f"atk_overlay_corrected_{i}"] = element["corrected"]
            hdu.header[f"atk_overlay_ra_{i}"] = element["ra"]
            hdu.header[f"atk_overlay_dec_{i}"] = element["dec"]
            hdu.header[f"atk_overlay_marker_size_{i}"] = element["marker_size"]
            hdu.header[f"atk_overlay_colour_{i}"] = element["colour"]
            hdu.header[f"atk_overlay_mag_name_{i}"] = element["mag_name"]
            hdu.header[f"atk_overlay_survey_{i}"] = element["survey"]

    fname = f"{fname}.fits"
    hdu.writeto(fname, overwrite=True)

    return fname


def CreateLocalReddening(struct, fname):
    fname = CreateLocalData(struct, fname)
    return fname


def CreateLocalSed(struct, fname):
    pos_ra, pos_dec = struct.pos[0], struct.pos[1]

    data_dict = {
        "atk_source": struct.source,
        "atk_pos_ra": struct.pos[0],
        "atk_pos_dec": struct.pos[1],
        "atk_identifier": struct.identifier,
        "sed_survey": [],
        "wavelength": [],
        "flux": [],
        "flux_rel_err": [],
    }
    for data_set in struct.data:
        for i, _ in enumerate(data_set["wavelength"]):
            data_dict["sed_survey"].append(data_set["survey"])
            data_dict["wavelength"].append(data_set["wavelength"][i])
            data_dict["flux"].append(data_set["flux"][i])
            data_dict["flux_rel_err"].append(data_set["flux_rel_err"][i])

    fname = f"{fname}.csv"

    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv(fname, index=False)

    return fname


def CreateLocalSpectrum(struct, fname):
    pos_ra, pos_dec = struct.pos[0], struct.pos[1]

    fname = f"{fname}.csv"

    data_dict = {
        "atk_survey": struct.survey,
        "atk_source": struct.source,
        "atk_pos_ra": pos_ra,
        "atk_pos_dec": pos_dec,
        "atk_identifier": struct.identifier,
    }

    for key in struct.data:
        data_dict[key] = struct.data[key]

    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv(fname, index=False)

    return fname


def CreateLocalHrd(struct, fname):
    fname = f"{fname}.csv"

    data_dict = {
        "atk_survey": struct.survey,
        "atk_sources": struct.sources,
        "atk_identifiers": struct.identifiers,
    }

    for key in struct.data:
        data_dict[key] = struct.data[key]

    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv(fname, index=False)

    return fname


def generate_local_file(struct):
    from .file_naming import name_file

    if hasattr(struct, "subkind"):
        ftype = struct.subkind
    else:
        ftype = struct.kind

    fname = name_file(struct)
    fname = globals()[f"CreateLocal{ftype.capitalize()}"](struct, fname)
    return fname
