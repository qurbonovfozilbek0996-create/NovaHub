from dataclasses import dataclass


@dataclass(slots=True)
class DashboardStats:
    total_users: int
    active_users: int
    total_orders: int
    pending_orders: int
    completed_orders: int
    total_services: int
    total_platforms: int
    total_providers: int
    wallet_balance: int
    total_roles: int
    total_permissions: int
