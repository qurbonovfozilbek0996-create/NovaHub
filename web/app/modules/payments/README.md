Payments Module

Status

ACTIVE

---

Purpose

Payments moduli NovaHub tizimida foydalanuvchilarning to‘lov jarayonlarini boshqarish uchun javob beradi.

Modul quyidagi imkoniyatlarni taqdim etadi:

- Payment Cards
- Payment Requests
- Balance Top Up
- Withdraw
- Payment Verification
- Provider Integrations

---

Responsibilities

Payments moduli faqat to‘lov jarayonlariga oid biznes mantiqni bajaradi.

Quyidagi modullar bilan integratsiyada ishlaydi:

- Wallet
- Users
- Orders
- Statistics
- Audit Log

---

Architecture

Ushbu modul NovaHub standart arxitekturasiga amal qiladi:

README

↓

Repository

↓

Service

↓

Scheduler

↓

Handler

↓

Web

↓

Testing

↓

Freeze

---

Rules

- Har bir qatlam faqat o‘z vazifasini bajaradi.
- Business Logic faqat Service qatlamida joylashadi.
- Repository faqat ma'lumotlar bazasi bilan ishlaydi.
- Handler faqat HTTP so‘rovlarini qabul qiladi va Service qatlamini chaqiradi.
- Modul ichidagi kod boshqa modullarning ichki biznes mantiqiga bog‘lanmaydi.

---

Status

ACTIVE
