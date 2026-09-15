"""Sinh DNF/CNF chuan tac hoan toan tu bang chan ly."""
from itertools import product


def dnf_chuan_tac(bien, f):
    """Tra ve chuoi DNF chuan tac hoan toan cua ham f."""
    hoi = []
    for vals in product([True, False], repeat=len(bien)):
        if f(*vals):
            tu_to = [(v if val else "¬" + v) for v, val in zip(bien, vals)]
            hoi.append("(" + " ∧ ".join(tu_to) + ")")
    return " ∨ ".join(hoi) if hoi else "⊥"


def cnf_chuan_tac(bien, f):
    """Tra ve chuoi CNF chuan tac hoan toan cua ham f.

    Moi dong SAI cho mot tuyen so cap (phu dinh cac tu to cua dong do).
    """
    tuyen = []
    for vals in product([True, False], repeat=len(bien)):
        if not f(*vals):
            tu_to = [("¬" + v if val else v) for v, val in zip(bien, vals)]
            tuyen.append("(" + " ∨ ".join(tu_to) + ")")
    return " ∧ ".join(tuyen) if tuyen else "⊤"


if __name__ == "__main__":
    F = lambda p, q, r: ((not p) or q) and r     # (p -> q) AND r
    print("DNF:", dnf_chuan_tac(["p", "q", "r"], F))
    print("CNF:", cnf_chuan_tac(["p", "q", "r"], F))
