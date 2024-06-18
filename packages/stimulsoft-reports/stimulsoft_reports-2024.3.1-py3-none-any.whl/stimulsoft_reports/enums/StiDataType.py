from enum import Enum


class StiDataType(Enum):

    NONE: None
    JAVASCRIPT = 'text/javascript'
    JSON = 'application/json'
    XML = 'application/xml'
    HTML = 'text/html'


### Helpers

    @staticmethod
    def getValues():
        return [enum.value for enum in StiDataType if enum.value != None]