# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * 
from PyQt5 import QtWidgets, uic, QtCore
import sys
from sqliteHelper import *
from random import shuffle
# import datetime 
# import pytz
helper = SqliteHelper("C:/allFiles/QuizDb.db")

class MonQuiz(QtWidgets.QMainWindow,QPushButton):
    def __init__(self):
        super(MonQuiz, self).__init__()
        uic.loadUi('C:/allFiles/Db_QuizPM.ui',self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.maFenetre()
        self.msg=QMessageBox()
        self.addimage1()
        self.tableWidget.setColumnWidth(0,45)
        self.tableWidget.setColumnWidth(1,100)
        self.tableWidget.setColumnWidth(2,100)
      
        self.tableWidget.setColumnWidth(3,250)
        self.tableWidget.setColumnWidth(4,150)
        self.tableWidget.setColumnWidth(5,120)
        self.tableWidget.setColumnWidth(6,120)
        self.tableWidget.setColumnWidth(7,120)
        self.loadData()
        # self.imgShow()
        
        self.button = self.findChild(QPushButton, "btn_load")
        self.minimizeButton.clicked.connect(lambda: self.showMinimized())
        self.closeButton.clicked.connect(lambda: self.close())
      
        self.btn_insert_3.clicked.connect(self.addUser)
        self.btn_update_3.clicked.connect(self.updateUser)
        self.btn_delete_3.clicked.connect(self.deleteUser)
        self.btn_new_3.clicked.connect(self.vider)

        self.tableWidget.itemSelectionChanged.connect(self.selectionChanged)
              
        self.comboCat_3.currentIndexChanged.connect(self.selectionComboChangeWrite)

                                                      
    def loadData(self):
        # global indice1
        # self.combo1.clear()
        self.clearData()
        users = helper.select("SELECT * FROM tb_quiz1")

        for row_number, user in enumerate(users):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(user):
                cell =QTableWidgetItem(str(data))
                self.tableWidget.setItem(row_number,column_number,cell)
        

    def clearData(self):
        self.tableWidget.clearSelection()
        while(self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
            self.tableWidget.clearSelection()
            
        
    def addUser(self):
        cat=self.comboCat_3.currentText()
        m_type=self.comboTyp_3.currentText()

        quest = self.plainTextEdit_question.toPlainText()
        juste = self.plainTextEdit_juste.toPlainText()
        faux1 = self.plainTextEdit_faux1.toPlainText()
        faux2 = self.plainTextEdit_faux2.toPlainText()
        faux3 = self.plainTextEdit_faux3.toPlainText()
           

        if cat.strip(" ") != "" :
            
            user =(cat,m_type,quest,juste,faux1,faux2,faux3)
            helper.insert("INSERT INTO tb_quiz1 (categorie,m_type,question,juste,faux1,faux2,faux3) VALUES (?,?,?,?,?,?,?)", user)
            self.refresh()
            self.vider()
            self.msg_display("نجاح","تم التسجيل")
        else:
            self.msg_display("فشل","لم يتم التسجيل")
            
        
    def updateUser(self):
        try:
            id_update = self.getSelectedUserId()
            if id_update != "" :
            
    
                cat=self.comboCat_3.currentText()
                m_type=self.comboTyp_3.currentText()
                # niv=self.comboNiv_3.currentText()
                quest = self.plainTextEdit_question.toPlainText()
                juste = self.plainTextEdit_juste.toPlainText()
                faux1 = self.plainTextEdit_faux1.toPlainText()
                faux2 = self.plainTextEdit_faux2.toPlainText()
                faux3 = self.plainTextEdit_faux3.toPlainText()
                                    
                user =(cat,m_type,quest,juste,faux1,faux2,faux3)
                helper.edit("UPDATE tb_quiz1 SET categorie =?, m_type=?, question=?, juste=?, faux1=?, faux2=?, faux3=? WHERE id="+id_update, user)
                self.refresh()
                self.vider()
                self.msg_display("نجاح","تم التحديث")
                        
                
            else:
                self.msg_display("خطأ","لم يتم التحديث")
        except:
            self.msg_display("خطأ","اختر عنصر من الجدول")


    def deleteUser(self):
        message=QMessageBox.question(self, "حذف", "هل انت من متأكد من الحذف ",
                                     QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        if message == QMessageBox.Yes:
        
            try:
                id_delete = self.getSelectedUserId()
                print(str(id_delete))
            
                if id_delete != "":          
                    helper.delete("DELETE FROM tb_quiz1 WHERE id = "+id_delete)
                    self.refresh()        
                    self.vider()
                    self.msg_display("نجاح","تم الحذف")
                else:
                    self.msg_display("خطأ","لم يتم الحذف")
                    return
            except:            
                self.msg_display("خطأ","اختر عنصر من الجدول")
        
        else:
            QMessageBox.warning(QMessageBox(), 'تنبيه', 'ألغي أمر الحذف.')
        

    def refresh(self):
        self.clearData()
        self.loadData()
           
############################################################        
    def selectionComboChangeWrite(self):
        
        if self.comboCat_3.currentIndex() == 0:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("تاريخ")
            self.comboTyp_3.addItem("جغرافية")


            
        if self.comboCat_3.currentIndex() == 1:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("عربية")
            self.comboTyp_3.addItem("اجنبية")
            
        if self.comboCat_3.currentIndex() == 2:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("عربية")
            self.comboTyp_3.addItem("اجنبية")
            
        if self.comboCat_3.currentIndex() == 3:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("عربية")
            self.comboTyp_3.addItem("اجنبية")
            
        if self.comboCat_3.currentIndex() == 4:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("عربية")
            self.comboTyp_3.addItem("اجنبية")

            
        elif self.comboCat_3.currentIndex() == 5:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem(u"عربية")
            self.comboTyp_3.addItem(u"اجنبية")
            self.comboTyp_3.addItem(u"رياضيات")
            self.comboTyp_3.addItem(u"فيزياء") 
            self.comboTyp_3.addItem(u"جغرافية_تاريخ")
            self.comboTyp_3.addItem(u"التربية_الاسلامية")
            self.comboTyp_3.addItem(u"علوم")
            self.comboTyp_3.addItem(u"الاعلام_الالي")
                
        elif self.comboCat_3.currentIndex() == 6:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem(u"عربية")
            self.comboTyp_3.addItem(u"اجنبية")
            self.comboTyp_3.addItem(u"رياضيات")
            self.comboTyp_3.addItem(u"فيزياء") 
            self.comboTyp_3.addItem(u"جغرافية_تاريخ")
            self.comboTyp_3.addItem(u"التربية_الاسلامية")
            self.comboTyp_3.addItem(u"علوم")
            self.comboTyp_3.addItem(u"الاعلام_الالي")
            
        elif self.comboCat_3.currentIndex() == 7:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem(u"عربية")
            self.comboTyp_3.addItem(u"اجنبية")
            self.comboTyp_3.addItem(u"رياضيات")
            self.comboTyp_3.addItem(u"فيزياء") 
            self.comboTyp_3.addItem(u"جغرافية_تاريخ")
            self.comboTyp_3.addItem(u"التربية_الاسلامية")
            self.comboTyp_3.addItem(u"علوم")
            self.comboTyp_3.addItem(u"الاعلام_الالي")
            
            
        elif self.comboCat_3.currentIndex() == 8:
            
            self.comboTyp_3.clear()
            self.comboTyp_3.addItem("عامة")
            


           
    def selectionChanged(self):
        global selected_row
        selected_row = self.getSelectedRowId()
        user_id = self.getSelectedUserId()
        cat = self.tableWidget.item(selected_row, 1).text()
        m_type = self.tableWidget.item(selected_row, 2).text()
        # niv = self.tableWidget.item(selected_row, 3).text()
        quest = self.tableWidget.item(selected_row, 3).text()
        juste = self.tableWidget.item(selected_row, 4).text()
        faux1 = self.tableWidget.item(selected_row, 5).text()
        faux2 = self.tableWidget.item(selected_row, 6).text()
        faux3 = self.tableWidget.item(selected_row, 7).text()
                    
        self.comboCat_3.setCurrentText(cat)
        self.comboTyp_3.setCurrentText(m_type)
        # self.comboNiv_3.setCurrentText(niv)
        
        self.plainTextEdit_question.setPlainText(quest)
        self.plainTextEdit_juste.setPlainText(juste)
        self.plainTextEdit_faux1.setPlainText(faux1)
        self.plainTextEdit_faux2.setPlainText(faux2)
        self.plainTextEdit_faux3.setPlainText(faux3)
        
    def vider(self):
        self.plainTextEdit_question.setPlainText("")
        self.plainTextEdit_juste.setPlainText("")
        self.plainTextEdit_faux1.setPlainText("")
        self.plainTextEdit_faux2.setPlainText("")
        self.plainTextEdit_faux3.setPlainText("")
        
    def getSelectedRowId(self):
        return self.tableWidget.currentRow()
            
    def getSelectedUserId(self):
        return self.tableWidget.item(self.getSelectedRowId(),0).text()
        
        
    def maFenetre(self):

        self.setFixedSize(1250,650)
        # self.setWindowIcon(QIcon('chat.png'))         
    
                
    def msg_display(self,title,msg):
        self.msg.setWindowTitle(title)
        self.msg.setText(msg)
        self.msg.exec()
        
    def addimage1(self):
        #Add the image
        qpixmap = QPixmap('C:/allFiles/images/newQuiz20.png')
        self.label_3.setPixmap(qpixmap)
        qpixmap = QPixmap('C:/allFiles/images/newQuiz21.png')
        self.label.setPixmap(qpixmap)
        qpixmap = QPixmap('C:/allFiles/images/bd10.png')
        self.label_2.setPixmap(qpixmap)



        
def main():            
    app = QtWidgets.QApplication(sys.argv)
    window = MonQuiz()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
    
