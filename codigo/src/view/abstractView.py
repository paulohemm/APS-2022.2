from abc import ABC, abstractmethod

class AbstractView(ABC):

    #dict keys as integers mean nothing to me
    def set_keys_to_attrs(self, values, attributes):
        count = 0
        foo = {}
        for value in values:
            foo[attributes[count]] = value
            count += 1

        return foo

