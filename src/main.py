"""
Main module for the AI Field Commander project.

This module initializes and runs the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from aifield.gui import MainWindow


def main():
    """
            The main entry point for the application.
        """
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
