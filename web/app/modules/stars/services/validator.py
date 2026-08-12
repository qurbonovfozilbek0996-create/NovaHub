from dataclasses import dataclass


@dataclass(slots=True)
class ValidationResult:
    success: bool
    message: str = ""


class StarsValidator:
    """
    Telegram Stars buyurtmasini tekshirish xizmati.
    """

    def __init__(
        self,
        min_stars: int,
        max_stars: int,
    ) -> None:

        self.min_stars = min_stars
        self.max_stars = max_stars

    def validate_stars(
        self,
        stars: int,
    ) -> ValidationResult:

        if stars < self.min_stars:

            return ValidationResult(
                False,
                f"Minimal miqdor {self.min_stars} ⭐."
            )

        if stars > self.max_stars:

            return ValidationResult(
                False,
                f"Maksimal miqdor {self.max_stars} ⭐."
            )

        return ValidationResult(True)

    def validate_balance(
        self,
        balance: int,
        amount: int,
    ) -> ValidationResult:

        if balance < amount:

            return ValidationResult(
                False,
                "Wallet balansingiz yetarli emas."
            )

        return ValidationResult(True)

    def validate_username(
        self,
        username: str,
    ) -> ValidationResult:

        username = username.strip()

        if not username:

            return ValidationResult(
                False,
                "Username kiritilmagan."
            )

        if username.startswith("@") is False:

            return ValidationResult(
                False,
                "Username @ bilan boshlanishi kerak."
            )

        if len(username) < 5:

            return ValidationResult(
                False,
                "Username juda qisqa."
            )

        return ValidationResult(True)
