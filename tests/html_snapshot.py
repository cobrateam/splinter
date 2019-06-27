import tempfile


class HTMLSnapshotTest(object):
    def test_html_snapshot(self):
        """Should take an html snapshot of the current page."""
        filename = self.browser.html_snapshot()
        self.assertTrue(tempfile.gettempdir() in filename)

    def test_html_snapshot_with_prefix(self):
        """Should add the prefix to the snapshot filename"""
        filename = self.browser.html_snapshot(name="foobar")
        self.assertTrue("foobar" in filename)

    def test_html_snapshot_with_suffix(self):
        """Should add the suffix to the snapshot filename"""
        filename = self.browser.html_snapshot(suffix="xml")
        self.assertEqual("xml", filename[-3:])
