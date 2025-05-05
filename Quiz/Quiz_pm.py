# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic, QtCore
import sys
from sqliteHelper import *
from random import shuffle
import datetime
import pytz

maListe1 = []
maListe3 = []
maListe2 = []
helper = SqliteHelper("C:/allFiles/QuizDb.db")


class AnalogClock(QtWidgets.QMainWindow, QPushButton):

    secondHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -95)
    ])
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -50)
    ])
    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -70)
    ])
    hourColor = QColor(255, 0, 0)
    minuteColor = QColor(0, 255, 0, 170)
    secondColor = QColor(10, 10, 10, 100)

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        super(AnalogClock, self).__init__(parent)
        uic.loadUi('C:/allFiles/primMoyen.ui', self)
        self.msg = QMessageBox()
        self.addimage1()
        # self.setWindowTitle("Analog Clock")
        # self.resize(1300, 700)

        timer = QTimer(self)
        timer.start(1000)
        timer.timeout.connect(self.update)
        self.i = 0
        self.comptage = 0

        self.btn_find.clicked.connect(self.findUser)
        self.btn_continue.clicked.connect(self.reset_continue)
        self.btn_afficherResult.clicked.connect(self.afficherResult)
        self.btn_demarer_new.clicked.connect(self.demarer_new)
        self.comboBoxCat_2.currentIndexChanged.connect(self.selectionComboChangeRead)
        
        self.listReponse = []
        self.listResultat = []
        # self.addimage1()

        self.lineEdit_temps.setText("60")
        self.labelQuestNumero.setText("0")
        self.lbl_TimeStart.setText("")
        self.label_resultat.setText("0 %")
        self.btn_continue.setDisabled(True)

        self.comptage2 = 0
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.compteur)
        self.btn_temporisation.clicked.connect(self.startTime)

        # self.timer1.timeout.connect(self.showTime)
        self.btn_find.setDisabled(True)

        self.btnanswer2_2.setDisabled(True)
        self.btnanswer3_2.setDisabled(True)
        self.btnanswer4_2.setDisabled(True)
        self.btnanswer1_2.setDisabled(True)

        self.btnanswer1_2.clicked.connect(self.checkAnswer1)
        self.btnanswer2_2.clicked.connect(self.checkAnswer2)
        self.btnanswer3_2.clicked.connect(self.checkAnswer3)
        self.btnanswer4_2.clicked.connect(self.checkAnswer4)

        # remove windows default title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())
        # self.btn_close.clicked.connect(lambda:MainApp.exit())

        dt_mtn = datetime.datetime.now()

        mtn_tz = pytz.timezone('US/Mountain')
        dt_mtn = mtn_tz.localize(dt_mtn)
        print(dt_mtn.strftime('%B %d, %Y'))
        self.label_6.setText(dt_mtn.strftime('%B %d, %Y'))

    def paintEvent(self, event):
        side = min(self.widget.width(), self.widget.height())
        time = QTime.currentTime()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        #position verticale et horizontale
        painter.translate(self.width() / 2 + 450, self.height() / 2 + 100)
        #largeur et longueur
        painter.scale(side / 210, side / 210)
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)
        painter.save()
        # 360/12.0 times per hour
        painter.rotate(30.0 * (time.hour() + time.minute() / 60.0))
        # print(f'hour:{time.hour()}, minute:{time.minute()}, second:{time.second()}')
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()
        painter.setPen(AnalogClock.hourColor)
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)
        painter.save()
        # 6 times a minute
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()
        painter.setPen(AnalogClock.minuteColor)
        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.secondColor)
        painter.save()
        # 360 times in a minute
        painter.rotate(360 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.secondHand)
        painter.restore()

#-------------------------------------# QUIZ #-------------------------------#

    def checkAnswer1(self):

        if self.btnanswer1_2.text() == str(self.rsTuple[4]):
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#00ff00';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer2_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("صحيح")
            self.listResultat.append(20)

        else:
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#ff0000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer2_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("خطأ")
            self.listResultat.append(0)

        result = sum(self.listResultat)
        self.label_resultat.setText(str(result) + "%")

    def checkAnswer2(self):

        if self.btnanswer2_2.text() == str(self.rsTuple[4]):
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#00ff00';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("صحيح")
            self.listResultat.append(20)

        else:
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#ff0000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("خطأ")
            self.listResultat.append(0)

        result = sum(self.listResultat)
        self.label_resultat.setText(str(result) + "%")

    def checkAnswer3(self):

        if self.btnanswer3_2.text() == str(self.rsTuple[4]):
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#00ff00';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer2_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("صحيح")
            self.listResultat.append(20)

        else:
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#ff0000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer2_2.setText("NOT")
            self.btnanswer4_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("خطأ")
            self.listResultat.append(0)

        result = sum(self.listResultat)
        self.label_resultat.setText(str(result) + "%")

    def checkAnswer4(self):

        if self.btnanswer4_2.text() == str(self.rsTuple[4]):
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#00ff00';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer2_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("صحيح")
            self.listResultat.append(20)

        else:
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: black;font-size: 16px;border-radius: 7px;background-color:'#ff0000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            self.btnanswer1_2.setText("NOT")
            self.btnanswer3_2.setText("NOT")
            self.btnanswer2_2.setText("NOT")
            self.btnanswer2_2.setDisabled(True)
            self.btnanswer3_2.setDisabled(True)
            self.btnanswer4_2.setDisabled(True)
            self.btnanswer1_2.setDisabled(True)

            self.listReponse.append("خطأ")
            self.listResultat.append(0)

        result = sum(self.listResultat)
        self.label_resultat.setText(str(result) + "%")

