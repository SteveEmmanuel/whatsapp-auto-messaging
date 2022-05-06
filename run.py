import sys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def find_contact_from_new_chat(user_name):
    pass
    # TODO implement finding contact from new chat


def check_presence_of_element_with_css_selector(driver, selector):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    except NoSuchElementException as se:
        print("No element found with selector " + selector)
        return None
    else:
        return element


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=<User Data Path>')
    options.add_argument('--profile-directory=Default')

    # Register the drive
    chrome_browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver',
                                      options=options)  # Change the path as per your local dir.
    chrome_browser.get('https://web.whatsapp.com/')

    user_name_list = ['Kiran Benny']

    for user_name in user_name_list:

        user = check_presence_of_element_with_css_selector(chrome_browser, 'span[title="{}"]'.format(user_name))
        if user is not None:
            user.click()

            message_box = check_presence_of_element_with_css_selector(chrome_browser, '._2vJ01 ._3FRCZ')
            if message_box is not None:
                message_box.send_keys('hey')

                send_button = check_presence_of_element_with_css_selector(chrome_browser, '._1U1xa')
                # Click on send button
                if send_button is not None:
                    send_button.click()
        else:
            # No user by the specified name in chat history
            # So looking in create new chat
            find_contact_from_new_chat(user_name)

    chrome_browser.close()
