# NovaHub — FINAL ROADMAP

> STATUS: ARCHITECTURE FREEZE
> Ushbu hujjat NovaHub loyihasining asosiy va yagona Source of Truth hujjatidir.
> Keyingi development ushbu roadmap asosida amalga oshiriladi.

---

## 1. LOYIHA MAQSADI

NovaHub — professional, modular va kengaytiriladigan SMM management platforma.

Asosiy tizim:

Platform → Category → Service → Order

NovaHub ikki alohida interfeysdan tashkil topadi:

- Admin Panel
- User Panel

Admin va User interfeyslari bir-biridan mustaqil arxitekturada ishlaydi.

---

## 2. ASOSIY TEXNOLOGIYALAR

Backend:
- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- SQLite (development)
- Aiosqlite

Frontend:
- Server-side templates / mavjud NovaHub web arxitekturasi
- Mobile-first yondashuv

Infrastructure:
- Cloudflare Tunnel (development/testing)
- GitHub (source control)
- Production deployment keyinchalik alohida belgilanadi

---

## 3. ARXITEKTURA PRINSIPLARI

1. Modular architecture.
2. Har bir modul faqat o‘z vazifasini bajaradi.
3. Business logic router ichiga yozilmaydi.
4. Repository — database access.
5. Service — business logic.
6. Router — HTTP/interface layer.
7. Model — database structure.
8. Dependency injection mavjud arxitektura bilan mos ishlatiladi.
9. Mavjud kod sababsiz buzilmaydi.
10. Bir modulni tugatmasdan keyingi modulga o'tilmaydi.
11. Database o‘zgarishlari migration orqali bajariladi.
12. Manual database modification asosiy development usuli emas.
13. Yangi feature faqat roadmap bilan mos bo‘lsa qo‘shiladi.

---

## 4. USER PANEL

User panel quyidagi asosiy yo‘nalishlarga ega:

- Authentication
- Profile
- Premium
- Stars
- Gifts
- Numbers
- Orders
- Payments
- Providers
- Recipients
- Support
- Settings
- Wallet

User uchun interfeys:
- Mobile-first
- Tushunarli
- Minimal
- Professional
- Uzbek tilida

---

## 5. ADMIN PANEL

Admin Panel User Panel'dan alohida ishlaydi.

Admin Dashboard asosiy ko‘rsatkichlari:

- Jami foydalanuvchilar
- Faol foydalanuvchilar
- Jami buyurtmalar
- Kutilayotgan buyurtmalar
- Yakunlangan buyurtmalar
- Bekor qilingan buyurtmalar
- Platformalar
- Kategoriyalar
- Servislar
- API providerlar
- Bugungi daromad
- Wallet turnover
- API status
- Oxirgi synchronization vaqti

Users sahifasida asosiy action:

- Ko‘rish

User detail sahifasida:

- Profil
- Vakolati
- Wallet
- Buyurtmalar
- Activity history
- Permissionlar
- Boshqaruv amallari

Termin:
- "Rol" o‘rniga "Vakolati" ishlatiladi.

---

## 6. AUTHENTICATION

Authentication tizimi:

- Login
- Session/authentication
- User identification
- Permission checking
- Admin access control

Permission architecture markazlashtirilgan bo‘ladi.

Admin access:
- Permission based
- Role/Vakolat asosida
- Protected routes

---

## 7. USER / ROLE / PERMISSION

Asosiy entitylar:

- User
- Role
- Permission
- UserPermission
- RolePermission

Founder/Admin huquqlari tizim tomonidan himoyalanadi.

Permission tekshiruvi router va service qatlamlari chegarasida professional tarzda tashkil qilinadi.

---

## 8. WALLET

Wallet tizimi NovaHub moliyaviy yadrosining asosiy qismlaridan biri.

Wallet ID:

WL000001
WL000002
...

Asosiy imkoniyatlar:

- Balance
- Top up
- Transfer
- Transaction history
- Internal transfer
- Financial statistics

Admin konfiguratsiyasi:

- Transfer commission
- Cashback
- Minimum transfer
- Maximum transfer
- Transfer enable/disable
- Wallet top-up enable/disable
- Cashback enable/disable
- Commission enable/disable

Transfer summary:

- Transfer amount
- Commission
- Cashback
- Total deducted

Moliyaviy operatsiyalar transaction orqali kuzatiladi.

---

## 9. PAYMENT CARDS

Payment Cards admin tomonidan boshqariladi.

Asosiy entity:

PaymentCard

CRUD:

- Create
- Read
- Update
- Delete

Payment card bilan bog‘liq ma'lumotlar:

- Card details
- Payment note
- Status
- Optional QR code
- Display/order information

