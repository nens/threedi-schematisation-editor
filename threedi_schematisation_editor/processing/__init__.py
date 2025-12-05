# Copyright (C) 2025 by Nelen & Schuurmans
import os

from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon

from threedi_schematisation_editor.processing.alghorithms_inflow import (
    AddNWRWSurfaceParameters,
    LinkDWFWithConnectionNodes,
    LinkSurfacesWithConnectionNodes,
)
from threedi_schematisation_editor.processing.algorithm_rasterize_channels import (
    RasterizeChannelsAlgorithm,
)
from threedi_schematisation_editor.processing.algorithms_1d import BottomLevelCalculator
from threedi_schematisation_editor.processing.algorithms_1d2d import (
    GenerateExchangeLines,
)
from threedi_schematisation_editor.processing.algorithms_import_utils import (
    ExtractLayerByNameAlgorithm,
    GetConfigFileAlgorithm,
)
from threedi_schematisation_editor.processing.algorithms_vector_data_importer import (
    ImportChannels,
    ImportConnectionNodes,
    ImportCrossSectionData,
    ImportCrossSectionLocation,
    ImportCulverts,
    ImportOrifices,
    ImportPipes,
    ImportWeirs,
)


class ThreediSchematisationEditorProcessingProvider(QgsProcessingProvider):
    def __init__(self):
        QgsProcessingProvider.__init__(self)
        self.activate = False
        self.algorithms_list = None

    def id(self):
        return "threedi_schematisation_editor"

    def name(self):
        return "Rana Schematisation Editor"

    def icon(self):
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "icons",
            "rana_blue_on_transparent.svg",
        )
        return QIcon(icon_path)

    def load(self):
        self.refreshAlgorithms()
        return True

    def unload(self):
        QgsProcessingProvider.unload(self)
        self.algorithms_list = None

    def loadAlgorithms(self):
        self.algorithms_list = [
            LinkSurfacesWithConnectionNodes(),
            LinkDWFWithConnectionNodes(),
            AddNWRWSurfaceParameters(),
            GenerateExchangeLines(),
            ImportCrossSectionLocation(),
            ImportCrossSectionData(),
            ImportConnectionNodes(),
            ImportCulverts(),
            ImportOrifices(),
            ImportWeirs(),
            ImportPipes(),
            ImportChannels(),
            BottomLevelCalculator(),
            RasterizeChannelsAlgorithm(),
            ExtractLayerByNameAlgorithm(),
            GetConfigFileAlgorithm(),
        ]
        for alg in self.algorithms_list:
            self.addAlgorithm(alg)
