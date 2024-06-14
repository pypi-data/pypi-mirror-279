"""Unit tests for t_bug_catcher flake8 plugin."""
import pytest
from flake8.api import legacy as flake8
from flake8_t_bug_catcher import TBugCatcherHook
import tempfile


@pytest.fixture
def code_without_issues():
    """Code without issues."""
    return """
import t_bug_catcher

try:
    pass
except Exception:
    t_bug_catcher.report_error()
"""


def run_flake8_on_code(code, plugin):
    """Run flake8 on code and return the number of errors."""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py") as temp_file:
        temp_file.write(code)
        temp_file.flush()  # Ensure content is written to disk

        style_guide = flake8.get_style_guide(plugins=[plugin])
        report = style_guide.check_files([temp_file.name])

        return report.total_errors


def test_code_without_issues(code_without_issues):
    """Check that the code without issues is not detected."""
    errors = run_flake8_on_code(code_without_issues, TBugCatcherHook)
    assert errors == 0  # Expecting no issues
