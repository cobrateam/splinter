from manpage import Writer
from sphinx.builders.text import TextBuilder


class ManBuilder(TextBuilder):
    name = 'manpage'
    format = 'man'
    out_suffix = '.man'

    def prepare_writing(self, docnames):
        self.writer = ManpageWriter(self)


class ManpageWriter(Writer):
    def __init__(self, builder):
        self.builder = builder
        Writer.__init__(self)


def setup(app):
    app.add_builder(ManBuilder)



