from typing import Dict, Any


class QuestionModel:
    '''
    Model for Question Object.
    '''

    def __init__(
        self,
        title: str,
        content: str,
        answer: str,
        extraction: Dict[str, Any]
    ):
        self.title = title
        self.content = content
        self.answer = answer
        self.extraction = extraction

    def to_dict(self) -> Dict[str, Any]:
        '''
        Convert the object to a dictionary.
        '''
        return {
            "title": self.title,
            "content": self.content,
            "answer": self.answer,
            "extraction": self.extraction
        }
