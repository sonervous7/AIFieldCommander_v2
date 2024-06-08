import random
from abc import ABC, abstractmethod


class Soldier(ABC):
    """
    An abstract base class representing a generic soldier with health.

    Attributes:
        health (int): The health of the soldier.
    """

    def __init__(self, health=100):
        """
        Initializes a Soldier with the specified health.

        Args:
            health (int): The health of the soldier. Default is 100.
        """
        self.health = health

    @abstractmethod
    def react_to_mine(self):
        """
        Defines the reaction to a mine. Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def react_to_bomb(self):
        """
        Defines the reaction to a bomb. Must be implemented by subclasses.
        """
        pass


class Heavy(Soldier):
    """
    A class representing a heavy soldier with additional armor.

    Attributes:
        health (int): The health of the soldier.
        armor (int): The armor of the soldier.
    """

    def __init__(self, health):
        """
        Initializes a Heavy soldier with the specified health and default armor of 100.

        Args:
            health (int): The health of the soldier.
        """
        super().__init__(health)
        self.armor = 100

    def react_to_mine(self):
        """
        Reacts to a mine by reducing armor if sufficient, otherwise reduces health.

        Overrides:
            Soldier.react_to_mine
        """
        if self.armor >= 50:
            self.armor -= 50
        else:
            if self.health >= 50:
                self.health -= 50

    def react_to_bomb(self):
        """
        Reacts to a bomb by significantly reducing armor or health.

        Overrides:
            Soldier.react_to_mine
        """
        if self.armor > 50:
            self.armor -= 100
        elif self.armor == 50:
            self.armor = 0
            self.health = 50
        else:
            self.health = 0

    def react_to_enemy(self):
        """
        Reacts to an enemy by setting health and armor to 0.
        """
        self.health, self.armor = 0, 0


class Sapper(Soldier):
    """
    A class representing a sapper soldier with disarming kits.

    Attributes:
        health (int): The health of the soldier.
        disarming_kits (int): The number of disarming kits the soldier has.name
    """

    def __init__(self, health, disarming_kits):
        """
        Initializes a Sapper soldier with the specified health and disarming kits.

        Args:
            health (int): The health of the soldier.
            disarming_kits (int): The number of disarming kits the soldier has.
        """
        super().__init__(health)
        self.disarming_kits = disarming_kits

    def react_to_mine(self):
        """
        Reacts to a mine by using a disarming kit if available, otherwise reduces health to 0.

        Overrides:
            Soldier.react_to_mine
        """
        if self.disarming_kits > 0:
            self.disarming_kits -= 1
        else:
            self.health = 0

    def react_to_bomb(self):
        """
        Reacts to a bomb by using two disarming kits if available, otherwise reduces health to 0.

        Overrides:
            Soldier.react_to_mine
        """
        if self.disarming_kits >= 2:
            self.disarming_kits -= 2
        else:
            self.health = 0

    def add_kit(self):
        """
        Adds a random number of disarming kits (1 or 2) to the sapper's inventory.
        """
        self.disarming_kits += random.randint(1, 2)
