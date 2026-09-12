import time
from playwright.sync_api import sync_playwright

def test_multitier_and_iot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1600, "height": 1050})
        page = context.new_page()

        print("Navigating to PRAVAH AI...")
        page.goto("http://127.0.0.1:5000")
        page.wait_for_selector(".multitier-leadtime-bar", timeout=10000)
        time.sleep(2)

        # 1. Verify Multi-Tier Lead Time Widget
        clock_text = page.locator("#countdown-clock").inner_text()
        print("Composite Evacuation Countdown:", clock_text)
        assert "MIN" in clock_text, f"Expected MIN in countdown clock, got {clock_text}"

        t1_val = page.locator("#tier1-val").inner_text()
        t2_val = page.locator("#tier2-val").inner_text()
        t3_val = page.locator("#tier3-val").inner_text()
        print(f"Tiers: Tier 1={t1_val}, Tier 2={t2_val}, Tier 3={t3_val}")

        # 2. Verify PGNN Machine Learning Concordance
        physics_pct = page.locator("#pgnn-physics-pct").inner_text()
        ml_pct = page.locator("#pgnn-ml-pct").inner_text()
        fused_pct = page.locator("#pgnn-fused-pct").inner_text()
        concordance = page.locator("#pgnn-concordance-badge").inner_text()
        print(f"PGNN AI: Physics={physics_pct}, ML={ml_pct}, Fused={fused_pct}")
        print("Concordance Badge:", concordance)

        page.screenshot(path="multitier_leadtime_dashboard.png")
        print("Screenshot saved: multitier_leadtime_dashboard.png")

        # 3. Test Live IoT Stream Toggle
        print("Toggling Live IoT Stream...")
        page.click("#btn-toggle-iot-stream")
        time.sleep(4) # Wait for live tick

        btn_text = page.locator("#iot-btn-text").inner_text()
        print("IoT Button State after click:", btn_text.encode("ascii", "ignore").decode())
        assert "Stop Live Feed" in btn_text, f"Expected Stop Live Feed, got {btn_text}"

        page.screenshot(path="live_iot_feed_active.png")
        print("Screenshot saved: live_iot_feed_active.png")

        # 4. Test IoT Sensors Network Modal
        print("Opening IoT Sensors Modal...")
        page.click(".iot-sensors-btn")
        page.wait_for_selector("#iotSensorsModal.active", timeout=5000)
        time.sleep(1.5)

        cards = page.locator(".iot-station-card").count()
        print(f"Rendered IoT Station Cards: {cards}")
        assert cards >= 3, f"Expected at least 3 station cards, found {cards}"

        peak_rain = page.locator("#iot-modal-peak-rain").inner_text()
        mean_moist = page.locator("#iot-modal-mean-moist").inner_text()
        print(f"Modal Telemetry Summary: Peak Rain={peak_rain}, Mean Moisture={mean_moist}")

        page.screenshot(path="iot_sensors_modal.png")
        print("Screenshot saved: iot_sensors_modal.png")

        browser.close()
        print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test_multitier_and_iot()
