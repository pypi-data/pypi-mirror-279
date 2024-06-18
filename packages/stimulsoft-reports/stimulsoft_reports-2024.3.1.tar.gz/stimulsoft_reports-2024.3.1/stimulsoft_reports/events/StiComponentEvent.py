import re

from stimulsoft_data_adapters.events.StiEvent import StiEvent
from stimulsoft_data_adapters.events.StiEventArgs import StiEventArgs

from ..classes.StiComponent import StiComponent


class StiComponentEvent(StiEvent):
    
### Fields

    __component: StiComponent = None
    __htmlRendered: bool = False


### Properties

    @property
    def handler(self):
        return self.component.handler if self.component.handler != None else super().handler
    
    @property
    def component(self):
        return self.__component
    
    @property
    def htmlRendered(self) -> str:
        return self.__htmlRendered

    
### Helpers

    def _setArgs(self, *args, **keywargs) -> StiEventArgs:
        eventArgs = super()._setArgs(*args, **keywargs)
        if isinstance(eventArgs, StiEventArgs):
            eventArgs.sender = self.component

        return eventArgs


### HTML

    def getHtml(self, callback = False, prevent = False, process = True, internal = False) -> str:
        """Gets the HTML representation of the event."""

        if (len(self) == 0 or self.__htmlRendered):
            return ''
        
        eventValue = ''
        for callbackName in self.callbacks:
            if type(callbackName) == str: eventValue += \
                f'if (typeof {callbackName} === "function") {callbackName}(args); ' \
                if re.search("^[a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*$", callbackName) \
                else callbackName

        if internal:
            eventArgs = f'let args = {{event: "{self.name[2:]}", sender: "{self.component.componentType}", report: {self.component.id}}}'
            return f'{eventArgs}\n{eventValue}\n'
        
        callbackValue = ', callback' if callback else ''
        preventValue = 'args.preventDefault = true; ' if prevent else ''
        processValue = f'Stimulsoft.handler.process(args{callbackValue}); ' if process else ('callback(); ' if callback else '')
        result = f'{self.component.id}.{self.name} = function (args{callbackValue}) {{ {preventValue}{eventValue}{processValue} }}\n'
        
        self.__htmlRendered = True
        return result
    

### Constructor

    def __init__(self, component: StiComponent, name: str):
        super().__init__(component.handler, name)
        self.__component = component