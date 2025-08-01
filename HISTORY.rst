History
=======

2.3.2 (unreleased)
------------------

- Nothing changed yet.


2.3.1 (2025-07-16)
------------------

- Bump Dependency Loader plugin version to 1.2.1 (nens/nens-dependency-loader#14)


2.3 (2025-06-10)
----------------

- Add processing algorithm to add NWRW parameters to surface parameters (#333)
- Fix removing of cross-section locations associated to channels not modified by object import (#378)
- Processing algorithms 'Map surfaces/DWF to connection nodes' now use point on surface instead of centroid as start vertex of mapping line (#396)
- Reset unspecified import settings on loading new import configuration (#286)
- Fix handling string keys in import with value_map (#279)
- Handle using source layer from conversion processing algorithms which is not a `QgsVectorLayer` (#404)
- Changing Material back to what it was does not update the friction value (#345)
- Allow digitising and importing pipes with > 2 vertices (#342)


2.2.2 (2025-05-20)
------------------

- Table control, memory control: dynamically change form based on "action type" (#381)
- Fix integrating objects with line geometries that contain more than 2 points (#382)
- Fix bug that showed error on loading channel attribute table (#379)
- Handle importing and integrating overlapping objects on channels (#370)


2.2.1 (2025-05-12)
------------------

- Fix integrating objects in channels when connection node and channel start do not match exactly (#372)

2.2.0 (2025-05-07)
------------------

- Display upgrade warnings (any UserWarning raised during upgrading)
- Split BoundaryTypes in 1D and 2D types and add boundary types Discharge (total) and Groundwater discharge (total) to BoundaryType2D
- Force conversion on importing feature attributes and show warnings when this is not possible
- Correctly set id's when importing orifices or weirs with edit channels option active (#363)
- Fix zooming to DEM extent when schematisation CRS differs from project CRS
- Fix associating imported structures with existing channels (#369)
- Add new sewerage types: Infiltration drain (8), Slot/trench drain (9), Pressure sewer (10)


2.1.4 (2025-04-18)
------------------

- Correct TargetType Enum for memory and table control
- Surface styling 25% transparent
- Fix disconnect between integer fields with boolean widgets
- Fix for grid level


2.1.3 (2025-04-14)
------------------

- Styling no longer causes unresponsiveness when editing vertices (#359)


2.1.2 (2025-04-14)
------------------

- Styling no longer causes unresponsiveness when editing vertices (#359)
- Added backwards compatibility to load a schematisation in 3.28. (#351)


2.1.1 (2025-04-03)
------------------

- Added check for obsolete geopackages generated by schematisation editor.

2.1 (2025-04-02)
----------------

- Bumped threedi-mi-utils to 0.1.10.


2.0 (2025-04-01)
----------------

- Update schematisation to >300.


1.16 (2024-12-03)

- Fixed import error

1.15 (2024-12-02)
-----------------

- Fix type error: #278
- Add news to QGIS news feed (#281)


1.14 (2024-11-12)
-----------------

- Add new 1D advection options
- Fixes/enhancements: #149, #254, #270

1.13.0 (2024-09-24)
-------------------

- Fixes/enhancements: #116, #250, #257
- Added handling of the multiple schematisations.
- Implemented import of the linear structures from the point datasets (#167).


1.12.0 (2024-07-17)
-------------------

- Fixes/enhancements: #184, #238, #241


1.11.0 (2024-06-21)
-------------------

- Fixes/enhancements: #236


1.10.1 (2024-06-05)
-------------------

- Fixes/enhancements: #188, #190, #196, #211, #219, #220, #221, #222, #224, #227, #228, #229, #230, #232


1.10 (2024-04-12)
-----------------

- Fixes/enhancements: #191
- No longer commit changes in processing algorithms "Manhole bottom levels from pipes" and "Map (impervious) surfaces to connection nodes"
- Add documentation to processing algorithm "Manhole bottom level from pipes"

1.9 (2024-03-14)
----------------

- Fixes/enhancements: #193, #194, #209, #976


1.8 (2024-01-11)
----------------

- Fixes/enhancements: #117, #503


1.7.2 (2023-12-01)
------------------

- Fixes/enhancements: #192


1.7.1 (2023-10-16)
------------------

- Fixes/enhancements: #100, #185


1.7.0 (2023-09-29)
------------------

- Fixes/enhancements: #170
- Added Import Weirs tool (#178, #179)
- Added Import Orifices tool (#180, #181)


1.6.0 (2023-09-21)
------------------

- Fixes/enhancements: #67, #103, #158, #161, #162, #169, #174
- Added Import Culverts GUI (#119)
- Added new friction types (#159)


1.5.0 (2023-06-16)
------------------

- Fixed issues: #141, #142
- Compatibility with schema 217 (#148)
- Added Vegetation drag settings table with associated raster layers (#145)
- Add "Import culverts" processing algorithm (#127)
- Exposing attributes for vegetation and groundwater exchange (#151, #153)


1.4.1 (2023-04-28)
------------------

- Fixed issue #139.


1.4 (2023-04-26)
----------------
- Compatibility with schema 216 (#451).
- Fixed issues: #126, #129, #134
- Added processing algorithm to generate exchange lines
- Added handling of the "Inverted egg" and "XY" cross-section shape types. (#89, #91)
- Changed the way of editing cross-section table to using proper table view. (#90)
- Sorted imports


1.3 (2023-02-06)
----------------

- Several UI fixes.
- Added fix for issue #107. (#112)
- Added breaches and exchange lines. (#111)
- Upgraded required schema version to 214.


1.2 (2022-11-28)
----------------

- Added 3Di plugin icon.
- Added explainer text for the cross-section 'table' input widgets (#64).
- Add units to attribute forms (#77).
- Initial cross section table validators (#76).
- Fix for issue #80, #79, #86, #75.
- Added compatibility with schema version 208 (#81).
- Added saving spatialite schema version in the geopackage.
- Removed "max_capacity" field from the Orifice layer.
- Modified channels editing rules.
- Added enabling/disabling the width, height and table widgets based on the cross-section shape (#82).
- Updated minimal schema version to 209.

1.1.1 (2022-06-29)
------------------

- Simplified schema migration workflow.


1.1 (2022-06-14)
----------------

- Prepared for release.


1.0.9 (2022-06-02)
------------------

- Added docker-compose configuration.


1.0.8 (2022-06-02)
------------------

- Github action: prevent zip from being generated twice.


1.0.7 (2022-06-02)
------------------

- Updated tests to run on Linux
- Added Docker container for running tests


1.0.6 (2022-05-18)
------------------

- Fix in run attribute in github workflow.


1.0.5 (2022-05-18)
------------------

- Added upload scripts and github workflows.


1.0.4 (2022-05-18)
------------------

- ZIP generation.


1.0.3 (2022-05-18)
------------------

Initial release.
