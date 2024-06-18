import copy

from stimulsoft_data_adapters.events.StiEventArgs import StiEventArgs

from .enums.StiPrintAction import StiPrintAction


class StiReportEventArgs(StiEventArgs):

### Fields

    __report: object = None


### Properties

    @property
    def report(self) -> object:
        """The current report JSON object with the set of all properties."""

        return self.__report
    
    @report.setter
    def report(self, value: object):
        self.__report = copy.deepcopy(value)
    
    fileName: str = None
    """The name of the report file to save."""

    isWizardUsed: bool = None
    """A flag indicating that the wizard was used when creating the report."""

    autoSave: bool = None
    """A flag indicating that the report was saved automatically."""

    printAction = StiPrintAction.NONE
    """[enum] The current print type of the report."""
