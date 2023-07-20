import pandas as pd
import requests
import re
import random
import configparser
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
# import openpyxl
from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, request, abort


from selenium import webdriver
chromeOption = webdriver.ChromeOptions()
import os
def news_crawler():
    import time
    url = f'https://udn.com/search/word/2/天然氣'
    urls = 'https://udn.com/search/word/2/天然氣'
    r = requests.get(url)
    s = Service(url)
    driver = webdriver.Chrome(url)
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

    news = []  # 存储新闻时间、标题和链接的列表
    for i in range(len(stories)):
        s = stories[i]
        time = times[i].text.strip()
        title = str(s.text)
        link = s.get('href')
        news.append([time, title, link])  # 将新闻时间、标题和链接组成一个列表，并添加到news列表中

    # 将news列表转换成DataFrame对象
    df = pd.DataFrame(news, columns=['时间', '标题', '链接'])

    # 将DataFrame对象保存为Excel文件
    df.to_excel('news.xlsx', index=False)

    return df
from main import GoogleAPIClient
import pandas as pd


class GoogleSheets(GoogleAPIClient):
    def __init__(self) -> None:
        # 呼叫 GoogleAPIClient.__init__()，並提供 serviceName, version, scope
        super().__init__(
            'sheets',
            'v4',
            ['https://www.googleapis.com/auth/spreadsheets'],
        )

    # def getWorksheet(self, spreadsheetId: str, range: str):
    #     request = self.googleAPIService.spreadsheets().values().get(
    #         spreadsheetId=spreadsheetId,
    #         range=range,
    #     )
    #     result = request.execute()['values']
    #     header = result[0]
    #     del result[0]
    #     return pd.DataFrame(result, columns=header)

    # def clearWorksheet(self, spreadsheetId: str, range: str):
    #     self.googleAPIService.spreadsheets().values().clear(
    #         spreadsheetId=spreadsheetId,
    #         range=range,
    #     ).execute()
    #     return 0

    def setWorksheet(self, spreadsheetId: str, range: str, df: pd.DataFrame):
        # self.clearWorksheet(spreadsheetId, range)
        self.googleAPIService.spreadsheets().values().update(
            spreadsheetId=spreadsheetId,
            range=range,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df.T.reset_index().T.values.tolist()
            },
        ).execute()
        return 0

    def appendWorksheet(self, spreadsheetId: str, range: str, df: pd.DataFrame):
        self.googleAPIService.spreadsheets().values().append(
            spreadsheetId=spreadsheetId,
            range=range,
            valueInputOption='USER_ENTERED',
            body={
                'majorDimension': 'ROWS',
                'values': df.values.tolist()
            },
        ).execute()
        return 0


if __name__ == '__main__':
    myWorksheet = GoogleSheets()

    # # 測試讀取數據
    # print(myWorksheet.getWorksheet(
    #     spreadsheetId='1SThj-wFLlDVXfLcRCdaDLYGcO3Tj1zfCN4ogepklNoY',
    #     range='工作表1'
    # ))

    # 測試輸出 pandas dataframe
    print(myWorksheet.setWorksheet(
        spreadsheetId='1SThj-wFLlDVXfLcRCdaDLYGcO3Tj1zfCN4ogepklNoY',
        range='工作表1',
        df=news_crawler()
    ))

    # 測試在末端加上新的一行
    # print(myWorksheet.appendWorksheet(
    #     spreadsheetId='1SThj-wFLlDVXfLcRCdaDLYGcO3Tj1zfCN4ogepklNoY',
    #     range='工作表1',
    #     df=pd.DataFrame(
    #         {'姓名': ['Brian'],
    #          '性別': ['M'],
    #          '體重': [65]}
    #     )
    # ))