from .base import RuleProvider
import math

class MockProvider(RuleProvider):
    def solve(self, problem_prompt: str):
        pp = problem_prompt.lower()

        # --------- Partie A : Harnack / admissibilité / marge / seuil / budget ---------
        if ("harnack" in pp) or ("admissibilit" in pp) or ("part a" in pp) or ("partie a" in pp):
            dsl = (
                "DEFINE ⊕ WITH ((a-1)*(a-2))/2 + 1\n"        # H(n)
                "DEFINE ⊗ WITH 1 if b<=a else 0\n"           # admissible ?
                "DEFINE ◇ WITH a-b\n"                        # marge = H-k
                "DEFINE τ WITH 1 if (a-b) >= 2 else 0\n"     # seuil (>=2)
                "DEFINE ♠ WITH math.floor((a+1)/3)\n"        # budget nids heuristique
            )
            return {
                "dsl": dsl,
                "evals": [
                    "6 ⊕ 6",
                    "8 ⊕ 8",
                    "11 ⊗ 10",
                    "11 ⊗ 12",
                    "11 maO 10",   # nouveaux alias (marge)
                    "11 maO 12",
                    "22 thO 20",   # (threshold)
                    "22 buO 0"     # (budget)
                ],
                "final": "Hilbert A: H(n), admissibilité, marge, seuil>=2, budget ≈ floor((H+1)/3)."
            }

        # --------- Partie B : ovale / nids / distribution / complexité ---------
        if ("part b" in pp) or ("partie b" in pp) or ("oval" in pp) or ("distribution" in pp):
            dsl = (
                "DEFINE ○ WITH 1\n"                                     # un ovale
                "DEFINE ⊂ WITH a+b\n"                                   # nid (somme)
                "DEFINE Δ WITH 'nested' if a<b else 'separated'\n"      # distribution
                "DEFINE χ WITH a+b\n"                                   # complexité
            )
            return {
                "dsl": dsl,
                "evals": [
                    "1 ovO 0",
                    "2 niO 3",
                    "2 diO 3",
                    "3 coO 5"
                ],
                "final": "Hilbert B: opérateurs de structure (ovale, nid, distribution, complexité)."
            }

        # --------- Fallback minimal ---------
        dsl = "DEFINE ⊕ WITH (a+b)/2\nDEFINE ⊗ WITH a*b\n"
        return {
            "dsl": dsl,
            "evals": ["3 ⊕ 7"],
            "final": "Règles par défaut."
        }
