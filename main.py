import sys
import math
import ast
import sqlite3

from operator import add, sub, truediv, mul
from typing import Union, Optional
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton,QVBoxLayout, QWidget, QLineEdit
from calculator import Ui_MainWindow
from PyQt6.QtGui import QFontDatabase 
from historycal import HistoryWindow

mine_operation = {
    '+': add,
    '*': mul,
    '-': sub,
    '/': truediv
}
#label -> вверх, le_enty -> низ
# Наследуемся от виджета из PyQt6.QtWidgets и от класса с интерфейсом
class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Calculator')
        self.label.setText('0')
        self.history_window = HistoryWindow()
        layout = QVBoxLayout()
        self.result_display = QLineEdit()


        # Кнопка "История"
        self.history_button = QPushButton("История")
        
        # Подключение кнопки к методу show_history
        self.history_button.clicked.connect(self.show_history)
        
        # Добавление кнопки в layout
        layout.addWidget(self.history_button)

        # Псписок строк
        self.historylist = []


        # Окно истории (по умолчанию None)
        self.history_window = None


        # 0-9
        self._0_.clicked.connect(lambda: self.numbers('0'))
        self._1_.clicked.connect(lambda: self.numbers('1'))
        self._2_.clicked.connect(lambda: self.numbers('2'))
        self._3_.clicked.connect(lambda: self.numbers('3'))
        self._4_.clicked.connect(lambda: self.numbers('4'))
        self._5_.clicked.connect(lambda: self.numbers('5'))
        self._6_.clicked.connect(lambda: self.numbers('6'))
        self._7_.clicked.connect(lambda: self.numbers('7'))
        self._8_.clicked.connect(lambda: self.numbers('8'))
        self._9_.clicked.connect(lambda: self.numbers('9'))
        # # процент, СЕ, С и стереть
        self.prosent.clicked.connect(self.prosentik)
        self.CE.clicked.connect(self.clear)
        self.C.clicked.connect(self.clear_all)
        self.steret.clicked.connect(self.backspace)
        # # 1/x, x**2, корень x, деление
        self._1_na_x.clicked.connect(self.one_na_num)
        self.x_in_2.clicked.connect(self.stepen)
        self.root_koren_.clicked.connect(self.sqr)
        self.delenie.clicked.connect(lambda: self.math_oper('/'))
        # # умножить, минус, плюс, равно
        self.mnogenie.clicked.connect(lambda: self.math_oper('*'))
        self.minus.clicked.connect(lambda: self.math_oper('-'))
        self.plus.clicked.connect(lambda: self.math_oper('+'))
        self.ravno.clicked.connect(self.schet)
        # # не целое, плюс/минус
        self.ne_seloe.clicked.connect(self.add_point)
        self.plus_or_minus.clicked.connect(self.negate)
        # история, закрыть историю 
        self.history.clicked.connect(self.show_history)
        #self.close_b.connect.connect(self.close_history)
        


    def numbers(self, btn_text: str) -> None:
        if self.le_enty.text() == '0':
            self.le_enty.setText(btn_text)
        else:
            self.le_enty.setText(self.le_enty.text() + btn_text)


    def backspace(self) -> None:
        enh = self.le_enty.text()

        if len(enh) != 1:
            if len(enh) == 2 and '-' in enh:
                self.le_enty.setText('0')
            else:
                self.le_enty.setText(enh[:-1])
        else:
            self.le_enty.setText('0')


    def clear_all(self):
        self.le_enty.setText('0')
        self.le_enty.clear()
        self.label.clear()
        self.le_enty.setText('0')

    def clear(self):
        self.le_enty.setText('0')
        self.label.setText('0')

    # точка 
    def add_point(self) -> None:
        self.le_enty.setText(self.le_enty.text() + '.')


    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.deletelast_zero(self.le_enty.text())

        if not self.label.text() or self.sign_fr_label() == '=':
            self.label.setText(entry + f' {btn.text()} ')
            self.le_enty.setText('0')

    def get_e_n(self) -> Union[int, float]:
        enh = self.le_enty.text().strip(".")

        return float(enh) if "." in enh else int(enh)
    #число из label
    def num_fr_label(self) -> Union[int, float, None]:
        if self.label.text():
            ttt =  self.label.text().strip(".").split()[0]
            return float(ttt) if '.' in ttt else int(ttt)

    #знак из label
    def sign_fr_label(self) -> Optional[str]:
        if self.label.text():
           return self.label.text().strip(".").split()[-1] 

    def schet(self) -> Optional[str]:
        try:
            # Получаем введенное выражение
            expression = self.le_enty.text()  # Это строка, которую ввел пользователь
            # Выполняем вычисления
            entry = eval(expression)  # Результат вычисления

            # Отображаем результат
            self.label.setText(str(entry))
            self.le_enty.setText(str(entry))  # Отображаем результат в поле ввода

            # Добавляем выражение и результат в историю
            self.historylist.append(f"{expression} = {entry}")  # Добавляем правильный формат

            # Обновляем окно истории, если оно открыто
            if self.history_window is not None:
                self.history_window.update_history(self.historylist)

        except ZeroDivisionError:
            self.le_enty.setText('Error, Zero')
        except Exception:
            self.le_enty.setText('Error')




    # убрать последние нули, долой!
    @staticmethod
    def deletelast_zero(num: str) -> str:
        n = str(float(num))
        return n[:2] if n[-2:] == '.0' else n



    def math_oper(self, math_sign: str) -> None:
        temp = self.le_enty.text()
        btn = self.sender()

        if not temp:
            self.add_temp(math_sign)
        else:
            if self.sign_fr_label() != math_sign:
                if self.sign_fr_label() == '=':
                    self.add_temp(math_sign)
                else:
                    self.le_enty.setText(temp + f' {math_sign} ')
            else:
                self.le_enty.setText(self.schet() + f' {math_sign}')



    def negate(self):
        enh = self.le_enty.text()

        if '-' not in enh:
            if enh != '0':
                enh = '-' + enh
        else:
            enh = enh[1:]

        self.le_enty.setText(enh)


    def clear_label(self) -> None:
        if self.sign_fr_label() == '=':
            self.label.clear()


    def stepen(self):
        entry = self.sender().text()
        if entry == '^' or entry == 'Х²' or entry == 'х²' or entry == 'X²' or entry == 'x²':
            entry = '**'
        self.le_enty.setText(self.le_enty.text() + entry)

    def sqr(self):
        try:
            entry = float(self.le_enty.text())
            res = math.sqrt(entry)
            self.le_enty.setText(str(res))
        except ValueError:
            self.le_enty.setText('Error')

    def one_na_num(self):
        try:
            entry = float(self.le_enty.text())
            if entry == 0:
                self.le_enty.setText('Error,zero')
            else:
                res = 1 / entry
                self.le_enty.setText(str(res))
        except ValueError:
            self.le_enty.setText('Error')

    def prosentik(self):
        try:
            entry = float(self.le_enty.text())
            res = entry // 100 
            self.le_enty.setText(str(res))
        except ValueError:
            self.le_enty.setText('Error')



    def show_history(self):
        if self.history_window is None:
            # Создаем окно истории и передаем список
            self.history_window = HistoryWindow(self.historylist)
        else:
            # Обновляем содержимое окна истории
            self.history_window.update_history(self.historylist)

        self.history_window.show()
        self.history_window.raise_()

    def close_history(self):
        """Закрытие окна истории."""
        if self.history_window is not None:
            self.history_window.close()
 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = MyWidget()
    calculator.show()
    sys.exit(app.exec())