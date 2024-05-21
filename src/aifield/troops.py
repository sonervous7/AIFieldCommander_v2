import random

from aifield.soldier import Heavy, Sapper


class Troops:
    """
    A class to create and manage a collection of soldiers, including Heavy and Sapper types.

    Static Methods:
        create_soldiers(quantity): Creates a specified quantity of soldiers with a fixed percentage of Heavy and Sapper types.
    """

    @staticmethod
    def create_soldiers(quantity):
        """
        Creates a specified quantity of soldiers, including a fixed percentage of Heavy and Sapper types.

        Args:
            quantity (int): The total number of soldiers to create.

        Returns:
            list: A list of soldier instances, shuffled to mix Heavy and Sapper soldiers.

        Note:
            The distribution of soldiers is as follows:
            - 3% Heavy soldiers
            - 2% Sapper soldiers
        """
        soldiers = []

        num_heavy = int(quantity * 0.03)  # 3% Heavy
        num_sapper = int(quantity * 0.02)  # 2% Sapper

        # print(f"Creating {num_heavy} Heavy soldiers and {num_sapper} Sapper soldiers")  # Debug print

        soldiers.extend([Heavy(health=100) for _ in range(num_heavy)])
        soldiers.extend([Sapper(health=100, disarming_kits=1) for _ in range(num_sapper)])

        random.shuffle(soldiers)

        return soldiers

