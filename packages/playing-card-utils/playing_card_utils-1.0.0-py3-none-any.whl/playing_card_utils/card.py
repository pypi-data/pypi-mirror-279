"""Card Class"""

from dataclasses import dataclass
from typing import Any
from .suites import Suite, SUITE_CODES
from .card_type import CardType, CARD_TYPE_CODES


@dataclass
class Card:
    """Card"""
    suite_code: str  # S, H, C, D
    card_type_code: str  # A, 2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K

    def __post_init__(self) -> None:
        if self.suite_code not in SUITE_CODES:
            raise ValueError(f"Invalid suite code: {self.suite_code}")
        if self.card_type_code not in CARD_TYPE_CODES:
            raise ValueError(f"Invalid card type code: {self.card_type_code}")

    @property
    def suite(self) -> Suite:
        """Get suite"""
        return Suite(code=self.suite_code)

    @property
    def card_type(self) -> CardType:
        """Get card type"""
        return CardType(code=self.card_type_code)

    @property
    def name(self) -> str:
        """Get name of the card"""
        return f"{self.card_type.name} of {self.suite.name}"

    def __str__(self) -> str:
        """Card string representation"""
        return f"{self.card_type.code}{self.suite.symbol}"

    def __repr__(self) -> str:
        """Card representation"""
        return f"{self.card_type.code}{self.suite.symbol}"

    def __eq__(self, other: Any) -> bool:
        """Card equality"""
        if isinstance(other, Card):
            return all(
                [
                    self.card_type.code == other.card_type.code,
                    self.suite.code == other.suite.code
                ]
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.card_type.code, self.suite.code))

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight < other.card_type.weight
        return NotImplemented

    def __le__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight <= other.card_type.weight
        return False

    def __gt__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight > other.card_type.weight
        return False

    def __ge__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.card_type.weight >= other.card_type.weight
        return False
