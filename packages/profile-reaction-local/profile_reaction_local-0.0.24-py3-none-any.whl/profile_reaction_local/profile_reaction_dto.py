import json

from logger_local.LoggerLocal import Logger

from .constants_profile_reaction import OBJECT_TO_INSERT_CODE

logger = Logger.create_logger(object=OBJECT_TO_INSERT_CODE)


class ProfileReactionDto:

    def __init__(self, **kwargs):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME, object={'kwargs': kwargs})
        self.kwargs = kwargs
        logger.end(INIT_METHOD_NAME, object={'kwargs': kwargs})

    def get(self, attr_name, default=None):
        arguments = getattr(self, 'kwargs', default)
        value = arguments.get(attr_name, default)
        return value

    def get_arguments(self):
        return getattr(self, 'kwargs', None)

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self) -> dict:
        return self.__dict__["kwargs"]

    def __repr__(self):
        return f"ProfileReactionDto({self.kwargs})"

    def __eq__(self, other):
        if not isinstance(other, ProfileReactionDto):
            return False
        return self.__dict__ == other.__dict__
