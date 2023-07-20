import requests
import re
import random
import configparser
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from selenium import webdriver
import os
from opencc import OpenCC

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)



app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['Channel_Access_Token'])
handler = WebhookHandler(config['line_bot']['Channel_Secret'])
client_id = config['imgur_api']['Client_ID']
client_secret = config['imgur_api']['Client_Secret']
album_id = config['imgur_api']['Album_ID']
API_Get_Image = config['other_api']['API_Get_Image']


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


def news_crawler():
    import time
    urls = 'https://udn.com/search/word/2/天然氣'
    driver.get(urls)
    content = ''
    xd = time
    for i in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xd.sleep(1)
    xd.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stories = soup.select('div.story-list__text h2 a')
    times = soup.find_all('time', class_='story-list__time')

    for i in range(len(stories)):
        s = stories[i]
        time = times[i].text.strip()
        title = str(s.text)
        link = s.get('href')
        content += '{}\n{}\n{}\n\n'.format(time, title, link)

    return content


def news_crawler_same(keyword):
    import time
    url=f'https://udn.com/search/word/2/{keyword}'
    urls = f'https://udn.com/search/word/2/{keyword}'
    r = requests.get(url)
    # s = Service(url)
    # driver = webdriver.Chrome(service=s)
    driver.get(urls)
    content = ''
    xd = time
    for i in range(2):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xd.sleep(0.1)
    xd.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    stories = soup.select('div.story-list__text h2 a')
    times = soup.find_all('time', class_='story-list__time')
    #

    for i in range(len(stories)):
        s = stories[i]
        time = times[i].text.strip()
        title = str(s.text)
        link = s.get('href')
        content += '{}\n{}\n{}\n\n'.format(time, title, link)

    return content


def news_2_crawler():
    crawler_data = []
    time_data = []
    content_data = ''

    for i in range(1, 2):
        r = requests.get('https://www.chinatimes.com/search/天然氣' + "?page=" + str(i) + "&chdtv")

        if r.status_code == requests.codes.ok:
            soup = BeautifulSoup(r.text, 'html.parser')
            stories = soup.select('h3.title a')
            times = soup.find_all('span', class_='date')
            hours = soup.find_all('span', class_='hour')
            for i in range(len(stories)):
                s = stories[i]
                hour = hours[i].text.strip()
                time = times[i].text.strip()
                t = time + ' ' + hour
                title = str(s.text)
                link = s.get('href')
                r_link = requests.get(link)
                if r_link.status_code == requests.codes.ok:
                    soup_link = BeautifulSoup(r_link.text, 'html.parser')
                    content = soup_link.select_one('div.article-body')
                    if content is not None:
                        content_text = content.get_text().strip().replace('\n', ' ')
                    else:
                        content_text = ""
                    content_data += '{}\n{}\n{}\n\n'.format(t, title, content_text)
                else:
                    content_data += '{}\n{}\n{}\n\n'.format(t, title, "")

    return content_data

