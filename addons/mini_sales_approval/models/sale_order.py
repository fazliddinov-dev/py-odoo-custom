from odoo import models, fields, api, _
from odoo.exceptions import UserError

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_count = fields.Integer(compute='_compute_approval_count', string="Approvals")

    def _compute_approval_count(self):
        for order in self:
            # count() ishlatishda model nomi to'g'riligiga e'tibor bering
            order.approval_count = self.env['sale.approval.request'].search_count([
                ('sale_order_id', '=', order.id)
            ])

    def action_confirm(self):
        if self.env.context.get('skip_approval'):
            return super(SaleOrder, self).action_confirm()

        for order in self:
            if order.amount_total > 10000:
                # 1. Avval tasdiqlangan so'rov bormi?
                approved_request = self.env['sale.approval.request'].search([
                    ('sale_order_id', '=', order.id),
                    ('state', '=', 'approved')
                ], limit=1)
                
                if not approved_request:
                    # 2. Agar yo'q bo'lsa, so'rov yaratamiz (yoki borini olamiz)
                    existing_request = self.env['sale.approval.request'].search([
                        ('sale_order_id', '=', order.id),
                        ('state', 'in', ['draft', 'submitted'])
                    ], limit=1)
                    
                    if not existing_request:
                        self.env['sale.approval.request'].create({
                            'sale_order_id': order.id,
                            'state': 'submitted',
                        })
                        # BU JUDA MUHIM: Bazaga yozishni majburlaymiz
                        self.env.cr.commit() 
                    
                    # 3. Keyin xatoni chiqaramiz
                    raise UserError(_("Sotuv summasi 10,000 dan yuqori. Tasdiqlash so'rovi yuborildi. Menejer tasdiqlashini kuting."))
        
        return super(SaleOrder, self).action_confirm()

    def action_view_approvals(self):
        self.ensure_one()
        return {
            'name': _('Approval Requests'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.approval.request',
            'view_mode': 'list,form', # Odoo 19 uchun 'list'
            'domain': [('sale_order_id', '=', self.id)],
            'context': {'default_sale_order_id': self.id},
            'target': 'current',
        }