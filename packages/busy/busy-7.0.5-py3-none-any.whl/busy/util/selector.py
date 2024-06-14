import re


class Selector:

    CRITERIUM_TYPES = []

    @classmethod
    def add_criterium_type(self, criterium_type):
        self.CRITERIUM_TYPES.append(criterium_type)

    @classmethod
    def get_criterium(self, word):
        for criterium_type in self.CRITERIUM_TYPES:
            if criterium_type.match(word):
                return criterium_type(word)
        raise RuntimeError(f"Invalid selection criterium {word}")

    def __init__(self, args):
        self.filter = [c for c in [self.get_criterium(w) for w in args] if c]

    def hit(self, index, value, count):
        if self.filter:
            return any([c.hit(index, value, count) for c in self.filter])
        else:
            return True

    def indices(self, elements):
        enumeration = enumerate(elements)
        count = len(elements)
        return [i for i, t in enumeration if self.hit(i, t, count)]


class NumberCriterium:

    def match(word):
        return str(word).isdigit()

    def __init__(self, word):
        self.index = int(word) - 1

    def hit(self, index, value, count):
        return index == self.index


Selector.add_criterium_type(NumberCriterium)


class RangeCriterium:

    def match(word):
        return isinstance(word, str) and bool(re.match(r'^\d*\-\d*$', word))

    def __init__(self, word):
        split = word.split('-')
        self.start = int(split[0]) - 1 if split[0] else None
        self.end = int(split[1]) - 1 if split[1] else None

    def hit(self, index, value, count):
        if self.start is None and self.end is None:
            return index == count - 1
        elif self.end is None:
            return index >= self.start
        else:
            return index >= self.start and index <= self.end


Selector.add_criterium_type(RangeCriterium)


class TagCriterium:

    def match(word):
        return isinstance(
            word, str) and bool(
            re.match(r'^\#[a-zA-Z0-9\-]+$', word))

    def __init__(self, word):
        self.tag = str(word).lower()

    def hit(self, index, value, count):
        return self.tag in str(value).lower().split()


Selector.add_criterium_type(TagCriterium)


class FunctionCriterium:
    """Evaluates a function against the value (not the index)"""

    def match(arg):
        return callable(arg)

    def __init__(self, arg):
        self.func = arg

    def hit(self, index, value, count):
        return self.func(value)


Selector.add_criterium_type(FunctionCriterium)