Payment Cards Wallet top-up jarayoni bilan integratsiya qilinadi.

---

## 10. PAYMENTS

Payment workflow:

User:
1. Payment usulini tanlaydi.
2. Kerakli summani ko‘radi.
3. Payment ma'lumotlarini oladi.
4. Zarur bo‘lsa screenshot/confirmation yuboradi.
5. Admin tekshiradi.
6. Payment tasdiqlanadi.
7. Wallet balance yangilanadi.

Payment statuslar aniq va transaction bilan bog‘langan bo‘ladi.

---

## 11. PLATFORM / CATEGORY / SERVICE

NovaHub SMM yadrosi:

Platform
↓
Category
↓
Service
↓
Order

Platform:
- Name
- Status
- Metadata

Category:
- Platform relation
- Name
- Status

Service:
- Category relation
- Provider relation
- API service ID
- API price
- Markup
- User price
- Status
- Sync information

Service price:

API price
+
Markup
=
User price

Service narxi 0 so‘m bo‘lib qolmasligi uchun pricing logic markazlashtirilgan bo‘ladi.

---

## 12. API PROVIDERS

Provider architecture:

Provider
↓
Adapter
↓
External API

Har bir provider uchun adapter architecture ishlatiladi.

Provider:
- Name
- API URL
- Credentials/configuration
- Status
- Synchronization status

Provider adapter:
- Service sync
- Order creation
- Order status
- Balance/status
- API communication

Provider API xatosi butun tizimni buzmasligi kerak.

---

## 13. SERVICE SYNCHRONIZATION

External provider → NovaHub Service

Synchronization:

- API service ID
- Name
- API price
- Service status
- Provider information
- Last synchronization time

Sync natijasi database'da saqlanadi.

Admin Dashboard:

- API status
- Last synchronization time

ko‘rsatadi.

---

## 14. ORDERS

Order flow:

1. Platform tanlash
2. Category tanlash
3. Service tanlash
4. Link kiritish
5. Quantity kiritish
6. Price calculation
7. Confirmation
8. Order yaratish
9. Provider API orqali yuborish
10. Status monitoring

Order statuslari tizim bo‘yicha yagona standartga ega bo‘ladi.

---

## 15. ORDER PRICE

Order price service pricing orqali hisoblanadi.

Asosiy formula:

API price
→ markup
→ user price
→ quantity
→ final order price

Pricing logic bir nechta joyda takrorlanmaydi.

---

## 16. TRANSACTIONS

Moliyaviy harakatlarning asosiy audit manbai:

Transaction

Transaction quyidagilarni kuzatadi:

- Wallet top-up
- Transfer
- Order payment
- Cashback
- Commission
- Other approved financial operations

Transactionlar o‘chirib yuboriladigan oddiy log sifatida ishlatilmaydi.

---

## 17. AUDIT LOG

Muhim admin harakatlari audit qilinadi.

Audit:

- Who
- What
- When
- Target
- Action
- Relevant metadata

Audit log security va debugging uchun ishlatiladi.

---

## 18. SUPPORT

Support moduli:

- User support request
- Admin response
- Request status
- Conversation/history

Support business logic alohida modulda saqlanadi.

---

## 19. SETTINGS

Settings orqali tizimning admin-configurable qiymatlari boshqariladi.

Settings:

- Feature toggles
- Financial settings
- System configuration
- User-facing configuration

Hardcoded configuration imkon qadar kamaytiriladi.

---

## 20. DATABASE

Database development:

SQLite

Production database keyinchalik alohida infrastructure qarori bilan belgilanadi.

Database changes:

Model
→ Alembic migration
→ Database

Har bir schema o‘zgarishi migration bilan amalga oshiriladi.

Database jadvali mavjud emasligini kod orqali yashirish mumkin emas.

Migration holati developmentdan oldin tekshiriladi.

---

## 21. MIGRATION QOIDASI

Migration tartibi:

1. Model o‘zgarishi.
2. Migration yaratish.
3. Migration tekshirish.
4. Database upgrade.
5. Schema verification.
6. Application test.

Mavjud migrationlar sababsiz o‘zgartirilmaydi.

---

## 22. SECURITY

Asosiy security prinsiplari:

- Password/hash security
- Permission checking
- Protected admin routes
- Secretlarni source code'ga yozmaslik
- Environment variables
- API credentials protection
- Financial operation validation
- Input validation
- Audit logging

`.env` GitHub'ga yuborilmaydi.

---

## 23. GITHUB

GitHub NovaHub source control uchun ishlatiladi.

Repository ichida:

- Source code
- docs
- migrations
- tests
- configuration examples

