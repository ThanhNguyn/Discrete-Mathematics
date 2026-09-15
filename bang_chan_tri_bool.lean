-- Kiem tra moi hang dung tren Bool bang cach duyet toan bo
example : forall p q : Bool, (!(p && q)) = ((!p) || (!q)) := by
  decide

example : forall p q r : Bool,
    (p && (q || r)) = ((p && q) || (p && r)) := by
  decide

-- Voi 4 bien van rat nhanh: 16 truong hop
example : forall p q r s : Bool,
    ((p && q) || (r && s)) =
      ((p || r) && (p || s) && (q || r) && (q || s)) := by
  decide
