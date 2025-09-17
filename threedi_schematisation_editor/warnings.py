class ThreediSchematisationEditorWarning(UserWarning):
    """
    Base warning class for the Threedi Schematisation Editor.
    """


class StructuresIntegratorWarning(ThreediSchematisationEditorWarning):
    """
    Custom warning to indicate issues related to the Structures Integrator.
    """


class FeaturesImporterWarning(ThreediSchematisationEditorWarning):
    """
    Custom warning to indicate issues related to the Structures Integrator.
    """


class ProcessorWarning(ThreediSchematisationEditorWarning):
    """
    Custom warning to indicate issues related to the Processor.
    """


class GeometryImporterWarning(ThreediSchematisationEditorWarning):
    """
    Custom warning to indicate issues related imported geometries
    """
