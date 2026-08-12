from .calculator import StarsCalculator
from .validator import StarsValidator


class StarsOrderService:
    """
    Telegram Stars buyurtmalarini boshqarish xizmati.
    """

    def __init__(
        self,
        calculator: StarsCalculator,
        validator: StarsValidator,
    ) -> None:

        self.calculator = calculator
        self.validator = validator

    def create_order(
        self,
        username: str,
        stars: int,
        balance: int,
    ):

        result = self.validator.validate_username(username)

        if not result.success:
            return result

        result = self.validator.validate_stars(stars)

        if not result.success:
            return result

        calculation = self.calculator.stars_to_amount(stars)

        result = self.validator.validate_balance(
            balance=balance,
            amount=calculation.amount,
        )

        if not result.success:
            return result

        return {
            "success": True,
            "username": username,
            "stars": calculation.stars,
            "amount": calculation.amount,
            "rate": calculation.rate,
        }
