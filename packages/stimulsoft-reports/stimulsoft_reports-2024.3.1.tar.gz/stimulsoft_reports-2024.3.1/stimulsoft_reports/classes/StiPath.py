import os

class StiPath:

### Fields

    filePath: str = None
    directoryPath: str = None
    fileName: str = None
    fileNameOnly: str = None
    fileExtension: str = None


### Helpers

    def __normalizePath(path: str) -> str:
        return os.path.normpath(path.split('?')[0]).strip('/\\')
    
    def __getMissingFileName(filePath: str) -> str:
        filePath = StiPath.__normalizePath(filePath)
        return os.path.basename(filePath)
    
    def __getRealFilePath(filePath: str) -> str:
        filePath = StiPath.__normalizePath(filePath)
        if os.path.isfile(filePath):
            return filePath

        filePath = os.path.join(os.getcwd(), filePath)
        if os.path.isfile(filePath):
            return filePath
        
        return None
    
    def __getRealDirectoryPath(directoryPath: str) -> str:
        filePath = StiPath.__normalizePath(directoryPath)
        
        directoryPath = filePath
        if os.path.isdir(directoryPath):
            return directoryPath

        directoryPath = os.path.join(os.getcwd(), directoryPath)
        if os.path.isdir(directoryPath):
            return directoryPath
        
        directoryPath = os.path.dirname(filePath)
        if os.path.isdir(directoryPath):
            return directoryPath

        directoryPath = os.path.join(os.getcwd(), directoryPath)
        if os.path.isdir(directoryPath):
            return directoryPath
        
        return None


### Constructor

    def __init__(self, filePath):
        self.filePath = StiPath.__getRealFilePath(filePath)
        self.directoryPath = StiPath.__getRealDirectoryPath(filePath)
        
        self.fileName = os.path.basename(self.filePath) if self.filePath != None else StiPath.__getMissingFileName(filePath)
        if self.filePath == None and (self.directoryPath or '').endswith(self.fileName):
            self.fileName = None

        if self.fileName != None:
            self.fileNameOnly, self.fileExtension = os.path.splitext(self.fileName)
            self.fileExtension = self.fileExtension[1:].lower() if len(self.fileExtension or '') > 1 else ''