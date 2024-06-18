import typing


class VolumeRequest:
    create_if_not_exists: bool
    name: str

    def __init__(self, name: str, create_if_not_exists: typing.Optional[bool] = None):
        self.name = name
        self.create_if_not_exists = create_if_not_exists or False
