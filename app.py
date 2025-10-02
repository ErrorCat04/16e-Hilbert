import argparse, json, sys, re
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from rule_engine import RuleEngine, EvaluationError
from providers.mock_provider import MockProvider
from providers.ollama_provider import OllamaProvider
from providers.openrouter_provider import OpenRouterProvider


# --- plotting Hilbert B ---
def visualize_hilbertB():
    """
    Illustration simple de Hilbert B : ovales imbriqués et séparés.
    """
    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_aspect("equal")
    ax.set_title("Hilbert B – Ovale, Nids et Distributions")

    # Exemple de nid imbriqué
    ax.add_patch(Circle((0,0), 1, fill=False, color="blue", lw=2))
    ax.add_patch(Circle((0,0), 0.8, fill=False, color="red", lw=2))
    ax.add_patch(Circle((0,0), 0.6, fill=False, color="green", lw=2))

    # Exemple de nids disjoints
    ax.add_patch(Circle((-0.6,-0.6), 0.3, fill=False, color="purple", lw=2))
    ax.add_patch(Circle((0.6,0.6), 0.4, fill=False, color="orange", lw=2))

    ax.set_xlim(-1.5,1.5)
    ax.set_ylim(-1.5,1.5)
    plt.show()



# ---------- Sanitizer utils ----------
def _extract_inner_json(text: str) -> str:
    """Retourne le JSON pur { ... } depuis un texte avec blabla / ```json ... ``` / etc."""
    try:
        json.loads(text)
        return text
    except Exception:
        pass
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, flags=re.S|re.I)
    if m:
        return m.group(1)
    m = re.search(r"(\{.*\})", text, flags=re.S)
    return m.group(1) if m else text

def sanitize_payload(payload):
    """
    - Si provider renvoie une string -> extraire le JSON pur.
    - Garante: dsl=str, evals=list[str], final=str.
    - Si dsl est une liste/objet -> convertir en lignes 'DEFINE ... WITH ...'.
    - Si dsl est une string MAIS contient un JSON entre ```...``` -> on l’extrait et on reconstruit.
    """
    if isinstance(payload, str):
        payload = json.loads(_extract_inner_json(payload))

    dsl = payload.get("dsl", "")
    evals = payload.get("evals", [])
    final = payload.get("final", "")

    # Cas 1 : dsl == string mais contient un JSON (code fence) -> extrait
    if isinstance(dsl, str) and "```" in dsl:
        inner = _extract_inner_json(dsl)
        try:
            inner_obj = json.loads(inner)
            dsl   = inner_obj.get("dsl", dsl)
            evals = inner_obj.get("evals", evals) or evals
            final = inner_obj.get("final", final) or final
        except Exception:
            pass

    # Cas 2 : dsl arrive comme une LISTE -> la convertir en lignes DEFINE … WITH …
    if isinstance(dsl, list):
        lines = []
        for item in dsl:
            # formats possibles: {"symbol":"⊕","law":"..."} ou {"rule":"DEFINE ⊕ WITH ..."}
            sym = (str(item.get("symbol","")).strip()
                   or re.sub(r"^DEFINE\s+(.+?)\s+WITH\s+.*$", r"\1", str(item.get("rule","")), flags=re.I))
            law = (str(item.get("law","")).strip()
                   or re.sub(r"^DEFINE\s+.+?\s+WITH\s+(.+)$", r"\1", str(item.get("rule","")), flags=re.I))
            if not sym or not law:
                continue
            # normalisation d’alias fréquents
            if sym == "+": sym = "⊕"
            if sym in {"+O","O+","oplus","OPLUS"}: sym = "⊕"
            if sym in {"*O","O*","otimes","OTIMES"}: sym = "⊗"
            lines.append(f"DEFINE {sym} WITH {law}")
        dsl = "\n".join(lines)

    # Nettoyage evals : enlever quotes superflues
    fixed_evals = []
    for e in evals:
        if isinstance(e, str):
            e = e.strip()
            if e.startswith("'") and e.endswith("'"):
                e = e[1:-1]
            fixed_evals.append(e)

    payload["dsl"] = dsl if isinstance(dsl, str) else ""
    payload["evals"] = fixed_evals
    payload["final"] = final if isinstance(final, str) else ""
    return payload
# ---------- /Sanitizer utils ----------


def main():
    p = argparse.ArgumentParser(description="Conceptual Solver IA (⊘/∞)")
    p.add_argument("--provider", choices=["ollama", "openrouter", "mock"], default="mock")
    p.add_argument("--model", default="llama3.1")
    p.add_argument("--problem", required=True)
    p.add_argument("--orientation", choices=["+","-"], default="+")
    p.add_argument("--test", action="append")
    p.add_argument("--no-evals", action="store_true")
    p.add_argument("--plot", action="store_true", help="Visualiser Hilbert B (ovales imbriqués/disjoints)")
    args = p.parse_args()

    # Provider
    if args.provider == "ollama":
        provider = OllamaProvider(model=args.model)
    elif args.provider == "openrouter":
        provider = OpenRouterProvider(model=args.model)
    else:
        provider = MockProvider()

    # 1 seul appel provider
    raw_payload = provider.solve(args.problem)
    payload = sanitize_payload(raw_payload)

    # Show provider (nettoyé)
    print("=== SORTIE PROVIDER ===")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("========================")

    dsl = payload.get("dsl", "")
    evals = payload.get("evals", [])
    final = payload.get("final", "")

    # Load rules
    if not dsl.strip():
        print("Aucune DSL reçue. Arrêt.")
        sys.exit(1)

    engine = RuleEngine(orientation=args.orientation)
    engine.load_rules_from_text(dsl)

    # Evaluate provider evals
    if not args.no_evals:
        for e in evals:
            try:
                res = engine.evaluate_expression(e)
                print(f"[EVAL IA] {e} => {res}")
            except EvaluationError as ex:
                print(f"[EVAL IA] {e} => ERREUR: {ex}")

    # Evaluate user tests
    if args.test:
        for t in args.test:
            try:
                res = engine.evaluate_expression(t)
                print(f"[TEST YOU] {t} => {res}")
            except EvaluationError as ex:
                print(f"[TEST YOU] {t} => ERREUR: {ex}")

    # Show final answer
    if final:
        print("\n=== SOLUTION PROPOSÉE ===")
        print(final)

    # Plot option
    if args.plot:
        visualize_hilbertB()


if __name__ == "__main__":
    main()
