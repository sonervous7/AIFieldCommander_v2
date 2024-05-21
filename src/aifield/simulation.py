import random

from aifield.soldier import Heavy, Sapper
from src.aifield.board import Board
from src.aifield.classifier_general import ClassifierGeneral
from src.aifield.troops import Troops


class Simulation:
    """
    A class to simulate the movement and actions of soldiers on a board with mines and bombs.

    Attributes:
        board (Board): The game board with mines and bombs.
        type_of_path (str): The type of path soldiers take ('Horizontal' or 'Diagonal').
        _classifier (ClassifierGeneral): The classifier used to predict the presence of mines and bombs.
        amount_of_soldiers (int): The initial number of soldiers.
        survivors (int): The current number of surviving soldiers.
        _special_soldiers (list): A list of special soldiers (Heavy and Sapper).
        _good_predictions (int): The number of correct predictions made by the classifier.
        disarmed_mines (int): The number of mines disarmed.
        disarmed_bombs (int): The number of bombs disarmed.
        random_events_log (list): A log of random events that occurred during the simulation.
        accuracy (float): The accuracy of the classifier's predictions.
        found_kits (int): The number of disarming kits found during the simulation.
        disarmed_locations (set): The set of locations where mines and bombs were disarmed.
    """

    def __init__(self, size_of_board, mine_probability, classifier_name, type_of_path=None, amount_of_soldiers=100):
        """
        Initializes the Simulation with the specified parameters.

        Args:
            size_of_board (int): The size of the board.
            mine_probability (float): The probability of a cell containing a mine or bomb.
            classifier_name (str): The name of the classifier to use.
            type_of_path (str, optional): The type of path soldiers take ('Horizontal' or 'Diagonal'). Default is 'Horizontal'.
            amount_of_soldiers (int, optional): The initial number of soldiers. Default is 100.
        """
        self.board = Board(size_of_board, mine_probability)
        if type_of_path is None:
            type_of_path = "Horizontal"
        self.type_of_path = type_of_path
        self._classifier = ClassifierGeneral(classifier_name, random_state=42)
        self.amount_of_soldiers = amount_of_soldiers
        self.survivors = self.amount_of_soldiers
        self._special_soldiers = Troops.create_soldiers(amount_of_soldiers)
        self._good_predictions = 0
        self.disarmed_mines = 0
        self.disarmed_bombs = 0
        self.random_events_log = []
        self.accuracy = -1
        self.found_kits = 0
        self.disarmed_locations = set()

    def simulate(self):
        """
        Runs the simulation and logs the results.
        """
        print(f"Sprawdźmy ilu mamy wszystkich żołnierzy: {self.amount_of_soldiers}")
        self._classifier.train()
        if self.type_of_path == "Diagonal":
            yield from self._diagonal_path()
        elif self.type_of_path == "Horizontal":
            yield from self._horizontal_path()

        print(f"Dokładność klasyfikatora: {self._classifier} wynosi: {self.accuracy * 100:.2f}%")
        print(f"All soldiers (special included): {self.survivors} out of {self.amount_of_soldiers}")
        print(f"Amount of Mines on board: {self.board.amount_of_mines}.")
        print(f"Disarmed Mines: {self.disarmed_mines}")
        print(f"Amount of Bombs on board: {self.board.amount_of_bombs}.")
        print(f"Disarmed Bombs: {self.disarmed_bombs}")
        print(f"The remaining Special force soldiers: {len(self._special_soldiers)}")
        print(f"Found disarming kits : {self.found_kits}")
        print("\nRandom Events Log:")
        for event in self.random_events_log:
            print(event)

    def _manage_soldiers(self, label, x, y):
        """
        Manages the actions of soldiers based on the presence of mines or bombs.

        Args:
            label (int): The label indicating the presence of a mine (1) or bomb (2).
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        special_soldier = self._special_soldiers.pop()  # It could be sapper or heavy, but there is an interface
        if label == 1:
            special_soldier.react_to_mine()
        elif label == 2:
            special_soldier.react_to_bomb()
        if isinstance(special_soldier, Heavy):
            if special_soldier.health != 0:
                self.random_events_log.append(f"Heavy saves us, HeavyStats: Health: {special_soldier.health},"
                                              f" Armor: {special_soldier.armor}")
                self._special_soldiers.append(special_soldier)
            else:
                self.random_events_log.append("Heavy sacrificed himself and DIED.")
                self.survivors = max(0, self.survivors - 1)
        else:
            if special_soldier.health != 0:
                self._special_soldiers.append(special_soldier)
                if label == 1:
                    self.disarmed_mines += 1
                    self.random_events_log.append(f"Sapper disarmed MINE!")
                    self.disarmed_locations.add((x, y))
                else:
                    self.disarmed_bombs += 1
                    self.random_events_log.append(f"Sapper disarmed BOMB!")
                    self.disarmed_locations.add((x, y))
            else:
                self.random_events_log.append("Sapper died during disarming...")
                self.survivors = max(0, self.survivors - 1)

        # print(f"Długość special forces --> {len(self._special_soldiers)}")

    def _update_game_stats(self, x, y):
        """
        Updates the game statistics based on the classifier's prediction and the actual label of the cell.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
        """
        self._classifier.train()
        predicted_label = self._classifier.predict(self.board.assigned_test_features[x, y])
        actual_label = self.board.array[x][y]
        is_mine = actual_label == 1
        is_bomb = actual_label == 2
        empty = actual_label == 0

        if actual_label == predicted_label and empty:
            self._good_predictions += 1
            self.random_events_log.append("Good prediction, there is no mine nor bomb.")

        elif actual_label == predicted_label and is_mine:
            self._good_predictions += 1
            self.disarmed_mines += 1
            self.random_events_log.append("Disarmed mine, because of good prediction!")
            self.disarmed_locations.add((x, y))

        elif actual_label == predicted_label and is_bomb:
            self._good_predictions += 1
            self.disarmed_bombs += 1
            self.random_events_log.append("Disarmed bomb, because of good prediction. WE'RE LUCKY SIR!")
            self.disarmed_locations.add((x, y))

        elif actual_label != predicted_label and is_mine:
            if self._special_soldiers:
                self.random_events_log.append("Bad prediction, but here are our SPECIAL FORCES SIR!")
                self._manage_soldiers(actual_label, x, y)
            else:
                casualties = random.randint(1, 5)
                self.survivors = max(0, self.survivors - casualties)
                if self.survivors != 0:
                    self.random_events_log.append(
                        f"Bad prediction (MINE) and there are no special forces available. Lost casualties: {casualties}")
                else:
                    self.random_events_log.append("Bad prediction and ALL SOLDIERS ARE DEAD")

        elif actual_label != predicted_label and is_bomb:
            if self._special_soldiers:
                self.random_events_log.append("Bad prediction, but here are our SPECIAL FORCES SIR!")
                self._manage_soldiers(actual_label, x, y)
            else:
                if self.amount_of_soldiers >= 500:
                    casualties = random.randint(25, 50)
                else:
                    casualties = random.randint(5, 15)
                self.survivors = max(0, self.survivors - casualties)
                if self.survivors != 0:
                    self.random_events_log.append(
                        f"Bad prediction (BOMB) and there are no special forces available. Lost casualties: {casualties}")
                else:
                    self.random_events_log.append("Bad prediction and ALL SOLDIERS ARE DEAD")

        elif actual_label != predicted_label and empty:
            self.random_events_log.append("BAD PREDICTION, but there is no mine nor bomb, WE ARE REALLY LUCKY!")

    def _diagonal_path(self):
        """
        Simulates the movement of soldiers along a diagonal path on the board.
        """
        i, j = 0, 0
        while i < self.board.size_of_board and j < self.board.size_of_board:
            # print(f"Diagonal path: updating stats for ({i}, {j})")  # Debug statement
            self._update_game_stats(i, j)
            self._random_event()
            yield i, j
            i += 1
            j += 1
            self.random_events_log.append(f"Moving to [{i}][{j}]")
        self.accuracy = self._good_predictions / self.board.size_of_board

    def _horizontal_path(self):
        """
        Simulates the movement of soldiers along a horizontal path on the board.
        """
        i = 0
        while i < self.board.size_of_board:
            if i % 2 == 0:
                for j in range(self.board.size_of_board):
                    # print(f"Horizontal path: updating stats for ({i}, {j})")  # Debug statement
                    self._update_game_stats(i, j)
                    self._random_event()
                    yield i, j
                    self.random_events_log.append(f"Moving to [{i}][{j}]")
            else:
                for j in reversed(range(self.board.size_of_board)):
                    # print(f"Horizontal path: updating stats for ({i}, {j})")  # Debug statement
                    self._update_game_stats(i, j)
                    self._random_event()
                    yield i, j
                    self.random_events_log.append(f"Moving to [{i}][{j}]")
            i += 1
        self.accuracy = self._good_predictions / (self.board.size_of_board * self.board.size_of_board)

    def _random_event(self):
        """
        Generates and handles random events during the simulation.
        """
        rnd_num = random.randint(1, 3)

        special_soldier = None
        if rnd_num == 1:

            if any(isinstance(soldier, Sapper) for soldier in self._special_soldiers):
                for index, soldier in enumerate(self._special_soldiers):
                    if isinstance(soldier, Sapper):
                        special_soldier = self._special_soldiers.pop(index)
                        break
                special_soldier.add_kit()
                self._special_soldiers.append(special_soldier)
                self.found_kits += 1
                self.random_events_log.append("RANDOM EVENT - Found disarming kit, adding it to SAPPER inventory.")
            else:
                self.random_events_log.append("RANDOM EVENT - Found disarming kit, BUT THERE AREN'T ANY SAPPERS")

        elif rnd_num == 2:
            if any(isinstance(soldier, Heavy) for soldier in self._special_soldiers):
                for index, soldier in enumerate(self._special_soldiers):
                    if isinstance(soldier, Heavy):
                        special_soldier = self._special_soldiers.pop(index)
                        break
                special_soldier.react_to_enemy()
                self.random_events_log.append("Enemy unit encountered, HEAVY DIED SAVING US!")
            else:
                casualties = random.randint(1, 5)
                self.survivors = max(0, self.survivors - casualties)
                self.random_events_log.append(f"Enemy unit encountered -> Lost: {casualties} casualties")

        else:
            recruits = random.randint(1, 3)
            self.survivors += recruits
            self.random_events_log.append(f"Recruited new soldiers: Gained: {recruits} soldiers.")



