import numpy as np
from sklearn import datasets


class Board:
    """
    A class to represent a game board with mines and bombs, which also assigns features from the Iris dataset.

    Attributes:
        size_of_board (int): The size of the board (size x size).
        mine_probability (float): The probability of a cell containing a mine or bomb.
        array (np.ndarray): The generated board array with mines and bombs.
        amount_of_mines (int): The total number of mines on the board.
        amount_of_bombs (int): The total number of bombs on the board.
        assigned_test_features (np.ndarray): The features from the Iris dataset assigned to the board cells.

    Note:
        The Iris dataset from scikit-learn is used to assign features to the board cells. More information about the
        Iris dataset can be found at:
        https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html
    """
    def __init__(self, size_of_board, mine_probability):
        """
        Initializes the Board with the specified size and mine probability.

        Args:
            size_of_board (int): The size of the board (size x size).
            mine_probability (float): The probability of a cell containing a mine or bomb.
        """
        self.size_of_board = size_of_board
        self.mine_probability = mine_probability
        self.array = self._generate_board()
        self.amount_of_mines = self._count_mines()
        self.amount_of_bombs = self._count_bombs()
        self.assigned_test_features = self._assign_iris_features()

    def _generate_board(self):
        """
        Generates the board with mines and bombs based on the mine probability.

        Returns:
            np.ndarray: A 2D array representing the board, where 0 indicates an empty cell,
                        1 indicates a mine, and 2 indicates a bomb.
        """
        return np.random.binomial(2, self.mine_probability, (self.size_of_board, self.size_of_board))

    def _count_mines(self):
        """
        Counts the number of mines on the board.

        Returns:
            int: The total number of mines on the board.
        """
        count = 0
        for i in range(self.size_of_board):
            for j in range(self.size_of_board):
                if self.array[i][j] == 1:
                    count += 1
        return count

    def _count_bombs(self):
        """
        Counts the number of bombs on the board.

        Returns:
            int: The total number of bombs on the board.
        """
        count = 0
        for i in range(self.size_of_board):
            for j in range(self.size_of_board):
                if self.array[i][j] == 2:
                    count += 1
        return count

    def _assign_iris_features(self):
        """
        Assigns features from the Iris dataset to the cells on the board based on the cell type.

        Returns:
            np.ndarray: A 3D array where each cell contains a feature vector from the Iris dataset.
        """
        iris = datasets.load_iris()

        data_label_0 = iris.data[iris.target == 0]
        data_label_1 = iris.data[iris.target == 1]
        data_label_2 = iris.data[iris.target == 2]

        features = np.zeros((self.size_of_board, self.size_of_board, iris.data.shape[1]))

        for i in range(self.size_of_board):
            for j in range(self.size_of_board):
                if self.array[i][j] == 0:
                    random_index = np.random.randint(0, len(data_label_0))
                    features[i, j, :] = data_label_0[random_index]
                elif self.array[i][j] == 1:
                    random_index = np.random.randint(0, len(data_label_1))
                    features[i, j, :] = data_label_1[random_index]
                else:
                    random_index = np.random.randint(0, len(data_label_2))
                    features[i, j, :] = data_label_2[random_index]
        return features