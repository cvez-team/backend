from typing import Dict, Any


class QuestionModel:
    '''
    Model for Question Object.
    '''

    def __init__(
        self,
        title: str,
        content: str,
        answers: str,
        extraction: Dict[str, Any]
    ):
        self.title = title
        self.content = content
        self.answers = answers
        self.extraction = extraction

    def to_dict(self) -> Dict[str, Any]:
        '''
        Convert the object to a dictionary.
        '''
        return {
            "title": self.title,
            "content": self.content,
            "answers": self.answers,
            "extraction": self.extraction
        }
