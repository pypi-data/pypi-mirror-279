#========================================================================================================================================
# CyborgAI CC BY-NC-ND 4.0 Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 Internation	https://github.com/cyborg-ai-git | 
#========================================================================================================================================

from evo_framework.entity.EObject import EObject
from evo_framework.core.evo_core_type.entity.EvoMap import EvoMap

from evo_framework.core.evo_core_api.entity.EnumApiCompress import EnumApiCompress
#========================================================================================================================================
"""EResponse

	EResponse DESCRIPTION
	
"""
class EResponse(EObject):

	VERSION:str="365c68d3636063fb2145211f197d427503ea8aab37608c832f01945165f82cbd"

	def __init__(self):
		super().__init__()
		
		self.enumApiCompress:EnumApiCompress = EnumApiCompress.LZ4
		self.sign:bytes = None
		self.hash:bytes = None
		self.chunk:int = None
		self.chunkTotal:int = None
		self.data:bytes = None
		self.isError:bool = None
		self.error:str = None
  
	def toStream(self, stream):
		super().toStream(stream)
		
		self._doWriteInt(self.enumApiCompress.value, stream)
		self._doWriteBytes(self.sign, stream)
		self._doWriteBytes(self.hash, stream)
		self._doWriteInt(self.chunk, stream)
		self._doWriteInt(self.chunkTotal, stream)
		self._doWriteBytes(self.data, stream)
		self._doWriteBool(self.isError, stream)
		self._doWriteStr(self.error, stream)
		
	def fromStream(self, stream):
		super().fromStream(stream)
		
		self.enumApiCompress = EnumApiCompress(self._doReadInt(stream))
		self.sign = self._doReadBytes(stream)
		self.hash = self._doReadBytes(stream)
		self.chunk = self._doReadInt(stream)
		self.chunkTotal = self._doReadInt(stream)
		self.data = self._doReadBytes(stream)
		self.isError = self._doReadBool(stream)
		self.error = self._doReadStr(stream)
	
	def __str__(self) -> str:
		strReturn = "\n".join([
				super().__str__(),
							
				f"\tenumApiCompress:{self.enumApiCompress}",
				f"\tsign length:{len(self.sign) if self.sign else 'None'}",
				f"\thash length:{len(self.hash) if self.hash else 'None'}",
				f"\tchunk:{self.chunk}",
				f"\tchunkTotal:{self.chunkTotal}",
				f"\tdata length:{len(self.data) if self.data else 'None'}",
				f"\tisError:{self.isError}",
				f"\terror:{self.error}",
							]) 
		return strReturn
	