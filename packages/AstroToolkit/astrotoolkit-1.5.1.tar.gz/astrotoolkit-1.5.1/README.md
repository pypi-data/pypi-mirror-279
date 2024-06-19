# AstroToolkit

AstroToolkit (ATK) is a set of tools for fetching, plotting, and analysing astronomical data.

## Features

## Table of Contents

[**Installation**](#installation)

[**Introduction**](#introduction)

[**Modules**](#modules)

<br>

[AstroToolkit.Tools](#tools)

* [Query](#query)
    * [Data Query](#dataquery)
    * [Photometry Query](#photquery)
    * [Bulk Photometry Query](#bulkphotquery)
    * [Light Curve Query](#lightcurvequery)
    * [Image Query](#imagequery)
    * [Spectrum Query](#spectrumquery)
    * [SED Query](#sedquery)
    * [HRD Query](#hrdquery)
    * [Reddening Query](#reddeningquery)
* [Proper Motion Correction](#correctpm)
* [Local File Saving](#savedata)
* [Local File Reading](#readdata)
* [SIMBAD/Vizier Searches](#search)
* [Fits Reading](#readfits)
* [Degrees to HMS](#deg2hms)
* [HMS to Degrees](#hms2deg)

<br>

[AstroToolkit.Datapages](#datapages)
* [Grid Setup](#gridsetup)
* [SIMBAD/Vizier Buttons](#buttons)
* [Datatables](#datatable)

<br>

[AstroToolkit.Config](#config)
* [Open Config File](#openconfig)
* [Edit Config File](#editconfig)
* [Output Config File](#outputconfig)
* [Reset Config File](#resetconfig)

<br>

[Code Examples](#examples)
* [Data Examples](#queryexamples)
* [Lightcurve Example](#lightcurveexample)
* [Timeseries Example](#timeseriesexample)
* [Image Example](#imageexample)
* [Spectrum Example](#spectrumexample)
* [SED Example](#sedexample)
* [HRD Example](#hrdexample)
* [Local File Example](#localfileexample)
* [Datapage Example](#datapageexample)

<br>

## Installation<a id="installation"></a>

The package can be installed like any other package, e.g. using pip:

```
pip install AstroToolkit
```

<br>

## Introduction<a id="introduction"></a>

ATK uses Bokeh as its primary plotting library. The official documentation can be found at [https://bokeh.org/](https://bokeh.org/). A key property of Bokeh plots is that they can be saved as static .html files, which can then be shared/accessed while retaining all interactivity.

Across ATK, there are two possible ways to target your system of interest:
1. pos = [ra,dec] in degrees
2. source = Gaia Source ID

Where possible, it is usually best to use a Gaia source as input, as this enables a key feature of ATK: **Proper Motion Correction**.

A good example of this is in imaging queries. If a 'pos' is used as input, the result will simply be the image data returned by the chosen imaging survey at those exact coordinates. However, this may not be ideal in the case of an object with a large proper motion. If a source is used instead, the data returned will have accounted for this, resulting in the image being centered on the target system. This concept is used throughout ATK when matching data from different surveys to a given system.

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/source_vs_pos.png?raw=true)

<br>

# Modules<a id="modules"></a>

There are currently three modules in ATK:

- AstroToolkit.Tools

- AstroToolkit.Config

- AstroToolkit.Datapages

<br>

In all functions, parameters with a ! proceeding them will be taken from the [config](#config) if absent.

In all plots, legends are hideable by double-clicking, and individual elements can be hidden by clicking them in the legend.

<br>

## AstroToolkit.Tools<a id="tools"></a>

### 1. query<a id="query"></a>

**Usage:**

```
query(kind, *)
```

**Where:**


```
kind: str = kind of query to perform
            Can be one of:
             - 'data': return raw data from any Vizier catalogue
             - 'phot': return only photometry from any supported survey
             - 'bulkphot': return all available photometry from all supported surveys
             - 'lightcurve': return light curve data from any supported survey
             - 'image': return image data from any supported survey
             - 'spectrum': return spectrum data from any supported survey
             - 'sed': return spectral energy distribution data from all supported surveys
             - 'hrd': return Gaia Hertzsprung Russell Diagram data for a set of Gaia sources
             - 'reddening': return reddening data from any supported survey
```

Each kind of query accepts/requires various other parameters.

If no data is returned in any kind of query, the *data* attribute will be set to None.

<br>

**The data returned by lightcurve, image, spectrum, sed and hrd queries can be plotted using the method *plot()* on the returned class. The resulting plot can then be shown using the method *show()* (which will also save the data locally) or just saved locally using the method *save()*.**

<br>

#### 1.1. data query<a id="dataquery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'gaia'
               - 'panstarrs'
               - 'skymapper'
               - 'galex'
               - 'sdss'
               - 'wise'
               - 'twomass'
               - 'rosat'
               - 'erosita'
               - any other Vizier catalogue ID. E.g. for Gaia DR3, the catalogue ID would be 'I/355/gaiadr3'
```

```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)], target position
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
DataStruct: class = ATK Data Structure
```

*Attributes:*

```
kind: str = 'data'
```

```
subkind: str = kind of query (as listed above)
```

```
survey: str = target survey of query
```

```
catalogue: str = target Vizier catalogue
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position 
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data, where:
             keys: str = column headers as given in Vizier (except for Gaia queries where they are the original column names)
             values: list = returned rows
```

*Methods:*
None

<br>

#### 1.2. phot query<a id="photquery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'gaia'
               - 'panstarrs'
               - 'skymapper'
               - 'galex'
               - 'sdss'
               - 'wise'
               - 'twomass'
```

```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)], target position
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
DataStruct: class = ATK Data Structure
```

*Attributes:*

```
kind: str = 'data'
```

```
subkind: str = kind of query (as listed above)
```

```
survey: str = target survey of query
```

```
catalogue: str = target Vizier catalogue
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data, where:
             keys: str = column headers as given in Vizier (except for Gaia queries where they are the original column names)
             values: list = returned rows
```

*Methods:*
None

<br>

#### 1.3. bulkphot query<a id="bulkphotquery"></a>

Retrieves photometry from all surveys supported by phot query.

**Additional Parameters:**


```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)], target position
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
DataStruct: class = ATK Data Structure
```

*Attributes:*

```
kind: str = 'data'
```

```
subkind: str = kind of query (as listed above)
```

```
survey: str = target survey of query
```

```
catalogue: str = target Vizier catalogue
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data, where:
             keys: str = survey supported by phot query
             values: dict where:
                keys: str = column headers as given in Vizier (except for Gaia queries where they are the original column names)
                values: list = returned rows
```

*Methods:*
None

<br>

#### 1.4. lightcurve query<a id="lightcurvequery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'ztf'
               - 'atlas'
               - 'crts'
               - 'asassn'
               - 'gaia'
```

```
!radius: int = search radius in arcseconds
```

```
!username: str = ATLAS username for use in ATLAS queries
```

```
!password: str =  ATLAS password for use in ATLAS queries
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
LightcurveStruct: class = ATK Lightcurve Structure
```

*Attributes:*

```
kind: str = 'lightcurve'
```

```
survey: str = target survey of query
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: list = list of returned data in each band, with each entry taking the form:
             {
              'band': str = light curve band
              'ra': float = right ascension (deg)
              'dec': float = declination (deg)
              'hjd'/'mjd': float = HJD/MJD given by survey, with minimum subtracted (starts at zero)
              'hjd_ori'/'mjd_ori' = original HJD/MJD as given by survey
              'mag': float = magnitude
              'mag_err': float = magnitude error
             }

             Here, supported surveys have the bands:
              - ztf: g,r,i
              - atlas: o,c,i
              - gaia: g,bp,rp
              - asassn: g,v
              - crts: v
```

*Methods:*

```
plot() - plots lightcurve data.
         Returns the original data class with modified attributes:
          - figure: bokeh figure = the actual plot object
          - filename: str = the default file name that the plot will be saved to

Arguments:
 - kind: str = kind of plot to produce
            Can be one of:
             - 'lightcurve' - light curve (default)
             - 'powspec' - Lomb-Scargle power spectrum
             - 'phase' - phase folded light curve using Lomb-Scargle

Additional Arguments:
For lightcurve plots:
 - colours: list = colour to plot each band that returned data. Defaults to black for all bands.
 - bands: list = bands to include. Includes all by default.

For phase fold plots:
- freq: float = frequency on which to fold the lightcurve data. If none is given, it will be folded on the peak Lomb-Scargle frequency.
```

```
sigmaclip() - sigma clips lightcurve data

Arguments:
- sigma: int = number of standard deviations beyond which data is clipped. Default is 3.
```

```
show() - shows the plot created by the plot() method (and also saves it locally)
```

```
save() - saves the plot created by the plot() method to local storage.
```

<br>

#### 1.5. image query<a id="imagequery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'panstarrs'
               - 'skymapper'
               - 'dss'
               - 'any', performs a hierarchical query: panstarrs > skymapper > dss until an image is found
```

```
!size: int = size of image in arcseconds
```

```
!band: str = bands to use in image. Default is g.
            Supported bands:
             - panstarrs: g,r,i,z,y
             - skymapper: g,r,i,z,u,v
             - dss: g

            e.g. for all panstarrs bands, use band='grizy'
```

```
!overlays: list/dict = surveys to generate detection overlays for.
                      
                      If list, can be one of:
                       - any survey supported by data query
                       - any survey supported by lightcurve query
                      and uses only the magnitude specified in the config for that survey

                      If dict:
                      keys are the survey to include, can be one of:
                       - any survey supported by phot query
                      values are the magnitudes to use from that survey
                      
                      E.g. to use all Gaia magnitudes: overlays={'gaia':['phot_g_mean_mag','phot_bp_mean_mag','phot_rp_mean_mag']}
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
ImageStruct: class = ATK Image Structure
```

*Attributes:*

```
kind: str = 'image'
```

```
survey: str = target survey of query
```

```
source: int = target Gaia DR3 source
```

```
pos: target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data in the form:
             {
              'image_data': arr = raw image data
              'image_header': astropy image header
              'size': int = input image size
              'image_time': list = [year,month], time at which image was taken
              'wcs': astropy wcs object
              'image_focus': list = [right ascension (deg),declination (deg)], image center coordinates
              'overlay': list or None = list of detection information to overlay in image plotting
             }
```

*Methods:*

```
plot() - plots image data.
        Returns the original data class with modified attributes:
          - figure: bokeh figure = the actual plot object
          - filename: str = the default file name that the plot will be saved to
```

```
show() - shows the plot created by the plot() method (and also saves it locally)
```

```
save() - saves the plot created by the plot() method to local storage.
```

<br>

#### 1.6. spectrum query<a id="spectrumquery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'ztf'
               - 'atlas'
               - 'crts'
               - 'asassn'
               - 'gaia'
```

```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
SpectrumStruct: class = ATK Spectrum Structure
```

*Attributes:*

```
kind: str = 'spectrum'
```

```
survey: str = target survey of query
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data in the form:
             {
              'wavelength': list = wavelengths (Angstroms)
              'flux': list = flux values (erg / cm^2 s AA^-1)
             }
```

*Methods:*

```
plot() - plots spectrum data.
         Returns the original data class with modified attributes:
          - figure: bokeh figure = the actual plot object
          - filename: str = the default file name that the plot will be saved to
```

```
show() - shows the plot created by the plot() method (and also saves it locally)
```

```
save() - saves the plot created by the plot() method to local storage.
```

<br>

#### 1.7. sed query<a id="sedquery"></a>

**Additional Parameters:**

```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:**

```
SedStruct: class = ATK SED Structure
```

*Attributes:*

```
kind: str = 'sed'
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: list = list of returned data for each survey with each entry in the form:
             {
              'survey': str = survey of data points
              'wavelength': list = central filter wavelengths (Angstroms)
              'flux': list = flux (mJy)
              'flux_err': list = relative error on the flux (as calculated from magnitudes) (mJy)
             }
```

*Methods:*

```
plot() - plots SED data.
         Returns the original data class with modified attributes:
          - figure: bokeh figure = the actual plot object
          - filename: str = the default file name that the plot will be saved to

Additional Arguments:
 - spectrum_overlay: Bool = overlays a spectrum where available
 - survey: str = survey to retrieve the spectrum from

```

```
show() - shows the plot created by the plot() method (and also saves it locally)
```

```
save() - saves the plot created by the plot() method to local storage.
```

<br>

#### 1.8. hrd query<a id="hrdquery"></a>

**Additional Parameters:**

```
sources: int/list = Gaia DR3 source or list of Gaia DR3 sources to overlay.
```

**Returns:**

```
HrdStruct: class = ATK HRD Structure
```

*Attributes:*

```
kind: str = 'hrd'
```

```
sources: int/list = Gaia DR3 source/Gaia DR3 sources
```

```
identifiers: str / list = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS (list if multiple sources)
```

```
data: list = list of returned data for each survey with each entry in the form:
             {
              'bp-rp': gaia bp magnitude - gaia rp magnitude
              'absg': absolute gaia g magnitude
             }
```

*Methods:*

```
plot() - plots HRD data.
         Returns the original data class with modified attributes:
          - figure: bokeh figure = the actual plot object
          - filename: str = the default file name that the plot will be saved to
```

```
show() - shows the plot created by the plot() method (and also saves it locally)
```

```
save() - saves the plot created by the plot() method to local storage.
```

<br>

#### 1.9. reddening query<a id="reddeningquery"></a>

**Additional Parameters:**

```
survey: str = target survey
              Can be one of:
               - 'stilism'
               - 'gdre'
```

```
!radius: int = search radius in arcseconds
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)], target position
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Note:** For stilism queries, source input is required as a parallax is needed for distance calculations.

**Returns:**

```
DataStruct: class = ATK Data Structure
```

*Attributes:*

```
kind: str = 'data'
```

```
subkind: str = kind of query (as listed above)
```

```
survey: str = target survey of query
```

```
catalogue: str = None
```

```
source: int = target Gaia DR3 source
```

```
pos: list = target position 
```

```
identifier: str = positional identifier of target in format JHHMMSS.SS±DDMMSS.SS
```

```
data: dict = returned data, where:
             keys: str = column headers
             values : float = column values
```

*Methods:*
None

<br>

### 2. correctpm<a id="correctpm"></a>

Automatically corrects for proper motion between two surveys or two times for a given Gaia DR3 source *or* position if proper motion measurements also provided.

**Usage:**

```
correctpm(*)
```

With any valid combination of input parameters:
```
source: int = Gaia DR3 source_id

target_time: list = [year,month], time to correct source's coordinates to
```

```
source: int = Gaia DR3 source_id

target_survey: str = survey to correct source's coordinates to=
                     Can be one of:
                      - any survey supported by data query
                      - any survey supported by lightcurve query
```

```
pos: list = [right ascension (deg), declination (deg)], target position

input_time: list = [year,month], time of object's input position

target_time: list = [year, month] time to correct position to 

pmra: float = right ascension component of proper motion in mas/yr

pmdec: float = declination component of proper motion in mas/yr
```

```
pos: list = [right ascension (deg), declination (deg)], target position

input_survey: str = survey to which position refers
                     Can be one of:
                      - any survey supported by data query
                      - any survey supported by lightcurve query

target_survey: str = survey to correct position to.
                     Can be one of:
                      - any survey supported by data query
                      - any survey supported by lightcurve query

pmra: float = right ascension component of proper motion in mas/yr

pmdec: float = declination component of proper motion in mas/yr

```

**Returns:**

```
position: list = [right ascension (deg), declination (deg)], corrected coordinates of input source/position
```

<br>

### 3. savedata<a id="savedata"></a>

Allows for lossless saving of any ATK data structure to local storage.

**Usage:**

```
savedata(data)
```

**Where:**

```
data: class = any ATK data structure returned by any kind of query
```

**Returns:**

```
fname: str = file name that data was saved to
```

<br>

### 4. readdata<a id="readdata"></a>

Allows for reading of any ATK files to reproduce the original data structure.

**Usage:**

```
readdata(fname)
```

**Where:**

```
fname: str = name of file to read
```

**Returns:**

```
Data Structure: class = ATK data structure that was used to create the file
```

<br>

### 5. search<a id="search"></a>

Searches for a given position or Gaia DR3 source in SIMBAD or Vizier (opens in the webbrowser)

**Usage:**

```
search(kind, !radius, *)
```

**Where:**

```
kind: str = search type
            Can be one of:
            - 'simbad'
            - 'vizier'
```

```
!radius: int = search radius
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
              Target Gaia DR3 source
```

**Returns:** None

<br>

### 6. readfits<a id="readfits"></a>

Reads columns from a given fits file.

**Usage:**

```
readfits(fname,columns)
```

**Where:**

```
fname: str = path to a .fits file
```

```
columns: str/list = columns to fetch from fits file
```

**Returns:**

```
data: list = list of returned data, in order it was asked for.
             E.g. for columns =['ra','dec'], returned data = [[returned ra],[returned dec]]
```

<br>

### 6. deg2hms<a id="deg2hms"></a>

Converts coordinates in degrees to coordinates in HHMMSS±DDMMSS

**Usage:**

```
deg2hms(pos)
```

**Where:**

```
pos: list = [right ascension (deg), declination (deg)], coordinates to convert
```

**Returns:**

```
converted coordinates: str = string representing converted coordinates in above format
```

<br>

#### 7. hms2deg<a id="hms2deg"></a>

Converts coordinates in format returned by deg2hms (HHMMSS±DDMMSS)

**Usage:**

```
hms2deg(pos)
```

**Where:**

```
pos: str = position in format given above
```

**Returns:**

```
converted coordinates: list = [right ascension (deg), declination (deg)]
```

<br>

## AstroToolkit.Datapages<a id="datapages"></a>

### 1.gridsetup<a id="gridsetup"></a>

**Usage:**

```
gridsetup(dimensions,plots,!grid_size)
```

**Where:**

```
dimensions: dict = total dimensions of grid in form {'width': int, 'height': int}
```

```
plots: list = list of dicts, where each dict forms a panel in the datapage:

              {
               'name': name to assign to the plot
               'figure': The figure to give this panel. This can take the form of:
                         - an ATK DataStructure (that has had plot() performed on it)
                         - a Bokeh figure
                         - None (to fill empty space)
               'width': width of the panel in grid units
               'height': height of the panel in grid units
              }
```

**Note:** The total area covered by panels must match the area specified by *dimensions*. Empty space must therefore be filled with empty space (entries with *None* in place of a figure).

```
!grid_size: int = the size that each grid unit represents
```

<br>

See [Examples](#examples) for an example datapage script.

<br>

### 2. buttons<a id="buttons"></a>

Generates a datapage element containing two buttons for Vizier/Simbad queries at the position/source the datapage is built around.

**Usage:**

```
buttons(!radius, !grid_size, *)
```

**Where:**

```
!radius: float = radius to use in the search in arcseconds
```

```
!grid_size: int = the grid_size of the datapage. Scales the buttons to match.
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
```

<br>

### 3. datatable<a id="datatable"></a>

Generates a datatable datapage element using data from supported surveys, along with any custom data.

**Usage:**

```
datatable(selection, !radius, *)
```

**Where:**

```
!radius: float = radius to use when gathering datatable data in arcseconds
```

and

```
selection: dict = datatable entry in the format:

'survey' : 'default'

to include basic preset information for a given survey, or:
                  
'survey' : {
            'parameters' : list of strings, names of parameters (i.e. column headers) that exist in that survey
            'errors' : list of strings, names of errors (i.e. column headers) for these parameters that exist in that survey
            'notes' : list of strings, any notes to include on this parameter/error/etc.
           }

where 'survey' is any survey supported by dataquery.
```

If an entry is provided who's key is not the name of a supported survey, that entry will be interpreted as a custom entry. In this case, an additional 'values' key must be included, and the values/errors must be passed manually. For example:

```
selection: dict = custom datatable entry in the format
                 
'custom' : {
            'parameters' : list of strings, names of parameters
            'values' : list of floats, parameter values
            'errors' : list of floats, error values
            'notes' : list of strings, any notes to include on this parameter.
           }
```

Additionally, requires one of:

```
pos: list = [right ascension (deg), declination (deg)]
            Position around which to search
```

```
source: int = Gaia DR3 source_id.
```

<br>

See [Examples](#examples) for an example datapage script.

<br>

## AstroToolkit.Config<a id="config"></a>

### 1. openconfig<a id="openconfig"></a>

**Usage:**

```
openconfig()
```

Opens the ATK config file for manual editing.

**Returns:**
None

<br>

### 2. editconfig<a id="editconfig"></a>

**Usage:**

```
editconfig(key,value)
```

**Where:**

```
key: str = a valid config key
           Can be one of:
            - 'enable_notifications' = True/False
               enables notifications of the currently running tool

            - 'unit_size' = int
               scales all ATK plots


            - 'query_data_radius' = float
               sets the default data query radius in arcseconds

            - 'query_phot_radius' = float
               sets the default phot query radius in arcseconds
            
            - 'query_bulkphot_radius' = float
               sets the default bulkphot query radius in arcseconds

            - 'query_lightcurve_radius' = float
               sets the default lightcurve query radius in arcseconds

            - 'query_spectrum_radius' = float
               sets the default spectrum query radius in arcseconds

            - 'query_sed_radius' = float
               sets the default sed query radius in arcseconds

            - 'query_reddening_radius' = float
               sets the default reddening query radius in arcseconds

            - 'query_image_size' = int 
               sets the default image query size in arc seconds

            - 'query_image_overlays' = str 
               sets a default overlay to use in image queries

            - 'query_image_band' = str 
               sets the default band to use in image queries

            - 'query_lightcurve_atlas_username' = str 
               sets the default username to use in ATLAS lightcurve queries

            - 'query_lightcurve_atlas_password' = str 
               sets the default password to use in ATLAS lightcurve queries


            - 'gaia_overlay_mag' = str 
               name of default magnitude to use from Gaia in image overlays

            - 'galex_overlay_mag' = str 
               name of default magnitude to use from GALEX in image overlays

            - 'wise_overlay_mag' = str 
               name of default magnitude to use from WISE in image overlays

            - 'sdss_overlay_mag' = str 
               name of default magnitude to use from SDSS in image overlays

            - 'twomass_overlay_mag' = str 
               name of default magnitude to use from 2MASS in image overlays

            - 'skymapper_overlay_mag' = str 
               name of default magnitude to use from SkyMapper in image overlays

            - 'panstarrs_overlay_mag' = str 
               name of default magnitude to use from PanSTARRS in image overlays


            - 'search_radius' = float 
               sets the default radius to use for search (SIMBAD and Vizier query) tool in arcseconds


            - 'datapage_search_button_radius' = float 
               sets the default radius to use for SIMBAD/Vizier search buttons in arcseconds

            - 'datapage_datatable_radius' = float
               sets the default radius to use for datatable queries

            - 'datapage_grid_size' = int 
               sets the default size to scale all plots to in gridsetup
```

<br>

### 3. outputconfig<a id="outputconfig"></a>

Prints the current config values.

**Usage:**

```
outputconfig()
```

**Returns:**
None

<br>

### 4. resetconfig<a id="resetconfig"></a>

Resets the config to default settings.

**Usage:**

```
resetconfig()
```

**Returns:**
None

<br>

## Examples<a id="examples"></a>

### 1. Query Examples<a id='queryexamples'></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 587316166180416640

# retrieve GALEX data, no radius is given so this will be taken from the config.
galex_data = query(kind="data", source=source, survey="galex")

# output this data to the terminal
print(galex_data.data)


# retrieve Gaia data, this time supplying a radius - overriding the config value.
gaia_data = query(kind="data", source=source, survey="gaia", radius=5)

# grab the parallax from Gaia
parallax = gaia_data.data["parallax"][0]


# retrieve WISE photometry
wise_phot = query(kind="phot", source=source, survey="wise")


# retrieve all available photometry
bulkphot = query(kind="bulkphot", source=source)

# grab the panstarrs and skymapper photometry from bulkphot
panstarrs_phot = bulkphot.data["panstarrs"]
skymapper_phot = bulkphot.data["skymapper"]
```

<br>

### 2. Lightcurve Example<a id="lightcurveexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 587316166180416640

# retrieve ZTF light curve data and plot it, specifying the colours for each band.
# No radius  is given, so this will be taken from the config.
figure = query(kind="lightcurve", source=source, survey="ztf").plot(
    colours=["green", "red", "blue"]
)

# show the lightcurves in the browser (and save to a static .html file)
figure.show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/lightcurve_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import lightcurve
```

<br>

### 3. Timeseries Example<a id="timeseriesexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 6050296829033196032

# retrieve ztf data for our Gaia source, plot it as a power spectrum, and then show it.
power_spectrum=query(kind='lightcurve',source=source,survey='ztf').plot(kind='powspec').show()

# retrieve ztf data for our Gaia source, phase fold it, and then show it.
phase_fold=query(kind='lightcurve',source=source,survey='ztf').plot(kind='phase').show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/timeseries_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import timeseries
```

<br>


### 4. Image Example<a id="imageexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 587316166180416640

""" 
Retrieve any available image and plot it.
No size or band is given, so these will be taken from the config. 
Since overlays is given as a list, only the magnitude listed for each survey in the config
will be overlayed as a detection (in this case, phot_g_mean_mag for gaia, and NUVmag for GALEX)
"""
figure = query(
    kind="image", source=source, survey="any", overlays=["gaia", "galex"]
).plot()

# show the image in the browser (and save to a static .html file)
figure.show()

# Now, give overlays as a dict containing all magnitudes to overlay.
figure_allmags = query(
    kind="image",
    source=source,
    survey="any",
    overlays={
        "gaia": ["phot_g_mean_mag", "phot_bp_mean_mag", "phot_rp_mean_mag"],
        "galex": ["NUVmag", "FUVmag"],
    },
).plot()

# show the image in the browser (and save to a static .html file)
figure_allmags.show()

"""
Now, include a light curve survey as an overlay. For surveys with enough positional
precision, this can be used to trace the motion of the object through time.
We have also specified an image size, which will override the value in the config.
A different gaia source with a large proper motion has been used.
"""
figure_tracer = query(
    kind="image",
    source=2552928187080872832,
    survey="panstarrs",
    overlays=["crts"],
    size=60,
).plot()

figure_tracer.show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/image_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import image
```

<br>

### 5. Spectrum Example<a id="spectrumexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 587316166180416640

# retrieve an SDSS spectrum for the gaia source, plot it and then show it.
# As no radius is given, this will be taken from the config.
spectrum = query(kind="spectrum", source=source, survey="sdss").plot().show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/spectrum_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import spectrum
```

<br>

### 6. SED Example<a id="sedexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source = 587316166180416640

# retrieve and plot an sed, with an overlayed SDSS spectrum.
sed=query(kind='sed',source=source).plot(spectrum_overlay=True,survey='sdss')

# show the figure in the browser (and save to a static .html file)
sed.show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/sed_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import sed
```

<br>

### 7. HRD Example<a id="hrdexample"></a>

```
from AstroToolkit.Tools import query

# specify a Gaia source
source1 = 587316166180416640

# Specify a second Gaia source. This is not necessary - any number of sources can be overlayed.
source2 = 6050296829033196032

# retrieve Gaia hrd data for our list of sources, plot it and then show it.
hrd=query(kind='hrd',sources=[source1,source2]).plot().show()
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/hrd_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import hrd
```

<br>

### 8. Local Files Example<a id="localfileexample"></a>

```
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
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/localfiles_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import localfiles
```

<br>

### 9. Datapage Example<a id="datapageexample"></a>

```
from bokeh.layouts import column, layout, row
from bokeh.plotting import output_file, show

from AstroToolkit.Datapages import buttons, datatable, gridsetup
from AstroToolkit.Tools import query

# source = Hu Leo
source = 587316166180416640

# set grid size (scales size of datapage)
grid_size = 250

# get image data and plot it
image = query(
    kind="image", survey="any", source=source, overlays=["gaia", "galex"]
).plot()

# get hrd data and plot it
hrd = query(kind="hrd", sources=source).plot()

# get sed data and plot it
sed = query(kind="sed", source=source).plot(spectrum_overlay=True, survey="sdss")

# get spectrum data and plot it
spectrum = query(kind="spectrum", survey="sdss", source=source).plot()

# get lightcurve data [g,r,i] and plot it
lightcurves = query(kind="lightcurve", survey="ztf", source=source).plot(
    colours=["green", "red", "blue"]
)

# get SIMBAD and Vizier buttons
buttons = buttons(source=source, grid_size=grid_size)

# make a custom metadatatable entry
custom_entry = {
    "parameters": ["one"],
    "values": ["two"],
    "errors": ["three"],
    "notes": ["four"],
}

# get a metadata table with default parameters for various surveys
metadata = datatable(
    source=source,
    selection={
        "gaia": "default",
        "galex": "default",
        "panstarrs": "default",
        "skymapper": "default",
        "sdss": "default",
        "wise": "default",
        "twomass": "default",
        "custom": custom_entry,
    },
)

# formats plots for use in grid
grid_plots = gridsetup(
    dimensions={"width": 6, "height": 6},
    plots=[
        {"name": "image", "figure": image, "width": 2, "height": 2},
        {"name": "hrd", "figure": hrd, "width": 2, "height": 2},
        {"name": "sed", "figure": sed, "width": 2, "height": 2},
        {"name": "lightcurves", "figure": lightcurves, "width": 2, "height": 1},
        {"name": "buttons", "figure": buttons, "width": 2, "height": 1},
        {"name": "spectrum", "figure": spectrum, "width": 4, "height": 2},
        {"name": "metadata_table", "figure": metadata, "width": 6, "height": 2},
    ],
    grid_size=grid_size,
)

# set up the final grid
datapage = layout(
    column(
        row(
            grid_plots["image"],
            grid_plots["hrd"],
            column(grid_plots["buttons"], grid_plots["lightcurves"]),
        ),
        row(grid_plots["sed"], grid_plots["spectrum"]),
        row(grid_plots["metadata_table"]),
    )
)

# give output file a name
output_file(f"{source}_datapage.html")

# show the datapage (also saves it)
show(datapage)
```

![](https://github.com/WD-planets/AstroToolkit/raw/latest/README_Images/datapage_example.png?raw=true)

**Note:** This example can be loaded from within the package using:

```
from AstroToolkit.Examples import datapage
```
