import sys
import random
import time
from enum import Enum
import pymysql
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

def mysqlconnect(pw):

    try:
        # To connect MySQL database
        conn = pymysql.connect(
            host='127.0.0.1',
            user= "root", 
            password = pw,
            db='hdtherapist',
            autocommit=True
        )
        print("Connected")
    except:
        print("Could not connect it")
    return conn

def Message(title, mssg):
    msg = QMessageBox()
    #msg.setIcon(QMessageBox.Information)
    msg.setText(mssg)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()

class Gender(Enum):
    male = 0
    female = 1

class RegisterWindow(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("Welcome!")
        self.resize(200, 150)
        vLayout = QVBoxLayout()

        name_layout = QHBoxLayout()
        age_layout = QHBoxLayout()
        id_layout = QHBoxLayout()
        pw_layout = QHBoxLayout()
        button_layout = QHBoxLayout()
        askPatient_layout = QHBoxLayout()
        gender_layout = QHBoxLayout()
        race_layout = QHBoxLayout()

        self.explanation = QLabel("Registration form:")
        name_label = QLabel("Name: ")
        age_label = QLabel("Age: ")
        id_label = QLabel('ID: ')
        pw_label = QLabel('PW: ')
        patient_label = QLabel("Are you a patient or therapist?")
        gender_label = QLabel("Gender: ")
        race_label = QLabel("Race: ")

        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter your name here...")
        self.nameInput.setFixedSize(200, 30)
        self.ageInput = QComboBox()
        self.idInput = QLineEdit()
        self.idInput.setPlaceholderText("Enter your ID here...")
        self.idInput.setFixedSize(200, 30)
        self.idCheck = False

        self.pwInput = QLineEdit()
        self.pwInput.setPlaceholderText("Enter your password here...")
        self.pwInput.setFixedSize(200, 30)
        

        self.patientInput = QComboBox()
        self.genderInput = QComboBox()
        self.raceInput = QComboBox()

        for i in range(10,80):
            self.ageInput.addItem(str(i))
        
        self.raceInput.addItem("White")
        self.raceInput.addItem("Black or African American")
        self.raceInput.addItem("American Indian")
        self.raceInput.addItem("Asian")
        self.raceInput.addItem("Other")

        self.patientInput.addItem("Patient")
        self.patientInput.addItem("Therapist")

        self.genderInput.addItem("male")
        self.genderInput.addItem("female")
        #ageInput.activated[str].connect(self.onChanged)     
        self.duplicateID = QPushButton("Valid?") # checks whether there are duplicate id in db
        self.duplicateID.clicked.connect(self.CheckDuplicateID)

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.nameInput)
        name_layout.addSpacing(110)

        id_layout.addWidget(id_label)
        id_layout.addSpacing(20)
        id_layout.addWidget(self.idInput, 0, Qt.AlignLeft)
        id_layout.addWidget(self.duplicateID)

        pw_layout.addWidget(pw_label)
        pw_layout.addWidget(self.pwInput, 0, Qt.AlignLeft)
        pw_layout.addSpacing(120)

        age_layout.addWidget(age_label)
        age_layout.addWidget(self.ageInput)

        askPatient_layout.addWidget(patient_label)
        askPatient_layout.addWidget(self.patientInput)

        gender_layout.addWidget(gender_label)
        gender_layout.addWidget(self.genderInput)

        race_layout.addWidget(race_label)
        race_layout.addWidget(self.raceInput)

        registerButton = QPushButton("Register") #if id is valid, Insert patient/Therapist info into the MySQL db
        registerButton.clicked.connect(self.CheckRegistrationGood)
        cancelButton = QPushButton("Cancel") #closes register window
        

        button_layout.addWidget(cancelButton)
        button_layout.addWidget(registerButton)

        #cancelButton.clicked.connect( functionName) connects cancelButton to that function with functionName

        vLayout.addWidget(self.explanation)
        vLayout.addLayout(id_layout)
        vLayout.addLayout(pw_layout)
        vLayout.addLayout(name_layout)
        vLayout.addLayout(askPatient_layout)
        vLayout.addLayout(gender_layout)
        vLayout.addLayout(race_layout)
        vLayout.addLayout(age_layout)
        
        
        vLayout.addLayout(button_layout)

        self.setLayout(vLayout)
        self.show()
    



    def CheckDuplicateID(self):
        # checks if there are duplicate ID in mysql db and length <= 15
        # if there is no duplicate, make self.idCheck = True
        # else False
        print(self.conn)
        if self.idInput.text() == "" or len(self.idInput.text()) < 3:
            self.explanation.setText("Registration form: " + "ID should be longer than 2 letters")
            self.duplicateID.setText("Not Valid!")
            self.duplicateID.setStyleSheet("background-color: red; color: white;")
            return
        self.explanation.setText("Registration form: ")

        try:
            cur = self.conn.cursor()
            sql_dup_check = "select duplicate_check(%s)"

            
            #print("dup check returns: " + self.idInput.text())
            
            cur.execute(sql_dup_check, self.idInput.text())
            num = cur.fetchone()[0]
            
            if num == 0:
                #if == 0, 
                # it means there is no duplicate id
                self.idCheck = True
                self.duplicateID.setText("Valid ID!")
                self.duplicateID.setStyleSheet("background-color: lightblue; color: white;")
                print("there is no id:", self.idInput.text())
            else:
                self.idCheck = False
                print("there exists id: ")
                self.duplicateID.setText("Not Valid!")
                self.duplicateID.setStyleSheet("background-color: red; color: white;")
            
            #for result in cur.fetchall():
            #    print(result)

        except:
            print("Error in check duplicate id ")
            #Run_Track_Char(conn)

    def Run_Register(self, id, pw, name, isPatient, gender, race, age):
        print(id, pw, name, isPatient, gender, race, age)
        cur = self.conn.cursor()
        sql_register = "CALL register_user(%s,%s,%s,%s,%s,%s,%s)"
        
        #char_name = lower(char_name)

        pat= "Patient"== isPatient

        data = (id, pw, name, pat, gender, race, age)

        cur.execute(sql_register, data)

        print("ran registration")
        for result in cur.fetchall():
            print(result)
        Message("Message", "Registration complete!")
        self.conn.commit()

        data2 = (id, "")
        sql_insert = "call insert_patient(%s, %s)"
        if pat: # if patient
            cur.execute(sql_insert, data2)
        else: # if therapist
            sql_insert = "call insert_therapist(%s, %s)"
            cur.execute(sql_insert, (id, str(0)))
        self.conn.commit()
        self.close()
        print("end")
     
    
    def CheckRegistrationGood(self):
        #check if id <= 15
        #check if pw <= 15
        #check if name <= 20
        if self.nameInput.text() == "":
            self.explanation.setText("Registration form: " + "Enter your name")
            self.explanation.setStyleSheet("background-color: red; color: white; border: 1px solid black;")
            return
        if self.idInput.text() == "" or len(self.idInput.text()) < 3:
            self.explanation.setText("Registration form: " + "ID should be longer than 2 letters")
            self.explanation.setStyleSheet("background-color: red; color: white; border: 1px solid black;")
            return

        if self.idCheck:
            if len(self.pwInput.text()) <= 15:
                if len(self.nameInput.text()) <= 20:
                    # Run register function to Insert into db in mysql
                    self.Run_Register(self.idInput.text(), self.pwInput.text(), self.nameInput.text(), str(self.patientInput.currentText()), str(self.genderInput.currentText()), str(self.raceInput.currentText()), int(self.ageInput.currentText()))
                else:
                    print("register failed")
                    self.explanation.setText("Registration form: " + "name is too long")
                    self.explanation.setStyleSheet("background-color: red; color: white; border: 1px solid black;")
            else:
                # pw exceeds 15 length
                self.explanation.setText("Registration form: " + "password is too long")
                self.explanation.setStyleSheet("background-color: red; color: white; border: 1px solid black;")
                print("password is too long")
        else:
            self.explanation.setText("Registration form: " + "Check ID Duplication")
            self.explanation.setStyleSheet("background-color: red; color: white; border: 1px solid black;")
            print("Please check the id duplication")


