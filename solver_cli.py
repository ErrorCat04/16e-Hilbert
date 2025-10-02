import sys
from rule_engine import RuleEngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python solver_cli.py \"<expression>\"")
        sys.exit(1)

    expr = sys.argv[1]

    # Préparer l’engin
    engine = RuleEngine()
    dsl = (
        "DEFINE ⊕ WITH (a-1)*(a-2)/2 + 1\n"
        "DEFINE ⊗ WITH 1 if b<=a else 0\n"
        "DEFINE ◇ WITH a-b\n"
        "DEFINE τ WITH 1 if (a-b)>=2 else 0\n"
        "DEFINE ♠ WITH (a+1)//3\n"
        "DEFINE ○ WITH 1\n"
        "DEFINE ⊂ WITH a+b\n"
        "DEFINE Δ WITH 'nested' if a<b else 'separated'\n"
        "DEFINE χ WITH a+b\n"
    )
    engine.load_rules_from_text(dsl)

    try:
        result = engine.evaluate_expression(expr)
        print(f"{expr} => {result}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    main()
    