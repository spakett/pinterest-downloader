from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep


def log_user_in(driver):
    driver.get('https://pinterest.com/')
    input('Please log in and press Enter to continue.')
    user_url = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Your profile"]').get_attribute('href')
    driver.get(user_url)
    sleep(3) # Wait for the page to load


def get_board_urls(driver):
    board_html_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pwt-grid-item"]')
    board_urls = []

    for board in board_html_elements:
        board_urls.append(board.find_element(By.TAG_NAME, 'a').get_attribute('href'))

    return board_urls


def get_pins_from_board(driver):
    board_name = driver.find_element(By.CSS_SELECTOR, '[id="board-name"]').text
    pin_count = int(driver.find_element(By.CSS_SELECTOR, '[data-test-id="pin-count"]').text.split()[0])
    
    if not pin_count:
        print(f'Board "{board_name}" contains no pins.')
        return []
    
    # TODO: Sections break the current logic. Search for sections and process them before processing the main board. 
    
    print(f'Now processing board "{board_name}" with {pin_count} pins.')

    pins_metadata = {} # Structure {pin_id: (href, is_removed)}
    highest_encountered_idx = -1

    while highest_encountered_idx < (pin_count - 1):
        pin_html_elements = driver.find_elements(By.CSS_SELECTOR, '[data-test-id="pin"]')
        for pin in pin_html_elements:
            pin_idx = int(pin.get_attribute('data-test-pin-slot-index'))
            highest_encountered_idx = pin_idx if pin_idx > highest_encountered_idx else highest_encountered_idx
            if pin_idx not in pins_metadata.keys():
                pin_href = pin.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # Information about the pin being unavailable is located in a child element
                is_pin_unavailable = False
                try:
                    pin.find_element(By.CSS_SELECTOR, '[data-test-id="unavailable-pin"]')
                    is_pin_unavailable = True
                except NoSuchElementException:
                    pass

                pins_metadata[pin_idx] = [pin_href, board_name, is_pin_unavailable]
        
        # Scroll down and wait for new pins to load
        driver.execute_script('window.scrollBy(0, 250);')
        sleep(1)

        print(f'{len(pins_metadata.keys())} of {pin_count} pins have been processed.')
    print(f'All pins from board {board_name} processed - moving onto the next board.')

    # The pin index is no longer needed
    return pins_metadata.values()


def main():
    print("Opening web driver. Please wait.")
    driver = webdriver.Firefox()
    log_user_in(driver)
    board_urls = get_board_urls(driver)

    pins_metadata = []
    for url in board_urls:
        driver.get(url)
        sleep(3) # Wait for the page to load
        pins_metadata += get_pins_from_board(driver)

    driver.close()


if __name__ == '__main__':
    main()