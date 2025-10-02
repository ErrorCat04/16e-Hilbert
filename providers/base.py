from abc import ABC, abstractmethod

class RuleProvider(ABC):
    @abstractmethod
    def solve(self, problem_prompt: str):
        """
        Retourne un dict:
        {
          "dsl": "<bloc DSL>",
          "evals": ["3 ⊕ 7", ...],
          "final": "texte explicatif"
        }
        ou une simple chaîne DSL.
        """
        raise NotImplementedError
