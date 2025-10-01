import matplotlib.pyplot as plt

# --- Définition des axiomes indépendants ---
def ovale(a, b):
    """Axiome : tout ovale existe, renvoie toujours 1."""
    return 1

def nid(a, b):
    """Axiome : nidation est additive."""
    return a + b

def distribution(a, b):
    """Axiome : Δ = nested si a<b, sinon separated."""
    return "nested" if a < b else "separated"

def complexite(a, b):
    """Axiome : χ est additif."""
    return a + b


# --- Mode démonstration graphique ---
def plot_axiomes():
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.set_title("Hilbert B – Ovale, Nids et Distributions")

    # 1) Ovale : cercle unité
    circle = plt.Circle((0, 0), 1, fill=False, color="blue", label="Ovale (○)")
    ax.add_patch(circle)

    # 2) Nid : deux cercles imbriqués
    c1 = plt.Circle((0, 0), 0.7, fill=False, color="red", label="Nid (⊂)")
    c2 = plt.Circle((0, 0), 0.4, fill=False, color="green")
    ax.add_patch(c1)
    ax.add_patch(c2)

    # 3) Distribution nested vs separated
    nested = plt.Circle((0.7, 0.7), 0.3, fill=False, color="orange", label="Nested Δ")
    separated = plt.Circle((-0.7, -0.7), 0.3, fill=False, color="purple", label="Separated Δ")
    ax.add_patch(nested)
    ax.add_patch(separated)

    # 4) Complexité χ : texte additif
    ax.text(0, -1.2, f"Complexité χ(3,5)={complexite(3,5)}", ha="center")

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.legend(loc="upper right")
    plt.show()


# --- Démonstration console ---
if __name__ == "__main__":
    print("Axiomes Hilbert B :")
    print("Ovale ○ =>", ovale(1, 0))
    print("Nid 1 ⊂ 2 =>", nid(1, 2))
    print("Distribution 2 Δ 3 =>", distribution(2, 3))
    print("Distribution 3 Δ 2 =>", distribution(3, 2))
    print("Complexité 3 χ 5 =>", complexite(3, 5))

    plot_axiomes()
