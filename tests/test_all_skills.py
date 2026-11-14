#!/usr/bin/env python3
"""Comprehensive test suite for all 13 Digital Thinking Tools AI Skills."""

import importlib.util
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"


def load_module(name: str, rel_path: str):
    path = ROOT / rel_path
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


linter = load_module("ste100_linter", "skills/asd-ste100-skill-linter/scripts/ste100_linter.py")
argmap = load_module("argmap_tool", "skills/argument-mapping-core/scripts/argmap_tool.py")
baserate = load_module("base_rate_calc", "skills/bayesian-base-rate-and-sample-auditor/scripts/base_rate_calc.py")
fermi = load_module("fermi_calc", "skills/fermi-estimation-calculator/scripts/fermi_calc.py")
euler = load_module("euler_sets", "skills/euler-set-reasoning/scripts/euler_sets.py")


class TestAllSkillsSTE100(unittest.TestCase):
    def test_all_13_skills_exist_and_pass_ste100_strict(self):
        skill_files = sorted(SKILLS_DIR.glob("*/SKILL.md"))
        self.assertEqual(len(skill_files), 13, f"Expected 13 skills, found {len(skill_files)}")
        for sf in skill_files:
            res = linter.lint_markdown(sf, strict=True)
            self.assertTrue(
                res["passed"],
                f"STE100 lint failed for {sf.parent.name}: {res['errors']}",
            )


class TestArgumentMappingCore(unittest.TestCase):
    def test_carrots_argument_map_and_exports(self):
        shorthand = (
            "MC 'Eating carrots improves eyesight.' "
            "SUPPORT 1 'Carrots are a source of Vitamin A.' "
            "2 'Taking vitamin A can reduce the risk of poor vision in individuals with a vitamin deficiency.' "
            "SUPPORT 2.1 'Christian et al. (1998) found lower night blindness risk in Asian women.' "
            "OPPOSE 3 'Carrots are a source of beta carotene.' "
            "4 'Beta carotene supplements will not strengthen eyesight in healthy people.' "
            "SUPPORT 4.1 'Christen et al. (2003) found no cataract reduction in US male physicians.'"
        )
        nodes = argmap.parse_shorthand(shorthand)
        audit = argmap.audit_map(nodes)
        self.assertTrue(audit["valid"])
        self.assertEqual(audit["total_claims"], 7)
        self.assertEqual(audit["max_level"], 2)
        self.assertEqual(audit["grouped_sets_count"], 2)
        base_ids = {b["id"] for b in audit["base_claims"]}
        self.assertEqual(base_ids, {"1", "2.1", "3", "4.1"})

        mermaid = argmap.to_mermaid(nodes)
        self.assertIn("graph LR", mermaid)
        self.assertIn("SUPPORT", mermaid)
        self.assertIn("OPPOSE", mermaid)

        mm_xml = argmap.to_freemind_xml(nodes)
        root = ET.fromstring(mm_xml)
        self.assertEqual(root.tag, "map")

        argdown = argmap.to_argdown(nodes)
        self.assertIn("# Eating carrots improves eyesight.", argdown)

    def test_tor_stinks_nested_oppose(self):
        shorthand = (
            "MC 'Tor stinks...' "
            "SUPPORT 1 'We will never be able to de-anonymize all Tor users all the time.' "
            "OPPOSE 1.1 'With manual analysis we can de-anonymize a very small fraction of Tor users.' "
            "OPPOSE 1.1.1 'There are certain communications on Tor that cannot be de-anonymized.'"
        )
        nodes = argmap.parse_shorthand(shorthand)
        audit = argmap.audit_map(nodes)
        self.assertEqual(audit["max_level"], 3)
        self.assertEqual(audit["oppose_claims"], 2)


class TestBayesianAndSmallNumbers(unittest.TestCase):
    def test_false_positive_paradox_course_values(self):
        res = baserate.false_positive_analysis(base_rate=0.001, accuracy=0.99, population=100_000)
        self.assertAlmostEqual(res["posterior_percent"], 9.02, places=1)
        self.assertEqual(res["natural_frequencies"]["D_positive"], 99)
        self.assertEqual(res["natural_frequencies"]["ND_positive_false_positives"], 999)
        self.assertTrue(res["base_rate_swamped"])

        res_1pct = baserate.false_positive_analysis(base_rate=0.01, accuracy=0.99)
        self.assertAlmostEqual(res_1pct["posterior_percent"], 50.0, places=1)

        res_10pct = baserate.false_positive_analysis(base_rate=0.1, accuracy=0.99)
        self.assertAlmostEqual(res_10pct["posterior_percent"], 91.67, places=1)

    def test_small_numbers_simulation(self):
        sim = baserate.small_numbers_simulation(rate=0.001, small_n=100, large_n=100_000, trials=30, seed=42)
        small_spread = sim["small_sample"]["max_observed_rate"] - sim["small_sample"]["min_observed_rate"]
        large_spread = sim["large_sample"]["max_observed_rate"] - sim["large_sample"]["min_observed_rate"]
        self.assertGreater(small_spread, large_spread)


class TestFermiEstimation(unittest.TestCase):
    def test_uk_gps_course_example(self):
        res = fermi.compute_fermi(
            numerators=[
                {"name": "uk_pop", "value": 65e6},
                {"name": "visits_per_year", "value": 3},
                {"name": "mins_per_visit", "value": 10},
            ],
            denominators=[
                {"name": "gp_hrs_wk", "value": 20},
                {"name": "gp_wks_yr", "value": 44},
                {"name": "mins_per_hr", "value": 60},
            ],
            round_digits=-3,
        )
        self.assertEqual(res["rounded_estimate"], 37000.0)


class TestEulerSets(unittest.TestCase):
    def test_playing_cards_partition(self):
        res = euler.analyze_two_sets(universe_size=52, set_a_size=12, set_b_size=13, intersection_size=3)
        self.assertEqual(res["euler_relation"], "INTERSECTION")
        self.assertEqual(res["regions"]["A_only"], 9)
        self.assertEqual(res["regions"]["B_only"], 10)
        self.assertEqual(res["regions"]["neither"], 30)
        self.assertTrue(res["conjunction_rule_holds"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
