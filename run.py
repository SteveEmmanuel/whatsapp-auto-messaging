import os
import socket
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
from os import path


def load_chat_with_phone_number(chrome_browser, phone_number):
    chrome_browser.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_number))


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        is_connected()


def check_presence_of_element_with_css_selector(chrome_browser, selector):
    print('check_presence_of_element_with_css_selector function entered')
    try:
        element = WebDriverWait(chrome_browser, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    except NoSuchElementException as se:
        # print("No element found with selector " + selector)
        print('NoSuchElementException ' + selector)
        return None
    except TimeoutException as te:
        # print("No element found with selector " + selector)
        print('TimeoutException ' + selector)
        chrome_browser.get('https://web.whatsapp.com/')
        return None
    else:
        print('Successfully obtained user element ' + selector)
        return element


def register_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=User Data')
    options.add_argument('--profile-directory=Default')

    # Register the drive
    chrome_browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver',
                                      options=options)

    return chrome_browser


def send_message(input_file_path, failed_file_path):
    chrome_browser = register_driver()

    chrome_browser.get('https://web.whatsapp.com/')
    with open(input_file_path) as input_csv_file, open(failed_file_path, 'w', newline='') as failed_csv_file:
        csv_reader = csv.reader(input_csv_file, delimiter=',')

        csv_writer = csv.writer(failed_csv_file, delimiter=',')
        csv_writer.writerow(['Name', 'Phone Number'])

        line_count = 0
        for user_row in csv_reader:
            success = True
            if line_count == 0:
                print(f'Column names are {", ".join(user_row)}')
                line_count += 1
            else:
                print(f'User by the name {user_row[0]} with phone number {user_row[1]}.')
                line_count += 1
                print('User loop entered')
                user_element = check_presence_of_element_with_css_selector(chrome_browser,
                                                                           'span[title="{}"]'.format(user_row[0]))
                print('User presence checked')
                if user_element is not None:
                    print(user_row[0] + ' present, trying to click')
                    try:
                        user_element.click()
                    except StaleElementReferenceException as se:
                        print('Stale element found, will find the user element again.')
                        user_element = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                   'span[title="{}"]'.format(
                                                                                       user_row[0]))
                        try:
                            user_element.click()
                        except StaleElementReferenceException as se:
                            success = False
                else:
                    # No user by the specified name in chat history
                    # So trying to create new chat
                    print(user_row[0] + ' not present in chat history.')
                    print('Loading the chat window using phone number.')
                    load_chat_with_phone_number(chrome_browser, user_row[1])

                message_box = check_presence_of_element_with_css_selector(chrome_browser, '._2vJ01 ._3FRCZ')
                if message_box is not None:
                    message_box.send_keys('hey')

                    send_button = check_presence_of_element_with_css_selector(chrome_browser, '._1U1xa')
                    # Click on send button
                    if send_button is not None:
                        try:
                            send_button.click()
                        except Exception as e:
                            print('Failed to send message.')
                            success = False
                    else:
                        print('Send Button not found.')
                        success = False
                else:
                    print('Message Box not found.')
                    success = False
                print('User loop exited')
            if success is False:
                csv_writer.writerow([user_row[0], user_row[1]])
    print(f'Processed {line_count - 1} lines. \n')
    chrome_browser.close()


if __name__ == '__main__':
    input_file_name = input("Enter the name of the file : ")

    cwd = os.path.dirname(os.path.abspath(__file__))
    input_file_path = cwd + "/" + input_file_name
    if path.exists(input_file_path):
        failed_file_name = input("Enter the name of the file to which failed user details are to be saved : ")
        failed_file_path = cwd + "/" + failed_file_name
        send_message(input_file_path, failed_file_path)
    else:
        print("File not found")
