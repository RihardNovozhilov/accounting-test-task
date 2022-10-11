from odoo import fields, models, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    additional_image = fields.Binary(string='Additional Image')
    active_additional_image = fields.Boolean('Enable Additional Image', default=False)
