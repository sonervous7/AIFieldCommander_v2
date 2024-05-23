import tracemalloc
from PyQt5.QtGui import QBrush
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QPushButton,
    QFormLayout,
    QDoubleSpinBox,
    QTextEdit,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QTabWidget,
)
from PyQt5.QtCore import Qt, QTimer

from aifield.simulation import Simulation


class MainWindow(QWidget):
    """
    A class to represent the main window of the AI Field Commander simulation application.

    Attributes:
        layout (QVBoxLayout): The main layout of the window.
        formLayout (QFormLayout): The layout for the form inputs.
        amount_of_soldiers_input (QLineEdit): Input field for the amount of soldiers.
        classifier_input (QComboBox): Dropdown menu for selecting the classifier.
        mine_probability_input (QDoubleSpinBox): Input field for the mine probability.
        mine_probability_label (QLabel): Label for the mine probability input field.
        size_of_board_input (QSpinBox): Input field for the size of the board.
        path_type_input (QComboBox): Dropdown menu for selecting the path type.
        tabs (QTabWidget): Tab widget containing the board visualization and log.
        board_view (QGraphicsView): Graphics view for the board visualization.
        board_scene (QGraphicsScene): Graphics scene for the board visualization.
        simulation_output (QTextEdit): Text area for displaying the simulation log.
        simulation (Simulation): The simulation instance.
        simulation_generator (generator): The generator for the simulation steps.
        timer (QTimer): Timer for updating the simulation steps.
        board_items (dict): Dictionary to store the graphical items representing the board cells.
        soldier_item (QGraphicsRectItem): Graphical item representing the soldier's position.
        board_size (int): The size of the board.
        cell_size (int): The size of each cell in the board visualization.

    Methods:
        initUI(): Initializes the user interface.
        run_simulation(): Starts the simulation with the specified parameters.
        init_board_visualization(size_of_board): Initializes the board visualization.
        update_simulation(): Updates the simulation and the board visualization.
        update_board_visualization(i, j): Updates the color of a cell in the board visualization.
        display_simulation_results(): Displays the results of the simulation in the log.
    """

    def __init__(self):
        """
        Initializes the main window.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initializes the user interface of the main window.
        """
        self.layout = QVBoxLayout()

        self.formLayout = QFormLayout()

        # Amount of Soldiers
        self.amount_of_soldiers_input = QLineEdit()
        self.amount_of_soldiers_input.setText("100")
        self.formLayout.addRow(QLabel("Amount of Soldiers"), self.amount_of_soldiers_input)

        # Classifier Name
        self.classifier_input = QComboBox()
        classifiers = [
            "RandomForest",
            "GradientBoosting",
            "LogisticRegression",
            "KNN",
            "SVM",
            "DecisionTree",
            "DummyClassifier",
            "GaussianNB",
            "LinearSVC",
        ]
        self.classifier_input.addItems(classifiers)
        self.classifier_input.setCurrentText("KNN")
        self.formLayout.addRow(QLabel("Classifier"), self.classifier_input)

        # Mine Probability
        self.mine_probability_input = QDoubleSpinBox()
        self.mine_probability_input.setRange(0.1, 0.9)
        self.mine_probability_input.setSingleStep(0.1)
        self.mine_probability_input.setValue(0.2)
        self.mine_probability_input.setDecimals(2)
        self.formLayout.addRow(QLabel("Mine Probability [0.1 to 0.9]"), self.mine_probability_input)

        # Expected value label for Mine Probability
        self.mine_probability_label = QLabel("Expected value from 0 to 1")
        self.formLayout.addRow(self.mine_probability_label)

        # Size of Board
        self.size_of_board_input = QSpinBox()
        self.size_of_board_input.setRange(5, 20)
        self.size_of_board_input.setValue(10)
        self.formLayout.addRow(QLabel("Size of Board"), self.size_of_board_input)

        # Path Type
        self.path_type_input = QComboBox()
        path_types = ["Horizontal", "Diagonal"]
        self.path_type_input.addItems(path_types)
        self.formLayout.addRow(QLabel("Path Type"), self.path_type_input)

        self.layout.addLayout(self.formLayout)

        # Run Simulation Button
        run_button = QPushButton("Run Simulation")
        run_button.clicked.connect(self.run_simulation)
        self.layout.addWidget(run_button)

        # Tab Widget
        self.tabs = QTabWidget()

        # Board Visualization
        self.board_view = QGraphicsView()
        self.board_scene = QGraphicsScene()
        self.board_view.setScene(self.board_scene)
        self.tabs.addTab(self.board_view, "Board Visualization")

        # Simulation Output Log
        self.simulation_output = QTextEdit()
        self.simulation_output.setReadOnly(True)
        self.simulation_output.setMinimumHeight(200)
        self.tabs.addTab(self.simulation_output, "Logs and Results")

        self.tabs.setCurrentIndex(0)  # Set the board tab as the default

        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)
        self.setWindowTitle("Ai Field Commander")
        self.setGeometry(300, 300, 800, 600)

    def run_simulation(self):
        """
        Starts the simulation with the specified parameters.
        """
        size_of_board = self.size_of_board_input.value()
        mine_probability = self.mine_probability_input.value()
        classifier_name = self.classifier_input.currentText()
        type_of_path = self.path_type_input.currentText()
        amount_of_soldiers = int(self.amount_of_soldiers_input.text())

        self.simulation = Simulation(size_of_board, mine_probability, classifier_name, type_of_path, amount_of_soldiers)

        # Initialize board visualization
        self.init_board_visualization(size_of_board)

        # Start memory tracking
        tracemalloc.start()

        # Run simulation step by step
        self.simulation_generator = self.simulation.simulate()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        if size_of_board <= 10:
            self.timer.start(150)  # Update every 1000 ms (1 second)
        else:
            self.timer.start(50)

    def init_board_visualization(self, size_of_board):
        """
        Initializes the board visualization.

        Args:
            size_of_board (int): The size of the board.
        """
        self.board_scene.clear()
        self.board_items = {}
        self.board_size = size_of_board
        self.cell_size = 20

        for i in range(size_of_board):
            for j in range(size_of_board):
                rect = QGraphicsRectItem(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)
                rect.setBrush(QBrush(Qt.white))
                self.board_scene.addItem(rect)
                self.board_items[(i, j)] = rect

        self.soldier_item = QGraphicsRectItem(0, 0, self.cell_size, self.cell_size)
        self.soldier_item.setBrush(QBrush(Qt.blue))
        self.board_scene.addItem(self.soldier_item)

    def update_simulation(self):
        """
        Updates the simulation and the board visualization.
        """
        try:
            i, j = next(self.simulation_generator)
            self.update_board_visualization(i, j)
        except StopIteration:
            self.timer.stop()
            self.display_simulation_results()

    def update_board_visualization(self, i, j):
        """
        Updates the color of a cell in the board visualization.

        Args:
            i (int): The x-coordinate of the cell.
            j (int): The y-coordinate of the cell.
        """
        if (i, j) not in self.board_items:
            return

        current_label = self.simulation.board.array[i][j]
        if current_label == 1:
            color = Qt.yellow  # Mine
        elif current_label == 2:
            color = Qt.red  # Bomb
        else:
            color = Qt.green  # Safe

        self.board_items[(i, j)].setBrush(QBrush(color))
        if self.soldier_item:
            self.soldier_item.setRect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size)

        if (i, j) in self.simulation.disarmed_locations:
            QTimer.singleShot(500, lambda: self.board_items[(i, j)].setBrush(QBrush(Qt.darkGreen)))

    def display_simulation_results(self):
        """
        Displays the results of the simulation in the log.
        """
        results = (
            f"Survivors: {self.simulation.survivors}/{self.simulation.amount_of_soldiers}\n"
            f"Amount of mines on board: {self.simulation.board.amount_of_mines}\n"
            f"Amount of bombs on board: {self.simulation.board.amount_of_bombs}\n"
            f"Disarmed Mines: {self.simulation.disarmed_mines}\n"
            f"Disarmed Bombs: {self.simulation.disarmed_bombs}\n"
            f"Remaining special soldiers: {len(self.simulation._special_soldiers)}\n"
            f"Classifier Accuracy - (metric : percentage of good predictions along the route): {self.simulation.accuracy * 100:.2f}%\n"
        )
        results += "\nRandom Events Log:\n" + "\n".join(self.simulation.random_events_log)
        self.simulation_output.setText(results)
