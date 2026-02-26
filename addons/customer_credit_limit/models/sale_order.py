from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    credit_limit = fields.Monetary(string="Credit Limit", compute="_compute_credit_data")
    total_due = fields.Monetary(string="Total Due", compute="_compute_credit_data")
    remaining_credit = fields.Monetary(string="Remaining Credit", compute="_compute_credit_data")
    credit_exceeded = fields.Boolean(compute="_compute_credit_data")

    @api.depends("partner_id", "amount_total")
    def _compute_credit_data(self):
        for order in self:
            limit_rec = self.env['customer.credit.limit'].search([
                ('partner_id', '=', order.partner_id.id),
                ('active', '=', True)
            ], limit=1)

            if limit_rec:
                order.credit_limit = limit_rec.credit_limit
                order.total_due = limit_rec.total_due
                
                # ASOSIY O'ZGARISH: 
                # Qolgan limit = Jami limit - (Eski qarz + Hozirgi buyurtma summasi)
                order.remaining_credit = limit_rec.credit_limit - (limit_rec.total_due + order.amount_total)
                
                # Agar qolgan limit 0 dan kichik bo'lsa, demak limit oshib ketdi
                order.credit_exceeded = order.remaining_credit < 0
            else:
                order.credit_limit = 0.0
                order.total_due = 0.0
                order.remaining_credit = 0.0
                order.credit_exceeded = False

    def action_confirm(self):
        for order in self:
            if order.credit_limit > 0 and order.credit_exceeded:
                raise ValidationError(_(
                    "DIQQAT! Kredit limiti oshib ketgan.\n"
                    "Maksimal limit: %s\n"
                    "Hozirgi qarz: %s\n"
                    "Bu buyurtma summasi: %s"
                ) % (order.credit_limit, order.total_due, order.amount_total))
        return super(SaleOrder, self).action_confirm()