"""Main module."""
from t_bug_catcher.validation import PreRunValidation


class TBugCatcherHook:
    """Main class for the plugin."""

    name = "flake8-t-bug-catcher"
    version = "0.1.0"

    def __init__(self, tree, filename):
        """Initialize the checker."""
        self.filename = filename

    def run(self):
        """Run the checker."""
        pre_run_validation = PreRunValidation()
        pre_run_validation.validate_file(self.filename)

        for warning in pre_run_validation.warnings:
            yield warning.lineno, 0, f"{warning.warning_code}: {warning.message}", type(self)
