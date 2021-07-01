from mmap import MAP_EXECUTABLE
from re import S
import psycopg2
import AccessDB
import random
import hashlib

# program login = OS login (net)
con = AccessDB.connectToDB()

def addUser(login, password, level=0):
    if (login == '' or password == ''):
        print("User adding failed: invalid login or password")
        print("Login.addUser return code: -1")
        return -1, -1
    cur = con.cursor()
    cur.execute('SELECT MAX("userID") FROM "Users"')
    id = cur.fetchall()
    if id[0][0] != None:
        maxid = id[0][0] + 1
    else:
        maxid = 0
    cur.execute('SELECT "username" FROM "Users"' + 
                ' WHERE "username" = %(username)s', {'username':login})
    username = cur.fetchall()
    if len(username) != 0:
        if username[0][0] == login:
            print("User adding failed: user already exists")
            print("Login.addUser return code: -1")
            return -1, -1
    salt = random.randint(1, 65535)
    password = password+str(salt)
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    cur.execute('INSERT INTO "Users" ("userID", "username", "password", "userLevel", "salt") VALUES ' + 
                "(%(userID)s, %(username)s, %(password)s, %(userLevel)s, %(salt)s)", 
                {'userID':maxid, 'username':login, 'password':password, 'userLevel':level, 'salt':salt})  #userlevel = 0 if discretion/level if mandatory
    try:
        con.commit()
        print("User added")
        print("Login.addUser return code: 0")
        return level, maxid
    except:
        print("User adding failed")
        print("Login.addUser return code: -1")
        return -1, -1

def deleteUser():
    errorcode = 0
    return errorcode

def updateUser(level, login):
    cur = con.cursor()
    cur.execute('UPDATE "Users" SET "userLevel" = %(level)s' +
                    ' WHERE "username" = %(login)s',
                    {'login':login, 'level':level})
    try:
        con.commit()
        print("User altered")
        print("Login.updateUser return code: 0")
        return 0
    except:
        print("User adding failed")
        print("Login.updateUser return code: 1")
        return 1

def setSessionLevel(level, login):         #set access level after login
    if level > selectLevel(login):
        errorcode = 1
        return errorcode
    else:
        errorcode = 0
        return errorcode

def logIn(login, password):
    salt = selectSalt(login)
    if salt == -1:
        print("Login failed: can't find salt")
        return -1, -1
    print(salt)
    password += str(salt)
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    cur = con.cursor()
    cur.execute('SELECT "password", "userLevel", "userID" FROM "Users"' + 
                ' WHERE "username" = %(username)s', {'username':login})
    userInfo = cur.fetchall()
    if len(userInfo) == 0:
        print("Login failed: no such user")
        return -1, -1
    elif userInfo[0][0] == password:
        print("User logged in")
        return userInfo[0][1], userInfo[0][2]   #userLevel
    else:
        print("Login failed: wrong password")
        return -1, -1
    

def setUserPassword(login, password):  #function for admin to set user's password
    salt = random.randint(1, 65535)
    password += str(salt)
    password = hashlib.sha256(str(password).encode('utf-8')).hexdigest()
    #add hash to DB
    errorcode = -1
    #add salt to DB
    return errorcode

def selectSalt(login):
    cur = con.cursor()
    cur.execute('SELECT "salt" FROM "Users"' + 
                ' WHERE "username" = %(username)s', {'username':login})
    salt = cur.fetchall()
    if len(salt) != 0:
        print("Salt selected")
        return salt[0][0]
    else:
        print("Salt not selected")
        print("Login.selectSalt return code: -1")
        return -1

def selectLevel(login):
    cur = con.cursor()
    cur.execute('SELECT "userLevel" FROM "Users"' + 
                ' WHERE "username" = %(username)s', {'username':login})
    level = cur.fetchall()
    if len(level) != 0:
        print("userLevel selected")
        return level[0][0]
    else:
        print("userLevel not selected")
        print("Login.selectLevel return code: -1")
        return -1

if __name__ == "__main__":
    print(hashlib.sha256("ban".encode('utf-8')).hexdigest())