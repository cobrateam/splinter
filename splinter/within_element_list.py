from splinter.element_list import ElementList


class WithinElementList(ElementList):

    def find_by_css(self, element):
        """
        Performs a find in the element context using the provided selector.
        """
        for context_elements in self.context:
          final_elements = context_elements.find_by_css(element)
        return final_elements
