def deleteData(database, msg):
    Ids = msg.splitlines()
    text = "已刪除\nId: "
    for Id in Ids:
        string = "DELETE FROM " + database.userID +\
                 " WHERE id= " + str(Id) + ";"
        database.cur.execute(string)
        database.con.commit()
        text = text + Id + " "
    return text
