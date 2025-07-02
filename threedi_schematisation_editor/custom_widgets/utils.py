import inspect
import warnings

from threedi_schematisation_editor import warnings as threedi_warnings


class CatchThreediWarnings:
    """
    A context manager that catches warnings from threedi_schematisation_editor.warnings,
    compiles them into a warnings_msg, and logs them to QGIS log system.
    """

    def __init__(self, log_category="Warnings"):
        self.caught_warnings = []
        self.warnings_msg = ""
        self.log_category = log_category

    def __enter__(self):
        # Create a warnings list to store caught warnings
        self._warnings_list = []

        # Save the old showwarning function to restore it later
        self._old_showwarning = warnings.showwarning

        # Define a custom function to intercept warnings
        def _showwarning(message, category, filename, lineno, file=None, line=None):
            self._warnings_list.append((message, category, filename, lineno))

        # Replace the default showwarning with our custom one
        warnings.showwarning = _showwarning

        # Set up the warnings filter
        warnings.simplefilter("ignore")  # Ignore all warnings by default

        # Enable warnings for all warning classes in the threedi module
        for name, obj in inspect.getmembers(threedi_warnings):
            if inspect.isclass(obj) and issubclass(obj, Warning):
                warnings.simplefilter("always", obj)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore the original showwarning function
        warnings.showwarning = self._old_showwarning

        # Process the warnings
        self.caught_warnings = self._warnings_list

        # Generate the warning message if any warnings were caught
        if self.caught_warnings:
            self.warnings_msg = (
                "\n\nNote: Some warnings were raised during the process. "
                "Check the 'Warnings' log for more details."
            )

            # Log each warning to QGIS
            for warning_info in self.caught_warnings:
                message, category, filename, lineno = warning_info
                warning_text = f"{category.__name__}: {message}"
                QgsMessageLog.logMessage(warning_text, self.log_category, level=Qgis.Warning)

        # Reset the warnings filter
        warnings.resetwarnings()

        # Don't suppress any exceptions
        return False
