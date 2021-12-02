from selenium import webdriver
import os
import time
import json
import random
import datetime
import smtplib
from email.mime.text import MIMEText

import config
from config import user_dict, smtp_dict, png2code
import threading


def get_now_time():
    return time.strftime('%Y%m%d %H.%M.%S', time.localtime())


def sendmail(text, to_address, to_name):
    message = MIMEText(text, "plain", "utf-8")
    message['Subject'] = "每日体温登记报告"
    message['From'] = smtp_dict["from_name"]
    message['To'] = to_name
    from_address = smtp_dict["from_address"]
    from_password = smtp_dict["from_password"]
    smtp_service = "smtp.qq.com"

    now_time = get_now_time()
    try:
        service = smtplib.SMTP_SSL(smtp_service.encode(), 465)
        service.login(from_address, from_password)
        service.sendmail(from_address, [to_address], message.as_string())
        service.quit()
    except Exception as e:
        print(now_time + str(e))


def chrome_submit(username, password):
    webdriver_path = os.path.join(os.getcwd(), "chromedriver.exe")
    driver = webdriver.Chrome(webdriver_path)
    temperature = str(random.uniform(float(36.1), float(36.9)))

    driver.get("https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp")

    flag = False
    for _ in range(10):
        if flag:
            break

        login_username = driver.find_element_by_id("username")
        login_username.send_keys(username)
        login_password = driver.find_element_by_id("password")
        login_password.send_keys(password)
        time.sleep(2)

        code_png = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div/div[1]/div/div/form[1]/div[4]/img")
        code_png.screenshot('codeImg.png')

        my_code = config.png2code()

        login_code = driver.find_element_by_id("authcode")
        login_code.send_keys(my_code)
        time.sleep(2)

        login_button = driver.find_element_by_id("passbutton")
        login_button.click()
        time.sleep(2)

        try:
            temperature_text = driver.find_element_by_xpath('//*[@id="form"]/div[18]/div[1]/div/div[2]/div/div/input')
            temperature_text.clear()
            time.sleep(2)

            temperature_text.send_keys(temperature)
            time.sleep(2)
            flag = True
        except Exception as e:
            print(f"验证码错误： {e}")

    submit_bottom = driver.find_element_by_id("post")
    submit_bottom.click()
    time.sleep(10)

    return_text = driver.find_element_by_xpath('/html/body/div[3]/div[2]').text
    driver.quit()

    if return_text != "健康填报成功":
        raise Exception(f"Wrong return {return_text}.")


def check_log(now_data, morning_or_afternoon):
    status_dict = {}
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            status_dict = json.load(f)
    except Exception as e:
        print(e)

    if now_data + morning_or_afternoon in status_dict.keys():
        if status_dict[now_data + morning_or_afternoon] == "正常":
            return True

    return False


def write_log(now_data, morning_or_afternoon, status):
    status_dict = {}
    try:
        with open("log.txt", "r", encoding="utf-8") as f:
            status_dict = json.load(f)
    except Exception as e:
        print(e)

    status_dict[now_data + morning_or_afternoon] = status

    with open("log.txt", "w", encoding="utf-8") as f:
        json_object = json.dumps(status_dict, indent=4, ensure_ascii=False)
        f.write(json_object)


def submit_temperature():
    while True:
        now_date = datetime.datetime.now().strftime('%Y%m%d')
        now_hour = datetime.datetime.now().strftime('%H')

        if 7 <= int(now_hour) <= 12:
            if not check_log(str(now_date), "上午"):
                try:
                    for user_name, user_details in user_dict.items():
                        chrome_submit(user_details["account"], user_details["password"])

                    write_log(str(now_date), "上午", "正常")
                    text = str(now_date) + '上午：体温登记成功！'
                except Exception as e:
                    print(e)
                    write_log(str(now_date), "上午", "异常")
                    text = str(now_date) + '上午：体温登记异常，请尽快处理！' + str(e)

                for user_name, user_details in user_dict.items():
                    sendmail(text, to_address=user_details["mail"], to_name=user_name)

        elif 13 <= int(now_hour) < 24:
            if not check_log(str(now_date), "下午"):
                try:
                    for user_name, user_details in user_dict.items():
                        chrome_submit(user_details["account"], user_details["password"])

                    write_log(str(now_date), "下午", "正常")
                    text = str(now_date) + '下午：体温登记成功！'
                except Exception as e:
                    print(e)
                    write_log(str(now_date), "下午", "异常")
                    text = str(now_date) + '下午：体温登记异常，请尽快处理！' + str(e)

                for user_name, user_details in user_dict.items():
                    sendmail(text, to_address=user_details["mail"], to_name=user_name)

        time.sleep(60 * 9)


def email_check():
    while True:
        now_date = datetime.datetime.now().strftime('%Y%m%d')
        now_hour = datetime.datetime.now().strftime('%H')

        if 8 <= int(now_hour) <= 12:
            if not check_log(str(now_date), "上午"):
                text = str(now_date) + '上午：体温登记巡查线程发现异常，请立刻通知管理员！！！'

                for user_name, user_details in user_dict.items():
                    sendmail(text, to_address=user_details["mail"], to_name=user_name)

        elif 14 <= int(now_hour) < 24:
            if not check_log(str(now_date), "下午"):
                text = str(now_date) + '下午：体温登记巡查线程发现异常，请立刻通知管理员！！！'

                for user_name, user_details in user_dict.items():
                    sendmail(text, to_address=user_details["mail"], to_name=user_name)

        time.sleep(60 * 5)


if __name__ == '__main__':
    t1 = threading.Thread(target=submit_temperature)
    t2 = threading.Thread(target=email_check)
    t1.start()
    t2.start()
