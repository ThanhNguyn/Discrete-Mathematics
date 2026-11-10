"""Dự án 1.1 - Bộ kiểm chứng đặc tả bằng DPLL.

Mỗi ràng buộc là một clause CNF, ví dụ ``{1, -2}`` nghĩa là
``p1 OR NOT p2``.
"""
from __future__ import annotations

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from other.bo_giai_sat import dpll


def kiem_tra_sat(constraints):
    """Trả về một cấu hình thỏa mãn hoặc ``None`` nếu mâu thuẫn."""
    clauses = [set(clause) for clause in constraints]
    return dpll(clauses)


def unsat_core(constraints):
    """Tìm một unsat core tối thiểu theo inclusion bằng loại bỏ từng clause."""
    core = [set(clause) for clause in constraints]
    if kiem_tra_sat(core) is not None:
        return []
    changed = True
    while changed:
        changed = False
        for index in range(len(core) - 1, -1, -1):
            candidate = core[:index] + core[index + 1 :]
            if kiem_tra_sat(candidate) is None:
                core = candidate
                changed = True
    return core


def cau_hinh_text(assignment) -> dict[int, bool]:
    """Đổi cấu hình DPLL thành ánh xạ biến -> giá trị."""
    if assignment is None:
        return {}
    return {abs(literal): literal > 0 for literal in assignment}


def kiem_chung(constraints):
    """Trả về báo cáo SAT/UNSAT, cấu hình hoặc unsat core."""
    assignment = kiem_tra_sat(constraints)
    if assignment is not None:
        return {"sat": True, "cau_hinh": cau_hinh_text(assignment), "unsat_core": []}
    return {"sat": False, "cau_hinh": {}, "unsat_core": unsat_core(constraints)}


if __name__ == "__main__":
    sat = [{1, 2}, {-1, 3}, {-2, -3}]
    unsat = [{1}, {-1}, {2, 3}]
    print("SAT:", kiem_chung(sat))
    print("UNSAT:", kiem_chung(unsat))
