# NovaHub Database Architecture (ERD)

## Core Models

User
│
├── 1 → 1 Wallet
├── 1 → N Orders
├── 1 → N Transactions

Wallet
│
├── belongs_to User
├── 1 → N Transactions

Transaction
│
├── belongs_to User
├── belongs_to Wallet

Platform
│
├── 1 → N Categories

Category
│
├── belongs_to Platform
├── 1 → N Services

Service
│
├── belongs_to Category
├── belongs_to ApiProvider
├── 1 → N Orders

Order
│
├── belongs_to User
├── belongs_to Service

ApiProvider
│
├── 1 → N ApiServices
├── 1 → N Services

ApiService
│
├── belongs_to ApiProvider

Setting

Admin

Notification
