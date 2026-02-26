{
    "name": "Customer Credit Control System",
    "version": "19.0.1.0.0",  # Odoo versiyasi va modul versiyasi
    "category": "Accounting/Accounting",
    "summary": "Manage customer credit limits and block sales if exceeded",
    "description": """
Customer Credit Control System
==============================
This module allows companies to manage customer credit limits effectively.

Key Features:
-------------
* **Custom Model**: customer.credit.limit to define limits per partner.
* **Accounting Integration**: Automatically computes total due from posted unpaid invoices.
* **Sales Integration**: Real-time remaining credit calculation and validation during confirmation.
* **Security**: Role-based access (Accounting Manager vs. Sales User).
* **Constraints**: Prevents multiple active limits for the same customer.
    """,
    "author": "Komoliddin",
    "website": "https://yourwebsite.com", # Agar mavjud bo'lsa
    "depends": [
        "base", 
        "account", 
        "sale_management"  # Sale moduliga bog'liqlik majburiy
    ],
    "data": [
        "security/security_groups.xml", # Guruhlar har doim birinchi yuklanishi shart
        "security/ir.model.access.csv", # Guruhlardan keyin ruxsatlar
        "views/customer_credit_limit_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
    "license": "LGPL-3",
}