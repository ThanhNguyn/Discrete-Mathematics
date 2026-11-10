from itertools import product

# Định nghĩa các phép toán logic cơ bản
NOT = lambda p: not p
AND = lambda p, q: p and q
OR = lambda p, q: p or q
XOR = lambda p, q: p != q
IMP = lambda p, q: (not p) or q  # p -> q
IFF = lambda p, q: p == q  # p <-> q


def la_hang_dung(bien, f):
  """Kiểm tra một công thức mệnh đề f có phải là hằng đúng (tautology) hay không.

  bien : danh sách tên biến, ví dụ ["p", "q"]
  f    : hàm nhận các giá trị chân lý (bool) theo đúng thứ tự của `bien`
  """
  return all(f(*vals) for vals in product([True, False], repeat=len(bien)))


# =====================================================================
# KIỂM THỬ VỚI CÁC CÔNG THỨC Ở BÀI 1.9
# =====================================================================
if __name__ == "__main__":
  # (a) (p -> q) <-> (~q -> ~p)  [Luật phản đảo]
  f_a = lambda p, q: IFF(IMP(p, q), IMP(NOT(q), NOT(p)))

  # (b) ((p \/ q) /\ (~p \/ r)) -> (q \/ r)  [Quy tắc phân giải / Resolution]
  f_b = lambda p, q, r: IMP(AND(OR(p, q), OR(NOT(p), r)), OR(q, r))

  # (c) [p -> (q -> r)] -> [(p -> q) -> (p -> r)]  [Tiên đề phân phối phép kéo theo]
  f_c = lambda p, q, r: IMP(IMP(p, IMP(q, r)), IMP(IMP(p, q), IMP(p, r)))

  # (d) ((p (+) q) (+) r) <-> (p (+) (q (+) r))  [Tính kết hợp của phép XOR]
  f_d = lambda p, q, r: IFF(XOR(XOR(p, q), r), XOR(p, XOR(q, r)))

  cac_cong_thuc = [
      ("(a) (p -> q) <-> (~q -> ~p)", ["p", "q"], f_a),
      ("(b) ((p ∨ q) ∧ (¬p ∨ r)) -> (q ∨ r)", ["p", "q", "r"], f_b),
      (
          "(c) [p -> (q -> r)] -> [(p -> q) -> (p -> r)]",
          ["p", "q", "r"],
          f_c,
      ),
      (
          "(d) ((p ⊕ q) ⊕ r) <-> (p ⊕ (q ⊕ r))",
          ["p", "q", "r"],
          f_d,
      ),
  ]

  print(f"{'Công thức':<50} | {'Là hằng đúng?'}")
  print("-" * 68)
  for ten, bien, f in cac_cong_thuc:
    kq = la_hang_dung(bien, f)
    print(f"{ten:<50} | {kq}")