class dialog(QWidget):
    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.setWindowTitle("Login Window")
        self.resize(270,110)
        verticalLayout = QVBoxLayout()
        
        id_layout = QHBoxLayout()
        pw_layout = QHBoxLayout()
        id_label = QLabel('ID:')
        pw_label = QLabel('PW: ')
        self.idInput = QLineEdit()
        self.pwInput = QLineEdit()

        id_layout.addWidget(id_label)
        id_layout.addWidget(self.idInput)

        pw_layout.addWidget(pw_label)
        pw_layout.addWidget(self.pwInput)
        
        button_layout = QHBoxLayout()
        loginButton = QPushButton("Login")
        cancelButton = QPushButton("Cancel")
        registerButton = QPushButton("Register")

        registerButton.clicked.connect(self.OpenRegistration)
        loginButton.clicked.connect(self.Login)
        cancelButton.clicked.connect(self.close)

        button_layout.addWidget(cancelButton)
        button_layout.addWidget(registerButton)
        button_layout.addWidget(loginButton)
        
        verticalLayout.addLayout(id_layout)
        verticalLayout.addLayout(pw_layout)
        verticalLayout.addLayout(button_layout)
        self.setLayout(verticalLayout)
        self.show()

    def OpenRegistration(self):
        self.reg = RegisterWindow(self.conn)

    def Login(self):
        if self.idInput.text() == "" or self.pwInput.text() == "":
            self.setWindowTitle("Wrong ID/PW!")
            return
        cur = self.conn.cursor()
        sql_login = "select password_check(%s, %s)"
        data = (self.idInput.text(), self.pwInput.text())
        # if returns 0, wrong info
        # 1, right info
        cur.execute(sql_login, data)
        num = cur.fetchone()[0]
        print("login: ", num)

        print(num, "login!")
        if num > 0: 
            #login!
            sql2 = "select is_patient from registration where username=%s"
            cur.execute(sql2, self.idInput.text())
            isPat = cur.fetchone()[0]
            if isPat:
                self.StartGame()

            else:
                self.StartTheapist()
            self.close()
        else:
            self.setWindowTitle("Wrong ID/PW!")

        for result in cur.fetchall():
            print(result)

    def StartTheapist(self):
        self.therap = TherapistWindow(self.conn, self.idInput.text())

    def StartGame(self):
        self.gameWind = GameWindow(self.conn, self.idInput.text())
        self.gameWind.NextRound()
        self.gameWind.countdown(60)

