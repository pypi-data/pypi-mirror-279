import pathlib


class StructureMixin:
    """
    These behaviours are common to every part of the file structure
    """

    def __str__(self):
        return self.id

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.id}')"

    @property
    def path(self) -> pathlib.Path:
        raise NotImplementedError

    @property
    def uri(self) -> str:
        return self.path.as_uri()
