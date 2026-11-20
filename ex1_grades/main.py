from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QSpinBox,
                               QTableWidget, QTableWidgetItem, QFileDialog,
                               QVBoxLayout, QHBoxLayout)
# the next two imports are only used by open_file (opens a file in its default program, on any OS)
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from About import About


class GradesWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.about_window = About()   # created once, but not visible until about_clicked calls show()

        # the data of the window - kept with self. so every method can use it
        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ''

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Grade Correction")
        self.setGeometry(100, 100, 520, 720)

        # step 1 of layouts: widgets without parent and without setGeometry
        self.title = QLabel("Grade Correction")
        self.title.setObjectName("title")           # lets style.qss style only this label (QLabel#title)

        # each button is connected to a method: the method runs when the button is clicked
        self.load_button = QPushButton("Load File")
        self.load_button.clicked.connect(self.load_clicked)

        self.update_button = QPushButton("Update File")
        self.update_button.clicked.connect(self.update_clicked)

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.about_clicked)

        self.bonus_label = QLabel("Bonus points (press ENTER):")

        # whole numbers only. returnPressed is the signal of the text box inside the spin box:
        # it fires when ENTER is pressed, so bonus_entered runs only then (not on every digit)
        self.bonus_spin = QSpinBox()
        self.bonus_spin.setRange(0, 100)
        self.bonus_spin.setValue(0)
        self.bonus_spin.lineEdit().returnPressed.connect(self.bonus_entered)

        # 50 rows, 3 columns, with the required column titles
        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Original Grades", "Corrected Grades"])

        # step 2: layouts. a row = QHBoxLayout, the rows go one under the other in a QVBoxLayout
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.update_button)
        buttons_layout.addWidget(self.about_button)

        bonus_layout = QHBoxLayout()
        bonus_layout.addWidget(self.bonus_label)
        bonus_layout.addWidget(self.bonus_spin)
        bonus_layout.addStretch()                   # pushes the label and spin box to the left

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title)
        main_layout.addLayout(buttons_layout)
        main_layout.addLayout(bonus_layout)
        main_layout.addWidget(self.table)

        # step 3: give the main layout to the window
        self.setLayout(main_layout)

    def update_table(self):
        # fills the table from the three lists. call it every time the lists change
        self.table.clearContents()
        for i in range(len(self.student_ids)):
            self.table.setItem(i, 0, QTableWidgetItem(str(self.student_ids[i])))
            self.table.setItem(i, 1, QTableWidgetItem(str(self.original_grades[i])))
            self.table.setItem(i, 2, QTableWidgetItem(str(self.corrected_grades[i])))

    def open_file(self, file_name):
        # opens a file with its default program (Excel for csv), on any operating system
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_name))

    def load_clicked(self):
        # the dialog returns the chosen path (and the filter, which we don't need)
        file_name, _ = QFileDialog.getOpenFileName(self, "Select students file", "", "CSV Files (*.csv)")
        if file_name ==  '':                                # the user closed the dialog without choosing
            return
        self.selected_file = file_name
        print(self.selected_file)

        # TODO (your code):
        # 1. save file_name in self.selected_file
        # 2. open the file for reading, skip the header line
        # 3. for every line: append the ID to self.student_ids and the grade to self.original_grades
        #    and the same grade to self.corrected_grades
        #    (tip: keep the ID as a string - a number would lose the leading zero)
        # 4. call self.update_table()

    def bonus_entered(self):
        bonus = self.bonus_spin.value()             # the number in the spin box

        # TODO (your code):
        # run over the two grade lists. Corrected grade = original grade + bonus, but not more than 100.
        # then call self.update_table()

    def update_clicked(self):
        # TODO (your code):
        # 1. overwrite self.selected_file: keep the original header line, write ID and corrected grade per line
        # 2. then call self.open_file(self.selected_file)
        pass

    def about_clicked(self):
        self.about_window.show()

    def closeEvent(self, event):
        # PySide6 calls this when the window closes. closes About too, so the program really ends
        self.about_window.close()


if __name__ == "__main__":
    app = QApplication()

    # load the design file once, before app.exec(). run the program from the folder that has style.qss
    with open("style.qss") as f:
        app.setStyleSheet(f.read())

    window = GradesWindow()
    window.show()
    app.exec()
