from typing import Dict, Any


class CVModel:
    '''
    Model for CV Object.
    '''

    def __init__(
        self,
        name: str,
        path: str,
        url: str,
        extraction: Dict[str, Any]
    ):
        self.name = name
        self.path = path
        self.url = url
        self.extraction = extraction

    def to_dict(self) -> Dict[str, Any]:
        '''
        Convert the object to a dictionary.
        '''
        return {
            "name": self.name,
            "path": self.path,
            "url": self.url,
            "extraction": self.extraction
        }
