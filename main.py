# https://chromedriver.storage.googleapis.com/index.html?path=96.0.4664.45/

from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import NoSuchElementException

import undetected_chromedriver.v2 as uc

def main(numbers):
    path = '/home/sawradip/Desktop/practice_python/checkMail/chromedriver'
    # s= Service(path)
    # driver = webdriver.Chrome(service = s)
    # driver = uc.Chrome()

    options = uc.ChromeOptions()
    # options.add_argument('disable-logging')
    options.add_argument('--log-level=3')
    driver = uc.Chrome(executable_path=path,  options=options)
    gmail_signin_page = r"https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
    driver.get(gmail_signin_page)
    driver.implicitly_wait(15)

    results = []

    for number in numbers:
        input_box = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        driver.implicitly_wait(15)
        length = len(input_box.get_attribute('value'))
        input_box.send_keys(length * Keys.BACKSPACE)
        input_box.send_keys(number)

        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

        driver.implicitly_wait(3)
        try:
            driver.find_element(By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[2]/div[2]/div')
            results.append('No Gmail associated')
        except NoSuchElementException:
            time.sleep(1)
            driver.execute_script ("window.history.go (-1)")
            time.sleep(1)
            results.append('Found associated Gmail.')
            
        time.sleep(1)
    driver.quit()

    return results

def sanity_check(number):
    number = number.strip()

    if len(number) == 11:
        number = '+88' + number
    elif len(number) == 14 and number.startswith('+88'):
        number = number
    else:
        print("BD phone number must be 0f 11 digits or should be provided with country code '+88'")
        return None
    return number



if __name__ == "__main__":

    import os
    import pickle 
    from datetime import datetime, timedelta

    license_path = './license.dat'
    admin_current_pass = "myadmin"

    while True:
        user_input = input("Enter command [check/admin/quit]: ")

        if user_input == 'quit':
            break

        elif user_input == 'admin':

            admin_pass = input("Enter admin password: ")
            if admin_pass == admin_current_pass:
                admin_command = input("Enter admin command[set_license]: ")

                if admin_command == "set_license":
                    if os.path.exists(license_path):
                        os.remove(license_path)
                    n_days = int(input("Enter number of days you want to add license for: "))

                    current_datetime = datetime.now()
                    days_to_add = timedelta(days = n_days)
                    license_expire_datetime = current_datetime + days_to_add

                    with open(license_path, 'wb') as license_file:
                        pickle.dump(license_expire_datetime, license_file)
                        print(f'License activated until {license_expire_datetime}')

                else:
                    print("Invalid command! Try Again.")
                    continue

            else:
                print("Incorrect Password! Try Again.")

        elif user_input == 'check':
            if os.path.exists(license_path):
                with open(license_path,'rb') as license_file:
                    license_expire_datetime = pickle.load(license_file)
                current_datetime = datetime.now()
                if license_expire_datetime > current_datetime:
                    print(f"You have lisence remaining for {license_expire_datetime - current_datetime}")
                else:
                    print(f"Your License is expired. Please contact the admin.")
                    continue
            else:
                print("License file doesn't exist. Please contact the admin.")
                continue
            
            
            user_command = input("Enter your choice [phone_number/txt_path]:")
            if user_command == "phone_number":
                number = sanity_check(input("Enter BD Phone number:"))
                if number is None:
                    continue
                else:
                    numbers = [number]
                    results = main(numbers)

                    print('\n' + '-'*25 + '\n' + '-'*25 + '\n')
                    for num, res in zip(numbers, results):
                        num = num[:-1]
                        print ( f'{num} ---> {res}')
                    print('\n' + '-'*25 + '\n' + '-'*25 + '\n')

            elif user_command == "txt_path":
                txt_path = input('Enter txt file path containing phone numbers:')

                with open(txt_path,"r") as file:
                    numbers = file.readlines()
                sane_numbers = [sanity_check(number) for number in numbers]
                results = main(sane_numbers)

                print('\n' + '-'*25 + '\n' + '-'*25 + '\n')
                for num, res in zip(numbers, results):
                    num = num[:-1]
                    print ( f'{num} ---> {res}')
                print('\n' + '-'*25 + '\n' + '-'*25 + '\n')

            else:
                print("Invalid Command! Try Again.")
                continue
        else:
            print("Invalid Command! Try Again.")
            continue

    # txt_path = 'habijabi/num.txt'

    # with open(txt_path,"r") as file:
    #     numbers = file.readlines()
    # sane_numbers = [sanity_check(number) for number in numbers]
    # results = main(sane_numbers)

    # print('\n' + '-'*25 + '\n' + '-'*25 + '\n')
    # for num, res in zip(numbers, results):
    #     num = num[:-1]
    #     print ( f'{num} ---> {res}')
    # print('\n' + '-'*25 + '\n' + '-'*25 + '\n')