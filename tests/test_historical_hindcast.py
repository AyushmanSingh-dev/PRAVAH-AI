"""
Unit test suite verifying PRAVAH AI historical hindcasting against landmark Indian disaster datasets.
"""

import unittest
from engine.historical_validation import run_historical_hindcast_suite

class TestHistoricalDisasterHindcast(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = run_historical_hindcast_suite()

    def test_total_events_evaluated(self):
        self.assertEqual(self.report["total_historical_events_tested"], 5)

    def test_peak_discharge_mape(self):
        # Mean Absolute Percentage Error for Peak Discharge must be under 15%
        mape = self.report["mean_absolute_percentage_error_q"]
        self.assertLess(mape, 15.0, f"MAPE {mape}% exceeds 15% threshold")

    def test_nash_sutcliffe_efficiency(self):
        # NSE must exceed 0.85 (excellent hydrologic model fit)
        nse = self.report["nash_sutcliffe_efficiency_nse"]
        self.assertGreater(nse, 0.85, f"NSE {nse} is below 0.85")

    def test_slope_failure_accuracy(self):
        # Geotechnical failure must be correctly detected for all historical mass movements
        accuracy = self.report["slope_failure_detection_accuracy_pct"]
        self.assertEqual(accuracy, 100.0)

    def test_flash_flood_alert_precision(self):
        # Red hazard alert precision must be 100%
        precision = self.report["flash_flood_alert_precision_pct"]
        self.assertEqual(precision, 100.0)

    def test_individual_events_bound(self):
        for ev in self.report["events"]:
            with self.subTest(event=ev["name"]):
                err = ev["metrics"]["relative_discharge_error_pct"]
                self.assertLess(err, 20.0, f"{ev['name']} error {err}% exceeds 20%")
                self.assertGreater(ev["predicted"]["flash_flood_probability_pct"], 75.0)

if __name__ == "__main__":
    unittest.main()
