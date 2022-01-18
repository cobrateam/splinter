import os
import tempfile


class HTMLSnapshotTest:
    def test_take_screenshot_no_unique_file(self):
        """When the unique_file parameter is false,
        Then the filename should match the name parameter exactly.
        """
        self.browser.html_snapshot(name='test_html_snap', unique_file=False)
        expected_filepath = os.path.abspath('test_html_snap.png')
        assert os.path.isfile(expected_filepath)

    def test_html_snapshot(self):
        """Should take an html snapshot of the current page."""
        filename = self.browser.html_snapshot()
        assert tempfile.gettempdir() in filename

    def test_html_snapshot_with_prefix(self):
        """Should add the prefix to the snapshot filename"""
        filename = self.browser.html_snapshot(name="foobar")
        assert "foobar" in filename

    def test_html_snapshot_with_suffix(self):
        """Should add the suffix to the snapshot filename"""
        filename = self.browser.html_snapshot(suffix="xml")
        assert "xml" == filename[-3:]
