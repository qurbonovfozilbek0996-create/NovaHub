import hashlib
import hmac
import time
from urllib.parse import parse_qsl

from app.core.config.settings import settings


class TelegramWebAppSecurity:
    """
    Telegram WebApp initData xavfsizlik tekshiruvi.

    Telegram yuborgan initData ichidagi hash orqali
    ma'lumotlarning haqiqiyligini tekshiradi.
    """

    MAX_AUTH_AGE = 86400

    @classmethod
    def validate_init_data(
        cls,
        init_data: str,
    ) -> dict[str, str]:
        """
        Telegram WebApp initData ni tekshiradi.

        Muvaffaqiyatli bo'lsa parsed data qaytaradi.
        Xavfsizlik xatosida ValueError chiqaradi.
        """

        if not init_data:
            raise ValueError(
                "Telegram WebApp initData mavjud emas."
            )

        parsed = dict(
            parse_qsl(
                init_data,
                keep_blank_values=True,
            )
        )

        received_hash = parsed.pop(
            "hash",
            None,
        )

        if not received_hash:
            raise ValueError(
                "Telegram WebApp hash mavjud emas."
            )

        auth_date_raw = parsed.get("auth_date")

        if not auth_date_raw:
            raise ValueError(
                "Telegram WebApp auth_date mavjud emas."
            )

        try:
            auth_date = int(auth_date_raw)
        except ValueError as exc:
            raise ValueError(
                "Telegram WebApp auth_date noto'g'ri."
            ) from exc

        if time.time() - auth_date > cls.MAX_AUTH_AGE:
            raise ValueError(
                "Telegram WebApp sessiyasi eskirgan."
            )

        if auth_date > time.time() + 60:
            raise ValueError(
                "Telegram WebApp auth_date noto'g'ri."
            )

        data_check_string = "\n".join(
            f"{key}={parsed[key]}"
            for key in sorted(parsed)
        )

        secret_key = hmac.new(
            b"WebAppData",
            settings.BOT_TOKEN.encode(),
            hashlib.sha256,
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            calculated_hash,
            received_hash,
        ):
            raise ValueError(
                "Telegram WebApp initData imzosi noto'g'ri."
            )

        return parsed
