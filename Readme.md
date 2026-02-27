
# Docker muhitida ishga tushirish



```bash
docker compose up -d 
```

# Customer Credit Control System (Odoo 19)

Ushbu modul mijozlarga qarz limitlari asosida savdo qilish imkonini beradi va limitdan oshib ketish holatlarini avtomatik nazorat qiladi.

## 🚀 Asosiy Imkoniyatlar
- **Kredit Limit Modeli**: Har bir hamkor (Partner) uchun alohida kredit limitlari belgilash.
- **Buxgalteriya Integratsiyasi**: Mijozning to'lanmagan (Posted, Unpaid) invoice summasini real-vaqtda hisoblash (`total_due`).
- **Savdo Nazorati**: Savdo buyurtmasini (Sale Order) tasdiqlashda mijozning joriy qarzi va yangi buyurtma summasini limitga solishtirish.
- **Smart Info**: Sale Order formasida qoldiq kredit (Remaining Credit) haqida ma'lumot va ogohlantirish (Alert) tizimi.

## 🛠 Model va Mantiq
- **customer.credit.limit**:
  - `partner_id`: Mijoz (res.partner).
  - `credit_limit`: Mijozga berilgan maksimal qarz miqdori.
  - `total_due`: Mijozning joriy qarzi (Invoice summalari).
  - `remaining_credit`: Limitdan qolgan qoldiq summa.
- **Constraint**: Bitta mijoz uchun faqat bitta faol (active) kredit limit bo'lishi mumkin.
- **Action Confirmation**: Agar `total_due + sale.amount_total > credit_limit` bo'lsa, Odoo `ValidationError` qaytaradi.

## 🔐 Xavfsizlik (Security)
- **Accounting Manager**: Limit yaratish va tahrirlash huquqiga ega.
- **Sales User**: Faqat limitlarni ko'rish imkoniyatiga ega.
- **Record Rules**: Foydalanuvchilar o'zlariga tegishli bo'lmagan ma'lumotlarni o'zgartirishdan cheklangan.

## 📂 O'rnatish
1. Modulni `addons` papkasiga yuklang.
2. `__manifest__.py` faylida `base`, `account`, `sale_management` bog'liqliklari borligiga ishonch hosil qiling.
3. Apps menyusidan modulni o'rnating.


# Mini Sales Approval Module

Kompaniya ichki nazoratini kuchaytirish uchun 10,000$ dan yuqori bo'lgan barcha savdo buyurtmalarini tasdiqlash tizimi.

## 🚀 Asosiy Imkoniyatlar
- **Avtomatik Approval**: 10,000$ dan oshgan buyurtmalar uchun avtomatik ravishda `sale.approval.request` yozuvi yaratiladi.
- **Process Lock**: Tasdiqlanmagan approval so'rovi bor buyurtmalarni confirm qilib bo'lmaydi.
- **Auto-Confirm**: Approval so'rovi tasdiqlanganda, tegishli Sale Order avtomatik ravishda `Confirm` holatiga o'tadi.
- **Reject Reason**: Rad etish (Reject) holatida sababini yozish majburiyati.

## 🛠 Model va Workflow
- **sale.approval.request**:
  - `state`: Draft -> Submitted -> Approved/Rejected.
  - `total_amount`: Sale Order summasidan olingan compute field.
- **Override logic**: `sale.order` modelidagi `action_confirm()` metodi o'zgartirilgan. Summa limitdan oshsa, status tekshiriladi.
- **Smart Button**: Sale Order oynasida tegishli approval so'rovini ko'rish uchun maxsus tugma.

## 🔐 Xavfsizlik (Security)
- **Sales Manager**: So'rovlarni tasdiqlash (Approve) yoki rad etish (Reject) huquqi.
- **Sales User**: Faqat so'rov yaratish va statusini kuzatish huquqi.
- **Record Rules**: So'rovlarni tahrirlash faqat `draft` holatida foydalanuvchiga ruxsat etiladi.

## 📊 Holatlar (States)
- **Draft**: So'rov tayyorlanmoqda.
- **Submitted**: Menejer tasdig'iga yuborildi.
- **Approved**: Menejer ruxsat berdi (Sale Order confirm bo'ladi).
- **Rejected**: Menejer rad etdi (Sabab yozilishi shart).