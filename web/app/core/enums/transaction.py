from enum import StrEnum


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
    PURCHASE = "purchase"
    COMMISSION = "commission"
    CASHBACK = "cashback"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"


class TransactionStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REVERSED = "reversed"
