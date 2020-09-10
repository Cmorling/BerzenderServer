createUserTable = ''' CREATE TABLE IF NOT EXISTS users (
                        id integer PRIMARY KEY,
                        userId text NOT NULL,
                        username text NOT NULL,
                        password text NOT NULL,
                        publicKey text NOT NULL,
                        session text
                  ); '''

createMessegesTable = '''CREATE TABLE IF NOT EXISTS messages (
                        id integer PRIMARY KEY,
                        user text NOT NULL,
                        messageId text NOT NULL,
                        message text NOT NULL,
                        recipitentId text NOT NULL,
                        date text NOT NULL
);'''
deleteAllUsers = 'DELETE FROM users'
deleteAllMessages = 'DELETE FROM messages'

mutations = {
    'createUser': '''INSERT INTO users(username,userId,password,publicKey,session)
              VALUES(?,?,?,?,?)''',
    'createMessage': '''INSERT INTO messages(message,messageId,recipitentId,date,user)
              VALUES(?,?,?,?,?)''',
    'deleteUser': '''DELETE FROM users WHERE userId=? ''',
    'deleteMessages': '''DELETE FROM messages WHERE user=? AND recipitentId=?''',
}

querys = {
    'getUserbyUsername': 'SELECT userId FROM users WHERE username=?',
    'getPassword': 'SELECT password FROM users WHERE userId=?',
    'getMessages': 'SELECT * FROM messages WHERE recipitentId=?',
    'getCurrentSession': 'SELECT session FROM users WHERE userId=?',
    'searchForUser': 'SELECT username, userId, publicKey FROM users WHERE username LIKE ?'
}

updates = {
    'session': '''UPDATE users 
                SET session=?
                WHERE userId=?''',
    'newPassword': '''UPDATE users
                SET password=?
                WHERE userId=?''',
}
