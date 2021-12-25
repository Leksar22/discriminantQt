import PyQt5.QtGui
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer
from io import BytesIO
import matplotlib.pyplot as plt
import sys

plt.rc('mathtext', fontset='cm')


class MyApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.window = uic.loadUi("untitled1.ui", self)

        self.onlyDouble = QtGui.QDoubleValidator()  # можно вводить только цифры
        self.window.lineEdit_1.setValidator(self.onlyDouble)
        self.window.lineEdit_2.setValidator(self.onlyDouble)
        self.window.lineEdit_3.setValidator(self.onlyDouble)

        self.eqt = QSvgWidget()
        self.c1 = QSvgWidget()
        self.c2 = QSvgWidget()

        self.window.verticalLayout_4.addWidget(self.eqt)
        self.window.verticalLayout_4.addWidget(self.c1)
        self.window.verticalLayout_4.addWidget(self.c2)

        self.window.lineEdit_1.textChanged.connect(self.to_calculate)
        self.window.lineEdit_2.textChanged.connect(self.to_calculate)
        self.window.lineEdit_3.textChanged.connect(self.to_calculate)

        # self.window.pushButton_1.clicked.connect(self.to_calculate)

    def to_calculate(self):
        A = self.window.lineEdit_1.text()
        B = self.window.lineEdit_2.text()
        C = self.window.lineEdit_3.text()
        try:
            A, B, C = [round(float(i.replace(',', '.').replace(' ', '')), 3) for i in [A, B, C]]
            # A, B, C = map(float, [A, B, C])
            discriminant = round(B ** 2 - 4 * A * C, 3)
            x1 = (-B + discriminant ** 0.5) / 2 / A
            x2 = (-B - discriminant ** 0.5) / 2 / A
            if isinstance(x1, complex) or isinstance(x2, complex):
                x1, x2 = round(x1.real, 3) + round(x1.imag, 3) * 1j, round(x2.real, 3) + round(x2.imag, 3) * 1j
            else:
                x1, x2 = round(x1, 3), round(x2, 3)

            EQUATION = str(A) + r'x^2' + f'{B:+}' + r'x' + f'{C:+}' + r'=0'

            FORMULA1 = r'x_1 = \frac{-b + \sqrt{D}}{2a} =' \
                       r' \frac{{' + str(-B) + '} + \sqrt{' + str(discriminant) + '}}{' + str(2 * A) + '} = ' + str(x1)

            FORMULA2 = r'x_2 = \frac{-b - \sqrt{D}}{2a} =' \
                       r' \frac{{' + str(-B) + '} - \sqrt{' + str(discriminant) + '}}{' + str(2 * A) + '} = ' + str(x2)

            eqt = self.__tex2svg(EQUATION)
            c1 = self.__tex2svg(FORMULA1)
            c2 = self.__tex2svg(FORMULA2)
            self.eqt.load(eqt)
            self.eqt.setFixedSize(QSvgRenderer(eqt).defaultSize())

            self.c1.load(c1)
            self.c1.setFixedSize(QSvgRenderer(c1).defaultSize())

            self.c2.load(c2)
            self.c2.setFixedSize(QSvgRenderer(c2).defaultSize())

        except:
            print('asdsad')
            # self.window.label_3.setText('Заполните все поля')

    @staticmethod
    def __tex2svg(formula, fontsize=34, dpi=300):
        """Render TeX formula to SVG.
        Args:
            formula (str): TeX formula.
            fontsize (int, optional): Font size.
            dpi (int, optional): DPI.
        Returns:
            str: SVG render.
        """

        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize, color='white')

        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                    bbox_inches='tight', pad_inches=0.5)
        plt.close(fig)

        output.seek(0)
        return output.getvalue()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = MyApp()
    win.show()

    sys.exit(app.exec())
