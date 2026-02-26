from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def log_user_in(driver):
    driver.get('https://pinterest.com/')
    input('Please log in and press Enter to continue')
    user_url = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Your profile"]').get_attribute('href')
    driver.get(user_url)
    sleep(5) # Wait for the page to load

def get_boards(driver):
    board_html_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pwt-grid-item"]')
    board_links = []
    for board in board_html_elements:
        board_links.append(board.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    return board_links

    
def main():
    print("Opening web driver. Please wait.")
    driver = webdriver.Firefox()
    log_user_in(driver)
    board_urls = get_boards(driver)

    driver.close()

if __name__ == '__main__':
    main()