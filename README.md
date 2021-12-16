# 免责审明：仅供学习使用，使用本脚本的任何后果需使用者本人承担！

---
## Version2.2 更新：
新增验证码自动填写功能，通过tensorflow实现的图片识别，tensorflow源码放在CodeModel下，准确率不是最高，如果有替代方案，png2code函数已封装到config.py下，用户自行替换即可。

---
---
# Version2.2 使用教程更新

---
最新的python环境：
```python
python==3.7.9
selenium==3.141.0
pillow
tensorflow==2.3.0
```
---

## 2021.12.02 紧急通告

今日下午学校登录页面加入了验证码校验功能，体温登记脚本暂时失效，该问题正在紧急解决中。

## 2021.11.10 通告

目前的体温登记脚本仅支持内网访问，今日学校的vpn前端发生了更新，如果有外网访问需求的同学可以在issues里给我留言，我可以做一版外网也可自动体温登记的版本。

## Version2.1 更新：

新增提交状态校验功能，防止定位问题的发生。


## Version2.0 更新：

开学季倾情放送，更工整的代码、多用户配置、更安全稳定的自动体温登记脚本。
旧版代码迁移至Version1.0，配置方案参照旧版教程。
新版代码仅需配置config.py即可。


---
---
# Version2.0 使用教程

---

## 推荐的运行环境：

+ 同 Version1.0

Windows 10，并安装最新版本的chrome浏览器。经测试支持所有桌面级系统，需要寻找对应版本的chromedriver。

建议使用anaconda搭建虚拟的python环境。

```python
python==3.7.9
selenium==3.141.0
```

最新版本的chromedriver，覆盖原始项目下的chromedriver。最新版本的chromedriver地址http://chromedriver.storage.googleapis.com/index.html ，若地址失效请自行百度下载。

## 脚本使用方案

1、配置项目内的config.py文件。

```python
user_dict = {
    "*****": {  # 你的姓名（可随便填）
        "account": "**********",  # 你的校园网账号
        "password": "**********",  # 你的校园网密码
        "mail": "**********@**.com"  # 收件人 email address
    },
    # ......可以复制上述格式实现多用户登录
}

smtp_dict = {
    "from_name": "*****",  # 发件人姓名（可随便填）
    "from_address": "**********@**.com",  # 发件人 email address
    "from_password": "**********"  # email smtp password
}
```

2、运行此脚本，你将看到chrome自动化体温登记的全部流程。

```
python auto_temp.py
```

---

# Version1.0 使用教程

---

## 推荐的运行环境：

Windows 10，并安装最新版本的chrome浏览器。经测试支持所有桌面级系统，需要寻找对应版本的chromedriver。

建议使用anaconda搭建虚拟的python环境。

```python
python==3.7.9
selenium==3.141.0
```

最新版本的chromedriver，覆盖原始项目下的chromedriver。最新版本的chromedriver地址http://chromedriver.storage.googleapis.com/index.html ，若地址失效请自行百度下载。

## 脚本使用方案一（简易方案）：

如果您只是想确认脚本是否可用，可以采用本方案快速上手。

1、请先克隆/下载本项目（共计3个文件）至您的计算机。

2、您可以在任意python3.7环境下使用pip/conda指令安装selenium库。

```python
pip install selenium
```

3、请确保您计算机上的chrome与chromedriver都更新至最新的版本。

4、配置项目内的config文件中的username与password。

```
username=你的学号
password=校园网密码
temperature_up=36.9
temperature_down=36.1
is_mail=False
```

5、在命令行中定位至项目路径。

```
cd C:\Users\Automatic-temperature-registration-master
```

* 请注意更改项目路径。

6、运行此脚本，你将看到chrome自动化体温登记的全部流程。

```
python AutoTemp.py
```

脚本会以进程的方式持续运行，您将需要一台阿里云服务器或永不关机的计算机。

## 脚本使用方案二（完整功能）：

强烈推荐使用本方案运行脚本。在本方案下，您需要配置您的smtp邮箱授权码，每日的体温申报结果都会以邮件的形式反馈给您。在遇到某些奇妙的问题（例如网络波动/chromedriver版本过期）时，您也可以及时得到反馈并做出相应的处理。

有关什么是smtp授权码，可以访问https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256 。qq邮箱以外的讯息请自行查找。

1、搭建推荐的运行环境，或是实现方案一。

2、配置项目内的config文件，将is_mail设置为True开启smtp邮件功能。为了避免检查，config文件中可以自由的调整您体温的上下限，脚本会以随机数的形式提交您的体温。

```
username=你的学号
password=校园网密码
temperature_up=36.9
temperature_down=36.1
is_mail=True
```

3、配置AutoTemp.py中的sendmail函数，填写您的姓名，邮箱地址以及smtp授权码，qq邮箱以外的smtp服务器地址请自行搜索并修改。

```
def sendmail(text):
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "每日体温登记报告"
    msg['From'] = "your name"
    msg['To'] = "your name"
    from_addr = "*@qq.com"
    from_pwd = "********"
    to_addr = "*@qq.com"
    smtp_srv = "smtp.qq.com"
```

4、对于Windows用户，可以利用pyinstaller将本脚本打包成.exe可执行文件，将该可执行文件加入windows任务计划/开机自启动是一个十分便利的做法。对于Linux用户，也可以自行编写.sh脚本文件实现脚本自动运行的目的。



开源不易，如果该脚本对您有用，点亮一个星星是您对我最大的鼓励。如果您在使用脚本的过程中有任何问题或者是建议，欢迎在Issues中与我探讨。
