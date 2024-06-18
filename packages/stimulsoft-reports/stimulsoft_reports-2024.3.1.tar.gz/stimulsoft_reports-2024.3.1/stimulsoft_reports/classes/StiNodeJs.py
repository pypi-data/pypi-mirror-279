from __future__ import annotations

import base64
import json
import os
import platform
import shutil
import subprocess
import typing
import urllib.request
from array import array

from stimulsoft_data_adapters.enums.StiDatabaseType import StiDatabaseType

from ..resources.StiResourcesHelper import StiResourcesHelper
from .StiFileResult import StiFileResult
from .StiHandler import StiHandler

if typing.TYPE_CHECKING:
    from .StiComponent import StiComponent


class StiNodeJs:

### Fields

    __component: StiComponent = None
    __error: str = None
    __errorStack: list = None

    @property
    def __handler(self) -> StiHandler:
        return self.__component.handler if self.__component else StiHandler()


### Options

    version = '20.12.2'
    architecture = 'x64'
    system = ''
    binDirectory = ''
    workingDirectory = ''


### Properties

    @property
    def error(self) -> str:
        """Main text of the last error."""

        return self.__error
    
    @property
    def errorStack(self) -> array:
        """Full text of the last error as an array of strings."""

        return self.__errorStack


### Parameters

    def __getSystem(self) -> str:
        systemName = platform.system()
        if systemName == 'Windows': return 'win'
        if systemName == 'Darwin': return 'darwin'
        return 'linux'
            
    def __getArchiveName(self) -> str:
        extension = '.zip' if self.system == 'win' else '.tar.gz'
        return self.__getDirectoryName() + extension
    
    def __getDirectoryName(self) -> str:
        return f'node-v{self.version}-{self.system}-{self.architecture}'
    
    def __getDirectory(self) -> str:
        return os.path.join(os.getcwd(), self.__getDirectoryName())
    
    def __getUrl(self) -> str:
        return f'https://nodejs.org/dist/v{self.version}/' + self.__getArchiveName()
    
    def __getVersion(self) -> str:
        return self.__handler.version


### Helpers

    def __isDashboardsProduct(self) -> bool:
        try:
            from stimulsoft_dashboards.report.StiDashboard import StiDashboard
        except Exception as e:
            return False
        return True
    
    def __clearError(self):
        self.__error = None
        self.__errorStack = None

    def __getNodeError(self, stderr: str) -> str:
        lines = (stderr or '').split('\n')
        npmError = False
        errors = ['npm ERR', 'Error', 'SyntaxError', 'ReferenceError', 'TypeError', 'RequestError']
        for line in lines:
            if len(line or '') > 0:
                for error in errors:
                    if line.startswith(error):
                        if line.startswith('npm') and not npmError:
                            npmError = True
                            continue
                        return line
        return None
    
    def __getNodeErrorStack(self, stderr: str) -> list:
        return None if len(stderr or '') == 0 else stderr.split('\n')
    
    def __getNodePath(self) -> str:
        if len(self.binDirectory or '') == 0:
            return None
        
        nodePath = os.path.join(self.binDirectory, 'node.exe') if self.system == 'win' else os.path.join(self.binDirectory, 'bin', 'node')
        return nodePath if os.path.isfile(nodePath) else None
    
    def __getNpmPath(self) -> str:
        nodePath = self.__getNodePath()
        if len(nodePath or '') == 0:
            return None
        
        npmPath = nodePath[:-8] + 'npm.cmd' if self.system == 'win' else nodePath[:-4] + 'npm'
        return npmPath if os.path.isfile(npmPath) else None
    
    def __download(self) -> bool:
        url = self.__getUrl()
        archivePath = os.path.join(self.binDirectory, self.__getArchiveName())

        try:
            if not os.path.isdir(self.binDirectory):
                os.mkdir(self.binDirectory)

            urllib.request.urlretrieve(url, archivePath)
        except Exception as e:
            self.__error = str(e)
            return False
        
        return True
    
    def __unpack(self) -> bool:
        archivePath = os.path.join(self.binDirectory, self.__getArchiveName())
        try:
            shutil.unpack_archive(archivePath, self.binDirectory)
        except Exception as e:
            self.__error = str(e)
            return False

        sourcesPath = os.path.join(self.binDirectory, self.__getDirectoryName())
        for sourceFile in os.listdir(sourcesPath):
            shutil.move(os.path.join(sourcesPath, sourceFile), self.binDirectory)
        
        os.rmdir(sourcesPath)
        os.remove(archivePath)
        
        return True
    
    def __getJavaScriptValue(self, value) -> str:
        if value == None: return ''
        if type(value) == list: return str(value)
        if type(value) == str: return f"'{value}'"
        return str(value).lower()
    
    def __getHandlerScript(self) -> str:
        scriptResult: StiFileResult = StiResourcesHelper.getResult('stimulsoft.handler.js')
        script = scriptResult.data.decode()
        script = script.replace('{databases}', str(StiDatabaseType.getValues()))
        script = script.replace('{csrf_token}', '')
        script = script.replace('{url}', self.__getJavaScriptValue(self.__handler.url))
        script = script.replace('{timeout}', self.__getJavaScriptValue(self.__handler.timeout))
        script = script.replace('{encryptData}', self.__getJavaScriptValue(self.__handler.encryptData))
        script = script.replace('{passQueryParametersToReport}', self.__getJavaScriptValue(self.__handler.passQueryParametersToReport))
        script = script.replace('{checkDataAdaptersVersion}', self.__getJavaScriptValue(self.__handler.checkDataAdaptersVersion))
        script = script.replace('{escapeQueryParameters}', self.__getJavaScriptValue(self.__handler.escapeQueryParameters))
        script = script.replace('Stimulsoft.handler.send', 'Stimulsoft.handler.https')
        return script


