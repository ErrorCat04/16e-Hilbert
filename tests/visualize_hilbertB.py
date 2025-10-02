import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_ovale(ax, center, radius, label=None, color="blue"):
    circle = patches.Circle(center, radius, fill=False, edgecolor=color, linewidth=2)
    ax.add_patch(circle)
    if label:
        ax.text(center[0], center[1], label, ha="center", va="center", fontsize=10, color=color)

def visualize_partB():
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect("equal")
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.axis("off")

    # Exemple : un ovale simple
    draw_ovale(ax, (0, 0), 4, label="○", color="blue")

    # Exemple : un nid (ovale dans un autre)
    draw_ovale(ax, (0, 0), 3, label="⊂", color="red")
    draw_ovale(ax, (0, 0), 2, label="⊂", color="green")

    # Exemple : distribution séparée
    draw_ovale(ax, (-2, -2), 1, label="○", color="purple")
    draw_ovale(ax, (3, 3), 1.5, label="○", color="orange")

    plt.title("Hilbert B – Ovale, Nids et Distributions", fontsize=14)
    plt.show()

if __name__ == "__main__":
    visualize_partB()
