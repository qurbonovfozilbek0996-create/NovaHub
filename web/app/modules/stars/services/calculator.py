from dataclasses import dataclass


@dataclass(slots=True)
class CalculationResult:
    stars: int
    amount: int
    rate: int


class StarsCalculator:
    """
    Telegram Stars hisoblash xizmati.
    """

    def __init__(self, rate: int) -> None:
        self.rate = rate

    def stars_to_amount(self, stars: int) -> CalculationResult:
        amount = stars * self.rate

        return CalculationResult(
            stars=stars,
            amount=amount,
            rate=self.rate,
        )

    def amount_to_stars(self, amount: int) -> CalculationResult:
        stars = amount // self.rate

        return CalculationResult(
            stars=stars,
            amount=amount,
            rate=self.rate,
        )