class GameWindow(QWidget):
    def __init__(self, conn, id):
        super().__init__()
        self.conn = conn
        self.id = id
        self.a= ["#3AD851","#4103FC","#815184","#A9D597", "#AD6EBA","#123DED","#CC555D", "#BCDEC7", "#AB2C40", "#9295AF", "#D74774", "#B9B3A6", "#90C37A", "#C4AB16", "#70AE40", "#F654C7"]
        self.setWindowTitle("Color Picker")
        self.resize(450,350)
        verticalLayout = QVBoxLayout()
        
        self.score = 0
        qhLayout = QHBoxLayout()
        self.timer = QLabel('time: 01:00')
        self.scoreLabel = QLabel("Score: 0")
        qhLayout.addWidget(self.timer)
        qhLayout.addWidget(self.scoreLabel)

        q_label = QLabel('Goal: Pick the matching COLOR out of 3')
        self.answer_label = QLabel('COLOR')
        self.answer_label.setStyleSheet("background-color: yellow; border: 1px solid black;")
        

        self.first = QPushButton("1st")
        self.second = QPushButton("2nd")
        self.third = QPushButton("3rd")
        self.buttonList = []
        self.buttonList.append(self.first)
        self.buttonList.append(self.second)
        self.buttonList.append(self.third)
        self.first.clicked.connect(self.nextScene)
        button_layout = QHBoxLayout()

        button_layout.addWidget(self.first)
        button_layout.addWidget(self.second)
        button_layout.addWidget(self.third)

        verticalLayout.addLayout(qhLayout)
        verticalLayout.addWidget(q_label)
        verticalLayout.addWidget(self.answer_label)
        verticalLayout.addLayout(button_layout)

        self.setLayout(verticalLayout)
        self.show()

    def NextRound(self):
        
        # 1. change color of answer background
        randN = self.RandomColor()
        thisRoundColor = self.a[randN]
        self.answer_label.setStyleSheet("background-color:%s"%thisRoundColor)
        randNum = random.randint(0,2)
        for i in range(0,3):
            print(i, randNum)
            if i == randNum: # answer button
                print("Same")
                self.buttonList[i].disconnect()
                self.buttonList[i].setStyleSheet("background-color:%s"%thisRoundColor)
                x = False
                self.buttonList[i].clicked.connect(self.Answer)
                self.buttonList[i].clicked.connect(self.NextRound)
            else:
                self.buttonList[i].disconnect()
                self.buttonList[i].setStyleSheet("background-color:%s"%self.a[self.RandomColor(randN)])
                self.buttonList[i].clicked.connect(self.NextRound)
        print("score: ", self.score)

    def Answer(self):
        print("Answer!")
        self.score += 1
        self.scoreLabel.setText("Score: "+ str(self.score))

    def countdown(self, t):
        if t>0:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            timer = 'Time: '+ timer
            
            QtCore.QTimer.singleShot(1000, lambda: self.OneSecPassed(timer, t))
        else:
            self.nextScene()
        
    def OneSecPassed(self,inp,t):
        self.timer.setText(inp)
        self.countdown(t-1)

    def RandomColor(self,num=-1):
        randN = random.randint(0,len(self.a)-1)
        if num >= 0:
            while num == randN:
                randN = random.randint(0,len(self.a)-1)
        return randN

    def nextScene(self):
        self.q = QuestionWindow(self.score, self.conn, self.id)
        self.close()


