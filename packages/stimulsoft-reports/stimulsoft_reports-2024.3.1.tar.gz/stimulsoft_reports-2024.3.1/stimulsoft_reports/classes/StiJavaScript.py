from __future__ import annotations

import typing

from ..classes.StiElement import StiElement
from ..enums.StiComponentType import StiComponentType

if typing.TYPE_CHECKING:
    from .StiComponent import StiComponent


class StiJavaScript(StiElement):

### Private

    __component: StiComponent = None


### Options

    usePacked = False
    reportsSet = True
    reportsChart = True
    reportsExport = True
    reportsImportXlsx = True
    reportsMaps = True
    blocklyEditor = True
    

### Private

    def __isDashboardsProduct(self) -> bool:
        try:
            from stimulsoft_dashboards.report.StiDashboard import StiDashboard
        except Exception as e:
            return False
        
        return True


### Public

    def getHtml(self) -> str:
        """
        Gets the HTML representation of the component.
        
        return:
            Prepared JavaScript code for embedding in an HTML template in the HEAD section.
        """
        
        extension = 'pack.js' if (self.usePacked) else 'js'
        scripts: list = []
        if self.reportsSet:
            scripts.append(f'stimulsoft.reports.{extension}')
        else:
            scripts.append(f'stimulsoft.reports.engine.{extension}')
            if self.reportsChart:
                scripts.append(f'stimulsoft.reports.chart.{extension}')
            if self.reportsExport:
                scripts.append(f'stimulsoft.reports.export.{extension}')
            if self.reportsMaps:
                scripts.append(f'stimulsoft.reports.maps.{extension}')
            if self.reportsImportXlsx:
                scripts.append(f'stimulsoft.reports.import.xlsx.{extension}')

        if self.__isDashboardsProduct():
            scripts.append(f'stimulsoft.dashboards.{extension}')

        if self.__component.componentType == StiComponentType.VIEWER or self.__component.componentType == StiComponentType.DESIGNER:
            scripts.append(f'stimulsoft.viewer.{extension}')

        if self.__component.componentType == StiComponentType.DESIGNER:
            scripts.append(f'stimulsoft.designer.{extension}')

            if self.blocklyEditor:
                scripts.append(f'stimulsoft.blockly.editor.{extension}')

        scripts.append('stimulsoft.handler.js')

        url = self.__component.handler.url
        separator = '?' if url.find('?') < 0 else '&'
        result = '\n'.join([f'<script src="{url}{separator}sti_event=GetResource&sti_data={name}" type="text/javascript"></script>' for name in scripts])
        
        return result + super().getHtml()
    

### Constructor

    def __init__(self, component: StiComponent):
        self.__component = component
