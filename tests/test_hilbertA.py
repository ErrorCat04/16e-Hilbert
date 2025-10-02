import unittest
from rule_engine import RuleEngine

class TestHilbertA(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
        dsl = (
            "DEFINE ⊕ WITH ((a-1)*(a-2))/2 + 1\n"  # H(n)
            "DEFINE ⊗ WITH 1 if b<=a else 0\n"     # admissible ?
            "DEFINE ◇ WITH a-b\n"                  # marge = H-k
            "DEFINE τ WITH 1 if (a-b) >= 2 else 0\n"  # seuil (>=2)
            "DEFINE ♠ WITH math.floor((a+1)/3)\n"  # budget nids (heuristique)
        )
        self.engine.load_rules_from_text(dsl)

    def test_harnack_values(self):
        assert self.engine.evaluate_expression("6 ⊕ 6") == 11
        assert self.engine.evaluate_expression("8 ⊕ 8") == 22

    def test_admissibilite(self):
        assert self.engine.evaluate_expression("11 ⊗ 10") == 1
        assert self.engine.evaluate_expression("11 ⊗ 12") == 0

    def test_marge(self):
        assert self.engine.evaluate_expression("11 ◇ 10") == 1
        assert self.engine.evaluate_expression("11 ◇ 12") == -1

    def test_seuil(self):
        assert self.engine.evaluate_expression("22 τ 20") == 1  # marge 2 -> OK
        assert self.engine.evaluate_expression("22 τ 21") == 0  # marge 1 -> KO

    def test_budget(self):
        assert self.engine.evaluate_expression("22 ♠ 0") == 7
        assert self.engine.evaluate_expression("11 ♠ 0") == 4


    def test_harnack_values(self):
        res6 = self.engine.evaluate_expression("6 ⊕ 6")
        res8 = self.engine.evaluate_expression("8 ⊕ 8")
        print("H(6) =", res6)
        print("H(8) =", res8)
        assert res6 == 11
        assert res8 == 22

    def test_harnack_values(self):
        res6 = self.engine.evaluate_expression("6 ⊕ 6")
        res8 = self.engine.evaluate_expression("8 ⊕ 8")
        print("H(6) =", res6)
        print("H(8) =", res8)
        assert res6 == 11
        assert res8 == 22

if __name__ == "__main__":
    unittest.main()
