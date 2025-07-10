from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QMessageBox, QStackedWidget, QTableWidget, QTableWidgetItem
from calculator import *
import sqlite3
import sys
import matplotlib.pyplot as plt

con = sqlite3.connect("expenses.sqlite3")
cur = con.cursor()
data = cur.execute("SELECT * FROM expenses").fetchall()
print(data)
headers = [description[0] for description in cur.description]

class Calculator(QMainWindow, Ui_Calculator):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Calculator++")

        '''bazis tablewidgetshi motavseba'''
        self.datatable.setRowCount(len(data))
        self.datatable.setColumnCount(len(data[0]))
        self.datatable.setHorizontalHeaderLabels(headers)
        self.orderbox.currentIndexChanged.connect(self.load_data_sorted)

        #mtliani bazis motavseba
        self.load_data_to_table()
        self.registerbutton.clicked.connect(lambda: self.register())
        #washlis metodi
        self.deletebutton.clicked.connect(lambda: self.delete_by_id())



        '''buttons'''
        self.expression = ""

        self.button0.clicked.connect(lambda: self.add_input('0'))
        self.button1.clicked.connect(lambda: self.add_input('1'))
        self.button2.clicked.connect(lambda: self.add_input('2'))
        self.button3.clicked.connect(lambda: self.add_input('3'))
        self.button4.clicked.connect(lambda: self.add_input('4'))
        self.button5.clicked.connect(lambda: self.add_input('5'))
        self.button6.clicked.connect(lambda: self.add_input('6'))
        self.button7.clicked.connect(lambda: self.add_input('7'))
        self.button8.clicked.connect(lambda: self.add_input('8'))
        self.button9.clicked.connect(lambda: self.add_input('9'))

        self.button_mul.clicked.connect(lambda: self.add_input(' × '))
        self.button_div.clicked.connect(lambda: self.add_input(' ÷ '))
        self.button_plus.clicked.connect(lambda: self.add_input(' + '))
        self.button_min.clicked.connect(lambda: self.add_input(' - '))
        self.button_flo.clicked.connect(lambda: self.add_comma(','))

        self.button_clear.clicked.connect(lambda: self.clearall())
        self.button_cleare.clicked.connect(lambda: self.clear_entry())
        self.button_del.clicked.connect(lambda: self.delete_last())

        self.button_equal.clicked.connect(lambda: self.equal())

        self.button_pm.clicked.connect(lambda: self.negative())

        self.button_percent.clicked.connect(lambda: self.add_input(' % '))
        self.button_pow.clicked.connect(lambda: self.add_input(' ^ '))
        self.button_sqrt.clicked.connect(lambda: self.add_input(' √ '))

        '''show matplotlib when clicking a button'''
        self.statisticbutton.clicked.connect(lambda: show_statistics())


        '''currency'''
        self.currency_rates = {
            'GEL ₾ ': {'GEL ₾ ': 1.0, 'USD $': 0.37, 'EUR €': 0.34, 'JPY ¥': 0.018, 'GBP £': 0.29, 'RUB ₽': 33.2,
                      'CNY ¥': 2.69},
            'USD $': {'GEL ₾ ': 2.70, 'USD $': 1.0, 'EUR €': 0.92, 'JPY ¥': 147.0, 'GBP £': 0.78, 'RUB ₽': 90.0,
                      'CNY ¥': 7.30},
            'EUR €': {'GEL ₾ ': 2.94, 'USD $': 1.09, 'EUR €': 1.0, 'JPY ¥': 160.0, 'GBP £': 0.85, 'RUB ₽': 98.0,
                      'CNY ¥': 7.90},
            'JPY ¥': {'GEL ₾ ': 0.0067, 'USD $': 0.0068, 'EUR €': 0.0063, 'JPY ¥': 1.0, 'GBP £': 0.0053, 'RUB ₽': 0.61,
                      'CNY ¥': 0.050},
            'GBP £': {'GEL ₾ ': 3.39, 'USD $': 1.28, 'EUR €': 1.18, 'JPY ¥': 189.0, 'GBP £': 1.0, 'RUB ₽': 116.0,
                      'CNY ¥': 9.30},
            'RUB ₽': {'GEL ₾ ': 0.030, 'USD $': 0.011, 'EUR €': 0.010, 'JPY ¥': 1.63, 'GBP £': 0.0086, 'RUB ₽': 1.0,
                      'CNY ¥': 0.080},
            'CNY ¥': {'GEL ₾ ': 0.37, 'USD $': 0.14, 'EUR €': 0.13, 'JPY ¥': 20.0, 'GBP £': 0.11, 'RUB ₽': 12.5,
                      'CNY ¥': 1.0}
        }

        self.button0_2.clicked.connect(lambda: self.add_convert('0'))
        self.button1_2.clicked.connect(lambda: self.add_convert('1'))
        self.button2_2.clicked.connect(lambda: self.add_convert('2'))
        self.button3_2.clicked.connect(lambda: self.add_convert('3'))
        self.button4_2.clicked.connect(lambda: self.add_convert('4'))
        self.button5_2.clicked.connect(lambda: self.add_convert('5'))
        self.button6_2.clicked.connect(lambda: self.add_convert('6'))
        self.button7_2.clicked.connect(lambda: self.add_convert('7'))
        self.button8_2.clicked.connect(lambda: self.add_convert('8'))
        self.button9_2.clicked.connect(lambda: self.add_convert('9'))
        self.button_clear_2.clicked.connect(lambda: self.clearall())
        self.button_flo_2.clicked.connect(lambda: self.add_comma(','))
        self.convertbutton.clicked.connect(lambda: self.convert_currency())


        '''combo box-it gverdebis shecvla'''
        self.comboBox.currentTextChanged.connect(self.change_page)
        self.comboBox_2.currentTextChanged.connect(self.change_page1)
        self.comboBox_3.currentTextChanged.connect(self.change_page2)

    def negative(self):
        if self.expression:
            if self.expression.startswith('-'):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression
            self.label.setText(self.expression)

    def add_input(self, c):
            self.expression += c
            self.label.setText(self.expression)

    def add_convert(self,c):
        self.expression += c
        self.converterin.setText(self.expression)


    def equal(self):
        sym = self.expression.split(' ')
        # print("Initial symbols:", sym)

        i = 0
        while i < len(sym):
            try:
                if sym[i] == '×':
                    a = float(sym[i - 1].replace(',', '.'))
                    b = float(sym[i + 1].replace(',', '.'))
                    result = a * b
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                elif sym[i] == '÷':
                    a = float(sym[i - 1].replace(',', '.'))
                    b = float(sym[i + 1].replace(',', '.'))
                    if b == 0:
                        self.label.setText("Divide by 0!")
                        return
                    result = a / b
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                else:
                    i += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Calculation error: {str(e)}")
                self.clearall()
                return

        i = 0
        while i < len(sym):
            try:
                if sym[i] == '+':
                    a = float(sym[i - 1].replace(',', '.'))
                    b = float(sym[i + 1].replace(',', '.'))
                    result = a + b
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                elif sym[i] == '-':
                    a = float(sym[i - 1].replace(',', '.'))
                    b = float(sym[i + 1].replace(',', '.'))
                    result = a - b
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                else:
                    i += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Calculation error: {str(e)}")
                self.clearall()
                return
        i = 0
        while i < len(sym):
            try:
                '''axarisxeba'''
                if sym[i] == '^':
                    a = float(sym[i - 1].replace(',', '.'))
                    b = float(sym[i + 1].replace(',', '.'))
                    result = a ** b
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                #fesvi
                elif sym[i] == '√':
                    a = float(sym[i + 1].replace(',', '.'))  # x
                    b = float(sym[i - 1].replace(',', '.'))  # y
                    if a < 0 and b % 2 == 0:
                        self.label.setText("Invalid root!")
                        return
                    result = a ** (1 / b)
                    sym[i - 1:i + 2] = [str(result)]
                    i = 0
                #procenti
                elif sym[i] == '%':
                    a = float(sym[i - 1].replace(',', '.'))
                    result = a / 100
                    sym[i - 1:i + 1] = [str(result)]
                    i = 0
                else:
                    i += 1
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Calculation error: {str(e)}")
                self.clearall()
                return

        self.label.setText(sym[0])
        self.expression = sym[0]

        self.label.setText(sym[0])
        self.expression = sym[0]

    def add_comma(self, c):
        operators = [' + ', ' - ', ' × ', ' ÷ ', ' ^ ', ' √ ', ' % ']

        if c in operators:
            if not self.expression or self.expression.endswith(tuple(operators)):
                return

        if c == ',':
            parts = self.expression.strip().split(' ')
            last_token = parts[-1] if parts else ''
            if ',' in last_token:
                return

        self.expression += c
        self.label.setText(self.expression)
        self.converterin.setText(self.expression)

    def clearall(self):
        self.expression = ""
        self.label.setText("0")
        self.converterin.setText("0")
        self.converterout.setText('0')

    def clear_entry(self):
        if not self.expression:
            return

        sym = self.expression.strip().split(' ')
        if sym:
            sym.pop()  #
            self.expression = ' '.join(sym)
            self.label.setText(self.expression)
        else:
            self.expression = ""
            self.label.setText("")

    def delete_last(self):
        if not self.expression:
            return
        if self.expression.endswith(' '):
            self.expression = self.expression[:-3]
        else:
            self.expression = self.expression[:-1]

        self.label.setText(self.expression)


    '''gverdebis shecvla'''
    def change_page(self):
        if self.comboBox.currentText() == "Calculator":
            self.stackedWidget.setCurrentWidget(self.page3)
            self.comboBox.setCurrentText("Calculator")
        elif self.comboBox.currentText() == "Currency Converter":
            self.stackedWidget.setCurrentWidget(self.page4)
            self.comboBox_2.setCurrentText("Currency Converter")
        elif self.comboBox.currentText() == "Data":
            self.stackedWidget.setCurrentWidget(self.page5)
            self.comboBox_3.setCurrentText("Data")

    def change_page1(self):
        if self.comboBox_2.currentText() == "Calculator":
            self.stackedWidget.setCurrentWidget(self.page3)
            self.comboBox.setCurrentText("Calculator")
        elif self.comboBox_2.currentText() == "Currency Converter":
            self.stackedWidget.setCurrentWidget(self.page4)
            self.comboBox_2.setCurrentText("Currency Converter")
        elif self.comboBox_2.currentText() == "Data":
            self.stackedWidget.setCurrentWidget(self.page5)
            self.comboBox_3.setCurrentText("Data")

    def change_page2(self):
        if self.comboBox_3.currentText() == "Calculator":
            self.stackedWidget.setCurrentWidget(self.page3)
            self.comboBox.setCurrentText("Calculator")
        elif self.comboBox_3.currentText() == "Currency Converter":
            self.stackedWidget.setCurrentWidget(self.page4)
            self.comboBox_2.setCurrentText("Currency Converter")
        elif self.comboBox_3.currentText() == "Data":
            self.stackedWidget.setCurrentWidget(self.page5)
            self.comboBox_3.setCurrentText("Data")


    '''convert'''
    def convert_currency(self):
        try:
            amount = float(self.converterin.text())
            from_currency = self.currency1.currentText()
            to_currency = self.currency2.currentText()
            rate = self.currency_rates[from_currency][to_currency]
            converted_amount = amount * rate
            self.converterout.setText(f"{converted_amount:.2f}")
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number first")

    '''bazaze mushaoba'''

    def load_data_to_table(self):
        conn = sqlite3.connect("expenses.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses")
        data = cursor.fetchall()
        headers = [description[0] for description in cursor.description]

        self.datatable.setRowCount(len(data))
        self.datatable.setColumnCount(len(headers))
        self.datatable.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.datatable.setItem(row_index, col_index, item)

        conn.close()

    def register(self):
        idd = self.datatable.rowCount() + 1
        rent = self.rentedit.text()
        education = self.educationedit.text()
        food = self.foodedit.text()
        clothing = self.clothingedit.text()
        entertainment = self.entertainmentedit.text()
        debt = self.debtedit.text()

        # Radio button value
        if self.radioyes.isChecked():
            owns = "Yes"
        elif self.r.isChecked():
            owns = "No"
        else:
            owns = None

        if not all([rent, education, food, clothing, entertainment, debt, owns]):
            QMessageBox.warning(self, "Missing data", "Please fill in all fields.")
            return

        try:
            conn = sqlite3.connect("expenses.sqlite3")
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO expenses (Id, rent, education, food, clothing, entertainment, debt, 'Owns appartement y/n')
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (idd, rent, education, food, clothing, entertainment, debt, owns))

            conn.commit()
            conn.close()

            QMessageBox.information(self, "Success", "Data saved successfully.")

            # Clear inputs
            self.rentedit.clear()
            self.educationedit.clear()
            self.foodedit.clear()
            self.clothingedit.clear()
            self.entertainmentedit.clear()
            self.debtedit.clear()
            self.radioyes.setChecked(False)
            self.r.setChecked(False)

            self.load_data_to_table()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))
    '''bazidan amoshla id-is mixedvit'''
    def delete_by_id(self):
        id_rem = self.idedit.text()
        try:
            conn = sqlite3.connect("expenses.sqlite3")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (id_rem,))
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def delete_by_id(self):
        id_rem = self.idedit.text().strip()
        if not id_rem.isdigit():
            QMessageBox.warning(self, "Invalid ID", "Please enter a valid numeric ID")
            return
        try:
            conn = sqlite3.connect("expenses.sqlite3")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE Id = ?", (int(id_rem),))
            if cursor.rowcount == 0:
                QMessageBox.information(self, "Not Found", f"No entry with ID {id_rem} found.")
            else:
                QMessageBox.information(self, "Deleted", f"Entry with ID {id_rem} deleted.")
            conn.commit()
            conn.close()
            self.load_data_to_table()
            self.idedit.clear()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def load_data_sorted(self):
        column_name = self.orderbox.currentText()
        try:
            conn = sqlite3.connect("expenses.sqlite3")
            cursor = conn.cursor()

            if column_name not in headers:
                column_name = headers[0]

            currency_columns = ['Rent', 'Education', 'Food', 'Clothing', 'Entertainment', 'Debt']

            if column_name in currency_columns:
                k = f"SELECT * FROM expenses ORDER BY CAST(REPLACE([{column_name}], '$', '') AS REAL)"
            else:
                k = f"SELECT * FROM expenses ORDER BY [{column_name}]"

            cursor.execute(k)
            data = cursor.fetchall()

            self.datatable.setRowCount(len(data))
            self.datatable.setColumnCount(len(headers))
            self.datatable.setHorizontalHeaderLabels(headers)

            for row_idx, row_data in enumerate(data):
                for col_idx, cell in enumerate(row_data):
                    self.datatable.setItem(row_idx, col_idx, QTableWidgetItem(str(cell)))

            conn.close()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", str(e))


