from security import Ui_Security
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDir
import design, design_auth, security, Login, AccessRules, AccessDB  # Это наш конвертированный файл дизайна
import os

class SecurityPopup(QtWidgets.QMainWindow, security.Ui_Security):
    def __init__(self, path, username):
        super().__init__()
        self.path = path
        self.username = username
        self.con = AccessDB.connectToDB()
        self.userList = AccessDB.selectUsers(self.con, path)    #username, ID, access, owner
        self.allUserList = AccessDB.selectOnlyUsers(self.con)  #username, ID
        self.mergedUserList = list()
        self.setupUi(self, path)
        self.mergedUserList = self.mergeUserLists()
        self.listWidget.setCurrentRow(0)
        self.currentUser = self.listWidget.currentItem()
        self.currentUser = self.currentUser.text().split("  /////   ")
        self.currentUser = int(self.currentUser[0])
        self.initRules()
        self.listWidget.itemSelectionChanged.connect(self.changeUser)
        self.btnSetSec.clicked.connect(self.confirm)
        
    def mergeUserLists(self):
        print(self.allUserList)
        print(self.userList)
        
        for user in self.allUserList:
            found = 0
            if self.userList != None:
                for userL in self.userList:
                    if user[1] == userL[1]:
                        self.mergedUserList.append([userL[0], userL[1], userL[2], userL[3]])
                        found = 1
                        break
            if found == 0:
                self.mergedUserList.append([user[0],user[1],"rwx",0])
        for user in self.mergedUserList:  
                self.listWidget.addItem(str(user[1]) + "  /////   " + str(user[0]))
        #self.listWidget.
        return self.mergedUserList

    def initRules(self):
        user = self.mergedUserList[self.currentUser]

        if user[2].find('r') != -1:
            self.checkRead.setChecked(True)
        else:
            self.checkRead.setChecked(False)
        if user[2].find('w') != -1:
            self.checkWrite.setChecked(True)
        else:
            self.checkWrite.setChecked(False)
        if user[2].find('x') != -1:
            self.checkExec.setChecked(True)
        else:
            self.checkExec.setChecked(False)
        
        return 0
    

    def changeUser(self):
        # try:
        #     userID = self.listWidget.CurrentItem()
        #     userID.split("  /////   ")
        #     userID = userID[0]
        #     print(userID)
        # except:
        #     userID = 1
        # if self.currentUser == None:
        #     self.currentUser = self.listWidget.currentItem()
        #     self.currentUser = self.currentUser.text().split("  /////   ")
        #     self.currentUser = int(self.currentUser[0])
        #     self.initRules()
        userID = self.listWidget.currentItem()
        userID = userID.text().split("  /////   ")
        userID = int(userID[0])
        print(userID)
        rule = ''
        if self.checkRead.isChecked():        #change
            rule += 'r'
        if self.checkWrite.isChecked():      #change
            rule += 'w'
        if self.checkExec.isChecked():     #change
            rule += 'x'
        if rule == '':
            rule = 'n'
        print(self.path)
        tmp = list(self.mergedUserList[self.currentUser])
        index = self.mergedUserList.index(tmp)
        print(self.mergedUserList)
        print(tmp)
        print("cur us", self.currentUser)
        print("index", index)
        self.mergedUserList.pop(index)
        tmp.pop(2)
        tmp.insert(2, rule)
        self.mergedUserList.insert(index, tmp)
        self.currentUser = userID
        self.initRules()

    def confirm(self):
        if self.username != 'admin':
           print('you have NO rights, you are NOT an admin')
           return 0
        rule = ''
        if self.checkRead.isChecked():        #change
            rule += 'r'
        if self.checkWrite.isChecked():      #change
            rule += 'w'
        if self.checkExec.isChecked():     #change
            rule += 'x'
        if rule == '':
            rule = 'n'
        print(self.path)
        print(self.mergedUserList)
        tmp = list(self.mergedUserList[self.currentUser])
        index = self.mergedUserList.index(tmp)
        self.mergedUserList.pop(index)
        tmp.pop(2)
        tmp.insert(2, rule)
        self.mergedUserList.insert(index, tmp)
        for user in self.mergedUserList:
            AccessDB.setRule(user[1], self.path, user[2], self.con)


    
            

        

