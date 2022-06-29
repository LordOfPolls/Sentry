import logging
from abc import abstractmethod

from naff import Extension
from naff.api.events import RawGatewayEvent


class Template(Extension):
    known_types: list[int]
    known_fields: list[str]
    log = logging.getLogger("Sentry_Ext")

    async def update_fields(self, new_fields: list[str]):
        self.known_fields += new_fields

        # todo: persistent storage

    async def update_types(self, new_type: int):
        self.known_types.append(new_type)

        # todo: persistent storage

    @abstractmethod
    async def dict_parser(self, event: RawGatewayEvent):
        raise NotImplementedError()
