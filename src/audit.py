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
              "日期: " + data[YEAR] + "/" + data[MONTH] + "/" + data[DAY] + "\n" +\
              "價格: " + str(data[VALUE]) + "\n" +\
              "種類: " + data[TYPE] + "\n"
        if data[DESCRIPTION] != "":
            msg = msg + "備註: " + data[DESCRIPTION] + "\n"
        msg = msg + "id: " + str(data[ID]) + "\n"
    msg = msg + "~~~~~~~~~~~\n總計" + str(len(datas)) + "筆資料"
    return msg

def getAuditInfo(database, msg):
    message_texts = msg.splitlines()
    fromDateTime = message_texts[0]
    toDateTime = message_texts[1]
    data_types = list()
    if len(message_texts) == 2:
        data_types = []
    else:
        data_types = message_texts[2:]
        for data_type in data_types:
            if data_type == "全":
                data_types = []
    type_num = len(data_types)
    month_num = (int(toDateTime[0:4]) - int(fromDateTime[0:4])) * 12 +\
                (int(toDateTime[4:6]) - int(fromDateTime[4:6])) + 1
    Datas = list()
    if month_num == 1:
        # Same month
        string = "SELECT id, year, month, date, value, type, description FROM " +\
                database.userID +\
                " WHERE action LIKE '%expenditure%' AND year = '" + fromDateTime[0:4] + "'" + \
                " AND month = '" + fromDateTime[4:6] + "'" +\
                " AND date >= '" + fromDateTime[6:8] + "'" +\
                " AND date <= '" + toDateTime[6:8] + "'"

        if not data_types:
            pass
        else:
            string = string + " AND ("
        i = 1
        for data_type in data_types:
            string = string + "type LIKE '" + data_type + "'"
            if i != type_num:
                string = string + " or "
            else:
                string = string + ")"
            i = i + 1

        string = string + " ORDER BY date;"
        print(string)
        datas = database.cur.execute(string)
        dealWithSqliteCursorObject(Datas, datas)
    else:
        # First month
        string = "SELECT id, year, month, date, value, type, description FROM " +\
                database.userID +\
                " WHERE action LIKE '%expenditure%' AND year = '" + fromDateTime[0:4] + "'" +\
                " AND month = '" + fromDateTime[4:6] + "'" +\
                " AND date >= '" + fromDateTime[6:8] + "'"

        if not data_types:
            pass
        else:
            string = string + " AND ("
        i = 1
        for data_type in data_types:
            string = string + "type LIKE '" + data_type + "'"
            if i != type_num:
                string = string + " or "
            else:
                string = string + ")"
            i = i + 1

        string = string + " ORDER BY date;"
        month_num = month_num - 1
        datas = database.cur.execute(string)
        dealWithSqliteCursorObject(Datas, datas)
        # Middle month
        month = int(fromDateTime[4:6])
        year = int(fromDateTime[0:4])
        while (month_num > 1):
            month = (month + 1) % 13
            if month == 0:
                month = 1
            if month == 1:
               year = year + 1
            else:
                pass
            if month > 0 and month < 10:
                month = str(month)
                month = month.zfill(2)
            dealWithSqliteCursorObject(Datas, 
                                       getAuditInfoSpecifiedMonth(database, 
                                                                  year, month, data_types))
            month_num = month_num - 1
            month = int(month)
        # Last month
        if (month_num == 1):
            string = "SELECT id, year, month, date, value, type, description FROM " +\
                    database.userID +\
                    " WHERE action LIKE '%expenditure%' AND year = '" + toDateTime[0:4] + "'" +\
                    " AND month = '" + toDateTime[4:6] + "'"+\
                    " AND date <= '" + toDateTime[6:8] + "'"

            if not data_types:
                pass
            else:
                string = string + " AND ("
            i = 1
            for data_type in data_types:
                string = string + "type LIKE '" + data_type + "'"
                if i != type_num:
                    string = string + " or "
                else:
                    string = string + ")"
                i = i + 1

            string = string + " ORDER BY date;"
            month_num = month_num - 1
            datas = database.cur.execute(string)
            dealWithSqliteCursorObject(Datas, datas)           
    return Datas
def getAuditInfoSpecifiedMonth(database, year, month, data_types):
    Datas = list()
    string = "SELECT id, year, month, date, value, type, description FROM " + database.userID +\
            " WHERE action LIKE '%expenditure%' AND year = '" + str(year) + "'" +\
            " AND month = '" + str(month) + "'"

    if not data_types:
        pass
    else:
        string = string + " AND ("
    i = 1
    for data_type in data_types:
        string = string + "type LIKE '" + data_type + "'"
        if i != len(data_types):
            string = string + " or "
        else:
            string = string + ")"
        i = i + 1

    string = string + " ORDER BY date;"
    datas = database.cur.execute(string)
    dealWithSqliteCursorObject(Datas, datas)
    return Datas

def dealWithSqliteCursorObject(originDatas, appendDatas):
    for data in appendDatas:
        if data != "":
            originDatas.append(data)
    return originDatas
