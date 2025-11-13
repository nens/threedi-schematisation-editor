threedi-schematisation-editor
==============================

A QGIS plugin containing N&S' schematisation editor.

Development
------------

Testing happens within a docker container, build (if necessary) and run your docker as follows::

    $ docker compose build qgis-desktop
    $ docker compose run qgis-desktop make test

[Design details can be found here](threedi_schematisation_editor/vector_data_importer/DESIGN.md)


Deployment
----------

Make sure you have ``zest.releaser`` with ``qgispluginreleaser`` installed. The
``qgispluginreleaser`` ensures the metadata.txt, which is used by the qgis plugin
manager, is also updated to the new version. To make a new release enter the following
commands and follow their steps::

    $ cd /path/to/the/plugin
    $ fullrelease

This creates a new release and optionally pushes to github. The deployment step is configured as a Github action. 
In case the commit is tagged with a version (which zest.releaser) does, a zip file ``threedi_schematisation_editor.<version>.zip`` is created
(via ``make zip`` and uploaded to https://artifacts.lizard.net/ via the ``upload-artifact.sh`` script. The tests are also run.

Installation
------------

- In case the plugin manager in QGIS is properly configured, the plugin should also be available via the plugin manager.

