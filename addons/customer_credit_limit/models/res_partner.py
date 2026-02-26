from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    # Har bir mijozni o'zining limit rekordiga bog'laymiz
    credit_limit_id = fields.One2one("customer.credit.limit", "partner_id", string="Credit Limit Record")