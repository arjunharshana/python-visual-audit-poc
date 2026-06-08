import os
import sys
import pytest
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.driver_setup import build_grid_driver

def setup_directory(user_id):
    """Creates a unique directory for EACH concurrent user to prevent overwriting."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join(project_root, "test_runs", f"run_{timestamp}_user_{user_id}")
    
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Each test run will be executed with a different user_id (1 to 5) to ensure unique folders for screenshots
@pytest.mark.parametrize("user_id", range(1, 6))
def test_visual_audit_load(user_id):
    run_folder = setup_directory(user_id)
    video_name = f"User_{user_id}_Login_Test"

    driver = build_grid_driver(session_name=video_name)
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get('https://the-internet.herokuapp.com/login')
        driver.save_screenshot(os.path.join(run_folder, "01_initial_load.png"))
        
        login_form = wait.until(EC.presence_of_element_located((By.ID, "login")))
        login_form.screenshot(os.path.join(run_folder, "02_login_form_only.png"))
        
        driver.find_element(By.ID, 'username').send_keys('tomsmith')
        driver.find_element(By.ID, 'password').send_keys('SuperSecretPassword!')
        driver.save_screenshot(os.path.join(run_folder, "03_form_filled.png"))
        
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        flash_banner = wait.until(EC.presence_of_element_located((By.ID, 'flash')))
        if "secure area" in flash_banner.text:
            driver.save_screenshot(os.path.join(run_folder, "04_login_success.png"))
            assert True 
        else:
            driver.save_screenshot(os.path.join(run_folder, "ERROR_login_failure.png"))
            assert False, "Login failed validation"

    except Exception as e:
        driver.save_screenshot(os.path.join(run_folder, "CRASH_STATE.png"))
        raise e
        
    finally:
        driver.quit()