'''matplotlib'''
def show_statistics():
    conn = sqlite3.connect('expenses.sqlite3')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    #1
    c.execute("SELECT Rent, Education, Food, Clothing, Entertainment, Debt FROM expenses;")
    expense_data = c.fetchall()

    categories = ['Rent', 'Education', 'Food', 'Clothing', 'Entertainment', 'Debt']
    totals = [0] * len(categories)

    for row in expense_data:
        for i, value in enumerate(row):
            numeric_value = int(value.replace('$', '').strip()) if value else 0
            totals[i] += numeric_value

    fig1, ax1 = plt.subplots()
    bar_colors = ['tab:blue', 'tab:green', 'tab:red', 'tab:orange', 'tab:purple', 'tab:brown']
    ax1.bar(categories, totals, color=bar_colors)

    for i, total in enumerate(totals):
        ax1.text(i, total + 100, str(total), ha='center')

    ax1.set_ylabel('Total Expenses ($)')
    ax1.set_title('Total Expenses by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    #2
    c.execute("SELECT [Owns appartement y/n] FROM expenses")
    data = c.fetchall()

    yes_count = sum(1 for row in data if row[0] == 'Yes')
    no_count = sum(1 for row in data if row[0] == 'No')

    labels = ['Yes', 'No']
    sizes = [yes_count, no_count]

    fig2, ax2 = plt.subplots()
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax2.set_title("Owns Apartment (Yes / No)")

    conn.close()

    plt.show()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())

