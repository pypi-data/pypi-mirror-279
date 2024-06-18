from __future__ import annotations

from stimulsoft_data_adapters.classes.StiBaseResult import StiBaseResult


class StiResult(StiBaseResult):
    """
    The result of processing a request from the client side. The result object will contain a collection of data, 
    message about the result of the command execution, and other technical information.
    """

### Abstract

    fileName: str
    variables: list
    settings: dict
    report: object

    
### Result

    @staticmethod
    def getSuccess(notice: str = None) -> StiResult:
        """Creates a successful result."""
        
        result: StiResult = StiBaseResult.getSuccess(notice)
        result.__class__ = StiResult
        return result
    
    @staticmethod
    def getError(notice: str) -> StiResult:
        """Creates an error result."""

        result: StiResult = StiBaseResult.getError(notice)
        result.__class__ = StiResult
        return result