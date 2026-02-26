# Customer Credit Control System

Ushbu Odoo moduli mijozlarning kredit limitlarini boshqarish va limit oshib ketganda sotuv buyurtmalarini avtomatik bloklash uchun mo'ljallangan.

## 🚀 Loyiha maqsadi

Kompaniya mijozlariga qarz asosida savdo qilishda xavfsizlikni ta'minlash:

* Mijozlar uchun individual kredit limitlarini belgilash.
* Buxgalteriya (Accounting) bilan integratsiya qilib, real vaqtdagi qarzdorlikni hisoblash.
* Sotuv (Sales) jarayonida limitdan oshish holatlarini bloklash.

## 🛠 Texnik imkoniyatlar

* **Custom Model**: `customer.credit.limit` modeli orqali limitlarni boshqarish.
* **Dynamic Calculation**:
* `Total Due`: To'lanmagan invoice'lar summasi.
* `Remaining Credit`: $Limit - (Eski Qarz + Yangi Buyurtma)$.


* **Role-Based Access (RBAC)**:
* `Manager`: Limitlarni yaratish, tahrirlash va o'chirish.
* `User`: Limitlarni faqat ko'rish (Read-only).


* **Validation**: Sotuv buyurtmasini tasdiqlashda `ValidationError` mexanizmi.

## 📦 O'rnatish va Run qilish

### 1. Modulni joylashtirish

Modul papkasini Odoo-ning `extra-addons` direktoriyasiga joylashtiring.

### 2. Docker muhitida ishga tushirish



```bash
docker compose up -d 
```

### 3. Odoo UI orqali faollashtirish

1. **Settings** -> **Activate Developer Mode** ni yoqing.
2. **Apps** menyusiga kiring.
3. **Update Apps List** tugmasini bosing.
4. Qidiruvga `Customer Credit Control` deb yozing va **Activate** tugmasini bosing.

## 🧪 Sinovdan o'tkazish (Testing)

1. **Security**: Foydalanuvchi sozlamalarida o'zingizga `Credit Control: Manager` huquqini bering.
2. **Limit**: Biror mijoz uchun $1,000$ limit o'rnating va `Active` qiling.
3. **Sales**: Yangi `Sale Order` yarating. Summa $1,000$ dan oshsa, tizim bloklashini tekshiring.
4. **Accounting**: Mijoz uchun invoice yarating va tasdiqlang. `Remaining Credit` avtomatik kamayishini kuzating.

---

## 🏗 Texnologiyalar

* **Odoo 19.0** (Master version)
* **Python 3.10+**
* **PostgreSQL**


---

### 💡 Eslatma:

Ushbu modul **Odoo 19** muhitida ishlab chiqilgan. Xavfsizlik guruhlari (Access Groups) versiyadagi o'zgarishlar sababli "Technical / Groups" bo'limida boshqariladi.