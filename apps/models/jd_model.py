from typing import Dict, Any


class JDModel:
    '''
    Model for JD Object.
    '''

    def __init__(
        self,
        title: str,
        content: str,
        extraction: Dict[str, Any]
    ):
        self.title = title
        self.content = content
        self.extraction = extraction

    def to_dict(self) -> Dict[str, Any]:
        '''
        Convert the object to a dictionary.
        '''
        return {
            "title": self.title,
            "content": self.content,
            "extraction": self.extraction
        }
