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

        try:
            # Select the user in the chat history with the specified name
            user = WebDriverWait(chrome_browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[title="{}"]'.format(user_name)))
            )
        except NoSuchElementException as se:
            # No user by the specified name in chat history
            # So looking in create new chat
            find_contact_from_new_chat(user_name)
        else:
            user.click()

            # Typing message into message box
            try:
                message_box = WebDriverWait(chrome_browser, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '._2vJ01 ._3FRCZ'))
                )
            except Exception as e:
                print(e)
            else:
                message_box.send_keys('hey')

                # Click on send button
                try:
                    send_button = WebDriverWait(chrome_browser, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '._1U1xa'))
                    )
                except Exception as e:
                    print(e)
                else:
                    send_button.click()

    chrome_browser.close()
