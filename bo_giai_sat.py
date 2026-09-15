"""Bo giai SAT theo thuat toan DPLL.

Bieu dien: cong thuc CNF la list cac clause;
mot clause la set cac so nguyen khac 0;
so duong  k  ung voi bien p_k, so am -k ung voi ¬p_k.
Vi du: (p1 ∨ ¬p2) ∧ (¬p1 ∨ p3)  ->  [{1, -2}, {-1, 3}]
"""


def lan_truyen_don_vi(cnf, gan):
    """Ap dung luat clause don vi den khi khong the nua."""
    thay_doi = True
    while thay_doi:
        thay_doi = False
        for clause in cnf:
            if len(clause) == 1:
                lit = next(iter(clause))
                if -lit in gan:
                    return None, None           # mau thuan
                if lit not in gan:
                    gan = gan | {lit}
                    cnf = rut_gon(cnf, lit)
                    if cnf is None:
                        return None, None
                    thay_doi = True
                    break
    return cnf, gan


def rut_gon(cnf, lit):
    """Gan lit = True: bo clause chua lit, bo -lit khoi cac clause con lai."""
    moi = []
    for clause in cnf:
        if lit in clause:
            continue                            # clause da thoa
        c = clause - {-lit}
        if not c:
            return None                         # clause rong -> mau thuan
        moi.append(c)
    return moi


def tu_to_thuan(cnf, gan):
    """Tim cac tu to chi xuat hien voi mot dau -> gan True cho chung."""
    xuat_hien = set()
    for clause in cnf:
        xuat_hien |= clause
    for lit in xuat_hien:
        if -lit not in xuat_hien and lit not in gan:
            return lit
    return None


def dpll(cnf, gan=frozenset()):
    """Tra ve tap gan thoa man, hoac None neu khong thoa duoc."""
    cnf, gan = lan_truyen_don_vi(cnf, set(gan))
    if cnf is None:
        return None
    if not cnf:                                 # het clause -> thoa
        return gan
    lit = tu_to_thuan(cnf, gan)
    if lit is not None:
        r = rut_gon(cnf, lit)
        return None if r is None else dpll(r, gan | {lit})
    # chia truong hop tren mot bien tuy y
    chon = next(iter(cnf[0]))
    for thu in (chon, -chon):
        r = rut_gon(cnf, thu)
        if r is not None:
            kq = dpll(r, gan | {thu})
            if kq is not None:
                return kq
    return None


if __name__ == "__main__":
    # (p1 ∨ p2) ∧ (¬p1 ∨ p3) ∧ (¬p2 ∨ ¬p3) ∧ (p1 ∨ ¬p3)
    F = [{1, 2}, {-1, 3}, {-2, -3}, {1, -3}]
    kq = dpll(F)
    print("THOA DUOC:", sorted(kq, key=abs) if kq else "KHONG")
    # >>> THOA DUOC: [1, -2, 3]

    # Cong thuc khong thoa duoc: (p) ∧ (¬p)
    print(dpll([{1}, {-1}]))     # >>> None
