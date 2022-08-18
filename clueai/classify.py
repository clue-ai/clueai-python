from clueai.response import ClueaiObject
from typing import List


class Confidence(ClueaiObject):
    def __init__(self, label: str, confidence: float) -> None:
        self.label = label
        self.confidence = confidence


class Classification(ClueaiObject):
    def __init__(self, input: str,
                 prediction: str, confidence: Confidence) -> None:
        self.input = input
        self.prediction = prediction
        self.confidence = confidence


class Classifications(ClueaiObject):
    def __init__(self, classifications: List[Classification]) -> None:
        self.classifications = classifications
        self.iterator = iter(classifications)

    def __iter__(self) -> iter:
        return self.iterator

    def __next__(self) -> next:
        return next(self.iterator)

    def __len__(self) -> int:
        return len(self.classifications)


class Example(ClueaiObject):
    def __init__(self, text: str, label: str) -> None:
        self.text = text
        self.label = label
