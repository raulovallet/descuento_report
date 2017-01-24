from openerp import models,fields, api


class descuento_report_res_partner_category(models.Model):

    _inherit = 'res.partner.category'

    max_discount = fields.Float('Descuento maximo')