# NovaHub Database Blueprint

## 1. User
Maqsad:
- Telegram foydalanuvchilari

Bog'lanish:
- 1 Wallet
- N Orders
- N Transactions

---

## 2. Wallet
Maqsad:
- Ichki balans

Qoidalar:
- 1 User = 1 Wallet
- Pul tashqariga chiqmaydi
- Wallet → Wallet transfer mavjud

---

## 3. Transaction
Maqsad:
- Barcha moliyaviy operatsiyalar jurnali

Turlari:
- Deposit
- Purchase
- Transfer In
- Transfer Out
- Cashback
- Commission

---

## 4. Payment
Maqsad:
- Wallet to'ldirish

Holatlar:
- Pending
- Approved
- Rejected

---

## 5. Transfer
Maqsad:
- Walletlar orasidagi o'tkazmalar

Qoidalar:
- Minimal balans
- Minimal qoldiq
- Komissiya
- Cashback
- Founder/Admin qoidalari

---

## 6. Platform

Telegram
Instagram
TikTok
YouTube
Facebook
va boshqalar

---

## 7. Category

Platform tarkibidagi kategoriyalar

---

## 8. Service

API yoki Manual xizmatlar

---

## 9. Order

Buyurtmalar

Holatlar:
- Pending
- Processing
- Completed
- Partial
- Cancelled
- Refunded

---

## 10. ApiProvider

SMM API provayderlari

---

## 11. ApiService

API orqali sinxronlangan xizmatlar

---

## 12. Setting

Founder tomonidan boshqariladigan tizim sozlamalari

Misollar:
- Transfer ON/OFF
- Cashback
- Commission
- Minimal transfer
- Maksimal transfer
- Minimal balans
- Walletda qoladigan minimal summa

---

## 13. Notification

Tizim xabarlari

---

## 14. Audit Log

Muhim amallar tarixi

---

## 15. Admin

Administratorlar

Role:
- Founder
- Super Admin
- Admin
- Moderator
