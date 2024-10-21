from PyQt5 import QtWidgets
from  ui.facturaView import FacturacionWindow

import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    facturaView = FacturacionWindow()
    facturaView.show()
    sys.exit(app.exec_())
    
