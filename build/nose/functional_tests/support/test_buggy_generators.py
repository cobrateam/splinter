def test_generator_fails_before_yield():
    a = 1 // 0
    yield lambda: True


def test_generator_fails_during_iteration():
    for i in [1, 2, 3, 0, 5, 6]:
        a = 1 // i
        yield lambda: True


def test_ok():
    pass


class TestBuggyGenerators(object):

    def test_generator_fails_before_yield(self):
        a = 1 // 0
        yield lambda: True

    def test_generator_fails_during_iteration(self):
        for i in [1, 2, 3, 0, 5, 6]:
            a = 1 // i
            yield lambda: True

    def test_ok(self):
        pass

