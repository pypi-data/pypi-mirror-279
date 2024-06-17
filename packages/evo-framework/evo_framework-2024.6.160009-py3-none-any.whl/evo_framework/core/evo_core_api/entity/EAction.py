#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation    https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EnumApiAction import EnumApiAction
#========================================================================================================================================
"""EAction

    EAction DESCRIPTION
    
"""
class EAction(EObject):

    VERSION:str="c4affdcf91dacfb167aef131fc1183f5c2143520387807b25806155dc24ae386"

    def __init__(self):
        super().__init__()
        
        self.enumApiAction:EnumApiAction = EnumApiAction.NONE
        self.action:str = None
        self.input:bytes = None
        self.output:bytes = None
        self.isError:bool = None
        self.error:str = None
  
    def toStream(self, stream):
        super().toStream(stream)
        
        self._doWriteInt(self.enumApiAction.value, stream)
        self._doWriteStr(self.action, stream)
        self._doWriteBytes(self.input, stream)
        self._doWriteBytes(self.output, stream)
        self._doWriteBool(self.isError, stream)
        self._doWriteStr(self.error, stream)
        
    def fromStream(self, stream):
        super().fromStream(stream)
        
        self.enumApiAction = EnumApiAction(self._doReadInt(stream))
        self.action = self._doReadStr(stream)
        self.input = self._doReadBytes(stream)
        self.output = self._doReadBytes(stream)
        self.isError = self._doReadBool(stream)
        self.error = self._doReadStr(stream)
    
    def __str__(self) -> str:
        strReturn = "\n".join([
                super().__str__(),
                            
                f"\tenumApiAction:{self.enumApiAction}",
                f"\taction:{self.action}",
                f"\tinput length:{len(self.input) if self.input else 'None'}",
                f"\toutput length:{len(self.output) if self.output else 'None'}",
                f"\tisError:{self.isError}",
                f"\terror:{self.error}",
                            ]) 
        return strReturn
#<
#----------------------------------------------------------------------------------------------------------------------------------------
#EXTENSION
#----------------------------------------------------------------------------------------------------------------------------------------
    def doSetInput(self, eObject:EObject):
        from evo_framework.core.evo_core_api.utility.IuApi import IuApi
        self.input = eObject.toBytes()
        self.doGenerateTime()
#----------------------------------------------------------------------------------------------------------------------------------------
    def doGetInput(self, EObjectClass:type) -> EObject:
        from evo_framework.core.evo_core_api.utility.IuApi import IuApi
        return IuApi.toEObject(EObjectClass(), self.input)     
#----------------------------------------------------------------------------------------------------------------------------------------
    def doSetOutput(self, eObject:EObject):
        from evo_framework.core.evo_core_api.utility.IuApi import IuApi
        self.output = eObject.toBytes()
        self.doGenerateTime()
#----------------------------------------------------------------------------------------------------------------------------------------
    def doGetOutput(self, EObjectClass:type) -> EObject:
        from evo_framework.core.evo_core_api.utility.IuApi import IuApi
        return IuApi.toEObject(EObjectClass(), self.output)     
#----------------------------------------------------------------------------------------------------------------------------------------
    def doSetError(self,error:str):
        self.isError = True
        self.error = error
        self.doGenerateTime()
#----------------------------------------------------------------------------------------------------------------------------------------
#>