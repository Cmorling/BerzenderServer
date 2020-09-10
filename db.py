import dbStrings
import sqlite3


class Database():
    def __init__(self):
        self._conn = None
      
    def _setup(self):
        try:
            cur = self._conn.cursor()
            cur.execute(dbStrings.createUserTable)
            cur.execute(dbStrings.createMessegesTable)

        except sqlite3.Error as e:
            print(e)

    def handleMutation(self, mutationTuple, mutationType):
        cur = self._conn.cursor()
        cur.execute(dbStrings.mutations[mutationType], mutationTuple)
        self._conn.commit()
        return mutationTuple

    def handleQuery(self, queryTuple, queryType):
        cur = self._conn.cursor()
        cur.execute(dbStrings.querys[queryType], queryTuple)

        rRows = cur.fetchall()
        return rRows

    def handleUpdate(self, udpateTuple, updateType):
        cur = self._conn.cursor()
        cur.execute(dbStrings.updates[updateType], udpateTuple)
        self._conn.commit()
        return udpateTuple

    def cleanTables(self):
        cur = self._conn.cursor()
        cur.execute(dbStrings.deleteAllUsers)
        cur.execute(dbStrings.deleteAllMessages)

    def __enter__(self):
        try:
            self._conn = sqlite3.connect(r"./berzenderDatabase.db")
            self._setup()

        except sqlite3.Error as e:
            print(e)
        return self

    def __exit__(self, *exc_info):
        if self._conn:
            self._conn.close()


if __name__ == '__main__':
    pass
