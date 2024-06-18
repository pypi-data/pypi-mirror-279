from ..classes.StiComponent import StiComponent
from ..classes.StiHandler import StiHandler
from ..classes.StiResult import StiResult
from ..enums.StiComponentType import StiComponentType
from ..enums.StiEventType import StiEventType
from ..enums.StiHtmlMode import StiHtmlMode
from ..events.StiComponentEvent import StiComponentEvent
from ..events.StiReportEventArgs import StiReportEventArgs
from ..report.StiReport import StiReport
from .options.StiDesignerOptions import StiDesignerOptions


class StiDesigner(StiComponent):
    
### Events

    onPrepareVariables: StiComponentEvent = None
    """The event is invoked before rendering a report after preparing report variables. Python and JavaScript functions are supported."""

    onBeginProcessData: StiComponentEvent = None
    """The event is invoked before data request, which are needed to render a report. Python and JavaScript functions are supported."""

    onEndProcessData: StiComponentEvent = None
    """The event is invoked after loading data before rendering a report. Python and JavaScript functions are supported."""

    onCreateReport: StiComponentEvent = None
    """The event is invoked after creation a new report in the designer. Python and JavaScript functions are supported."""

    onOpenReport: StiComponentEvent = None
    """The event is invoked before opening a report from the designer menu after clicking the button. Only JavaScript functions are supported."""

    onOpenedReport: StiComponentEvent = None
    """The event is invoked after opening a report before sending to the designer. Python and JavaScript functions are supported."""

    onSaveReport: StiComponentEvent = None
    """The event is invoked when saving a report in the designer. Python and JavaScript functions are supported."""

    onSaveAsReport: StiComponentEvent = None
    """The event is invoked when saving a report in the designer with a preliminary input of the file name. Python and JavaScript functions are supported."""

    onPreviewReport: StiComponentEvent = None
    """The event is invoked when going to the report view tab. Python and JavaScript functions are supported."""

    onExit: StiComponentEvent = None
    """The event is invoked when by clicking the Exit button in the main menu of the designer. Only JavaScript functions are supported."""


### Fields

    __options: StiDesignerOptions = None
    __report: StiReport = None


### Properties

    @property
    def componentType(self) -> StiComponentType:
        return StiComponentType.DESIGNER

    @property
    def handler(self) -> StiHandler:
        """
        Gets or sets an event handler that controls data passed from client to server and from server to client.
        Contains the necessary options for sending data.
        """
        
        return super().handler
    
    @handler.setter
    def handler(self, value: StiHandler):
        super(type(self), type(self)).handler.fset(self, value)
        if value != None:
            value.component = self
            value.onBeginProcessData = self.onBeginProcessData
            value.onEndProcessData = self.onEndProcessData
            value.onPrepareVariables = self.onPrepareVariables

    @property
    def report(self) -> StiReport:
        """Gets or sets a report object for the designer."""

        return self.__report
    
    @report.setter
    def report(self, value: StiReport):
        self.__report = value
        if value != None:
            value.onBeginProcessData = self.onBeginProcessData
            value.onEndProcessData = self.onEndProcessData
            value.onPrepareVariables = self.onPrepareVariables
            value.handler = self.handler
            value.license = self.license
    
    @property
    def options(self) -> StiDesignerOptions:
        """All designer component options, divided by categories."""

        return self.__options
    
    @options.setter
    def options(self, value: StiDesignerOptions):
        if value != None:
            value.component = self
            self.__options = value


### Event handlers

    def __getCreateReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onCreateReport, args)
    
    def __getOpenedReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onOpenedReport, args)

    def __getSaveReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onSaveReport, args)
    
    def __getSaveAsReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        return self._getDefaultEventResult(self.onSaveAsReport, args)
    
    def __getPreviewReportResult(self) -> StiResult:
        args = StiReportEventArgs(self.handler.request)
        result = self._getDefaultEventResult(self.onPreviewReport, args)
        if result != None and args.report != self.handler.request.report:
            result.report = args.report

        return result

    def getEventResult(self) -> StiResult:
        if self.request.event == StiEventType.CREATE_REPORT:
            return self.__getCreateReportResult()
        
        if self.request.event == StiEventType.OPENED_REPORT:
            return self.__getOpenedReportResult()
        
        if self.request.event == StiEventType.SAVE_REPORT:
            return self.__getSaveReportResult()
        
        if self.request.event == StiEventType.SAVE_AS_REPORT:
            return self.__getSaveAsReportResult()
        
        if self.request.event == StiEventType.PREVIEW_REPORT:
            return self.__getPreviewReportResult()
        
        return super().getEventResult()
    

### Helpers
        
    def _updateEvents(self):
        super()._updateEvents()

        if self.onBeginProcessData == None: self.onBeginProcessData = True
        self._updateEvent('onBeginProcessData')

        self._updateEvent('onEndProcessData')
        self._updateEvent('onPrepareVariables')
        self._updateEvent('onCreateReport')
        self._updateEvent('onOpenReport')
        self._updateEvent('onOpenedReport')
        self._updateEvent('onSaveReport')
        self._updateEvent('onSaveAsReport')
        self._updateEvent('onPreviewReport')
        self._updateEvent('onExit')


### HTML

    def _getComponentHtml(self) -> str:
        result = ''

        result += self.options.getHtml()
        result += f"let {self.id} = new Stimulsoft.Designer.StiDesigner({self.options.id}, '{self.id}', false);\n"

        result += self.onPrepareVariables.getHtml(True)
        result += self.onBeginProcessData.getHtml(True)
        result += self.onEndProcessData.getHtml()
        result += self.onCreateReport.getHtml(True)
        result += self.onOpenReport.getHtml()
        result += self.onOpenedReport.getHtml()
        result += self.onSaveReport.getHtml(False, True)
        result += self.onSaveAsReport.getHtml(False, True)
        result += self.onPreviewReport.getHtml(True)
        result += self.onExit.getHtml(False, False, False)

        if self.report != None:
            if not self.report.htmlRendered:
                result += self.report.getHtml(StiHtmlMode.SCRIPTS)

            result += f'{self.id}.report = {self.report.id};\n'
            
        result += f"{self.id}.renderHtml('{self.id}Content');\n"

        return result

    def getHtml(self, mode = StiHtmlMode.HTML_SCRIPTS) -> str:
        if mode == StiHtmlMode.HTML_PAGE:
            self.options.appearance.fullScreenMode = True
    
        return super().getHtml(mode)
    

### Constructor

    def __init__(self):
        super().__init__()

        self.id = 'designer'
        self.options = StiDesignerOptions()
        self.handler = StiHandler()