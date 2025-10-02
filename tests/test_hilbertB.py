import unittest
from rule_engine import RuleEngine

class TestHilbertB(unittest.TestCase):
    def setUp(self):
        self.engine = RuleEngine()
        dsl = (
            "DEFINE ○ WITH 1\n"
            "DEFINE ⊂ WITH a+b\n"
            "DEFINE Δ WITH 'nested' if a<b else 'separated'\n"
            "DEFINE χ WITH a+b\n"
        )
        self.engine.load_rules_from_text(dsl)

    def test_ovale(self):
        assert self.engine.evaluate_expression("1 oO 0") == 1
        assert self.engine.evaluate_expression("1 ○ 0") == 1

    def test_nid(self):
        assert self.engine.evaluate_expression("1 nO 1") == 2
        assert self.engine.evaluate_expression("1 ⊂ 2") == 3

    def test_distribution(self):
        assert self.engine.evaluate_expression("2 dO 3") == "nested"
        assert self.engine.evaluate_expression("3 dO 2") == "separated"

    def test_complexite(self):
        assert self.engine.evaluate_expression("3 cO 5") == 8
