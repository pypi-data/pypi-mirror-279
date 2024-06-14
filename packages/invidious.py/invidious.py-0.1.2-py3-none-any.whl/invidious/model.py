
class Model:

    def from_json(self, data) -> None:
        """Loads class info from dictionary"""
        for key in data:
            setattr(self, key, data[key])

    def convert(self, cls):
        self.__class__ = cls

