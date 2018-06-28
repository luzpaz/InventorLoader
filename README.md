# InventorLoader
Loads / Imports Autodesk (R) Inventor (R) files into FreeCAD (min. Version 0.17). Until now only
Parts (IPT) but nor assemblies (IAM) nor drawings (IDW) can be displayed.

## Prerequisites
- The AddON requires additional python packages in the FreeCAD python installation:
  - https://pypi.python.org/pypi/xlrd - for reading embedded Excel workbooks
  - http://pypi.python.org/pypi/xlutils - for preparing imported Excel workbooks to
    be stored
  - https://pypi.python.org/pypi/xlwt - for writing embedded Excel workbooks
  - http://www.decalage.info/python/olefileio - olefile for reading Microsoft OLE(2)
  	files.
- Minimum Version 0.17 of FreeCAD is required!

## Installation
Download the repository as a ZIP archive and expand its content directly into the
FreeCAD module's folder "Mod".There exists two locations where FreeCAD searches for
addons:  
a) beside FreeCAD's bin folder  
b) in user's application data (%APPDATA% on windows) or home folder (on linux/MAC).  
A new folder "InvetorLoader-master" will be created.

The next time FreeCAD will offer new import formats for ACIS' SAT (\*.sat) files and Autodesk
Inventor's IPT (\*.ipt) files as supported import formats.

As new python packages are required (ref. "Prerequisites") FreeCAD has to be restarted
so that the new packages become available.

### Solving installation problems
Sometimes it can happen that the packages can't be installed.  
a) navigate to the InventorLoader plugin (ILP) folder with your file-browser (e.g.
   Windows-Explorer)
b) Extract the libs.zip into the ILP's folder (a new folder libs should be created).
c) open a command shell (e.g. `cmd` on windows or `sh` on linux)
   i) adapt the PATH variable to point to FreeCAD's python: `set PATH="<PATH-TO-FREECAD>\bin";%PATH%`
      (on linux you have to export the PATH variable - I think). Linux and MAC users
      should use '/' instead of '\'!
   ii) change the working folder to ILP's libs folder (e.g. `cd <PATH-TO-FREECAD>\Mod\InventorLoader-master\libs`)
   iii) run the installation script: `python ./installLibs.py`  
      This should install the required packages.
d) reopen FreeCAD

## Status:
> Alpha!

Autodesk Inventor files have a OLE2 files.
That allows it to embed Excel workboos e.g.

- The addon is able to read Inventor files from 2010 till 2019.
- Read the iProperties (only a few can be applied in FreeCAD)
- Display embedded workbooks as a new spreadsheet
- Two strategies are provided:
 -- feature base: the addon tries to rebuild all the features.
 -- SAT based: like STEP file, model will be imported based on FACE, EDGES and VERTICES.

## History:
- 0.9.1 Added colors to STEP.  

- 0.9 Added convertation to STEP.
	IPT files can now either be imported
	* based on features (nearest to FreeCAD so changing the model is easy)
	* based on SAT (model is imported based on stored Surfaces and Edges)
	* based on STEP (SAT model is converted to STEP and importd into FreeCAD using built in reader)

- 0.8.1 Fixed support of cone surfaces.

- 0.8 Added handling of Inventor 2019 file format.

- 0.7.2 added interpolated surfaces for SAT files.

- 0.7.1 added interpolated curves for SAT files.

- 0.7: added ACIS file format reading for IPT and SAT files.
	* IPT: during import user selectable strategy with thumbnail.

- 0.6: continued working on Features
	* added Coil as Part::Helix and Part::Spiral with Sweep
	* automated installation of required site-packages

- 0.5.5: Maintenance version
	* Fixed wrong creation of boundary wires/faces from sketches
	* Fixed wrong handling of constraints in sketches
	* Code reviewed

- 0.5.4: continued working on Features
	* added Sweep  as Part::Sweep
	* added Thicken as Part::Offset
	* Fixed encoding problems regarding filename and Sketch/Feature names

- 0.5.3: continued working on Features
	* added Client as a new group of objects.

- 0.5.2: continued working on Features
	* added Hole as combination of creating Part::Cylinder, Part::Cone(s) and Part::MultiFuse and Part::Cut

- 0.5.1: continued working on Features
	* added Revolve as Part::Revolution
	* added Extrude as Part::Extrusion
	* added Loft  as Part::Loft
	* added boolean operations as Part::Cut, Part::MultiFuse, Part::MultiCommon
	* added Polar-Pattern, Rectangular-Pattern with Draft.makeArray()
	* added Mirror-Pattern as 'Part::Mirroring'

- 0.5: Preparation for supporting Features (except iFeature)
	Most sections found in pro samples (2010..2018) are now decoded (structured)

- 0.4.2: Only Code Review
	Most sections found in LT samples are now decoded (structured)

- 0.4.1: Completed parameter management.
	Parameter table now contains the name, value, formula, tolerance and comment
	of each parameter
	- Added parameter unit handling
	- Added parameter formulas handling
	- Added parameter operations handling (e.g. '+', '-', '*' and '/')
	Even if operations or functions are not supported by FreeCAD (e.g. modulo
	operator, signum or random function), parameters will be replaced by their
	nominal value and unit.

- 0.4: Added spreadsheet for parameters.
	- Added handling of expressions for parameters
	- fixed missing placement for 2D-sketches

- 0.3: Started working on sketches.
	- Added placement to sketches. <s>Sometimes Placements have to "Orientation"
	  references, so that a correct placement is not possible</s>
	- Added pad feature. Maybe this will be changed to Part instead of PartDesign.

- 0.2: Reading document content now from DC-Segment instead of Graphics-/Browser-
  Segment
	- added reading of object names
	- 2D sketch constraints and dimensions

- 0.1: first "working" prototype.
	- reading Inventor file Structure
	- reading compressed data for Model-Segments (e.g. Graphics- and Browser-View)
	- displaying Sketches
		- Points-2D
		- Line-2D
		- (Arc-)Circle-2D
		- (Arc-)Ellipse-2D
	- embedded files dumped to export folder

## Next steps in unsorted order:
- Features like Grave, etc.
- Features like Fillet, Champher, Draft, etc.
- Preferences page