def news_2_crawler_same(keyword):
    crawler_data=[]
    time_data=[]
    content_data = []
    content = ''
    # 下載 udn新聞網「熱門」新聞內容

    # keyword=input("請輸入新聞搜尋主題:")
    # page=int(input("請輸入想要爬取的頁數:"))

    # url=f'https://www.chinatimes.com/search/{keyword}'+"page"+str(i)+"&chdtv"

    for i in range(1,3):
        r = requests.get('https://www.chinatimes.com/search/' + keyword + "?page=" + str(i) + "&chdtv")
    # s=Service(r"https://udn.com/search/word/2/%E5%A4%A9%E7%84%B6%E6%B0%A3")
    # driver=webdriver.Chrome(service=s)
    # driver.get('https://udn.com/search/word/2/%E5%A4%A9%E7%84%B6%E6%B0%A3')
    # # 確認是否下載成功

        if r.status_code == requests.codes.ok:
            # print('ok')  # 後續可刪除或標註為註解
            # 以BeautifulSoup解析HTML程式碼
            soup = BeautifulSoup(r.text, 'html.parser')
            stories = soup.select('h3.title a')
            # print(stories)
            times=soup.find_all('span', class_='date')
            hours = soup.find_all('span', class_='hour')
            # print(times)
            # print(stories)
            #         for link in stories:
            #             crawler_data_sub = []
            #             # 爬取新聞內容
            #             r_link = requests.get(link.get('href'))
            #             if r_link.status_code == requests.codes.ok:
            #                 soup_link = BeautifulSoup(r_link.text, 'html.parser')
            #                 content = soup_link.select_one('div.article-body')
            #                 if content is not None:
            #                     content_text = content.get_text().strip().replace('\n', ' ')
            #                 else:
            #                     content_text = ""
            #                 content_data.append(content_text)
            #             else:
            #                 content_data.append("")
            for i in range(len(stories)):
                s = stories[i]
                hour = hours[i].text.strip()
                time = times[i].text.strip()
                t = time + ' ' + hour
                title = str(s.text)
                #             .text.strip()
                link = s.get('href')
                content += '{}\n{}\n{}\n\n'.format(t, title, link)

    #         for time in times:
    #             time_data_sub=[]
    #             time_data_sub.append(str(time.text))
    #             time_data.append(time_data_sub)
    return content

def wiki(keyword):
    url = f"https://zh.wikipedia.org/wiki/{keyword}"
    content=''
    # 发送请求并获取响应
    response = requests.get(url)

    # 使用 BeautifulSoup 解析响应内容
    soup = BeautifulSoup(response.text, "html.parser")
    cc = OpenCC('s2tw')
    infobox = soup.find("table")
    info=infobox.find_all("tr")
    for i in info:
        infos=(cc.convert(i.text))
        if "出生" in infos:
            content+=infos+"\n"
#             print(infos)
        if "國籍" in infos:
            content+=infos+"\n\n"
#             print(infos)
        if "政黨" in infos:
            content+=infos+"\n"
#             print(infos)
        if "學歷" in infos:
            content+=infos+"\n"
#             print(infos)
        if "經歷" in infos:
            content+=infos+"\n"
#             print(infos)
    content+=url+"\n"
    return content

def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq


def crawl_page_gossiping(res):
    soup = BeautifulSoup(res.text, 'html.parser')
    article_gossiping_seq = []
    for r_ent in soup.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']

            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                url_link = 'https://www.ptt.cc' + link
                article_gossiping_seq.append({
                    'url_link': url_link,
                    'title': title
                })

        except Exception as e:
            # print u'crawPage function error:',r_ent.find(class_="title").text.strip()
            # print('本文已被刪除')
            print('delete', e)
    return article_gossiping_seq


def ptt_gossiping():
    rs = requests.session()
    load = {
        'from': '/bbs/Gossiping/index.html',
        'yes': 'yes'
    }
    res = rs.post('https://www.ptt.cc/ask/over18', verify=False, data=load)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    index_list = []
    article_gossiping = []
    for page in range(start_page, start_page - 2, -1):
        page_url = 'https://www.ptt.cc/bbs/Gossiping/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_gossiping = crawl_page_gossiping(res)
            # print u'OK_URL:', index
            # time.sleep(0.05)
    content = ''
    for index, article in enumerate(article_gossiping, 0):
        if index == 15:
            return content
        data = '{}\n{}\n\n'.format(article.get('title', None), article.get('url_link', None))
        content += data
    return content

