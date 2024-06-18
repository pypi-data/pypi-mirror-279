import base64
import gzip
import os

from ..classes.StiComponent import StiComponent
from ..classes.StiHandler import StiHandler
from ..classes.StiNodeJs import StiNodeJs
from ..classes.StiPath import StiPath
from ..enums.StiComponentType import StiComponentType
from ..enums.StiHtmlMode import StiHtmlMode
from ..events.StiComponentEvent import StiComponentEvent
from ..export.enums.StiExportFormat import StiExportFormat
from ..export.StiDataExportSettings import StiDataExportSettings
from ..export.StiExportSettings import StiExportSettings
from ..export.StiHtmlExportSettings import StiHtmlExportSettings
from ..export.StiImageExportSettings import StiImageExportSettings
from .dictionary.StiDictionary import StiDictionary
from .enums.StiEngineType import StiEngineType
from .enums.StiRangeType import StiRangeType
from .StiPagesRange import StiPagesRange


class StiReport(StiComponent):

### Events

    onBeforeRender: StiComponentEvent = None
    """The event is invoked called before all actions related to report rendering. Only JavaScript functions are supported."""
    
    onAfterRender: StiComponentEvent = None
    """The event is invoked called immediately after report rendering. Only JavaScript functions are supported."""

    onPrepareVariables: StiComponentEvent = None
    """The event is invoked before rendering a report after preparing report variables. Python and JavaScript functions are supported."""

    onBeginProcessData: StiComponentEvent = None
    """The event is invoked before data request, which needed to render a report. Python and JavaScript functions are supported."""

    onEndProcessData: StiComponentEvent = None
    """The event is invoked after loading data before rendering a report. Python and JavaScript functions are supported."""


### Fields

    __dictionary: StiDictionary = None
    __renderCalled = False
    __printCalled = False
    __exportCalled = False
    __openAfterExport = False

    __nodejs: StiNodeJs = None
    __reportString: str = None
    __reportFile: str = None
    __documentString: str = None
    __documentFile: str = None
    __exportFile: str = None
    __exportFormat: int = None
    __pagesRange: str = None
    __exportSettings: StiExportSettings = None


### Helpers

    def __clearReport(self) -> None:
        self.__reportString = None
        self.__reportFile = None
        self.__documentString = None
        self.__documentFile = None
        self.__exportFile = None
    
    def __loadReportFile(self, path: StiPath|str) -> str:
        path = path if isinstance(path, StiPath) else StiPath(path)
        if path.filePath != None:
            with open(path.filePath, mode='r', encoding='utf-8') as file:
                data = file.read()
                if path.fileExtension == 'mrz' or path.fileExtension == 'mdz':
                    return data
                
                buffer = gzip.compress(data.encode())
                return base64.b64encode(buffer).decode()
        
        return None
    
    def __saveReportFile(self, path: StiPath|str, extension: str, data: bytes) -> bool:
        path = path if isinstance(path, StiPath) else StiPath(path)
        if path.directoryPath != None:
            path.fileName = path.fileName or (self.__exportFile or 'Report') + '.' + extension
            filePath = os.path.join(path.directoryPath, path.fileName)
            with open(filePath, mode='wb') as file:
                file.write(data)
                file.close()
                return True
        
        return False
    
    def _updateEvents(self):
        super()._updateEvents()

        if self.onBeginProcessData == None: self.onBeginProcessData = True
        self._updateEvent('onBeginProcessData')

        self._updateEvent('onEndProcessData')
        self._updateEvent('onPrepareVariables')
        self._updateEvent('onBeforeRender')
        self._updateEvent('onAfterRender')
    

### Properties

    engine = StiEngineType.CLIENT_JS
    """Gets or sets the report building and export mode - on the client side in a browser window or on the server side using Node.js"""

    @property
    def componentType(self) -> StiComponentType:
        return StiComponentType.REPORT

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
    def dictionary(self) -> StiDictionary:
        """Gets a report data dictionary that allows you to add new variables to an existing report."""

        return self.__dictionary
    
    @property
    def nodejs(self) -> StiNodeJs:
        """
        Gets the Node.js engine, used to build and export reports on the server side.
        Contains the necessary deployment and operation settings.
        """

        if self.__nodejs == None:
            self.__nodejs = StiNodeJs(self)

        return self.__nodejs
    

