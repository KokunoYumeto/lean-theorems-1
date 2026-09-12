"""Synthetic checker tests only; these do not run Lean or certify any theorem."""
import unittest
from check_pilot import audit_axiom_log, preflight


class PilotChecks(unittest.TestCase):
    def test_real_preflight(self):
        self.assertEqual(len(preflight()["noether"]["axiom_audit_targets"]), 10)

    def test_standard_axioms(self):
        self.assertEqual(audit_axiom_log("'T' depends on axioms: [propext, Classical.choice, Quot.sound]", ["T"])["T"],
                         ["propext", "Classical.choice", "Quot.sound"])

    def test_multiline(self):
        self.assertEqual(audit_axiom_log("'T' depends on axioms:\n[propext,\n Quot.sound]", ["T"])["T"],
                         ["propext", "Quot.sound"])

    def test_no_axioms(self):
        self.assertEqual(audit_axiom_log("'T' does not depend on any axioms", ["T"]), {"T": []})

    def test_missing_target(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("'Other' depends on axioms: [propext]", ["T"])

    def test_duplicate_target(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("'T' depends on axioms: []\n'T' depends on axioms: []", ["T"])

    def test_custom_axiom(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("'T' depends on axioms: [Project.assumeMainTheorem]", ["T"])

    def test_sorry(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("'T' depends on axioms: [sorryAx]", ["T"])

    def test_native_escape(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("'T' depends on axioms: [Lean.ofReduceBool]", ["T"])

    def test_empty_log(self):
        with self.assertRaises(ValueError):
            audit_axiom_log("", ["T"])


if __name__ == "__main__":
    unittest.main()
