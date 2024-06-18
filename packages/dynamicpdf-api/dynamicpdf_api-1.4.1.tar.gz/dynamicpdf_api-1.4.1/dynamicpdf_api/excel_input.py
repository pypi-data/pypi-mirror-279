from .input_type import InputType
from .page_size import PageSize
from .page_orientation import PageOrientation
from .converter_input import ConverterInput

class ExcelInput(ConverterInput):
    '''
    Represents a Excel input.
    '''

    def __init__(self, resource, size = None, orientation = None, margins = None):
        '''
        Initializes a new instance of the ExcelInput class.

        Args:
            resource (ExcelResource): The resource of type ExcelResource.
            size (PageSize): The page size of the output PDF.
            orientation (PageOrientation): The page orientation of the output PDF.
            margins (float): The page margins of the output PDF.
        '''
        
        super().__init__(resource, size, orientation, margins)
       
        self._type = InputType.Excel

    def to_json(self):
        json = {
            "id":self.id,
            "resourceName": self.resource_name,
            "templateId": self._template_id,
            "type": self._type,
            "pageWidth": self.page_width,
            "pageHeight": self.page_height,
        }
        if self.top_margin:
            json["topMargin"] = self.top_margin
        if self.left_margin:
            json["leftMargin"] = self.left_margin
        if self.bottom_margin:
            json["bottomMargin"] = self.bottom_margin
        if self.right_margin:
            json["rightMargin"] = self.right_margin
        return json