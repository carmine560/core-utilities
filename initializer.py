"""Script execution environment initialization utilities."""

import os

from . import file_utilities


class Initializer:
    """Initialize the script execution environment."""

    def __init__(self, vendor, process, script_path):
        """Construct an Initializer instance."""
        self.vendor = vendor
        if os.path.isfile(process):
            self.executable = os.path.abspath(process)
            self.process = os.path.splitext(os.path.basename(self.executable))[
                0
            ]
        else:
            self.executable = None
            self.process = process

        self.script_file = os.path.basename(script_path)
        self.script_base = os.path.splitext(self.script_file)[0]
        self.config_path = file_utilities.get_config_path(script_path)
        self.config_directory = os.path.dirname(self.config_path)

        self.actions_section = f"{self.process} Actions"
        self.variables_section = f"{self.process} Variables"
