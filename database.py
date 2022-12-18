import sqlite3

class ChatsDB:
    def __init__(self, dbName):
        self.db = sqlite3.connect(dbName)
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS chats (chatID TEXT UNIQUE NOT NULL)")
        self.db.commit()

    def add_chat(self, chatID):
        self.cursor.execute("INSERT INTO chats VALUES (?)", (chatID,))
        self.db.commit()

    def __iter__(self):
        return iter([int(i[0]) for i in self.cursor.execute("SELECT * FROM chats").fetchall()])


chats = ChatsDB("chats.db")
