from selenium.webdriver.common.by import By
import os

r = open("urls.txt", "r", encoding="utf-8")
urls = r.read().splitlines()
r.close()
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.page_load_strategy = "eager"
browser = webdriver.Chrome(options=options)
browser.implicitly_wait(3)
if not os.path.exists("data"):
    os.mkdir("data")
for i in range(3155, 5000):
    browser.delete_all_cookies()
    w = open("data/" + str(i + 1) + ".txt", "w", encoding="utf-8")
    attempts = 0
    flag = False
    while attempts < 5 and not flag:
        try:
            attempts += 1
            browser.get(urls[i])
            participation_num = browser.find_element(
                By.CSS_SELECTOR,
                "#bottom_sina_comment > div.sina-comment-form.sina-comment-top > div.hd.clearfix > span.count > em:nth-child(3) > a",
            )
            comment_num = browser.find_element(
                By.CSS_SELECTOR,
                "#bottom_sina_comment > div.sina-comment-form.sina-comment-top > div.hd.clearfix > span.count > em:nth-child(1) > a",
            )
            flag = True
        except:
            try:
                participation_num = browser.find_element(
                    By.CSS_SELECTOR,
                    "#SI_FormList1 > div.sina-comment-form.sina-comment-top > div.hd.clearfix > span.count > em:nth-child(3) > a",
                )
                comment_num = browser.find_element(
                    By.CSS_SELECTOR,
                    "#SI_FormList1 > div.sina-comment-form.sina-comment-top > div.hd.clearfix > span.count > em:nth-child(1) > a",
                )
                flag = True
            except:
                continue
    if attempts == 5:
        try:
            comment_num = browser.find_element(
                By.CSS_SELECTOR,
                "#bottom_sina_comment > div.sina-comment-list.sina-comment-list-has-all.sina-comment-list-has-latest > div.latest-wrap > div.list-ft > a > em",
            )
            w.write("评论人数：" + comment_num.text + "\n")
            continue
        except:
            continue
    if not participation_num.text.isdigit():
        print("WARNING!!:\n\n", i)
    w.write("参与人数：" + participation_num.text + "\n")
    if not comment_num.text.isdigit():
        print("WARNING!!:\n\n", i)
    w.write("评论人数：" + comment_num.text + "\n")
