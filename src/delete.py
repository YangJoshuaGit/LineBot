def deleteData(database, msg):
    Ids = msg.splitlines()
    text = "已刪除\nId: "
    for i, record in enumerate(database.sheet.get_all_records(), start=2):
        print(record["ID"])
        if record["ID"] == Ids[0]:
            database.sheet.delete_row(i)
            text = text + Ids[0] + " "
            Ids.pop(0)
        if Ids == []:
            break
    return text
