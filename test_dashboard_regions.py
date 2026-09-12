import time
import subprocess
import requests
from playwright.sync_api import sync_playwright

def run_test():
    print("Starting fresh Flask server...")
    proc = subprocess.Popen(["python", "app.py"])
    
    # Wait for server to start
    for _ in range(25):
        try:
            r = requests.get("http://127.0.0.1:5000/api/regions", timeout=1)
            if r.status_code == 200:
                print("Server is live with /api/regions!")
                break
        except Exception:
            time.sleep(0.4)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1500, "height": 950})

        print("Navigating to dashboard...")
        page.goto("http://127.0.0.1:5000/")
        page.wait_for_timeout(2000)

        # 1. Alaknanda (Chamoli) Baseline
        page.screenshot(path="region_alaknanda_chamoli.png")
        print("Captured region_alaknanda_chamoli.png")

        # 2. Switch to Mandakini (Kedarnath)
        print("Switching basin to Mandakini (Kedarnath)...")
        page.select_option("#select-himalayan-basin", "mandakini")
        page.wait_for_timeout(1500)
        basin_text = page.inner_text("#ribbon-basin-name")
        print(f"Active Basin: {basin_text}")
        page.screenshot(path="region_mandakini_kedarnath.png")
        print("Captured region_mandakini_kedarnath.png")

        # 3. Switch to Bhagirathi (Uttarkashi)
        print("Switching basin to Bhagirathi (Uttarkashi)...")
        page.select_option("#select-himalayan-basin", "bhagirathi")
        page.wait_for_timeout(1500)
        basin_text = page.inner_text("#ribbon-basin-name")
        print(f"Active Basin: {basin_text}")
        page.screenshot(path="region_bhagirathi_uttarkashi.png")
        print("Captured region_bhagirathi_uttarkashi.png")

        # 4. Test Lead Time Horizon Switching (180 min nowcast horizon)
        print("Testing 180 min Horizon switch...")
        page.click("#btn-horizon-180")
        page.wait_for_timeout(1000)
        clock_text = page.inner_text("#clock-lead-time")
        print(f"Lead time clock under 180m Horizon: {clock_text}")
        page.screenshot(path="horizon_180min_watch.png")
        print("Captured horizon_180min_watch.png")

        browser.close()

    if proc:
        proc.terminate()
    print("Multi-region tests finished successfully!")

if __name__ == "__main__":
    run_test()