### Methods

    def installNodeJS(self) -> bool:
        """
        Installs the version of Node.js specified in the parameters into the working directory from the official website.
        
        return:
            Boolean execution result.
        """

        self.__clearError()
        if self.__getNodePath() == None:
            if not self.__download(): return False
            if not self.__unpack(): return False
        return True

    def updatePackages(self) -> bool:
        """
        Updates product packages to the current version.
        
        return:
            Boolean execution result.
        """

        self.__clearError()
        npmPath = self.__getNpmPath()
        product = 'dashboards' if self.__isDashboardsProduct() else 'reports'
        version = self.__getVersion()
        result = subprocess.run([npmPath, 'install', f'stimulsoft-{product}-js@{version}'], cwd=self.workingDirectory, capture_output=True, text=True, shell=True)
        self.__error = self.__getNodeError(result.stderr)
        self.__errorStack = self.__getNodeErrorStack(result.stderr)
        return len(self.error or '') == 0

    def run(self, script) -> bytes|str|bool:
        """
        Executes server-side script using Node.js
        
        script:
            JavaScript prepared for execution in Node.js

        return:
            Depending on the script, it returns a byte stream or string data or a bool result.
        """

        self.__clearError()
        nodePath = self.__getNodePath()
        product = 'dashboards' if self.__isDashboardsProduct() else 'reports'
        require = f"var Stimulsoft = require('stimulsoft-{product}-js');\n"
        handler = self.__getHandlerScript()
        result = subprocess.run(nodePath, cwd=self.workingDirectory, input=require+handler+script, capture_output=True, text=True, shell=True)
        self.__error = self.__getNodeError(result.stderr) or self.__getNodeError(result.stdout)
        self.__errorStack = self.__getNodeErrorStack(result.stderr)
        if len(self.error or '') > 0:
            return False

        if len(result.stdout or '') > 0:
            try:
                jsonData = json.loads(result.stdout)
                if jsonData['type'] == 'string': return jsonData['data']
                if jsonData['type'] == 'bytes': return base64.b64decode(jsonData['data'])
            except Exception as e:
                self.__error = 'ParseError: ' + str(e)
                return False
        
        return True


### Constructor

    def __init__(self, component: StiComponent = None):
        self.__component = component
        self.system = self.__getSystem()
        self.binDirectory = self.__getDirectory()
        self.workingDirectory = os.getcwd()