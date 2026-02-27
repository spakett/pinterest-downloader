from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

def log_user_in(driver):
    driver.get('https://pinterest.com/')
    input('Please log in and press Enter to continue.')
    user_url = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Your profile"]').get_attribute('href')
    driver.get(user_url)
    sleep(3) # Wait for the page to load

def get_boards(driver):
    board_html_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pwt-grid-item"]')
    board_links = []
    for board in board_html_elements:
        board_links.append(board.find_element(By.TAG_NAME, 'a').get_attribute('href'))
    return board_links

def get_pins_from_board(driver):
    
    board_name = driver.find_element(By.CSS_SELECTOR, '[id="board-name"]').text
    pin_count = int(driver.find_element(By.CSS_SELECTOR, '[data-test-id="pin-count"]').text.split()[0])
    removed_pin_count = len(driver.find_elements(By.CSS_SELECTOR, '[data-test-id="unavailable-pin"]'))
    
    if not pin_count:
        print(f'Board "{board_name}" contains no pins.')
        return {}
    
    print(f'Now processing board "{board_name}" with {pin_count} pins.')

    pins_metadata = {} # Structure {pin_id: (href, is_removed)}
    highest_encountered_idx = -1

    while highest_encountered_idx < pin_count:
        pin_html_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pin"]')
        for pin in pin_html_elements:
            pin_idx = int(pin.get_attribute('data-test-pin-slot-index'))
            highest_encountered_idx = pin_idx if pin_idx > highest_encountered_idx else highest_encountered_idx
            if pin_idx not in pins_metadata.keys():
                pin_href = pin.find_element(By.TAG_NAME, 'a').get_attribute('href')
                is_pin_unavailable = False
                if len(pin.find_element(By.CSS_SELECTOR, '[data-test-id="unavailable-pin"]')):
                    is_pin_unavailable = True
                pins_metadata[pin_idx] = [pin_href, is_pin_unavailable]

def main():
    print("Opening web driver. Please wait.")
    driver = webdriver.Firefox()
    log_user_in(driver)
    board_urls = get_boards(driver)

    for url in board_urls:
        driver.get(url)
        sleep(3) # Wait for the page to load
        get_pins_from_board(driver)
        break

    driver.close()

if __name__ == '__main__':
    main()