from fake_webapp import EXAMPLE_APP


class SlowlyTypeTest(object):

    def test_simple_type(self):
        "should provide a away to change field value using type method"
        self.browser.visit(EXAMPLE_APP)
        self.browser.type('query', ' with type method')
        value = self.browser.find_by_name('query').first.value
        self.assertEquals('default value with type method', value)

    def test_simple_type_on_element(self):
        self.browser.visit(EXAMPLE_APP)
        self.browser.find_by_name('query').type(' with type method')
        value = self.browser.find_by_name('query').first.value
        self.assertEquals('default value with type method', value)

    def test_slowly_typing(self):
        "should be able to slowly type some text in a field"
        self.browser.visit(EXAMPLE_APP + 'type')
        num = 0
        num_max = 6
        for key in self.browser.type('type-input', 'typing', slowly=True):
            self.assertEquals(self.browser.is_text_present("#%d" % num), True)
            num += 1
        self.assertEquals(num, num_max)

        element = self.browser.find_by_name('type-input').first
        self.assertEquals(element.value, 'typing')

    def test_slowly_typing_on_element(self):
        self.browser.visit(EXAMPLE_APP + 'type')
        num = 0
        num_max = 6
        for key in self.browser.find_by_name('type-input').type('typing', slowly=True):
            self.assertEquals(self.browser.is_text_present("#%d" % num), True)
            num += 1
        self.assertEquals(num, num_max)

        element = self.browser.find_by_name('type-input').first
        self.assertEquals(element.value, 'typing')
