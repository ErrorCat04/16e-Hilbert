import re, math
from typing import Callable, Dict

class EvaluationError(Exception):
    pass

class RuleEngine:
    """
    Maintains a registry of operations and applies them to simple binary expressions like '3 ⊕ 7'.
    Supports multi-law SELECT depending on orientation.
    Adds operator aliasing so Windows shells can use ASCII fallbacks like '+O' or '*O'.
    """
    def __init__(self, orientation: str = "+"):
        self.orientation = orientation
        self.ops: Dict[str, Dict] = {}
        self._law_globals = {
            "math": math,
            "__builtins__": {
                "abs": abs, "max": max, "min": min, "pow": pow,
                "round": round, "float": float, "int": int, "str": str
            }
        }
        self.aliases = {
            # === Partie A (Harnack/admissibilité/marge/seuil/budget) ===
            # Nouveaux alias (safe)
            "opo": "⊕",       # Harnack
            "oto": "⊗",       # admissibilité
            "mao": "◇",       # marge
            "tho": "τ",       # seuil (threshold)
            "buo": "♠",       # budget heuristique

            # Rétro-compat: anciens alias largement utilisés
            "+o": "⊕",
            "o+": "⊕",
            "oplus": "⊕",
            "oplUS".lower(): "⊕",   # par sécurité si des prompts mixtes passent

            "*o": "⊗",
            "o*": "⊗",
            "otimes": "⊗",
            "otimes".upper().lower(): "⊗",  # garde-fou

            "◇": "◇", "τ": "τ", "♠": "♠", "⊕": "⊕", "⊗": "⊗",

            # === Partie B (ovales/nids/distribution/complexité) ===
            # Nouveaux alias (safe)
            "ovo": "○",       # ovale
            "nio": "⊂",       # nid
            "dio": "Δ",       # distribution
            "coo": "χ",       # complexité

            # Rétro-compat: anciens alias des tests
            "oo": "○",        # oO
            "no": "⊂",        # nO
            "do": "Δ",        # dO
            "co": "χ",        # cO

            # Unicode self-maps
            "○": "○", "⊂": "⊂", "Δ": "Δ", "χ": "χ",
        
    }
        
                # Legacy aliases (to warn and still support)
        self._legacy_aliases = {
            "+O": "⊕", "O+": "⊕", "oplus": "⊕", "OPLUS": "⊕",
            "*O": "⊗", "O*": "⊗", "otimes": "⊗", "OTIMES": "⊗",
            "oO": "○", "nO": "⊂", "dO": "Δ", "cO": "χ",
        }

    # dans RuleEngine.__init__, après tes alias propres:
        self.aliases.update({
            # rétro-compat pour anciens scripts / providers
            "mO": "◇",   # ancien alias marge
            "tO": "τ",   # ancien alias seuil
            "sO": "♠",   # ancien alias budget
        })


    def _norm_op(self, op: str) -> str:
        token = op.strip()
        # unicode direct → OK
        if token in self.aliases:
            return self.aliases[token]
        # case-insensitive
        key = token.lower()
        if key in self.aliases:
            return self.aliases[key]
        # legacy support + warning
        if token in self._legacy_aliases:
            mapped = self._legacy_aliases[token]
            print(f"[warn] Legacy alias '{token}' → use the new ASCII alias instead "
                  f"(e.g. opO/otO/maO/thO/buO or ovO/niO/diO/coO). Mapping to '{mapped}'.")
            return mapped
        return token

    def load_rules_from_text(self, text: str):
        lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        for line in lines:
            if line.upper().startswith("DEFINE "):
                self._parse_define(line)
            elif line.upper().startswith("REPLACE "):
                self._parse_replace(line)
            elif line.upper().startswith("DELETE "):
                self._parse_delete(line)
            elif line.upper().startswith("ENABLE "):
                self._parse_enable(line, True)
            elif line.upper().startswith("DISABLE "):
                self._parse_enable(line, False)
            elif line.upper().startswith("SELECT "):
                self._parse_select(line)

    def _compile_law(self, expr: str):
        code = compile(expr, "<law>", "eval")
        def fn(a, b):
            return eval(code, self._law_globals, {"a": a, "b": b})
        return fn

    def _parse_define(self, line: str):
        m = re.match(r"DEFINE\s+(.+?)\s+WITH\s+(.+)$", line, flags=re.IGNORECASE)
        if not m: raise EvaluationError(f"Bad DEFINE: {line}")
        op_raw, law_expr = m.group(1).strip(), m.group(2).strip()
        op = self._norm_op(op_raw)
        self.ops[op] = {"enabled": True, "law": self._compile_law(law_expr)}

    def _parse_replace(self, line: str):
        m = re.match(r"REPLACE\s+(.+?)\s+WITH\s+(.+)$", line, flags=re.IGNORECASE)
        if not m: raise EvaluationError(f"Bad REPLACE: {line}")
        op_raw, law_expr = m.group(1).strip(), m.group(2).strip()
        op = self._norm_op(op_raw)
        if op not in self.ops: raise EvaluationError(f"Unknown op for REPLACE: {op_raw}")
        self.ops[op]["law"] = self._compile_law(law_expr)
        if "laws" in self.ops[op]:
            del self.ops[op]["laws"]

    def _parse_delete(self, line: str):
        m = re.match(r"DELETE\s+(.+)$", line, flags=re.IGNORECASE)
        if not m: raise EvaluationError(f"Bad DELETE: {line}")
        op_raw = m.group(1).strip()
        op = self._norm_op(op_raw)
        self.ops.pop(op, None)

    def _parse_enable(self, line: str, enable: bool):
        m = re.match(r"(EN|DIS)ABLE\s+(.+)$", line, flags=re.IGNORECASE)
        if not m: raise EvaluationError(f"Bad ENABLE/DISABLE: {line}")
        op_raw = m.group(2).strip()
        op = self._norm_op(op_raw)
        if op not in self.ops: raise EvaluationError(f"Unknown op: {op_raw}")
        self.ops[op]["enabled"] = enable

    def _parse_select(self, line: str):
        m = re.match(r"SELECT\s+(.+?)\s+WITH\s*\{\s*(.+?)\s*\}\s*USING\s*ORIENTATION\s*([+\-])$", line, flags=re.IGNORECASE)
        if not m: raise EvaluationError(f"Bad SELECT: {line}")
        op_raw = m.group(1).strip()
        laws_blob = m.group(2).strip()
        orientation = m.group(3).strip()
        op = self._norm_op(op_raw)
        laws = [x.strip() for x in laws_blob.split(";") if x.strip()]
        compiled = [self._compile_law(expr) for expr in laws]
        self.ops[op] = {"enabled": True, "laws": compiled, "selector_orientation": orientation}

    def evaluate_expression(self, expr: str):
        tokens = expr.strip().split()
        if len(tokens) != 3:
            raise EvaluationError("Expression must be 'a OP b' with spaces, e.g., '3 ⊕ 7' or '3 +O 7'")
        try:
            a = float(tokens[0]); b = float(tokens[2])
        except ValueError:
            raise EvaluationError("Operands must be numeric")

        op_token = tokens[1]
        op = self._norm_op(op_token)

        if op not in self.ops or not self.ops[op].get("enabled", False):
            raise EvaluationError(f"Operation '{op_token}' is not defined or disabled")

        spec = self.ops[op]
        if "law" in spec:
            return spec["law"](a, b)
        elif "laws" in spec:
            orient = spec.get("selector_orientation", self.orientation)
            idx = 0 if orient == "+" else -1
            return spec["laws"][idx](a, b)
        raise EvaluationError("Malformed operation spec")