class AuthWindow(QtWidgets.QMainWindow, design_auth.Ui_AuthWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btnAuth.clicked.connect(self.auth)
        self.btnSignUp.clicked.connect(self.register)
        
    def auth(self):
        userLevel, userID = Login.logIn(self.inputLogin.text(), self.inputPass.text())
        if userID != -1:
            self.close()
            self.window = ExampleApp(self.inputLogin.text(), userID, userLevel)
            self.window.show()
        else:
            print("Login failed")   # change to message box or label

    def register(self):
        userLevel, userID = Login.addUser(self.inputLogin.text(), self.inputPass.text())
        if userID != -1:
            self.close()
            self.window = ExampleApp(self.inputLogin.text(), userID, userLevel)
            self.window.show()
        else:
            print("Register failed")   # change to message box or label
        
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    global path
    path = QDir.homePath()
    #path = '/'
    #QDir("/home/pda7271")
    print(path)

    def __init__(self, login, userID, userLevel):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.username = login
        self.userID = userID
        self.userLevel = userLevel
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.authWindow = None
        self.actionLogOut.triggered.connect(self.auth)
        self.actionOpen.triggered.connect(self.open_folder)
        self.btnBrowse.clicked.connect(self.browse_folder) #Home
        self.btnOpen.clicked.connect(self.open_folder) #Open
        self.listWidget.itemDoubleClicked.connect(self.open_folder)
        self.btnSec.clicked.connect(self.security)
        self.btnBack.clicked.connect(self.back_folder) #Back
        self.menuUserName.setTitle(login) #get userName from db
        
    def auth(self):
        self.close()
        self.authWindow = AuthWindow()
        self.authWindow.show()
        
    def security(self):
        print('security settings here popup')
        item = self.listWidget.currentItem()
        if item:
            self.window = SecurityPopup(path + '/' + item.text(),self.username)
        else:
            self.window = SecurityPopup(path, self.username)
        self.window.show()

    def open_folder(self):
        global path
        print('1')
        #print('clicked items:', self.listWidget.selectedItems())
        item = self.listWidget.currentItem()
        print('2')
        if item:  #if
            print('3')
            #print(path.QtCore.QDir.exists())
            path = path + '/' + item.text()
            if os.path.isdir(path):
                accs = AccessRules.checkAccess(self.userID, path)
                if accs.find('r') != -1:
                    print('4')
                    rule = ''
                    if accs.find("r"):
                        rule += "r"
                    else:
                        rule += "-"
                    if accs.find("w"):
                        rule += "w"
                    else:
                        rule += "-"
                    if accs.find("x"):
                        rule += "x"
                    else:
                        rule += "-"
                    
                    # os.system('sudo chmod u=' + rule + path)
                    # os.system('sudo chown appusr ' + path)
                    print('dir:',path)
                    self.list_appear()  
                else:
                    index = path.rfind('/', 0)
                    path = path[0:index]
                    print('file  dir:',path)
                    print("Access denied")                ### ckinut dashe
            elif os.path.isfile(path):
                print('5')
                print('file:',path)
                accs = AccessRules.checkAccess(self.userID, path)
                if accs.find('r') != -1:
                    print('6')
                    rule = ''
                    if accs.find("r"):
                        rule += "r"
                    else:
                        rule += "-"
                    if accs.find("w"):
                        rule += "w"
                    else:
                        rule += "-"
                    if accs.find("x"):
                        rule += "x"
                    else:
                        rule += "-"
                    
                    # os.system('sudo chmod u=' + rule + path)
                    # os.system('sudo chown appusr ' + path)
                    os.system('xdg-open '+path)
                    index = path.rfind('/', 0)
                    path = path[0:index]
                    print('file  dir:',path)
                else:
                    index = path.rfind('/', 0)
                    path = path[0:index]
                    print('file  dir:',path)
                    print("Access denied")
            else:
                print(path)
                print("kak-to plyusuetsya")
                
    def back_folder(self):
        global path
        if path != QtCore.QDir.homePath():
            # os.system('sudo chown root ' + path)
            index = path.rfind('/', 0)
            path = path[0:index]
            #QtCore.QDir.cdUp()
            self.list_appear()        
        
    def browse_folder(self):
        #path = QtWidgets.QFileDialog.getExistingDirectory(self, "Browse..")
        #path = '/home/pda7271/kursovaya'
        #print(path)
        global path
        path = QtCore.QDir.homePath()
        print(path)       
        if path:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.list_appear()
                
    def list_appear(self):
        self.listWidget.clear()
        for file_name in os.listdir(path):  # для каждого файла в директории
                self.listWidget.addItem(file_name)   # добавить файл в listWidget

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AuthWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
