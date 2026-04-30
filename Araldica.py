from enum import Enum


class Araldica(Enum):
    NESSUNA = (0, 0, "Nessuna araldica")

    CITTADINO_A = (2, 5, "Cittadino/a")
    MESSERE_DAMA = (6, 10, "Messere/Dama")
    SIR_MISS = (14, 15, "Sir/Miss")
    LORD_LADY = (28, 30, "Lord/Lady")
    SAVIO_A = (52, 60, "Savio/a")
    ARCONTE_ARCONTESSA = (102, 120, "Arconte/Contessa")

    def __init__(self, required_weeks: int, price: int, label: str):
        self.required_weeks = required_weeks
        self.price = price
        self.label = label

    @classmethod
    def from_weeks(cls, weeks: int):
        """
        Returns the highest Araldica obtainable with the given weeks.
        """

        result = cls.NESSUNA

        for araldica in cls:
            if weeks >= araldica.required_weeks:
                result = araldica
            else:
                break

        return result

    @classmethod
    def calculate_price(
        cls,
        old_araldica,
        new_araldica
    ) -> int:
        """
        Calculates the total price needed to upgrade from
        old_araldica to new_araldica.

        Includes all intermediate araldiche.
        """

        if old_araldica == new_araldica:
            return 0

        members = list(cls)

        old_index = members.index(old_araldica)
        new_index = members.index(new_araldica)

        # Prevent downgrades
        if new_index < old_index:
            return 0

        total = 0

        for araldica in members[old_index + 1:new_index + 1]:
            total += araldica.price

        return total

    def __str__(self):
        return self.label