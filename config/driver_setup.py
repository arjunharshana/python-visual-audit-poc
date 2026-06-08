from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def build_grid_driver():
    options = Options()
    # options.add_argument("-headless")
    
    print("Connecting to Docker Grid at localhost:4444...")
 
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    
    return driver