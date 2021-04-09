from selenium import webdriver
import os
import time
import random
import datetime
import smtplib
from email.mime.text import MIMEText


def sendmail(text):
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "每日体温登记报告"
    msg['From'] = "your name"
    msg['To'] = "your name"
    from_addr = "*@qq.com"
    from_pwd = "********"
    to_addr = "*@qq.com"
    smtp_srv = "smtp.qq.com"

    try:
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        srv.login(from_addr, from_pwd)
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        print('邮件发送成功')
        srv.quit()
    except Exception as e:
        print('邮件发送失败， ' + str(e))


def ReadConfig(configPath):
    configList = []

    f = open(configPath)
    for i in range(5):
        line = f.readline()
        line = line.replace("\n", "")
        configList.append(line)
    f.close()

    return configList


def Registration(webdriverPath, configPath, now_date, status):
    try:
        driver = webdriver.Chrome(webdriverPath)

        try:
            configList = ReadConfig(configPath)
        except Exception as e:
            print("config文件配置错误， " + str(e))
            return -1

        username = configList[0][9:]
        password = configList[1][9:]
        temperature_up = float(configList[2][15:])
        temperature_down = float(configList[3][17:])
        is_mail = configList[4][8:]

        tempstr = str(random.uniform(temperature_down, temperature_up))
        temperature = tempstr

        driver.get("https://workflow.sues.edu.cn/default/work/shgcd/jkxxcj/jkxxcj.jsp")
        login_username = driver.find_element_by_id("username")
        login_username.send_keys(username)
        login_password = driver.find_element_by_id("password")
        login_password.send_keys(password)
        time.sleep(2)

        login_button = driver.find_element_by_id("passbutton")
        login_button.click()
        time.sleep(2)

        temperature_text = driver.find_element_by_xpath('//*[@id="form"]/div[18]/div[1]/div/div[2]/div/div/input')
        temperature_text.clear()
        time.sleep(2)

        temperature_text.send_keys(temperature)
        time.sleep(2)

        submit_bottom = driver.find_element_by_id("post")
        submit_bottom.click()
        time.sleep(2)

        driver.quit()
        if status == 'm':
            open(str(now_date) + "m.txt", "w", encoding="utf-8")
            TextDetail = str(now_date) + '上午：体温登记成功！'
        elif status == 'a':
            open(str(now_date) + "a.txt", "w", encoding="utf-8")
            TextDetail = str(now_date) + '下午：体温登记成功！'
    except Exception as e:
        if status == 'm':
            TextDetail = str(now_date) + '上午：体温登记异常，请尽快处理！' + str(e)
        elif status == 'a':
            TextDetail = str(now_date) + '下午：体温登记异常，请尽快处理！' + str(e)

    if is_mail == "True":
        sendmail(TextDetail)
    else:
        print(TextDetail)


def main():
    Path = os.getcwd()
    webdriverPath = os.path.join(Path, "chromedriver.exe")
    configPath = os.path.join(Path, "config.txt")

    try_morning = 0
    try_afternoon = 0

    while True:
        now_date = datetime.datetime.now().strftime('%Y%m%d')
        now_hour = datetime.datetime.now().strftime('%H')

        if int(now_hour) < 8:
            try_morning = 0
            try_afternoon = 0
        elif int(now_hour) < 12:
            try_morning = try_morning + 1
            if try_morning == 1:
                Registration(webdriverPath, configPath, now_date, status='m')
            elif try_morning > 1:
                if os.path.isfile(str(now_date) + "m.txt"):
                    pass
                else:
                    Registration(webdriverPath, configPath, now_date, status='m')
        elif int(now_hour) < 13:
            pass
        elif int(now_hour) < 24:
            try_afternoon = try_afternoon + 1
            if try_afternoon == 1:
                Registration(webdriverPath, configPath, now_date, status='a')
            elif try_afternoon > 1:
                if os.path.isfile(str(now_date) + "a.txt"):
                    pass
                else:
                    Registration(webdriverPath, configPath, now_date, status='a')
        time.sleep(60 * 10)


if __name__ == '__main__':
    main()
