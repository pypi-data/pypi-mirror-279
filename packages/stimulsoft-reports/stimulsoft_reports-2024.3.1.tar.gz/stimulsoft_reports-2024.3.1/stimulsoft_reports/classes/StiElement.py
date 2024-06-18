class StiElement:

### Fields

    __htmlRendered = False


### Properties
    
    id: str = None
    """Gets or sets the component or element ID that will be used for the name of the object when preparing JavaScript code."""

    @property
    def htmlRendered(self) -> str:
        return self.__htmlRendered


### HTML

    def getHtml(self) -> str:
        """
        Gets the HTML representation of the element.
        
        return:
            Prepared HTML and JavaScript code for embedding in an HTML template.
        """

        self.__htmlRendered = True
        return ''
    