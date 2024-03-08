from abc import abstractmethod
from typing import TypedDict, Literal, Dict, Optional, Any, Tuple, Union
from pydantic import Field


TypeLiteral = Literal["string", "integer",
                      "float", "boolean", "list", "dictionary"]


class LLMFmtItem(TypedDict):
    type: TypeLiteral
    description: Optional[str]
    items: Optional['LLMFmtItem']
    properties: Optional[Dict[str, 'LLMFmtItem']]


LLMFmt = Dict[str, LLMFmtItem]


PydanticFmt = Dict[str, Union[Tuple[type, Field], list]]


class LCEL:
    '''
    Abstract class for Language Chain Element (LCEL).
    '''
    @abstractmethod
    def invoke(data: Dict[str, Any]) -> Any:
        '''
        Invokes the model and returns the result.
        '''
