from itertools import product
import re


# =====================================================================
# 1. BỘ PHÂN TÍCH TỪ VỰNG (LEXER)
# =====================================================================
class Token:

  def __init__(self, type_: str, value: str):
    self.type = type_
    self.value = value

  def __repr__(self):
    return f"Token({self.type}, '{self.value}')"


TOKEN_SPEC = [
    ("IFF", r"<->|<=>|↔"),  # Phép tương đương
    ("IMP", r"->|=>|→"),  # Phép kéo theo
    ("XOR", r"\^|⊕|\bxor\b|\bXOR\b"),  # Phép tuyển loại trừ
    ("OR", r"\|\||\||∨|\bor\b|\bOR\b"),  # Phép tuyển
    ("AND", r"&&|&|∧|\band\b|\bAND\b"),  # Phép hội
    ("NOT", r"~|!|¬|\bnot\b|\bNOT\b"),  # Phép phủ định
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("VAR", r"[a-zA-Z_][a-zA-Z0-9_]*"),  # Biến mệnh đề
    ("SKIP", r"[ \t\r\n]+"),  # Bỏ qua khoảng trắng
    ("MISMATCH", r"."),  # Ký tự lạ
]

TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)


def tokenize(expr: str):
  """Chuyển chuỗi biểu thức logic thành danh sách các Token."""
  tokens = []
  for match in re.finditer(TOKEN_REGEX, expr):
    kind = match.lastgroup
    val = match.group()
    if kind == "SKIP":
      continue
    elif kind == "MISMATCH":
      raise SyntaxError(
          f"Ký tự không hợp lệ trong biểu thức: '{val}' tại vị trí"
          f" {match.start()}"
      )
    tokens.append(Token(kind, val))
  tokens.append(Token("EOF", ""))
  return tokens


# =====================================================================
# 2. CÂY CÚ PHÁP TRỪU TƯỢNG (AST - ABSTRACT SYNTAX TREE)
# =====================================================================
class Node:

  def evaluate(self, env: dict) -> bool:
    raise NotImplementedError

  def get_vars(self) -> set:
    raise NotImplementedError

  def draw(self, prefix="", is_last=True) -> str:
    raise NotImplementedError


class VarNode(Node):
  """Nút lá biểu diễn biến mệnh đề (p, q, r,...)."""

  def __init__(self, name: str):
    self.name = name

  def evaluate(self, env: dict) -> bool:
    return env[self.name]

  def get_vars(self) -> set:
    return {self.name}

  def draw(self, prefix="", is_last=True) -> str:
    branch = "└── " if is_last else "├── "
    return f"{prefix}{branch}Biến({self.name})\n"


class UnaryOpNode(Node):
  """Nút biểu diễn phép toán 1 ngôi (phủ định ~)."""

  def __init__(self, op: str, operand: Node):
    self.op = op
    self.operand = operand

  def evaluate(self, env: dict) -> bool:
    return not self.operand.evaluate(env)

  def get_vars(self) -> set:
    return self.operand.get_vars()

  def draw(self, prefix="", is_last=True) -> str:
    branch = "└── " if is_last else "├── "
    res = f"{prefix}{branch}Toán tử: {self.op}\n"
    new_prefix = prefix + ("    " if is_last else "│   ")
    res += self.operand.draw(new_prefix, is_last=True)
    return res


class BinaryOpNode(Node):
  """Nút biểu diễn phép toán 2 ngôi (&, |, ^, ->, <->)."""

  def __init__(self, op: str, left: Node, right: Node):
    self.op = op
    self.left = left
    self.right = right

  def evaluate(self, env: dict) -> bool:
    l_val = self.left.evaluate(env)
    r_val = self.right.evaluate(env)
    if self.op in ("&", "&&", "∧", "and", "AND"):
      return l_val and r_val
    elif self.op in ("|", "||", "∨", "or", "OR"):
      return l_val or r_val
    elif self.op in ("^", "⊕", "xor", "XOR"):
      return l_val != r_val
    elif self.op in ("->", "=>", "→"):
      return (not l_val) or r_val
    elif self.op in ("<->", "<=>", "↔"):
      return l_val == r_val
    raise ValueError(f"Toán tử chưa được định nghĩa: {self.op}")

  def get_vars(self) -> set:
    return self.left.get_vars() | self.right.get_vars()

  def draw(self, prefix="", is_last=True) -> str:
    branch = "└── " if is_last else "├── "
    res = f"{prefix}{branch}Toán tử: {self.op}\n"
    new_prefix = prefix + ("    " if is_last else "│   ")
    res += self.left.draw(new_prefix, is_last=False)
    res += self.right.draw(new_prefix, is_last=True)
    return res


