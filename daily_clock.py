import smtplib
from email.header import Header
from email.mime.text import MIMEText
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

"""
用户的基本信息:账号、密码、qq邮箱、
打卡情况：成功、异常
"""
user_names = ['********']
pass_words = ['********']
user_mails = ['********']
successes = [0] * len(user_names)
fails = [1] * len(user_names)


def visual_free_interface():
    """
    功能：实现无可视化界面的操作和规避检测
    """
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--hide-scrollbars')
    options.add_argument('blink-settings=imagesEnabled=false')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    return options

def send_emails(index, content):
    """
    功能：向用户发邮件汇报打卡情况
    """
    mail_host = 'smtp.qq.com'
    mail_user = user_mails[index]
    mail_pass = 'knkagtmgnwmzdhhg'
    sender = user_mails[index]
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header('Daily Health Report', 'utf-8')
    message['From'] = Header('Catcher', 'utf-8')
    try:
        smtp = smtplib.SMTP_SSL(mail_host)
        smtp.login(mail_user, mail_pass)
        smtp.sendmail(sender, user_mails[index], message.as_string())
        print('************ 邮件已发送 ************')
    except smtplib.SMTPException:
        print('************ Error: 邮件发送失败 ! ************')
    return


def daily_health_report():
    """
    功能：实现每日定时健康打卡，并将打卡结果反馈用户
    """
    result_list = []
    for i in range(len(user_names)):
        # noinspection PyBroadException
        try:
            # 获取登陆界面，并为网页预留 2s 加载时间
            options = visual_free_interface()
            bro = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=options)
            bro.get('https://ids.xmu.edu.cn/authserver/login?service=https://xmuxg.xmu.edu.cn/login/cas/xmu')
            sleep(2)

            # 通过用户名和密码进行登录
            user_name = bro.find_element_by_id('username')
            pass_word = bro.find_element_by_id('password')
            login_button = bro.find_element_by_class_name('auth_login_btn')
            user_name.click()
            user_name.send_keys(user_names[i])
            pass_word.click()
            pass_word.send_keys(pass_words[i])
            login_button.click()
            print('************ 登录成功 ************')
            sleep(2)

            # 获取健康打卡界面中我的表单，并 switch_to 此界面
            report_page = bro.find_element_by_xpath('//div[contains(text(),"Daily Health Report 健康打卡")]')
            report_page.click()
            sleep(2)
            handles = bro.window_handles
            bro.switch_to.window(handles[-1])
            sleep(5)
            print('************ current_url:', bro.current_url, ' ************')
            mine_page = bro.find_element_by_xpath('//div[contains(text(),"我的表单")]')
            mine_page.click()
            sleep(5)

            # 判断是否已打卡
            confirm = bro.find_element_by_xpath('//*[@id="select_1582538939790"]/div')
            if confirm.text[0] == "是":
                print("************ 已打卡 ************")
                content = user_names[i]+" 已健康打卡 !"
                send_emails(i, content)
                result_list.append(True)
                continue

            # 打卡操作
            print('************ ', user_names[i], '正在打卡 ************')
            confirm.click()
            sleep(10)
            s = bro.find_element_by_xpath('//span[contains(text(),"是 Yes")]')
            s.click()
            sleep(2)
            save_button = bro.find_element_by_class_name("form-save")
            save_button.click()
            sleep(2)
            bro.switch_to.alert.accept()
            sleep(2)
            content = user_names[i]+" 健康打卡成功 !"
            send_emails(i, content)
            bro.quit()
            result_list.append(True)
        except Exception as e:
            print(e)
            content = user_names[i] + " 打卡失败 !"
            send_emails(i, content)
            result_list.append(False)
    return result_list


if __name__ == "__main__":
    daily_health_report()
