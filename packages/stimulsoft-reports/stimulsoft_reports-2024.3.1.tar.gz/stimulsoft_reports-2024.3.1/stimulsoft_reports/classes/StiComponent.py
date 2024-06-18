from __future__ import annotations

import typing

from stimulsoft_data_adapters.events.StiEvent import StiEvent
from stimulsoft_data_adapters.events.StiEventArgs import StiEventArgs

from ..classes.StiElement import StiElement
from ..classes.StiFileResult import StiFileResult
from ..classes.StiJavaScript import StiJavaScript
from ..classes.StiLicense import StiLicense
from ..classes.StiRequest import StiRequest
from ..classes.StiResponse import StiResponse
from ..classes.StiResult import StiResult
from ..enums.StiComponentType import StiComponentType
from ..enums.StiDataType import StiDataType
from ..enums.StiHtmlMode import StiHtmlMode

if typing.TYPE_CHECKING:
    from .StiHandler import StiHandler


class StiComponent(StiElement):

### Fields
    
    __handler: StiHandler = None
    __processRequestResult: bool = None
    __javascript: StiJavaScript = None
    __license: StiLicense = None


### Properties

    @property
    def componentType(self) -> StiComponentType:
        return None

    @property
    def handler(self) -> StiHandler:
        """
        Gets or sets an event handler that controls data passed from client to server and from server to client.
        Contains the necessary options for sending data.
        """
        
        return self.__handler
    
    @handler.setter
    def handler(self, value: StiHandler):
        if value != None:
            self.__handler = value

    @property
    def request(self) -> StiRequest:
        return self.handler.request if self.handler != None else None

    @property
    def javascript(self) -> StiJavaScript:
        """Gets a JavaScript manager that controls the deployment of JavaScript code necessary for components to work."""

        return self.__javascript
    
    @property
    def license(self) -> StiLicense:
        """Gets a license manager that allows you to load a license key in various formats."""

        return self.__license
    
    @license.setter
    def license(self, value: StiLicense):
        self.__license = value


### Events
    
    def _getDefaultEventResult(self, event: StiEvent, args: StiEventArgs) -> StiResult | None:
        if len(event) > 0:
            result = event(args)
            if result == None or result == True:
                return StiResult.getSuccess()
            if result == False:
                return StiResult.getError(f'An error occurred while processing the {self.request.event} event.')
            if isinstance(result, StiResult):
                return result
            return StiResult.getSuccess(str(result))
        
        return None
    
    def _updateEvents(self):
        pass

    def _updateEvent(self, eventName: str):
        event = getattr(self, eventName)
        from ..events.StiComponentEvent import StiComponentEvent
        if not isinstance(event, StiComponentEvent):
            callback = event if callable(event) or isinstance(event, (str, bool)) else None
            event = StiComponentEvent(self, eventName)
            if callback != None: event.append(callback)
            setattr(self, eventName, event)
    
    def getEventResult(self) -> StiResult:
        return None


### Request

    def processRequest(self, request: object = None, query: dict | str = None, body: bytes | str = None) -> bool:
        """
        Processing an HTTP request from the client side of the component. If successful, it is necessary to return a response 
        with the processing result, which can be obtained using the 'getResponse()' or 'getFrameworkResponse()' functions.
        
        request
            A request object for one of the supported frameworks.

        query:
            The GET query string if no framework request is specified.
        
        body:
            The POST form data if no framework request is specified.

        return:
            True if the request was processed successfully.
        """

        self.__processRequestResult = self.handler.processRequest(request, query, body)
        return self.__processRequestResult
    
    def getResponse(self) -> StiResponse:
        """
        Returns the result of processing a request from the client side. The response object will contain the data for the response, 
        as well as their MIME type, Content-Type, and other useful information to create a web server response.
        """

        if self.__processRequestResult == False:
            html = self.getHtml(StiHtmlMode.HTML_PAGE)
            result = StiFileResult(html, StiDataType.HTML)
            return StiResponse(self.handler, result)

        self.__processRequestResult = None
        return self.handler.getResponse()
    
    def getFrameworkResponse(self, handler = None) -> object:
        """Returns the result of processing a request from the client side intended for one of the supported frameworks."""
        
        return self.getResponse().getFrameworkResponse(handler)


### HTML

    def _getComponentHtml(self) -> str:
        return ''

    def getHtml(self, mode = StiHtmlMode.HTML_SCRIPTS) -> str:
        """
        Gets the HTML representation of the component.
        
        mode:
            HTML code generation mode.
        
        return:
            Prepared HTML and JavaScript code for embedding in an HTML template.
        """

        self._updateEvents()
        result = ''

        if mode == StiHtmlMode.HTML_PAGE:
            result += '<!DOCTYPE html>\n<html>\n<head>\n'
            result += self.javascript.getHtml()
            result += '</head>\n<body onload="start()">\n'

        if mode == StiHtmlMode.HTML_SCRIPTS or mode == StiHtmlMode.HTML_PAGE:
            if self.componentType == StiComponentType.VIEWER or self.componentType == StiComponentType.DESIGNER:
                result += f'<div id="{self.id}Content"></div>\n'

            result += '<script type="text/javascript">\n'

        if mode == StiHtmlMode.HTML_PAGE:
            result += 'function start() {\n'

        result += self._getComponentHtml()

        if mode == StiHtmlMode.HTML_PAGE:
            result += '}\n'

        if mode == StiHtmlMode.HTML_SCRIPTS or mode == StiHtmlMode.HTML_PAGE:
            result += '</script>\n'

        if mode == StiHtmlMode.HTML_PAGE:
            result += '</body>\n</html>'

        return result + super().getHtml()
    
    
### Constructor

    def __init__(self):
        self._updateEvents()

        self.__javascript = StiJavaScript(self)
        self.__license = StiLicense()