from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_pin(pin: str) -> str:
    """
    PIN kodni bcrypt yordamida hash qiladi.
    """
    return pwd_context.hash(pin)


def verify_pin(pin: str, pin_hash: str) -> bool:
    """
    Kiritilgan PIN saqlangan hash bilan mosligini tekshiradi.
    """
    return pwd_context.verify(pin, pin_hash)
