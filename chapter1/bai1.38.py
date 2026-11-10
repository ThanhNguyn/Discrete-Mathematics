"""Bài 1.38 - Tô màu đồ thị bằng 3 màu với bộ giải DPLL."""
from __future__ import annotations

import random

try:
    from other.bo_giai_sat import dpll
except ImportError:
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from other.bo_giai_sat import dpll


def bien(vertex: int, color: int, colors: int = 3) -> int:
    return vertex * colors + color + 1


def tao_cnf_to_mau(vertex_count, edges, colors=3):
    clauses = []
    for vertex in range(vertex_count):
        clauses.append({bien(vertex, color, colors) for color in range(colors)})
        for first in range(colors):
            for second in range(first + 1, colors):
                clauses.append({-bien(vertex, first, colors), -bien(vertex, second, colors)})
    for first_vertex, second_vertex in edges:
        for color in range(colors):
            clauses.append(
                {-bien(first_vertex, color, colors), -bien(second_vertex, color, colors)}
            )
    return clauses


def to_mau_do_thi(vertex_count, edges, colors=3):
    if colors < 1:
        raise ValueError("số màu phải dương")
    if any(
        u < 0 or u >= vertex_count or v < 0 or v >= vertex_count or u == v
        for u, v in edges
    ):
        raise ValueError("cạnh chứa đỉnh không hợp lệ")
    assignment = dpll(tao_cnf_to_mau(vertex_count, edges, colors))
    if assignment is None:
        return None
    return {
        vertex: next(
            color for color in range(colors) if bien(vertex, color, colors) in assignment
        )
        for vertex in range(vertex_count)
    }


def do_thi_ngau_nhien(vertex_count=20, probability=0.12, seed=1):
    rng = random.Random(seed)
    edges = [
        (u, v)
        for u in range(vertex_count)
        for v in range(u + 1, vertex_count)
        if rng.random() < probability
    ]
    return edges, to_mau_do_thi(vertex_count, edges)


if __name__ == "__main__":
    edges, coloring = do_thi_ngau_nhien()
    print(f"{len(edges)} cạnh")
    print("màu:", coloring or "không tô được bằng 3 màu")
