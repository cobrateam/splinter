from nose.tools import assert_equals
from fake_webapp import EXAMPLE_APP


class SlowlyTypeTest(object):

    def test_simple_type(self):
        "should provide a away to change field value using type method"
        self.browser.visit(EXAMPLE_APP)
        self.browser.type('query',' with type method')
        value = self.browser.find_by_name('query').first.value
        assert_equals('default value with type method', value)

    def test_slowly_typing(self):
        "should be able to slowly type some text in a field"
        self.browser.visit(EXAMPLE_APP + 'type')
        num = 0
        num_max = 6
        for key in self.browser.type('type-input', 'typing', slowly=True):
            assert_equals(self.browser.is_text_present("#%d" % num), True)
            num += 1
        assert_equals(num, num_max)

        element = self.browser.find_by_name('type-input').first
        assert_equals(element.value, 'typing')

