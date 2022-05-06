import os
import platform
import re
import socket
import sys
from time import sleep

import pyautogui
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    InvalidArgumentException, SessionNotCreatedException
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
        return False


def check_presence_of_element_with_css_selector(chrome_browser, selector, time=15):
    print('check_presence_of_element_with_css_selector function entered')
    try:
        element = WebDriverWait(chrome_browser, time).until(
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
    import chromedriver_autoinstaller

    chromedriver_autoinstaller.install()
    # Register the driver
    try:
        chrome_browser = webdriver.Chrome()
    except InvalidArgumentException as ia:
        print("Please Close the previous Whatsapp web window.")

    return chrome_browser


def send_message(input_file_path, image_file_path, failed_file_path, message_template):
    chrome_browser = register_driver()
    chrome_browser.get('https://web.whatsapp.com/')

    qr_code = check_presence_of_element_with_css_selector(chrome_browser, '.NVQmc')

    retries = 0
    while qr_code is not None or retries <= 3:
        retries = retries + 1
        qr_code = check_presence_of_element_with_css_selector(chrome_browser, '.NVQmc')

    if qr_code is None:
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
                            success = True
                        except StaleElementReferenceException as se:
                            print('Stale element found, will find the user element again.')
                            user_element = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                       'span[title="{}"]'.format(
                                                                                           user_row[0]))
                            try:
                                user_element.click()
                                success = True
                            except StaleElementReferenceException as se:
                                success = False
                        else:
                            print('Successfully clicked user element.')
                    else:
                        # No user by the specified name in chat history
                        # So trying to create new chat
                        print(user_row[0] + ' not present in chat history.')
                        print('Loading the chat window using phone number.')
                        load_chat_with_phone_number(chrome_browser, user_row[1])
                        user_element = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                   'span[title="{}"]'.format(
                                                                                       user_row[0]))

                    if user_element is not None:
                        print('Chat window for ' + user_row[0] + ' opened successfully.')

                        if image_file_path is not None and success is True:
                            attach_files_button = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                              "#main > header > div._3nq_A > div > div:nth-child(2) > div")

                            if attach_files_button is not None:
                                try:
                                    attach_files_button.click()
                                    success = True
                                except Exception as e:
                                    print('Failed to click attach file button.')
                                    success = False
                                else:
                                    print('Successfully clicked attach file button.')
                            else:
                                print('Attach file Button not found.')
                                success = False

                            media_attachment = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                           "#main > header > div._3nq_A > div > div.PVMjB._4QpsN > span > div > div > ul > li:nth-child(1) > button")

                            if media_attachment is not None:
                                try:
                                    sleep(1)
                                    media_attachment.click()
                                    success = True
                                except Exception as e:
                                    print('Failed to click attach media file button.')
                                    success = False
                                else:
                                    print('Successfully clicked attach media file button.')
                            else:
                                print('Attach media file Button not found.')
                                success = False

                            sleep(1)
                            pyautogui.write(image_file_path)
                            pyautogui.press('enter')
                            sleep(2)

                            image = check_presence_of_element_with_css_selector(chrome_browser, '._2YWgP')

                            if image is None:
                                break
                            send_attachment_button = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                                 '._3y5oW._3qMYG')

                            if send_attachment_button is not None:
                                try:
                                    send_attachment_button.click()
                                    success = True
                                except Exception as e:
                                    print('Failed to find send attachment button.')
                                    success = False
                            else:
                                print('Send attachment Button not found.')
                                success = False

                        message_box = check_presence_of_element_with_css_selector(chrome_browser, '._2vJ01 ._3FRCZ')
                        message = message_template
                        if message_box is not None and success is True:
                            if "{}" in message_template:
                                message = message_template.format(user_row[0])
                            message_box.send_keys(message)

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
                        print('User loop exited\n\n')
                    else:
                        success = False
                        print(user_row[0] + ' not present in chat history.')

                    if success is False:
                        print('Writing failed users to csv.')
                        csv_writer.writerow([user_row[0], user_row[1]])
    else:
        return 8
    print(f'Processed {line_count - 1} lines. \n')
    chrome_browser.close()
    return 0


def get_absolute_path(file_name):
    cwd = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(cwd, file_name)


def validate_csv(input_file_path):
    valid = True
    error_line_count_list = []
    with open(input_file_path) as input_csv_file:
        csv_reader = csv.reader(input_csv_file, delimiter=',')
        line_count = 0
        for user_row in csv_reader:
            if line_count == 0:
                if len(user_row) < 2:
                    valid = False
            else:
                if len(user_row) < 2:
                    valid = False
                else:
                    if len(user_row[1]) == 10:
                        if not user_row[1].isdigit():
                            valid = False
                    elif len(user_row[1]) == 12:
                        if not user_row[1].isdigit():
                            valid = False
                        if not user_row[1].startswith("91"):
                            valid = False
                    elif len(user_row[1]) == 13:
                        if not user_row[1].isdigit():
                            valid = False
                        if not user_row[1].startswith("+91"):
                            valid = False
                    else:
                        valid = False
            line_count += 1
            if valid is False:
                error_line_count_list.append(line_count)
    return line_count, error_line_count_list


def main(input_file_path, image_file_path, failed_file_path, message_template):
    if not is_connected():
        return 5, []

    line_count, error_line_count_list = validate_csv(input_file_path)

    if line_count <= 1:
        return 7, []

    if len(error_line_count_list) > 0:
        return 6, error_line_count_list

    try:
        chrome_browser = register_driver()

    except SessionNotCreatedException as snce:
        print(
            'Please download the appropriate version of the chrome driver from '
            'https://chromedriver.chromium.org/downloads ')
        print('After downloading, place the file in the appropriate sub folder in the folder [chromedrivers].')
        return 1
    except Exception as e:
        print(str(e))
        return 2, []
    else:
        chrome_browser.close()

    if not path.exists(input_file_path):
        return 3, []

    if image_file_path is not None:
        if not path.exists(image_file_path):
            return 4, []

    if failed_file_path is None:
        failed_file_path = get_absolute_path("../failed.csv")

    status_code = send_message(input_file_path, image_file_path, failed_file_path, message_template)
    return status_code, []
