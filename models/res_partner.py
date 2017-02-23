from openerp import models,fields, api

class DescuentoReportResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    category_id = fields.Many2one('res.partner.category', id1='partner_id', id2='category_id', string='Tags')

class descuento_report_res_partner_category(models.Model):

    _inherit = 'res.partner.category'

    max_discount = fields.Float('Descuento maximo')