def _concat_xpath_from_str(text):
    """Take a string and splice it into an xpath concat locator.

    Arguments:
        text (str): Text block to scan.
    """
    concat_text = _recurse(
        text,
        split_on='\"',
        wrapper="'{}',",
        replacer="'\"',",
    )
    return '//*[text()=concat({} "")]'.format(concat_text)


def _recurse(text, split_on, wrapper, replacer, inner=False):
    """Take a string, split it, then build a new string from the parts.

    The position of the character used to split the original string will be
    replaced in the new string by cap.

    Arguments:
        text (str): Text block to scan.
        split_on (str): A character to remove via splitting.
        wrapper (str): The wrapper for each sub-block.
        replacer (str): The replacement for the removed character.
        inner (bool): True if already inside a sub-block.

    Returns:
        str

    """
    final_value = ''
    split_text = text.split(split_on)

    # Ignore single length split lists in nested searches.
    if inner and len(split_text) <= 1:
        return

    for index, item in enumerate(split_text):
        # Check every block of text for a single quotation mark
        sub_block = _recurse(
            item,
            split_on="\'",
            wrapper='"{}",',
            replacer='"\'",',
            inner=True,
        )

        if sub_block:
            final_value += sub_block

        else:
            final_value += wrapper.format(item)

        # Don't cap the last item in the block.
        if index != len(split_text) - 1:
            final_value += replacer

    return final_value
