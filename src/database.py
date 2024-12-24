import sqlite3

class Database:
    def __init__(self, userID):
        self.userID = userID
        self.con = sqlite3.connect("./db/" + userID + ".db", check_same_thread=False)
        self.cur = self.con.cursor()
        self.createTable()

    def createTable(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS " + self.userID + " ( "
            + "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            + "action TEXT DEFAULT 支出, "
            + "type TEXT NOT NULL, "
            + "value INTEGER DEFAULT 0, "
            + "description TEXT, "
            + "year TEXT NOT NULL, "
            + "month TEXT NOT NULL, "
            + "date TEXT NOT NULL, "
            + "time TEXT NOT NULL)"
        )
    
    def insertToTable(self, data):
        sql = "INSERT INTO " + self.userID +\
        " (action, type, value, description, year, month, date, time)" +\
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
        self.cur.execute(sql, data)
        self.con.commit()

    def deleteFromTable(self, ID):
        sql = "DELETE FROM " + self.userID + " WHERE id=" + ID
        self.cur.execute(sql)
        self.con.commit()

    def getAllInfoFromTable(self):
        sql = "SELECT year, month, date, value, type, description FROM " + self.userID +\
        " WHERE action LIKE '%expenditure%' AND month LIKE '12' ORDER BY date;"
        datas = self.cur.execute(sql)
        return datas
