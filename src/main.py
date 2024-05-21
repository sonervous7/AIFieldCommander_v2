import sys
from PyQt5.QtWidgets import QApplication
from src.aifield.gui import MainWindow
from aifield.simulation import Simulation


if __name__ == '__main__':
    # simulation = Simulation(50, 0.2, "KNN", "Horizontal", 200)
    # print(simulation.board.array)
    # simulation.simulate()
    sys._excepthook = sys.excepthook


    def exception_hook(exctype, value, traceback):
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    # NALEZALO DODAC _EXCEPTHOOK ABY WYKRYL UKRYTE SILENT ERRORY

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


