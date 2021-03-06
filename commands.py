import uuid
import db


class Commands():
    def __init__(self, database):
        self._db = database

    def login(self, command):
        if not command['body']['username'] or not command['body']['password']:
            return({'code': '400', 'message': 'Missing Parameters'})

        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        password = self._db.handleQuery((userId[0][0],), 'getPassword')
        if password[0][0] != command['body']['password']:
            return({
                'code': '401',
                'message': 'Username or password is incorrect'
            })
        newSess = self._db.handleUpdate(
            (str(uuid.uuid4()), userId[0][0]), 'session')

        return {
            'code': '200',
            'session': newSess[0],
        }

    def createUser(self, command):
        if not command['body']['username'] or not command['body']['password'] or not command['body']['publicKey']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) != 0:
            return({'code': '400', 'message': 'Username Taken'})
        mResponse = self._db.handleMutation(
            (command['body']['username'], str(uuid.uuid4()), command['body']['password'], command['body']['publicKey'], 'foo'), 'createUser')
        newSess = self._db.handleUpdate(
            (str(uuid.uuid4()), mResponse[1]), 'session')
        return {
            'code': '200',
            'session': newSess[0],
        }

    def deleteUser(self, command):
        if not command['body']['username'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleMutation(
            (userId[0][0],), 'deleteUser')

        return {
            'code': '200',
        }

    def newPassword(self, command):
        if not command['body']['username'] or not command['session'] or not command['body']['newPassword']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleUpdate(
            (command['body']['newPassword'], userId[0][0],), 'newPassword')

        return {
            'code': '200',
        }

    def getPublicKey(self, command):
        if not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        pubKey = self._db.handleQuery(
            (userId[0][0],), 'getPublicKey')
        return {
            'code': '200',
            'response': pubKey,
        }

    def sendMessage(self, command):
        if not command['body']['message'] or not command['body']['recipitentId'] or not command['body']['date'] or not command['session'] or not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleMutation((command['body']['message'], str(uuid.uuid4()), command['body']['recipitentId'],
                                 command['body']['date'], command['body']['username']), 'createMessage')
        return {
            'code': '200',
        }

    def getMessages(self, command):
        if not command['body']['username'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        myMessages = self._db.handleQuery(
            (userId[0][0],), 'getMessages')

        return {
            'code': '200',
            'response': myMessages,
        }

    def searchUser(self, command):
        if not command['body']['searchTerm']:
            return({'code': '400', 'message': 'Missing Parameters'})
        searchString = '%' + command['body']['searchTerm'] + '%'
        searchResult = self._db.handleQuery((searchString,), 'searchForUser')

        return {
            'code': '200',
            'response': searchResult,
        }

    def deleteMesseges(self, command):
        if not command['body']['sender'] or not command['body']['recipitent'] or not command['session']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['recipitent'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        session = self._db.handleQuery(
            (userId[0][0],), 'getCurrentSession')
        if session[0][0] != command['session']:
            return({'code': '401', 'message': 'No session established'})
        self._db.handleMutation(
            (command['body']['sender'], userId[0][0]), 'deleteMessages')

    def logout(self, command):
        if not command['body']['username']:
            return({'code': '400', 'message': 'Missing Parameters'})
        userId = self._db.handleQuery(
            (command['body']['username'],), 'getUserbyUsername')
        if len(userId) == 0:
            return({'code': '400', 'message': 'Username Does not match any records'})
        self._db.handleUpdate(
            (str(uuid.uuid4()), userId[0][0]), 'session')

    def handleCommand(self, command):
        try:
            return getattr(self, command['head'])(command)
        except Exception as e:
            print('exception reached')
            print(e)
            return Exception


if __name__ == '__main__':
    pass
