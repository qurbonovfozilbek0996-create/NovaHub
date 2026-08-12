from enum import StrEnum


class AuditAction(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"

    LOGIN = "login"
    LOGOUT = "logout"

    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_REVOKED = "permission_revoked"

    WALLET_TRANSFER = "wallet_transfer"
    WALLET_LOCK = "wallet_lock"
    WALLET_UNLOCK = "wallet_unlock"

    ORDER_CREATE = "order_create"
    ORDER_CANCEL = "order_cancel"

    API_SYNC = "api_sync"

    SUPPORT_REPLY = "support_reply"

    SETTINGS_UPDATE = "settings_update"

    SYSTEM = "system"
