from odoo import fields, models

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    coupon_applied = fields.Boolean(default=False)
    coupon_error = fields.Char()