from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class CustomCustomerPortal(CustomerPortal):

    def _get_optional_fields(self):
        # Call original method to get base fields
        fields = super()._get_optional_fields()

        # custom fields
        custom_fields = [
            'x_studio_nome_giocatore',
            'x_studio_nome_giocatore_2',
            'x_studio_sez_squadra',
        ]

        # List fusion
        return list(set(fields + custom_fields))

class PortalCouponController(http.Controller):
    @http.route(['/my/orders/<int:order_id>/apply_coupon'], methods=["POST"], type='http', auth="user", website=True)
    def portal_apply_coupon(self, order_id, **post):
        order = request.env['sale.order'].sudo().browse(order_id)
        try:
            code = (post.get('code') or '').strip()
            coupon_applied = False
            coupon_error = False

            if order and order.state in ('draft',):  # Limita ai preventivi, togli state check per consentire anche su sale
                if code:
                    result = order._check_and_apply_coupon(code)
                    if result.get('error'):
                        coupon_error = result['error']
                    else:
                        coupon_applied = True
                else:
                    coupon_error = "Inserisci un codice sconto valido."

            # Re-renderizza la stessa pagina con messaggio
            # values = request.env['sale.order']._get_portal_order_page_view_values(order, None)
            # values.update({'coupon_applied': coupon_applied, 'coupon_error': coupon_error})
            order.write({'coupon_applied': coupon_applied, 'coupon_error': coupon_error})
            values = {
                'order': order,
                'message_partner_ids': order.partner_id.ids,
                'token': None,
                'bootstrap_formatting': True,
                'res_partner': order.partner_id,
                'report_type': 'pdf'
            }

            return request.render('sale.sale_order_portal_template', values)
            # return request.render('sale.portal_order_page', order)
            return request.redirect('/my/orders/%s' % order_id)
        except Exception as err:
            _logger.info("==============")
            _logger.info("Error to apply a coupon")
            _logger.info(str(err))
            return request.redirect('/my/orders/%s' % order_id)