### HTML

    def __getLoadReportHtml(self) -> str:
        if len(self.__documentFile or '') > 0:
            return f"{self.id}.loadDocumentFile('{self.__documentFile}');\n"

        elif len(self.__documentString or '') > 0:
            return f"{self.id}.loadPackedDocument('{self.__documentString}');\n"
        
        elif len(self.__reportFile or '') > 0:
            return f"{self.id}.loadFile('{self.__reportFile}');\n"

        elif len(self.__reportString or '') > 0:
            return f"{self.id}.loadPacked('{self.__reportString}');\n"
        
        return ''
    
    def __getPrintHtml(self) -> str:
        if self.__printCalled:
            pagesRange = self.__pagesRange
            pagesRangeHtml = ''
            pagesRangeId = ''

            if self.__pagesRange != None:
                if not isinstance(pagesRange, StiPagesRange) and len(str(pagesRange)) > 0:
                    pagesRange = StiPagesRange(StiRangeType.PAGES, str(pagesRange))
                
                pagesRangeHtml = pagesRange.getHtml()
                pagesRangeId = pagesRange.id

            return f'{pagesRangeHtml}{self.id}.print({pagesRangeId});\n'
        
        return ''
    
    def __getExportHtml(self) -> str:
        result = ''
        if self.__exportCalled:
            exportFileExt = StiExportFormat.getFileExtension(self.__exportFormat)
            exportMimeType = StiExportFormat.getMimeType(self.__exportFormat)
            exportName = StiExportFormat.getFormatName(self.__exportFormat)

            result = self.__exportSettings.getHtml() if self.__exportSettings != None and not self.__exportSettings.htmlRendered else 'let settings = null;\n'
            result += f'{self.id}.exportDocumentAsync(function (data) {{\n'
            if self.engine == StiEngineType.SERVER_NODE_JS:
                result += \
                    "let buffer = Buffer.from(data);\n" \
                    "console.log('{\"type\":\"bytes\", \"data\":\"' + buffer.toString('base64') + '\"}');\n"
            else:
                result += \
                    f"let blob = new Blob([new Uint8Array(data)], {{type: '{exportMimeType}'}});\nlet fileURL = URL.createObjectURL(blob);\nwindow.open(fileURL);\n" \
                    if self.__openAfterExport else f"Stimulsoft.System.StiObject.saveAs(data, '{self.__exportFile}.{exportFileExt}', '{exportMimeType}');\n"
            result += f'}}, Stimulsoft.Report.StiExportFormat.{exportName}, null, settings);\n'
        
        return result
    
    def __getAfterRenderNodeHtml(self) -> str:
        return f"let {self.id}String = {self.id}.savePackedDocumentToString();\n" \
            f"console.log('{{\"type\":\"string\", \"data\":\"' + {self.id}String + '\"}}');\n"

    def _getComponentHtml(self) -> str:
        result = self.license.getHtml()

        result += f'let {self.id} = new Stimulsoft.Report.StiReport();\n'
        
        result += self.onPrepareVariables.getHtml(True)
        result += self.onBeginProcessData.getHtml(True)
        result += self.onEndProcessData.getHtml(process = False)
        result += self.__getLoadReportHtml()
        result += self.dictionary.getHtml()
        result += self.onBeforeRender.getHtml(internal = True)

        if self.__renderCalled:
            result += f'{self.id}.renderAsync(function () {{\n'
            result += self.onAfterRender.getHtml(internal = True)

        result += self.__getPrintHtml()
        result += self.__getExportHtml()

        if self.__renderCalled:
            result += '});\n'

        return result
    

