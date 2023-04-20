import db
import auth

def dbTest():
    query = input('Enter the query: ')
    res = db.runQuery(query=query)
    print(res)

def authTest():
    uname = input('Enter the username: ')
    pwd = input('Enter the password: ')
    res = auth.getToken(uname, pwd)
    print(res)
    token = input('Enter the token for verification: ')
    print(auth.verifyToken(token))

if __name__ == '__main__':
    # dbTest()

    authTest()