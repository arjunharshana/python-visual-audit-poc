import os
import sys
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.driver_setup import build_grid_driver

def setup_directory():
    """Creates a unique timestamped directory in the project root."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join(project_root, "test_runs", f"run_{timestamp}")
    
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def run_visual_audit():
    run_folder = setup_directory()
    print(f"Saving screenshots to: {run_folder}/")
    
    driver = build_grid_driver()
    wait = WebDriverWait(driver, 10)

    try:
        print("Navigating to target site...")
        driver.get('https://the-internet.herokuapp.com/login')
        driver.save_screenshot(os.path.join(run_folder, "01_initial_load.png"))
        
        print("Capturing Login Form Element...")
        login_form = wait.until(EC.presence_of_element_located((By.ID, "login")))
        login_form.screenshot(os.path.join(run_folder, "02_login_form_only.png"))
        
        print("Entering credentials...")
        driver.find_element(By.ID, 'username').send_keys('tomsmith')
        driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
        driver.save_screenshot(os.path.join(run_folder, "03_form_filled.png"))
        
        print("Clicking submit...")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Validate Success
        flash_banner = wait.until(EC.presence_of_element_located((By.ID, 'flash')))
        if "secure area" in flash_banner.text:
            print("Login Successful.")
            driver.save_screenshot(os.path.join(run_folder, "04_login_success.png"))
        else:
            print("Login Failed.")
            driver.save_screenshot(os.path.join(run_folder, "ERROR_login_failure.png"))

    except Exception as e:
        print(f"Test crashed: {e}")
        driver.save_screenshot(os.path.join(run_folder, "CRASH_STATE.png"))
        
    finally:
        print("Tearing down Grid Node connection.")
        driver.quit()

if __name__ == "__main__":
    run_visual_audit()