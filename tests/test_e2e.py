import unittest
from rule_engine import RuleEngine

class TestHilbertEndToEnd(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()

    def test_partA(self):
        dsl = (
            "DEFINE ⊕ WITH ((a-1)*(a-2))/2 + 1\n"   # Harnack H(n)
            "DEFINE ⊗ WITH 1 if b<=a else 0\n"      # admissibilite
            "DEFINE ◇ WITH a-b\n"                   # marge
            "DEFINE τ WITH 1 if (a-b) >= 2 else 0\n"# seuil
            "DEFINE ♠ WITH math.floor((a+1)/3)\n"   # budget heuristique
        )
        self.engine.load_rules_from_text(dsl)

        # mêmes checks que ta CLI
        assert self.engine.evaluate_expression("6 opO 0")  == 11.0
        assert self.engine.evaluate_expression("11 otO 10") == 1
        assert self.engine.evaluate_expression("11 maO 12") == -1.0
        assert self.engine.evaluate_expression("22 thO 20") == 1
        assert self.engine.evaluate_expression("22 buO 0")  == 7

    def test_partB(self):
        self.engine = RuleEngine()  # reset propre
        dsl = (
            "DEFINE ○ WITH 1\n"
            "DEFINE ⊂ WITH a+b\n"
            "DEFINE Δ WITH 'nested' if a<b else 'separated'\n"
            "DEFINE χ WITH a+b\n"
        )
        self.engine.load_rules_from_text(dsl)

        assert self.engine.evaluate_expression("1 ovO 0") == 1
        assert self.engine.evaluate_expression("2 niO 3") == 5
        assert self.engine.evaluate_expression("2 diO 3") == "nested"
        assert self.engine.evaluate_expression("3 coO 5") == 8
