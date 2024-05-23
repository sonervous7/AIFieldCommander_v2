import pandas as pd
from sklearn.model_selection import train_test_split


class DataReader:
    """
    A class to handle loading, reducing, and splitting the Iris dataset.

    Attributes:
        X_train (np.ndarray): Training features.
        X_test (np.ndarray): Testing features.
        y_train (np.ndarray): Training labels.
        y_test (np.ndarray): Testing labels.
        X (np.ndarray): All features.
        y (np.ndarray): All labels.
    """

    X_train = None
    X_test = None
    y_train = None
    y_test = None
    X = None
    y = None

    @classmethod
    def initialize(cls, file_path="../data/Augmented_Iris.csv", test_size=0.33, random_state=42):
        """
        Initializes the DataReader by loading, reducing, and splitting the data.

        Args:
            file_path (str): The path to the CSV file.
            test_size (float): The fraction of data to be used as the test set.
            random_state (int): The random state for reproducibility.
        """
        cls.load_augmented_data(file_path)
        cls.split_data(test_size, random_state)

    @classmethod
    def load_augmented_data(cls, file_path):
        """
        Loads the augmented Iris dataset from a CSV file, reduce samples, and replacing categorical labels to numerical.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            None
        """
        df = pd.read_csv(
            file_path, usecols=["SepalLengthCm", "SepalWidthCm", "PetalLengthCm", "PetalWidthCm", "Species"]
        )

        # Zamiana etykiety tekstowe na liczbowe

        label_mapping = {"Iris-setosa": 0, "Iris-versicolor": 1, "Iris-virginica": 2}

        df["Species"] = df["Species"].map(label_mapping)

        # Redukcja liczby próbek

        reduced_df = df.groupby("Species").apply(lambda x: x.sample(frac=0.015))

        # Podział na dane i cechy
        cls.X = reduced_df.drop("Species", axis=1).values
        cls.y = reduced_df["Species"].values

    @classmethod
    def split_data(cls, test_size=0.33, random_state=42):
        """
        Splits the dataset into training and testing sets.

        Args:
            test_size (float): The fraction of data to be used as the test set.
            random_state (int): The random state for reproducibility.

        Returns:
            None
        """
        cls.X_train, cls.X_test, cls.y_train, cls.y_test = train_test_split(
            cls.X, cls.y, test_size=test_size, random_state=random_state
        )

    @classmethod
    def get_train_data(cls):
        """
        Returns the training set.

        Returns:
            tuple: A tuple containing the training sets (X_train, y_train).
        """
        if cls.X_train is None or cls.y_train is None:
            raise ValueError("Data has not been split. Call split_data() first.")
        return cls.X_train, cls.y_train

    @classmethod
    def get_test_data(cls):
        """
        Returns the testing set.

        Returns:
            tuple: A tuple containing the testing sets (X_test, y_test).
        """
        if cls.X_test is None or cls.y_test is None:
            raise ValueError("Data has not been split. Call split_data() first.")
        return cls.X_test, cls.y_test
