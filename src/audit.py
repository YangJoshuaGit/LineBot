import datetime

ID = 0
YEAR = 1
MONTH = 2
DAY = 3
VALUE = 4
TYPE = 5
DESCRIPTION = 6

def auditDataToLineString(datas):
    msg = str("")
    for data in datas:
        msg = msg + "~~~~~~~~~~~\n" +\
              "日期: " + data["date"] + "\n" +\
              "價格: " + str(data["value"]) + "\n" +\
              "種類: " + data["type"] + "\n"
        if data["description"] != ' ':
            msg = msg + "備註: " + data["description"] + "\n"
        msg = msg + "id: " + str(data["ID"]) + "\n"
    msg = msg + "~~~~~~~~~~~\n總計" + str(len(datas)) + "筆資料"
    return msg

def getFilterTypes(msg):
    filter_types = list()
    if not msg[0].isdigit():
        filter_types = msg[0:]
    else:
        if len(msg) == 2:
            # all types
            return []
        filter_types = msg[2:]
        for filter_type in filter_types:
            if filter_type == "全":
                # all types
                filter_types = []
                break
    return filter_types
