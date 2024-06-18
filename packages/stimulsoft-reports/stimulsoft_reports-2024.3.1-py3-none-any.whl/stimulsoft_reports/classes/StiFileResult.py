from __future__ import annotations

from stimulsoft_data_adapters.classes.StiBaseResult import StiBaseResult

from ..enums import StiDataType


class StiFileResult(StiBaseResult):

### Properties
    
    data: bytes = None
    dataType: StiDataType = None


### Result

    def getError(notice: str) -> StiFileResult:
        """Creates an error result."""

        result: StiFileResult = StiBaseResult.getError(notice)
        result.__class__ = StiFileResult
        return result
    

### Constructor

    def __init__(self, data: bytes | str, dataType: StiDataType) -> None:
        self.data = data.encode() if type(data) == str else data
        self.dataType = dataType