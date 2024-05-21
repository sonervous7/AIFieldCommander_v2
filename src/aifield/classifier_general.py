from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC


class ClassifierGeneral:
    """
    A general classifier wrapper class that allows the selection and use of various
    machine learning classifiers from scikit-learn.

    Attributes:
        classifier_name (str): The name of the classifier to use.
        random_state (int): The random state for reproducibility.
        classifier (object): The selected classifier instance.

    Note:
        For more information about the classifiers, refer to the scikit-learn documentation:
        https://scikit-learn.org/stable/supervised_learning.html
    """
    def __init__(self, classifier_name, random_state):
        """
        Initializes the ClassifierGeneral with the specified classifier name and random state.

        Args:
            classifier_name (str): The name of the classifier to use.
            random_state (int): The random state for reproducibility.
        """
        self.classifier_name = classifier_name
        self.random_state = random_state
        self.classifier = self._select_classifier()

    def _select_classifier(self):
        """
        Selects and initializes the classifier based on the classifier_name attribute.

        Returns:
            object: An instance of the selected classifier.

        Raises:
            ValueError: If the classifier_name is not supported.
        """
        match self.classifier_name:
            case "RandomForest":
                return RandomForestClassifier(self.random_state)
            case "GradientBoosting":
                return GradientBoostingClassifier(random_state=self.random_state)
            case "LogisticRegression":
                return LogisticRegression(max_iter=1000, random_state=self.random_state)
            case "KNN":
                return KNeighborsClassifier()
            case "SVM":
                return SVC(random_state=self.random_state)
            case "DecisionTree":
                return DecisionTreeClassifier(random_state=self.random_state)
            case "DummyClassifier":
                return DummyClassifier(random_state=self.random_state)
            case "GaussianNB":
                return GaussianNB()
            case "LinearSVC":
                return LinearSVC(max_iter=10000, random_state=self.random_state)
            case _:
                raise ValueError(f"Unsupported classifier: {self.classifier_name}")

    def train(self):
        """
        Trains the classifier using the Iris dataset from scikit-learn.
        """
        iris = datasets.load_iris()
        X = iris.data
        y = iris.target
        self.classifier.fit(X, y)

    def predict(self, features):
        """
        Predicts the class label for a given set of features.

        Args:
            features (array-like): The input features for prediction.

        Returns:
            int: The predicted class label.
        """
        return self.classifier.predict([features])[0]

    def __str__(self):
        """
        Returns the string representation of the classifier.

        Returns:
            str: The name of the classifier.
        """
        return self.classifier_name