bo‘ladi.

GitHub'ga yuborilmaydi:

- `.env`
- Secret keys
- API credentials
- Private tokens
- Local database
- Temporary files
- Virtual environment

`.gitignore` professional holatda saqlanadi.

---

## 24. DOCUMENTATION

Asosiy roadmap:

docs/FINAL_ROADMAP.md

Bu fayl NovaHub uchun Source of Truth hisoblanadi.

Texnik qarorlar imkon qadar documentation bilan mustahkamlanadi.

---

## 25. TESTING

Har bir muhim modul:

- Unit-level logic
- Service logic
- Repository logic
- API/route behavior
- Integration

darajasida tekshiriladi.

Productionga chiqarishdan oldin critical financial va order flow test qilinadi.

---

## 26. DEPLOYMENT

Development:

Local/Termux
→ Ubuntu proot
→ FastAPI
→ Cloudflare Tunnel

Cloudflare Quick Tunnel faqat development/testing uchun.

Production uchun:

- Named Cloudflare Tunnel
- Stable domain
- Production server
- Secure secrets
- Production database

alohida bosqichda amalga oshiriladi.

---

## 27. CURRENT DEVELOPMENT STATUS

### Tayyor

- Project base architecture
- Auth foundation
- User model
- Wallet foundation
- Transaction foundation
- Payment foundation
- PaymentCard model
- PaymentCard repository
- PaymentCard service
- Payment Cards router
- Payment Cards router connection
- API management foundation
- Provider architecture foundation

### Tekshirilayotgan

- Services architecture
- Service database migration
- Service pricing
- Provider synchronization
- API price
- Markup
- User price

### Muhim aniqlangan muammo

Development database'da `services` table mavjud emasligi aniqlangan.

Bu muammo:

- Migration
- Model
- Database schema
- Service initialization

ketma-ketligi orqali to‘g‘ri hal qilinadi.

Muammoni vaqtinchalik workaround bilan yashirish mumkin emas.

---

## 28. DEVELOPMENT ORDER

NovaHub development tartibi:

1. Architecture verification
2. Database/migration integrity
3. Auth
4. Users
5. Roles/Permissions
6. Wallet
7. Transactions
8. Payments
9. Payment Cards
10. Providers
11. Platforms
12. Categories
13. Services
14. Service synchronization
15. Pricing
16. Orders
17. Admin Dashboard
18. User Panel polish
19. Security
20. Testing
21. Documentation
22. GitHub
23. Production preparation

---

## 29. WORKING RULES

NovaHub bilan ishlashda:

- Har safar bitta fayl.
- Avval nano orqali fayl ochiladi.
- Keyin o‘zgartirish qilinadi.
- Mavjud kod buzilmaydi.
- O‘zboshimchalik bilan yangi feature qo‘shilmaydi.
- Avval architecture, keyin implementation.
- Har bir bosqich tekshiriladi.
- "Tayyor" keyingi bosqichga o'tish belgisi hisoblanadi.

---

## 30. ARCHITECTURE FREEZE

Ushbu hujjat NovaHub'ning asosiy arxitekturasini belgilaydi.

Architecture Freeze'dan keyin:

- Asosiy modul chegaralari o‘zboshimchalik bilan o‘zgartirilmaydi.
- Business flow o‘zboshimchalik bilan o‘zgartirilmaydi.
- Database architecture sababsiz almashtirilmaydi.
- Yangi feature faqat aniq texnik/business zarurat bo‘lsa ko‘rib chiqiladi.
- Existing modules must be preserved.
- Refactoring faqat real texnik sabab bilan amalga oshiriladi.

---

## 31. FINAL PRODUCT STRUCTURE

NovaHub yakuniy konsepsiyasi:

USER
↓
AUTH
↓
PROFILE / WALLET / SERVICES / ORDERS / PAYMENTS
↓
PLATFORM
↓
CATEGORY
↓
SERVICE
↓
PROVIDER API
↓
ORDER

ADMIN
↓
DASHBOARD
↓
USERS
↓
WALLET / PAYMENTS / CARDS
↓
PLATFORMS / CATEGORIES / SERVICES
↓
PROVIDERS / SYNCHRONIZATION
↓
ORDERS / AUDIT / SETTINGS

---

## 32. FINAL PRINCIPLE

NovaHub tasodifiy featurelar yig‘indisi emas.

NovaHub:

- professional architecture
- modular backend
- controlled financial system
- API-driven SMM system
- separated Admin/User interfaces
- secure permissions
- reliable order processing
- controlled service pricing
- documented development

asosida quriladi.

ROADMAP STATUS: FINAL
ARCHITECTURE STATUS: FROZEN