class QuestionWindow(QWidget):
    def __init__(self, score, conn, id):
        super().__init__()
        self.questions = []
        self.conn = conn
        self.cur = self.conn.cursor()
        self.id = id
        loadquestionsql = "SELECT * FROM question"
        self.cur.execute(loadquestionsql)
        for result in self.cur.fetchall():
            print(result)
            self.questions.append(result[1])

        
        #self.questions.append("Did anything happen today that made you upset?")
        #self.questions.append("Did you read or see anything that got you thinking hard?")
        #self.questions.append("Did you do anything that was challenging and how did it make you feel?")
        #self.questions.append("Did you show kindness to anyone today?")
        #self.questions.append("What is one thing you liked about your day?")
        #self.questions.append("If you can change something about your day, what would it be?")
        #self.questions.append("Did someone say anything that made you upset today?")
        #self.questions.append("Did you ask for help from anyone today?")
        #self.questions.append("What are you most grateful about today?")
        #self.questions.append("What is the favourite part of your day?")
        #self.questions.append("What are you most thankful for today?")
        #self.questions.append("One the scale of 1 to 10 (1 being worst, 10 being best) how do you feel?")

        self.num = 0
        self.score = score
        self.answers = []
        self.setWindowTitle("You scored " + str(self.score) +" " + "Question" +str(self.num+1) + "/" + str(len(self.questions)))
        self.resize(550,350)
        
        verticalLayout = QVBoxLayout()
        
        self.question = QLabel(self.questions[self.num])
        self.answer = QTextEdit()
        self.answer.setFocus()

        buttonLayout = QHBoxLayout()
        self.submit = QPushButton("Submit")
        self.submit.clicked.connect(self.SetProblem)
        self.clear = QPushButton("Clear")
        self.clear.clicked.connect(self.Clear)
        buttonLayout.addWidget(self.submit)
        buttonLayout.addWidget(self.clear)

        verticalLayout.addWidget(self.question)
        verticalLayout.addWidget(self.answer)
        verticalLayout.addLayout(buttonLayout)

        self.setLayout(verticalLayout)
        self.show()

    def Clear(self):
        self.answer.setPlainText("")
        self.answer.setFocus()
    
    # Submit answer and goes to next question
    def SetProblem(self):
        txt = str(self.answer.toPlainText())
        if txt != "" and len(txt) > 3:
           
            # send text to db or save it
            self.answers.append(txt)

            self.SaveAnswer(str(self.num+1), str(self.num+1), self.id, txt)
            print(txt)
            self.num += 1
            if self.num >= len(self.questions):
                #all questions answered
                print("end")
                print("set highscore")
                print(len(self.answers))
                print("user logout")
                self.close()
            else:
                self.question.setText(self.questions[self.num])
                self.setWindowTitle("You scored " + str(self.score) +" " + "Question" +str(self.num+1) + "/" + str(len(self.questions)))                
                self.Clear()
               
    def SaveAnswer(self, aid, qid, pid, response):
        self.conn.commit()
        sql = "CALL insert_answer(%s,%s,%s,%s)"

        data = (aid, qid, pid, response)
        print(data)
        self.cur.execute(sql, data)

        

   
    