# =====================================================================
# 3. BỘ PHÂN TÍCH CÚ PHÁP (RECURSIVE DESCENT PARSER)
# =====================================================================
class Parser:
  """Bộ phân tích cú pháp theo kỹ thuật Đệ quy xuống.

  Độ ưu tiên (từ thấp đến cao):
    1. parse_iff     : <-> (kết hợp trái)
    2. parse_imp     : ->  (kết hợp phải)
    3. parse_or_xor  : |, ^ (kết hợp trái)
    4. parse_and     : & (kết hợp trái)
    5. parse_not     : ~ (phép 1 ngôi, kết hợp phải)
    6. parse_primary : Biến, dấu ngoặc đơn (...)
  """

  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0

  def peek(self) -> Token:
    return self.tokens[self.pos]

  def consume(self, expected_type=None) -> Token:
    tok = self.peek()
    if expected_type and tok.type != expected_type:
      raise SyntaxError(
          f"Mong đợi token '{expected_type}' nhưng gặp '{tok.value}'"
          f" (loại {tok.type})"
      )
    self.pos += 1
    return tok

  def parse(self) -> Node:
    node = self.parse_iff()
    if self.peek().type != "EOF":
      raise SyntaxError(f"Ký tự thừa ở cuối biểu thức: '{self.peek().value}'")
    return node

  # Mức 5: Tương đương (<->)
  def parse_iff(self) -> Node:
    node = self.parse_imp()
    while self.peek().type == "IFF":
      op = self.consume().value
      right = self.parse_imp()
      node = BinaryOpNode(op, node, right)
    return node

  # Mức 4: Kéo theo (->), kết hợp phải: p -> q -> r == p -> (q -> r)
  def parse_imp(self) -> Node:
    node = self.parse_or_xor()
    if self.peek().type == "IMP":
      op = self.consume().value
      right = self.parse_imp()  # Đệ quy chính nó để tạo kết hợp phải
      node = BinaryOpNode(op, node, right)
    return node

  # Mức 3: Tuyển (OR), Tuyển loại trừ (XOR)
  def parse_or_xor(self) -> Node:
    node = self.parse_and()
    while self.peek().type in ("OR", "XOR"):
      op = self.consume().value
      right = self.parse_and()
      node = BinaryOpNode(op, node, right)
    return node

  # Mức 2: Hội (AND)
  def parse_and(self) -> Node:
    node = self.parse_not()
    while self.peek().type == "AND":
      op = self.consume().value
      right = self.parse_not()
      node = BinaryOpNode(op, node, right)
    return node

  # Mức 1: Phủ định (NOT)
  def parse_not(self) -> Node:
    if self.peek().type == "NOT":
      op = self.consume().value
      operand = self.parse_not()  # Hỗ trợ phủ định liên tiếp: ~~p
      return UnaryOpNode(op, operand)
    return self.parse_primary()

  # Mức cơ sở: Biến hoặc Cặp ngoặc (Expression)
  def parse_primary(self) -> Node:
    tok = self.peek()
    if tok.type == "VAR":
      self.consume("VAR")
      return VarNode(tok.value)
    elif tok.type == "LPAREN":
      self.consume("LPAREN")
      sub_expr = self.parse_iff()
      self.consume("RPAREN")
      return sub_expr
    else:
      raise SyntaxError(f"Cú pháp không hợp lệ tại token: '{tok.value}'")


# =====================================================================
# 4. IN BẢNG CHÂN LÝ VÀ PHÂN LOẠI
# =====================================================================
def in_bang_chan_ly(ast_root: Node, bieu_thuc_goc: str):
  """Sinh và hiển thị bảng chân lý cho cây AST."""
  bien_ds = sorted(list(ast_root.get_vars()))
  n = len(bien_ds)

  # Tiêu đề bảng
  cot_bien = " | ".join(f"{b:^5}" for b in bien_ds)
  tieu_de = f"{cot_bien} || {bieu_thuc_goc:^15}"
  duong_ke = "=" * len(tieu_de)

  print("\n" + duong_ke)
  print(tieu_de)
  print(duong_ke)

  tat_ca_ket_qua = []
  # Duyệt toàn bộ 2^n bộ giá trị chân lý
  for vals in product([True, False], repeat=n):
    env = dict(zip(bien_ds, vals))
    res = ast_root.evaluate(env)
    tat_ca_ket_qua.append(res)

    dong_bien = " | ".join(f"{('T' if v else 'F'):^5}" for v in vals)
    dong_res = f"{('T' if res else 'F'):^15}"
    print(f"{dong_bien} || {dong_res}")

  print(duong_ke)

  # Kết luận phân loại công thức
  if all(tat_ca_ket_qua):
    phan_loai = "HẰNG ĐÚNG (Tautology)"
  elif not any(tat_ca_ket_qua):
    phan_loai = "HẰNG SAI (Contradiction)"
  else:
    phan_loai = "THỎA ĐƯỢC (Satisfiable / Contingent)"

  print(f"-> Phân loại: Mệnh đề là {phan_loai}.\n")


# =====================================================================
# 5. CHƯƠNG TRÌNH CHÍNH (DEMO)
# =====================================================================
def main():
  print("=" * 65)
  print(" TRÌNH PHÂN TÍCH CÚ PHÁP & SINH BẢNG CHÂN LÝ MỆNH ĐỀ")
  print(" Hỗ trợ các ký hiệu:")
  print("   - NOT       : ~  hoặc !")
  print("   - AND       : &  hoặc ∧")
  print("   - OR        : |  hoặc ∨")
  print("   - XOR       : ^  hoặc ⊕")
  print("   - IMPLIES   : ->")
  print("   - IFF       : <->")
  print("=" * 65)

  user_input = input("\nNhập công thức (Enter để lấy mẫu '(p & ~q) -> r'): ")
  expr = user_input.strip() if user_input.strip() else "(p & ~q) -> r"

  print(f"\n[1] Công thức đang xử lý: {expr}")

  try:
    # Bước 1: Lexing
    tokens = tokenize(expr)

    # Bước 2: Parsing & Xây cây cú pháp
    parser = Parser(tokens)
    ast = parser.parse()

    # Bước 3: In cây cú pháp (AST)
    print("\n[2] Cây cú pháp trừu tượng (AST):")
    print(ast.draw().rstrip())

    # Bước 4: Lập và in bảng chân lý
    in_bang_chan_ly(ast, expr)

  except SyntaxError as e:
    print(f"\n[!] Lỗi cú pháp: {e}")
  except Exception as e:
    print(f"\n[!] Có lỗi xảy ra: {e}")


if __name__ == "__main__":
  main()