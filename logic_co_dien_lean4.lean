open Classical

-- Luat bai trung: can logic co dien
theorem bai_trung (p : Prop) : Or p (Not p) := Classical.em p

-- Chieu con lai cua De Morgan: cung can logic co dien
theorem de_morgan_2 (p q : Prop) :
    Iff (Not (And p q)) (Or (Not p) (Not q)) := by
  constructor
  · intro h
    by_cases hp : p
    · exact Or.inr (fun hq => h (And.intro hp hq))
    · exact Or.inl hp
  · intro h hpq
    cases h with
    | inl hnp => exact hnp hpq.1
    | inr hnq => exact hnq hpq.2

-- Phan chung: tu Not (Not p) suy ra p
theorem phan_chung (p : Prop) (h : Not (Not p)) : p := by
  by_cases hp : p
  · exact hp
  · exact absurd hp h
