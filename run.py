import os
import socket
from time import sleep

import pyautogui
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, \
    InvalidArgumentException
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
    try:
        chrome_browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver',
                                          options=options)
    except InvalidArgumentException as ia:
        print("Please Close the previous Whatsapp web window.")

    return chrome_browser

JS_DROP_FILES = "var c=arguments,b=c[0],k=c[1];c=c[2];for(var d=b.ownerDocument||document,l=0;;){var e=b.getBoundingClientRect(),g=e.left+(k||e.width/2),h=e.top+(c||e.height/2),f=d.elementFromPoint(g,h);if(f&&b.contains(f))break;if(1<++l)throw b=Error('Element not interactable'),b.code=15,b;b.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var a=d.createElement('INPUT');a.setAttribute('type','file');a.setAttribute('multiple','');a.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');a.onchange=function(b){a.parentElement.removeChild(a);b.stopPropagation();var c={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:a.files,setData:function(){},getData:function(){},clearData:function(){},setDragImage:function(){}};window.DataTransferItemList&&(c.items=Object.setPrototypeOf(Array.prototype.map.call(a.files,function(a){return{constructor:DataTransferItem,kind:'file',type:a.type,getAsFile:function(){return a},getAsString:function(b){var c=new FileReader;c.onload=function(a){b(a.target.result)};c.readAsText(a)}}}),{constructor:DataTransferItemList,add:function(){},clear:function(){},remove:function(){}}));['dragenter','dragover','drop'].forEach(function(a){var b=d.createEvent('DragEvent');b.initMouseEvent(a,!0,!0,d.defaultView,0,0,0,g,h,!1,!1,!1,!1,0,null);Object.setPrototypeOf(b,null);b.dataTransfer=c;Object.setPrototypeOf(b,DragEvent.prototype);f.dispatchEvent(b)})};d.documentElement.appendChild(a);a.getBoundingClientRect();return a;"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []

    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]):
        if not os.path.isfile(file):
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))

    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})


WebElement.drop_files = drop_files


def send_message(input_file_path, failed_file_path, message_template):
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
                            break
                    else:
                        print('Successfully clicked user element.')
                else:
                    # No user by the specified name in chat history
                    # So trying to create new chat
                    print(user_row[0] + ' not present in chat history.')
                    print('Loading the chat window using phone number.')
                    load_chat_with_phone_number(chrome_browser, user_row[1])

                print('Chat window for ' + user_row[0] + ' opened successfully.')

                attach_files_button = check_presence_of_element_with_css_selector(chrome_browser,
                                                                                  "#main > header > div._3nq_A > div > div:nth-child(2) > div")

                if attach_files_button is not None:
                    try:
                        attach_files_button.click()
                    except Exception as e:
                        print('Failed to click attach file button.')
                        success = False
                        break
                    else:
                        print('Successfully clicked attach file button.')
                else:
                    print('Attach file Button not found.')
                    success = False
                    break

                media_attachment = check_presence_of_element_with_css_selector(chrome_browser,
                                                                               "#main > header > div._3nq_A > div > div.PVMjB._4QpsN > span > div > div > ul > li:nth-child(1) > button")

                if media_attachment is not None:
                    try:
                        sleep(1)
                        media_attachment.click()
                    except Exception as e:
                        print('Failed to click attach media file button.')
                        success = False
                        break
                    else:
                        print('Successfully clicked attach media file button.')
                else:
                    print('Attach media file Button not found.')
                    success = False
                    break

                sleep(1)
                cwd = os.path.dirname(os.path.abspath(__file__))
                pyautogui.write(cwd + "/a.jpg")
                pyautogui.press('enter')
                sleep(2)

                send_attachment_button = check_presence_of_element_with_css_selector(chrome_browser, '._3y5oW._3qMYG')

                if send_attachment_button is not None:
                    try:
                        send_attachment_button.click()
                    except Exception as e:
                        print('Failed to find send attachment button.')
                        success = False
                else:
                    print('Send attachment Button not found.')
                    success = False


                message_box = check_presence_of_element_with_css_selector(chrome_browser, '._2vJ01 ._3FRCZ')

                if message_box is not None:
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
                print('User loop exited/n/n')
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

        message_template = input(
            "Enter the message to be sent ( please enter {} where you need to edit in the customer name provided in "
            "the CSV) : ")

        send_message(input_file_path, failed_file_path, message_template)
    else:
        print("File not found")
