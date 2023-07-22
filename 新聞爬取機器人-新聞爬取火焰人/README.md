# 新聞爬取火焰人

1. 主要功能：
    - 新聞擷取：使用Selenium和BeautifulSoup來從聯合新聞和中時新聞網站擷取新聞標題、時間和連結。使用者可以輸入"聯合新聞"或"中時新聞"觸發相應的新聞擷取。
    - 新聞搜尋：使用者可以輸入"聯合新聞,搜尋關鍵字"或"中時新聞,搜尋關鍵字"來搜尋相關主題的新聞。
    - 維基百科擷取：使用BeautifulSoup來從維基百科擷取特定人物的出生地、國籍、政黨、學歷和經歷等資訊。使用者可以輸入"維基百科,人物名稱"觸發相應的擷取。
</br>
</br>
2. 程式結構：
    使用LineBot API和Flask建立一個Line Bot應用。
    定義了callback函數，用於處理用戶傳送的訊息。
    使用者可透過Line Bot傳送特定訊息來觸發相應的功能。
    每個功能都有對應的爬蟲函數，用於擷取網站上的資訊。
    爬蟲函數主要使用requests和BeautifulSoup庫來解析HTML內容。
</br>
</br>
3. 內容展示：
    <img width="1280" alt="Screenshot" src="https://github.com/Shawn0604/Analysis-and-Application/blob/main/%E6%96%B0%E8%81%9E%E7%88%AC%E5%8F%96%E6%A9%9F%E5%99%A8%E4%BA%BA-%E6%96%B0%E8%81%9E%E7%88%AC%E5%8F%96%E7%81%AB%E7%84%B0%E4%BA%BA/pic/0722.png">  
