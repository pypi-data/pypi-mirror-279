from datetime import datetime

from stimulsoft_data_adapters.classes.StiBaseHandler import StiBaseHandler
from stimulsoft_data_adapters.enums.StiDatabaseType import StiDatabaseType
from stimulsoft_data_adapters.events.StiEvent import StiEvent

from ..classes.StiComponent import StiComponent
from ..enums.StiEventType import StiEventType
from .StiRequest import StiRequest
from .StiResponse import StiResponse
from .StiResult import StiResult
from .StiFileResult import StiFileResult


class StiHandler(StiBaseHandler):
    """
    Event handler for all requests from components. Processes the incoming request, communicates with data adapters, 
    prepares parameters and triggers events, and performs all necessary actions. After this, the event handler 
    prepares a response for the web server.
    """


### Properties
    
    component: StiComponent = None
    request: StiRequest = None
    timeout = 30
    encryptData = True
    escapeQueryParameters = True
    passQueryParametersToReport = False
    

### Events

    onPrepareVariables: StiEvent = None
    """The event is invoked before rendering a report after preparing report variables. Python and JavaScript functions are supported."""


### Helpers

    def _createRequest(self):
        return StiRequest()
    
    def _checkEvent(self):
        return self.request.event.value in StiEventType.getValues()
    
    def _checkCommand(self):
        if self.request.event == StiEventType.BEGIN_PROCESS_DATA:
            return super()._checkCommand()
        
        return True
    
    def _updateEvents(self):
        super()._updateEvents()
        
        self._updateEvent('onPrepareVariables')


### Results

    def __getPrepareVariablesResult(self) -> StiResult:
        self._updateEvents()

        if len(self.onPrepareVariables) > 0:
            from ..events.StiVariablesEventArgs import StiVariablesEventArgs
            from ..report.enums.StiVariableType import StiVariableType
            
            args = StiVariablesEventArgs(self.request)
            self.onPrepareVariables(args)

            result: StiResult = StiResult.getSuccess()
            result.handlerVersion = self.version
            result.variables = list()
            for variableName in args.variables:
                variable = args.variables[variableName]
                variableChanged = True
                for variableOriginal in self.request.variables:
                    valueOriginal = variableOriginal['value']
                    if variableOriginal['name'] == variableName:
                        if variable.typeName[-5:] == 'Range' and type(variable.value) == dict:
                            value = variable.value
                            variableChanged = value.get('from') != valueOriginal.get('from') or value.get('to') != valueOriginal.get('to')
                        elif variable.typeName[-4:] == 'List' and type(variable.value) == list:
                            value = variable.value
                            variableChanged = len(value) != len(valueOriginal) or len(value) != sum([1 for i, j in zip(value, valueOriginal) if i == j])
                        else:
                            variableChanged = variableOriginal['value'] != variable.value
                        break
                if variableChanged:
                    if variable.type == StiVariableType.DATETIME and type(variable.value) == datetime:
                        variable.value = variable.value.strftime('%Y-%m-%d %H:%M:%S')
                    result.variables.append({ 'name': variable.name, 'type': variable.typeName, 'value': variable.value })
        else:
            result = StiResult.getError("The handler for the 'onPrepareVariables' event is not specified.")

        return result

    def getResponse(self) -> StiResponse:
        """
        Returns the result of processing a request from the client side. The response object will contain the data for the response, 
        as well as their MIME type, Content-Type, and other useful information to create a web server response.
        """

        return StiResponse(self)
    
    def getResult(self):
        """
        Returns the result of processing a request from the client side. The result object will contain a collection of data, 
        message about the result of the command execution, and other technical information.
        """

        if self.request.event == StiEventType.GET_RESOURCE:
            try:
                from stimulsoft_dashboards.resources.StiResourcesHelper import StiResourcesHelper
            except Exception as e:
                from ..resources.StiResourcesHelper import StiResourcesHelper
            
            result: StiFileResult = StiResourcesHelper.getResult(self.request.data)
            if result.success and self.request.data == 'stimulsoft.handler.js':
                result.data = self.__getJavaScript(result.data)
                result.handlerVersion = self.version

            return result
        
        if self.request.event == StiEventType.PREPARE_VARIABLES:
            return self.__getPrepareVariablesResult()
        
        if self.component != None:
            result = self.component.getEventResult()
            if result != None:
                result.handlerVersion = self.version
                return result
        
        return super().getResult()


### JavaScript

    def __getJavaScriptValue(self, value) -> str:
        if value == None: return ''
        if type(value) == list: return str(value)
        if type(value) == str: return f"'{value}'"
        return str(value).lower()

    def __getJavaScript(self, data: bytes) -> bytes:
        csrf_token = None
        script = data.decode()
        script = script.replace('{databases}', self.__getJavaScriptValue(StiDatabaseType.getValues()))
        script = script.replace('{csrf_token}', '' if csrf_token == None else csrf_token)
        script = script.replace('{url}', self.__getJavaScriptValue(self.url))
        script = script.replace('{timeout}', self.__getJavaScriptValue(self.timeout))
        script = script.replace('{encryptData}', self.__getJavaScriptValue(self.encryptData))
        script = script.replace('{passQueryParametersToReport}', self.__getJavaScriptValue(self.passQueryParametersToReport))
        script = script.replace('{checkDataAdaptersVersion}', self.__getJavaScriptValue(self.checkDataAdaptersVersion))
        script = script.replace('{escapeQueryParameters}', self.__getJavaScriptValue(self.escapeQueryParameters))
        return script.encode()


### Constructor

    def __init__(self, url: str = None, timeout = 30):
        super().__init__(url)
        
        self.timeout = timeout
