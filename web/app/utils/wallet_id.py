from app.models.wallet import Wallet


class WalletIdGenerator:
    """
    NovaHub Wallet ID Generator.
    """

    PREFIX = "WL"

    @classmethod
    def generate(cls, wallet_number: int) -> str:
        """
        Example:
        1 -> WL00000001
        25 -> WL00000025
        999 -> WL00000999
        """
        return f"{cls.PREFIX}{wallet_number:08d}"

    @classmethod
    def next_from_wallet(cls, wallet: Wallet | None) -> str:
        """
        Generate the next wallet ID based on the latest wallet.
        """
        if wallet is None:
            return cls.generate(1)

        current = int(wallet.wallet_id.replace(cls.PREFIX, ""))

        return cls.generate(current + 1)
