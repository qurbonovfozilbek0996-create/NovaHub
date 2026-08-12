# NovaHub System Architecture

Version: 1.0

Status: APPROVED

Founder:
Fozil Qurbonov

---

# Loyiha maqsadi

NovaHub — Telegram Mini App asosidagi professional SMM platformasi.

Tizim modulli arxitekturada ishlab chiqiladi.

Hech bir modul boshqa modulning ichida biznes mantiqini saqlamaydi.

Har bir modul faqat o'z vazifasini bajaradi.

---

# Asosiy tamoyillar

- Professional Architecture
- Modular Structure
- Service Layer
- Repository Layer
- Scheduler
- Audit Log
- Role Based Access
- High Performance
- Mobile First
- Telegram Mini App
- Freeze Policy

---

# Asosiy modullar

## Authentication

Login

Registration

Roles

Permissions

Sessions

---

## Users

Profil

Til

Sozlamalar

Referral

Activity

---

## Wallet

Wallet

Wallet ID

Transfer

History

Transactions

Cards

Payment Requests

Top Up

Withdraw

Cashback

Commission

Limits

---

## Cards

Karta qo'shish

Karta tahrirlash

Karta o'chirish

Asosiy karta

UZCARD

HUMO

Kelajakda:

Click

Payme

Uzum

va boshqa provayderlar.

---

## Orders

Buyurtma yaratish

Holati

Tarix

Bekor qilish

Monitoring

---

## Platforms

Platformalar

---

## Categories

Kategoriyalar

---

## Services

Xizmatlar

Narx

API

Status

---

## Promotions

Aksiyalar

Scheduler

Banner

AI

Channel Post

Statistics

---

## Broadcast

Barcha foydalanuvchilarga xabar

Segment bo'yicha xabar

Oldindan ko'rish

Rejalashtirilgan yuborish

---

## Maintenance

Texnik ishlar

Boshlash

Yakunlash

Scheduler

Rasmiy kanal

Faqat Founder va ruxsatli adminlar tizimga kira oladi.

Oddiy foydalanuvchilarga faqat Texnik ishlar sahifasi ko'rsatiladi.

Pastda faqat:

📢 Rasmiy kanal

tugmasi bo'ladi.

---

## Scheduler

Promotion

Birthday

Maintenance

Broadcast

API Sync

Statistics

Reminder

---

## API Management

Provider

Balance

Sync

Orders

Services

Health Check

---

## Statistics

Users

Wallet

Orders

Revenue

API

Promotions

Broadcast

---

## Audit Log

Har bir amal yoziladi.

Kim

Qachon

Nima

Qayerda

Natija

---

## Web App

Telegram Mini App

Premium UI

Responsive

Light

Dark

Bottom Navigation

Cards UI

---

## Telegram Bot

Bot faqat tezkor kirish va bildirishnomalar uchun ishlatiladi.

Asosiy boshqaruv Web App orqali amalga oshiriladi.

---

## Admin Panel

Dashboard

Users

Wallet

Cards

Orders

Platforms

Categories

Services

Promotions

Broadcast

Maintenance

API

Statistics

Settings

Audit Log

---

# Dizayn

Barcha sahifalar:

Bir xil dizayn tizimida yoziladi.

---

# Kod yozish qoidalari

Har bir modul:

README

↓

Model

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

# Freeze Policy

Freeze holatiga o'tgan modul:

Qayta yozilmaydi.

Faqat:

- Xatolar
- Founder tasdiqlagan yangi imkoniyatlar

qo'shilishi mumkin.

---

# Founder

NovaHub Founder

Fozil Qurbonov

Ushbu hujjat NovaHub loyihasining rasmiy arxitektura hujjati hisoblanadi.
