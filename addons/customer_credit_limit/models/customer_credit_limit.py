# models/customer_credit_limit.py
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomerCreditLimit(models.Model):
    _name = "customer.credit.limit"
    _description = "Customer Credit Limit"
    _rec_name = "partner_id"

    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade")
    credit_limit = fields.Monetary(required=True, currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id.id
    )
    active = fields.Boolean(default=True)
    note = fields.Text()

    total_due = fields.Monetary(compute="_compute_total_due", store=True, currency_field="currency_id")
    remaining_credit = fields.Monetary(compute="_compute_remaining_credit", store=True,currency_field="currency_id")

    @api.depends("partner_id")
    def _compute_total_due(self):
        for rec in self:
            invoices = self.env["account.move"].search([
                ("partner_id", "=", rec.partner_id.id),
                ("move_type", "=", "out_invoice"),
                ("state", "=", "posted"),
                ("payment_state", "!=", "paid"),
            ])
            rec.total_due = sum(invoices.mapped("amount_residual"))

    @api.depends("credit_limit", "total_due")
    def _compute_remaining_credit(self):
        for rec in self:
            rec.remaining_credit = rec.credit_limit - rec.total_due

    @api.constrains("partner_id", "active")
    def _check_single_active_limit(self):
        for rec in self:
            if rec.active:
                count = self.search_count([
                    ("partner_id", "=", rec.partner_id.id),
                    ("active", "=", True),
                    ("id", "!=", rec.id)
                ])
                if count:
                    raise ValidationError("This customer already has an active credit limit!")