### Load / Save

    def loadFile(self, filePath: str, load = False) -> None:
        """
        Loads a report template from a file or URL address.

        filePath:
            The path to the .mrt file or the URL of the report template.

        load:
            Loads a report file on the server side into report object.
        """
    
        self.__clearReport()
        path = StiPath(filePath)
        self.__exportFile = path.fileNameOnly

        if load: self.__reportString = self.__loadReportFile(path)
        else: self.__reportFile = filePath

    def load(self, data: str, fileName: str = 'Report') -> None:
        """
        Loads a report template from an XML or JSON string and store it as a packed string in Base64 format.

        data:
            Report template in XML or JSON format.

        fileName:
            The name of the report file to be used for saving and exporting.
        """

        self.__clearReport()
        self.__exportFile = fileName
        gzipBytes = gzip.compress(data.encode())
        self.__reportString = base64.b64encode(gzipBytes).decode()

    def loadPacked(self, data: str, fileName = 'Report') -> None:
        """
        Loads a report template from a packed string in Base64 format.

        data:
            Report template as a packed string in Base64 format.

        fileName:
            The name of the report file to be used for saving and exporting.
        """
    
        self.__clearReport()
        self.__exportFile = fileName
        self.__reportString = data
    
    def loadDocumentFile(self, filePath: str, load = False) -> None:
        """
        Loads a rendered report from a file or URL address.

        filePath:
            The path to the .mdc file or the URL of the rendered report.

        load:
            Loads a report file on the server side into report object.
        """

        self.__clearReport()
        path = StiPath(filePath)
        self.__exportFile = path.fileNameOnly

        if load: self.__documentString = self.__loadReportFile(path)
        else: self.__documentFile = filePath

    def loadDocument(self, data: str, fileName = 'Report') -> None:
        """
        Loads a rendered report from an XML or JSON string and send it as a packed string in Base64 format.

        data:
            Rendered report in XML or JSON format.

        fileName:
            The name of the report file to be used for saving and exporting.
        """
    
        self.__clearReport()
        self.__exportFile = fileName
        gzipBytes = gzip.compress(data.encode())
        self.__documentString = base64.b64encode(gzipBytes).decode()

    def loadPackedDocument(self, data: str, fileName = 'Report') -> None:
        """
        Loads a rendered report from a packed string in Base64 format.

        data:
            Rendered report as a packed string in Base64 format.

        fileName:
            The name of the report file to be used for saving and exporting.
        """
    
        self.__clearReport()
        self.__exportFile = fileName
        self.__documentString = data

    def saveDocument(self, filePath: str = None) -> str|bool:
        """
        Saves a rendered report in JSON format.

        filePath:
            The path to the .mdc file of the rendered report.

        return:
            The result of saving the report. If property 'filePath' not specified, the function will return JSON string of the report.
        """

        if len(self.__documentString or '') > 0:
            data = gzip.decompress(base64.b64decode(self.__documentString))
            return data.decode() if len(filePath or '') == 0 else self.__saveReportFile(filePath, 'mdc', data)
        
        return False

    def savePackedDocument(self, filePath: str = None) -> str|bool:
        """
        Saves a rendered report as packed string in Base64 format.

        filePath:
            The path to the .mdz file of the rendered report.

        return:
            The result of saving the report. If property 'filePath' not specified, the function will return Base64 string of the report.
        """

        if len(self.__documentString or '') > 0:
            if len(filePath or '') == 0:
                return self.__documentString
            
            data = base64.b64decode(self.__documentString)
            return self.__saveReportFile(filePath, 'mdz', data)
            
        return False
        

### Process

    def render(self) -> bool:
        """
        Builds a report, or prepares the necessary JavaScript to build the report.
        
        return:
            The result of building a report.
        """
    
        self.__renderCalled = True

        if self.engine == StiEngineType.SERVER_NODE_JS:
            afterRenderScript = self.__getAfterRenderNodeHtml()
            self.onAfterRender += afterRenderScript
            script = self.getHtml(StiHtmlMode.SCRIPTS)
            self.onAfterRender -= afterRenderScript
            self.__renderCalled = False
            
            result = self.nodejs.run(script)
            if not result:
                return False
            
            self.__documentString = result

        return True

    def print(self, pagesRange: StiPagesRange|str|int = None) -> None:
        """
        Prepares the necessary JavaScript to print the report. The browser print dialog will be called.
        
        pagesRande:
            The pages range or the page number to print.
        """
    
        self.__printCalled = True
        self.__pagesRange = pagesRange

    def exportDocument(self, format: StiExportFormat, settings: StiExportSettings = None, openAfterExport = False, filePath: str = None) -> bytes|bool:
        """
        Exports the rendered report to the specified format, or prepares the necessary JavaScript to export the report.

        Important! The export function does not automatically build the report template.

        format:
            [enum] Report export format.

        settings:
            Export settings, the type of settings must match the export format.
        
        openAfterExport:
            Automatically open the exported report in a browser window if the export is performed on the client side.

        filePath:
            The path to the file of the exported document. It only works with server-side Node.js mode.

        return:
            Byte data of the exported report, or the boolean result of the export.
        """
    
        self.__exportCalled = True
        self.__openAfterExport = openAfterExport
        self.__exportFormat = format

        self.__exportSettings = settings
        if settings != None:
            if isinstance(settings, StiHtmlExportSettings) and settings.htmlType == None:
                settings.setHtmlType(format)

            if isinstance(settings, StiDataExportSettings) and settings.dataType == None:
                settings.setDataType(format)

            if isinstance(settings, StiImageExportSettings) and settings.imageType == None:
                settings.setImageType(format)
                
            self.__exportFormat = settings.getExportFormat()

        if self.engine == StiEngineType.SERVER_NODE_JS:
            script = self.getHtml(StiHtmlMode.SCRIPTS)
            self.__exportCalled = False
            result = self.nodejs.run(script)
            
            if result and len(filePath or '') > 0:
                extension = StiExportFormat.getFileExtension(format)
                result = self.__saveReportFile(filePath, extension, result)
            
            return result
        
        return True
    

### Constructor

    def __init__(self):
        super().__init__()

        self.id = 'report'
        self.__dictionary = StiDictionary(self)
        self.handler = StiHandler()