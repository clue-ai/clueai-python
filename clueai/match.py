from clueai.response import ClueaiObject
from typing import List


class Score(ClueaiObject):
    def __init__(self, doc: str, confidence: float) -> None:
        self.doc = doc 
        self.confidence = confidence


class Match(ClueaiObject):
    def __init__(self, query: str,
                 best_doc: str, score: Score) -> None:
        self.query = query
        self.best_doc = best_doc
        self.score = score 


class Matches(ClueaiObject):
    def __init__(self, matches: List[Match]) -> None:
        self.matches = matches
        self.iterator = iter(matches)

    def __iter__(self) -> iter:
        return self.iterator

    def __next__(self) -> next:
        return next(self.iterator)

    def __len__(self) -> int:
        return len(self.matches)
