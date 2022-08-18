from clueai.response import ClueaiObject
from typing import List


class TokenLikelihood(ClueaiObject):
    def __init__(self, token: str, likelihood: float) -> None:
        self.token = token
        self.likelihood = likelihood


class Generation(ClueaiObject):
    def __init__(self,
                 promot: str,
                 text: str,
                 likelihood: float,
                 token_likelihoods: TokenLikelihood) -> None:
        self.promot = promot
        self.text = text
        self.likelihood = likelihood
        self.token_likelihoods = token_likelihoods


class Generations(ClueaiObject):
    def __init__(self,
                 generations: List[Generation],
                 return_likelihoods: str) -> None:
        self.generations = generations
        self.return_likelihoods = return_likelihoods
        self.iterator = iter(generations)

    def __iter__(self) -> iter:
        return self.iterator

    def __next__(self) -> next:
        return next(self.iterator)
