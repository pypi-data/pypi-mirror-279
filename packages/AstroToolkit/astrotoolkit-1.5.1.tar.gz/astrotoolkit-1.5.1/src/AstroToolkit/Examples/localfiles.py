from AstroToolkit.Tools import query, readdata, savedata

# specify a Gaia source
source = 587316166180416640

# retrieve ZTF light curve data for our source
lightcurve_data = query(kind="lightcurve", source=source, survey="ztf")

# save data to a local file and retrieve the name of this file
filename = savedata(lightcurve_data)

# recreate the original data structure from the local file
recreated_data = readdata(filename)

# plot only the g band of this data in the colour green, and show it.
recreated_data.plot(colours=["green"], bands=["g"]).show()
