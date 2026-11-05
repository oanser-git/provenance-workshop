#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "figures" / "results"
MODEL_COLORS = {
    "MLP": "#8064A2",
    "MLP + LR-E2E": "#4F9D78",
    "LSTM": "#4C78A8",
    "Transformer": "#59A14F",
}
MODEL_MARKERS = {"MLP": "D", "MLP + LR-E2E": "D", "LSTM": "o", "Transformer": "s"}
SCOPE_COLORS = {
    "Ligolo-ng": "#4C78A8",
    "LinPEAS": "#59A14F",
    "Combined": "#F28E2B",
}
SCOPE_MARKERS = {"Ligolo-ng": "o", "LinPEAS": "s", "Combined": "^"}
GUIDE_COLOR = "#8F9CA6"
GUIDE_LINESTYLE = (0, (3, 4))


def save_figure(fig: plt.Figure, name: str) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_DIR / f"{name}.pdf", bbox_inches="tight", transparent=True)
    fig.savefig(OUT_DIR / f"{name}.png", dpi=240, bbox_inches="tight", transparent=True)
    plt.close(fig)


def plot_mlp_baseline() -> None:
    # Reported experimental results are embedded here; this is not training code.
    value = 0.588105
    fig, ax = plt.subplots(figsize=(8.3, 1.82))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.axvspan(0.55, 0.75, color="#F2F4F5", zorder=0)
    ax.hlines(
        0,
        xmin=0.55,
        xmax=value,
        color=GUIDE_COLOR,
        linewidth=1.05,
        alpha=0.95,
        linestyles=GUIDE_LINESTYLE,
        zorder=1,
    )
    ax.scatter(
        value,
        0,
        s=82,
        marker=MODEL_MARKERS["MLP"],
        color=MODEL_COLORS["MLP"],
        edgecolor="#30353A",
        linewidth=0.7,
        zorder=3,
        label="MLP",
    )
    ax.text(
        value + 0.005,
        0,
        f"{value:.3f}",
        va="center",
        ha="left",
        fontsize=11,
        fontweight="bold",
        color="#2F3438",
    )

    ax.set_xlim(0.55, 0.75)
    ax.set_ylim(-0.38, 0.38)
    ax.set_yticks([0], ["MLP baseline"], fontsize=11, fontweight="bold")
    ax.set_xlabel("Macro F1", fontsize=10.5)
    ax.set_xticks(np.arange(0.55, 0.751, 0.05))
    ax.tick_params(axis="x", labelsize=9.5)
    ax.xaxis.grid(True, color="#D8DCE0", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#7A7F85")

    fig.legend(
        loc="upper center",
        ncol=1,
        frameon=False,
        fontsize=14,
        markerscale=1.35,
        bbox_to_anchor=(0.56, 1.03),
        handletextpad=0.7,
    )
    fig.subplots_adjust(left=0.20, right=0.96, top=0.70, bottom=0.32)
    save_figure(fig, "mlp_baseline_macro_f1")


def plot_mlp_rules_main_result() -> None:
    baseline = 0.588105
    methods = ["Baseline", "LR-INF", "LR-KD", "LR-E2E"]
    scopes = ["Ligolo-ng", "LinPEAS", "Combined"]
    values = {
        "LR-INF": {"Ligolo-ng": 0.629413, "LinPEAS": 0.643021, "Combined": 0.684329},
        "LR-KD": {"Ligolo-ng": 0.607181, "LinPEAS": 0.677476, "Combined": 0.707150},
        "LR-E2E": {"Ligolo-ng": 0.609245, "LinPEAS": 0.685923, "Combined": 0.726609},
    }
    offsets = {"Ligolo-ng": -0.25, "LinPEAS": 0.0, "Combined": 0.25}
    y = np.arange(len(methods))

    fig, ax = plt.subplots(figsize=(8.9, 3.65))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.axvspan(0.55, 0.75, color="#F2F4F5", zorder=0)
    for separator in [0.5, 1.5, 2.5]:
        ax.axhline(separator, color="#AEB8C0", linewidth=0.8, alpha=0.95, zorder=1)

    ax.hlines(
        y[0],
        xmin=0.55,
        xmax=baseline,
        color=GUIDE_COLOR,
        linewidth=1.05,
        alpha=0.95,
        linestyles=GUIDE_LINESTYLE,
        zorder=1,
    )
    ax.scatter(
        baseline,
        y[0],
        s=86,
        marker=MODEL_MARKERS["MLP"],
        color=MODEL_COLORS["MLP"],
        edgecolor="#30353A",
        linewidth=0.75,
        zorder=3,
        label="MLP baseline",
    )
    ax.text(
        baseline + 0.004,
        y[0],
        f"{baseline:.3f}",
        va="center",
        ha="left",
        fontsize=10.5,
        fontweight="bold",
        color="#2F3438",
    )

    for scope in scopes:
        scope_values = [values[method][scope] for method in methods[1:]]
        positions = y[1:] + offsets[scope]
        for value, position in zip(scope_values, positions):
            ax.hlines(
                position,
                xmin=0.55,
                xmax=value,
                color=GUIDE_COLOR,
                linewidth=1.05,
                alpha=0.95,
                linestyles=GUIDE_LINESTYLE,
                zorder=1,
            )
        ax.scatter(
            scope_values,
            positions,
            s=78,
            marker=SCOPE_MARKERS[scope],
            color=SCOPE_COLORS[scope],
            edgecolor="#30353A",
            linewidth=0.75,
            zorder=3,
            label=scope,
        )
        for value, position in zip(scope_values, positions):
            ax.text(
                value + 0.004,
                position,
                f"{value:.3f}",
                va="center",
                ha="left",
                fontsize=9.5,
                fontweight="bold",
                color="#2F3438",
            )

    fig.legend(
        loc="upper center",
        ncol=4,
        frameon=False,
        fontsize=12.5,
        markerscale=1.35,
        columnspacing=1.6,
        handletextpad=0.7,
        bbox_to_anchor=(0.56, 0.99),
    )

    ax.set_xlim(0.55, 0.75)
    ax.set_xticks(np.arange(0.55, 0.751, 0.05))
    ax.set_ylim(3.85, -0.85)
    ax.set_yticks(y, methods, fontsize=11, fontweight="bold")
    ax.set_xlabel("Macro F1", fontsize=10.5)
    ax.tick_params(axis="x", labelsize=9.5)
    ax.xaxis.grid(True, color="#D8DCE0", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#7A7F85")

    fig.subplots_adjust(left=0.15, right=0.94, top=0.84, bottom=0.13)
    save_figure(fig, "mlp_rules_main_result")


def plot_context_native_comparison() -> None:
    rows = [
        ("MLP baseline", "MLP", 0.588105),
        ("Transformer baseline", "Transformer", 0.719512),
        ("MLP + LR-E2E", "MLP + LR-E2E", 0.726609),
        ("LSTM baseline", "LSTM", 0.735775),
    ]
    y = np.arange(len(rows))

    fig, ax = plt.subplots(figsize=(8.9, 3.45))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    ax.axvspan(0.55, 0.75, color="#F2F4F5", zorder=0)
    for separator in [0.5, 1.5, 2.5]:
        ax.axhline(separator, color="#AEB8C0", linewidth=0.8, alpha=0.95, zorder=1)

    for position, (_label, model, value) in enumerate(rows):
        ax.hlines(
            position,
            xmin=0.55,
            xmax=value,
            color=GUIDE_COLOR,
            linewidth=1.05,
            alpha=0.95,
            linestyles=GUIDE_LINESTYLE,
            zorder=1,
        )
        ax.scatter(
            value,
            position,
            s=88,
            marker=MODEL_MARKERS[model],
            color=MODEL_COLORS[model],
            edgecolor="#30353A",
            linewidth=0.75,
            zorder=3,
            label=model,
        )
        ax.text(
            value + 0.004,
            position,
            f"{value:.3f}",
            va="center",
            ha="left",
            fontsize=10.5,
            fontweight="bold",
            color="#2F3438",
        )

    handles = [
        plt.Line2D(
            [0],
            [0],
            marker=MODEL_MARKERS[model],
            color="none",
            markerfacecolor=MODEL_COLORS[model],
            markeredgecolor="#30353A",
            markeredgewidth=0.75,
            markersize=8,
            label=model,
        )
        for model in ["MLP", "Transformer", "MLP + LR-E2E", "LSTM"]
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        ncol=4,
        frameon=False,
        fontsize=12.5,
        markerscale=1.25,
        columnspacing=1.5,
        handletextpad=0.7,
        bbox_to_anchor=(0.56, 0.99),
    )

    ax.set_xlim(0.55, 0.75)
    ax.set_xticks(np.arange(0.55, 0.751, 0.05))
    ax.set_ylim(3.75, -0.75)
    ax.set_yticks(y, [label for label, _model, _value in rows], fontsize=11, fontweight="bold")
    ax.set_xlabel("Macro F1", fontsize=10.5)
    ax.tick_params(axis="x", labelsize=9.5)
    ax.xaxis.grid(True, color="#D8DCE0", linewidth=0.7)
    ax.set_axisbelow(True)
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#7A7F85")

    fig.subplots_adjust(left=0.24, right=0.94, top=0.83, bottom=0.14)
    save_figure(fig, "context_native_comparison")


def main() -> None:
    plot_mlp_baseline()
    plot_mlp_rules_main_result()
    plot_context_native_comparison()


if __name__ == "__main__":
    main()
