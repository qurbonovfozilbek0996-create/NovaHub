# NovaHub Promotions Module

## Status

Architecture v1.0

Tasdiqlovchi:
Founder - Fozil Qurbonov

---

# Modul maqsadi

Promotions moduli NovaHub platformasida platforma, kategoriya, xizmat yoki butun tizim uchun vaqtinchalik aksiyalar yaratish va ularni avtomatik boshqarish uchun mo'ljallangan.

Barcha jarayonlar Scheduler tomonidan avtomatik boshqariladi.

---

# Asosiy tamoyillar

- Professional arxitektura
- Mavjud kodlarni buzmaslik
- Modulli tuzilma
- Scheduler orqali avtomatlashtirish
- Audit yuritish
- AI qo'llab-quvvatlashi
- Yakuniy tasdiqlashsiz hech qanday aksiya ishga tushmaydi

---

# Promotion Wizard

Administrator "➕ Aksiya yaratish" tugmasini bosadi.

Shundan keyin Wizard boshlanadi.

Har bir bosqichda quyidagi tugmalar mavjud bo'ladi:

⬅️ Orqaga

🏠 Bosh menyu

❌ Bekor qilish

---

1-qadam

Aksiya qayerga qo'llaniladi?

• Butun bot

• Platforma

• Kategoriya

• Xizmat

---

2-qadam

Kerakli obyektlarni tanlash.

Bir vaqtning o'zida bir nechta platforma, kategoriya yoki xizmat tanlash mumkin.

---

3-qadam

Chegirma turi.

• Foiz

• Aniq summa

---

4-qadam

Chegirma qiymatini kiritish.

Misol:

20%

yoki

5000 so'm

---

5-qadam

Boshlanish vaqti.

Administrator belgilaydi.

---

6-qadam

Tugash vaqti.

Administrator belgilaydi.

---

7-qadam

Banner.

Variantlar:

• AI Banner

• Admin yuklagan banner

• Banner ishlatilmaydi

---

8-qadam

Post matni.

Variantlar:

• AI yozadi

• Administrator yozadi

---

9-qadam

Kanal tanlash.

Administrator oldindan qo'shilgan rasmiy kanallardan birini tanlaydi.

Agar kanal mavjud bo'lmasa:

➕ Kanal qo'shish

bo'limi ochiladi.

---

10-qadam

Eslatmalar.

Administrator:

• yoqadi

• o'chiradi

hamda

eslatma vaqtlarini belgilaydi.

Misollar:

30 daqiqa

1 soat

6 soat

24 soat

3 kun

yoki

ixtiyoriy vaqt.

---

11-qadam

Yakuniy ko'rinish.

Tizim barcha ma'lumotlarni chiqaradi.

Administrator:

✅ Tasdiqlash

✏️ Tahrirlash

❌ Bekor qilish

---

# Promotion holatlari

Draft

Scheduled

Active

Paused

Finished

Cancelled

---

# Scheduler

Scheduler avtomatik:

- Aksiyani boshlaydi.
- Narxlarni o'zgartiradi.
- Kanalga post yuboradi.
- Belgilangan vaqtda eslatmalar yuboradi.
- Tugaganda narxlarni tiklaydi.
- Aksiyani yakunlaydi.

---

# Kanal

Aksiya boshlanganda:

Bitta post yuboriladi.

Post ID bazaga saqlanadi.

Aksiya tugaganda:

Yangi post yuborilmaydi.

Mavjud post tahrirlanadi.

Matn:

⛔ Aksiya yakunlandi

Tugma:

🌐 NovaHub

yoki

🤖 Bot

(global sozlamaga qarab avtomatik)

---

# Tugmalar

Tugmalar administrator tomonidan har safar tanlanmaydi.

Tizim avtomatik qo'yadi.

Variantlar:

🌐 Web Panel

🤖 Bot

---

# AI

AI quyidagilarni yaratishi mumkin:

• Banner

• Reklama matni

---

# Admin huquqlari

Administrator istalgan vaqtda:

• Pauza qilishi

• Davom ettirishi

• Muddatidan oldin yakunlashi

mumkin.

---

# Audit

Saqlanadi:

Kim yaratdi

Kim tahrirladi

Kim pauza qildi

Kim davom ettirdi

Kim yakunladi

Sana

Vaqt

---

# Texnik ishlar

Agar tizim Texnik ishlar holatiga o'tsa:

- Promotion Scheduler ishlashda davom etadi.
- Founder va ruxsatli adminlar tizimga kira oladi.
- Oddiy foydalanuvchilar faqat Texnik ishlar sahifasini ko'radi.
- Web Panel ishlamaydi.
- Pastda faqat bitta tugma bo'ladi:

📢 Rasmiy kanal

---

# Freeze

Modul 100% testdan o'tgandan so'ng

FREEZE

holatiga o'tadi.

Shundan keyin faqat:

- Xatolarni tuzatish

yoki

- Founder Fozil Qurbonov tasdiqlagan yangi imkoniyatlar

qo'shilishi mumkin.

---

Status:

✅ Founder tomonidan tasdiqlangan arxitektura.