#----------------------------------# DATABASE #-------------------------------#

    def demarer_new(self):
        maListe1.clear()
        self.findDataQuest()
        self.resetChamps()
        self.btn_find.setDisabled(False)

    def reset_continue(self):
        self.resetChamps()
        self.btn_find.setDisabled(False)
        self.btn_continue.setDisabled(True)
        self.i = 0
        self.comptage = 0
        self.labelQuestNumero.setText("0")
        self.lbl_reponse.clear()
        self.listReponse.clear()
        self.listResultat.clear()
        self.label_resultat.setText("0 %")

    def findDataQuest(self):

        indice1 = str(self.comboBoxCat_2.currentText()).strip()
        print("indice1 :", indice1)

        indice2 = str(self.comboBoxTyp_2.currentText()).strip()
        print("indice2 :", indice2)

        self.rsTuple = helper.find2(
            "SELECT * from tb_quiz1 WHERE categorie = (?) and m_type = (?)", (indice1, indice2))

        for x in self.rsTuple:
            maListe1.append(int(x[0]))

        print("maListe1 est debut-1:  = ", maListe1)
        shuffle(maListe1)

        # print("maListe1 est shufflee:  = ",maListe1 )

    def findUser(self):

        global maListe1

        try:

            self.btnanswer1_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer2_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer3_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
            self.btnanswer4_2.setStyleSheet(
                "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

            indice = int(maListe1[self.i])

            # print("indice = ",indice)
            maListe2.append(indice)
            print("maListe2: AVANT ", maListe2)
            self.labelQuestNumero.setText(str(self.i+1))

            self.rsTuple = helper.find(
                "SELECT * FROM tb_quiz1 WHERE id="+str(indice))
            self.maListe = []
            a = self.rsTuple[3]
            self.lbl_question.setText(a)
            b = self.rsTuple[4]
            # print(str(b))
            self.maListe.append(b)
            c = self.rsTuple[5]
            self.maListe.append(c)
            d = self.rsTuple[6]
            self.maListe.append(d)
            e = self.rsTuple[7]
            self.maListe.append(e)

            # print(self.maListe)
            shuffle(self.maListe)
            self.btnanswer1_2.setText(self.maListe[0])
            self.btnanswer2_2.setText(self.maListe[1])
            self.btnanswer3_2.setText(self.maListe[2])
            self.btnanswer4_2.setText(self.maListe[3])
            self.btnanswer1_2.setDisabled(False)
            self.btnanswer2_2.setDisabled(False)
            self.btnanswer3_2.setDisabled(False)
            self.btnanswer4_2.setDisabled(False)
            self.i += 1
            self.comptage += 1

            if self.comptage >= 5:

                self.btn_continue.setDisabled(False)
                self.btn_find.setDisabled(True)

                # print("-------------------")
                # print("maListe1 est: APRES = ", maListe1)
                # print("-------------------")
                # print("maListe2 est: APRES = ", maListe2)
                # print("-------------------")
                for elem in maListe1:
                    if elem not in maListe2:
                        maListe3.append(elem)
                        # print("maListe2 = ", elem[0])

                # print("maListe3 = ", maListe3)
                maListe1 = maListe3.copy()
                # print("maListe1 NEW = ", maListe1)
                maListe3.clear()
                maListe2.clear()

        except Exception:
            self.msg_display('خطأ', 'لا توجد بيانات اخرى')
            self.btn_continue.setDisabled(True)
            self.afficherResult()

    def afficherResult(self):
        self.lbl_reponse.clear()
        for i in range(len(self.listReponse)):

            text = self.lbl_reponse.text()
            self.lbl_reponse.setText(
                f" {text}  \n\n{str(i+1)} :-  السؤال : {self.listReponse[i]}  ")

    def resetChamps(self):
        self.btnanswer1_2.setText("الجواب 1")
        self.btnanswer2_2.setText("الجواب 2")
        self.btnanswer3_2.setText("الجواب 3")
        self.btnanswer4_2.setText("الجواب 4")

        self.btnanswer1_2.setStyleSheet(
            "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
        self.btnanswer2_2.setStyleSheet(
            "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
        self.btnanswer3_2.setStyleSheet(
            "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")
        self.btnanswer4_2.setStyleSheet(
            "QPushButton{color: white;font-size: 16px;border-radius: 7px;background-color:'#000000';border-bottom: 1px solid '#ffffff';}")

        self.lbl_reponse.clear()
        self.lbl_question.setText("")
        self.labelQuestNumero.setText("0")
        self.label_resultat.setText("0 %")

 #----------------timing--------------------

    def startTime(self):
        monTexte = self.lineEdit_temps.text()
        if monTexte != "":
            self.timer1.start()
        else:
            self.msg_display("خطأ", "  املأ الوقت")
            return

    def compteur(self):
        interv = int(self.lineEdit_temps.text())
        self.timer1.start(1000)
        # print(self.comptage2)
        self.comptage2 = self.comptage2 + 1
        self.lbl_TimeStart.setText(str(self.comptage2))
        if self.comptage2 == interv:
            self.lbl_TimeStart.setText("انتهى الوقت")
            self.comptage2 = 0
            self.timer1.stop()

#----------------FIN timing--------------------
# -----------------------------------------------

    def selectionComboChangeRead(self):

        if self.comboBoxCat_2.currentIndex() == 0:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("تاريخ")
            self.comboBoxTyp_2.addItem("جغرافية")

        if self.comboBoxCat_2.currentIndex() == 1:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")

        if self.comboBoxCat_2.currentIndex() == 2:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")

        if self.comboBoxCat_2.currentIndex() == 3:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")

        if self.comboBoxCat_2.currentIndex() == 4:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")

        elif self.comboBoxCat_2.currentIndex() == 5:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")
            self.comboBoxTyp_2.addItem("رياضيات")
            self.comboBoxTyp_2.addItem("فيزياء")
            self.comboBoxTyp_2.addItem("جغرافية_تاريخ")
            self.comboBoxTyp_2.addItem("التربية_الاسلامية")
            self.comboBoxTyp_2.addItem("علوم")
            self.comboBoxTyp_2.addItem("الاعلام_الالي")

        elif self.comboBoxCat_2.currentIndex() == 6:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")
            self.comboBoxTyp_2.addItem("رياضيات")
            self.comboBoxTyp_2.addItem("فيزياء")
            self.comboBoxTyp_2.addItem("جغرافية_تاريخ")
            self.comboBoxTyp_2.addItem("التربية_الاسلامية")
            self.comboBoxTyp_2.addItem("علوم")
            self.comboBoxTyp_2.addItem("الاعلام_الالي")

        elif self.comboBoxCat_2.currentIndex() == 7:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem("عربية")
            self.comboBoxTyp_2.addItem("اجنبية")
            self.comboBoxTyp_2.addItem("رياضيات")
            self.comboBoxTyp_2.addItem("فيزياء")
            self.comboBoxTyp_2.addItem("جغرافية_تاريخ")
            self.comboBoxTyp_2.addItem("التربية_الاسلامية")
            self.comboBoxTyp_2.addItem("علوم")
            self.comboBoxTyp_2.addItem("الاعلام_الالي")

        elif self.comboBoxCat_2.currentIndex() == 8:

            self.comboBoxTyp_2.clear()
            self.comboBoxTyp_2.addItem(u"عامة")

#     def afficher_tout_etudiants(self):
# #        cnn=sqlite3.connect("university.db")
# #        connection=get_sql_connection()
#         rs=connection.cursor()
#         sql = "SELECT * FROM Janvier24"
#         result=rs.execute(sql)
#         self.tabledetails.setRowCount(0)
#         for row_number, row_data in enumerate(result):
# #            print(row_number)
#             self.tabledetails.insertRow(row_number)
#             for column_number, data in enumerate(row_data):
#                 self.tabledetails.setItem(row_number, column_number, QTableWidgetItem(str(data)))
# #        cnn.close()


# ----------------------------------------------


    def msg_display(self, title, msg):
        self.msg.setWindowTitle(title)
        self.msg.setText(msg)
        self.msg.exec()

    def addimage1(self):
        #Add the image
        qpixmap = QPixmap('C:/allFiles/images/quiz57.png')
        self.label1.setPixmap(qpixmap)
        qpixmap = QPixmap('C:/allFiles/images/quiz36.png')
        self.label_3.setPixmap(qpixmap)
        qpixmap = QPixmap('C:/allFiles/images/quiz36.png')
        self.label_4.setPixmap(qpixmap)
        qpixmap = QPixmap('C:/allFiles/images/logbce.png')
        self.label_5.setPixmap(qpixmap)
# -----------------------------------------------


if __name__ == "__main__":
    MainApp = QtWidgets.QApplication(sys.argv)
    App = AnalogClock()
    App.show()
    sys.exit(MainApp.exec_())