def ptt_hot():
    target_url = 'http://disp.cc/b/PttHot'
    print('Start parsing pttHot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('#list div.row2 div span.listTitle'):
        title = data.text
        link = "http://disp.cc/b/" + data.find('a')['href']
        if data.find('a')['href'] == "796-59l9":
            break
        content += '{}\n{}\n\n'.format(title, link)
    return content

def technews():
    target_url = 'https://technews.tw/'
    print('Start parsing movie ...')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""

    for index, data in enumerate(soup.select('article div h1.entry-title a')):
        if index == 12:
            return content
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content


def panx():
    target_url = 'https://panx.asia/'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    for data in soup.select('div.container div.row div.desc_wrap h2 a'):
        title = data.text
        link = data['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    if event.message.text == "聯合新聞":
        content = news_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if "聯合新聞," in event.message.text:
        keyword = event.message.text.split(',')[1]
        content = news_crawler_same(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "中時新聞":
        content = news_2_crawler()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if "中時新聞," in event.message.text:
        keyword = event.message.text.split(',')[1]
        content = news_2_crawler_same(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    if "維基百科," in event.message.text:
        keyword = event.message.text.split(',')[1]
        content = wiki(keyword)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
    if event.message.text == "近期熱門廢文":
        content = ptt_hot()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "即時廢文":
        content = ptt_gossiping()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "科技新報":
        content = technews()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "PanX泛科技":
        content = panx()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "你好":
        buttons_template = TemplateSendMessage(
            alt_text='開始玩 template',
            template=ButtonsTemplate(
                title='你想選擇哪種服務呢',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/onRCAkH.jpg',
                # https: // imgur.com / hbGzMVL
                # https: // i.imgur.com / xQF5dZT.jpg
                actions=[
                    MessageTemplateAction(
                        label='新聞',
                        text='新聞'
                    ),
                    MessageTemplateAction(
                        label='維基百科',
                        text='維基百科'
                    ),
                    MessageTemplateAction(
                        label='看廢文',
                        text='看廢文'
                    )
                    # MessageTemplateAction(
                    #     label='正妹',
                    #     text='正妹'
                    # )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "新聞":
        buttons_template = TemplateSendMessage(
            alt_text='新聞 template',
            template=ButtonsTemplate(
                title='請選擇新聞類型',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/Nf1Wq4J.jpeg',
                actions=[
                    MessageTemplateAction(
                        label='聯合新聞',
                        text='聯合新聞'
                    )
                    ,
                    MessageTemplateAction(
                        label='中時新聞',
                        text='中時新聞'
                    )
                    ,
                    MessageTemplateAction(
                        label='科技新報',
                        text='科技新報'
                    ),
                    MessageTemplateAction(
                        label='PanX泛科技',
                        text='PanX泛科技'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "維基百科":
        buttons_template = TemplateSendMessage(
            alt_text='維基百科 template',
            template=ButtonsTemplate(
                title='點選下方熱門人物或是\n輸入"維基百科,你想搜尋的人物"',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/k8K7Vqv.jpg',
                actions=[
                    MessageTemplateAction(
                        label='蔡英文',
                        text='維基百科,蔡英文'
                    ),
                    MessageTemplateAction(
                        label='侯友宜',
                        text='維基百科,侯友宜'
                    ),
                    MessageTemplateAction(
                        label='柯文哲',
                        text='維基百科,柯文哲'
                    ),
                    MessageTemplateAction(
                        label='連勝文',
                        text='維基百科,連勝文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0
    if event.message.text == "看廢文":
        buttons_template = TemplateSendMessage(
            alt_text='看廢文 template',
            template=ButtonsTemplate(
                title='你想看什麼廢文呢',
                text='請選擇',
                thumbnail_image_url='https://i.imgur.com/ap59eQp.jpg',
                # https: // i.imgur.com / ocmxAdS.jpg
                actions=[
                    MessageTemplateAction(
                        label='近期熱門廢文',
                        text='近期熱門廢文'
                    ),
                    MessageTemplateAction(
                        label='即時廢文',
                        text='即時廢文'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
        return 0

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    print("package_id:", event.message.package_id)
    print("sticker_id:", event.message.sticker_id)
    # ref. https://developers.line.me/media/messaging-api/sticker_list.pdf
    sticker_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 100, 101, 102, 103, 104, 105, 106,
                   107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125,
                   126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 401, 402]
    index_id = random.randint(0, len(sticker_ids) - 1)
    sticker_id = str(sticker_ids[index_id])
    print(index_id)
    sticker_message = StickerSendMessage(
        package_id='1',
        sticker_id=sticker_id
    )
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)


if __name__ == '__main__':
    app.run()
