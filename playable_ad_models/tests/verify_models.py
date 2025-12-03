import sys
import time
import subprocess
from playwright.sync_api import sync_playwright

PORT = 8081

def verify_models():
    # Start server serving the current directory (repo root)
    server_process = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print(f"Server started at port {PORT}")
    time.sleep(2) # Wait for server to start

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # 1. Verify Arcelik Model
            print("Verifying Arcelik Model...")
            url = f"http://localhost:{PORT}/playable_ad_models/arcelik_model.html"
            page.goto(url)
            page.wait_for_selector("#header")
            header_text = page.text_content("#header")
            if "SENARYOYU EŞLEŞTİR" not in header_text:
                raise Exception(f"Arcelik header mismatch: {header_text}")
            page.screenshot(path="playable_ad_models/tests/arcelik_verify.png")
            print("Arcelik Model Verified.")

            # 2. Verify Parking Model
            print("Verifying Parking Model...")
            url = f"http://localhost:{PORT}/playable_ad_models/parking_model.html"
            page.goto(url)
            page.wait_for_selector("h1")
            title_text = page.text_content("h1")
            if "DRAG TO" not in title_text:
                raise Exception(f"Parking title mismatch: {title_text}")
            page.screenshot(path="playable_ad_models/tests/parking_verify.png")
            print("Parking Model Verified.")

            # 3. Verify Migros Model
            print("Verifying Migros Model...")
            url = f"http://localhost:{PORT}/playable_ad_models/migros_model.html"
            page.goto(url)
            page.wait_for_selector(".logo-text.logo-migros")
            migros_text = page.text_content(".logo-text.logo-migros")
            if "MIGROS" not in migros_text:
                raise Exception(f"Migros logo mismatch: {migros_text}")
            page.screenshot(path="playable_ad_models/tests/migros_verify.png")
            print("Migros Model Verified.")

            # 4. Verify Aksigorta Model
            print("Verifying Aksigorta Model...")
            url = f"http://localhost:{PORT}/playable_ad_models/aksigorta_model.html"
            page.goto(url)
            page.wait_for_selector("header")
            header_text = page.text_content("header")
            if "AKSIGORTA" not in header_text:
                raise Exception(f"Aksigorta header mismatch: {header_text}")

            # Verify canvas exists
            if not page.is_visible("#game-canvas"):
                 raise Exception("Game canvas not visible")

            page.screenshot(path="playable_ad_models/tests/aksigorta_verify.png")
            print("Aksigorta Model Verified.")

            browser.close()
            print("All models verified successfully.")

    except Exception as e:
        print(f"Verification failed: {e}")
        sys.exit(1)
    finally:
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    verify_models()
