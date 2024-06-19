#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

#========================================================================================================================================
"""EApiText

    EApiFile DESCRIPTION
    
"""
class EApiText(EObject):

    VERSION:str="664638a07251ff0d9e044b09a0fdfee7519352dc39de391dc833163d8b63e064"

    def __init__(self):
        super().__init__()
        
        self.header:str = None
        self.language:str = None
        self.text:str = None
        self.isComplete:bool = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteStr(self.header, stream)
        self._doWriteStr(self.language, stream)
        self._doWriteStr(self.text, stream)
        self._doWriteBool(self.isComplete, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.header = self._doReadStr(stream)
        self.language = self._doReadStr(stream)
        self.text = self._doReadStr(stream)
        self.isComplete = self._doReadBool(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\theader:{self.header}",
                f"\tlanguage:{self.language}",
                f"\ttext:{self.text}",
                f"\tisComplete:{self.isComplete}",
                            ]) 
        return strReturn