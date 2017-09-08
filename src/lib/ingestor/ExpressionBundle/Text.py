from ..ExpressionEvaluator import ExpressionEvaluator

class _Text(object):
    """
    Basic image sequence functions.
    """

    @staticmethod
    def upper(string):
        """
        Return string coverted to upper case.
        """
        return str(string).upper()

    @staticmethod
    def lower(string):
        """
        Return string coverted to lower case.
        """
        return str(string).lower()

    @staticmethod
    def replace(text, searchValue, replaceValue):
        """
        Return a string where all search value are replaced by the replace value.
        """
        return text.replace(searchValue, replaceValue)

    @staticmethod
    def remove(text, removeValue):
        """
        Return a string where all remove value are removed from the text.
        """
        return text.replace(removeValue, '')


# upper case
ExpressionEvaluator.register(
    'upper',
    _Text.upper
)

# lower case
ExpressionEvaluator.register(
    'lower',
    _Text.lower
)

# replace
ExpressionEvaluator.register(
    'replace',
    _Text.replace
)

# remove
ExpressionEvaluator.register(
    'remove',
    _Text.remove
)