class TherapistWindow(QWidget):
    def __init__(self, conn, tid):
        super().__init__()
        self.conn = conn
        self.id = tid
        self.patients = []

        self.setWindowTitle("Hi, Therapist %s" %tid)
        self.vLayout = QVBoxLayout()
        
        name_layout = QHBoxLayout()
        id_layout = QHBoxLayout()
        self.patient_layout = QVBoxLayout()
        self.LoadPatients()

        explanation = QLabel("Enter name or id of the patient you want to view and edit")
        id_label = QLabel("Enter ID:")
        name_label = QLabel("Enter name")

        idInput = QLineEdit()
        nameInput = QLineEdit()

        findButton = QPushButton("Find Patient")
        viewAllButton = QPushButton("View All")
        findButton.clicked.connect(lambda: self.FindPatients(idInput.text(),nameInput.text()))
        viewAllButton.clicked.connect(self.ViewAll)
        deleteButton = QPushButton("DeleteMe")
        deleteButton.clicked.connect(self.DeletePatient)

        hLayout = QHBoxLayout()
        hLayout.addWidget(findButton)
        hLayout.addWidget(viewAllButton)
        hLayout.addWidget(deleteButton)

        id_layout.addWidget(id_label)
        id_layout.addWidget(idInput)

        name_layout.addWidget(name_label)
        name_layout.addWidget(nameInput)

        self.vLayout.addWidget(explanation)
        self.vLayout.addLayout(id_layout)
        self.vLayout.addLayout(name_layout)
        self.vLayout.addLayout(hLayout)
        self.vLayout.addLayout(self.patient_layout)


        self.setLayout(self.vLayout)
        self.show()

    def DeletePatient(self):
        cur = self.conn.cursor()
        sql = "Call delete_therapist(%s)"
        cur.execute(sql, self.id)
        Message("Delete", "Deleted Therapist %s"%self.id)
        self.conn.commit()
        self.close()

    def LoadPatients(self):
        cur = self.conn.cursor()
        loadsql = "SELECT * FROM registration where is_patient = %s"
        temp = []
            
        #print("dup check returns: " + self.idInput.text())
        cur2 = self.conn.cursor()    
        cur.execute(loadsql, str(1))
        i = 0
        for result in cur.fetchall():
            #id name gender race age note
            print(result)
            #qh = QHBoxLayout()
            #ab = QLabel("%s %s %s %s %s"%(result[i][0], result[i][2], result[i][4], result[i][5], result[i][6]))
            
            patsql = "SELECT notes FROM patient WHERE personalID=%s"
            print(result)
            cur2.execute(patsql, result[0])
            #print("res", cur2.fetchall())
            notes = cur2.fetchone()[0]
            print("notes:", len(notes), type(notes))
            qh = PatientSlot(self.conn, result[0], result[2], result[4], result[5], result[6], notes)

            self.patient_layout.addLayout(qh)
            qh.hide()
            self.patients.append(qh)
            i+= 1
        print(self.patients)

    def FindPatients(self, id, name):
        for patient in self.patients:
            patient.hide()

        for patient in self.patients:
            if patient.id  == id:
                patient.show()

            elif patient.name == name:
                patient.show()

            else:
                pass
        self.adjustSize()

    def ViewAll(self):
        for pat in self.patients:
            pat.show()

    def OpenNote(self, ut):
        self.n = Note(self.conn, self.id, ut)

class PatientSlot(QHBoxLayout):
    def __init__(self, conn, id, name, gender, race, age, note):
        super().__init__()
        #id name gender race age note
        self.conn = conn
        self.id = id
        self.name = name
        self.qh = QHBoxLayout()
        self.ab = QLabel("%s %s %s %s %s"%(id, name, gender, race, age))
        
       
        self.but = QPushButton("Note")
        self.but.clicked.connect(self.OpenNote)
        self.but.resize(50,50)

        self.addWidget(self.ab)
        self.addWidget(self.but)

    def hide(self):
        self.ab.hide()
        self.but.hide()

    def show(self):
        self.ab.show()
        self.but.show()

    def OpenNote(self):
        cur2 = self.conn.cursor()
        patsql = "SELECT notes FROM patient WHERE personalID=%s"
        cur2.execute(patsql, self.id)
        notes = cur2.fetchone()[0]
        self.n = Note(self.conn, self.id, notes)

class Note(QWidget):
    def __init__(self, conn, id, txt):
        super().__init__()
        self.conn = conn
        self.note = txt
        self.id = id
        
        self.resize(400,300)
        self.setWindowTitle("%s""'""s note" %id)
        self.intro = QTextEdit(txt)
        self.vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()

        self.editButton = QPushButton("Edit")
        self.exitButton = QPushButton("Exit")
        hlayout.addWidget(self.editButton)
        hlayout.addWidget(self.exitButton)

        self.editButton.clicked.connect(self.Edit)
        self.exitButton.clicked.connect(self.close)

        self.vlayout.addWidget(self.intro)
        self.vlayout.addLayout(hlayout)
        self.setLayout(self.vlayout)
        self.show()

    def Edit(self):
        cur = self.conn.cursor()
        sql = "CALL update_note(%s, %s)"
        cur.execute(sql, (self.id, str(self.intro.toPlainText())))
        Message("Edit", "Edit Success!")
        self.close()

if __name__ == "__main__":
    connection = mysqlconnect("1t2j3e4M")
    app = QApplication(sys.argv)
    w = dialog(connection)
    #Message("hi", "popup")
    #w= QuestionWindow(10, connection, "qqqq")
    #w = RegisterWindow(connection)
    #w = TherapistWindow(connection, "qqqq")
    #connection.close()
    sys.exit(app.exec_())