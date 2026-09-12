"""
Unit tests for PRAVAH AI Physics Engine
"""

import unittest
from engine.physics import PravahPhysicsEngine

class TestPravahPhysics(unittest.TestCase):
    def setUp(self):
        self.engine = PravahPhysicsEngine()

    def test_green_ampt_infiltration(self):
        res = self.engine.compute_infiltration(rainfall_rate_mm_hr=40.0, duration_hr=2.0, initial_soil_moisture=0.20)
        self.assertIn("infiltration_capacity_mm_hr", res)
        self.assertIn("surface_runoff_rate_mm_hr", res)
        self.assertTrue(res["soil_saturation_ratio"] > 0.20)
        self.assertTrue(res["soil_saturation_ratio"] <= 1.0)
        print("Green-Ampt Infiltration Test Passed:", res)

    def test_slope_stability_dry_vs_saturated(self):
        # Low saturation should yield high FS (Stable)
        res_dry = self.engine.compute_slope_stability(saturation_ratio=0.30)
        self.assertTrue(res_dry["factor_of_safety"] > 1.3)
        self.assertEqual(res_dry["status"], "STABLE")

        # High saturation (near 100%) should trigger failure (FS < 1.0)
        res_sat = self.engine.compute_slope_stability(saturation_ratio=0.98)
        self.assertTrue(res_sat["factor_of_safety"] < 1.0)
        self.assertEqual(res_sat["status"], "FAILURE")
        print("Slope Stability Test Passed. Dry FS:", res_dry["factor_of_safety"], "Sat FS:", res_sat["factor_of_safety"])

    def test_manning_hydraulics_inversion(self):
        # Check forward
        stage = 3.5
        q, v, a = self.engine.manning_discharge(stage)
        self.assertTrue(q > 50.0)
        self.assertTrue(v > 1.0)

        # Check inversion back to stage
        inverted_h = self.engine.invert_manning_depth(q)
        self.assertAlmostEqual(stage, inverted_h, delta=0.15)
        print(f"Manning Inversion Test Passed: Stage {stage}m -> Q={q} m^3/s -> Inverted Stage={inverted_h}m")

    def test_full_pipeline_chamoli_cloudburst(self):
        # 110 mm/hr cloudburst
        res = self.engine.run_full_pipeline(rainfall_rate_mm_hr=110.0, duration_hr=2.0, initial_soil_moisture=0.35)
        self.assertEqual(res["overall_hazard_level"], "RED")
        self.assertEqual(len(res["deliverable_1_settlements"]), 4)
        
        # Verify lead times are positive and increase downstream
        times = [s["evacuation_lead_time_min"] for s in res["deliverable_1_settlements"]]
        self.assertTrue(all(t > 0 for t in times))
        self.assertTrue(times[0] < times[-1])
        print("Full Pipeline Chamoli Event Passed. Lead times downstream:", times)

if __name__ == "__main__":
    unittest.main()
