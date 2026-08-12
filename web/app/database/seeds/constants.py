SYSTEM_ROLES = [
    {
        "name": "Founder",
        "code": "founder",
        "description": "System Founder",
    },
    {
        "name": "Administrator",
        "code": "admin",
        "description": "System Administrator",
    },
    {
        "name": "Support",
        "code": "support",
        "description": "Support Operator",
    },
    {
        "name": "Moderator",
        "code": "moderator",
        "description": "System Moderator",
    },
]

SYSTEM_PERMISSIONS = [
    # Users
    {
        "module": "users",
        "action": "view",
        "code": "users.view",
        "description": "View users",
    },
    {
        "module": "users",
        "action": "edit",
        "code": "users.edit",
        "description": "Edit users",
    },
    {
        "module": "users",
        "action": "ban",
        "code": "users.ban",
        "description": "Ban users",
    },

    # Wallet
    {
        "module": "wallet",
        "action": "view",
        "code": "wallet.view",
        "description": "View wallets",
    },
    {
        "module": "wallet",
        "action": "manage",
        "code": "wallet.manage",
        "description": "Manage wallets",
    },

    # Orders
    {
        "module": "orders",
        "action": "view",
        "code": "orders.view",
        "description": "View orders",
    },
    {
        "module": "orders",
        "action": "manage",
        "code": "orders.manage",
        "description": "Manage orders",
    },

    # Support
    {
        "module": "support",
        "action": "reply",
        "code": "support.reply",
        "description": "Reply support requests",
    },

    # Roles
    {
        "module": "roles",
        "action": "manage",
        "code": "roles.manage",
        "description": "Manage roles",
    },

    # Permissions
    {
        "module": "permissions",
        "action": "manage",
        "code": "permissions.manage",
        "description": "Manage permissions",
    },

    # Audit
    {
        "module": "audit",
        "action": "view",
        "code": "audit.view",
        "description": "View audit logs",
    },

    # Settings
    {
        "module": "settings",
        "action": "manage",
        "code": "settings.manage",
        "description": "Manage system settings",
    },
]
