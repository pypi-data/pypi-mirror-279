
class Model:

    @classmethod
    def from_json(cls, data: dict):
        """Loads class info from dictionary"""
        if 'type' in data.keys():
            data.pop('type')
        return cls(**data)

    def convert(self, cls):
        self.__class__ = cls

