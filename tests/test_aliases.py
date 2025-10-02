import unittest
from rule_engine import RuleEngine

class TestAliases(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
        dsl = (
            "DEFINE ⊕ WITH a+b\n"
            "DEFINE ⊗ WITH a*b\n"
            "DEFINE ◇ WITH a-b\n"
            "DEFINE τ WITH 1 if (a-b)>=2 else 0\n"
            "DEFINE ♠ WITH (a+1)//3\n"
        )
        self.engine.load_rules_from_text(dsl)

    def test_oplus_aliases(self):
        for expr in ["3 +O 4", "3 O+ 4", "3 oplus 4", "3 OPLUS 4", "3 ⊕ 4"]:
            assert self.engine.evaluate_expression(expr) == 7

    def test_otimes_aliases(self):
        for expr in ["3 *O 4", "3 O* 4", "3 otimes 4", "3 OTIMES 4", "3 ⊗ 4"]:
            assert self.engine.evaluate_expression(expr) == 12

    def test_marge(self):
        for expr in ["7 mO 4", "7 ◇ 4"]:
            assert self.engine.evaluate_expression(expr) == 3

    def test_seuil(self):
        assert self.engine.evaluate_expression("7 tO 4") == 1
        assert self.engine.evaluate_expression("7 τ 4") == 1
        assert self.engine.evaluate_expression("5 τ 4") == 0

    def test_budget(self):
        for expr in ["8 sO 0", "8 ♠ 0"]:
            assert self.engine.evaluate_expression(expr) == 3

if __name__ == "__main__":
    unittest.main()
