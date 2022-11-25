from clueai.response import ClueaiObject
from typing import List

class QAPair(ClueaiObject):
    def __init__(self, question: str, answer: str) -> None:
        self.question = question
        self.answer = answer

class QA(ClueaiObject):
    def __init__(self, doc: str, qa_pairs: List[QAPair]) -> None:
        self.doc = doc 
        self.qa_pairs = qa_pairs


class QAs(ClueaiObject):
    def __init__(self, qas: List[QA]) -> None:
        self.qas = qas
        self.iterator = iter(qas)

    def __iter__(self) -> iter:
        return self.iterator

    def __next__(self) -> next:
        return next(self.iterator)

    def __len__(self) -> int:
        return len(self.qas)
