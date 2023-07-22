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
        df=pd.DataFrame(
            {'姓名': ['Janice', 'Wade', 'Henry', 'Wendy'],
             '性別': ['F', 'M', 'M', 'F'],
             '體重': [54, 67, 82, 68]}
        )
    ))

    # 測試在末端加上新的一行
    print(myWorksheet.appendWorksheet(
        spreadsheetId='1SThj-wFLlDVXfLcRCdaDLYGcO3Tj1zfCN4ogepklNoY',
        range='工作表1',
        df=pd.DataFrame(
            {'姓名': ['Brian'],
             '性別': ['M'],
             '體重': [65]}
        )
    ))