import Formalization.ErdosKoRado

/-!
# Completing the two-uniform EKR equality case

This extends the triangle classification contributed in upstream PR #5.
It proves the complete equality statement (a unique full star, not merely
existence of a common element), plus the sharp four-point counterexample.
The general higher-uniformity uniqueness problem is not claimed here.
These are classical consequences, not claims of new extremal mathematics.
-/

open Finset

section
variable {α : Type*} [DecidableEq α]

/-- Two distinct two-sets cannot share two distinct common centres. -/
theorem two_uniform_center_unique (F : Finset (Finset α))
    (hF_two : ∀ A ∈ F, A.card = 2) (hlarge : 1 < F.card)
    {x y : α} (hx : ∀ A ∈ F, x ∈ A) (hy : ∀ A ∈ F, y ∈ A) : x = y := by
  by_contra hxy
  have hpair : ({x, y} : Finset α).card = 2 := by simp [hxy]
  have hsub : F ⊆ ({{x, y}} : Finset (Finset α)) := by
    intro A hA
    have hinc : ({x, y} : Finset α) ⊆ A := by simp [hx A hA, hy A hA]
    have heq : ({x, y} : Finset α) = A :=
      Finset.eq_of_subset_of_card_le hinc (by rw [hpair, hF_two A hA])
    exact Finset.mem_singleton.mpr heq.symm
  have hbound := Finset.card_le_card hsub
  simp only [Finset.card_singleton] at hbound
  omega

/-- The triangle obstruction is the only reason an intersecting two-family can fail to be a star. -/
theorem two_uniform_large_intersecting_isStar [Nonempty α]
    (F : Finset (Finset α)) (hF_two : ∀ A ∈ F, A.card = 2)
    (h_inter : ∀ A ∈ F, ∀ B ∈ F, ¬ Disjoint A B) (hlarge : 3 < F.card) :
    IsStarFamily F := by
  by_contra h
  have hc := two_uniform_intersecting_not_star_card_eq_three F hF_two h_inter h
  omega

variable [Fintype α]

/-- For any uniformity, a star of the full star cardinality is the full star. -/
theorem uniform_star_eq_full_of_card_eq {n k : ℕ}
    (hn : Fintype.card α = n) (hk : 1 ≤ k) (hkn : k ≤ n)
    (F : Finset (Finset α)) (hF_k : ∀ A ∈ F, A.card = k)
    (hstar : IsStarFamily F) (hcard : F.card = Nat.choose (n - 1) (k - 1)) :
    ∃ x : α, F = starFamily x k := by
  obtain ⟨x, hx⟩ := hstar
  have hsub : F ⊆ starFamily x k := by
    intro A hA
    exact Finset.mem_filter.mpr
      ⟨Finset.mem_powersetCard.mpr ⟨Finset.subset_univ A, hF_k A hA⟩, hx A hA⟩
  refine ⟨x, Finset.eq_of_subset_of_card_le hsub ?_⟩
  exact (card_starFamily hn hk hkn x).le.trans hcard.ge

/-- EKR uniqueness for two-element sets, completing the next missing parameter case. -/
theorem erdos_ko_rado_uniqueness_two {n : ℕ}
    (hn : Fintype.card α = n) (h4n : 4 < n)
    (F : Finset (Finset α)) (hF_two : ∀ A ∈ F, A.card = 2)
    (h_inter : ∀ A ∈ F, ∀ B ∈ F, ¬ Disjoint A B)
    (h_max : F.card = Nat.choose (n - 1) (2 - 1)) : IsStarFamily F := by
  haveI : Nonempty α := Fintype.card_pos_iff.mp (by omega)
  have hc : F.card = n - 1 := by simpa using h_max
  exact two_uniform_large_intersecting_isStar F hF_two h_inter (by omega)

/-- The exact two-uniform equality theorem: there is a unique centre, and every pair
containing that centre occurs in the family. -/
theorem erdos_ko_rado_equality_two {n : ℕ}
    (hn : Fintype.card α = n) (h4n : 4 < n)
    (F : Finset (Finset α)) (hF_two : ∀ A ∈ F, A.card = 2)
    (h_inter : ∀ A ∈ F, ∀ B ∈ F, ¬ Disjoint A B)
    (h_max : F.card = Nat.choose (n - 1) (2 - 1)) :
    ∃! x : α, F = starFamily x 2 := by
  have hs := erdos_ko_rado_uniqueness_two hn h4n F hF_two h_inter h_max
  obtain ⟨x, hx⟩ := uniform_star_eq_full_of_card_eq hn (by omega : 1 ≤ 2)
    (by omega : 2 ≤ n) F hF_two hs h_max
  have hc : F.card = n - 1 := by simpa using h_max
  refine ⟨x, hx, ?_⟩
  intro y hy
  apply two_uniform_center_unique F hF_two (by omega)
  · intro A hA
    rw [hy] at hA
    exact (Finset.mem_filter.mp hA).2
  · intro A hA
    rw [hx] at hA
    exact (Finset.mem_filter.mp hA).2

end

/-- At n = 4 the equality bound is attained by a non-star triangle, so strict n > 4
is necessary in the general equality statement above. This uses kernel reduction. -/
theorem ekr_four_point_boundary_counterexample :
    ∃ F : Finset (Finset (Fin 4)),
      (∀ A ∈ F, A.card = 2) ∧
      (∀ A ∈ F, ∀ B ∈ F, ¬ Disjoint A B) ∧
      F.card = Nat.choose (4 - 1) (2 - 1) ∧ ¬ IsStarFamily F := by
  refine ⟨{{0, 1}, {1, 2}, {0, 2}}, ?_, ?_, ?_, ?_⟩ <;> decide
