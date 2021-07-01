import AccessDB, Login
#' ' - no access
def checkAccess(userID, path):
    userAccess = AccessDB.selectRules(userID, path, Login.con)
    return userAccess

def checkAccessMand(userLevel, path, action):
    userAccess = AccessDB.selectRuleMand(userLevel, path, Login.con)
    if userAccess.find(action) == -1:
        return -1
    else:
        return 0

if __name__ == "__main__":
    print(checkAccess(0, "/Users/fetargo", "x"))
    print(checkAccess(0, "/Users/tester", "x"))
    print(checkAccess(0, "/Users/tester/ban", "x"))