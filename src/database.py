import gspread
import pandas as pd
import datetime
from oauth2client.service_account import ServiceAccountCredentials
from audit import *

class Database:
    def __init__(self, userID):
        self.userID = userID
        self.scope = ["https://spreadsheets.google.com/feeds", 
                      "https://www.googleapis.com/auth/drive"]
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.userID, self.scope)
        self.client = gspread.authorize(self.credentials)
        self.sheet = self.client.open("Accouting Book").sheet1

        row_data = self.sheet.row_values(1)
        if row_data == []:
            new_data = ["ID", "action", "type", "value", "description", "date", "time"]
            self.sheet.insert_row(new_data, 1)
    
    def getRowCount(self):
        values = self.sheet.get_all_values()
        return len(values)

    def insertToTable(self, data):
        self.sheet.append_row(data)

    def deleteData(self, msg):
        Ids = msg.splitlines()
        Ids.sort(key=int)
        print(Ids)
        text = "已刪除\nId: "
        i = 2
        for record in self.sheet.get_all_records():
            if int(record["ID"]) == int(Ids[0]):
                self.sheet.delete_rows(i)
                text = text + Ids[0] + " "
                Ids.pop(0)
            else:
                i = i + 1
            if Ids == []:
                break
        return text

    def filterDataByType(self, data_type, filters):
        for filter_type in filters:
            if data_type == filter_type:
                return True
        return False

    def getAuditInfo(self, msg):
        msg = msg.splitlines()
        records = self.sheet.get_all_records()
        flag = {"date": 0, "type": 0}
        if not msg[0].isdigit():
            flag["date"] = 0
        else:
            flag["date"] = 1
            start_date = msg[0][0:4] + "-" + msg[0][4:6] + "-" + msg[0][6:8]
            end_date = msg[1][0:4] + "-" + msg[1][4:6] + "-" + msg[1][6:8]
            start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        filter_types = getFilterTypes(msg)
        # Filter
        filtered_records = dict()
        # choose data by date
        if flag["date"]:
            filtered_records = [record for record in records 
                                if (datetime.datetime.strptime(record['date'], "%Y-%m-%d") 
                                    >= start_date) 
                                and (datetime.datetime.strptime(record['date'], "%Y-%m-%d")
                                    <= end_date)]
        else:
            filtered_records = records
        # choose data by type
        if filter_types == []:
            pass
        else:
            filtered_records = [
                record for record in filtered_records
                if self.filterDataByType(record["type"], filter_types)
            ]
        # order data by date
        filtered_records = sorted(filtered_records, 
                            key=lambda x: datetime.datetime.strptime(x['date'], '%Y-%m-%d'))
        return filtered_records
